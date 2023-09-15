from scripts.src.common.classes import FinalResult
from scripts.src.common.plotting_functions import group_violin_box_distribution_plot, group_bar_plot, \
    scatter_plot_for_simulated_result, FigurePlotting
from scripts.src.common.config import Color, Direct, Keywords
from scripts.src.common.third_party_packages import np, pd, manifold, decomposition
from scripts.src.common.result_processing_functions import experimental_mid_prediction

from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.figure_data_format import FigureData
from common_and_plotting_functions.config import FigureDataKeywords
from common_and_plotting_functions.core_plotting_functions import cmap_mapper_generator, shape_category_list
from ..common.result_processing_functions import loss_data_distribution_plotting, reconstruct_and_filter_data_dict, \
    time_distribution_plotting, result_verification
from ..common.result_output_functions import output_raw_flux_data, output_predicted_mid_data

from . import config

figure_plotting: FigurePlotting = None


def initialize_figure_plotting():
    global figure_plotting
    if figure_plotting is not None:
        return
    from figures.figure_plotting.common.config import ParameterName
    from figures.figure_plotting.figure_elements.element_dict import element_dict, ElementName
    figure_plotting = FigurePlotting(ParameterName, ElementName, element_dict)


def result_label_generator(mfa_data, obj_threshold):
    if obj_threshold == Keywords.unoptimized:
        return f'{mfa_data.data_name}__{Keywords.unoptimized}'
    else:
        return mfa_data.data_name


class CurrentFinalResult(FinalResult):
    def __init__(
            self, project_output_direct, common_data_output_direct, result_name, data_model_object):
        super(CurrentFinalResult, self).__init__(project_output_direct, common_data_output_direct, result_name, None)
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

    if config.verify_result:
        result_verification(solver_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict)
    subset_index_dict = loss_data_distribution_plotting(
        result_name, final_loss_data_dict,
        output_direct=final_result_obj.this_result_output_direct, loss_percentile=config.loss_percentile)
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


def hct116_result_process(final_result_obj, final_mapping_dict, solver_dict):
    optimized_num_for_analysis = 400
    unoptimized_num_for_mid_prediction = 400
    # unoptimized_num_for_embedding = 500
    # optimized_num_for_embedding = 30
    unoptimized_num_for_embedding = 400
    optimized_num_for_embedding = 400
    # parallel_num = 6
    parallel_num = 16

    result_name = final_result_obj.result_name
    final_information_dict = final_result_obj.final_information_dict
    raw_final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    raw_loss_data_dict = final_result_obj.final_loss_data_dict
    raw_solution_data_dict = final_result_obj.final_solution_data_dict
    raw_time_data_dict = final_result_obj.final_time_data_dict
    mid_prediction_dict = {}
    loss_data_dict = {}
    solution_data_dict = {}
    time_data_dict = {}
    flux_name_index_dict = None
    for result_label, (
            experiments_key, condition_key, repeat_index, unoptimized_result_label) in final_mapping_dict.items():
        if unoptimized_result_label is not None:
            total_size = len(raw_loss_data_dict[unoptimized_result_label])
            random_unoptimized_index = np.random.choice(total_size, unoptimized_num_for_mid_prediction, replace=False)
            current_predicted_data_dict = raw_final_predicted_data_dict[unoptimized_result_label]
            filtered_predicted_data_dict = {}
            for mid_title, current_predicted_data_array_list in current_predicted_data_dict.items():
                filtered_predicted_data_dict[mid_title] = np.array(current_predicted_data_array_list)[
                    random_unoptimized_index, :]
            mid_prediction_dict[Keywords.unoptimized] = {result_label: filtered_predicted_data_dict}
            loss_data_dict[Keywords.unoptimized] = raw_loss_data_dict[unoptimized_result_label]
            solution_data_dict[Keywords.unoptimized] = raw_solution_data_dict[unoptimized_result_label]
        total_size = len(raw_loss_data_dict[result_label])
        if total_size > optimized_num_for_analysis:
            random_optimized_index = np.random.choice(total_size, optimized_num_for_analysis, replace=False)
            filtered_predicted_data_dict = {}
            for mid_title, current_predicted_data_array_list in raw_final_predicted_data_dict[result_label].items():
                filtered_predicted_data_dict[mid_title] = np.array(current_predicted_data_array_list)[
                    random_optimized_index, :]
            filtered_loss_data = raw_loss_data_dict[result_label][random_optimized_index]
            filtered_solution_data = raw_solution_data_dict[result_label][random_optimized_index, :]
            filtered_time_data = raw_time_data_dict[result_label][random_optimized_index]
        else:
            filtered_predicted_data_dict = raw_final_predicted_data_dict[result_label]
            filtered_loss_data = raw_loss_data_dict[result_label]
            filtered_solution_data = raw_solution_data_dict[result_label]
            filtered_time_data = raw_time_data_dict[result_label]
        mid_prediction_dict[Keywords.optimized] = {result_label: filtered_predicted_data_dict}
        loss_data_dict[Keywords.optimized] = filtered_loss_data
        solution_data_dict[Keywords.optimized] = filtered_solution_data
        current_time_data_array = filtered_time_data
        time_data_dict[Keywords.optimized] = current_time_data_array / parallel_num
        if flux_name_index_dict is None:
            flux_name_index_dict = final_result_obj.final_flux_name_index_dict[result_label]
    if config.verify_result:
        result_verification(solver_dict, raw_solution_data_dict, raw_loss_data_dict, raw_final_predicted_data_dict)
    # time_distribution_plotting(
    #     result_name, time_data_dict, final_result_obj.this_result_output_direct)
    # experimental_mid_prediction(
    #     result_name, mid_prediction_dict,
    #     final_result_obj.final_target_experimental_mid_data_dict, final_result_obj.mid_prediction_output_direct)
    # loss_data_distribution_plotting(
    #     result_name, loss_data_dict, final_result_obj.this_result_output_direct)
    # best_solution_generator(
    #     result_name, loss_data_dict[Keywords.optimized], solution_data_dict[Keywords.optimized],
    #     flux_name_index_dict)
    # output_predicted_mid_data(
    #     final_result_obj.mid_prediction_result_output_xlsx_path, raw_loss_data_dict, raw_final_predicted_data_dict,
    #     final_result_obj.final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=None)
    # output_raw_flux_data(
    #     final_result_obj.flux_result_output_xlsx_path, raw_loss_data_dict,
    #     raw_solution_data_dict, final_result_obj.final_flux_name_index_dict,
    #     final_information_dict, subset_index_dict=None, other_label_column_dict=None)
    solution_embedding_and_visualization(
        result_name, solution_data_dict, loss_data_dict, final_result_obj.this_result_output_direct,
        optimized_num_for_embedding, unoptimized_num_for_embedding)


def best_solution_generator(result_name, loss_data_vector, solution_data_matrix, flux_name_index_dict):
    best_solution_index = loss_data_distribution_plotting(result_name, {'': loss_data_vector}, select_num=1)[''][0]
    best_solution_raw_data = FigureData(FigureDataKeywords.best_solution, result_name)
    best_solution_raw_data.save_data(
        best_loss_data=loss_data_vector[best_solution_index],
        best_solution_vector=solution_data_matrix[best_solution_index],
        flux_name_index_dict=flux_name_index_dict)


def solution_embedding_and_visualization(
        result_name, solution_data_dict, loss_data_dict, output_direct, optimized_embedding_num=None,
        unoptimized_embedding_num=None):
    def calculate_distance_between_best_solutions_and_random_fluxes(
            optimized_flux_solution, optimized_loss_array, unoptimized_flux_solution, unoptimized_loss_array):
        # num_of_optimized_solutions = 5
        num_of_optimized_solutions = 400
        best_flux_solution = optimized_flux_solution[0, :]
        target_optimized_flux_solution = optimized_flux_solution[:num_of_optimized_solutions, :]
        target_optimized_loss_array = optimized_loss_array[:num_of_optimized_solutions]
        distance_to_optimized_flux_solution = np.linalg.norm(
            best_flux_solution - target_optimized_flux_solution, axis=1)
        distance_to_unoptimized_flux_solution = np.linalg.norm(
            best_flux_solution - unoptimized_flux_solution, axis=1)
        return {
            Keywords.optimized: (distance_to_optimized_flux_solution, target_optimized_loss_array),
            Keywords.unoptimized: (distance_to_unoptimized_flux_solution, unoptimized_loss_array)
        }

    min_value = None
    max_value = 8
    cmap = 'copper'

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
    scatter_plot_for_simulated_result(scatter_data_dict, output_direct=output_direct, color_mapper=color_mapper)
    separated_distance_and_loss_dict = calculate_distance_between_best_solutions_and_random_fluxes(
        filtered_solution_data_dict[Keywords.optimized], filtered_loss_data_dict[Keywords.optimized],
        filtered_solution_data_dict[Keywords.unoptimized], filtered_loss_data_dict[Keywords.unoptimized])
    embedding_visualization_raw_data = FigureData(FigureDataKeywords.embedding_visualization, result_name)
    embedding_visualization_raw_data.save_data(
        embedded_flux_data_dict=embedded_flux_data_dict,
        complete_distance_dict=complete_distance_dict,
        separated_distance_and_loss_dict=separated_distance_and_loss_dict,
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

        output_file_path = f'{figure_output_direct}/metabolic_network_{raw_result_label}.pdf'
        figure_plotting.metabolic_flux_model_function(
            output_file_path, (8.5, 8.5),
            input_metabolite_set, c13_labeling_metabolite_set, experimental_mid_metabolite_set,
            experimental_mixed_mid_metabolite_set,
            biomass_metabolite_set, boundary_flux_set, current_reaction_value_dict=current_reaction_value_dict,
            infusion=infusion)
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

