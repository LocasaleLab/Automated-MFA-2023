from scripts.src.common.built_in_packages import abc
from scripts.src.common.third_party_packages import np
from scripts.src.common.config import Color, Direct, Keywords as CommonKeywords, random_seed, FigureData, \
    traditional_method_optimize_size
from scripts.src.common.classes import FinalResult
from scripts.src.common.plotting_functions import group_violin_box_distribution_plot, \
    multi_row_col_scatter_plot_for_result_selection, heat_map_plotting, HeatmapValueFormat
from scripts.src.common.functions import add_empty_obj
from scripts.src.common.result_processing_functions import loss_data_distribution_plotting, experimental_mid_prediction
from ..common.result_output_functions import output_raw_flux_data, output_predicted_mid_data
from ..common.functions import analyze_simulated_flux_value_dict, link_flux_name, \
    determine_order_by_specific_data_dict, calculate_raw_and_net_distance

from figure_plotting_package.common.core_plotting_functions import heatmap_and_box3d_parameter_preparation
from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.config import FigureDataKeywords, DefaultDict

from scripts.src.core.common.config import CoreConstants
from .sensitivity_config import ExperimentName, ModelSetting, DataSetting, Keywords, averaged_solution_data_obj
from . import config
from .boundary_condition_generation import base_flux_range

raw_type = Keywords.raw_type


def result_label_generator(model_label, data_label, config_label=raw_type):
    if config_label == raw_type:
        return '{}__{}'.format(model_label, data_label)
    else:
        return '{}__{}__{}'.format(model_label, data_label, config_label)


raw_model_data_result_label_dict = {
    result_label_generator(ModelSetting.raw_model, DataSetting.raw_data): ExperimentName.raw_model_raw_data,
    result_label_generator(ModelSetting.raw_model, DataSetting.all_data): ExperimentName.raw_model_all_data,
}


def result_information_generator(model_information, data_information, config_information=raw_type):
    return {
        Keywords.model: model_information,
        Keywords.data: data_information,
        Keywords.config: config_information
    }


class CurrentFinalResult(FinalResult):
    def __init__(
            self, project_output_direct, common_data_output_direct, result_name, suffix=None):
        super(CurrentFinalResult, self).__init__(
            project_output_direct, common_data_output_direct, result_name, suffix=suffix)

    def _generate_path(self, current_result_label):
        if current_result_label in raw_model_data_result_label_dict:
            current_result_path = '{}/{}/{}/{}'.format(
                self.project_output_direct, raw_model_data_result_label_dict[current_result_label],
                Direct.raw_flux_analysis, current_result_label)
        else:
            current_result_path = '{}/{}'.format(self.raw_result_data_output_direct, current_result_label)
        check_and_mkdir_of_direct(current_result_path)
        return self._generate_path_given_result_path(current_result_path)

    def repair_predicted_mid_dict(self, solver_dict, result_process_name):
        if result_process_name != Keywords.raw_model_result_process:
            solver_dict_for_repair = {
                result_label: solver_obj for result_label, solver_obj in solver_dict.items()
                if result_label not in raw_model_data_result_label_dict}
        else:
            solver_dict_for_repair = solver_dict
        super().repair_predicted_mid_dict_and_merge(solver_dict_for_repair)

    def final_process(
            self, solver_dict, final_information_dict, result_process_name, result_process_func,
            each_case_target_optimization_num, *args, extra_result_suffix=False, **kwargs):
        self.final_information_dict = final_information_dict
        if each_case_target_optimization_num is None:
            raw_data_analyzing_num = 0
        else:
            raw_data_analyzing_num = each_case_target_optimization_num
        for current_result_label in solver_dict.keys():
            if extra_result_suffix:
                extra_result_suffix_tuple = Keywords.extra_result_suffix_tuple
            else:
                extra_result_suffix_tuple = ()
            (
                loss_data_array, solution_data_array, flux_name_index_dict, _,
                predicted_data_dict, target_experimental_mid_data_dict, _) = self.iteration(
                current_result_label, result_label_suffix_tuple=extra_result_suffix_tuple)
            if current_result_label in raw_model_data_result_label_dict:
                total_data_size = len(loss_data_array)
                if result_process_name != Keywords.raw_model_result_process and \
                        total_data_size > raw_data_analyzing_num:
                    analyzed_index_array = random_seed.choice(
                        total_data_size, raw_data_analyzing_num, replace=False)
                    loss_data_array = loss_data_array[analyzed_index_array]
                    solution_data_array = solution_data_array[analyzed_index_array, :]
                    new_predicted_data_dict = {}
                    for flux_name, mid_data_list in predicted_data_dict.items():
                        new_predicted_data_dict[flux_name] = [
                            mid_data_list[data_index] for data_index in analyzed_index_array]
                    predicted_data_dict = new_predicted_data_dict
            else:
                raw_data_analyzing_num = np.maximum(raw_data_analyzing_num, len(loss_data_array))
            (
                self.final_loss_data_dict[current_result_label],
                self.final_solution_data_dict[current_result_label],
                self.final_flux_name_index_dict[current_result_label],
                self.final_predicted_data_dict[current_result_label],
                self.final_target_experimental_mid_data_dict[current_result_label]) = (
                loss_data_array, solution_data_array, flux_name_index_dict,
                predicted_data_dict, target_experimental_mid_data_dict
            )

        result_process_func(self, solver_dict, *args, **kwargs)


def data_sensitivity_result_process(
        final_result_obj, solver_dict, important_flux_list,
        important_flux_replace_dict, net_flux_list, loss_percentile, common_simulated_flux_value_dict, *other_args,
        **kwargs):

    final_information_dict = final_result_obj.final_information_dict
    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    final_solution_data_dict = final_result_obj.final_solution_data_dict
    final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    final_flux_name_index_dict = final_result_obj.final_flux_name_index_dict
    final_target_experimental_mid_data_dict = final_result_obj.final_target_experimental_mid_data_dict
    processed_mid_name_dict = final_result_obj.processed_mid_name_dict
    flux_range = base_flux_range

    analyzed_set_size_list = config.data_sensitivity_simulated_analyzed_set_size_list
    selected_min_loss_size_list = config.selected_min_loss_size_list
    repeat_time_each_analyzed_set = config.data_sensitivity_repeat_time_each_analyzed_set

    this_result_output_direct = final_result_obj.this_result_output_direct
    flux_comparison_output_direct = final_result_obj.flux_comparison_output_direct
    flux_result_output_xlsx_path = final_result_obj.flux_result_output_xlsx_path
    mid_prediction_result_output_xlsx_path = final_result_obj.mid_prediction_result_output_xlsx_path

    # subset_index_dict = loss_data_distribution_plotting(
    #     result_name, final_loss_data_dict, output_direct=this_result_output_direct,
    #     loss_percentile=loss_percentile)
    # output_raw_flux_data(
    #     flux_result_output_xlsx_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
    #     final_information_dict, subset_index_dict=subset_index_dict)
    # output_predicted_mid_data(
    #     mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
    #     final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=subset_index_dict)
    # important_flux_display(
    #     final_solution_data_dict, final_flux_name_index_dict, final_information_dict,
    #     important_flux_list, common_simulated_flux_value_dict, important_flux_replace_dict,
    #     flux_comparison_output_direct, subset_index_dict=subset_index_dict)
    # # normal_flux_euclidean_distance_plotting(
    # #     final_solution_data_dict, final_flux_name_index_dict,
    # #     simulated_flux_value_dict, net_flux_list, subset_index_dict=subset_index_dict)
    # all_fluxes_relative_error_heatmap(
    #     result_name, flux_comparison_output_direct, final_solution_data_dict, final_flux_name_index_dict,
    #     common_simulated_flux_value_dict, net_flux_list, important_flux_replace_dict, subset_index_dict)
    data_sensitivity_result_processing(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, final_flux_name_index_dict,
        common_simulated_flux_value_dict, analyzed_set_size_list,
        selected_min_loss_size_list, repeat_time_each_analyzed_set,
        net_flux_list, important_flux_replace_dict, flux_range, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path)


def raw_model_result_process(
        final_result_obj, solver_dict, important_flux_list,
        important_flux_replace_dict, mfa_config, net_flux_list, common_simulated_flux_value_dict, *other_args,
        **kwargs):

    analyzed_set_size_list = config.analyzed_set_size_list
    repeat_time_each_analyzed_set = config.repeat_time_each_analyzed_set
    selected_min_loss_size_list = config.selected_min_loss_size_list
    test_mode = config.test_raw_model_analysis
    flux_range = mfa_config.common_flux_range

    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    this_result_output_direct = final_result_obj.this_result_output_direct
    flux_result_output_xlsx_path = final_result_obj.flux_result_output_xlsx_path
    mid_prediction_result_output_xlsx_path = final_result_obj.mid_prediction_result_output_xlsx_path
    # raw_model_prediction(
    #     result_name, final_loss_data_dict, final_predicted_data_dict, final_target_experimental_mid_data_dict,
    #     500, 10, mid_prediction_output_direct)
    assert len(final_loss_data_dict) == 1
    result_label, loss_data_array = final_loss_data_dict.items().__iter__().__next__()
    raw_model_solver = solver_dict[result_label]
    solution_data_array = final_result_obj.final_solution_data_dict[result_label]
    flux_name_index_dict = final_result_obj.final_flux_name_index_dict[result_label]
    information_dict = final_result_obj.final_information_dict[result_label]
    predicted_data_dict = final_result_obj.final_predicted_data_dict[result_label]
    target_experimental_mid_data_dict = final_result_obj.final_target_experimental_mid_data_dict[result_label]
    processed_mid_name_dict = final_result_obj.processed_mid_name_dict

    raw_model_result_processing_func(
        result_name, raw_model_solver, loss_data_array, solution_data_array, flux_name_index_dict, information_dict,
        predicted_data_dict, processed_mid_name_dict, target_experimental_mid_data_dict,
        common_simulated_flux_value_dict, important_flux_list, important_flux_replace_dict,
        analyzed_set_size_list, selected_min_loss_size_list,
        repeat_time_each_analyzed_set, flux_range, this_result_output_direct, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path, net_flux_list, test_mode=test_mode)


def raw_model_optimization_from_averaged_solution_result_process(
        final_result_obj, solver_dict, important_flux_list,
        important_flux_replace_dict, mfa_config, net_flux_list, common_simulated_flux_value_dict, *other_args,
        **kwargs):
    flux_range = mfa_config.common_flux_range
    final_information_dict = final_result_obj.final_information_dict
    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    final_solution_data_dict = final_result_obj.final_solution_data_dict
    final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    common_flux_name_index_dict = final_result_obj.final_flux_name_index_dict.values().__iter__().__next__()
    processed_mid_name_dict = final_result_obj.processed_mid_name_dict

    analyzed_set_size_list = config.analyzed_set_size_list
    selected_min_loss_size_list = config.selected_min_loss_size_list

    optimization_from_averaged_solution_result_processing_func(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, common_flux_name_index_dict, common_simulated_flux_value_dict,
        net_flux_list, important_flux_replace_dict, analyzed_set_size_list, selected_min_loss_size_list, flux_range
    )


def raw_model_batched_simulated_data_result_process(
        final_result_obj, solver_dict, important_flux_list,
        important_flux_replace_dict, mfa_config, net_flux_list, nested_simulated_flux_value_dict_dict, *other_args,
        optimization_from_averaged_solutions=False, **kwargs):
    flux_range = mfa_config.common_flux_range
    final_information_dict = final_result_obj.final_information_dict
    result_name = final_result_obj.result_name
    final_loss_data_dict = final_result_obj.final_loss_data_dict
    final_solution_data_dict = final_result_obj.final_solution_data_dict
    final_predicted_data_dict = final_result_obj.final_predicted_data_dict
    common_flux_name_index_dict = final_result_obj.final_flux_name_index_dict.values().__iter__().__next__()
    processed_mid_name_dict = final_result_obj.processed_mid_name_dict

    flux_result_output_xlsx_path = final_result_obj.flux_result_output_xlsx_path
    mid_prediction_result_output_xlsx_path = final_result_obj.mid_prediction_result_output_xlsx_path

    analyzed_set_size_list = config.batched_simulated_analyzed_set_size_list
    selected_min_loss_size_list = config.selected_min_loss_size_list
    repeat_time_each_analyzed_set = config.batched_simulated_repeat_time_each_analyzed_set

    multiple_simulated_data_result_processing_func(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, common_flux_name_index_dict,
        nested_simulated_flux_value_dict_dict, analyzed_set_size_list,
        selected_min_loss_size_list, repeat_time_each_analyzed_set,
        net_flux_list, important_flux_replace_dict, flux_range, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path,
        optimization_from_averaged_solutions=optimization_from_averaged_solutions)


def important_flux_display(
        solution_array_dict, flux_name_index_dict, information_dict, important_flux_list, simulated_flux_value_dict,
        replace_flux_dict, flux_comparison_output_direct, subset_index_dict=None):
    final_data_dict = {}
    final_color_dict = {}
    simulated_flux_cutoff_value_dict = {}
    # raw_flux_name1 = ''
    # raw_flux_name2 = ''
    # simulated_flux_value = -1

    empty_array = np.array([np.nan, np.nan])
    for flux_name in important_flux_list:
        current_flux_data_dict = {}
        current_color_dict = {}

        simulated_flux_value, flux_title, reverse_order, common_flux_name = determine_order_by_specific_data_dict(
            flux_name, simulated_flux_value_dict)
        for result_label, solution_array in solution_array_dict.items():
            current_flux_name_index_dict = flux_name_index_dict[result_label]
            if subset_index_dict is not None:
                target_solution_array = solution_array[subset_index_dict[result_label], :]
            else:
                target_solution_array = solution_array
            final_data_array, real_flux_name = decipher_flux_title(
                flux_name, current_flux_name_index_dict, replace_flux_dict,
                target_solution_array, reverse_order)
            if real_flux_name != common_flux_name:
                result_label = link_flux_name(result_label, real_flux_name)
            current_flux_data_dict[result_label] = final_data_array
            current_color_dict[result_label] = Color.blue
        final_data_dict[flux_title] = current_flux_data_dict
        # final_color_dict[flux_title] = current_color_dict
        final_color_dict.update(current_color_dict)
        simulated_flux_cutoff_value_dict[flux_title] = simulated_flux_value

    group_violin_box_distribution_plot(
        final_data_dict, nested_color_dict=final_color_dict, nested_median_color_dict=final_color_dict,
        cutoff_dict=simulated_flux_cutoff_value_dict, title_dict=None,
        output_direct=flux_comparison_output_direct, ylim=None, xaxis_rotate=True,
        figsize=None, figure_type='box')
    return final_data_dict, final_color_dict, simulated_flux_cutoff_value_dict


def find_single_percentile_location_in_sorted_array(sorted_data_array, target_value, min_value, max_value):
    if target_value < min_value or target_value > max_value:
        raise ValueError(
            'Current value {} is not in the range: ({}, {})'.format(target_value, min_value, max_value))
    complete_size = len(sorted_data_array) + 1
    min_data = sorted_data_array[0]
    max_data = sorted_data_array[-1]
    if target_value <= min_data:
        current_percentile = 1 / complete_size * (target_value - min_value) / (min_data - min_value)
    elif target_value >= max_data:
        current_percentile = 1 - 1 / complete_size * (max_value - target_value) / (max_value - max_data)
    else:
        current_location = np.searchsorted(sorted_data_array, target_value)
        right_value = sorted_data_array[current_location]
        right_percentile = (current_location + 1) / complete_size
        left_value = sorted_data_array[current_location - 1]
        left_percentile = current_location / complete_size
        current_percentile = (
                (target_value - left_value) / (right_value - left_value) * (right_percentile - left_percentile)
                + left_percentile)
    return current_percentile


def find_percentile_location(complete_data_array_dict, target_value_list, current_range):
    def find_percentile_location_in_sorted_array(_raw_single_data_array, _target_value_list):
        # _complete_sorted_data_array = np.hstack([min_value, np.sort(_raw_single_data_array), max_value])
        _sorted_data_array = np.sort(_raw_single_data_array)
        if isinstance(_target_value_list, np.ndarray):
            return find_single_percentile_location_in_sorted_array(
                _sorted_data_array, _target_value_list, min_value, max_value)
        elif isinstance(_target_value_list, abc.Iterable):
            return [
                find_single_percentile_location_in_sorted_array(
                    _sorted_data_array, _target_value, min_value, max_value)
                for _target_value in _target_value_list]
        else:
            raise ValueError()

    raw_min_value, raw_max_value = current_range
    min_value = raw_min_value - CoreConstants.eps_for_computation
    max_value = raw_max_value + CoreConstants.eps_for_computation
    if isinstance(complete_data_array_dict, dict):
        sorted_complete_data_array_dict = {}
        for data_array_name, single_data_array in complete_data_array_dict.items():
            sorted_complete_data_array_dict[data_array_name] = find_percentile_location_in_sorted_array(
                single_data_array, target_value_list)
        return sorted_complete_data_array_dict
    elif isinstance(complete_data_array_dict, np.ndarray):
        return find_percentile_location_in_sorted_array(complete_data_array_dict, target_value_list)
    else:
        raise ValueError()


def normalized_difference_to_array(
        raw_data_array, target_value, normalized_distance=None, reduced_metric=Keywords.median):
    if reduced_metric is None:
        reduced_value = raw_data_array
    elif reduced_metric == Keywords.median:
        reduced_value = np.median(raw_data_array)
    elif reduced_metric == Keywords.mean:
        reduced_value = np.mean(raw_data_array)
    else:
        raise ValueError()
    if normalized_distance is None:
        normalized_distance = target_value
    if abs(normalized_distance) < 1e-5:
        # ratio = np.nan
        ratio = (reduced_value - target_value) / 10
    else:
        ratio = (reduced_value - target_value) / normalized_distance
    return ratio


def euclidean_distance_of_mean_point_to_simulated_array(
        solution_data_array, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
        normal_core_flux_index_array):
    vertical_net_simulated_flux_vector = simulated_net_flux_vector.reshape([-1, 1])
    # vertical_net_simulated_flux_vector = net_flux_matrix @ simulated_flux_vector.reshape([-1, 1])
    # if filtered_solution_flux_index is not None:
    #     solution_data_array = solution_data_array[:, filtered_solution_flux_index]
    (
        raw_all_select_euclidean_distance_array, _, net_all_select_euclidean_distance_array,
        net_all_select_diff_vector) = calculate_raw_and_net_distance(
        solution_data_array, net_flux_matrix, simulated_flux_vector, vertical_net_simulated_flux_vector,
        reduced=False, core_flux_index_array=normal_core_flux_index_array)
    simulated_net_vector_for_normalization = np.sign(simulated_net_flux_vector + 1e-6) * np.clip(
        np.abs(simulated_net_flux_vector), a_min=10, a_max=None)
    net_all_select_relative_ratio = net_all_select_diff_vector / simulated_net_vector_for_normalization
    mean_selected_solution_vector = solution_data_array.mean(axis=0)
    (
        raw_mean_euclidean_distance, _, net_mean_euclidean_distance,
        net_mean_diff_vector) = calculate_raw_and_net_distance(
        mean_selected_solution_vector, net_flux_matrix, simulated_flux_vector, vertical_net_simulated_flux_vector,
        reduced=False, core_flux_index_array=normal_core_flux_index_array)
    net_mean_relative_ratio = net_mean_diff_vector / simulated_net_vector_for_normalization
    return (
        raw_mean_euclidean_distance, net_mean_euclidean_distance, net_mean_diff_vector, net_mean_relative_ratio,
        raw_all_select_euclidean_distance_array, net_all_select_euclidean_distance_array, net_all_select_diff_vector,
        net_all_select_relative_ratio, )


# standard_flux_name should be flux name in simulated_flux_value_dict
def decipher_flux_title(
        standard_flux_name, flux_name_index_dict, replace_flux_dict, solution_array, reverse_order):
    empty_array = np.array([np.nan, np.nan])
    if isinstance(standard_flux_name, str):
        tmp_flux_name = standard_flux_name
        try:
            while tmp_flux_name not in flux_name_index_dict:
                tmp_flux_name = replace_flux_dict[tmp_flux_name]
        except KeyError:
            final_data_array = empty_array
            real_flux_name = ''
        else:
            current_flux_index = flux_name_index_dict[tmp_flux_name]
            final_data_array = solution_array[:, current_flux_index]
            real_flux_name = tmp_flux_name
    elif isinstance(standard_flux_name, (tuple, list)):
        final_data_array = 0
        tmp_flux_name0, tmp_flux_name1 = standard_flux_name
        failed_one = False
        failed_two = False
        try:
            while tmp_flux_name0 not in flux_name_index_dict:
                tmp_flux_name0 = replace_flux_dict[tmp_flux_name0]
        except KeyError:
            failed_one = True
        try:
            while tmp_flux_name1 not in flux_name_index_dict:
                tmp_flux_name1 = replace_flux_dict[tmp_flux_name1]
        except KeyError:
            failed_two = True
        if failed_one and failed_two:
            final_data_array = empty_array
            real_flux_name = ''
        else:
            if reverse_order:
                tmp_flux_name1, tmp_flux_name0 = tmp_flux_name0, tmp_flux_name1
            flux_name_list = []
            if tmp_flux_name0 in flux_name_index_dict:
                final_data_array += solution_array[:, flux_name_index_dict[tmp_flux_name0]]
                flux_name_list.append(tmp_flux_name0)
            if tmp_flux_name1 in flux_name_index_dict:
                final_data_array -= solution_array[:, flux_name_index_dict[tmp_flux_name1]]
                flux_name_list.append(tmp_flux_name1)
            real_flux_name = link_flux_name(*flux_name_list)
    else:
        raise ValueError()
    return final_data_array, real_flux_name


def raw_model_prediction(
        result_name, final_loss_data_dict, final_predicted_data_dict, final_target_experimental_mid_data_dict,
        analyzed_set_size, selected_min_loss_size, mid_prediction_output_direct):
    selected_predicted_data_dict = {}
    for result_label, loss_data_array in final_loss_data_dict.items():
        predicted_data_dict = final_predicted_data_dict[result_label]
        total_data_size = len(loss_data_array)
        complete_analyzed_index_set_array = random_seed.choice(
            total_data_size, analyzed_set_size, replace=False)
        sorted_index_of_index_array = np.argpartition(
            loss_data_array[complete_analyzed_index_set_array], selected_min_loss_size)
        selected_index_array = complete_analyzed_index_set_array[sorted_index_of_index_array][:selected_min_loss_size]
        final_loss_array = loss_data_array[selected_index_array]
        current_selected_predicted_data_dict = {}
        for mid_name, mid_array_list in predicted_data_dict.items():
            current_selected_predicted_data_dict[mid_name] = [
                mid_array_list[selected_index] for selected_index in selected_index_array]
        selected_predicted_data_dict[result_label] = current_selected_predicted_data_dict
    experimental_mid_prediction(
        result_name, {CommonKeywords.optimized: selected_predicted_data_dict},
        final_target_experimental_mid_data_dict, mid_prediction_output_direct, subset_index_dict=None)


def all_fluxes_relative_error_heatmap(
        result_name, flux_comparison_output_direct, final_solution_data_dict, final_flux_name_index_dict,
        simulated_flux_value_dict, net_flux_list, replace_flux_dict, subset_index_dict=None):
    def display_flux_name_generator(_modified_flux_name, _reverse_order):
        if isinstance(_modified_flux_name, tuple):
            _forward_flux_name = _modified_flux_name[0]
            if _forward_flux_name.endswith('__R'):
                _forward_flux_name = _modified_flux_name[1]
            if _reverse_order:
                _display_flux_name = f'{_forward_flux_name} Rnet'
            else:
                _display_flux_name = f'{_forward_flux_name} net'
        elif _modified_flux_name == 'BIOMASS_REACTION':
            _display_flux_name = 'Biomass'
        elif _modified_flux_name == 'Salvage_c':
            _display_flux_name = 'Salvage'
        else:
            _display_flux_name = _modified_flux_name
        return _display_flux_name

    distance_dict = {}
    result_label_list = list(final_solution_data_dict.keys())
    common_flux_name_list = []

    common_flux_name_simulated_value_dict = analyze_simulated_flux_value_dict(
        simulated_flux_value_dict, net_flux_list)

    flux_id_display_flux_name_dict = {}
    for common_flux_name, (modified_flux_name, simulated_flux_value, _, reverse_order) in \
            common_flux_name_simulated_value_dict.items():
        common_flux_name_list.append(common_flux_name)
        flux_id_display_flux_name_dict[common_flux_name] = display_flux_name_generator(
            modified_flux_name, reverse_order)
        for result_label, raw_solution_array in final_solution_data_dict.items():
            flux_name_index_dict = final_flux_name_index_dict[result_label]
            if subset_index_dict is not None:
                target_solution_array = raw_solution_array[subset_index_dict[result_label], :]
            else:
                target_solution_array = raw_solution_array
            final_data_array, real_flux_name = decipher_flux_title(
                modified_flux_name, flux_name_index_dict, replace_flux_dict, target_solution_array, reverse_order)
            if real_flux_name == '':
                relative_distance = np.nan
            else:
                relative_distance = normalized_difference_to_array(
                    final_data_array, simulated_flux_value, None, Keywords.mean)
            if result_label not in distance_dict:
                distance_dict[result_label] = {}
            distance_dict[result_label][common_flux_name] = relative_distance

    for flux_id, display_flux_name in flux_id_display_flux_name_dict.items():
        print(f"'{flux_id}': '{display_flux_name}',")

    distance_matrix = np.zeros([len(result_label_list), len(common_flux_name_list)])
    for row_index, result_label in enumerate(result_label_list):
        for col_index, common_flux_name in enumerate(common_flux_name_list):
            distance_matrix[row_index, col_index] = distance_dict[result_label][common_flux_name]
    heat_map_plotting(
        distance_matrix, common_flux_name_list, result_label_list, 'all_fluxes', flux_comparison_output_direct,
        min_value=-0.5, max_value=0.5, figsize=None, value_number_format=HeatmapValueFormat.no_text, xaxis_rotate=True)

    figure_raw_data = FigureData(FigureDataKeywords.all_fluxes_relative_error, result_name)
    figure_raw_data.save_data(
        distance_matrix=distance_matrix,
        common_flux_name_list=common_flux_name_list,
        result_label_list=result_label_list,
    )


def each_cycle_analyzer(
        analyzed_set_size, selected_min_loss_size,
        solution_data_array, loss_data_array, predicted_data_dict, solver_obj, flux_name_index_dict,
        common_flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
        normal_core_flux_index_array, total_data_size, replace_flux_dict, max_flux_diff,

        final_flux_absolute_distance_dict,
        final_flux_relative_distance_dict,
        final_raw_mean_euclidian_distance_dict,
        final_net_mean_euclidian_distance_dict,
        final_raw_all_select_euclidian_distance_dict,
        final_net_all_select_euclidian_distance_dict,
        maximal_absolute_distance_dict,
        maximal_relative_distance_dict,
        max_raw_euclidian_distance,
        max_net_euclidian_distance,
        raw_selected_flux_value_dict,
        selected_averaged_flux_value_dict,
        raw_selected_diff_vector_dict,
        selected_averaged_diff_vector_dict,
        net_all_selected_relative_error_dict,
        net_selected_averaged_relative_error_dict,
        raw_selected_loss_value_dict,
        loss_of_mean_solution_dict,
        processed_mid_name_dict,
        raw_selected_predicted_data_dict,
        selected_averaged_predicted_data_dict,
        max_loss_value,
        select_mode=True,
        sorted_index_array=None,
        repeat_time_each_analyzed_set=1,
):
    def calculate_ordered_selected_index_solution_each_cycle(
            analyzed_set_size, selected_min_loss_size, repeat_time_index):
        complete_analyzed_index_set_array = all_repeat_analyzed_index_set_array[
            repeat_time_index * analyzed_set_size:(repeat_time_index + 1) * analyzed_set_size].copy()
        complete_analyzed_index_set_array.sort()
        ordered_selected_index_array = sorted_index_array[
            complete_analyzed_index_set_array[:selected_min_loss_size]]
        ordered_selected_solution_data_array = solution_data_array[ordered_selected_index_array, :]
        add_empty_obj(
            raw_selected_flux_value_dict, list, analyzed_set_size, selected_min_loss_size).append(
            ordered_selected_solution_data_array)
        return ordered_selected_index_array, ordered_selected_solution_data_array

    def filter_each_mid_dict(
            input_predicted_data_dict, analyzed_set_size, selected_min_loss_size, current_ordered_selected_index_array,
            target_predicted_data_dict, append=False):
        for mid_name, mid_value_list in input_predicted_data_dict.items():
            current_output_predicted_mid_value_list = add_empty_obj(
                target_predicted_data_dict, list, selected_min_loss_size, analyzed_set_size, mid_name)
            if current_ordered_selected_index_array is not None:
                selected_mid_value_list = [
                    mid_value_list[selected_index] for selected_index in current_ordered_selected_index_array]
            else:
                selected_mid_value_list = mid_value_list
            if append:
                current_output_predicted_mid_value_list.append(selected_mid_value_list)
            else:
                current_output_predicted_mid_value_list.extend(selected_mid_value_list)

    def calculate_loss_and_mid_each_cycle(
            analyzed_set_size, selected_min_loss_size, current_ordered_selected_index_array,
            current_solution_data_array):
        if current_ordered_selected_index_array is not None:
            current_loss_array = loss_data_array[current_ordered_selected_index_array]
        else:
            current_loss_array = loss_data_array
        add_empty_obj(
            raw_selected_loss_value_dict, list, selected_min_loss_size, analyzed_set_size).append(
            current_loss_array)
        new_max_loss_value = max(max_loss_value, np.max(current_loss_array))
        filter_each_mid_dict(
            predicted_data_dict, analyzed_set_size, selected_min_loss_size, current_ordered_selected_index_array,
            raw_selected_predicted_data_dict, append=False)
        if selected_averaged_flux_value_dict is not None and loss_of_mean_solution_dict is not None:
            mean_solution = np.mean(current_solution_data_array, axis=0)
            add_empty_obj(
                selected_averaged_flux_value_dict, list, analyzed_set_size, selected_min_loss_size).append(
                mean_solution)
            loss_of_mean_solution = float(solver_obj.obj_eval(mean_solution))
            add_empty_obj(
                loss_of_mean_solution_dict, list, selected_min_loss_size, analyzed_set_size).append(loss_of_mean_solution)
            new_max_loss_value = max(new_max_loss_value, loss_of_mean_solution)
            if selected_averaged_predicted_data_dict is not None:
                raw_mid_dict_of_selected_averaged_solution = solver_obj.predict(mean_solution)
                mid_dict_of_selected_averaged_solution = {
                    processed_mid_name_dict[mid_name]: mid_value_list
                    for mid_name, mid_value_list in raw_mid_dict_of_selected_averaged_solution.items()
                    if mid_name in processed_mid_name_dict
                }
                filter_each_mid_dict(
                    mid_dict_of_selected_averaged_solution, analyzed_set_size, selected_min_loss_size,
                    None, selected_averaged_predicted_data_dict, append=True)
        return new_max_loss_value

    def calculate_distance_each_cycle(current_solution_data_array):
        (
            raw_mean_euclidean_distance, net_mean_euclidean_distance, net_mean_diff_vector, net_mean_relative_ratio,
            raw_all_select_euclidean_distance_array, net_all_select_euclidean_distance_array,
            net_all_select_diff_vector, net_all_select_relative_ratio
        ) = euclidean_distance_of_mean_point_to_simulated_array(
            current_solution_data_array, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
            normal_core_flux_index_array)
        if final_raw_all_select_euclidian_distance_dict is not None:
            add_empty_obj(
                final_raw_all_select_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size).append(
                raw_all_select_euclidean_distance_array)
        new_max_net_euclidian_distance = max(
            max_net_euclidian_distance, np.max(net_all_select_euclidean_distance_array))
        add_empty_obj(
            final_net_all_select_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size).append(
            net_all_select_euclidean_distance_array)
        add_empty_obj(
            raw_selected_diff_vector_dict, list, selected_min_loss_size, analyzed_set_size).append(
            net_all_select_diff_vector)
        new_max_raw_euclidian_distance = max(
            max_raw_euclidian_distance, np.max(raw_all_select_euclidean_distance_array))
        if final_raw_mean_euclidian_distance_dict is not None:
            add_empty_obj(
                final_raw_mean_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size).append(
                raw_mean_euclidean_distance)
            new_max_raw_euclidian_distance = max(
                new_max_raw_euclidian_distance, raw_mean_euclidean_distance)
        if final_net_mean_euclidian_distance_dict is not None:
            add_empty_obj(
                final_net_mean_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size).append(
                net_mean_euclidean_distance)
            new_max_net_euclidian_distance = max(
                new_max_net_euclidian_distance, net_mean_euclidean_distance)
        if selected_averaged_diff_vector_dict is not None:
            add_empty_obj(
                selected_averaged_diff_vector_dict, list, selected_min_loss_size, analyzed_set_size).append(
                net_mean_diff_vector)
        if net_all_selected_relative_error_dict is not None:
            add_empty_obj(
                net_all_selected_relative_error_dict, list, selected_min_loss_size, analyzed_set_size).append(
                net_all_select_relative_ratio)
        if net_selected_averaged_relative_error_dict is not None:
            add_empty_obj(
                net_selected_averaged_relative_error_dict, list, selected_min_loss_size, analyzed_set_size).append(
                net_mean_relative_ratio)
        return new_max_raw_euclidian_distance, new_max_net_euclidian_distance

    def calculate_flux_each_cycle(
            analyzed_set_size, selected_min_loss_size, empty=False, current_solution_data_array=None, reduced=True):
        if reduced:
            reduced_method = Keywords.mean
        else:
            reduced_method = None
        for flux_title, (modified_flux_name, simulated_flux_value, _, reverse_order) in \
                common_flux_name_simulated_value_dict.items():
            add_empty_obj(
                final_flux_absolute_distance_dict, list, flux_title, selected_min_loss_size,
                analyzed_set_size)
            add_empty_obj(
                final_flux_relative_distance_dict, list, flux_title, selected_min_loss_size,
                analyzed_set_size)
            if not empty:
                assert current_solution_data_array is not None
                current_flux_data_array, _ = decipher_flux_title(
                    modified_flux_name, flux_name_index_dict, replace_flux_dict,
                    current_solution_data_array, reverse_order)
                absolute_distance = normalized_difference_to_array(
                    current_flux_data_array, simulated_flux_value, max_flux_diff, reduced_method)
                if len(np.shape(absolute_distance)) == 0:
                    absolute_distance = np.reshape(absolute_distance, [-1])
                final_flux_absolute_distance_dict[flux_title][selected_min_loss_size][analyzed_set_size].extend(
                    absolute_distance)
                relative_distance = normalized_difference_to_array(
                    current_flux_data_array, simulated_flux_value, None, reduced_method)
                if len(np.shape(relative_distance)) == 0:
                    relative_distance = np.reshape(relative_distance, [-1])
                final_flux_relative_distance_dict[flux_title][selected_min_loss_size][analyzed_set_size].extend(
                    relative_distance)
                if flux_title not in maximal_absolute_distance_dict:
                    maximal_absolute_distance_dict[flux_title] = np.max(np.abs(absolute_distance))
                    maximal_relative_distance_dict[flux_title] = np.max(np.abs(relative_distance))
                else:
                    maximal_absolute_distance_dict[flux_title] = np.maximum(
                        maximal_absolute_distance_dict[flux_title], np.max(np.abs(absolute_distance)))
                    maximal_relative_distance_dict[flux_title] = np.maximum(
                        maximal_relative_distance_dict[flux_title], np.max(np.abs(relative_distance)))

    print(f'Analyzing total_size={analyzed_set_size} and select_size={selected_min_loss_size}...')
    if selected_min_loss_size > analyzed_set_size:
        if final_raw_mean_euclidian_distance_dict is not None:
            add_empty_obj(
                final_raw_mean_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
        if final_net_mean_euclidian_distance_dict is not None:
            add_empty_obj(
                final_net_mean_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
        calculate_flux_each_cycle(analyzed_set_size, selected_min_loss_size, empty=True)
    else:
        if select_mode:
            assert sorted_index_array is not None
            total_required_num = repeat_time_each_analyzed_set * analyzed_set_size
            if total_required_num > total_data_size:
                replace = True
            else:
                replace = False
            all_repeat_analyzed_index_set_array = random_seed.choice(
                total_data_size, total_required_num, replace=replace)
            ordered_selected_index_array_list = []
            ordered_selected_solution_data_array_list = []
            for repeat_time_index in range(repeat_time_each_analyzed_set):
                (
                    ordered_selected_index_array, ordered_selected_solution_data_array
                ) = calculate_ordered_selected_index_solution_each_cycle(
                    analyzed_set_size, selected_min_loss_size, repeat_time_index)
                ordered_selected_index_array_list.append(ordered_selected_index_array)
                ordered_selected_solution_data_array_list.append(ordered_selected_solution_data_array)
        else:
            add_empty_obj(
                raw_selected_flux_value_dict, list, analyzed_set_size, selected_min_loss_size).append(
                solution_data_array)
            ordered_selected_index_array_list = [None]
            ordered_selected_solution_data_array_list = [solution_data_array]
        for ordered_selected_index_array, ordered_selected_solution_data_array in zip(
                ordered_selected_index_array_list, ordered_selected_solution_data_array_list):
            max_loss_value = calculate_loss_and_mid_each_cycle(
                analyzed_set_size, selected_min_loss_size,
                ordered_selected_index_array, ordered_selected_solution_data_array)
            max_raw_euclidian_distance, max_net_euclidian_distance = calculate_distance_each_cycle(
                ordered_selected_solution_data_array)
            calculate_flux_each_cycle(
                analyzed_set_size, selected_min_loss_size,
                current_solution_data_array=ordered_selected_solution_data_array, reduced=select_mode)
    return max_raw_euclidian_distance, max_net_euclidian_distance, max_loss_value


def generate_y_lim_dict(maximal_distance_dict):
    y_lim_dict = {}
    for flux_title, maximal_absolute_distance in maximal_distance_dict.items():
        if maximal_absolute_distance < 0.1:
            distance_factor = 100.0
        else:
            distance_factor = 10.0
        y_lim_dict[flux_title] = np.ceil(maximal_absolute_distance * distance_factor) / distance_factor
    return y_lim_dict


def construct_output_dict(
        result_label, analyzed_set_size, selected_min_loss_size,
        current_raw_loss_array_list, current_raw_solution_array_list, current_raw_predicted_data_dict,
        target_experimental_mid_data_dict, flux_name_index_dict, raw_information_dict,
        index_column_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
        final_target_experimental_mid_data_dict, final_flux_name_index_dict, final_information_dict,
        solution_state, single_item=False
):
    current_repeat_index_list = []
    current_each_repeat_index_list = []
    for repeat_index, raw_loss_array in enumerate(current_raw_loss_array_list):
        if single_item:
            current_size = 1
        else:
            current_size = len(raw_loss_array)
        current_repeat_index_list.extend([repeat_index + 1] * current_size)
        current_each_repeat_index_list.extend(range(1, current_size + 1))
    index_column_dict[result_label] = {
        'repeat_index': current_repeat_index_list,
        'index_in_each_repeat': current_each_repeat_index_list,
    }
    final_solution_data_dict[result_label] = np.vstack(current_raw_solution_array_list)
    final_loss_data_dict[result_label] = np.hstack(current_raw_loss_array_list)
    final_predicted_data_dict[result_label] = current_raw_predicted_data_dict
    final_target_experimental_mid_data_dict[result_label] = target_experimental_mid_data_dict
    final_flux_name_index_dict[result_label] = flux_name_index_dict
    final_information_dict[result_label] = {
        **raw_information_dict,
        'total_analyzed_set_size': analyzed_set_size,
        'num_of_min_loss_be_selected': selected_min_loss_size,
        'solution_type': solution_state,
    }


def output_analyzed_raw_flux_and_predicted_mid_data(
        analyzed_set_size_list, selected_min_loss_size_list,
        raw_selected_flux_value_dict, selected_averaged_flux_value_dict,
        raw_selected_loss_value_dict, selected_averaged_loss_dict,
        raw_selected_predicted_data_dict, selected_averaged_predicted_data_dict,
        target_experimental_mid_data_dict, flux_name_index_dict,
        raw_information_dict, flux_result_output_xlsx_path, mid_prediction_result_output_xlsx_path):
    final_loss_data_dict = {}
    final_solution_data_dict = {}
    final_flux_name_index_dict = {}
    final_information_dict = {}
    index_column_dict = {}
    final_predicted_data_dict = {}
    final_target_experimental_mid_data_dict = {}
    # common_information_dict = raw_information_dict.values().__iter__().__next__()
    for analyzed_set_size in analyzed_set_size_list:
        for selected_min_loss_size in selected_min_loss_size_list:
            result_label = f'{analyzed_set_size}_{selected_min_loss_size}'
            try:
                current_raw_solution_array_list = raw_selected_flux_value_dict[
                    analyzed_set_size][selected_min_loss_size]
                current_raw_loss_array_list = raw_selected_loss_value_dict[selected_min_loss_size][analyzed_set_size]
                current_raw_predicted_data_dict = raw_selected_predicted_data_dict[
                    selected_min_loss_size][analyzed_set_size]
            except KeyError:
                continue
            else:
                if analyzed_set_size == traditional_method_optimize_size and selected_min_loss_size == 1:
                    selected_state = Keywords.traditional_method_solutions
                    current_result_label = f'{result_label}_traditional'
                else:
                    selected_state = Keywords.selected_solutions
                    current_result_label = result_label
                averaged_result_label = f'{result_label}_averaged'
                construct_output_dict(
                    current_result_label, analyzed_set_size, selected_min_loss_size,
                    current_raw_loss_array_list, current_raw_solution_array_list, current_raw_predicted_data_dict,
                    target_experimental_mid_data_dict, flux_name_index_dict, raw_information_dict,
                    index_column_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
                    final_target_experimental_mid_data_dict, final_flux_name_index_dict, final_information_dict,
                    selected_state, single_item=False,
                )
                if selected_min_loss_size != 1:
                    current_selected_averaged_solution_array_list = selected_averaged_flux_value_dict[
                        analyzed_set_size][selected_min_loss_size]
                    current_selected_averaged_loss_array_list = selected_averaged_loss_dict[
                        selected_min_loss_size][analyzed_set_size]
                    current_selected_averaged_predicted_data_dict = selected_averaged_predicted_data_dict[
                        selected_min_loss_size][analyzed_set_size]
                    construct_output_dict(
                        averaged_result_label, analyzed_set_size, selected_min_loss_size,
                        current_selected_averaged_loss_array_list, current_selected_averaged_solution_array_list,
                        current_selected_averaged_predicted_data_dict,
                        target_experimental_mid_data_dict, flux_name_index_dict, raw_information_dict,
                        index_column_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_data_dict,
                        final_target_experimental_mid_data_dict, final_flux_name_index_dict, final_information_dict,
                        Keywords.averaged_solutions, single_item=True,
                    )
    output_raw_flux_data(
        flux_result_output_xlsx_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
        final_information_dict, subset_index_dict=None, other_label_column_dict=index_column_dict)
    output_predicted_mid_data(
        mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
        final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=None,
        other_label_row_dict=index_column_dict)


def raw_model_result_processing_func(
        result_name, solver_obj, loss_data_array, solution_data_array, flux_name_index_dict, raw_information_dict,
        predicted_data_dict, processed_mid_name_dict, target_experimental_mid_data_dict, simulated_flux_value_dict,
        important_flux_list, replace_flux_dict, analyzed_set_size_list,
        selected_min_loss_size_list, repeat_time_each_analyzed_set,
        flux_range, this_result_output_direct, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path, net_flux_list, test_mode=False):

    def scatter_plotting(final_flux_distance_dict, y_lim_dict, distance_output_direct):
        for flux_title, each_flux_data_dict in final_flux_distance_dict.items():
            y_lim = y_lim_dict[flux_title]
            multi_row_col_scatter_plot_for_result_selection(
                each_flux_data_dict, x_label_index_dict, y_label_index_dict, flux_title,
                output_direct=distance_output_direct, cutoff_value=0, figsize=None, ylim=(-y_lim, y_lim))

    def heatmap_and_box3d_plotting(
            data_dict, distribution_output_direct, figure_title, percentage=False):
        mean_matrix, std_matrix, mean_lim_pair, mean_value_text_format = heatmap_and_box3d_parameter_preparation(
            data_dict, percentage)
        heat_map_plotting(
            mean_matrix, analyzed_set_size_list, selected_min_loss_size_list, f'{figure_title}_mean',
            distribution_output_direct, *mean_lim_pair, figsize=None, value_number_format=mean_value_text_format)
        heat_map_plotting(
            std_matrix, analyzed_set_size_list, selected_min_loss_size_list, f'{figure_title}_std',
            distribution_output_direct, 0, None, figsize=None,
            value_number_format=HeatmapValueFormat.scientific_format)
        # lb_matrix = mean_matrix - std_matrix
        # ub_matrix = mean_matrix + std_matrix
        # box_plot_3d(
        #     mean_matrix, lb_matrix, ub_matrix, analyzed_set_size_list, selected_min_loss_size_list, figure_title,
        #     distribution_output_direct, z_lim=y_lim_tuple, cutoff=0, figsize=None)

    def heatmap_and_box3d_plotting_by_fluxes(
            final_flux_distance_dict, y_lim_dict, distribution_output_direct, percentage=False):
        for flux_title, each_flux_data_dict in final_flux_distance_dict.items():
            y_lim = y_lim_dict[flux_title]
            heatmap_and_box3d_plotting(
                each_flux_data_dict, distribution_output_direct, flux_title, percentage)

    def heatmap_and_box3d_plotting_euclidean(euclidean_distance_dict, distribution_output_direct):
        heatmap_and_box3d_plotting(
            euclidean_distance_dict, distribution_output_direct, 'net_euclidian_distance')

    print(f'Start result analysis for {result_name}...')
    min_value, max_value = flux_range
    # reduced_metric = Keywords.median
    # reduced_metric = Keywords.mean
    sorted_index_array = np.argsort(loss_data_array)
    total_data_size = len(loss_data_array)
    final_flux_absolute_distance_dict = {}
    final_flux_relative_distance_dict = {}
    final_raw_mean_euclidian_distance_dict = {}
    final_net_mean_euclidian_distance_dict = {}
    final_raw_all_select_euclidian_distance_dict = {}
    final_net_all_select_euclidian_distance_dict = {}
    maximal_absolute_distance_dict = {}
    maximal_relative_distance_dict = {}
    max_raw_euclidian_distance = 0
    max_net_euclidian_distance = 0
    raw_selected_flux_value_dict = {}
    selected_averaged_flux_value_dict = {}
    raw_selected_diff_vector_dict = {}
    selected_averaged_diff_vector_dict = {}
    net_all_selected_relative_error_dict = {}
    net_selected_averaged_relative_error_dict = {}
    raw_selected_loss_value_dict = {}
    loss_of_mean_solution_dict = {}
    raw_selected_predicted_data_dict = {}
    selected_averaged_predicted_data_dict = {}
    max_loss_value = 0

    (
        common_flux_name_simulated_value_dict, simulated_flux_vector, simulated_net_flux_vector,
        common_flux_name_list, net_flux_matrix, normal_core_flux_index_array) = analyze_simulated_flux_value_dict(
        simulated_flux_value_dict, net_flux_list, flux_name_index_dict)

    for analyzed_set_size in analyzed_set_size_list:
        for selected_min_loss_size in selected_min_loss_size_list:
            max_raw_euclidian_distance, max_net_euclidian_distance, max_loss_value = each_cycle_analyzer(
                analyzed_set_size, selected_min_loss_size,
                solution_data_array, loss_data_array, predicted_data_dict, solver_obj, flux_name_index_dict,
                common_flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector,
                simulated_net_flux_vector, normal_core_flux_index_array, total_data_size, replace_flux_dict,
                max_value - min_value,

                final_flux_absolute_distance_dict,
                final_flux_relative_distance_dict,
                final_raw_mean_euclidian_distance_dict,
                final_net_mean_euclidian_distance_dict,
                final_raw_all_select_euclidian_distance_dict,
                final_net_all_select_euclidian_distance_dict,
                maximal_absolute_distance_dict,
                maximal_relative_distance_dict,
                max_raw_euclidian_distance,
                max_net_euclidian_distance,
                raw_selected_flux_value_dict,
                selected_averaged_flux_value_dict,
                raw_selected_diff_vector_dict,
                selected_averaged_diff_vector_dict,
                net_all_selected_relative_error_dict,
                net_selected_averaged_relative_error_dict,
                raw_selected_loss_value_dict,
                loss_of_mean_solution_dict,
                processed_mid_name_dict,
                raw_selected_predicted_data_dict,
                selected_averaged_predicted_data_dict,
                max_loss_value,
                select_mode=True,
                sorted_index_array=sorted_index_array,
                repeat_time_each_analyzed_set=repeat_time_each_analyzed_set,
            )

    absolute_y_lim_dict = generate_y_lim_dict(maximal_absolute_distance_dict)
    relative_y_lim_dict = generate_y_lim_dict(maximal_relative_distance_dict)
    x_label_index_dict = {
        analyzed_set_size: index for index, analyzed_set_size in enumerate(analyzed_set_size_list)}
    y_label_index_dict = {
        selected_min_loss_size: index for index, selected_min_loss_size in enumerate(selected_min_loss_size_list)}

    # print('Finish analysis. Printing result figures...')
    # current_result_output_direct = '{}/{}'.format(
    #     this_result_output_direct, config.Direct.raw_model_approximation_percentile)
    # current_metric_output_direct = '{}/{}'.format(current_result_output_direct, reduced_metric)
    # absolute_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.absolute_distance)
    # check_and_mkdir_of_direct(absolute_distance_output_direct)
    # relative_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.relative_distance)
    # check_and_mkdir_of_direct(relative_distance_output_direct)
    # scatter_plotting(final_flux_absolute_distance_dict, absolute_y_lim_dict, absolute_distance_output_direct)
    # scatter_plotting(final_flux_relative_distance_dict, relative_y_lim_dict, relative_distance_output_direct)
    # heatmap_and_box3d_plotting_by_fluxes(
    #     final_flux_absolute_distance_dict, absolute_y_lim_dict, absolute_distance_output_direct)
    # heatmap_and_box3d_plotting_by_fluxes(
    #     final_flux_relative_distance_dict, relative_y_lim_dict, relative_distance_output_direct, percentage=True)
    # if reduced_metric == Keywords.mean:
    #     euclidean_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.euclidean_distance)
    #     check_and_mkdir_of_direct(euclidean_distance_output_direct)
    #     multi_row_col_scatter_plot_for_result_selection(
    #         final_raw_mean_euclidian_distance_dict, x_label_index_dict, y_label_index_dict, 'raw_euclidian_distance',
    #         output_direct=euclidean_distance_output_direct, cutoff_value=0, figsize=None,
    #         ylim=(0, max_raw_euclidian_distance * 1.1))
    #     multi_row_col_scatter_plot_for_result_selection(
    #         final_net_mean_euclidian_distance_dict, x_label_index_dict, y_label_index_dict, 'net_euclidian_distance',
    #         output_direct=euclidean_distance_output_direct, cutoff_value=0, figsize=None,
    #         ylim=(0, max_net_euclidian_distance * 1.1))
    #     # heatmap_and_box3d_plotting(
    #     #     final_net_mean_euclidian_distance_dict, None, current_metric_output_direct, 'net_euclidian_distance')
    #     heatmap_and_box3d_plotting_euclidean(final_net_mean_euclidian_distance_dict, euclidean_distance_output_direct)

    print('Saving result files...')
    if not test_mode:
        output_analyzed_raw_flux_and_predicted_mid_data(
            analyzed_set_size_list, selected_min_loss_size_list,
            raw_selected_flux_value_dict, selected_averaged_flux_value_dict,
            raw_selected_loss_value_dict, loss_of_mean_solution_dict,
            raw_selected_predicted_data_dict, selected_averaged_predicted_data_dict,
            target_experimental_mid_data_dict, flux_name_index_dict,
            raw_information_dict, flux_result_output_xlsx_path, mid_prediction_result_output_xlsx_path)
    figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
    figure_raw_data.save_data(
        raw_selected_flux_value_dict=raw_selected_flux_value_dict,
        selected_averaged_flux_value_dict=selected_averaged_flux_value_dict,
        raw_selected_diff_vector_dict=raw_selected_diff_vector_dict,
        selected_averaged_diff_vector_dict=selected_averaged_diff_vector_dict,
        common_flux_name_list=common_flux_name_list,
        final_flux_absolute_distance_dict=final_flux_absolute_distance_dict,
        final_flux_relative_distance_dict=final_flux_relative_distance_dict,
        absolute_y_lim_dict=absolute_y_lim_dict,
        relative_y_lim_dict=relative_y_lim_dict,
        final_raw_euclidian_distance_dict=final_raw_mean_euclidian_distance_dict,
        final_net_euclidian_distance_dict=final_net_mean_euclidian_distance_dict,
        final_raw_all_select_euclidian_distance_dict=final_raw_all_select_euclidian_distance_dict,
        final_net_all_select_euclidian_distance_dict=final_net_all_select_euclidian_distance_dict,
        maximal_raw_euclidian_distance=max_raw_euclidian_distance,
        maximal_net_euclidian_distance=max_net_euclidian_distance,
        net_all_selected_relative_error_dict=net_all_selected_relative_error_dict,
        net_selected_averaged_relative_error_dict=net_selected_averaged_relative_error_dict,
        raw_loss_value_dict=raw_selected_loss_value_dict,
        loss_of_mean_solution_dict=loss_of_mean_solution_dict,
        max_loss_value=max_loss_value,
        x_label_index_dict=x_label_index_dict, y_label_index_dict=y_label_index_dict,
        analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
        raw_selected_predicted_data_dict=raw_selected_predicted_data_dict,
        selected_averaged_predicted_data_dict=selected_averaged_predicted_data_dict,
        target_experimental_mid_data_dict=target_experimental_mid_data_dict,
    )


def flatten_2d_data_dict(data_dict):
    for index1, content_dict in data_dict.items():
        for index2, target_item in content_dict.items():
            if isinstance(target_item, list):
                if len(np.shape(target_item)) == 1:
                    target_array = np.array(target_item)
                else:
                    target_array = np.concatenate(target_item)
                data_dict[index1][index2] = target_array


def optimization_from_averaged_solution_result_processing_func(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, common_flux_name_index_dict, simulated_flux_value_dict,
        net_flux_list, replace_flux_dict, analyzed_set_size_list, selected_min_loss_size_list, flux_range
):
    def distance_between_average_and_reoptimized_solution(
            initial_averaged_diff_vector_dict, raw_selected_diff_vector_dict):
        for analyzed_size in analyzed_set_size_list:
            for selected_size in selected_min_loss_size_list:
                try:
                    averaged_data_vector_list = initial_averaged_diff_vector_dict[selected_size][analyzed_size]
                    reoptimized_data_vector_list = raw_selected_diff_vector_dict[selected_size][analyzed_size]
                except KeyError:
                    net_diff_vector_between_averaged_and_reoptimized_list = None
                    net_distance_between_averaged_and_reoptimized_list = None
                else:
                    net_diff_vector_between_averaged_and_reoptimized_list = [
                        reoptimized_data_vector - averaged_data_vector
                        for reoptimized_data_vector, averaged_data_vector
                        in zip(reoptimized_data_vector_list, averaged_data_vector_list)]
                    net_distance_between_averaged_and_reoptimized_list = [
                        np.sqrt(np.sum(net_diff_vector_between_averaged_and_reoptimized ** 2))
                        for net_diff_vector_between_averaged_and_reoptimized in
                        net_diff_vector_between_averaged_and_reoptimized_list
                    ]
                add_empty_obj(diff_vector_between_averaged_and_reoptimized_dict, list, selected_size, analyzed_size)
                add_empty_obj(net_distance_between_averaged_and_reoptimized_dict, list, selected_size, analyzed_size)
                diff_vector_between_averaged_and_reoptimized_dict[selected_size][analyzed_size] = (
                    net_diff_vector_between_averaged_and_reoptimized_list)
                net_distance_between_averaged_and_reoptimized_dict[selected_size][analyzed_size] = (
                    net_distance_between_averaged_and_reoptimized_list)

    print(f'Start result analysis for {result_name}...')
    final_flux_absolute_distance_dict = {}
    final_flux_relative_distance_dict = {}
    final_raw_mean_euclidian_distance_dict = None
    final_net_mean_euclidian_distance_dict = None
    final_raw_all_select_euclidian_distance_dict = {}
    final_net_all_select_euclidian_distance_dict = {}
    maximal_absolute_distance_dict = {}
    maximal_relative_distance_dict = {}
    max_raw_euclidian_distance = 0
    max_net_euclidian_distance = 0
    raw_selected_flux_value_dict = {}
    selected_averaged_flux_value_dict = None
    raw_selected_diff_vector_dict = {}
    selected_averaged_diff_vector_dict = None
    net_all_selected_relative_error_dict = {}
    net_selected_averaged_relative_error_dict = None
    raw_selected_loss_value_dict = {}
    loss_of_mean_solution_dict = None
    raw_selected_predicted_data_dict = {}
    selected_averaged_predicted_data_dict = {}
    diff_vector_between_averaged_and_reoptimized_dict = {}
    net_distance_between_averaged_and_reoptimized_dict = {}
    max_loss_value = 0
    min_value, max_value = flux_range

    # target_analyzed_set_size_list = [1000, 2000, 5000, 10000, 20000, 50000]
    # analyzed_set_size_list = target_analyzed_set_size_list
    # target_selected_min_loss_size_list = [10, 20, 50, 100, 200, 500]
    # selected_min_loss_size_list = target_selected_min_loss_size_list

    (
        common_flux_name_simulated_value_dict, simulated_flux_vector, simulated_net_flux_vector,
        common_flux_name_list, net_flux_matrix, normal_core_flux_index_array) = analyze_simulated_flux_value_dict(
        simulated_flux_value_dict, net_flux_list, common_flux_name_index_dict)
    analyzed_selected_result_label_dict = {}
    for result_label, result_information_dict in final_information_dict.items():
        analyzed_set_size = result_information_dict[Keywords.config][Keywords.optimized_size]
        selected_min_loss_size = result_information_dict[Keywords.config][Keywords.selection_size]
        if analyzed_set_size not in analyzed_selected_result_label_dict:
            analyzed_selected_result_label_dict[analyzed_set_size] = {}
        analyzed_selected_result_label_dict[analyzed_set_size][selected_min_loss_size] = result_label

    # analyzed_set_size_set = set(target_analyzed_set_size_list)
    # selected_min_loss_size_set = set(target_selected_min_loss_size_list)
    for analyzed_set_size in analyzed_set_size_list:
        for selected_min_loss_size in selected_min_loss_size_list:
            try:
                result_label = analyzed_selected_result_label_dict[analyzed_set_size][selected_min_loss_size]
                solution_data_array = final_solution_data_dict[result_label]
                loss_data_array = final_loss_data_dict[result_label]
                total_data_size = len(loss_data_array)
                predicted_data_dict = final_predicted_data_dict[result_label]
                solver_obj = solver_dict[result_label]
            except KeyError:
                solution_data_array = None
                loss_data_array = None
                total_data_size = 0
                predicted_data_dict = None
                solver_obj = None

            max_raw_euclidian_distance, max_net_euclidian_distance, max_loss_value = each_cycle_analyzer(
                analyzed_set_size, selected_min_loss_size,
                solution_data_array, loss_data_array, predicted_data_dict, solver_obj, common_flux_name_index_dict,
                common_flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
                normal_core_flux_index_array, total_data_size, replace_flux_dict, max_value - min_value,

                final_flux_absolute_distance_dict,
                final_flux_relative_distance_dict,
                final_raw_mean_euclidian_distance_dict,
                final_net_mean_euclidian_distance_dict,
                final_raw_all_select_euclidian_distance_dict,
                final_net_all_select_euclidian_distance_dict,
                maximal_absolute_distance_dict,
                maximal_relative_distance_dict,
                max_raw_euclidian_distance,
                max_net_euclidian_distance,
                raw_selected_flux_value_dict,
                selected_averaged_flux_value_dict,
                raw_selected_diff_vector_dict,
                selected_averaged_diff_vector_dict,
                net_all_selected_relative_error_dict,
                net_selected_averaged_relative_error_dict,
                raw_selected_loss_value_dict,
                loss_of_mean_solution_dict,
                processed_mid_name_dict,
                raw_selected_predicted_data_dict,
                selected_averaged_predicted_data_dict,
                max_loss_value,
                select_mode=False,
            )

    flatten_2d_data_dict(raw_selected_flux_value_dict)
    flatten_2d_data_dict(raw_selected_diff_vector_dict)
    flatten_2d_data_dict(raw_selected_loss_value_dict)
    flatten_2d_data_dict(final_raw_all_select_euclidian_distance_dict)
    flatten_2d_data_dict(final_net_all_select_euclidian_distance_dict)
    flatten_2d_data_dict(net_all_selected_relative_error_dict)
    relative_y_lim_dict = generate_y_lim_dict(maximal_relative_distance_dict)
    x_label_index_dict = {
        analyzed_set_size: index for index, analyzed_set_size in enumerate(analyzed_set_size_list)}
    y_label_index_dict = {
        selected_min_loss_size: index for index, selected_min_loss_size in enumerate(selected_min_loss_size_list)}

    data_label = final_information_dict.values().__iter__().__next__()[Keywords.data][Keywords.label]
    (
        initial_raw_selected_flux_value_dict, initial_averaged_flux_value_dict,
        initial_raw_selected_diff_vector_dict, initial_averaged_diff_vector_dict,
        loss_of_initial_raw_selected_solutions_dict, loss_of_initial_averaged_solutions_dict,
        raw_euclidian_distance_of_initial_raw_selected_dict,
        net_euclidian_distance_of_initial_raw_selected_dict,
        raw_euclidian_distance_of_initial_averaged_solutions_dict,
        net_euclidian_distance_of_initial_averaged_solutions_dict,
        net_relative_error_of_initial_raw_selected_dict,
        net_relative_error_of_initial_averaged_solutions_dict,
        flux_relative_distance_of_initial_averaged_solutions_dict,
        _
    ) = averaged_solution_data_obj.return_averaged_data(data_label)
    distance_between_average_and_reoptimized_solution(
        initial_averaged_diff_vector_dict, raw_selected_diff_vector_dict)

    flatten_2d_data_dict(initial_raw_selected_flux_value_dict)
    flatten_2d_data_dict(initial_raw_selected_diff_vector_dict)
    flatten_2d_data_dict(initial_averaged_diff_vector_dict)
    flatten_2d_data_dict(loss_of_initial_raw_selected_solutions_dict)
    flatten_2d_data_dict(net_euclidian_distance_of_initial_raw_selected_dict)
    flatten_2d_data_dict(net_relative_error_of_initial_raw_selected_dict)
    flatten_2d_data_dict(net_relative_error_of_initial_averaged_solutions_dict)
    flatten_2d_data_dict(diff_vector_between_averaged_and_reoptimized_dict)
    figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
    figure_raw_data.save_data(
        initial_raw_selected_flux_value_dict=initial_raw_selected_flux_value_dict,
        initial_averaged_flux_value_dict=initial_averaged_flux_value_dict,
        raw_selected_flux_value_dict=raw_selected_flux_value_dict,
        initial_raw_selected_diff_vector_dict=initial_raw_selected_diff_vector_dict,
        initial_averaged_diff_vector_dict=initial_averaged_diff_vector_dict,
        raw_selected_diff_vector_dict=raw_selected_diff_vector_dict,
        common_flux_name_list=common_flux_name_list,
        flux_relative_distance_of_initial_averaged_solutions_dict=flux_relative_distance_of_initial_averaged_solutions_dict,
        final_flux_relative_distance_dict=final_flux_relative_distance_dict,
        relative_y_lim_dict=relative_y_lim_dict,
        raw_euclidian_distance_of_initial_raw_selected_dict=raw_euclidian_distance_of_initial_raw_selected_dict,
        net_euclidian_distance_of_initial_raw_selected_dict=net_euclidian_distance_of_initial_raw_selected_dict,
        raw_euclidian_distance_of_initial_averaged_solutions_dict=raw_euclidian_distance_of_initial_averaged_solutions_dict,
        net_euclidian_distance_of_initial_averaged_solutions_dict=net_euclidian_distance_of_initial_averaged_solutions_dict,
        final_raw_all_select_euclidian_distance_dict=final_raw_all_select_euclidian_distance_dict,
        final_net_all_select_euclidian_distance_dict=final_net_all_select_euclidian_distance_dict,
        maximal_raw_euclidian_distance=max_raw_euclidian_distance,
        maximal_net_euclidian_distance=max_net_euclidian_distance,
        net_relative_error_of_initial_raw_selected_dict=net_relative_error_of_initial_raw_selected_dict,
        net_relative_error_of_initial_averaged_solutions_dict=net_relative_error_of_initial_averaged_solutions_dict,
        net_all_selected_relative_error_dict=net_all_selected_relative_error_dict,
        loss_of_initial_raw_selected_solutions_dict=loss_of_initial_raw_selected_solutions_dict,
        loss_of_initial_averaged_solutions_dict=loss_of_initial_averaged_solutions_dict,
        raw_loss_value_dict=raw_selected_loss_value_dict,
        max_loss_value=max_loss_value,
        x_label_index_dict=x_label_index_dict, y_label_index_dict=y_label_index_dict,
        analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
        raw_selected_predicted_data_dict=raw_selected_predicted_data_dict,
        diff_vector_between_averaged_and_reoptimized_dict=diff_vector_between_averaged_and_reoptimized_dict,
        net_distance_between_averaged_and_reoptimized_dict=net_distance_between_averaged_and_reoptimized_dict,
    )


def multiple_simulated_data_result_processing_func(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, common_flux_name_index_dict,
        nested_simulated_flux_value_dict_dict, analyzed_set_size_list, selected_min_loss_size_list,
        repeat_time_each_analyzed_set, net_flux_list, replace_flux_dict, flux_range, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path, optimization_from_averaged_solutions=False,
):
    print(f'Start result analysis for {result_name}...')
    min_value, max_value = flux_range
    final_flux_absolute_distance_dict = {}
    final_flux_relative_distance_dict = {}
    final_raw_mean_euclidian_distance_dict = None
    final_net_mean_euclidian_distance_dict = {}
    final_raw_all_select_euclidian_distance_dict = {}
    final_net_all_select_euclidian_distance_dict = {}
    maximal_absolute_distance_dict = {}
    maximal_relative_distance_dict = {}
    max_raw_euclidian_distance = 0
    max_net_euclidian_distance = 0
    raw_selected_flux_value_dict = {}
    selected_averaged_flux_value_dict = {}
    separate_selected_averaged_flux_value_dict = {}
    raw_selected_diff_vector_dict = {}
    selected_averaged_diff_vector_dict = {}
    net_all_selected_relative_error_dict = {}
    net_selected_averaged_relative_error_dict = {}
    raw_selected_loss_value_dict = {}
    loss_of_mean_solution_dict = {}
    raw_selected_predicted_data_dict = {}
    selected_averaged_predicted_data_dict = {}
    each_simulated_absolute_y_lim_dict = {}
    each_simulated_relative_y_lim_dict = {}
    max_loss_value = 0

    common_flux_name_list = None

    net_distance_between_different_simulated_flux_dict = {}
    net_distance_between_different_simulated_flux_list = []
    previous_simulated_net_flux_vector_list = []
    standard_simulated_flux_value_dict = None

    for result_label, simulated_flux_value_dict in nested_simulated_flux_value_dict_dict.items():
        loss_data_array = final_loss_data_dict[result_label]
        solution_data_array = final_solution_data_dict[result_label]
        predicted_data_dict = final_predicted_data_dict[result_label]
        solver_obj = solver_dict[result_label]

        sorted_index_array = np.argsort(loss_data_array)
        total_data_size = len(loss_data_array)
        print(f'{total_data_size} results loaded in {result_label}')

        (
            flux_name_simulated_value_dict, simulated_flux_vector, simulated_net_flux_vector,
            this_common_flux_name_list, net_flux_matrix, normal_core_flux_index_array
        ) = analyze_simulated_flux_value_dict(
            simulated_flux_value_dict, net_flux_list, common_flux_name_index_dict,
            standard_simulated_flux_value_dict=standard_simulated_flux_value_dict)
        # (
        #     flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, formal_flux_name_list
        # ) = analyze_simulated_flux_value_dict(
        #     simulated_flux_value_dict, net_flux_list, common_flux_name_index_dict,
        #     standard_simulated_flux_value_dict=standard_simulated_flux_value_dict)
        if not optimization_from_averaged_solutions:
            if standard_simulated_flux_value_dict is None:
                standard_simulated_flux_value_dict = simulated_flux_value_dict
            if len(previous_simulated_net_flux_vector_list) > 0:
                net_euclidean_distance = calculate_raw_and_net_distance(
                    previous_simulated_net_flux_vector_list, None, simulated_net_flux_vector)
                try:
                    net_distance_between_different_simulated_flux_list.extend(net_euclidean_distance)
                except TypeError:
                    net_distance_between_different_simulated_flux_list.append(net_euclidean_distance)
            previous_simulated_net_flux_vector_list.append(simulated_net_flux_vector)

        if common_flux_name_list is None:
            common_flux_name_list = this_common_flux_name_list

        for analyzed_set_size in analyzed_set_size_list:
            for selected_min_loss_size in selected_min_loss_size_list:
                max_raw_euclidian_distance, max_net_euclidian_distance, max_loss_value = each_cycle_analyzer(
                    analyzed_set_size, selected_min_loss_size,
                    solution_data_array, loss_data_array, predicted_data_dict, solver_obj, common_flux_name_index_dict,
                    flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
                    normal_core_flux_index_array, total_data_size, replace_flux_dict, max_value - min_value,

                    final_flux_absolute_distance_dict,
                    final_flux_relative_distance_dict,
                    final_raw_mean_euclidian_distance_dict,
                    final_net_mean_euclidian_distance_dict,
                    final_raw_all_select_euclidian_distance_dict,
                    final_net_all_select_euclidian_distance_dict,
                    maximal_absolute_distance_dict,
                    maximal_relative_distance_dict,
                    max_raw_euclidian_distance,
                    max_net_euclidian_distance,
                    raw_selected_flux_value_dict,
                    selected_averaged_flux_value_dict,
                    raw_selected_diff_vector_dict,
                    selected_averaged_diff_vector_dict,
                    net_all_selected_relative_error_dict,
                    net_selected_averaged_relative_error_dict,
                    raw_selected_loss_value_dict,
                    loss_of_mean_solution_dict,
                    processed_mid_name_dict,
                    raw_selected_predicted_data_dict,
                    selected_averaged_predicted_data_dict,
                    max_loss_value,
                    select_mode=True,
                    sorted_index_array=sorted_index_array,
                    repeat_time_each_analyzed_set=repeat_time_each_analyzed_set,
                )
                if not optimization_from_averaged_solutions:
                    if selected_min_loss_size not in net_distance_between_different_simulated_flux_dict:
                        net_distance_between_different_simulated_flux_dict[selected_min_loss_size] = {}
                    if analyzed_set_size not in net_distance_between_different_simulated_flux_dict[selected_min_loss_size]:
                        net_distance_between_different_simulated_flux_dict[selected_min_loss_size][analyzed_set_size] = (
                            net_distance_between_different_simulated_flux_list)

        each_simulated_absolute_y_lim_dict = generate_y_lim_dict(
            maximal_absolute_distance_dict)
        each_simulated_relative_y_lim_dict = generate_y_lim_dict(
            maximal_relative_distance_dict)
    x_label_index_dict = {
        analyzed_set_size: index for index, analyzed_set_size in enumerate(analyzed_set_size_list)}
    y_label_index_dict = {
        selected_min_loss_size: index for index, selected_min_loss_size in enumerate(selected_min_loss_size_list)}

    if not optimization_from_averaged_solutions:
        for analyzed_set_size in analyzed_set_size_list:
            for selected_min_loss_size in selected_min_loss_size_list:
                for result_index, result_label in enumerate(nested_simulated_flux_value_dict_dict.keys()):
                    data_label = final_information_dict[result_label][Keywords.data][Keywords.index_label]
                    start_result_index = result_index * repeat_time_each_analyzed_set
                    end_result_index = start_result_index + repeat_time_each_analyzed_set
                    add_empty_obj(
                        separate_selected_averaged_flux_value_dict, dict, analyzed_set_size, selected_min_loss_size
                    )[data_label] = selected_averaged_flux_value_dict[
                        analyzed_set_size][selected_min_loss_size][start_result_index:end_result_index]

        print('Saving result files...')
        # output_analyzed_raw_flux_and_predicted_mid_data(
        #     analyzed_set_size_list, selected_min_loss_size_list,
        #     raw_selected_flux_value_dict, raw_selected_loss_value_dict, raw_selected_predicted_data_dict,
        #     target_experimental_mid_data_dict, common_flux_name_index_dict, raw_information_dict,
        #     flux_result_output_xlsx_path, mid_prediction_result_output_xlsx_path)
        figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
        figure_raw_data.save_data(
            raw_selected_flux_value_dict=raw_selected_flux_value_dict,
            selected_averaged_flux_value_dict=selected_averaged_flux_value_dict,
            separate_selected_averaged_flux_value_dict=separate_selected_averaged_flux_value_dict,
            raw_selected_diff_vector_dict=raw_selected_diff_vector_dict,
            selected_averaged_diff_vector_dict=selected_averaged_diff_vector_dict,
            common_flux_name_list=common_flux_name_list,
            final_flux_absolute_distance_dict=final_flux_absolute_distance_dict,
            final_flux_relative_distance_dict=final_flux_relative_distance_dict,
            absolute_y_lim_dict=each_simulated_absolute_y_lim_dict,
            relative_y_lim_dict=each_simulated_relative_y_lim_dict,
            final_raw_euclidian_distance_dict=final_raw_mean_euclidian_distance_dict,
            final_net_euclidian_distance_dict=final_net_mean_euclidian_distance_dict,
            final_raw_all_select_euclidian_distance_dict=final_raw_all_select_euclidian_distance_dict,
            final_net_all_select_euclidian_distance_dict=final_net_all_select_euclidian_distance_dict,
            maximal_net_euclidian_distance=max_net_euclidian_distance,
            net_distance_between_different_simulated_flux_dict=net_distance_between_different_simulated_flux_dict,
            net_all_selected_relative_error_dict=net_all_selected_relative_error_dict,
            net_selected_averaged_relative_error_dict=net_selected_averaged_relative_error_dict,
            raw_loss_value_dict=raw_selected_loss_value_dict,
            loss_of_mean_solution_dict=loss_of_mean_solution_dict,
            max_loss_value=max_loss_value,
            x_label_index_dict=x_label_index_dict, y_label_index_dict=y_label_index_dict,
            analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
            raw_selected_predicted_data_dict=raw_selected_predicted_data_dict,
        )
    else:
        flatten_2d_data_dict(raw_selected_flux_value_dict)
        flatten_2d_data_dict(raw_selected_diff_vector_dict)
        flatten_2d_data_dict(raw_selected_loss_value_dict)
        flatten_2d_data_dict(final_raw_all_select_euclidian_distance_dict)
        flatten_2d_data_dict(final_net_all_select_euclidian_distance_dict)
        flatten_2d_data_dict(net_all_selected_relative_error_dict)

        data_label = final_information_dict.values().__iter__().__next__()[Keywords.data][Keywords.label]
        (
            initial_raw_selected_flux_value_dict, initial_averaged_flux_value_dict,
            initial_raw_selected_diff_vector_dict, initial_averaged_diff_vector_dict,
            loss_of_initial_raw_selected_solutions_dict, loss_of_initial_averaged_solutions_dict,
            raw_euclidian_distance_of_initial_raw_selected_dict,
            net_euclidian_distance_of_initial_raw_selected_dict,
            raw_euclidian_distance_of_initial_averaged_solutions_dict,
            net_euclidian_distance_of_initial_averaged_solutions_dict,
            net_relative_error_of_initial_raw_selected_dict,
            net_relative_error_of_initial_averaged_solutions_dict,
            flux_relative_distance_of_initial_averaged_solutions_dict,
            net_distance_between_different_simulated_flux_dict,
        ) = averaged_solution_data_obj.return_averaged_data(data_label)

        flatten_2d_data_dict(initial_raw_selected_flux_value_dict)
        flatten_2d_data_dict(initial_raw_selected_diff_vector_dict)
        flatten_2d_data_dict(initial_averaged_diff_vector_dict)
        flatten_2d_data_dict(loss_of_initial_raw_selected_solutions_dict)
        flatten_2d_data_dict(net_euclidian_distance_of_initial_raw_selected_dict)
        flatten_2d_data_dict(net_relative_error_of_initial_raw_selected_dict)
        flatten_2d_data_dict(net_relative_error_of_initial_averaged_solutions_dict)
        figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
        figure_raw_data.save_data(
            initial_raw_selected_flux_value_dict=initial_raw_selected_flux_value_dict,
            initial_averaged_flux_value_dict=initial_averaged_flux_value_dict,
            raw_selected_flux_value_dict=raw_selected_flux_value_dict,

            initial_raw_selected_diff_vector_dict=initial_raw_selected_diff_vector_dict,
            initial_averaged_diff_vector_dict=initial_averaged_diff_vector_dict,
            raw_selected_diff_vector_dict=raw_selected_diff_vector_dict,

            common_flux_name_list=common_flux_name_list,

            flux_relative_distance_of_initial_averaged_solutions_dict=flux_relative_distance_of_initial_averaged_solutions_dict,
            final_flux_relative_distance_dict=final_flux_relative_distance_dict,

            net_distance_between_different_simulated_flux_dict=net_distance_between_different_simulated_flux_dict,
            raw_euclidian_distance_of_initial_raw_selected_dict=raw_euclidian_distance_of_initial_raw_selected_dict,
            net_euclidian_distance_of_initial_raw_selected_dict=net_euclidian_distance_of_initial_raw_selected_dict,
            raw_euclidian_distance_of_initial_averaged_solutions_dict=raw_euclidian_distance_of_initial_averaged_solutions_dict,
            net_euclidian_distance_of_initial_averaged_solutions_dict=net_euclidian_distance_of_initial_averaged_solutions_dict,
            final_raw_all_select_euclidian_distance_dict=final_raw_all_select_euclidian_distance_dict,
            final_net_all_select_euclidian_distance_dict=final_net_all_select_euclidian_distance_dict,
            maximal_raw_euclidian_distance=max_raw_euclidian_distance,
            maximal_net_euclidian_distance=max_net_euclidian_distance,

            net_relative_error_of_initial_raw_selected_dict=net_relative_error_of_initial_raw_selected_dict,
            net_relative_error_of_initial_averaged_solutions_dict=net_relative_error_of_initial_averaged_solutions_dict,
            net_all_selected_relative_error_dict=net_all_selected_relative_error_dict,

            loss_of_initial_raw_selected_solutions_dict=loss_of_initial_raw_selected_solutions_dict,
            loss_of_initial_averaged_solutions_dict=loss_of_initial_averaged_solutions_dict,
            raw_loss_value_dict=raw_selected_loss_value_dict,
            max_loss_value=max_loss_value,

            x_label_index_dict=x_label_index_dict, y_label_index_dict=y_label_index_dict,
            analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
            raw_selected_predicted_data_dict=raw_selected_predicted_data_dict,
        )


def data_sensitivity_result_processing(
        result_name, solver_dict, final_information_dict, final_loss_data_dict, final_solution_data_dict,
        final_predicted_data_dict, processed_mid_name_dict, final_flux_name_index_dict,
        common_simulated_flux_value_dict, analyzed_set_size_list, selected_min_loss_size_list,
        repeat_time_each_analyzed_set, net_flux_list, replace_flux_dict, flux_range, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path,
):
    print(f'Start result analysis for {result_name}...')
    min_value, max_value = flux_range
    final_flux_absolute_distance_dict = DefaultDict({})
    final_flux_relative_distance_dict = DefaultDict({})
    final_raw_mean_euclidian_distance_dict = DefaultDict(None)
    final_net_mean_euclidian_distance_dict = DefaultDict({})
    final_raw_all_select_euclidian_distance_dict = DefaultDict(None)
    final_net_all_select_euclidian_distance_dict = DefaultDict({})
    maximal_absolute_distance_dict = DefaultDict({})
    maximal_relative_distance_dict = DefaultDict({})
    max_raw_euclidian_distance = 0
    max_net_euclidian_distance = 0
    raw_selected_flux_value_dict = DefaultDict({})
    selected_averaged_flux_value_dict = DefaultDict({})
    raw_selected_diff_vector_dict = DefaultDict({})
    selected_averaged_diff_vector_dict = DefaultDict({})
    net_all_selected_relative_error_dict = DefaultDict({})
    net_selected_averaged_relative_error_dict = DefaultDict({})
    raw_selected_loss_value_dict = DefaultDict({})
    loss_of_mean_solution_dict = DefaultDict({})
    raw_selected_predicted_data_dict = DefaultDict({})
    selected_averaged_predicted_data_dict = DefaultDict({})
    each_flux_absolute_y_lim_dict = DefaultDict({})
    each_flux_relative_y_lim_dict = DefaultDict({})
    max_loss_value = 0

    common_flux_name_list = None

    for result_label, solution_data_array in final_solution_data_dict.items():
        result_information = final_information_dict[result_label]
        data_label = str(result_information[Keywords.data][Keywords.label])
        loss_data_array = final_loss_data_dict[result_label]
        predicted_data_dict = final_predicted_data_dict[result_label]
        solver_obj = solver_dict[result_label]
        flux_name_index_dict = final_flux_name_index_dict[result_label]

        sorted_index_array = np.argsort(loss_data_array)
        total_data_size = len(loss_data_array)

        (
            flux_name_simulated_value_dict, simulated_flux_vector, simulated_net_flux_vector,
            this_common_flux_name_list, net_flux_matrix, normal_core_flux_index_array
        ) = analyze_simulated_flux_value_dict(
            common_simulated_flux_value_dict, net_flux_list, flux_name_index_dict)

        if common_flux_name_list is None:
            common_flux_name_list = this_common_flux_name_list

        for analyzed_set_size in analyzed_set_size_list:
            for selected_min_loss_size in selected_min_loss_size_list:
                max_raw_euclidian_distance, max_net_euclidian_distance, max_loss_value = each_cycle_analyzer(
                    analyzed_set_size, selected_min_loss_size,
                    solution_data_array, loss_data_array, predicted_data_dict, solver_obj, flux_name_index_dict,
                    flux_name_simulated_value_dict, net_flux_matrix, simulated_flux_vector, simulated_net_flux_vector,
                    normal_core_flux_index_array, total_data_size, replace_flux_dict, max_value - min_value,

                    final_flux_absolute_distance_dict[data_label],
                    final_flux_relative_distance_dict[data_label],
                    final_raw_mean_euclidian_distance_dict[data_label],
                    final_net_mean_euclidian_distance_dict[data_label],
                    final_raw_all_select_euclidian_distance_dict[data_label],
                    final_net_all_select_euclidian_distance_dict[data_label],
                    maximal_absolute_distance_dict[data_label],
                    maximal_relative_distance_dict[data_label],
                    max_raw_euclidian_distance,
                    max_net_euclidian_distance,
                    raw_selected_flux_value_dict[data_label],
                    selected_averaged_flux_value_dict[data_label],
                    raw_selected_diff_vector_dict[data_label],
                    selected_averaged_diff_vector_dict[data_label],
                    net_all_selected_relative_error_dict[data_label],
                    net_selected_averaged_relative_error_dict[data_label],
                    raw_selected_loss_value_dict[data_label],
                    loss_of_mean_solution_dict[data_label],
                    processed_mid_name_dict,
                    raw_selected_predicted_data_dict[data_label],
                    selected_averaged_predicted_data_dict[data_label],
                    max_loss_value,
                    select_mode=True,
                    sorted_index_array=sorted_index_array,
                    repeat_time_each_analyzed_set=repeat_time_each_analyzed_set,
                )

        each_flux_absolute_y_lim_dict[result_label] = generate_y_lim_dict(
            maximal_absolute_distance_dict[result_label])
        each_flux_relative_y_lim_dict[result_label] = generate_y_lim_dict(
            maximal_relative_distance_dict[result_label])

        flatten_2d_data_dict(raw_selected_flux_value_dict[data_label])
        flatten_2d_data_dict(selected_averaged_flux_value_dict[data_label])
        flatten_2d_data_dict(raw_selected_diff_vector_dict[data_label])
        flatten_2d_data_dict(selected_averaged_diff_vector_dict[data_label])
        flatten_2d_data_dict(raw_selected_loss_value_dict[data_label])
        flatten_2d_data_dict(loss_of_mean_solution_dict[data_label])
        flatten_2d_data_dict(final_net_all_select_euclidian_distance_dict[data_label])
        flatten_2d_data_dict(final_net_mean_euclidian_distance_dict[data_label])
        flatten_2d_data_dict(net_all_selected_relative_error_dict[data_label])
        flatten_2d_data_dict(net_selected_averaged_relative_error_dict[data_label])

    x_label_index_dict = {
        analyzed_set_size: index for index, analyzed_set_size in enumerate(analyzed_set_size_list)}
    y_label_index_dict = {
        selected_min_loss_size: index for index, selected_min_loss_size in enumerate(selected_min_loss_size_list)}

    print('Saving result files...')
    figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
    figure_raw_data.save_data(
        raw_selected_flux_value_dict=dict(raw_selected_flux_value_dict),
        selected_averaged_flux_value_dict=dict(selected_averaged_flux_value_dict),
        raw_selected_diff_vector_dict=dict(raw_selected_diff_vector_dict),
        selected_averaged_diff_vector_dict=dict(selected_averaged_diff_vector_dict),
        common_flux_name_list=common_flux_name_list,
        final_flux_absolute_distance_dict=dict(final_flux_absolute_distance_dict),
        final_flux_relative_distance_dict=dict(final_flux_relative_distance_dict),
        absolute_y_lim_dict=dict(each_flux_absolute_y_lim_dict),
        relative_y_lim_dict=dict(each_flux_relative_y_lim_dict),
        final_net_euclidian_distance_dict=dict(final_net_mean_euclidian_distance_dict),
        final_net_all_select_euclidian_distance_dict=dict(final_net_all_select_euclidian_distance_dict),
        net_all_selected_relative_error_dict=dict(net_all_selected_relative_error_dict),
        net_selected_averaged_relative_error_dict=dict(net_selected_averaged_relative_error_dict),
        maximal_net_euclidian_distance=max_net_euclidian_distance,
        raw_loss_value_dict=dict(raw_selected_loss_value_dict),
        loss_of_mean_solution_dict=dict(loss_of_mean_solution_dict),
        max_loss_value=max_loss_value,
        x_label_index_dict=dict(x_label_index_dict), y_label_index_dict=dict(y_label_index_dict),
        analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
        raw_selected_predicted_data_dict=dict(raw_selected_predicted_data_dict),
    )

