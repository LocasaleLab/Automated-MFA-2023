from ...common.config import CoreConstants, ParamName
from ...common.packages import np, np_float_type, np_int_type
from ...common.numba_packages import numba_jit, numba_jit_mode, nb_list

from .common_generator_functions import common_preprocess

eps_for_log = CoreConstants.eps_for_log
entropy_loss_code = 0
squared_loss_code = 1


@numba_jit(numba_jit_mode)
def np_log_eps(experimental_vector, predicted_vector, eps):
    return -np.sum((experimental_vector + eps) * np.log(predicted_vector + eps))


@numba_jit(numba_jit_mode)
def emu_index_list_conv(complete_emu_data_list, emu_index_array):
    result_array = complete_emu_data_list[emu_index_array[0]]
    for input_emu_index in emu_index_array[1:]:
        input_array = complete_emu_data_list[input_emu_index]
        result_array = np.convolve(result_array, input_array)
    return result_array


@numba_jit(numba_jit_mode)
def update_matrix(
        flux_vector, target_matrix, location_pair_tuple, flux_index_array_list, coefficient_nested_list):
    target_matrix.fill(0)
    for location_pair_index, location_pair in enumerate(location_pair_tuple):
        flux_index_array = flux_index_array_list[location_pair_index]
        coefficient_array = coefficient_nested_list[location_pair_index]
        element_update_value = 0.0
        # Vectorization will slow down this process
        for flux_index_index, flux_index in enumerate(flux_index_array):
            element_update_value += flux_vector[flux_index] * coefficient_array[flux_index_index]
        target_matrix[location_pair] += element_update_value


@numba_jit(numba_jit_mode)
def one_layer_prediction(
        complete_predicted_mid_data_list, flux_vector,
        matrix_a, location_pair_tuple_a, flux_index_array_list_a, coefficient_array_list_a,
        matrix_b, location_pair_tuple_b, flux_index_array_list_b, coefficient_array_list_b,
        matrix_y, emu_index_array_list, matrix_x_emu_index_list):
    update_matrix(
        flux_vector, matrix_a, location_pair_tuple_a, flux_index_array_list_a, coefficient_array_list_a)
    update_matrix(
        flux_vector, matrix_b, location_pair_tuple_b, flux_index_array_list_b, coefficient_array_list_b)

    matrix_y.fill(0)
    for row_index, emu_index_array in enumerate(emu_index_array_list):
        matrix_y[row_index] = emu_index_list_conv(complete_predicted_mid_data_list, emu_index_array)

    matrix_x = np.linalg.solve(matrix_a, matrix_b @ matrix_y)
    # numba solve function will produce F-contiguous array
    for row_index, row in enumerate(matrix_x):
        complete_predicted_mid_data_list[matrix_x_emu_index_list[row_index]][:] = row


@numba_jit(numba_jit_mode)
def base_prediction_function(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list):
    total_iter_num = len(matrix_a_tuple)
    for iter_index in range(total_iter_num):
        one_layer_prediction(
            complete_predicted_mid_data_list, flux_vector,
            matrix_a_tuple[iter_index], location_pair_nested_tuple_a[iter_index],
            flux_index_nested_array_list_a[iter_index], coefficient_nested_array_list_a[iter_index],
            matrix_b_tuple[iter_index], location_pair_nested_tuple_b[iter_index],
            flux_index_nested_array_list_b[iter_index], coefficient_nested_array_list_b[iter_index],
            matrix_y_tuple[iter_index], emu_index_nested_array_list[iter_index],
            matrix_x_emu_index_nested_list[iter_index])


@numba_jit(numba_jit_mode)
def mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, modified_mix_operation_list,
        mixed_item_index_tuple, mix_ratio_multiplier):
    if len(mixed_item_index_tuple) == 0:
        # This clause must be added to prevent class inspection on mixed_item_index_tuple.
        # Class inspection will raise error if mixed_item_index_tuple is empty.
        return
    for mix_operation_index, mix_operation_pair_list in enumerate(modified_mix_operation_list):
        current_mixed_item_vector = complete_predicted_mid_data_list[mixed_item_index_tuple[mix_operation_index]]
        current_mixed_item_vector.fill(0)
        total_flux_value = 0  # New line
        # TODO: repaired but not tested
        for mix_operation_pair in mix_operation_pair_list:
            flux_index = mix_operation_pair[0]
            mid_index = mix_operation_pair[1]
            # mixed_mid_vector = complete_predicted_mid_data_list[mid_index] * flux_vector[flux_index] / mix_ratio_multiplier
            mixed_mid_vector = complete_predicted_mid_data_list[mid_index] * flux_vector[flux_index]  # New line
            total_flux_value += flux_vector[flux_index]  # New line
            current_mixed_item_vector += mixed_mid_vector
        current_mixed_item_vector /= total_flux_value  # New line


@numba_jit(numba_jit_mode)
def entropy_loss_func_calculation(
        complete_predicted_mid_data_list, predicted_mid_index_tuple, experimental_mid_data_tuple, optimal_cross_entropy):
    cross_entropy = -optimal_cross_entropy
    for index, predicted_mid_index in enumerate(predicted_mid_index_tuple):
        cross_entropy += np_log_eps(
            experimental_mid_data_tuple[index], complete_predicted_mid_data_list[predicted_mid_index], eps_for_log)
    return cross_entropy


@numba_jit(numba_jit_mode)
def squared_loss_func_calculation(
        complete_predicted_mid_data_list, predicted_mid_index_tuple, experimental_mid_data_tuple):
    squared_loss = 0
    for index, predicted_mid_index in enumerate(predicted_mid_index_tuple):
        squared_loss += np.sum(
            (experimental_mid_data_tuple[index] - complete_predicted_mid_data_list[predicted_mid_index]) ** 2)
    return squared_loss


def emu_value_dict_generator(complete_predicted_mid_data_list, target_emu_index_dict):
    return {
        emu_name: complete_predicted_mid_data_list[emu_index]
        for emu_name, emu_index in target_emu_index_dict.items()}


def mid_prediction(complete_predicted_mid_data_list, predicted_emu_name_tuple, predicted_mid_index_tuple):
    target_predicted_mid_data_dict = {
        predicted_emu_name: complete_predicted_mid_data_list[predicted_mid_index].copy()
        for predicted_emu_name, predicted_mid_index in zip(predicted_emu_name_tuple, predicted_mid_index_tuple)}
    return target_predicted_mid_data_dict


def all_target_metabolite_mid_prediction(
        complete_predicted_mid_data_list, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict):
    all_target_emu_value_dict = emu_value_dict_generator(complete_predicted_mid_data_list, all_target_emu_index_dict)
    predicted_all_target_mid_data_dict = {
        all_target_emu_name_metabolite_name_dict[target_emu_name]: predicted_mid_data.copy()
        for target_emu_name, predicted_mid_data in all_target_emu_value_dict.items()
    }
    return predicted_all_target_mid_data_dict


@numba_jit(numba_jit_mode)
def solver_objective_func(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list,
        modified_mix_operation_list, mixed_item_index_tuple,
        mix_ratio_multiplier, predicted_emu_name_tuple, predicted_mid_index_tuple, experimental_mid_data_tuple,
        loss_code, optimal_cross_entropy):
    base_prediction_function(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list)
    mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, modified_mix_operation_list,
        mixed_item_index_tuple, mix_ratio_multiplier)
    if loss_code == entropy_loss_code:
        loss = entropy_loss_func_calculation(
            complete_predicted_mid_data_list, predicted_mid_index_tuple, experimental_mid_data_tuple,
            optimal_cross_entropy)
    elif loss_code == squared_loss_code:
        loss = squared_loss_func_calculation(
            complete_predicted_mid_data_list, predicted_mid_index_tuple, experimental_mid_data_tuple)
    else:
        raise ValueError()
    return loss


def solver_target_mid_dict_prediction_func(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list,
        modified_mix_operation_list, mixed_item_index_tuple,
        mix_ratio_multiplier, predicted_emu_name_tuple, predicted_mid_index_tuple, 
        experimental_mid_data_tuple, loss_code, optimal_cross_entropy):
    base_prediction_function(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list)
    mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, modified_mix_operation_list,
        mixed_item_index_tuple, mix_ratio_multiplier)
    target_predicted_mid_data_dict = mid_prediction(
        complete_predicted_mid_data_list, predicted_emu_name_tuple, predicted_mid_index_tuple)
    return target_predicted_mid_data_dict


def solver_all_target_metabolite_mid_prediction_func(
        flux_vector, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict,
        complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list,
        modified_mix_operation_list, mixed_item_index_tuple,
        mix_ratio_multiplier, predicted_emu_name_tuple, predicted_mid_index_tuple, experimental_mid_data_tuple,
        loss_code, optimal_cross_entropy):
    base_prediction_function(
        flux_vector, complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list)
    predicted_all_target_mid_data_dict = all_target_metabolite_mid_prediction(
        complete_predicted_mid_data_list, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict)
    return predicted_all_target_mid_data_dict


def solver_initializer(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict,
        experimental_mid_data_obj_dict, nested_mix_equation_dict,
        all_target_metabolite_name_carbon_num_dict, loss_type, mix_ratio_multiplier):
    def construct_update_list_for_each_matrix(
            matrix_row_col_tuple, matrix_update_list, matrix_list, location_pair_nested_list,
            flux_index_nested_list, coefficient_nested_list):
        matrix_list.append(np.zeros(matrix_row_col_tuple, dtype=np_float_type))
        current_layer_location_pair_list = nb_list()
        current_layer_flux_index_list = nb_list()
        current_layer_coefficient_list = nb_list()
        for row_index, col_index, flux_value_update_list in matrix_update_list:
            current_layer_location_pair_list.append((row_index, col_index))
            current_location_flux_index_list = []
            current_location_coefficient_list = []
            for flux_index, coefficient in flux_value_update_list:
                current_location_flux_index_list.append(flux_index)
                current_location_coefficient_list.append(coefficient)
            current_layer_flux_index_list.append(np.array(current_location_flux_index_list, dtype=np_int_type))
            current_layer_coefficient_list.append(np.array(current_location_coefficient_list, dtype=np_float_type))
        location_pair_nested_list.append(current_layer_location_pair_list)
        flux_index_nested_list.append(current_layer_flux_index_list)
        coefficient_nested_list.append(current_layer_coefficient_list)

    (
        input_emu_data_list, operation_list, mix_operation_list, loss_operation_list,
        complete_emu_name_index_size_dict, target_emu_index_dict, optimal_cross_entropy,
        all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict, target_mid_data_dict,
        emu_name_experimental_name_dict) = common_preprocess(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict, experimental_mid_data_obj_dict,
        nested_mix_equation_dict, all_target_metabolite_name_carbon_num_dict)

    if loss_type == ParamName.cross_entropy_loss:
        loss_code = entropy_loss_code
    elif loss_type == ParamName.mean_squared_loss:
        loss_code = squared_loss_code
    else:
        raise ValueError()

    complete_predicted_mid_data_list = nb_list(input_emu_data_list)
    input_emu_num = len(input_emu_data_list)
    for emu_index, emu_size in sorted(complete_emu_name_index_size_dict.values(), key=lambda x: x[0]):
        if emu_index < input_emu_num:
            assert emu_size == len(complete_predicted_mid_data_list[emu_index])
        else:
            complete_predicted_mid_data_list.append(np.zeros(emu_size))

    complete_loss_operation_list = tuple(zip(*loss_operation_list))
    predicted_emu_name_tuple = complete_loss_operation_list[0]
    predicted_mid_index_tuple = complete_loss_operation_list[1]
    experimental_mid_data_tuple = complete_loss_operation_list[2]

    # modified_mix_operation_list = nb_list()
    modified_mix_operation_list = nb_list([nb_list([(0, 0)])])
    modified_mix_operation_list.pop()
    mixed_item_index_list = []
    for _, current_mixed_item_index, mix_operation in mix_operation_list:
        current_mix_operation_list = nb_list()
        for flux_index, mid_index in mix_operation:
            current_mix_operation_list.append((flux_index, mid_index))
        modified_mix_operation_list.append(current_mix_operation_list)
        mixed_item_index_list.append(current_mixed_item_index)
    mixed_item_index_tuple = tuple(mixed_item_index_list)

    matrix_a_list = []
    matrix_b_list = []
    location_pair_nested_list_a = []
    location_pair_nested_list_b = []
    flux_index_nested_array_list_a = nb_list()
    flux_index_nested_array_list_b = nb_list()
    coefficient_nested_array_list_a = nb_list()
    coefficient_nested_array_list_b = nb_list()
    matrix_x_emu_index_nested_list = nb_list()
    matrix_y_list = []
    emu_index_nested_array_list = nb_list()
    for (
            carbon_num, matrix_a_dim, matrix_b_col, matrix_a_update_list, matrix_b_update_list,
            matrix_y_update_list, this_layer_matrix_x_emu_index_list) in operation_list:
        construct_update_list_for_each_matrix(
            (matrix_a_dim, matrix_a_dim), matrix_a_update_list, matrix_a_list, location_pair_nested_list_a,
            flux_index_nested_array_list_a, coefficient_nested_array_list_a)
        construct_update_list_for_each_matrix(
            (matrix_a_dim, matrix_b_col), matrix_b_update_list, matrix_b_list, location_pair_nested_list_b,
            flux_index_nested_array_list_b, coefficient_nested_array_list_b)

        matrix_y = np.zeros((matrix_b_col, carbon_num + 1), dtype=np_float_type)
        matrix_y_list.append(matrix_y)
        current_layer_emu_index_nested_array_list = nb_list()
        for emu_index_list in matrix_y_update_list:
            if isinstance(emu_index_list, list):
                new_array = np.array(emu_index_list)
            else:
                new_array = np.array([emu_index_list])
            current_layer_emu_index_nested_array_list.append(new_array)
        emu_index_nested_array_list.append(current_layer_emu_index_nested_array_list)
        matrix_x_emu_index_nested_list.append(nb_list(this_layer_matrix_x_emu_index_list))

    matrix_a_tuple = tuple(matrix_a_list)
    matrix_b_tuple = tuple(matrix_b_list)
    matrix_y_tuple = tuple(matrix_y_list)
    location_pair_nested_tuple_a = tuple(location_pair_nested_list_a)
    location_pair_nested_tuple_b = tuple(location_pair_nested_list_b)

    objective_function_args = (
        complete_predicted_mid_data_list,
        matrix_a_tuple, location_pair_nested_tuple_a, flux_index_nested_array_list_a, coefficient_nested_array_list_a,
        matrix_b_tuple, location_pair_nested_tuple_b, flux_index_nested_array_list_b, coefficient_nested_array_list_b,
        matrix_y_tuple, emu_index_nested_array_list, matrix_x_emu_index_nested_list,
        modified_mix_operation_list, mixed_item_index_tuple,
        mix_ratio_multiplier, predicted_emu_name_tuple, predicted_mid_index_tuple, experimental_mid_data_tuple,
        loss_code, optimal_cross_entropy)

    return objective_function_args, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict, \
        target_mid_data_dict, emu_name_experimental_name_dict


