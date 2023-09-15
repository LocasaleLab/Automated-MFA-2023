from scripts.src.core.common.classes import DefaultDict
from scripts.src.common.third_party_packages import tqdm
from scripts.src.core.model.model_constructor import common_model_constructor
from scripts.src.core.solver.solver_construction_functions.solver_constructor import base_solver_constructor, \
    common_solver_constructor

from scripts.model.model_loader import model_loader
from scripts.src.common_parallel_solver.feasible_solution_generator import universal_feasible_solution_generator

from ..common.result_output_functions import solver_output

from ..common.config import Keywords as GeneralKeywords

from . import config
from .config import Direct
from .sensitivity_config import RunningMode, Keywords, net_flux_list, model_data_config_dict
from .model_pattern_generation import model_processor
from .data_leave_out_generation import data_loader
from .boundary_condition_generation import boundary_condition_processor
from .result_processing_functions import result_label_generator, result_information_generator, CurrentFinalResult, \
    normal_result_process, raw_model_result_process
from scripts.src.common_parallel_solver.common_parallel_solver import slsqp_solving, common_parallel_solver, \
    each_case_optimization_distribution_iter_generator


def serial_solver(
        mfa_model_dict, mfa_data_dict, mfa_config_dict, test_mode, model_information_dict,
        data_information_dict, config_information_dict, final_result_obj, each_case_target_optimization_num,
        load_results=False):
    if load_results:
        optimization_num_dict, total_optimization_num = load_previous_results(
            mfa_model_dict, mfa_data_dict, mfa_config_dict, final_result_obj, each_case_target_optimization_num)
    else:
        optimization_num_dict = DefaultDict(each_case_target_optimization_num)
        total_optimization_num = len(mfa_model_dict) * len(mfa_data_dict) * len(mfa_config_dict) * \
            each_case_target_optimization_num
    pbar = tqdm.tqdm(
        total=total_optimization_num, smoothing=0, maxinterval=5,
        desc="Computation progress of {}".format(final_result_obj.result_name))
    for model_label, mfa_model in mfa_model_dict.items():
        for data_label, mfa_data in mfa_data_dict.items():
            for config_label, mfa_config in mfa_config_dict.items():
                result_label = result_label_generator(model_label, data_label, config_label)
                result_information = result_information_generator(
                    model_information_dict[model_label], data_information_dict[data_label],
                    config_information_dict[config_label])
                this_case_optimization_num = optimization_num_dict[result_label]
                if this_case_optimization_num == 0:
                    print(f'No solutions of {result_label} needs to be generated.')
                else:
                    print(f'{result_label} started: {this_case_optimization_num} solutions need to be generated')
                slsqp_obj = common_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
                initial_flux_input = universal_feasible_solution_generator(slsqp_obj, this_case_optimization_num)
                # initial_flux_input = feasible_flux_input_generator(
                #     slsqp_obj, config.random_initial_point_num, '', refresh=True)
                if initial_flux_input is None:
                    print(f'{result_label} failed to generate initial flux')
                else:
                    print('Initial flux generated')
                    result_list = slsqp_solving(
                        slsqp_obj, initial_flux_input, verbose=not test_mode, report_interval=config.report_interval)
                    pbar.update(this_case_optimization_num)
                    print(f'{result_label} ended')
                    final_result_obj.add_and_save_result(
                        result_label, result_information, result_list, slsqp_obj.flux_name_index_dict,
                        slsqp_obj.target_experimental_mid_data_dict)


def load_previous_results(mfa_model_dict, mfa_data_dict, mfa_config_dict, final_result_obj, each_case_optimization_num):
    # TODO: remove this function and use that in common_parallel_solver
    optimization_num_dict = {}
    total_optimization_num = 0
    for model_label, mfa_model in mfa_model_dict.items():
        for data_label, mfa_data in mfa_data_dict.items():
            for config_label, mfa_config in mfa_config_dict.items():
                result_label = result_label_generator(model_label, data_label, config_label)
                loaded_num = final_result_obj.load_previous_results(result_label)
                if loaded_num >= each_case_optimization_num:
                    new_optimization_num = 0
                else:
                    new_optimization_num = each_case_optimization_num - loaded_num
                total_optimization_num += new_optimization_num
                optimization_num_dict[result_label] = new_optimization_num
    return optimization_num_dict, total_optimization_num


def parallel_parameter_generator(
        mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict,
        config_information_dict, optimization_num_dict, test_mode, max_optimization_each_generation,
        each_process_optimization_num, **other_parameters):
    for model_label, mfa_model in mfa_model_dict.items():
        for data_label, mfa_data in mfa_data_dict.items():
            for config_label, mfa_config in mfa_config_dict.items():
                result_label = result_label_generator(model_label, data_label, config_label)
                result_information = result_information_generator(
                    model_information_dict[model_label], data_information_dict[data_label],
                    config_information_dict[config_label])
                this_case_optimization_num = optimization_num_dict[result_label]
                base_solver_obj = base_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
                base_solver_obj.base_initialize_solver()
                print(f'{result_label} started')
                each_case_iter = each_case_optimization_distribution_iter_generator(
                    this_case_optimization_num, each_process_optimization_num,
                    solver_obj=base_solver_obj, max_optimization_each_generation=max_optimization_each_generation)
                for current_initial_flux_input, current_optimization_num, start_index in each_case_iter:
                    yield base_solver_obj, mfa_config, current_initial_flux_input, test_mode, \
                        result_label, result_information, current_optimization_num, \
                        start_index, config.report_interval, config.thread_num_constraint
                # print('{} ended'.format(result_label))


def parallel_solver(
        mfa_model_dict, mfa_data_dict, mfa_config_dict, test_mode, model_information_dict,
        data_information_dict, config_information_dict, final_result_obj, each_case_target_optimization_num,
        parallel_parameter_dict, load_results=False):
    if load_results:
        optimization_num_dict, total_optimization_num = load_previous_results(
            mfa_model_dict, mfa_data_dict, mfa_config_dict, final_result_obj, each_case_target_optimization_num)
    else:
        optimization_num_dict = DefaultDict(each_case_target_optimization_num)
        total_optimization_num = len(mfa_model_dict) * len(mfa_data_dict) * len(mfa_config_dict) * \
            each_case_target_optimization_num
    parameter_list_iter = parallel_parameter_generator(
        mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict,
        config_information_dict, optimization_num_dict, test_mode, **parallel_parameter_dict)
    common_parallel_solver(
        final_result_obj, each_case_target_optimization_num, total_optimization_num, parameter_list_iter,
        **parallel_parameter_dict)


def materials_preparation(
        raw_model, model_process_type, data_process_list, mfa_data_obj_generation, mfa_config_type,
        simulated_flux_value_dict):
    complete_defined_model = model_loader(raw_model)
    (
        modified_defined_model_dict, model_information_dict, important_flux_list,
        important_flux_replace_dict) = model_processor(
        model_process_type, complete_defined_model, simulated_flux_value_dict)
    mfa_model_dict = {}
    for model_label, current_defined_model in modified_defined_model_dict.items():
        mfa_model_dict[model_label] = common_model_constructor(current_defined_model)
    modified_data_dict, data_information_dict = data_loader(data_process_list)
    mfa_data_dict = {}
    for data_label, current_experimental_mid_data_obj_dict in modified_data_dict.items():
        mfa_data_dict[data_label] = mfa_data_obj_generation(current_experimental_mid_data_obj_dict)
    mfa_config_dict, config_information_dict = boundary_condition_processor(mfa_config_type, simulated_flux_value_dict)
    return mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict, \
        config_information_dict, important_flux_list, important_flux_replace_dict


def solver_dict_constructor(
        mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict,
        config_information_dict):
    target_solver_dict = {}
    final_information_dict = {}
    same_model_dict = {}
    same_data_dict = {}
    previous_model = None
    previous_data = None
    for model_label, mfa_model in mfa_model_dict.items():
        for data_label, mfa_data in mfa_data_dict.items():
            for config_label, mfa_config in mfa_config_dict.items():
                result_label = result_label_generator(model_label, data_label, config_label)
                result_information_dict = result_information_generator(
                    model_information_dict[model_label], data_information_dict[data_label],
                    config_information_dict[config_label])
                current_solver_obj = common_solver_constructor(
                    mfa_model, mfa_data, mfa_config, name=result_label, verbose=False)
                target_solver_dict[result_label] = current_solver_obj
                final_information_dict[result_label] = result_information_dict
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
        result_process_name, important_flux_list, important_flux_replace_dict, base_mfa_config, loss_percentile):
    # complete_defined_model = model_loader(raw_model)
    # (
    #     modified_defined_model_dict, model_information_dict, important_flux_list,
    #     important_flux_replace_dict) = model_processor(
    #     model_process_type, complete_defined_model, simulated_flux_value_dict)
    # model_label_list = list(modified_defined_model_dict.keys())
    # modified_data_dict, data_information_dict = data_loader(data_process_list)
    # data_label_list = list(modified_data_dict.keys())
    # mfa_config_dict, config_information_dict = boundary_condition_processor(mfa_config_type, simulated_flux_value_dict)
    # config_label_list = list(mfa_config_dict.keys())
    # final_information_dict = {}
    # for model_label, mfa_model_information in model_information_dict.items():
    #     for data_label, mfa_data_information in data_information_dict.items():
    #         for config_label, mfa_config_information in config_information_dict.items():
    #             result_label = result_label_generator(model_label, data_label, config_label)
    #             result_information = result_information_generator(
    #                 mfa_model_information, mfa_data_information, mfa_config_information)
    #             final_information_dict[result_label] = result_information

    # final_result_obj.repair_predicted_mid_dict_and_merge(target_solver_dict)
    # exit()

    if result_process_name == Keywords.normal_result_process:
        result_process_func = normal_result_process
        other_parameter_list = [important_flux_list, important_flux_replace_dict, net_flux_list, loss_percentile]
    elif result_process_name == Keywords.raw_model_result_process:
        result_process_func = raw_model_result_process
        other_parameter_list = [
            important_flux_list, important_flux_replace_dict, base_mfa_config, net_flux_list]
    else:
        raise ValueError()
    final_result_obj.final_process(
        target_solver_dict, final_information_dict, result_process_name, result_process_func, *other_parameter_list)


def model_data_sensitivity_common_dispatcher(
        raw_model, model_process_type, data_process_list, mfa_config_type, final_result_obj, simulated_flux_value_dict,
        mfa_data_obj_generation, experiment_name, parallel_num, test_mode, running_mode):
    (
        each_case_target_optimization_num, parallel_parameter_dict, result_process_name,
        loss_percentile) = config.running_settings(test_mode, experiment_name)
    if parallel_parameter_dict is not None and parallel_num is not None:
        parallel_parameter_dict['processes_num'] = parallel_num
    (
        mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict,
        config_information_dict, important_flux_list, important_flux_replace_dict) = materials_preparation(
        raw_model, model_process_type, data_process_list, mfa_data_obj_generation, mfa_config_type,
        simulated_flux_value_dict)
    if running_mode == RunningMode.flux_analysis:
        if parallel_parameter_dict is not None:
            parallel_solver(
                mfa_model_dict, mfa_data_dict, mfa_config_dict, test_mode, model_information_dict,
                data_information_dict, config_information_dict, final_result_obj, each_case_target_optimization_num,
                parallel_parameter_dict, config.load_previous_results)
        else:
            serial_solver(
                mfa_model_dict, mfa_data_dict, mfa_config_dict, test_mode, model_information_dict,
                data_information_dict, config_information_dict, final_result_obj, each_case_target_optimization_num,
                config.load_previous_results)
    else:
        target_solver_dict, final_information_dict, same_model_dict, same_data_dict = solver_dict_constructor(
            mfa_model_dict, mfa_data_dict, mfa_config_dict, model_information_dict, data_information_dict,
            config_information_dict)

        # final_result_obj.repair_predicted_mid_dict(target_solver_dict, result_process_name)
        # exit()

        if running_mode == RunningMode.solver_output:
            solver_output(
                target_solver_dict, final_information_dict, final_result_obj, same_model_dict, same_data_dict)
        elif running_mode == RunningMode.result_process:
            base_mfa_config = mfa_config_dict[Keywords.raw_type]
            model_data_sensitivity_result_display(
                target_solver_dict, final_information_dict, final_result_obj,
                result_process_name, important_flux_list, important_flux_replace_dict, base_mfa_config, loss_percentile)
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
    simulated_flux_value_dict = config.simulated_flux_value_dict
    final_result_obj = CurrentFinalResult(
        Direct.output_direct, Direct.common_data_direct, experiment_name, simulated_flux_value_dict)
    model_data_sensitivity_common_dispatcher(
        raw_model, model_process_type, data_process_list, mfa_config_type, final_result_obj,
        simulated_flux_value_dict, config.mfa_data_obj_generation,
        experiment_name, parallel_num, test_mode, running_mode)

