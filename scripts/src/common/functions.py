from common_and_plotting_functions.functions import default_parameter_extract, check_and_mkdir_of_direct
from scripts.src.core.common.config import CoreConstants

from .config import np, Keywords, Direct
obj_threshold_key = Keywords.obj_threshold_key


def mid_name_process(raw_mid_name):
    emu_sep = CoreConstants.emu_carbon_list_str_sep
    modified_str_list = []
    str_start = 0
    while str_start < len(raw_mid_name):
        emu_location = raw_mid_name.find(emu_sep, str_start)
        if emu_location == -1:
            modified_str_list.append(raw_mid_name[str_start:])
            break
        modified_str_list.append(raw_mid_name[str_start:emu_location])
        new_start = emu_location + len(emu_sep)
        while new_start != len(raw_mid_name) and raw_mid_name[new_start] == '1':
            new_start += 1
        str_start = new_start
    modified_str = ''.join(modified_str_list)
    return modified_str


def tissue_name_breakdown(raw_name):
    tissue_sep = CoreConstants.specific_tissue_sep
    plus = '+'
    prefix = None
    search_start = 0
    main_body_list = []
    while True:
        sep_location = raw_name.find(tissue_sep, search_start)
        if sep_location == -1:
            break
        else:
            this_prefix = raw_name[search_start:sep_location]
            if prefix is None:
                prefix = this_prefix
            else:
                assert this_prefix == prefix
            body_start = sep_location + len(tissue_sep)
            next_plus_location = raw_name.find(plus, sep_location)
            if next_plus_location == -1:
                main_body_list.append(raw_name[body_start:])
                break
            else:
                next_search_start = next_plus_location + 1
                main_body_list.append(raw_name[body_start:next_search_start])
                search_start = next_search_start
    main_body = ''.join(main_body_list)
    return prefix, main_body


def excel_column_letter_to_0_index(raw_column_str):
    final_index = -1
    for loc_index, letter in enumerate(raw_column_str[::-1]):
        letter_index = ord(letter) - ord('A') + 1
        if not 0 <= letter_index <= 26:
            raise ValueError('Should pass letter between A to Z: {}'.format(raw_column_str))
        final_index += letter_index * (26 ** loc_index)
    return final_index


def update_parameter_object(original_parameter_object, new_parameter_object):
    for item_key, item_value in new_parameter_object.__class__.__dict__.items():
        if not item_key.startswith('__'):
            if hasattr(original_parameter_object, item_key) and isinstance(
                    getattr(original_parameter_object, item_key), dict):
                getattr(original_parameter_object, item_key).update(item_value)
            else:
                original_parameter_object.__setattr__(item_key, item_value)
    return original_parameter_object


def add_empty_obj(root_dict, final_empty_class, *args):
    current_dict = root_dict
    total_arg_num = len(args)
    for label_index, label in enumerate(args):
        if label not in current_dict:
            if label_index == total_arg_num - 1:
                current_dict[label] = final_empty_class()
            else:
                current_dict[label] = {}
        current_dict = current_dict[label]
    return current_dict


def link_flux_name(*flux_name_list):
    return '_'.join(flux_name_list)


def special_result_label_converter(raw_result_label, current_keyword, decipher=False):
    specialized_str = f'__{current_keyword}'
    if decipher:
        if not raw_result_label.endswith(specialized_str):
            raise ValueError()
        return raw_result_label[:-len(specialized_str)]
    else:
        return f'{raw_result_label}{specialized_str}'


def determine_order_by_specific_data_dict(
        standard_flux_name, specific_flux_value_dict, reference_flux_value_dict=None):
    reverse_order = False
    if reference_flux_value_dict is None:
        reference_flux_value_dict = specific_flux_value_dict
    if isinstance(standard_flux_name, str):
        specific_flux_value = specific_flux_value_dict[standard_flux_name]
        flux_title = standard_flux_name
        common_flux_name = standard_flux_name
    elif isinstance(standard_flux_name, (tuple, list)):
        flux_name0, flux_name1 = standard_flux_name
        # specific_flux_value1 = specific_flux_value_dict[flux_name0]
        # specific_flux_value2 = specific_flux_value_dict[flux_name1]
        reference_flux_value1 = reference_flux_value_dict[flux_name0]
        reference_flux_value2 = reference_flux_value_dict[flux_name1]
        if reference_flux_value1 < reference_flux_value2:
            flux_name1, flux_name0 = standard_flux_name
            reverse_order = True
        specific_flux_value = specific_flux_value_dict[flux_name0] - specific_flux_value_dict[flux_name1]
        flux_title = '{} - {}'.format(flux_name0, flux_name1)
        common_flux_name = link_flux_name(flux_name0, flux_name1)
    else:
        raise ValueError()
    return specific_flux_value, flux_title, reverse_order, common_flux_name


def net_flux_pair_dict_constructor(net_flux_list):
    net_flux_pair_dict = {}
    for flux_name0, flux_name1 in net_flux_list:
        net_flux_pair_dict[flux_name0] = (flux_name0, flux_name1)
        net_flux_pair_dict[flux_name1] = (flux_name0, flux_name1)
    return net_flux_pair_dict


def net_flux_pair_analyzer(flux_name, net_flux_pair_dict, analyzed_flux_set):
    if flux_name in net_flux_pair_dict:
        modified_flux_name = net_flux_pair_dict[flux_name]
        for one_directional_flux_name in modified_flux_name:
            analyzed_flux_set.add(one_directional_flux_name)
    else:
        modified_flux_name = flux_name
        analyzed_flux_set.add(flux_name)
    return modified_flux_name


def net_flux_matrix_generator_new(
        common_flux_name_simulated_value_dict, normal_flux_name_index_dict):
    net_matrix_list = []
    normal_core_flux_index_list = []
    total_raw_flux_num = len(normal_flux_name_index_dict)
    for formal_flux_name, (
            modified_flux_name, simulated_net_flux_value, raw_flux_title, reverse_order
    ) in common_flux_name_simulated_value_dict.items():
        new_one_hot_array = np.zeros(total_raw_flux_num)
        if isinstance(modified_flux_name, tuple):
            flux_name0, flux_name1 = modified_flux_name
            normal_flux_index0 = normal_flux_name_index_dict[flux_name0]
            normal_flux_index1 = normal_flux_name_index_dict[flux_name1]
            normal_core_flux_index_list.extend([normal_flux_index0, normal_flux_index1])
            if reverse_order:
                normal_flux_index0, normal_flux_index1 = normal_flux_index1, normal_flux_index0
            new_one_hot_array[normal_flux_index0] = 1
            new_one_hot_array[normal_flux_index1] = -1
            # if not reverse_order:
            #     flux_name0, flux_name1 = modified_flux_name
            # else:
            #     flux_name1, flux_name0 = modified_flux_name
            # new_one_hot_array[normal_flux_name_index_dict[flux_name0]] = 1
            # new_one_hot_array[normal_flux_name_index_dict[flux_name1]] = -1
        else:
            flux_name = modified_flux_name
            current_normal_flux_index = normal_flux_name_index_dict[flux_name]
            normal_core_flux_index_list.append(current_normal_flux_index)
            new_one_hot_array[current_normal_flux_index] = 1
        net_matrix_list.append(new_one_hot_array)
    normal_core_flux_index_array = np.array(normal_core_flux_index_list)
    net_flux_matrix = np.array(net_matrix_list)
    return net_flux_matrix, normal_core_flux_index_array


def analyze_simulated_flux_value_dict(
        simulated_flux_value_dict, net_flux_list, normal_flux_name_index_dict=None,
        standard_simulated_flux_value_dict=None):
    net_flux_pair_dict = net_flux_pair_dict_constructor(net_flux_list)
    common_flux_name_simulated_value_dict = {}
    if standard_simulated_flux_value_dict is None:
        standard_simulated_flux_value_dict = simulated_flux_value_dict
    # for flux_name in important_flux_list:
    analyzed_flux_set = set()
    simulated_flux_index_dict = {}
    simulated_core_flux_vector_list = []
    simulated_net_vector_flux_list = []
    formal_flux_name_list = []
    for flux_index, flux_name in enumerate(standard_simulated_flux_value_dict.keys()):
        if flux_name in analyzed_flux_set:
            continue
        if flux_name.startswith('MIX'):
            continue
        modified_flux_name = net_flux_pair_analyzer(
            flux_name, net_flux_pair_dict, analyzed_flux_set)
        if isinstance(modified_flux_name, tuple):
            simulated_core_flux_vector_list.extend(
                [standard_simulated_flux_value_dict[flux_name] for flux_name in modified_flux_name])
        else:
            simulated_core_flux_vector_list.append(standard_simulated_flux_value_dict[modified_flux_name])
        simulated_net_flux_value, raw_flux_title, reverse_order, formal_flux_name = \
            determine_order_by_specific_data_dict(
                modified_flux_name, simulated_flux_value_dict, standard_simulated_flux_value_dict)
        simulated_flux_index_dict[flux_name] = flux_index
        if formal_flux_name not in common_flux_name_simulated_value_dict:
            common_flux_name_simulated_value_dict[formal_flux_name] = (
                modified_flux_name, simulated_net_flux_value, raw_flux_title, reverse_order)
            simulated_net_vector_flux_list.append(simulated_net_flux_value)
            formal_flux_name_list.append(formal_flux_name)
    simulated_core_flux_vector = np.array(simulated_core_flux_vector_list)
    simulated_net_flux_vector = np.array(simulated_net_vector_flux_list)

    result_list = [
        common_flux_name_simulated_value_dict, simulated_core_flux_vector, simulated_net_flux_vector,
        formal_flux_name_list]
    if normal_flux_name_index_dict is not None:
        # net_flux_matrix, _, simulated_flux_vector, filtered_solution_flux_index = net_flux_matrix_generator(
        #     net_flux_list, flux_name_index_dict, simulated_flux_value_dict)
        # return common_flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, \
        #     filtered_solution_flux_index
        normal_net_flux_matrix, normal_core_flux_index_array = net_flux_matrix_generator_new(
            common_flux_name_simulated_value_dict, normal_flux_name_index_dict)
        result_list.extend([normal_net_flux_matrix, normal_core_flux_index_array])
    return result_list


def net_flux_matrix_generator(net_flux_list, flux_name_index_dict, specific_flux_value_dict):
    net_flux_name_flux_pair_dict = {}
    for flux_name0, flux_name1 in net_flux_list:
        net_flux_name_flux_pair_dict[flux_name0] = (flux_name0, flux_name1)
        net_flux_name_flux_pair_dict[flux_name1] = (flux_name0, flux_name1)
    total_raw_flux_num = len(specific_flux_value_dict)
    analyzed_flux_set = set()
    final_array_list = []
    common_flux_name_dict = {}
    for flux_name in specific_flux_value_dict.keys():
        if flux_name in analyzed_flux_set:
            continue
        new_one_hot_array = np.zeros(total_raw_flux_num)
        if flux_name in net_flux_name_flux_pair_dict:
            flux_name_pair = net_flux_name_flux_pair_dict[flux_name]
            _, _, reverse_order, common_flux_name = determine_order_by_specific_data_dict(
                flux_name_pair, specific_flux_value_dict)
            if not reverse_order:
                (flux_name0, flux_name1) = flux_name_pair
            else:
                (flux_name1, flux_name0) = flux_name_pair
            # (flux_name0, flux_name1) = flux_name_pair
            new_one_hot_array[flux_name_index_dict[flux_name0]] = 1
            new_one_hot_array[flux_name_index_dict[flux_name1]] = -1
            analyzed_flux_set.add(flux_name0)
            analyzed_flux_set.add(flux_name1)
        else:
            new_one_hot_array[flux_name_index_dict[flux_name]] = 1
            analyzed_flux_set.add(flux_name)
            common_flux_name = flux_name
        if common_flux_name not in common_flux_name_dict:
            common_flux_name_dict[common_flux_name] = None
        final_array_list.append(new_one_hot_array)
    flux_name_list = list(common_flux_name_dict.keys())

    specific_flux_vector = np.zeros(len(specific_flux_value_dict))
    filtered_solution_flux_index = np.zeros(len(specific_flux_value_dict), dtype=int)
    raw_flux_name_list = []
    for specific_flux_index, (flux_name, flux_value) in enumerate(specific_flux_value_dict.items()):
        current_index = flux_name_index_dict[flux_name]
        specific_flux_vector[specific_flux_index] = flux_value
        filtered_solution_flux_index[specific_flux_index] = current_index
        raw_flux_name_list.append(flux_name)
    return np.array(final_array_list), flux_name_list, specific_flux_vector, filtered_solution_flux_index


def calculate_raw_and_net_distance(
        flux_array, net_flux_matrix, target_core_flux_vector, vertical_net_target_flux_vector=None, reduced=True,
        core_flux_index_array=None):
    if np.ndim(flux_array) < 2:
        transformed_solution_array = flux_array.reshape([1, -1])
    else:
        transformed_solution_array = flux_array
    if core_flux_index_array is not None:
        transformed_core_solution_array = transformed_solution_array[:, core_flux_index_array]
        # target_flux_vector = target_flux_vector[core_flux_index_array]
    else:
        transformed_core_solution_array = transformed_solution_array
    final_output_list = []
    if target_core_flux_vector is not None:
        raw_diff_vector = transformed_core_solution_array - target_core_flux_vector
        raw_euclidean_distance = np.sqrt(np.sum(raw_diff_vector ** 2, axis=1))
        if len(raw_euclidean_distance) == 1:
            raw_euclidean_distance = raw_euclidean_distance[0]
        final_output_list.append(raw_euclidean_distance)
        if not reduced:
            final_output_list.append(raw_diff_vector)
    if net_flux_matrix is not None:
        if vertical_net_target_flux_vector is None:
            assert target_core_flux_vector is not None
            vertical_net_target_flux_vector = net_flux_matrix @ target_core_flux_vector.reshape([-1, 1])
        else:
            assert net_flux_matrix.shape[0] == len(vertical_net_target_flux_vector)
        net_diff_vector = (
                net_flux_matrix @ transformed_solution_array.T -
                vertical_net_target_flux_vector).T
        net_euclidean_distance = np.sqrt(np.sum(net_diff_vector ** 2, axis=1))
        if len(net_euclidean_distance) == 1:
            net_euclidean_distance = net_euclidean_distance[0]
        final_output_list.append(net_euclidean_distance)
        if not reduced:
            final_output_list.append(net_diff_vector)
    if len(final_output_list) == 1:
        final_output_list = final_output_list[0]
    return final_output_list


def data_param_list_generator_func_template(keyword_list, extra_key_default_value_dict=None):
    empty_str = ''

    def data_param_list_generator_iter_func(current_dict_list, current_index, current_complete_param_dict, final_list):
        current_keyword = keyword_list[current_index]
        for current_simplified_param_dict in current_dict_list:
            current_key = current_simplified_param_dict[current_keyword]
            new_complete_param_dict = {
                **current_complete_param_dict,
                current_keyword: current_key
            }
            if empty_str in current_simplified_param_dict:
                next_layer_dict_list = current_simplified_param_dict[empty_str]
                data_param_list_generator_iter_func(
                    next_layer_dict_list, current_index + 1, new_complete_param_dict, final_list)
            else:
                if extra_key_default_value_dict is not None:
                    for extra_key, default_value in extra_key_default_value_dict.items():
                        new_complete_param_dict[extra_key] = default_parameter_extract(
                            current_simplified_param_dict, extra_key, default_value)
                new_complete_param_dict[Keywords.miscellaneous] = {}
                for other_key, value in current_simplified_param_dict.items():
                    if (other_key not in new_complete_param_dict) or (
                            extra_key_default_value_dict is not None and other_key in extra_key_default_value_dict):
                        new_complete_param_dict[Keywords.miscellaneous][other_key] = value
                # if obj_threshold:
                #     new_complete_param_dict[obj_threshold_key] = default_parameter_extract(
                #         current_simplified_param_dict, obj_threshold_key, None)
                final_list.append(new_complete_param_dict)

    def data_param_list_generator(param_raw_list):
        data_param_list = []
        data_param_list_generator_iter_func(
            param_raw_list, 0, {}, data_param_list)
        return data_param_list

    return data_param_list_generator


def collect_results_func_template(
        project_name_generator, total_param_list, project_parameter_key_list, obj_threshold=False,
        different_final_data_obj=None):
    def collect_results(final_data_obj):
        final_mapping_dict = {}
        for param_dict in total_param_list:
            project_parameter_tuple = tuple(param_dict[key] for key in project_parameter_key_list)
            project_name = project_name_generator(*project_parameter_tuple)
            if project_name not in final_mapping_dict:
                final_mapping_dict[project_name] = project_parameter_tuple
            if different_final_data_obj is not None:
                different_final_data_obj.load_current_result_label(project_name)
                final_data_obj.share_data(different_final_data_obj)
            else:
                final_data_obj.load_current_result_label(project_name)
            if obj_threshold:
                final_data_obj.final_information_dict[project_name][obj_threshold_key] = default_parameter_extract(
                    param_dict, obj_threshold_key, None)
        return final_mapping_dict

    return collect_results


def simulated_output_file_name_constructor(index: int = None, with_noise=False, batched_data=False, with_glns_m=False):
    output_py_direct = Direct.simulated_output_py_file_direct
    output_xlsx_direct = Direct.simulated_output_xlsx_file_direct
    output_pickle_direct = Direct.simulated_output_pickle_direct
    if batched_data:
        base_name = Keywords.batched_simulated_base_name
    elif with_glns_m:
        base_name = Keywords.normal_simulated_base_name_with_glns_m
    else:
        base_name = Keywords.normal_simulated_base_name
    if index is not None:
        index_str = f'_{index}'
    else:
        index_str = ''
    if with_noise:
        noise_str = Keywords.simulated_noise_str
    else:
        noise_str = ''
    check_and_mkdir_of_direct(output_py_direct)
    check_and_mkdir_of_direct(output_xlsx_direct)
    check_and_mkdir_of_direct(output_pickle_direct)
    output_py_file_path = f'{output_py_direct}/{base_name}{index_str}{noise_str}.py'
    output_xlsx_file_path = f'{output_xlsx_direct}/{base_name}{index_str}{noise_str}.xlsx'
    output_pickle_file_path = f'{output_pickle_direct}/{base_name}{noise_str}'
    return output_py_file_path, output_xlsx_file_path, output_pickle_file_path

