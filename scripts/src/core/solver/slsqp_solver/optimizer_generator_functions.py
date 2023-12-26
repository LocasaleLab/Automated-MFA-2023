from ...common.config import CoreConstants, ParamName
from ...common.packages import np
from ...common.functions import full_emu_name_constructor, np_log_eps, np_list_conv

from ..solver_construction_functions.common_construct_functions import target_emu_name_list_generator, \
    all_target_emu_name_metabolite_name_dict_generator, apply_mix_equation, calculate_optimal_entropy

float_type = CoreConstants.float_type
eps_for_log = CoreConstants.eps_for_log


def emu_graph_constructor_optimized_pure_python(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict, target_emu_name_list,
        all_target_metabolite_emu_name_list):
    """

    all_emu_list = [np_array_for_EMU1, np_array_for_EMU2, ... ,]
    operation_list = [
        (carbon_num, matrix_a_dim, matrix_b_col, matrix_A_update_list, matrix_B_update_list,
        matrix_Y_update_list),
        ...]
    target_emu_index_dict = {
        target_emu_name: target_emu_index,
        ...
    }

    :param all_target_metabolite_emu_name_list:
    :param emu_mid_equation_dict:
    :param flux_name_index_dict:
    :param input_emu_data_dict:
    :param target_emu_name_list:
    :return:
    """

    def generate_updating_list_of_matrix(_matrix_flux_location_dict, _flux_name_index_dict):
        matrix_updates_list = []
        for (row_index, col_index), reaction_dict in _matrix_flux_location_dict.items():
            flux_value_update_list = []
            for reaction_id, coefficient in reaction_dict.items():
                flux_value_update_list.append((_flux_name_index_dict[reaction_id], coefficient))
            matrix_updates_list.append((row_index, col_index, flux_value_update_list))
        return matrix_updates_list

    emu_matrix_equation_carbon_num_dict = emu_mid_equation_dict
    complete_emu_name_index_size_dict = {}
    input_emu_data_list = []
    for index, (emu_name, emu_data) in enumerate(input_emu_data_dict.items()):
        complete_emu_name_index_size_dict[emu_name] = (index, len(emu_data))
        input_emu_data_list.append(emu_data)

    operation_list = []
    for carbon_num, (
            this_layer_emu_dict_list, input_and_lower_layer_emu_dict_list, matrix_a_flux_location_dict,
            matrix_b_flux_location_dict, matrix_a_dim, matrix_b_col) in emu_matrix_equation_carbon_num_dict.items():
        if len(this_layer_emu_dict_list) == 0:
            continue

        matrix_a_update_list = generate_updating_list_of_matrix(matrix_a_flux_location_dict, flux_name_index_dict)
        matrix_b_update_list = generate_updating_list_of_matrix(matrix_b_flux_location_dict, flux_name_index_dict)

        matrix_y_update_list = []
        for emu_name, input_and_lower_layer_emu in input_and_lower_layer_emu_dict_list.items():
            if isinstance(input_and_lower_layer_emu, list):
                emu_index_list = [
                    complete_emu_name_index_size_dict[emu.full_name][0] for emu in input_and_lower_layer_emu]
            else:
                emu_index_list = [complete_emu_name_index_size_dict[emu_name][0]]
            matrix_y_update_list.append(emu_index_list)

        start_index = len(complete_emu_name_index_size_dict)
        complete_emu_name_index_size_dict.update({
            emu_obj.full_name: (start_index + index, carbon_num + 1)
            for index, emu_obj in enumerate(this_layer_emu_dict_list)})

        operation_list.append(
            (carbon_num, matrix_a_dim, matrix_b_col, matrix_a_update_list, matrix_b_update_list, matrix_y_update_list))

    target_emu_index_dict = {
        target_emu_name: complete_emu_name_index_size_dict[target_emu_name][0]
        for target_emu_name in target_emu_name_list}
    all_target_emu_index_dict = {
        target_emu_name: complete_emu_name_index_size_dict[target_emu_name][0]
        for target_emu_name in all_target_metabolite_emu_name_list}

    return input_emu_data_list, operation_list, complete_emu_name_index_size_dict, target_emu_index_dict, \
        all_target_emu_index_dict


def optimized_prediction_function_generator(
        input_emu_data_list, operation_list, target_emu_index_dict, all_target_emu_index_dict):
    def base_prediction_function(flux_vector):
        def create_and_update_matrix(row_size, col_size, update_list):
            matrix = np.zeros((row_size, col_size))
            for (row_index, col_index, flux_value_update_list) in update_list:
                element_update_value = 0
                for (flux_index, coefficient) in flux_value_update_list:
                    element_update_value += flux_vector[flux_index] * coefficient
                matrix[row_index, col_index] += element_update_value
            return matrix

        complete_emu_data_list = list(input_emu_data_list)
        for (
                carbon_num, matrix_a_dim, matrix_b_col, matrix_a_update_list, matrix_b_update_list,
                matrix_y_update_list) in operation_list:
            matrix_a = create_and_update_matrix(matrix_a_dim, matrix_a_dim, matrix_a_update_list)
            matrix_b = create_and_update_matrix(matrix_a_dim, matrix_b_col, matrix_b_update_list)

            matrix_y_list = []
            for emu_index_list in matrix_y_update_list:
                # if isinstance(emu_index_list, list):
                #     matrix_y_list.append(np_list_conv([complete_emu_data_list[index] for index in emu_index_list]))
                # else:
                #     matrix_y_list.append(complete_emu_data_list[emu_index_list])
                matrix_y_list.append(np_list_conv([complete_emu_data_list[index] for index in emu_index_list]))
            matrix_y = np.array(matrix_y_list)

            matrix_x = np.linalg.solve(matrix_a, matrix_b @ matrix_y)
            for row in matrix_x:
                complete_emu_data_list.append(row)

        return complete_emu_data_list

    def optimized_prediction_function(flux_vector):
        complete_emu_data_list = base_prediction_function(flux_vector)
        target_emu_value_dict = {
            emu_name: complete_emu_data_list[emu_index] for emu_name, emu_index in target_emu_index_dict.items()}
        return target_emu_value_dict

    def optimized_all_metabolite_prediction_function(flux_vector):
        complete_emu_data_list = base_prediction_function(flux_vector)
        all_target_emu_value_dict = {
            emu_name: complete_emu_data_list[emu_index] for emu_name, emu_index in all_target_emu_index_dict.items()}
        return all_target_emu_value_dict

    return optimized_prediction_function, optimized_all_metabolite_prediction_function


def loss_and_mix_operation_list_generator(
        loss_operation_list, mix_operation_list, target_emu_name_list, nested_mix_equation_dict,
        experimental_mid_data_obj_dict, flux_name_index_dict):
    target_mid_data_dict = {}
    # target_emu_experimental_data_name_dict = {}
    emu_name_experimental_name_dict = {}
    experimental_mid_data_vector_list = []
    new_emu_index_dict = {target_emu_name: (index, None) for index, target_emu_name in enumerate(target_emu_name_list)}
    for experimental_mid_data_name, mix_equation in nested_mix_equation_dict.items():
        current_experimental_mid_data_obj = experimental_mid_data_obj_dict[experimental_mid_data_name]
        emu_name, emu_index, _ = apply_mix_equation(
            mix_equation, mix_operation_list, new_emu_index_dict, current_experimental_mid_data_obj.carbon_num,
            1, flux_name_index_dict)
        current_experimental_mid_data_vector = current_experimental_mid_data_obj.data_vector
        loss_operation_list.append((emu_name, emu_index, current_experimental_mid_data_vector))
        target_mid_data_dict[emu_name] = current_experimental_mid_data_vector
        # target_emu_experimental_data_name_dict[emu_name] = current_experimental_mid_data_obj.name
        emu_name_experimental_name_dict[emu_name] = current_experimental_mid_data_obj.name
        experimental_mid_data_vector_list.append(current_experimental_mid_data_vector)
    optimal_cross_entropy = calculate_optimal_entropy(experimental_mid_data_vector_list, eps_for_log)
    return optimal_cross_entropy, target_mid_data_dict, emu_name_experimental_name_dict


def optimized_function_with_loss_generator_pure_python(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict,
        experimental_mid_data_obj_dict, nested_mix_equation_dict, mix_ratio_multiplier,
        all_target_metabolite_name_carbon_num_dict, loss_type):

    def predicted_mid_data_list_generator(flux_vector):
        target_emu_value_dict = prediction_func(flux_vector)
        predicted_mid_data_list = list(target_emu_value_dict.values())
        for *_, mix_operation in mix_operation_list:
            new_mid_vector = None
            total_flux_value = 0  # New line
            for flux_index, mid_index in mix_operation:
                updated_mid_vector = predicted_mid_data_list[mid_index] * flux_vector[flux_index]  # New line
                total_flux_value += flux_vector[flux_index]  # New line
                if new_mid_vector is None:
                    new_mid_vector = updated_mid_vector
                else:
                    new_mid_vector += updated_mid_vector
            predicted_mid_data_list.append(new_mid_vector / total_flux_value)  # New line
        return predicted_mid_data_list

    def entropy_loss_func_calculation(flux_vector):
        predicted_mid_data_list = predicted_mid_data_list_generator(flux_vector)
        cross_entropy = -optimal_cross_entropy
        for _, predicted_mid_index, experimental_mid_data in loss_operation_list:
            cross_entropy += np_log_eps(
                experimental_mid_data, predicted_mid_data_list[predicted_mid_index], eps_for_log)
        return cross_entropy

    def squared_loss_func_calculation(flux_vector):
        predicted_mid_data_list = predicted_mid_data_list_generator(flux_vector)
        squared_loss = 0
        for _, predicted_mid_index, experimental_mid_data in loss_operation_list:
            squared_loss += np.sum((experimental_mid_data - predicted_mid_data_list[predicted_mid_index]) ** 2)
        return squared_loss

    def mid_prediction(flux_vector):
        predicted_mid_data_list = predicted_mid_data_list_generator(flux_vector)
        predicted_mid_data_dict = {
            predicted_emu_name: predicted_mid_data_list[predicted_mid_index]
            for predicted_emu_name, predicted_mid_index, _ in loss_operation_list}
        return predicted_mid_data_dict

    def all_target_metabolite_mid_prediction(flux_vector):
        all_target_emu_value_dict = all_target_metabolite_prediction_func(flux_vector)
        predicted_all_target_mid_data_dict = {
            all_target_emu_name_metabolite_name_dict[target_emu_name]: predicted_mid_data
            for target_emu_name, predicted_mid_data in all_target_emu_value_dict.items()
        }
        return predicted_all_target_mid_data_dict

    # target_emu_name_list = []
    # for experimental_mid_data_name, mix_equation in nested_mix_equation_dict.items():
    #     current_experimental_mid_data_obj = experimental_mid_data_obj_dict[experimental_mid_data_name]
    #     collect_target_emu_list(mix_equation, target_emu_name_list, current_experimental_mid_data_obj.carbon_num)
    target_emu_name_list = target_emu_name_list_generator(
        nested_mix_equation_dict, experimental_mid_data_obj_dict)
    all_target_emu_name_metabolite_name_dict = all_target_emu_name_metabolite_name_dict_generator(
        all_target_metabolite_name_carbon_num_dict)
    all_target_metabolite_emu_name_list = list(all_target_emu_name_metabolite_name_dict.keys())

    mix_operation_list = []
    loss_operation_list = []

    (
        input_emu_data_list, operation_list, complete_emu_name_index_size_dict, target_emu_index_dict,
        all_target_emu_index_dict) = emu_graph_constructor_optimized_pure_python(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict, target_emu_name_list,
        all_target_metabolite_emu_name_list)
    prediction_func, all_target_metabolite_prediction_func = optimized_prediction_function_generator(
        input_emu_data_list, operation_list, target_emu_index_dict, all_target_emu_index_dict)

    (
        optimal_cross_entropy, target_mid_data_dict, emu_name_experimental_name_dict
    ) = loss_and_mix_operation_list_generator(
        loss_operation_list, mix_operation_list, target_emu_name_list, nested_mix_equation_dict,
        experimental_mid_data_obj_dict, flux_name_index_dict)

    loss_function = None
    if loss_type == ParamName.cross_entropy_loss:
        loss_function = entropy_loss_func_calculation
    elif loss_type == ParamName.mean_squared_loss:
        loss_function = squared_loss_func_calculation
    else:
        raise ValueError()

    return loss_function, mid_prediction, all_target_metabolite_mid_prediction, \
        target_mid_data_dict, emu_name_experimental_name_dict


def combined_function_generator_pure_python(
        loss_func_calculation_func_dict, mid_prediction_func_dict, all_target_metabolite_mid_prediction_func_dict,
        target_mid_data_nested_dict, emu_name_experimental_name_nested_dict, ratio_dict_to_objective_func,
        list_of_case_name):
    def combined_loss_func_calculation(flux_vector):
        combined_cross_entropy = 0
        for loss_func_calculation_func, ratio_to_objective_func in loss_func_ratio_pair_list:
            combined_cross_entropy += ratio_to_objective_func * loss_func_calculation_func(flux_vector)
        return combined_cross_entropy

    def combined_mid_prediction(flux_vector):
        predicted_mid_data_dict = {}
        for case_name, mid_prediction_func in mid_prediction_func_dict.items():
            current_predicted_dict = mid_prediction_func(flux_vector)
            for emu_name, mid_value in current_predicted_dict.items():
                predicted_mid_data_dict['{}_{}'.format(case_name, emu_name)] = mid_value
        return predicted_mid_data_dict

    def combined_all_target_metabolite_mid_prediction(flux_vector):
        predicted_all_target_mid_data_dict = {}
        for case_name, all_target_mid_prediction_func in all_target_metabolite_mid_prediction_func_dict.items():
            current_all_target_predicted_dict = all_target_mid_prediction_func(flux_vector)
            for metabolite_name, mid_value in current_all_target_predicted_dict.items():
                predicted_all_target_mid_data_dict['{}_{}'.format(case_name, metabolite_name)] = mid_value
        return predicted_all_target_mid_data_dict

    loss_func_ratio_pair_list = [
        (loss_func_calculation_func_dict[case_name], ratio_dict_to_objective_func[case_name])
        for case_name in list_of_case_name]
    combined_target_mid_data_dict = {}
    combined_emu_name_experimental_name_dict = {}
    for case_name in list_of_case_name:
        for emu_name, mid_value in target_mid_data_nested_dict[case_name].items():
            combined_target_mid_data_dict['{}_{}'.format(case_name, emu_name)] = mid_value
        for emu_name, experimental_name in emu_name_experimental_name_nested_dict[case_name].items():
            combined_emu_name_experimental_name_dict['{}_{}'.format(case_name, emu_name)] = '{}_{}'.format(
                case_name, experimental_name)

    return combined_loss_func_calculation, combined_mid_prediction, combined_all_target_metabolite_mid_prediction,\
        combined_target_mid_data_dict, combined_emu_name_experimental_name_dict

