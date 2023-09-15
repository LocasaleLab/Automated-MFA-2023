from scripts.src.common.built_in_packages import abc
from scripts.src.common.third_party_packages import np
from scripts.src.common.config import Color, Direct, Keywords as CommonKeywords
from scripts.src.common.classes import FinalResult
from scripts.src.common.plotting_functions import group_violin_box_distribution_plot, \
    multi_row_col_scatter_plot_for_result_selection, heat_map_plotting, HeatmapValueFormat
from scripts.src.common.functions import add_empty_obj
from scripts.src.common.result_processing_functions import loss_data_distribution_plotting, \
    experimental_mid_prediction
from ..common.result_output_functions import output_raw_flux_data, output_predicted_mid_data

from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.figure_data_format import FigureData
from common_and_plotting_functions.core_plotting_functions import heatmap_and_box3d_parameter_preparation
from common_and_plotting_functions.config import FigureDataKeywords

from scripts.src.core.common.config import CoreConstants
from .sensitivity_config import ExperimentName, ModelSetting, DataSetting, Keywords
from . import config

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
            self, project_output_direct, common_data_output_direct, result_name, target_simulated_flux_value_dict):
        super(CurrentFinalResult, self).__init__(
            project_output_direct, common_data_output_direct, result_name, target_simulated_flux_value_dict)

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
            self, solver_dict, final_information_dict, result_process_name, result_process_func, *args):
        self.final_information_dict = final_information_dict
        raw_data_analyzing_num = 20000
        # for current_model_label in model_label_list:
        #     for current_data_label in data_label_list:
        #         for current_config_label in config_label_list:
        #             current_result_label = result_label_generator(
        #                 current_model_label, current_data_label, current_config_label)
        for current_result_label in solver_dict.keys():
            (
                loss_data_array, solution_data_array, flux_name_index_dict, _,
                predicted_data_dict, target_experimental_mid_data_dict, _) = self.iteration(current_result_label)
            if current_result_label in raw_model_data_result_label_dict:
                total_data_size = len(loss_data_array)
                if result_process_name != Keywords.raw_model_result_process and \
                        total_data_size > raw_data_analyzing_num:
                    analyzed_index_array = np.random.choice(
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

        final_data_list = [
            self.final_loss_data_dict, self.final_solution_data_dict,
            self.final_flux_name_index_dict, self.final_information_dict,
            self.final_predicted_data_dict, self.final_target_experimental_mid_data_dict,
            self.simulated_flux_value_dict]

        output_direct_list = [
            self.this_result_output_direct,
            self.flux_comparison_output_direct,
            self.mid_prediction_output_direct,
            self.flux_result_output_xlsx_path,
            self.mid_prediction_result_output_xlsx_path]

        result_process_func(self.result_name, *final_data_list, *output_direct_list, *args)


def normal_result_process(
        result_name, final_loss_data_dict, final_solution_data_dict,
        final_flux_name_index_dict, final_information_dict,
        final_predicted_data_dict, final_target_experimental_mid_data_dict, simulated_flux_value_dict,
        this_result_output_direct, flux_comparison_output_direct, mid_prediction_output_direct,
        flux_result_output_xlsx_path, mid_prediction_result_output_xlsx_path, important_flux_list,
        important_flux_replace_dict, net_flux_list, loss_percentile, *other_args):
    subset_index_dict = loss_data_distribution_plotting(
        result_name, final_loss_data_dict, output_direct=this_result_output_direct,
        loss_percentile=loss_percentile)
    output_raw_flux_data(
        flux_result_output_xlsx_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
        final_information_dict, subset_index_dict=subset_index_dict)
    output_predicted_mid_data(
        mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
        final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=subset_index_dict)
    important_flux_display(
        final_solution_data_dict, final_flux_name_index_dict, final_information_dict,
        important_flux_list, simulated_flux_value_dict, important_flux_replace_dict,
        flux_comparison_output_direct, subset_index_dict=subset_index_dict)
    # normal_flux_euclidean_distance_plotting(
    #     final_solution_data_dict, final_flux_name_index_dict,
    #     simulated_flux_value_dict, net_flux_list, subset_index_dict=subset_index_dict)
    all_fluxes_relative_error_heatmap(
        result_name, flux_comparison_output_direct, final_solution_data_dict, final_flux_name_index_dict,
        simulated_flux_value_dict, net_flux_list, important_flux_replace_dict, subset_index_dict)


def raw_model_result_process(
        result_name, final_loss_data_dict, final_solution_data_dict,
        final_flux_name_index_dict, final_information_dict,
        final_predicted_data_dict, final_target_experimental_mid_data_dict, simulated_flux_value_dict,
        this_result_output_direct, flux_comparison_output_direct, mid_prediction_output_direct,
        flux_result_output_xlsx_path, mid_prediction_result_output_xlsx_path, important_flux_list,
        important_flux_replace_dict, mfa_config, net_flux_list, *other_args):
    analyzed_set_size_list = (
        100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000
    )
    repeat_time_each_analyzed_set = 30
    selected_min_loss_size_list = (1, 2, 5, 10, 20, 50, 100, 200, 500)
    flux_range = mfa_config.common_flux_range
    # raw_model_prediction(
    #     result_name, final_loss_data_dict, final_predicted_data_dict, final_target_experimental_mid_data_dict,
    #     500, 10, mid_prediction_output_direct)
    assert len(final_loss_data_dict) == 1
    result_label, loss_data_array = final_loss_data_dict.items().__iter__().__next__()
    solution_data_array = final_solution_data_dict[result_label]
    flux_name_index_dict = final_flux_name_index_dict[result_label]
    information_dict = final_information_dict[result_label]
    predicted_data_dict = final_predicted_data_dict[result_label]
    target_experimental_mid_data_dict = final_target_experimental_mid_data_dict[result_label]
    raw_model_approximation_percentile_analysis(
        result_name, loss_data_array, solution_data_array, flux_name_index_dict, information_dict,
        predicted_data_dict, target_experimental_mid_data_dict, simulated_flux_value_dict,
        important_flux_list, important_flux_replace_dict, analyzed_set_size_list, selected_min_loss_size_list,
        repeat_time_each_analyzed_set, flux_range, this_result_output_direct, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path, net_flux_list)


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
        # if isinstance(flux_name, str):
        #     single_flux = True
        #     flux_title = flux_name
        #     tmp_flux_name = flux_name
        #     while tmp_flux_name not in simulated_flux_value_dict:
        #         tmp_flux_name = replace_flux_dict[tmp_flux_name]
        #     simulated_flux_value = simulated_flux_value_dict[tmp_flux_name]
        # elif isinstance(flux_name, tuple) or isinstance(flux_name, list):
        #     single_flux = False
        #     tmp_flux_name1, tmp_flux_name2 = flux_name
        #     while tmp_flux_name1 not in simulated_flux_value_dict:
        #         tmp_flux_name1 = replace_flux_dict[tmp_flux_name1]
        #     while tmp_flux_name2 not in simulated_flux_value_dict:
        #         tmp_flux_name2 = replace_flux_dict[tmp_flux_name2]
        #     simulated_flux_value1 = simulated_flux_value_dict[tmp_flux_name1]
        #     simulated_flux_value2 = simulated_flux_value_dict[tmp_flux_name2]
        #     if simulated_flux_value1 > simulated_flux_value2:
        #         raw_flux_name1 = tmp_flux_name1
        #         raw_flux_name2 = tmp_flux_name2
        #     else:
        #         raw_flux_name1 = tmp_flux_name2
        #         raw_flux_name2 = tmp_flux_name1
        #     simulated_flux_value = simulated_flux_value_dict[raw_flux_name1] - simulated_flux_value_dict[raw_flux_name2]
        #     flux_title = '{} - {}'.format(raw_flux_name1, raw_flux_name2)
        # else:
        #     raise ValueError()
        # for result_label, solution_array in solution_array_dict.items():
        #     current_flux_name_index_dict = flux_name_index_dict[result_label]
        #     # current_information_dict = information_dict[result_label]
        #     # if result_label == raw_result_label:
        #     #     result_label = 'Raw'
        #     #     current_color = Color.blue
        #     # else:
        #     #     current_color = Color.orange
        #     if subset_index_dict is not None:
        #         target_solution_array = solution_array[subset_index_dict[result_label], :]
        #     else:
        #         target_solution_array = solution_array
        #     if isinstance(flux_name, str):
        #         replace_flux = flux_name
        #         try:
        #             while replace_flux not in current_flux_name_index_dict:
        #                 replace_flux = replace_flux_dict[replace_flux]
        #         except KeyError:
        #             current_flux_data_dict[result_label] = empty_array
        #         else:
        #             current_flux_index = current_flux_name_index_dict[replace_flux]
        #             if replace_flux != flux_name:
        #                 result_label = '{}__{}'.format(result_label, replace_flux)
        #             current_flux_data_dict[result_label] = target_solution_array[:, current_flux_index]
        #     elif isinstance(flux_name, tuple):
        #         result_array = 0
        #         flux_name1 = flux_name[0]
        #         flux_name2 = flux_name[1]
        #         try:
        #             while (
        #                     (flux_name1 not in current_flux_name_index_dict) and
        #                     (flux_name2 not in current_flux_name_index_dict)):
        #                 flux_name1 = replace_flux_dict[flux_name1]
        #                 flux_name2 = replace_flux_dict[flux_name2]
        #         except KeyError:
        #             current_flux_data_dict[result_label] = empty_array
        #         else:
        #             if flux_name1 in current_flux_name_index_dict:
        #                 result_array += target_solution_array[:, current_flux_name_index_dict[flux_name1]]
        #             if flux_name2 in current_flux_name_index_dict:
        #                 result_array -= target_solution_array[:, current_flux_name_index_dict[flux_name2]]
        #             current_flux_data_dict[result_label] = result_array
        #     else:
        #         raise ValueError()
        #     # current_color_dict[result_label] = current_color
        #     current_color_dict[result_label] = Color.blue

        simulated_flux_value, flux_title, reverse_order, common_flux_name = determine_order_by_simulated_data(
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
    if reduced_metric == Keywords.median:
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


def net_flux_matrix_generator(net_flux_list, flux_name_index_dict, simulated_flux_value_dict):
    net_flux_name_flux_pair_dict = {}
    for flux_name0, flux_name1 in net_flux_list:
        net_flux_name_flux_pair_dict[flux_name0] = (flux_name0, flux_name1)
        net_flux_name_flux_pair_dict[flux_name1] = (flux_name0, flux_name1)
    total_raw_flux_num = len(simulated_flux_value_dict)
    analyzed_flux_set = set()
    final_array_list = []
    for flux_name in simulated_flux_value_dict.keys():
        if flux_name in analyzed_flux_set:
            continue
        new_one_hot_array = np.zeros(total_raw_flux_num)
        if flux_name in net_flux_name_flux_pair_dict:
            flux_name_pair = net_flux_name_flux_pair_dict[flux_name]
            _, _, reverse_order, _ = determine_order_by_simulated_data(
                flux_name_pair, simulated_flux_value_dict)
            if not reverse_order:
                (flux_name0, flux_name1) = flux_name_pair
            else:
                (flux_name1, flux_name0) = flux_name_pair
            # (flux_name0, flux_name1) = flux_name_pair
            new_one_hot_array[flux_name_index_dict[flux_name0]] = 1
            new_one_hot_array[flux_name_index_dict[flux_name1]] = -1
            analyzed_flux_set.add(flux_name0)
            analyzed_flux_set.add(flux_name1)
        else:
            new_one_hot_array[flux_name_index_dict[flux_name]] = 1
            analyzed_flux_set.add(flux_name)
        final_array_list.append(new_one_hot_array)
    return np.array(final_array_list)


def euclidean_distance_of_mean_point_to_simulated_array(
        solution_data_array, simulated_flux_value_dict, flux_name_index_dict,
        net_flux_matrix):
    simulated_flux_vector = np.zeros(len(simulated_flux_value_dict))
    filtered_solution_flux_index = np.zeros(len(simulated_flux_value_dict), dtype=int)
    flux_name_list = []
    for simulated_flux_index, (flux_name, flux_value) in enumerate(simulated_flux_value_dict.items()):
        current_index = flux_name_index_dict[flux_name]
        simulated_flux_vector[simulated_flux_index] = flux_value
        filtered_solution_flux_index[simulated_flux_index] = current_index
        flux_name_list.append(flux_name)
    mean_selected_solution_vector = solution_data_array[:, filtered_solution_flux_index].mean(axis=0)
    raw_diff_vector = mean_selected_solution_vector - simulated_flux_vector
    test_flux_name_diff_dict = {
        flux_name: raw_diff_vector[flux_index]
        for flux_index, flux_name in enumerate(flux_name_list)}
    raw_euclidean_distance = np.sqrt(np.sum(raw_diff_vector ** 2))
    net_diff_vector = (
            net_flux_matrix @ mean_selected_solution_vector.reshape([-1, 1]) -
            net_flux_matrix @ simulated_flux_vector.reshape([-1, 1])).reshape([-1])
    new_euclidean_distance = np.sqrt(np.sum(net_diff_vector ** 2))
    return raw_euclidean_distance, new_euclidean_distance


def link_flux_name(*flux_name_list):
    return '_'.join(flux_name_list)


def determine_order_by_simulated_data(standard_flux_name, simulated_flux_value_dict):
    reverse_order = False
    if isinstance(standard_flux_name, str):
        simulated_flux_value = simulated_flux_value_dict[standard_flux_name]
        flux_title = standard_flux_name
        common_flux_name = standard_flux_name
    elif isinstance(standard_flux_name, (tuple, list)):
        flux_name0, flux_name1 = standard_flux_name
        simulated_flux_value1 = simulated_flux_value_dict[flux_name0]
        simulated_flux_value2 = simulated_flux_value_dict[flux_name1]
        if simulated_flux_value1 < simulated_flux_value2:
            flux_name1, flux_name0 = standard_flux_name
            reverse_order = True
        simulated_flux_value = simulated_flux_value_dict[flux_name0] - simulated_flux_value_dict[flux_name1]
        flux_title = '{} - {}'.format(flux_name0, flux_name1)
        common_flux_name = link_flux_name(flux_name0, flux_name1)
    else:
        raise ValueError()
    return simulated_flux_value, flux_title, reverse_order, common_flux_name


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
        complete_analyzed_index_set_array = np.random.choice(
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


def net_flux_pair_dict_constructor(net_flux_list):
    net_flux_pair_dict = {}
    for flux_name0, flux_name1 in net_flux_list:
        net_flux_pair_dict[flux_name0] = (flux_name0, flux_name1)
        net_flux_pair_dict[flux_name1] = (flux_name0, flux_name1)
    return net_flux_pair_dict


def net_flux_pair_analyzer(flux_name, net_flux_pair_dict, analyzed_flux_set):
    if flux_name in net_flux_pair_dict:
        modified_flux_name = net_flux_pair_dict[flux_name]
        for one_directional_flux_name in modified_flux_name:
            analyzed_flux_set.add(one_directional_flux_name)
    else:
        modified_flux_name = flux_name
        analyzed_flux_set.add(flux_name)
    return modified_flux_name


def raw_model_approximation_percentile_analysis(
        result_name, loss_data_array, solution_data_array, flux_name_index_dict, raw_information_dict,
        predicted_data_dict, target_experimental_mid_data_dict, simulated_flux_value_dict,
        important_flux_list, replace_flux_dict, analyzed_set_size_list,
        selected_min_loss_size_list, repeat_time_each_analyzed_set,
        flux_range, this_result_output_direct, flux_result_output_xlsx_path,
        mid_prediction_result_output_xlsx_path, net_flux_list):
    def generate_y_lim_dict(maximal_distance_dict):
        y_lim_dict = {}
        for flux_title, maximal_absolute_distance in maximal_distance_dict.items():
            if maximal_absolute_distance < 0.1:
                distance_factor = 100.0
            else:
                distance_factor = 10.0
            y_lim_dict[flux_title] = np.ceil(maximal_absolute_distance * distance_factor) / distance_factor
        return y_lim_dict

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
            distribution_output_direct, 0, None, figsize=None, value_number_format=HeatmapValueFormat.scientific_format)
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

    def output_analyzed_raw_flux_and_predicted_mid_data():
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
                    current_repeat_index_list = []
                    current_each_repeat_index_list = []
                    for repeat_index, raw_loss_array in enumerate(current_raw_loss_array_list):
                        current_size = len(raw_loss_array)
                        current_repeat_index_list.extend([repeat_index + 1] * current_size)
                        current_each_repeat_index_list.extend(range(1, current_size + 1))
                    index_column_dict[result_label] = {
                        'repeat_index': current_repeat_index_list,
                        'index_in_each_repeat': current_each_repeat_index_list
                    }
                    final_solution_data_dict[result_label] = np.vstack(current_raw_solution_array_list)
                    final_loss_data_dict[result_label] = np.hstack(current_raw_loss_array_list)
                    final_predicted_data_dict[result_label] = current_raw_predicted_data_dict
                    final_target_experimental_mid_data_dict[result_label] = target_experimental_mid_data_dict
                    final_flux_name_index_dict[result_label] = flux_name_index_dict
                    final_information_dict[result_label] = {
                        **raw_information_dict,
                        'total_analyzed_set_size': analyzed_set_size,
                        'num_of_min_loss_be_selected': selected_min_loss_size
                    }
        output_raw_flux_data(
            flux_result_output_xlsx_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
            final_information_dict, subset_index_dict=None, other_label_column_dict=index_column_dict)
        output_predicted_mid_data(
            mid_prediction_result_output_xlsx_path, final_loss_data_dict, final_predicted_data_dict,
            final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=None,
            other_label_row_dict=index_column_dict)

    print('Start result analysis...')
    net_flux_pair_dict = net_flux_pair_dict_constructor(net_flux_list)
    min_value, max_value = flux_range
    # reduced_metric = Keywords.median
    reduced_metric = Keywords.mean
    final_flux_absolute_distance_dict = {}
    final_flux_relative_distance_dict = {}
    final_raw_euclidian_distance_dict = {}
    final_net_euclidian_distance_dict = {}
    sorted_index_array = np.argsort(loss_data_array)
    maximal_absolute_distance_dict = {}
    maximal_relative_distance_dict = {}
    maximal_raw_euclidian_distance = 0
    maximal_net_euclidian_distance = 0
    raw_selected_flux_value_dict = {}
    raw_selected_loss_value_dict = {}
    raw_selected_predicted_data_dict = {}
    max_loss_value = 0
    total_data_size = len(loss_data_array)
    common_flux_name_dict = {}
    net_flux_matrix = net_flux_matrix_generator(net_flux_list, flux_name_index_dict, simulated_flux_value_dict)
    for analyzed_set_size in analyzed_set_size_list:
        for selected_min_loss_size in selected_min_loss_size_list:
            print(f'Analyzing total_size={analyzed_set_size} and select_size={selected_min_loss_size}...')
            if selected_min_loss_size > analyzed_set_size:
                add_empty_obj(
                    final_raw_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
                add_empty_obj(
                    final_net_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
                # for flux_name in important_flux_list:
                analyzed_flux_set = set()
                for flux_name in simulated_flux_value_dict.keys():
                    if flux_name in analyzed_flux_set:
                        continue
                    modified_flux_name = net_flux_pair_analyzer(flux_name, net_flux_pair_dict, analyzed_flux_set)
                    _, flux_title, reverse_order, common_flux_name = determine_order_by_simulated_data(
                        modified_flux_name, simulated_flux_value_dict)
                    if common_flux_name not in common_flux_name_dict:
                        common_flux_name_dict[common_flux_name] = None
                    flux_title = common_flux_name  # Test
                    add_empty_obj(
                        final_flux_absolute_distance_dict, list, flux_title, selected_min_loss_size, analyzed_set_size)
                    add_empty_obj(
                        final_flux_relative_distance_dict, list, flux_title, selected_min_loss_size, analyzed_set_size)
            else:
                total_required_num = repeat_time_each_analyzed_set * analyzed_set_size
                if total_required_num > total_data_size:
                    replace = True
                else:
                    replace = False
                all_repeat_analyzed_index_set_array = np.random.choice(
                        total_data_size, repeat_time_each_analyzed_set * analyzed_set_size, replace=replace)
                for repeat_time_index in range(repeat_time_each_analyzed_set):
                    # complete_analyzed_index_set_array = np.random.choice(
                    #     total_data_size, analyzed_set_size, replace=False)
                    complete_analyzed_index_set_array = all_repeat_analyzed_index_set_array[
                        repeat_time_index * analyzed_set_size:(repeat_time_index + 1) * analyzed_set_size].copy()
                    complete_analyzed_index_set_array.sort()
                    ordered_selected_index_array = sorted_index_array[
                        complete_analyzed_index_set_array[:selected_min_loss_size]]
                    ordered_selected_solution_data_array = solution_data_array[ordered_selected_index_array, :]
                    add_empty_obj(
                        raw_selected_flux_value_dict, list, analyzed_set_size, selected_min_loss_size)
                    raw_selected_flux_value_dict[analyzed_set_size][selected_min_loss_size].append(
                        ordered_selected_solution_data_array)
                    add_empty_obj(
                        raw_selected_loss_value_dict, list, selected_min_loss_size, analyzed_set_size)
                    current_loss_array = loss_data_array[ordered_selected_index_array]
                    raw_selected_loss_value_dict[selected_min_loss_size][analyzed_set_size].append(current_loss_array)
                    # add_empty_obj(
                    #     raw_selected_predicted_data_dict, dict, selected_min_loss_size, analyzed_set_size)
                    for mid_name, mid_value_list in predicted_data_dict.items():
                        add_empty_obj(
                            raw_selected_predicted_data_dict, list, selected_min_loss_size, analyzed_set_size, mid_name)
                        raw_selected_predicted_data_dict[selected_min_loss_size][analyzed_set_size][mid_name].extend(
                            [mid_value_list[selected_index] for selected_index in ordered_selected_index_array]
                        )
                    # raw_selected_predicted_data_dict[selected_min_loss_size][analyzed_set_size] = {
                    #     mid_name: [mid_value_list[selected_index] for selected_index in ordered_selected_index_array]
                    #     for mid_name, mid_value_list in predicted_data_dict.items()
                    # }
                    max_loss_value = np.maximum(max_loss_value, np.max(current_loss_array))

                    add_empty_obj(
                        final_raw_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
                    add_empty_obj(
                        final_net_euclidian_distance_dict, list, selected_min_loss_size, analyzed_set_size)
                    raw_euclidean_distance, net_euclidean_distance = euclidean_distance_of_mean_point_to_simulated_array(
                        ordered_selected_solution_data_array, simulated_flux_value_dict, flux_name_index_dict,
                        net_flux_matrix)
                    final_raw_euclidian_distance_dict[selected_min_loss_size][analyzed_set_size].append(
                        raw_euclidean_distance)
                    final_net_euclidian_distance_dict[selected_min_loss_size][analyzed_set_size].append(
                        net_euclidean_distance)
                    maximal_raw_euclidian_distance = np.maximum(maximal_raw_euclidian_distance, raw_euclidean_distance)
                    maximal_net_euclidian_distance = np.maximum(maximal_net_euclidian_distance, net_euclidean_distance)
                    # for flux_name in important_flux_list:
                    analyzed_flux_set = set()
                    for flux_name in simulated_flux_value_dict.keys():
                        if flux_name in analyzed_flux_set:
                            continue
                        modified_flux_name = net_flux_pair_analyzer(
                            flux_name, net_flux_pair_dict, analyzed_flux_set)
                        simulated_flux_value, flux_title, reverse_order, common_flux_name = \
                            determine_order_by_simulated_data(modified_flux_name, simulated_flux_value_dict)
                        if common_flux_name not in common_flux_name_dict:
                            common_flux_name_dict[common_flux_name] = None
                        flux_title = common_flux_name  # Test
                        current_flux_data_array, _ = decipher_flux_title(
                            modified_flux_name, flux_name_index_dict, replace_flux_dict,
                            ordered_selected_solution_data_array, reverse_order)
                        add_empty_obj(
                            final_flux_absolute_distance_dict, list, flux_title, selected_min_loss_size,
                            analyzed_set_size)
                        add_empty_obj(
                            final_flux_relative_distance_dict, list, flux_title, selected_min_loss_size,
                            analyzed_set_size)
                        absolute_distance = normalized_difference_to_array(
                            current_flux_data_array, simulated_flux_value, max_value - min_value, reduced_metric)
                        final_flux_absolute_distance_dict[flux_title][selected_min_loss_size][analyzed_set_size].append(
                            absolute_distance)
                        relative_distance = normalized_difference_to_array(
                            current_flux_data_array, simulated_flux_value, None, reduced_metric)
                        final_flux_relative_distance_dict[flux_title][selected_min_loss_size][analyzed_set_size].append(
                            relative_distance)
                        if flux_title not in maximal_absolute_distance_dict:
                            maximal_absolute_distance_dict[flux_title] = np.abs(absolute_distance)
                            maximal_relative_distance_dict[flux_title] = np.abs(relative_distance)
                        else:
                            maximal_absolute_distance_dict[flux_title] = np.maximum(
                                maximal_absolute_distance_dict[flux_title], np.abs(absolute_distance))
                            maximal_relative_distance_dict[flux_title] = np.maximum(
                                maximal_relative_distance_dict[flux_title], np.abs(relative_distance))

    absolute_y_lim_dict = generate_y_lim_dict(maximal_absolute_distance_dict)
    relative_y_lim_dict = generate_y_lim_dict(maximal_relative_distance_dict)
    x_label_index_dict = {
        analyzed_set_size: index for index, analyzed_set_size in enumerate(analyzed_set_size_list)}
    y_label_index_dict = {
        selected_min_loss_size: index for index, selected_min_loss_size in enumerate(selected_min_loss_size_list)}

    print('Finish analysis. Printing result figures...')
    current_result_output_direct = '{}/{}'.format(
        this_result_output_direct, config.Direct.raw_model_approximation_percentile)
    current_metric_output_direct = '{}/{}'.format(current_result_output_direct, reduced_metric)
    absolute_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.absolute_distance)
    check_and_mkdir_of_direct(absolute_distance_output_direct)
    relative_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.relative_distance)
    check_and_mkdir_of_direct(relative_distance_output_direct)
    scatter_plotting(final_flux_absolute_distance_dict, absolute_y_lim_dict, absolute_distance_output_direct)
    scatter_plotting(final_flux_relative_distance_dict, relative_y_lim_dict, relative_distance_output_direct)
    heatmap_and_box3d_plotting_by_fluxes(
        final_flux_absolute_distance_dict, absolute_y_lim_dict, absolute_distance_output_direct)
    heatmap_and_box3d_plotting_by_fluxes(
        final_flux_relative_distance_dict, relative_y_lim_dict, relative_distance_output_direct, percentage=True)
    if reduced_metric == Keywords.mean:
        euclidean_distance_output_direct = '{}/{}'.format(current_metric_output_direct, Keywords.euclidean_distance)
        check_and_mkdir_of_direct(euclidean_distance_output_direct)
        multi_row_col_scatter_plot_for_result_selection(
            final_raw_euclidian_distance_dict, x_label_index_dict, y_label_index_dict, 'raw_euclidian_distance',
            output_direct=euclidean_distance_output_direct, cutoff_value=0, figsize=None,
            ylim=(0, maximal_raw_euclidian_distance * 1.1))
        multi_row_col_scatter_plot_for_result_selection(
            final_net_euclidian_distance_dict, x_label_index_dict, y_label_index_dict, 'net_euclidian_distance',
            output_direct=euclidean_distance_output_direct, cutoff_value=0, figsize=None,
            ylim=(0, maximal_net_euclidian_distance * 1.1))
        # heatmap_and_box3d_plotting(
        #     final_net_euclidian_distance_dict, None, current_metric_output_direct, 'net_euclidian_distance')
        heatmap_and_box3d_plotting_euclidean(final_net_euclidian_distance_dict, euclidean_distance_output_direct)

    print('Saving result files...')
    output_analyzed_raw_flux_and_predicted_mid_data()
    figure_raw_data = FigureData(FigureDataKeywords.raw_model_distance, result_name)
    figure_raw_data.save_data(
        common_flux_name_list=list(common_flux_name_dict.keys()),
        final_flux_absolute_distance_dict=final_flux_absolute_distance_dict,
        final_flux_relative_distance_dict=final_flux_relative_distance_dict,
        absolute_y_lim_dict=absolute_y_lim_dict,
        relative_y_lim_dict=relative_y_lim_dict,
        final_net_euclidian_distance_dict=final_net_euclidian_distance_dict,
        maximal_net_euclidian_distance=maximal_net_euclidian_distance,
        raw_loss_value_dict=raw_selected_loss_value_dict,
        max_loss_value=max_loss_value,
        x_label_index_dict=x_label_index_dict, y_label_index_dict=y_label_index_dict,
        analyzed_set_size_list=analyzed_set_size_list, selected_min_loss_size_list=selected_min_loss_size_list,
    )


def normal_flux_euclidean_distance_plotting(
        final_solution_data_dict, final_flux_name_index_dict,
        simulated_flux_value_dict, net_flux_list, subset_index_dict=None):
    for result_label, raw_solution_array in final_solution_data_dict.items():
        flux_name_index_dict = final_flux_name_index_dict[result_label]
        if subset_index_dict is not None:
            target_solution_array = raw_solution_array[subset_index_dict[result_label], :]
        else:
            target_solution_array = raw_solution_array
        net_flux_matrix = net_flux_matrix_generator(net_flux_list, flux_name_index_dict, simulated_flux_value_dict)
        raw_euclidean_distance, new_euclidean_distance = euclidean_distance_of_mean_point_to_simulated_array(
            target_solution_array, simulated_flux_value_dict, flux_name_index_dict, net_flux_matrix)


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
    # net_flux_pair_dict = {}
    # for flux_name0, flux_name1 in net_flux_list:
    #     net_flux_pair_dict[flux_name0] = (flux_name0, flux_name1)
    #     net_flux_pair_dict[flux_name1] = (flux_name0, flux_name1)
    net_flux_pair_dict = net_flux_pair_dict_constructor(net_flux_list)
    result_label_list = list(final_solution_data_dict.keys())
    common_flux_name_list = []
    analyzed_flux_set = set()
    flux_id_display_flux_name_dict = {}
    for flux_name in simulated_flux_value_dict.keys():
        if flux_name in analyzed_flux_set:
            continue
        # if flux_name in net_flux_pair_dict:
        #     modified_flux_name = net_flux_pair_dict[flux_name]
        #     for one_directional_flux_name in modified_flux_name:
        #         analyzed_flux_set.add(one_directional_flux_name)
        # else:
        #     modified_flux_name = flux_name
        #     analyzed_flux_set.add(flux_name)
        modified_flux_name = net_flux_pair_analyzer(flux_name, net_flux_pair_dict, analyzed_flux_set)
        simulated_flux_value, flux_title, reverse_order, common_flux_name = determine_order_by_simulated_data(
            modified_flux_name, simulated_flux_value_dict)
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

