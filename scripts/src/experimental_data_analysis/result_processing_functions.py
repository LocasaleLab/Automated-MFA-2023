from scripts.src.common.classes import FinalResult
from scripts.src.common.functions import calculate_raw_and_net_distance, \
    special_result_label_converter, analyze_simulated_flux_value_dict
from scripts.src.common.plotting_functions import group_violin_box_distribution_plot, \
    scatter_plot_for_simulated_result, FigurePlotting
from scripts.src.common.config import Keywords, net_flux_list, np, random_seed, FigureData
from scripts.src.common.third_party_packages import np, decomposition
from scripts.src.common.result_processing_functions import experimental_mid_prediction

from scripts.data.simulated_data.simulated_data_loader import simulated_data_loader

from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.config import FigureDataKeywords
from ..common.result_processing_functions import loss_data_distribution_plotting, reconstruct_and_filter_data_dict, \
    time_distribution_plotting, result_verification, multiple_repeat_result_processing, \
    traditional_method_result_selection
from ..common.result_output_functions import output_raw_flux_data, output_predicted_mid_data

from . import config
from .inventory import DataModelType

figure_plotting: FigurePlotting = None


def initialize_figure_plotting():
    global figure_plotting
    if figure_plotting is not None:
        return
    from figures.figure_content.common.config import ParameterName
    from figures.figure_content.common.elements import Elements
    figure_plotting = FigurePlotting(ParameterName, Elements)


def result_label_generator(mfa_data, obj_threshold=None):
    if obj_threshold == Keywords.unoptimized:
        return f'{mfa_data.data_name}__{Keywords.unoptimized}'
    else:
        return mfa_data.data_name


class CurrentFinalResult(FinalResult):
    def __init__(
            self, project_output_direct=config.Direct.output_direct,
            common_data_output_direct=config.Direct.common_data_direct,
            result_name=None, data_model_object=None):
        super(CurrentFinalResult, self).__init__(
            project_output_direct, common_data_output_direct, result_name)
        self.data_model_object = data_model_object

    def final_process(self, result_process_func, solver_dict):
        final_mapping_dict = self.data_model_object.collect_results(self)
        result_process_func(self, final_mapping_dict, solver_dict)


def normal_result_process(final_result_obj, final_mapping_dict, solver_dict):
    data_model_object = final_result_obj.data_model_object
    final_information_dict = final_result_obj.final_information_dict
    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    final_solution_data_dict = final_result_obj.final_solution_data_dict
    final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    final_flux_name_index_dict = final_result_obj.final_flux_name_index_dict
    final_target_experimental_mid_data_dict = final_result_obj.final_target_experimental_mid_data_dict

    print(f'Result processing for {result_name}')
    if config.verify_result:
        result_verification(solver_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict)
    loss_percentile = config.loss_percentile
    if config.repeat_each_analyzed_set:
        optimization_num = 20000
        if result_name == DataModelType.lung_tumor_invivo_infusion:
            repeat_time_each_analyzed_set = 3
        else:
            repeat_time_each_analyzed_set = config.repeat_time_each_analyzed_set
        final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict = multiple_repeat_result_processing(
            solver_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
            repeat_division_num=repeat_time_each_analyzed_set, each_optimization_num=optimization_num,
            loss_percentile=loss_percentile)
        loss_percentile = None
    subset_index_dict = loss_data_distribution_plotting(
        result_name, final_loss_data_dict,
        output_direct=final_result_obj.this_result_output_direct, loss_percentile=loss_percentile)
    important_flux_display(
        result_name, final_solution_data_dict, final_mapping_dict,
        data_model_object, final_flux_name_index_dict,
        final_result_obj.flux_comparison_output_direct, subset_index_dict=subset_index_dict)
    experimental_mid_prediction(
        result_name, {Keywords.optimized: final_predicted_data_dict},
        final_target_experimental_mid_data_dict, final_result_obj.mid_prediction_output_direct,
        subset_index_dict=subset_index_dict)
    try:
        figure_config_dict = data_model_object.figure_config_dict
    except AttributeError:
        figure_config_dict = None
    mid_grid_plotting(
        result_name, final_predicted_data_dict, data_model_object,
        final_result_obj.mid_prediction_output_direct, figure_config_dict)
    metabolic_network_plotting(
        result_name, data_model_object, final_solution_data_dict,
        final_flux_name_index_dict, final_result_obj.metabolic_network_visualization_direct,
        subset_index_dict=subset_index_dict)
    output_raw_flux_data(
        final_result_obj.flux_result_output_xlsx_path, final_loss_data_dict,
        final_solution_data_dict, final_flux_name_index_dict,
        final_information_dict, subset_index_dict=subset_index_dict, other_label_column_dict=None)
    output_predicted_mid_data(
        final_result_obj.mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
        final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=subset_index_dict)
    try:
        multi_tumor_comparison = data_model_object.multi_tumor_comparison
    except AttributeError:
        pass
    else:
        if multi_tumor_comparison:
            multi_tumor_comparison_plotting(
                result_name, final_result_obj.flux_comparison_output_direct)


def traditional_method_result_process(final_result_obj, final_mapping_dict, solver_dict):
    data_model_object = final_result_obj.data_model_object
    final_information_dict = final_result_obj.final_information_dict
    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    final_solution_data_dict = final_result_obj.final_solution_data_dict
    final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    final_flux_name_index_dict = final_result_obj.final_flux_name_index_dict
    final_target_experimental_mid_data_dict = final_result_obj.final_target_experimental_mid_data_dict

    print(f'Result processing for {result_name}')
    if config.traditional_repeat_each_analyzed_set:
        (
            final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict
        ) = traditional_method_result_selection(
            final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
            config.traditional_method_total_num,
            repeat_time_each_analyzed_set=config.repeat_time_each_analyzed_set)
    else:
        (
            final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict
        ) = traditional_method_result_selection(
            final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
            config.traditional_method_total_num, select_num=config.traditional_method_select_num)
    subset_index_dict = loss_data_distribution_plotting(
        result_name, final_loss_data_dict,
        output_direct=final_result_obj.this_result_output_direct)
    modified_final_mapping_dict = {
        key: value[:-1] for key, value in final_mapping_dict.items()}
    important_flux_display(
        result_name, final_solution_data_dict, modified_final_mapping_dict,
        data_model_object, final_flux_name_index_dict,
        final_result_obj.flux_comparison_output_direct, subset_index_dict=subset_index_dict)
    output_raw_flux_data(
        final_result_obj.flux_result_output_xlsx_path, final_loss_data_dict,
        final_solution_data_dict, final_flux_name_index_dict,
        final_information_dict, subset_index_dict=subset_index_dict, other_label_column_dict=None)
    output_predicted_mid_data(
        final_result_obj.mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
        final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=subset_index_dict)


def hct116_result_process(final_result_obj, final_mapping_dict, solver_dict):
    def return_target_data_dict(squared_loss=False):
        if squared_loss:
            target_mid_prediction_dict = squared_mid_prediction_dict
            target_loss_data_dict = squared_loss_data_dict
            target_solution_data_dict = squared_solution_data_dict
            target_time_data_dict = squared_time_data_dict
        else:
            target_mid_prediction_dict = normal_mid_prediction_dict
            target_loss_data_dict = normal_loss_data_dict
            target_solution_data_dict = normal_solution_data_dict
            target_time_data_dict = normal_time_data_dict
        return target_loss_data_dict, target_solution_data_dict, target_mid_prediction_dict, target_time_data_dict

    def filter_and_update_data_dicts(
            input_data_label, output_class_label, output_mid_data_label, current_total_size, selected_index=None,
            mid_selected_index=None, loss_evaluation_solver=None):
        filtered_loss_data_array = raw_loss_data_dict[input_data_label]
        filtered_solution_data_array = raw_solution_data_dict[input_data_label]
        current_predicted_data_dict = raw_final_predicted_data_dict[input_data_label]
        if input_data_label in raw_time_data_dict:
            filtered_time_data_array = raw_time_data_dict[input_data_label]
        else:
            filtered_time_data_array = None
        # if selected_num is not None and selected_num < current_total_size:
        if selected_index is not None:
            assert len(selected_index) < current_total_size
            # selected_index = this_process_random_seed.choice(current_total_size, selected_num, replace=False)
            filtered_solution_data_array = filtered_solution_data_array[selected_index, :]
            filtered_loss_data_array = filtered_loss_data_array[selected_index]
            if filtered_time_data_array is not None:
                filtered_time_data_array = filtered_time_data_array[selected_index]
        else:
            selected_index = None
        if mid_selected_index is None and selected_index is not None:
            mid_selected_index = selected_index
        # if mid_prediction_selected_num is not None:
        #     if selected_index is not None:
        #         if len(selected_index) < mid_prediction_selected_num:
        #             raise ValueError()
        #         elif len(selected_index) > mid_prediction_selected_num:
        #             selected_index = this_process_random_seed.choice(selected_index, mid_prediction_selected_num, replace=False)
        #     else:
        #         selected_index = this_process_random_seed.choice(current_total_size, mid_prediction_selected_num, replace=False)
        filtered_predicted_data_dict = {}
        for mid_title, current_predicted_data_array_list in current_predicted_data_dict.items():
            current_predicted_data_array = np.array(current_predicted_data_array_list)
            if mid_selected_index is not None:
                current_predicted_data_array = current_predicted_data_array[mid_selected_index, :]
            filtered_predicted_data_dict[mid_title] = current_predicted_data_array
        (
            target_loss_data_dict, target_solution_data_dict, target_mid_prediction_dict, target_time_data_dict
        ) = return_target_data_dict(loss_evaluation_solver is not None)
        target_mid_prediction_dict[output_class_label] = {output_mid_data_label: filtered_predicted_data_dict}
        target_loss_data_dict[output_class_label] = filtered_loss_data_array
        target_solution_data_dict[output_class_label] = filtered_solution_data_array
        if filtered_time_data_array is not None:
            target_time_data_dict[output_class_label] = filtered_time_data_array / parallel_num

    def load_and_save_previous_result(
            input_data_label, output_class_label, loss_evaluation_solver=None):
        (
            input_loss_data_dict, input_solution_data_dict, input_mid_prediction_dict, input_time_data_dict
        ) = return_target_data_dict(False)
        (
            target_loss_data_dict, target_solution_data_dict, target_mid_prediction_dict, target_time_data_dict
        ) = return_target_data_dict(loss_evaluation_solver is not None)
        target_mid_prediction_dict[output_class_label] = {
            output_class_label: input_mid_prediction_dict[input_data_label]}
        input_solution_data_array = input_solution_data_dict[input_data_label]
        target_solution_data_dict[output_class_label] = input_solution_data_array
        if loss_evaluation_solver is not None:
            loss_value_list = []
            for flux_vector in input_solution_data_array:
                current_loss = loss_evaluation_solver.obj_eval(flux_vector)
                loss_value_list.append(current_loss)
            output_loss_data_array = np.array(loss_value_list)
        else:
            output_loss_data_array = input_loss_data_dict[input_data_label]
        target_loss_data_dict[output_class_label] = output_loss_data_array
        if input_data_label in input_time_data_dict:
            target_time_data_dict[output_class_label] = input_time_data_dict[input_data_label]

    total_size = 2000
    optimized_num_for_analysis = 400
    # unoptimized_num_for_embedding = 500
    # optimized_num_for_embedding = 30
    # unoptimized_num_for_embedding = 400
    # optimized_num_for_embedding = 400
    # parallel_num = 6
    # parallel_num = 16
    parallel_num = 20

    # this_process_random_seed = np.random.default_rng(59475)
    this_process_random_seed = np.random.default_rng(4837)

    optimized_index = this_process_random_seed.choice(total_size, optimized_num_for_analysis, replace=False)

    result_name = final_result_obj.result_name
    final_information_dict = final_result_obj.final_information_dict
    raw_final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    raw_loss_data_dict = final_result_obj.final_loss_data_dict
    raw_solution_data_dict = final_result_obj.final_solution_data_dict
    raw_time_data_dict = final_result_obj.final_time_data_dict
    with_glns_m = 'with_glns_m' in final_result_obj.result_name.value
    simulated_flux_value_dict, *_ = simulated_data_loader(with_glns_m=with_glns_m)
    the_only_experimental_mid_dict = None
    the_only_flux_name_index_dict = None
    loaded_result_label_dict = {}
    normal_mid_prediction_dict = {}
    normal_loss_data_dict = {}
    normal_solution_data_dict = {}
    normal_time_data_dict = {}
    squared_mid_prediction_dict = {}
    squared_solution_data_dict = {}
    squared_loss_data_dict = {}
    squared_time_data_dict = {}
    raw_output_information_dict = {}
    common_flux_name_index_dict = None
    for result_label, (
            experiments_key, condition_key, repeat_index, unoptimized_label, squared_loss_label
    ) in final_mapping_dict.items():
        if result_label in loaded_result_label_dict:
            continue
        loss_evaluation_solver = None
        if unoptimized_label:
            unoptimized_result_label = result_label
            optimized_result_label = special_result_label_converter(result_label, Keywords.unoptimized, decipher=True)

            filter_and_update_data_dicts(
                unoptimized_result_label, Keywords.unoptimized, optimized_result_label, total_size,
                selected_index=optimized_index)
            # filter_and_update_data_dicts(
            #     unoptimized_result_label, Keywords.unoptimized, optimized_result_label, selected_num=None,
            #     mid_prediction_selected_num=unoptimized_num_for_mid_prediction)
            loaded_result_label_dict[unoptimized_result_label] = None
        elif squared_loss_label is not None:
            optimized_result_label = result_label
            raw_result_label = special_result_label_converter(result_label, Keywords.squared_loss, decipher=True)
            unoptimized_result_label = special_result_label_converter(raw_result_label, Keywords.unoptimized)
            loss_evaluation_solver = solver_dict[result_label]
            load_and_save_previous_result(
                Keywords.unoptimized, Keywords.unoptimized, loss_evaluation_solver)
        else:
            optimized_result_label = result_label
            unoptimized_result_label = special_result_label_converter(optimized_result_label, Keywords.unoptimized)

        if optimized_result_label not in loaded_result_label_dict:
            filter_and_update_data_dicts(
                optimized_result_label, Keywords.optimized, optimized_result_label, total_size,
                selected_index=optimized_index, loss_evaluation_solver=loss_evaluation_solver)
            loaded_result_label_dict[optimized_result_label] = None
        # if unoptimized_result_label not in loaded_result_label_dict:
        #     filter_and_update_data_dicts(
        #         unoptimized_result_label, Keywords.unoptimized, optimized_result_label, selected_num=None,
        #         mid_prediction_selected_num=unoptimized_num_for_mid_prediction,
        #         loss_evaluation_solver=loss_evaluation_solver)
        #     loaded_result_label_dict[unoptimized_result_label] = None
        if the_only_experimental_mid_dict is None:
            the_only_experimental_mid_dict = final_result_obj.final_target_experimental_mid_data_dict[
                optimized_result_label]
            the_only_flux_name_index_dict = final_result_obj.final_flux_name_index_dict[optimized_result_label]
        if len(raw_output_information_dict) == 0:
            raw_output_information_dict = {
                Keywords.unoptimized: final_information_dict[unoptimized_result_label],
                Keywords.optimized: final_information_dict[optimized_result_label],
            }

        if common_flux_name_index_dict is None:
            common_flux_name_index_dict = final_result_obj.final_flux_name_index_dict[optimized_result_label]
        else:
            new_flux_name_index_dict = final_result_obj.final_flux_name_index_dict[optimized_result_label]
            assert len(new_flux_name_index_dict) == len(common_flux_name_index_dict)
    if config.verify_result:
        result_verification(solver_dict, raw_solution_data_dict, raw_loss_data_dict, raw_final_predicted_data_dict)
    time_distribution_plotting(
        result_name, normal_time_data_dict, final_result_obj.this_result_output_direct)
    experimental_mid_prediction(
        result_name, normal_mid_prediction_dict,
        final_result_obj.final_target_experimental_mid_data_dict, final_result_obj.mid_prediction_output_direct)
    loss_data_distribution_plotting(
        result_name, normal_loss_data_dict, final_result_obj.this_result_output_direct)
    best_solution_generator(
        result_name, normal_loss_data_dict[Keywords.optimized], normal_solution_data_dict[Keywords.optimized],
        common_flux_name_index_dict)
    solution_embedding_and_visualization(
        result_name, normal_solution_data_dict, normal_loss_data_dict, final_result_obj.this_result_output_direct,
        common_flux_name_index_dict, simulated_flux_value_dict)
    # solution_embedding_and_visualization(
    #     result_name, squared_solution_data_dict, squared_loss_data_dict, final_result_obj.this_result_output_direct,
    #     common_flux_name_index_dict, simulated_flux_value_dict,
    #     optimized_num_for_embedding, unoptimized_num_for_embedding, squared_loss=True)

    output_mid_prediction_dict = {}
    output_experimental_mid_dict = {}
    output_information_dict = {}
    output_flux_name_index_dict = {Keywords.top_100: the_only_flux_name_index_dict}
    output_information_label_set = raw_output_information_dict[Keywords.optimized].keys() - {
        Keywords.loss, Keywords.miscellaneous}
    output_solution_data_dict = dict(normal_solution_data_dict)
    output_loss_data_dict = dict(normal_loss_data_dict)
    for optimization_label, each_optimization_data_dict in normal_mid_prediction_dict.items():
        bare_optimization_data_dict = each_optimization_data_dict.values().__iter__().__next__()
        output_mid_prediction_dict[optimization_label] = bare_optimization_data_dict
        output_experimental_mid_dict[optimization_label] = the_only_experimental_mid_dict
        output_flux_name_index_dict[optimization_label] = the_only_flux_name_index_dict
        output_information_dict[optimization_label] = {
            key: value for key, value in raw_output_information_dict[optimization_label].items()
            if key in output_information_label_set}
    optimized_solution_data_array = normal_solution_data_dict[Keywords.optimized]
    optimized_loss_data_array = normal_loss_data_dict[Keywords.optimized]
    top_100_data_index = np.argsort(optimized_loss_data_array)[:100]
    output_loss_data_dict[Keywords.top_100] = optimized_loss_data_array[top_100_data_index]
    output_solution_data_dict[Keywords.top_100] = optimized_solution_data_array[top_100_data_index]
    output_information_dict[Keywords.top_100] = output_information_dict[Keywords.optimized]
    output_predicted_mid_data(
        final_result_obj.mid_prediction_result_output_xlsx_path, normal_loss_data_dict, output_mid_prediction_dict,
        output_experimental_mid_dict, output_information_dict, subset_index_dict=None)
    output_raw_flux_data(
        final_result_obj.flux_result_output_xlsx_path, output_loss_data_dict,
        output_solution_data_dict, output_flux_name_index_dict,
        output_information_dict, subset_index_dict=None, other_label_column_dict=None)


def best_solution_generator(result_name, loss_data_vector, solution_data_matrix, flux_name_index_dict):
    best_solution_index = loss_data_distribution_plotting(result_name, {'': loss_data_vector}, select_num=1)[''][0]
    best_solution_raw_data = FigureData(FigureDataKeywords.best_solution, result_name)
    best_solution_raw_data.save_data(
        best_loss_data=loss_data_vector[best_solution_index],
        best_solution_vector=solution_data_matrix[best_solution_index],
        flux_name_index_dict=flux_name_index_dict)


def solution_embedding_and_visualization(
        result_name, solution_data_dict, loss_data_dict, output_direct, common_flux_name_index_dict,
        simulated_flux_value_dict, optimized_embedding_num=None, unoptimized_embedding_num=None, squared_loss=False):
    def calculate_distance_between_best_solutions_and_random_fluxes(
            optimized_flux_solution, optimized_loss_array, unoptimized_flux_solution, unoptimized_loss_array):
        # num_of_optimized_solutions = 5
        num_of_optimized_solutions = 400
        best_flux_solution = optimized_flux_solution[0, :]
        # vertical_best_flux_solution = net_flux_matrix @ best_flux_solution.reshape([-1, 1])
        target_optimized_flux_solution = optimized_flux_solution[:num_of_optimized_solutions, :]
        target_optimized_loss_array = optimized_loss_array[:num_of_optimized_solutions]
        # difference_vector_to_optimized_flux_solution = target_optimized_flux_solution - best_flux_solution
        # difference_vector_to_unoptimized_flux_solution = unoptimized_flux_solution - best_flux_solution
        # distance_to_optimized_flux_solution = np.linalg.norm(
        #     difference_vector_to_optimized_flux_solution, axis=1)
        # distance_to_unoptimized_flux_solution = np.linalg.norm(
        #     difference_vector_to_unoptimized_flux_solution, axis=1)
        # distance_to_optimized_flux_solution = np.linalg.norm(
        #     best_flux_solution - target_optimized_flux_solution, axis=1)
        # distance_to_unoptimized_flux_solution = np.linalg.norm(
        #     best_flux_solution - unoptimized_flux_solution, axis=1)
        # return {
        #     Keywords.optimized: (
        #         difference_vector_to_optimized_flux_solution, distance_to_optimized_flux_solution,
        #         target_optimized_loss_array),
        #     Keywords.unoptimized: (
        #         difference_vector_to_unoptimized_flux_solution, distance_to_unoptimized_flux_solution,
        #         unoptimized_loss_array)
        # }
        core_best_flux_solution = best_flux_solution[normal_core_flux_index_array]
        vertical_net_best_flux_solution = net_flux_matrix @ best_flux_solution.reshape([-1, 1])
        (
            raw_target_optimized_distance, raw_target_optimized_diff_vector,
            filtered_net_target_optimized_distance, filtered_net_target_optimized_diff_vector
        ) = calculate_raw_and_net_distance(
            target_optimized_flux_solution, net_flux_matrix, core_best_flux_solution,
            reduced=False, vertical_net_target_flux_vector=vertical_net_best_flux_solution,
            core_flux_index_array=normal_core_flux_index_array)
        (
            raw_unoptimized_distance, raw_unoptimized_diff_vector,
            filtered_net_unoptimized_distance, filtered_net_unoptimized_diff_vector
        ) = calculate_raw_and_net_distance(
            unoptimized_flux_solution, net_flux_matrix, core_best_flux_solution,
            reduced=False, vertical_net_target_flux_vector=vertical_net_best_flux_solution,
            core_flux_index_array=normal_core_flux_index_array)
        return {
            Keywords.optimized: (
                filtered_net_target_optimized_diff_vector, raw_target_optimized_distance,
                filtered_net_target_optimized_distance, target_optimized_loss_array),
            Keywords.unoptimized: (
                filtered_net_unoptimized_diff_vector, raw_unoptimized_distance,
                filtered_net_unoptimized_distance, unoptimized_loss_array)
        }

    from figure_plotting_package.common.core_plotting_functions import cmap_mapper_generator, shape_category_list
    min_value = None
    max_value = 8
    cmap = 'copper'

    if squared_loss:
        result_name = f'{result_name}_{Keywords.squared_loss}'

    embedding_solution_index_dict = {}
    if optimized_embedding_num is None:
        optimized_embedding_num = len(loss_data_dict[Keywords.optimized])
    embedding_solution_index_dict.update(loss_data_distribution_plotting(
        result_name, {Keywords.optimized: loss_data_dict[Keywords.optimized]},
        select_num=optimized_embedding_num))
    if unoptimized_embedding_num is not None:
        # embedding_solution_index_dict.update(loss_data_distribution_plotting(
        #     result_name, {Keywords.unoptimized: loss_data_dict[Keywords.unoptimized]},
        #     select_num=unoptimized_embedding_num))
        embedding_solution_index_dict.update(
            {Keywords.unoptimized: np.random.choice(
                len(loss_data_dict[Keywords.unoptimized]), unoptimized_embedding_num, replace=False)}
        )

    # net_flux_matrix, flux_name_list, _, filtered_solution_flux_index = net_flux_matrix_generator(
    #     net_flux_list, common_flux_name_index_dict, simulated_flux_value_dict)
    *_, formal_flux_name_list, net_flux_matrix, normal_core_flux_index_array = analyze_simulated_flux_value_dict(
        simulated_flux_value_dict, net_flux_list, normal_flux_name_index_dict=common_flux_name_index_dict)
    scatter_data_dict = {}
    size_dict = {Keywords.optimized: 10, Keywords.unoptimized: 3}
    new_loss_data_dict = {}

    color_mapper, _ = cmap_mapper_generator(cmap, min_value=min_value, max_value=max_value)
    # learn_obj = manifold.MDS(n_components=2, n_jobs=-1, max_iter=1000)
    # learn_obj = manifold.TSNE(n_components=2, n_jobs=-1, learning_rate=50)
    learn_obj = decomposition.PCA(n_components=2)
    solution_data_location_dict = {}
    start = 0
    complete_solution_data_list = []
    complete_distance_dict = {}
    filtered_solution_data_dict = {}
    filtered_loss_data_dict = {}
    for index, (result_label, solution_data_array) in enumerate(solution_data_dict.items()):
        loss_array = loss_data_dict[result_label]
        if result_label in embedding_solution_index_dict:
            subset_index = embedding_solution_index_dict[result_label]
            solution_data_array = solution_data_array[subset_index, :]
            loss_array = loss_array[subset_index]
        filtered_solution_data_dict[result_label] = solution_data_array
        filtered_loss_data_dict[result_label] = loss_array
        data_size = len(loss_array)
        distance_list = []
        for i in range(1, data_size):
            diff = solution_data_array[0:data_size - i, :] - solution_data_array[i:data_size, :]
            distance_list.extend(np.linalg.norm(diff, axis=1))
        complete_distance_dict[result_label] = np.array(distance_list)
        new_loss_data_dict[result_label] = loss_array
        color_array = color_mapper.to_rgba(loss_array)
        end = start + len(solution_data_array)
        solution_data_location_dict[result_label] = (start, end)
        start = end
        complete_solution_data_list.append(solution_data_array)
        scatter_data_dict[result_label] = (
            color_array, size_dict[result_label], shape_category_list[index])

    complete_solution_data_array = np.vstack(complete_solution_data_list)
    embedded_flux_matrix = learn_obj.fit_transform(complete_solution_data_array)
    embedded_flux_data_dict = {}
    for result_label, (start, end) in solution_data_location_dict.items():
        current_embedded_flux_matrix = embedded_flux_matrix[start:end]
        embedded_flux_data_dict[result_label] = current_embedded_flux_matrix
        scatter_data_dict[result_label] = (current_embedded_flux_matrix, *scatter_data_dict[result_label])
    separated_distance_and_loss_dict = calculate_distance_between_best_solutions_and_random_fluxes(
        filtered_solution_data_dict[Keywords.optimized], filtered_loss_data_dict[Keywords.optimized],
        filtered_solution_data_dict[Keywords.unoptimized], filtered_loss_data_dict[Keywords.unoptimized])
    if not squared_loss:
        scatter_plot_for_simulated_result(scatter_data_dict, output_direct=output_direct, color_mapper=color_mapper)

    embedding_visualization_raw_data = FigureData(FigureDataKeywords.embedding_visualization, result_name)
    embedding_visualization_raw_data.save_data(
        embedded_flux_data_dict=embedded_flux_data_dict,
        complete_distance_dict=complete_distance_dict,
        separated_distance_and_loss_dict=separated_distance_and_loss_dict,
        flux_name_list=formal_flux_name_list,
    )


def important_flux_display(
        result_name, raw_solution_data_dict, final_mapping_dict, data_model_object, final_flux_name_index_dict,
        flux_comparison_output_direct, subset_index_dict=None):
    reconstructed_solution_data_dict, reconstructed_flux_name_index_dict = reconstruct_and_filter_data_dict(
        raw_solution_data_dict, final_flux_name_index_dict, final_mapping_dict, subset_index_dict)
    final_dict_for_comparison, final_key_name_parameter_dict, final_color_dict = \
        data_model_object.flux_comparison_parameter_generator(
            reconstructed_solution_data_dict, reconstructed_flux_name_index_dict)
    for comparison_name, data_dict_for_plotting in final_dict_for_comparison.items():
        current_labeling_data_output_folder = '{}/{}'.format(flux_comparison_output_direct, comparison_name)
        check_and_mkdir_of_direct(current_labeling_data_output_folder)
        color_dict = final_color_dict[comparison_name]
        group_violin_box_distribution_plot(
            data_dict_for_plotting, nested_color_dict=color_dict, nested_median_color_dict=color_dict,
            title_dict=None, output_direct=current_labeling_data_output_folder, ylim=None, figsize=None,
            xaxis_rotate=True, figure_type='box')
    figure_raw_data = FigureData(FigureDataKeywords.flux_comparison, result_name)
    figure_raw_data.save_data(
        final_dict_for_comparison=final_dict_for_comparison,
        final_key_name_parameter_dict=final_key_name_parameter_dict)


def metabolic_network_plotting(
        result_name, data_model_object, final_solution_data_dict, final_flux_name_index_dict, figure_output_direct,
        subset_index_dict=None):
    initialize_figure_plotting()
    global figure_plotting
    (
        experimental_mid_metabolite_set, experimental_mixed_mid_metabolite_set, biomass_metabolite_set,
        input_metabolite_set, c13_labeling_metabolite_set, boundary_flux_set, infusion
    ) = data_model_object.metabolic_network_parameter_generator()
    raw_flux_value_dict = {}
    for raw_result_label, raw_solution_data_array in final_solution_data_dict.items():
        if subset_index_dict is not None:
            subset_index = subset_index_dict[raw_result_label]
            solution_data_array = raw_solution_data_array[subset_index]
        else:
            solution_data_array = raw_solution_data_array
        current_data_array = solution_data_array.mean(axis=0)
        current_reaction_value_dict = {
            flux_name: current_data_array[flux_index]
            for flux_name, flux_index in final_flux_name_index_dict[raw_result_label].items()}
        raw_flux_value_dict[raw_result_label] = current_reaction_value_dict

        # output_file_path = f'{figure_output_direct}/metabolic_network_{raw_result_label}.pdf'
        figure_name = f'metabolic_network_{raw_result_label}'
        figure_plotting.metabolic_flux_model_function(
            figure_output_direct, figure_name,
            input_metabolite_set, c13_labeling_metabolite_set, experimental_mid_metabolite_set,
            experimental_mixed_mid_metabolite_set,
            biomass_metabolite_set, boundary_flux_set, current_reaction_value_dict=current_reaction_value_dict,
            infusion=infusion, figure_size=(8.5, 8.5))
    figure_raw_data = FigureData(FigureDataKeywords.raw_flux_value_dict, result_name)
    figure_raw_data.save_data(raw_flux_value_dict=raw_flux_value_dict)


def experimental_mid_and_raw_data_plotting(
        complete_experimental_mid_data_obj_dict, result_information_dict, final_result_obj):
    final_result_obj.data_model_object.experimental_data_plotting(
        complete_experimental_mid_data_obj_dict, result_information_dict,
        final_result_obj.raw_and_mid_experimental_data_display_direct)


def mid_grid_plotting(
        result_name, final_predicted_data_dict, data_model_object, mid_prediction_output_direct,
        figure_config_dict=None):
    initialize_figure_plotting()
    global figure_plotting
    figure_size = (8.5, 11)
    if figure_config_dict is None:
        figure_config_dict = {}
    for result_label in final_predicted_data_dict.keys():
        figure_plotting.mid_prediction_function(
            result_name, result_label, data_model_object.mid_name_list, mid_prediction_output_direct,
            figure_config_dict, figure_size)


def multi_tumor_comparison_plotting(result_name, flux_comparison_output_direct):
    initialize_figure_plotting()
    global figure_plotting
    figure_size = (8.5, 11)
    multi_tumor_flux_comparison_nested_list = [
        [Keywords.tca_index, Keywords.cancer_index, Keywords.non_canonical_tca_index],
        ['GLC_input', 'SHMT_c - SHMT_c__R', Keywords.net_r5p_production]
    ]
    figure_plotting.multi_tumor_figure_plotting(
        'multi_tumor', multi_tumor_flux_comparison_nested_list, flux_comparison_output_direct, figure_size)

