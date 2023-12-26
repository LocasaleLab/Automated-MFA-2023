from scripts.src.core.model.model_constructor import common_model_constructor
from scripts.src.core.solver.solver_construction_functions.solver_constructor import common_solver_constructor

from scripts.model.model_loader import model_loader

from ..common.result_output_functions import solver_output
from ..common.config import net_flux_list

from . import config
from .config import Direct
from .sensitivity_config import RunningMode, Keywords, DataSetting, ExperimentName, model_data_config_dict, \
    averaged_solution_data_obj, squared_loss_data_dict
from .model_pattern_generation import model_processor
from .data_leave_out_generation import data_loader
from .boundary_condition_generation import boundary_condition_processor, base_slsqp_mfa_config
from .result_processing_functions import result_label_generator, result_information_generator, CurrentFinalResult, \
    data_sensitivity_result_process, raw_model_result_process, raw_model_optimization_from_averaged_solution_result_process, \
    raw_model_batched_simulated_data_result_process
from ..common_parallel_solver.common_parallel_solver import common_solver


def load_averaged_solutions(
        model_label, data_label, config_label, optimization_from_averaged_solutions_parameter_dict):
    optimized_size = optimization_from_averaged_solutions_parameter_dict[Keywords.optimized_size]
    selection_size = optimization_from_averaged_solutions_parameter_dict[Keywords.selection_size]
    if selection_size > optimized_size:
        return []
    else:
        if data_label.startswith(DataSetting.all_data_batch.value):
            data_label = DataSetting.all_data_batch
        elif data_label.startswith(DataSetting.raw_data_batch.value):
            data_label = DataSetting.raw_data_batch
        if config_label.startswith(Keywords.squared_loss):
            data_label = squared_loss_data_dict[data_label]
        averaged_solution_matrix = averaged_solution_data_obj.return_averaged_flux_solutions(
            data_label, optimized_size, selection_size)
        return averaged_solution_matrix


def materials_preparation(
        raw_model, model_process_type, data_process_list, mfa_data_obj_generation, mfa_config_type):
    modified_data_dict, data_information_dict, common_or_dict_simulated_flux_value_dict = data_loader(data_process_list)
    # The common_or_dict_simulated_flux_value_dict will be nested dict only if the data type is batched_simulated_data.
    # In this case, the model and config will be the raw setting.
    mfa_data_dict = {}
    for data_label, current_experimental_mid_data_obj_dict in modified_data_dict.items():
        mfa_data_dict[data_label] = mfa_data_obj_generation(current_experimental_mid_data_obj_dict)
    complete_defined_model = model_loader(raw_model)
    (
        modified_defined_model_dict, model_information_dict, important_flux_list,
        important_flux_replace_dict) = model_processor(
        model_process_type, complete_defined_model, common_or_dict_simulated_flux_value_dict)
    mfa_model_dict = {}
    for model_label, current_defined_model in modified_defined_model_dict.items():
        mfa_model_dict[model_label] = common_model_constructor(current_defined_model)
    mfa_config_dict, config_information_dict = boundary_condition_processor(
        mfa_config_type, common_or_dict_simulated_flux_value_dict)

    new_common_or_dict_simulated_flux_value_dict = {}
    parameter_label_content_dict = {}
    for model_label, mfa_model in mfa_model_dict.items():
        for data_label, mfa_data in mfa_data_dict.items():
            for config_label, mfa_config in mfa_config_dict.items():
                result_label = result_label_generator(model_label, data_label, config_label)
                result_information = result_information_generator(
                    model_information_dict[model_label], data_information_dict[data_label],
                    config_information_dict[config_label])
                other_information_dict = {}
                parameter_label_content_dict[result_label] = (
                    (model_label, data_label, config_label), (mfa_model, mfa_data, mfa_config),
                    result_information, other_information_dict
                )
                if (
                        data_label in common_or_dict_simulated_flux_value_dict and
                        result_label not in new_common_or_dict_simulated_flux_value_dict):
                    new_common_or_dict_simulated_flux_value_dict[result_label] = (
                        common_or_dict_simulated_flux_value_dict)[data_label]
    if len(new_common_or_dict_simulated_flux_value_dict) != 0:
        common_or_dict_simulated_flux_value_dict = new_common_or_dict_simulated_flux_value_dict
    return parameter_label_content_dict, important_flux_list, important_flux_replace_dict, \
        common_or_dict_simulated_flux_value_dict


def solver_dict_constructor(parameter_label_content_dict):
    target_solver_dict = {}
    final_information_dict = {}
    same_model_dict = {}
    same_data_dict = {}
    previous_model = None
    previous_data = None
    for result_label, (
            (model_label, data_label, config_label), (mfa_model, mfa_data, mfa_config),
            result_information, other_information_dict) in parameter_label_content_dict.items():
        current_solver_obj = common_solver_constructor(
            mfa_model, mfa_data, mfa_config, name=result_label, verbose=False)
        target_solver_dict[result_label] = current_solver_obj
        final_information_dict[result_label] = result_information
        if model_label != previous_model:
            same_model_dict[result_label] = False
            previous_model = model_label
            same_data_dict[result_label] = False
            previous_data = data_label
        else:
            same_model_dict[result_label] = True
            if data_label != previous_data:
                previous_data = data_label
                same_data_dict[result_label] = False
            else:
                same_data_dict[result_label] = True
    return target_solver_dict, final_information_dict, same_model_dict, same_data_dict


def model_data_sensitivity_result_display(
        target_solver_dict, final_information_dict, final_result_obj,
        result_process_name, important_flux_list, important_flux_replace_dict, base_mfa_config, loss_percentile,
        common_or_dict_simulated_flux_value_dict, each_case_target_optimization_num):
    # final_result_obj.repair_predicted_mid_dict_and_merge(target_solver_dict)
    # exit()
    print(f'Result processing for {final_result_obj.result_name}...')

    other_parameter_dict = {}
    if result_process_name == Keywords.normal_result_process:
        result_process_func = data_sensitivity_result_process
        other_parameter_list = [
            important_flux_list, important_flux_replace_dict, net_flux_list, loss_percentile,
            common_or_dict_simulated_flux_value_dict]
    elif result_process_name in {
            Keywords.raw_model_result_process, Keywords.raw_model_averaged_optimization_result_process,
            Keywords.raw_model_batched_simulated_data_result_process,
            Keywords.raw_model_batched_simulated_data_averaged_optimization_result_process}:
        if result_process_name == Keywords.raw_model_result_process:
            result_process_func = raw_model_result_process
        elif result_process_name == Keywords.raw_model_averaged_optimization_result_process:
            result_process_func = raw_model_optimization_from_averaged_solution_result_process
        elif result_process_name == Keywords.raw_model_batched_simulated_data_result_process:
            result_process_func = raw_model_batched_simulated_data_result_process
        elif result_process_name == Keywords.raw_model_batched_simulated_data_averaged_optimization_result_process:
            result_process_func = raw_model_batched_simulated_data_result_process
            other_parameter_dict.update({
                'optimization_from_averaged_solutions': True
            })
        else:
            raise ValueError()
        other_parameter_list = [
            important_flux_list, important_flux_replace_dict, base_mfa_config, net_flux_list,
            common_or_dict_simulated_flux_value_dict]
    else:
        raise ValueError()
    final_result_obj.final_process(
        target_solver_dict, final_information_dict, result_process_name, result_process_func,
        each_case_target_optimization_num, *other_parameter_list, **other_parameter_dict)


def model_data_sensitivity_common_dispatcher(
        raw_model, model_process_type, data_process_list, mfa_config_type,
        mfa_data_obj_generation, experiment_name, parallel_num, test_mode, running_mode):
    (
        each_case_target_optimization_num, parallel_parameter_dict, result_process_name,
        loss_percentile) = config.running_settings(test_mode, experiment_name)
    if parallel_parameter_dict is not None and parallel_num is not None:
        parallel_parameter_dict[Keywords.processes_num] = parallel_num
    final_result_obj = CurrentFinalResult(
        Direct.output_direct, Direct.common_data_direct, experiment_name)
    (
        parameter_label_content_dict, important_flux_list, important_flux_replace_dict,
        common_or_dict_simulated_flux_value_dict) = materials_preparation(
        raw_model, model_process_type, data_process_list, mfa_data_obj_generation, mfa_config_type)
    if running_mode == RunningMode.flux_analysis:
        common_solver(
            parameter_label_content_dict, test_mode, final_result_obj, each_case_target_optimization_num,
            config.report_interval, parallel_parameter_dict, config.load_previous_results,
            predefined_initial_solution_matrix_loader=load_averaged_solutions)
    else:
        target_solver_dict, final_information_dict, same_model_dict, same_data_dict = solver_dict_constructor(
            parameter_label_content_dict)

        # final_result_obj.repair_predicted_mid_dict(target_solver_dict, result_process_name)
        # exit()

        if running_mode == RunningMode.solver_output:
            solver_output(
                target_solver_dict, final_information_dict, final_result_obj, same_model_dict, same_data_dict)
        elif running_mode == RunningMode.result_process:
            model_data_sensitivity_result_display(
                target_solver_dict, final_information_dict, final_result_obj,
                result_process_name, important_flux_list, important_flux_replace_dict, base_slsqp_mfa_config,
                loss_percentile, common_or_dict_simulated_flux_value_dict, each_case_target_optimization_num)
        else:
            raise ValueError()


def model_data_sensitivity(running_mode, experiment_name, test_mode, parallel_num):
    if experiment_name is None:
        experiment_name = config.current_experiment_name
    target_model_data_config = model_data_config_dict[experiment_name]
    model_process_type = target_model_data_config[Keywords.model]
    data_process_list = target_model_data_config[Keywords.data]
    if Keywords.config not in target_model_data_config:
        mfa_config_type = Keywords.raw_type
    else:
        mfa_config_type = target_model_data_config[Keywords.config]
    raw_model = config.raw_model
    model_data_sensitivity_common_dispatcher(
        raw_model, model_process_type, data_process_list, mfa_config_type, config.mfa_data_obj_generation,
        experiment_name, parallel_num, test_mode, running_mode)

