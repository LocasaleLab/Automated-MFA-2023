from ...common.functions import group_emu_name_constructor


def solver_objective_func_generator(
        single_solver_objective_func, ratio_list_to_objective_func):
    def solver_objective_func(flux_vector, *objective_function_args_list):
        total_loss = 0
        for ratio_to_objective_func, objective_function_args in zip(
                ratio_list_to_objective_func, objective_function_args_list):
            total_loss += ratio_to_objective_func * single_solver_objective_func(
                flux_vector, *objective_function_args)
        return total_loss
    return solver_objective_func


def solver_target_mid_dict_prediction_func_generator(
        single_solver_target_mid_dict_prediction_func, case_name_list):
    def solver_target_mid_dict_prediction_func(flux_vector, *objective_function_args_list):
        predicted_mid_data_dict = {}
        for case_name, objective_function_args in zip(case_name_list, objective_function_args_list):
            current_predicted_dict = single_solver_target_mid_dict_prediction_func(
                flux_vector, *objective_function_args)
            for emu_name, mid_value in current_predicted_dict.items():
                predicted_mid_data_dict[group_emu_name_constructor(emu_name, case_name)] = mid_value
        return predicted_mid_data_dict
    return solver_target_mid_dict_prediction_func


def solver_all_target_metabolite_mid_prediction_func_generator(
        single_solver_all_target_metabolite_mid_prediction_func, case_name_list):
    def solver_all_target_metabolite_mid_prediction_func(
            flux_vector, all_target_emu_index_dict_list, all_target_emu_name_metabolite_name_dict_list,
            *objective_function_args_list):
        predicted_all_target_mid_data_dict = {}
        for (
                case_name, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict, objective_function_args
        ) in zip(
                case_name_list, all_target_emu_index_dict_list, all_target_emu_name_metabolite_name_dict_list,
                objective_function_args_list):
            current_all_target_predicted_dict = single_solver_all_target_metabolite_mid_prediction_func(
                flux_vector, all_target_emu_index_dict, all_target_emu_name_metabolite_name_dict,
                *objective_function_args)
            for metabolite_name, mid_value in current_all_target_predicted_dict.items():
                predicted_all_target_mid_data_dict[group_emu_name_constructor(metabolite_name, case_name)] = mid_value
        return predicted_all_target_mid_data_dict
    return solver_all_target_metabolite_mid_prediction_func

