from scripts.src.common.config import Direct as CommonDirect

from scripts.src.core.common.config import ParamName

from scripts.model.base_model import simulated_flux_vector_and_mid_data, \
    simulated_flux_vector_and_mid_data_with_noise
from scripts.model.model_loader import ModelList

from .sensitivity_config import RunningMode, ExperimentName, Keywords


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

report_interval = 50
thread_num_constraint = None

# analysis_solver = ParamName.slsqp_numba_python_solver
# analysis_solver = ParamName.slsqp_numba_nopython_solver
analysis_solver = ParamName.slsqp_solver


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
            'max_optimization_each_generation': 2000,
            'each_process_optimization_num': 200,
            'processes_num': 6
        }
        if experiment_name == ExperimentName.raw_model_all_data or \
                experiment_name == ExperimentName.raw_model_raw_data:
            each_case_target_optimization_num = 1100000
            result_process_name = Keywords.raw_model_result_process
            loss_percentile = 0.01
        elif experiment_name == ExperimentName.data_sensitivity or \
                experiment_name == ExperimentName.data_sensitivity_with_noise:
            each_case_target_optimization_num = 20000
            result_process_name = Keywords.normal_result_process
            loss_percentile = 0.005
        else:
            each_case_target_optimization_num = 20000
            result_process_name = Keywords.normal_result_process
            loss_percentile = 0.01
    return each_case_target_optimization_num, parallel_parameter_dict, result_process_name, loss_percentile


raw_model = ModelList.base_model

simulated_flux_value_dict = simulated_flux_vector_and_mid_data.simulated_flux_value_dict
mfa_data_obj_generation = simulated_flux_vector_and_mid_data.mfa_data_obj_generation

normal_simulated_experimental_mid_data_obj_dict = \
    simulated_flux_vector_and_mid_data.simulated_experimental_mid_data_obj_dict
all_metabolite_simulated_experimental_mid_data_obj_dict = \
    simulated_flux_vector_and_mid_data.simulated_all_mid_data_obj_dict

normal_simulated_experimental_mid_data_obj_dict_with_noise = \
    simulated_flux_vector_and_mid_data_with_noise.simulated_experimental_mid_data_obj_dict
all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise = \
    simulated_flux_vector_and_mid_data_with_noise.simulated_all_mid_data_obj_dict




