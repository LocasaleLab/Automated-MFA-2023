from ...common.packages import np
from ...common.config import CoreConstants, ParamName, ModelKeyword
from ...common.functions import remove_numerical_error, natural_dist, isdigit, full_emu_name_constructor, \
    mix_flux_name_constructor, tissue_specific_name_constructor, compartmental_mid_name_constructor, np_log_eps, \
    check_if_subsequence


def data_verification(
        experimental_mid_data_obj_dict, bare_metabolite_dim_dict, model_metabolite_to_standard_name_dict):
    standard_name_to_model_name_dict = {value: key for key, value in model_metabolite_to_standard_name_dict.items()}
    for metabolite_experimental_name, metabolite_mid_data_obj in experimental_mid_data_obj_dict.items():
        if metabolite_experimental_name not in standard_name_to_model_name_dict:
            continue
        current_model_name = standard_name_to_model_name_dict[metabolite_experimental_name]
        current_metabolite_dim = metabolite_mid_data_obj.carbon_num
        if current_model_name not in bare_metabolite_dim_dict:
            continue
        model_metabolite_dim = bare_metabolite_dim_dict[current_model_name]
        if current_metabolite_dim != model_metabolite_dim:
            raise ValueError(
                'Dimension of metabolite in experimental data {} is {}, '
                'which is not equal to that metabolite {} ({}) in model!'.format(
                    metabolite_experimental_name, current_metabolite_dim, current_model_name, model_metabolite_dim))


def input_emu_mid_generator(
        input_metabolite_dict, input_emu_dict):
    input_emu_data_dict = {}
    any_of_emu_mapped = False
    for input_emu in input_emu_dict.values():
        current_metabolite_name = input_emu.metabolite_name
        if current_metabolite_name in input_metabolite_dict:
            input_metabolite_obj = input_metabolite_dict[current_metabolite_name]
            input_emu_data_dict[input_emu.full_name] = input_metabolite_obj.generate_mid_vector(
                input_emu.selected_carbon_list)
            any_of_emu_mapped = True
        else:
            carbon_num = input_emu.emu_carbon_num
            input_emu_data_dict[input_emu.full_name] = natural_dist(carbon_num)
    if not any_of_emu_mapped:
        raise ValueError('At least one input EMU should be mapped to input_metabolite_dict')
    return input_emu_data_dict


def mix_ratio_balance_constraint_constructor(mix_ratio_balance_list, flux_name_index_dict, mix_ratio_multiplier):
    total_flux_size = len(flux_name_index_dict)
    mix_ratio_balance_matrix_list = []
    mix_ratio_balance_right_side_list = []
    for mix_ratio_balance in mix_ratio_balance_list:
        current_mix_ratio_balance_vector = np.zeros(total_flux_size)
        for mix_ratio_name in mix_ratio_balance:
            current_mix_ratio_balance_vector[flux_name_index_dict[mix_ratio_name]] = 1
        mix_ratio_balance_matrix_list.append(current_mix_ratio_balance_vector)
        mix_ratio_balance_right_side_list.append(mix_ratio_multiplier)
    return mix_ratio_balance_matrix_list, mix_ratio_balance_right_side_list


def mixing_equation_constructor(
        experimental_mid_data_obj_dict, model_target_metabolite_compartment_dict,
        model_metabolite_to_standard_name_dict, metabolite_bare_metabolite_name_dict,
        specific_flux_range_dict, common_mix_ratio_range, mix_ratio_multiplier, list_of_case_name=None):
    """
    Experimental metabolite: one metabolite that can be distinguished by mass spec. eg. 3PG/2PG
    Elemental metabolite: one metabolite that for a whole cell. eg. oxaloacetate
    Compartmental metabolite: one metabolite in each compartment. eg. OAC_m

    Compartment mixing: OAC_m + OAC_c -> OAC
    Experimental mixing: 3PG + 2PG -> 3PG/2PG

    If some element metabolite does not exist, just jump it.

    :param mix_ratio_multiplier:
    :param common_mix_ratio_range:
    :param specific_flux_range_dict:
    :param experimental_mid_data_obj_dict:
    :param mixed_compartment_list:
    :param model_target_metabolite_compartment_dict:
    :param model_metabolite_to_standard_name_dict:
    :return:
    """

    def data_mixing_equation_dict_generator(_experimental_mid_data_obj_dict):
        _data_mixing_equation_dict = {}
        for experimental_metabolite_name, experimental_mid_data in _experimental_mid_data_obj_dict.items():
            if experimental_mid_data.excluded_from_mfa:
                continue
            nested_metabolite_compartment_list = []
            if experimental_mid_data.combined:
                standard_name_list = experimental_mid_data.combined_standard_name_list
            else:
                standard_name_list = [experimental_mid_data.name]
            for elemental_standard_name in standard_name_list:
                current_tissue_elemental_name_list = []
                for tissue_name in experimental_mid_data.tissue:
                    current_compartmental_elemental_name_list = []
                    tissue_specific_elemental_standard_name = tissue_specific_name_constructor(
                        elemental_standard_name, tissue_name)
                    for compartment_name in experimental_mid_data.compartment:
                        tissue_specific_elemental_complete_name = compartmental_mid_name_constructor(
                            tissue_specific_elemental_standard_name, compartment_name)
                        if tissue_specific_elemental_complete_name in model_mixing_equation_dict:
                            current_compartmental_elemental_name_list.append((
                                tissue_specific_elemental_complete_name,
                                model_mixing_equation_dict[tissue_specific_elemental_complete_name]))
                            # elemental_to_experimental_metabolite_dict_from_data[elemental_complete_name] = \
                            #     experimental_metabolite_name
                    if len(current_compartmental_elemental_name_list) != 0:
                        current_tissue_elemental_name_list.append((
                            tissue_specific_elemental_standard_name, current_compartmental_elemental_name_list))
                if len(current_tissue_elemental_name_list) != 0:
                    nested_metabolite_compartment_list.append((
                        tissue_specific_name_constructor(elemental_standard_name, experimental_mid_data.tissue),
                        current_tissue_elemental_name_list))
            if len(nested_metabolite_compartment_list) != 0:
                _data_mixing_equation_dict[experimental_metabolite_name] = \
                    nested_metabolite_compartment_list
        return _data_mixing_equation_dict

    def check_if_new_balance_tuple_exist(new_balance_tuple, _mix_ratio_balance_dict):
        subseq_bool = False
        reverse = False
        target_item = None
        for exist_balance_tuple in _mix_ratio_balance_dict.keys():
            subseq_bool, reverse = check_if_subsequence(new_balance_tuple, exist_balance_tuple)
            if subseq_bool:
                target_item = exist_balance_tuple
                break
        return subseq_bool, reverse, target_item

    def analyze_nested_dependence(_data_mixing_list, _metabolite_name):
        if _data_mixing_list is None:
            return _metabolite_name
        returned_obj_list = []
        for new_metabolite_name, new_nested_obj in _data_mixing_list:
            returned_obj_list.append(analyze_nested_dependence(new_nested_obj, new_metabolite_name))
        if len(returned_obj_list) == 1:
            return returned_obj_list[0]
        else:
            result_dict = {}
            new_balance_list = []
            for index, returned_metabolite in enumerate(returned_obj_list):
                mix_ratio_name = mix_flux_name_constructor(_metabolite_name, index)
                result_dict[mix_ratio_name] = returned_metabolite
                new_balance_list.append(mix_ratio_name)
                if mix_ratio_name not in mix_ratio_name_index_dict:
                    mix_ratio_name_index_dict[mix_ratio_name] = len(mix_ratio_name_index_dict)
            new_balance_tuple = tuple(sorted(new_balance_list))
            if new_balance_tuple not in mix_ratio_balance_dict:
                new_balance_exist, replace, target_item = check_if_new_balance_tuple_exist(
                    new_balance_tuple, mix_ratio_balance_dict)
                if not new_balance_exist:
                    mix_ratio_balance_dict[new_balance_tuple] = None
                elif new_balance_exist and replace:
                    del mix_ratio_balance_dict[target_item]
                    mix_ratio_balance_dict[new_balance_tuple] = None
            return result_dict

    def nested_mix_equation_dict_generator(_data_mixing_equation_dict):
        _nested_mix_equation_dict = {}
        for experimental_metabolite_name, data_mixing_list in _data_mixing_equation_dict.items():
            if experimental_metabolite_name not in _nested_mix_equation_dict:
                _nested_mix_equation_dict[experimental_metabolite_name] = analyze_nested_dependence(
                    data_mixing_list, experimental_metabolite_name)
        return _nested_mix_equation_dict

    model_mixing_equation_dict = {}
    for tissue_name, each_tissue_metabolite_compartment_dict in model_target_metabolite_compartment_dict.items():
        for compartment_name, model_target_metabolite_set in each_tissue_metabolite_compartment_dict.items():
            for model_metabolite_name in model_target_metabolite_set:
                bared_metabolite_name = metabolite_bare_metabolite_name_dict[model_metabolite_name]
                standard_metabolite_name = model_metabolite_to_standard_name_dict[bared_metabolite_name]
                tissue_specific_elemental_complete_name = compartmental_mid_name_constructor(
                    tissue_specific_name_constructor(standard_metabolite_name, tissue_name),
                    compartment_name)
                if tissue_specific_elemental_complete_name not in model_mixing_equation_dict:
                    model_mixing_equation_dict[tissue_specific_elemental_complete_name] = []
                model_mixing_equation_dict[tissue_specific_elemental_complete_name].append(
                    (model_metabolite_name, None))

    # Mapping from experimental_metabolite_name to model_metabolite_name
    # {'experimental_metabolite1': {
    #     'MIX:exp_1': 'elemental_metabolite1',
    #     'MIX:exp_2': {   # 'elemental_metabolite2'
    #         'MIX_ele1': 'compartmental_metabolite1',
    #         'MIX_ele2': 'compartmental_metabolite2'}
    #     }
    #  'experimental_metabolite2': ...
    # }
    mix_ratio_balance_dict = {}
    mix_ratio_name_index_dict = {}
    if list_of_case_name is not None:
        nested_mix_equation_dict = {}
        for case_name in list_of_case_name:
            data_mixing_equation_dict = data_mixing_equation_dict_generator(experimental_mid_data_obj_dict[case_name])
            nested_mix_equation_dict[case_name] = nested_mix_equation_dict_generator(data_mixing_equation_dict)
    else:
        data_mixing_equation_dict = data_mixing_equation_dict_generator(experimental_mid_data_obj_dict)
        nested_mix_equation_dict = nested_mix_equation_dict_generator(data_mixing_equation_dict)
    mix_ratio_balance_list = list(mix_ratio_balance_dict.keys())

    if common_mix_ratio_range is None:
        common_mix_ratio_range = (0, 1)
    mix_range = (common_mix_ratio_range[0] * mix_ratio_multiplier, common_mix_ratio_range[1] * mix_ratio_multiplier)
    updated_specific_flux_range_dict = dict(specific_flux_range_dict)
    for current_mix_ratio_name in mix_ratio_name_index_dict.keys():
        updated_specific_flux_range_dict[current_mix_ratio_name] = mix_range
    return nested_mix_equation_dict, mix_ratio_name_index_dict, mix_ratio_balance_list, \
        updated_specific_flux_range_dict


def flux_balance_horizontal_extend(raw_flux_balance_matrix, mix_ratio_num):
    flux_balance_matrix = np.hstack(
        [raw_flux_balance_matrix, np.zeros((raw_flux_balance_matrix.shape[0], mix_ratio_num))])
    return flux_balance_matrix


def constant_flux_matrix_generator(constant_flux_matrix_array_list, constant_flux_name, flux_name_index_dict):
    new_balance_array = np.zeros(len(flux_name_index_dict))
    flux_index = flux_name_index_dict[constant_flux_name]
    new_balance_array[flux_index] = 1
    constant_flux_matrix_array_list.append(new_balance_array)


def constant_flux_constraint_list_constructor(
        dynamic_constant_flux_name_list, preset_constant_flux_value_dict, flux_name_index_dict):
    constant_flux_multiply_array_list = []
    constant_flux_right_side_list = []
    for constant_flux_name in dynamic_constant_flux_name_list:
        constant_flux_matrix_generator(constant_flux_multiply_array_list, constant_flux_name, flux_name_index_dict)
        constant_flux_right_side_list.append(constant_flux_name)
    for constant_flux_name, constant_flux_value in preset_constant_flux_value_dict.items():
        constant_flux_matrix_generator(constant_flux_multiply_array_list, constant_flux_name, flux_name_index_dict)
        constant_flux_right_side_list.append(constant_flux_value)
    return constant_flux_multiply_array_list, constant_flux_right_side_list


# Suppose constraint: Ax = b
# Projection matrix: P = I - A.T @ (A @ A.T)^-1 @ A
def matrix_and_right_side_combine_and_projection_matrix(
        flux_balance_matrix, constant_flux_matrix_list, mix_ratio_balance_matrix_list,
        flux_balance_right_side_vector, constant_flux_right_side_list, mix_ratio_right_side_list,
        eps_for_computation):
    total_matrix_list = list(flux_balance_matrix)
    total_matrix_list.extend(constant_flux_matrix_list)
    total_matrix_list.extend(mix_ratio_balance_matrix_list)

    complete_right_side_list = list(flux_balance_right_side_vector)
    complete_right_side_list.extend(constant_flux_right_side_list)
    complete_right_side_list.extend(mix_ratio_right_side_list)

    complete_flux_constraint_matrix = np.concatenate([total_matrix_list])
    final_dim = complete_flux_constraint_matrix.shape[1]
    projection_matrix = np.identity(final_dim) - complete_flux_constraint_matrix.T @ np.linalg.inv(
        complete_flux_constraint_matrix @ complete_flux_constraint_matrix.T) @ complete_flux_constraint_matrix
    remove_numerical_error(projection_matrix, eps_for_computation)
    return complete_flux_constraint_matrix, projection_matrix, complete_right_side_list


def flux_bounds_constructor(
        common_flux_range, composite_reaction_dict, specific_flux_range_dict, flux_name_index_dict):
    common_min_value, common_max_value = common_flux_range
    new_specific_flux_range_dict = dict(specific_flux_range_dict)
    for reaction_id, composite_reaction_obj in composite_reaction_dict.items():
        if reaction_id in specific_flux_range_dict:
            final_range = specific_flux_range_dict[reaction_id]
        else:
            if composite_reaction_obj.flux_range == ModelKeyword.normal_range_type:
                continue
            elif composite_reaction_obj.flux_range == ModelKeyword.add_range_type:
                final_range = [0, 0]
                for composite_node_obj in composite_reaction_obj.compose_list:
                    if composite_node_obj.reaction_id in specific_flux_range_dict:
                        current_composite_range = specific_flux_range_dict[composite_node_obj.reaction_id]
                    else:
                        current_composite_range = common_flux_range
                    if not isinstance(current_composite_range, np.ndarray):
                        current_composite_range = np.array(current_composite_range)
                    current_composite_range_with_coefficient = current_composite_range * composite_node_obj.coefficient
                    final_range[0] += np.min(current_composite_range_with_coefficient)
                    final_range[1] += np.max(current_composite_range_with_coefficient)
                final_range = tuple(final_range)
            elif composite_reaction_obj.flux_range == ModelKeyword.no_range_type:
                final_range = (
                    -CoreConstants.maximal_unconstrained_flux_value, CoreConstants.maximal_unconstrained_flux_value)
            elif composite_reaction_obj.flux_range == ModelKeyword.specific_range_type:
                final_range = composite_reaction_obj.specific_range
            else:
                raise ValueError('Cannot recognize!')
            if final_range[1] - final_range[0] < 1e-3:
                raise ValueError(f'Invalid range {final_range} of composite reaction {reaction_id} ')
        new_specific_flux_range_dict[reaction_id] = final_range
    total_flux_num = len(flux_name_index_dict)
    if len(new_specific_flux_range_dict) == 0:
        min_bound_vector = np.ones(total_flux_num) * common_min_value
        max_bound_vector = np.ones(total_flux_num) * common_max_value
    else:
        min_bound_vector = np.zeros(total_flux_num)
        max_bound_vector = np.zeros(total_flux_num)
        for flux_name, flux_index in flux_name_index_dict.items():
            if flux_name not in new_specific_flux_range_dict:
                min_bound_vector[flux_index] = common_min_value
                max_bound_vector[flux_index] = common_max_value
            else:
                min_bound_vector[flux_index], max_bound_vector[flux_index] = new_specific_flux_range_dict[flux_name]
    return min_bound_vector, max_bound_vector


def right_side_array_constructor(
        complete_right_side_list, dynamic_default_value=0):
    dynamic_constraint_index_dict = {}
    complete_right_side_array_list = []
    for item_index, right_side_item in enumerate(complete_right_side_list):
        if isdigit(right_side_item):
            complete_right_side_array_list.append(right_side_item)
        elif isinstance(right_side_item, str):
            complete_right_side_array_list.append(dynamic_default_value)
            dynamic_constraint_index_dict[right_side_item] = item_index
        else:
            raise ValueError('Not recognized type in right side list: {}'.format(right_side_item))
    complete_right_side_array = np.array(complete_right_side_array_list)
    return complete_right_side_array, dynamic_constraint_index_dict


def target_emu_name_list_generator(nested_mix_equation_dict, experimental_mid_data_obj_dict):
    def collect_target_emu_list(current_mix_equation_dict, _target_emu_name_list, current_carbon_num=None):
        if isinstance(current_mix_equation_dict, dict):
            for child_mix_equation_dict in current_mix_equation_dict.values():
                collect_target_emu_list(child_mix_equation_dict, _target_emu_name_list, current_carbon_num)
        else:
            current_name = full_emu_name_constructor(current_mix_equation_dict, current_carbon_num)
            _target_emu_name_list.append(current_name)

    target_emu_name_list = []
    for experimental_mid_data_name, mix_equation in nested_mix_equation_dict.items():
        current_experimental_mid_data_obj = experimental_mid_data_obj_dict[experimental_mid_data_name]
        collect_target_emu_list(mix_equation, target_emu_name_list, current_experimental_mid_data_obj.carbon_num)
    return target_emu_name_list


def all_target_emu_name_metabolite_name_dict_generator(all_target_metabolite_name_carbon_num_dict):
    all_target_emu_name_metabolite_name_dict = {}
    for target_metabolite_name, metabolite_carbon_num in all_target_metabolite_name_carbon_num_dict.items():
        current_name = full_emu_name_constructor(target_metabolite_name, metabolite_carbon_num)
        all_target_emu_name_metabolite_name_dict[current_name] = target_metabolite_name
    return all_target_emu_name_metabolite_name_dict


def apply_mix_equation(
        current_mix_equation_dict, mix_operation_list, emu_name_index_size_dict, current_carbon_num,
        batch_size, flux_name_index_dict):
    if isinstance(current_mix_equation_dict, dict):
        current_substrate_list = []
        current_item_name_list = []
        for mix_ratio_name, child_mix_equation_dict in current_mix_equation_dict.items():
            child_item_name, child_item_index, _ = apply_mix_equation(
                child_mix_equation_dict, mix_operation_list, emu_name_index_size_dict, current_carbon_num,
                batch_size, flux_name_index_dict)
            current_item_name_list.append(child_item_name)
            current_substrate_list.append(
                (flux_name_index_dict[mix_ratio_name], child_item_index))
        current_item_name = '+'.join(current_item_name_list)
        if current_item_name not in emu_name_index_size_dict:
            emu_name_index_size_dict[current_item_name] = (len(emu_name_index_size_dict), current_carbon_num + 1)
        current_result_index = emu_name_index_size_dict[current_item_name][0]
        mix_operation_list.append(((batch_size, current_carbon_num + 1), current_result_index, current_substrate_list))
    else:
        current_item_name = full_emu_name_constructor(current_mix_equation_dict, current_carbon_num)
        # if current_item_name not in emu_name_index_size_dict:
        #     emu_name_index_size_dict[current_item_name] = (len(emu_name_index_size_dict), current_carbon_num + 1)
    return current_item_name, emu_name_index_size_dict[current_item_name][0], current_carbon_num + 1


def calculate_optimal_entropy(exp_data_np_vector_list, eps_for_log=CoreConstants.eps_for_log):
    optimal_cross_entropy = 0
    for current_exp_data_vector in exp_data_np_vector_list:
        if current_exp_data_vector is None:
            raise ValueError('Experimental data vector is None!')
        optimal_cross_entropy += np_log_eps(
            current_exp_data_vector, current_exp_data_vector, eps_for_log)
        if np.isnan(optimal_cross_entropy):
            raise ValueError('Optimal cross entropy is not a number!')
    return optimal_cross_entropy


def constraint_loss_operation_constructor(
        penalty_coefficient_dict, flux_constraint_tensor=None,
        flux_constraint_right_side_tensor=None, min_flux_expanded_tensor=None, max_flux_expanded_tensor=None,
        flux_identity_tensor=None):
    constraint_loss_operation_list = [
        (0, penalty_coefficient_dict[ParamName.mid_loss])]
    if flux_constraint_tensor is not None or flux_constraint_right_side_tensor is not None:
        constraint_loss_operation_list.append((
            1, penalty_coefficient_dict[ParamName.flux_constraint_loss],
            flux_constraint_tensor, flux_constraint_right_side_tensor))
    if min_flux_expanded_tensor is not None or max_flux_expanded_tensor is not None:
        larger_or_equal_bound = min_flux_expanded_tensor
        smaller_or_equal_bound = max_flux_expanded_tensor
        constraint_loss_operation_list.append((
            2, penalty_coefficient_dict[ParamName.inequality_loss], flux_identity_tensor,
            larger_or_equal_bound, smaller_or_equal_bound))

    return constraint_loss_operation_list


def constraint_matrix_verification_and_simplification(constraint_matrix, right_side_array, computation_eps):
    raw_constraint_num, variable_num = constraint_matrix.shape
    _, flux_constraint_matrix_r = np.linalg.qr(constraint_matrix.T)
    flux_constraint_matrix_l = flux_constraint_matrix_r.T
    redundant_row_list = []
    for row_index, row_array in enumerate(flux_constraint_matrix_l):
        if np.abs(row_array[row_index]) < computation_eps:
            redundant_row_list.append(row_index)
    redundant_row_num = len(redundant_row_list)
    real_constraint_num = raw_constraint_num - redundant_row_num
    if real_constraint_num >= variable_num:
        raise ValueError(f'Constraint number {real_constraint_num} is larger than variable number {variable_num}')
    if redundant_row_num > 0:
        valid_constraint_list = []
        valid_right_side_list = []
        last_valid_constraint = 0
        for redundant_row_index in redundant_row_list:
            valid_constraint_list.extend(constraint_matrix[last_valid_constraint:redundant_row_index])
            valid_right_side_list.extend(right_side_array[last_valid_constraint:redundant_row_index])
            """
            Construct a linear system P = [A', b'] including all previous valid constraints and 
            current redundant row index. If P is not full-rank, than the redundant row is incompatible. 
            Otherwise, this row is redundant and can be deleted.
            """
            valid_constraint_num = len(valid_constraint_list)
            updated_right_side_array = np.array(
                [*valid_right_side_list, right_side_array[redundant_row_index]]).reshape(-1, 1)
            new_linear_system_matrix = np.hstack([
                [*valid_constraint_list, constraint_matrix[redundant_row_index]],
                updated_right_side_array])
            rank = np.linalg.matrix_rank(new_linear_system_matrix, tol=computation_eps)
            if rank < valid_constraint_num - 1:
                raise ValueError('Some redundant rows already exist!')
            elif rank == valid_constraint_num:
                raise ValueError('Current redundant row is incompatible!')
        valid_constraint_num = len(valid_constraint_list)
        valid_constraint_matrix = np.array(valid_constraint_list)
        valid_right_side_array = np.array(valid_right_side_list)
    else:
        valid_constraint_num = raw_constraint_num
        valid_constraint_matrix = constraint_matrix
        valid_right_side_array = right_side_array
    return valid_constraint_matrix, valid_right_side_array, valid_constraint_num


def inequality_bound_matrix_simplification(
        raw_flux_coefficient_matrix, transform_matrix, valid_constraint_num,
        min_flux_vector, max_flux_vector, computation_eps):
    """
    Each row of flux_coefficient_matrix corresponds to constrains of one flux.
    If two rows have the same coefficient, the corresponding two fluxes will be identical all the time.
    One of them can be removed, and the exact bound could be the larger one in min bound, and smaller one in max bound
    """
    def indexing_key_generator(current_array):
        round_decimal_num = 10
        decimal_format_string = f'{{:.{round_decimal_num}e}}'
        indexing_str = ';'.join([
            '0' if abs(current_num) < computation_eps else decimal_format_string.format(current_num)
            for current_num in current_array
        ])
        return indexing_str

    def check_if_exist_and_update_min_max_bound(coefficient_array, new_min_value, new_max_value):
        indexing_str = indexing_key_generator(coefficient_array)
        if indexing_str not in existing_coefficient_dict:
            existing_coefficient_dict[indexing_str] = (new_min_value, new_max_value)
            existence = False
        else:
            current_min_value, current_max_value = existing_coefficient_dict[indexing_str]
            existing_coefficient_dict[indexing_str] = (
                max(current_min_value, new_min_value),
                min(current_max_value, new_max_value)
            )
            existence = True
        return existence, indexing_str

    eps = 1e-12
    transformed_flux_coefficient_matrix = (raw_flux_coefficient_matrix @ transform_matrix)[:, valid_constraint_num:]
    final_row_list = []
    final_indexing_str_list = []
    final_min_bound_list = []
    final_max_bound_list = []
    existing_coefficient_dict = {}
    for row_index, each_row_array in enumerate(transformed_flux_coefficient_matrix):
        if sum(abs(each_row_array)) < eps:
            continue
        existence, indexing_str = check_if_exist_and_update_min_max_bound(
            each_row_array, min_flux_vector[row_index], max_flux_vector[row_index])
        if not existence:
            final_row_list.append(row_index)
            final_indexing_str_list.append(indexing_str)
    for indexing_str in final_indexing_str_list:
        min_value, max_value = existing_coefficient_dict[indexing_str]
        final_min_bound_list.append(min_value)
        final_max_bound_list.append(max_value)
    valid_bound_coefficient_matrix = raw_flux_coefficient_matrix[final_row_list, :]
    valid_min_bound_vector = np.array(final_min_bound_list)
    valid_max_bound_vector = np.array(final_max_bound_list)
    assert np.linalg.matrix_rank(valid_bound_coefficient_matrix, eps) == valid_bound_coefficient_matrix.shape[0]
    return valid_bound_coefficient_matrix, valid_min_bound_vector, valid_max_bound_vector
