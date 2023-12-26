from scripts.src.common.config import Direct as CommonDirect, Keywords
from scripts.src.core.common.config import ParamName

from ...data.simulated_data import simulated_flux_vector_and_mid_data_with_noise, simulated_flux_vector_and_mid_data
from ...data.simulated_data.simulated_data_loader import mfa_data_obj_generation
from scripts.model.model_loader import ModelList

from .sensitivity_config import RunningMode, ExperimentName, Keywords, \
    return_analyzed_set_and_selected_min_loss_set, complete_optimization_selection_parameters_dict_generator


class Direct(object):
    name = 'model_data_sensitivity'
    output_direct = f'{CommonDirect.output_direct}/{name}'
    common_data_direct = f'{CommonDirect.common_submitted_raw_data_direct}/{name}'

    raw_model_approximation_percentile = 'raw_model_approximation_percentile'


running_mode = RunningMode.flux_analysis
# running_mode = RunningMode.result_process
load_previous_results = True

# current_experiment_name = ExperimentName.raw_model_raw_data
current_experiment_name = ExperimentName.raw_model_all_data
# current_experiment_name = ExperimentName.prune_branches_all_data
# current_experiment_name = ExperimentName.merge_reversible_reaction_all_data
# current_experiment_name = ExperimentName.different_constant_flux
# current_experiment_name = ExperimentName.data_sensitivity
# current_experiment_name = ExperimentName.data_sensitivity_with_noise
# current_experiment_name = ExperimentName.different_flux_range
# current_experiment_name = ExperimentName.different_constant_flux_with_noise
# current_experiment_name = ExperimentName.different_flux_range
# current_experiment_name = ExperimentName.different_flux_range_all_data
# current_experiment_name = ExperimentName.different_constant_flux_all_data
# current_experiment_name = ExperimentName.optimization_from_raw_data_average_solutions
# current_experiment_name = ExperimentName.optimization_from_all_data_average_solutions
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_raw_data
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_all_data
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_raw_data_average_solutions
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_all_data_average_solutions
# current_experiment_name = ExperimentName.raw_model_raw_data_with_squared_loss
# current_experiment_name = ExperimentName.raw_model_all_data_with_squared_loss
# current_experiment_name = ExperimentName.optimization_from_raw_data_average_solutions_with_squared_loss
# current_experiment_name = ExperimentName.optimization_from_all_data_average_solutions_with_squared_loss
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_raw_data_with_squared_loss
# current_experiment_name = ExperimentName.optimization_from_batched_simulated_all_data_with_squared_loss

report_interval = 50
# repeat_time_each_analyzed_set = 30

analysis_solver = ParamName.slsqp_numba_python_solver
# analysis_solver = ParamName.slsqp_numba_nopython_solver
# analysis_solver = ParamName.slsqp_solver

test_raw_model_analysis = True
analyzed_set_size_list, selected_min_loss_size_list = return_analyzed_set_and_selected_min_loss_set(
    test_raw_model_analysis, current_experiment_name)
if test_raw_model_analysis:
    repeat_time_each_analyzed_set = 10
else:
    repeat_time_each_analyzed_set = 30

average_solution_optimization_selection_parameters_dict = complete_optimization_selection_parameters_dict_generator(
    analyzed_set_size_list, selected_min_loss_size_list)
(
    batched_simulated_analyzed_set_size_list, batched_simulated_selected_min_loss_size_list
) = return_analyzed_set_and_selected_min_loss_set(True, current_experiment_name)
batched_simulated_repeat_time_each_analyzed_set = 1
data_sensitivity_simulated_analyzed_set_size_list = [50000, 20000]
data_sensitivity_repeat_time_each_analyzed_set = 5


def running_settings(test_mode, experiment_name):
    if test_mode:
        each_case_target_optimization_num = 30
        result_process_name = Keywords.normal_result_process
        loss_percentile = 0.01
        parallel_parameter_dict = None
        # parallel_parameter_dict = {
        #     'max_optimization_each_generation': 20,
        #     'each_process_optimization_num': 10,
        #     'processes_num': 1
        # }
    else:
        parallel_parameter_dict = {
            Keywords.max_optimization_each_generation: 2000,
            Keywords.each_process_optimization_num: 200,
            Keywords.processes_num: 6,
            Keywords.thread_num_constraint: None,
            # Keywords.parallel_test: True,
        }
        each_case_target_optimization_num = 20000
        if experiment_name in {
                ExperimentName.raw_model_all_data, ExperimentName.raw_model_raw_data}:
            each_case_target_optimization_num = 1100000
            result_process_name = Keywords.raw_model_result_process
            loss_percentile = 0.01
        elif experiment_name in {
                ExperimentName.raw_model_raw_data_with_squared_loss,
                ExperimentName.raw_model_all_data_with_squared_loss}:
            each_case_target_optimization_num = 400000
            parallel_parameter_dict[Keywords.max_optimization_each_generation] = 3200
            result_process_name = Keywords.raw_model_result_process
            loss_percentile = 0.01
        elif experiment_name in {
                ExperimentName.data_sensitivity, ExperimentName.data_sensitivity_with_noise}:
            result_process_name = Keywords.normal_result_process
            each_case_target_optimization_num = 250000
            loss_percentile = 0.005
        elif experiment_name in {
                ExperimentName.optimization_from_all_data_average_solutions,
                ExperimentName.optimization_from_raw_data_average_solutions,
        }:
            each_case_target_optimization_num = None
            result_process_name = Keywords.raw_model_averaged_optimization_result_process
            loss_percentile = None
        elif experiment_name in {
                ExperimentName.optimization_from_batched_simulated_all_data,
                ExperimentName.optimization_from_batched_simulated_raw_data,
                ExperimentName.optimization_from_batched_simulated_all_data_with_squared_loss,
                ExperimentName.optimization_from_batched_simulated_raw_data_with_squared_loss}:
            each_case_target_optimization_num = 60000
            result_process_name = Keywords.raw_model_batched_simulated_data_result_process
            loss_percentile = None
        elif experiment_name in {
                ExperimentName.optimization_from_batched_simulated_all_data_average_solutions,
                ExperimentName.optimization_from_batched_simulated_raw_data_average_solutions,}:
            result_process_name = Keywords.raw_model_batched_simulated_data_averaged_optimization_result_process
            loss_percentile = None
        else:
            result_process_name = Keywords.normal_result_process
            loss_percentile = 0.01
    return each_case_target_optimization_num, parallel_parameter_dict, result_process_name, loss_percentile


raw_model = ModelList.base_model

simulated_flux_value_dict = simulated_flux_vector_and_mid_data.simulated_flux_value_dict

normal_simulated_experimental_mid_data_obj_dict = \
    simulated_flux_vector_and_mid_data.simulated_experimental_mid_data_obj_dict
all_metabolite_simulated_experimental_mid_data_obj_dict = \
    simulated_flux_vector_and_mid_data.simulated_all_mid_data_obj_dict

normal_simulated_experimental_mid_data_obj_dict_with_noise = \
    simulated_flux_vector_and_mid_data_with_noise.simulated_experimental_mid_data_obj_dict
all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise = \
    simulated_flux_vector_and_mid_data_with_noise.simulated_all_mid_data_obj_dict


