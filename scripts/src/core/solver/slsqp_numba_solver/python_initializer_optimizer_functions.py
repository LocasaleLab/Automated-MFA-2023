from ...common.config import CoreConstants, ParamName
from ...common.packages import np, np_float_type
from ...common.functions import np_log_eps

from .common_generator_functions import common_preprocess


eps_for_log = CoreConstants.eps_for_log
entropy_loss_code = 0
squared_loss_code = 1


def emu_index_list_conv(complete_emu_data_list, emu_index_list):
    result_array = complete_emu_data_list[emu_index_list[0]]
    for input_emu_index in emu_index_list[1:]:
        input_array = complete_emu_data_list[input_emu_index]
        result_array = np.convolve(result_array, input_array, mode='full')
    return result_array


def construct_and_update_matrix(flux_vector, row_num, col_num, update_list):
    # matrix.fill(0)
    matrix = np.zeros((row_num, col_num), dtype=np_float_type)
    for (row_index, col_index, flux_value_update_list) in update_list:
        element_update_value = 0
        for (flux_index, coefficient) in flux_value_update_list:
            element_update_value += flux_vector[flux_index] * coefficient
        matrix[row_index, col_index] += element_update_value
    return matrix


def base_prediction_function(flux_vector, complete_predicted_mid_data_list, operation_list):
    for (
            carbon_num, matrix_a_dim, matrix_b_col, matrix_a_update_list, matrix_b_update_list,
            matrix_y_update_list, this_layer_matrix_x_emu_index_list) in operation_list:
        matrix_a = construct_and_update_matrix(flux_vector, matrix_a_dim, matrix_a_dim, matrix_a_update_list)
        matrix_b = construct_and_update_matrix(flux_vector, matrix_a_dim, matrix_b_col, matrix_b_update_list)

        # matrix_y.fill(0)
        matrix_y = np.zeros((matrix_b_col, carbon_num + 1))
        for row_index, emu_index_list in enumerate(matrix_y_update_list):
            # np.copyto(matrix_y[row_index], emu_index_list_conv(complete_predicted_mid_data_list, emu_index_list))
            matrix_y[row_index] = emu_index_list_conv(complete_predicted_mid_data_list, emu_index_list)

        matrix_x = np.linalg.solve(matrix_a, matrix_b @ matrix_y)
        for row, row_emu_index in zip(matrix_x, this_layer_matrix_x_emu_index_list):
            # complete_predicted_mid_data_list.append(row)
            # np.copyto(complete_predicted_mid_data_list[row_emu_index], row)
            complete_predicted_mid_data_list[row_emu_index] = row

    # return complete_predicted_mid_data_list


def mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, mix_operation_list, mix_ratio_multiplier):
    for _, current_mixed_item_index, mix_operation in mix_operation_list:
        current_mixed_vector = complete_predicted_mid_data_list[current_mixed_item_index]
        current_mixed_vector.fill(0)
        total_flux_value = 0  # New line
        for flux_index, mid_index in mix_operation:
            # updated_mid_vector = complete_predicted_mid_data_list[mid_index] * flux_vector[flux_index] / mix_ratio_multiplier
            updated_mid_vector = complete_predicted_mid_data_list[mid_index] * flux_vector[flux_index]  # New line
            total_flux_value += flux_vector[flux_index]  # New line
            current_mixed_vector += updated_mid_vector
        current_mixed_vector /= total_flux_value  # New line


def entropy_loss_func_calculation(complete_predicted_mid_data_list, loss_operation_list, optimal_cross_entropy):
    cross_entropy = -optimal_cross_entropy
    for _, predicted_mid_index, experimental_mid_data in loss_operation_list:
        cross_entropy += np_log_eps(
            experimental_mid_data, complete_predicted_mid_data_list[predicted_mid_index], eps_for_log)
    return cross_entropy


def squared_loss_func_calculation(complete_predicted_mid_data_list, loss_operation_list):
    squared_loss = 0
    for _, predicted_mid_index, experimental_mid_data, valid_index_array in loss_operation_list:
        current_predicted_mid_vector = complete_predicted_mid_data_list[predicted_mid_index]
        if len(valid_index_array) > 0:
            current_valid_predicted_mid_vector = current_predicted_mid_vector[valid_index_array]
            current_experimental_mid_normalization = np.sum(current_valid_predicted_mid_vector)
            current_loss = np.sum((
                experimental_mid_data[valid_index_array] * current_experimental_mid_normalization
                - current_valid_predicted_mid_vector
            ) ** 2)
        else:
            current_loss = np.sum((experimental_mid_data - current_predicted_mid_vector) ** 2)
        squared_loss += current_loss
        # squared_loss += np.sum((experimental_mid_data - complete_predicted_mid_data_list[predicted_mid_index]) ** 2)
    return squared_loss


def emu_value_dict_generator(complete_predicted_mid_data_list, target_emu_index_dict):
    return {emu_name: complete_predicted_mid_data_list[emu_index] for emu_name, emu_index in target_emu_index_dict.items()}


def mid_prediction(complete_predicted_mid_data_list, loss_operation_list):
    # Must copy the vector, or any following modification will change the value of vector.
    target_predicted_mid_data_dict = {
        predicted_emu_name: complete_predicted_mid_data_list[predicted_mid_index].copy()
        for predicted_emu_name, predicted_mid_index, *_ in loss_operation_list}
    return target_predicted_mid_data_dict


def all_target_metabolite_mid_prediction(
        complete_predicted_mid_data_list, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict):
    # Must copy the vector, or any following modification will change the value of vector.
    all_target_emu_value_dict = emu_value_dict_generator(complete_predicted_mid_data_list, all_target_emu_index_dict)
    predicted_all_target_mid_data_dict = {
        all_target_emu_name_metabolite_name_dict[target_emu_name]: predicted_mid_data.copy()
        for target_emu_name, predicted_mid_data in all_target_emu_value_dict.items()
    }
    return predicted_all_target_mid_data_dict


def solver_objective_func(
        flux_vector, complete_predicted_mid_data_list, operation_list,
        mix_operation_list, mix_ratio_multiplier, loss_operation_list, loss_code, optimal_cross_entropy):

    base_prediction_function(flux_vector, complete_predicted_mid_data_list, operation_list)
    mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, mix_operation_list, mix_ratio_multiplier)
    if loss_code == entropy_loss_code:
        loss = entropy_loss_func_calculation(complete_predicted_mid_data_list, loss_operation_list, optimal_cross_entropy)
    elif loss_code == squared_loss_code:
        loss = squared_loss_func_calculation(complete_predicted_mid_data_list, loss_operation_list)
    else:
        raise ValueError()
    return loss


def solver_target_mid_dict_prediction_func(
        flux_vector, complete_predicted_mid_data_list, operation_list,
        mix_operation_list, mix_ratio_multiplier, loss_operation_list, loss_code, optimal_cross_entropy):
    base_prediction_function(flux_vector, complete_predicted_mid_data_list, operation_list)
    mix_mid_data_list(
        flux_vector, complete_predicted_mid_data_list, mix_operation_list, mix_ratio_multiplier)
    target_predicted_mid_data_dict = mid_prediction(complete_predicted_mid_data_list, loss_operation_list)
    return target_predicted_mid_data_dict


def solver_all_target_metabolite_mid_prediction_func(
        flux_vector, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict,
        complete_predicted_mid_data_list, operation_list, mix_operation_list,
        mix_ratio_multiplier, loss_operation_list, loss_code, optimal_cross_entropy):
    base_prediction_function(flux_vector, complete_predicted_mid_data_list, operation_list)
    predicted_all_target_mid_data_dict = all_target_metabolite_mid_prediction(
        complete_predicted_mid_data_list, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict)
    return predicted_all_target_mid_data_dict


def solver_initializer(
        emu_mid_equation_dict, flux_name_index_dict, input_emu_data_dict,
        experimental_mid_data_obj_dict, nested_mix_equation_dict,
        all_target_metabolite_name_carbon_num_dict, loss_type, mix_ratio_multiplier):
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

    modified_loss_operation_list = []
    for (
            carbon_num, matrix_a_dim, matrix_b_col, *others) in operation_list:
        matrix_a = np.zeros((matrix_a_dim, matrix_a_dim), dtype=np_float_type)
        matrix_b = np.zeros((matrix_a_dim, matrix_b_col), dtype=np_float_type)
        matrix_y = np.zeros((matrix_b_col, carbon_num + 1), dtype=np_float_type)
        modified_loss_operation_list.append((matrix_a, matrix_b, matrix_y, *others))

    complete_predicted_mid_data_list = input_emu_data_list
    input_emu_num = len(input_emu_data_list)
    for emu_index, emu_size in sorted(complete_emu_name_index_size_dict.values(), key=lambda x: x[0]):
        if emu_index < input_emu_num:
            assert emu_size == len(complete_predicted_mid_data_list[emu_index])
        else:
            complete_predicted_mid_data_list.append(np.zeros(emu_size))

    objective_function_args = (
        complete_predicted_mid_data_list, operation_list,
        mix_operation_list, mix_ratio_multiplier, loss_operation_list, loss_code, optimal_cross_entropy)

    return objective_function_args, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict, \
        target_mid_data_dict, emu_name_experimental_name_dict


