from scripts.src.core.solver.solver_construction_functions.solver_constructor import common_solver_constructor, \
    base_solver_constructor
from scripts.src.core.common.classes import MFAConfig
from scripts.src.core.common.config import ParamName
from ..common.functions import update_parameter_object
from ..common.result_output_functions import solver_output

from scripts.src.common.config import Keywords
from scripts.src.common_parallel_solver.feasible_solution_generator import universal_feasible_solution_generator
from scripts.src.common_parallel_solver.common_parallel_solver import slsqp_solving, common_parallel_solver, \
    each_case_optimization_distribution_iter_generator, generate_unoptimized_solutions, parallel_parameter_generator, \
    load_previous_results

from .inventory import RunningMode, DataModelType
from .specific_data_model_combination.common_data_model_loader import common_data_model_function_loader
from .result_processing_functions import CurrentFinalResult, result_label_generator, \
    experimental_mid_and_raw_data_plotting, normal_result_process, hct116_result_process
from . import config
Direct = config.Direct


def serial_solver(
        mfa_data_dict, result_information_dict, mfa_model, mfa_config, each_case_optimization_num,
        final_result_obj, test_mode):
    for result_label, mfa_data in mfa_data_dict.items():
        result_information = result_information_dict[result_label]
        slsqp_solver_obj = common_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
        initial_flux_input = universal_feasible_solution_generator(slsqp_solver_obj, each_case_optimization_num)
        print('{} started'.format(result_label))
        if initial_flux_input is None:
            print('{} failed to generate initial flux'.format(result_label))
        else:
            print('Initial flux generated')
            result_list = slsqp_solving(
                slsqp_solver_obj, initial_flux_input, verbose=not test_mode, report_interval=config.report_interval)
            print('{} ended'.format(result_label))
            final_result_obj.add_and_save_result(
                result_label, result_information, result_list, slsqp_solver_obj.flux_name_index_dict,
                slsqp_solver_obj.target_experimental_mid_data_dict)

#
# def load_previous_results_old(mfa_data_dict, final_result_obj, each_case_optimization_num):
#     optimization_num_dict = {}
#     total_optimization_num = 0
#     for data_label, mfa_data in mfa_data_dict.items():
#         result_label = result_label_generator(mfa_data, 99999)
#         loaded_num = final_result_obj.load_previous_results(result_label)
#         if loaded_num >= each_case_optimization_num:
#             new_optimization_num = 0
#         else:
#             new_optimization_num = each_case_optimization_num - loaded_num
#         total_optimization_num += new_optimization_num
#         optimization_num_dict[result_label] = new_optimization_num
#     return optimization_num_dict, total_optimization_num


# Since sampling procedure will conflict with multiprocessing, construct solver list first
def solver_and_solution_list_construct(
        mfa_model, mfa_data_dict, mfa_config, result_information_dict, final_result_obj, test_mode,
        each_case_optimization_num, load_results, each_process_optimization_num,
        max_optimization_each_generation, **other_parameters):
    result_list = []
    total_optimization_num = 0
    for result_label, mfa_data_obj in mfa_data_dict.items():
        base_solver_obj = base_solver_constructor(mfa_model, mfa_data_obj, mfa_config, verbose=test_mode)
        base_solver_obj.base_initialize_solver()
        result_information = result_information_dict[result_label]
        if load_results:
            new_optimization_num = load_previous_results(result_label, final_result_obj, each_case_optimization_num)
        else:
            new_optimization_num = each_case_optimization_num
        if new_optimization_num == 0:
            print('No solution of {} need to be obtained. Abort'.format(result_label))
            continue
        print('{} initial value of {} need to be generated. Start generating...'.format(
            new_optimization_num, result_label))
        if result_label.endswith(Keywords.unoptimized):
            generate_unoptimized_solutions(
                mfa_config, new_optimization_num, final_result_obj, base_solver_obj, result_label,
                result_information, each_case_optimization_num)
            print(f'{new_optimization_num} number of unoptimized solutions have been saved.')
        else:
            total_optimization_num += new_optimization_num
            total_initial_flux_input = universal_feasible_solution_generator(
                base_solver_obj, new_optimization_num)
            each_case_iter = each_case_optimization_distribution_iter_generator(
                new_optimization_num, each_process_optimization_num,
                total_initial_flux_input=total_initial_flux_input)
            print(f'{result_label} initial value finished')
            result_list.append((
                base_solver_obj, each_case_iter, result_label, result_information))
    return result_list, total_optimization_num


# def parallel_parameter_generator_old(
#         mfa_data_dict, result_information_dict, mfa_model, mfa_config, optimization_num_dict,
#         test_mode, max_optimization_each_generation, each_process_optimization_num, **other_parameters):
#     for result_label, mfa_data in mfa_data_dict.items():
#         result_information = result_information_dict[result_label]
#         this_case_optimization_num = optimization_num_dict[result_label]
#         base_solver_obj = base_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
#         base_solver_obj.base_initialize_solver()
#         print('{} started'.format(result_label))
#         each_case_iter = each_case_optimization_distribution_iter_generator(
#             this_case_optimization_num, each_process_optimization_num,
#             solver_obj=base_solver_obj, max_optimization_each_generation=max_optimization_each_generation)
#         for current_initial_flux_input, current_optimization_num, start_index in each_case_iter:
#             yield base_solver_obj, mfa_config, current_initial_flux_input, test_mode, \
#                   result_label, result_information, current_optimization_num, \
#                   start_index, config.report_interval, config.thread_num_constraint
#         # print('{} ended'.format(result_label))


def parallel_solver(
        mfa_data_dict, result_information_dict, mfa_model, mfa_config, each_case_optimization_num, final_result_obj,
        test_mode, parallel_parameter_dict, load_results=False):
    result_list, total_optimization_num = solver_and_solution_list_construct(
        mfa_model, mfa_data_dict, mfa_config, result_information_dict, final_result_obj, test_mode,
        each_case_optimization_num, load_results, **parallel_parameter_dict)
    parameter_list_iter = parallel_parameter_generator(
        result_list, mfa_config, test_mode, config.report_interval, config.thread_num_constraint)
    common_parallel_solver(
        final_result_obj, each_case_optimization_num, total_optimization_num, parameter_list_iter,
        **parallel_parameter_dict)


def mfa_data_loader(total_param_list, data_wrap_obj):
    mfa_data_dict = {}
    result_information_dict = {}
    for param_dict in total_param_list:
        mfa_data = data_wrap_obj.return_dataset(param_dict)
        result_label = result_label_generator(mfa_data, param_dict[Keywords.obj_threshold_key])
        mfa_data_dict[result_label] = mfa_data
        if param_dict[Keywords.obj_threshold_key] is None:
            del param_dict[Keywords.obj_threshold_key]
        result_information_dict[result_label] = param_dict
    return mfa_data_dict, result_information_dict


def solver_dict_constructor(mfa_model, mfa_data_dict, mfa_config):
    target_solver_dict = {}
    same_model_dict = {}
    same_data_dict = {}
    previous_label = None
    for result_label, mfa_data in mfa_data_dict.items():
        current_solver_obj = common_solver_constructor(
            mfa_model, mfa_data, mfa_config, name=result_label, verbose=False)
        target_solver_dict[result_label] = current_solver_obj
        if previous_label is None:
            same_model_dict[result_label] = False
            previous_label = result_label
        else:
            same_model_dict[result_label] = True
        if result_label.startswith(previous_label) and result_label.endswith(Keywords.unoptimized):
            same_data_dict[result_label] = True
        else:
            same_data_dict[result_label] = False
    return target_solver_dict, same_model_dict, same_data_dict


def raw_experimental_data_plotting(solver_dict, result_information_dict, final_result_obj):
    target_metabolite_data_obj_dict = {}
    for result_label, solver_obj in solver_dict.items():
        if result_label == Keywords.unoptimized:
            continue
        current_data_obj_dict = {}
        for emu_name in solver_obj.target_experimental_mid_data_dict.keys():
            experimental_name = solver_obj.emu_name_experimental_name_dict[emu_name]
            current_data_obj_dict[experimental_name] = solver_obj.experimental_mid_data_obj_dict[experimental_name]
        target_metabolite_data_obj_dict[result_label] = current_data_obj_dict
    experimental_mid_and_raw_data_plotting(target_metabolite_data_obj_dict, result_information_dict, final_result_obj)


# def experimental_analysis_solver_output(
#         solver_dict, final_information_dict, final_result_obj, same_model_dict, same_data_dict):
#     sheet_name_dict = {}
#     sheet_information_dict = {}
#     sheet_information_item_name_dict = {}
#     for result_label, result_information_dict in final_information_dict.items():
#         tmp_information_item_dict = excel_sheet_information_process(
#             result_label, result_information_dict, sheet_name_dict, sheet_information_dict)
#         sheet_information_item_name_dict.update(tmp_information_item_dict)
#     solver_memo_output(
#         final_result_obj.solver_descriptions_output_xlsx_path, sheet_name_dict, sheet_information_dict,
#         solver_dict, list(sheet_information_item_name_dict.keys()), same_model_dict=same_model_dict,
#         same_data_dict=same_data_dict)


def result_display(solver_dict, final_result_obj, data_model_name):
    if data_model_name == DataModelType.hct116_cultured_cell_line:
        result_process_func = hct116_result_process
    else:
        result_process_func = normal_result_process
    final_result_obj.final_process(result_process_func, solver_dict)


def experimental_data_analysis_common_dispatcher(
        data_model_name, data_model_object, final_result_obj, test_mode, parallel_num, running_mode):
    mfa_model = data_model_object.mfa_model_obj
    data_wrap_obj = data_model_object.data_wrap_obj
    total_param_list = data_model_object.total_param_list

    common_parameter = config.CommonParameters()
    specific_parameter = data_model_object.SpecificParameter()
    common_parameter = update_parameter_object(common_parameter, specific_parameter)

    mfa_config = MFAConfig(
        common_parameter.common_flux_range, common_parameter.specific_flux_range_dict,
        common_parameter.test_dynamic_constant_flux_list, common_parameter.test_preset_constant_flux_value_dict,
        common_parameter.common_mix_ratio_range, common_parameter.mix_ratio_multiplier, config.solver_type,
        common_parameter.solver_config_dict)

    each_case_optimization_num, parallel_parameter_dict = config.running_settings(test_mode)
    if parallel_parameter_dict is not None and parallel_num is not None:
        parallel_parameter_dict['processes_num'] = parallel_num

    mfa_data_dict, result_information_dict = mfa_data_loader(total_param_list, data_wrap_obj)

    if running_mode == RunningMode.flux_analysis:
        if parallel_parameter_dict is not None:
            parallel_solver(
                mfa_data_dict, result_information_dict, mfa_model, mfa_config, each_case_optimization_num,
                final_result_obj, test_mode, parallel_parameter_dict, config.load_previous_results)
        else:
            serial_solver(
                mfa_data_dict, result_information_dict, mfa_model, mfa_config, each_case_optimization_num,
                final_result_obj, test_mode)
    else:
        solver_dict, same_model_dict, same_data_dict = solver_dict_constructor(mfa_model, mfa_data_dict, mfa_config)
        if running_mode == RunningMode.raw_experimental_data_plotting:
            raw_experimental_data_plotting(solver_dict, result_information_dict, final_result_obj)
        elif running_mode == RunningMode.solver_output:
            solver_output(
                solver_dict, result_information_dict, final_result_obj, same_model_dict, same_data_dict)
        elif running_mode == RunningMode.result_process:
            result_display(solver_dict, final_result_obj, data_model_name)
        else:
            raise ValueError()


# def raw_experimental_data_plotting_old(data_model_object, final_result_obj):
#     data_wrap_obj = data_model_object.data_wrap_obj
#     total_param_list = data_model_object.total_param_list
#     mfa_model = data_model_object.mfa_model_obj
#
#     common_parameter = config.CommonParameters()
#     specific_parameter = data_model_object.SpecificParameter()
#     common_parameter = update_parameter_object(common_parameter, specific_parameter)
#
#     mfa_config = MFAConfig(
#         common_parameter.common_flux_range, common_parameter.specific_flux_range_dict,
#         common_parameter.test_dynamic_constant_flux_list, common_parameter.test_preset_constant_flux_value_dict,
#         common_parameter.common_mix_ratio_range, common_parameter.mix_ratio_multiplier, ParamName.slsqp_solver,
#         common_parameter.solver_config_dict)
#
#     mfa_data_dict, result_information_dict = mfa_data_loader(total_param_list, data_wrap_obj)
#
#     target_metabolite_data_obj_dict = {}
#     for result_label, mfa_data in mfa_data_dict.items():
#         if result_label == Keywords.unoptimized:
#             continue
#         current_solver_obj = common_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=False)
#         current_data_obj_dict = {}
#         for emu_name in current_solver_obj.target_experimental_mid_data_dict.keys():
#             experimental_name = current_solver_obj.emu_name_experimental_name_dict[emu_name]
#             current_data_obj_dict[experimental_name] = current_solver_obj.experimental_mid_data_obj_dict[experimental_name]
#         target_metabolite_data_obj_dict[result_label] = current_data_obj_dict
#     experimental_mid_and_raw_data_plotting(target_metabolite_data_obj_dict, result_information_dict, final_result_obj)


def data_analysis_main(running_mode, data_model_name, test_mode, parallel_num):
    if data_model_name is None:
        data_model_name = config.data_model_name
    data_model_object = common_data_model_function_loader(data_model_name)
    final_result_obj = CurrentFinalResult(
        Direct.output_direct, Direct.common_data_direct, data_model_name, data_model_object)
    # running_mode = config.running_mode
    experimental_data_analysis_common_dispatcher(
        data_model_name, data_model_object, final_result_obj, test_mode, parallel_num, running_mode)

