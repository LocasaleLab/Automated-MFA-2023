from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.figure_data_format import FigureData
from common_and_plotting_functions.config import FigureDataKeywords

from .third_party_packages import np
from .plotting_functions import group_violin_box_distribution_plot, group_bar_plot
from .config import Keywords

from scripts.src.core.solver.solver_construction_functions.solver_constructor import common_solver_constructor


def time_distribution_plotting(
        experiment_name, time_data_dict, output_direct=None):
    group_violin_box_distribution_plot(
        {'time_distribution': time_data_dict}, nested_color_dict=None,
        nested_median_color_dict=None, cutoff_dict=None, title_dict=None,
        output_direct=output_direct, ylim=None, xaxis_rotate=True,
        figsize=None, figure_type='box')
    if output_direct is not None:
        figure_raw_data = FigureData(FigureDataKeywords.time_data_distribution, experiment_name)
        figure_raw_data.save_data(
            time_data_dict=time_data_dict)


def loss_data_distribution_plotting(
        experiment_name, loss_data_dict, output_direct=None, loss_percentile=None, select_num=None):
    if output_direct is not None:
        group_violin_box_distribution_plot(
            {'loss_distribution': loss_data_dict}, nested_color_dict=None,
            nested_median_color_dict=None, cutoff_dict=None, title_dict=None,
            output_direct=output_direct, ylim=None, xaxis_rotate=True,
            figsize=None, figure_type='box')
    if loss_percentile is not None or select_num is not None:
        if loss_percentile is not None and select_num is not None:
            raise ValueError()
        subset_index_dict = {}
        filtered_loss_data_dict = {}
        for result_label, loss_array in loss_data_dict.items():
            index_array = np.argsort(loss_array)
            total_num = loss_array.shape[0]
            target_num = total_num
            if loss_percentile is not None:
                target_num = int(loss_percentile * total_num + 0.9999)
            elif select_num is not None:
                target_num = select_num
            filtered_index = index_array[:target_num]
            subset_index_dict[result_label] = filtered_index
            filtered_loss_data_dict[result_label] = loss_array[filtered_index]
        if output_direct is not None:
            group_violin_box_distribution_plot(
                {'filtered_loss_distribution': filtered_loss_data_dict}, nested_color_dict=None,
                nested_median_color_dict=None, cutoff_dict=None, title_dict=None,
                output_direct=output_direct, ylim=None, xaxis_rotate=True,
                figsize=None, figure_type='box')
    else:
        subset_index_dict = None
        filtered_loss_data_dict = loss_data_dict
    if output_direct is not None:
        figure_raw_data = FigureData(FigureDataKeywords.loss_data_comparison, experiment_name)
        figure_raw_data.save_data(
            loss_data_dict=loss_data_dict,
            filtered_loss_data_dict=filtered_loss_data_dict)
    return subset_index_dict


def experimental_mid_prediction(
        experiment_name, complex_predicted_data_dict, final_target_experimental_mid_data_dict,
        mid_prediction_output_direct, subset_index_dict=None, mid_tissue_raw_name_dict=None):
    final_group_mid_dict = {}
    final_stderr_dict = {}
    final_complete_data_dict = {}
    for data_label, raw_final_predicted_data_dict in complex_predicted_data_dict.items():
        for result_label, result_specific_predicted_data_dict in raw_final_predicted_data_dict.items():
            if result_label not in final_group_mid_dict:
                final_group_mid_dict[result_label] = {}
                final_stderr_dict[result_label] = {}
            for mid_title, current_predicted_data_array_list in result_specific_predicted_data_dict.items():
                if mid_tissue_raw_name_dict is not None:
                    tissue_name, raw_metabolite_name = mid_tissue_raw_name_dict[mid_title]
                    if raw_metabolite_name not in final_group_mid_dict[result_label]:
                        final_group_mid_dict[result_label][raw_metabolite_name] = {}
                        final_stderr_dict[result_label][raw_metabolite_name] = {}
                    if tissue_name not in final_group_mid_dict[result_label][raw_metabolite_name]:
                        final_group_mid_dict[result_label][raw_metabolite_name][tissue_name] = {}
                        final_stderr_dict[result_label][raw_metabolite_name][tissue_name] = {}
                    current_average_mid_dict = final_group_mid_dict[result_label][raw_metabolite_name][tissue_name]
                    current_stderr_mid_dict = final_stderr_dict[result_label][raw_metabolite_name][tissue_name]
                else:
                    if mid_title not in final_group_mid_dict[result_label]:
                        final_group_mid_dict[result_label][mid_title] = {}
                        final_stderr_dict[result_label][mid_title] = {}
                    current_average_mid_dict = final_group_mid_dict[result_label][mid_title]
                    current_stderr_mid_dict = final_stderr_dict[result_label][mid_title]
                current_predicted_data_array = np.array(current_predicted_data_array_list)
                if subset_index_dict is not None:
                    target_predicted_data_array = current_predicted_data_array[subset_index_dict[result_label], :]
                else:
                    target_predicted_data_array = current_predicted_data_array
                current_average_mid_dict[data_label] = target_predicted_data_array.mean(axis=0)
                current_stderr_mid_dict[data_label] = target_predicted_data_array.std(axis=0)
    for data_label, raw_final_predicted_data_dict in complex_predicted_data_dict.items():
        for result_label, result_specific_predicted_data_dict in raw_final_predicted_data_dict.items():
            for mid_title in result_specific_predicted_data_dict.keys():
                if mid_tissue_raw_name_dict is not None:
                    tissue_name, raw_metabolite_name = mid_tissue_raw_name_dict[mid_title]
                    current_average_mid_dict = final_group_mid_dict[result_label][raw_metabolite_name][tissue_name]
                else:
                    current_average_mid_dict = final_group_mid_dict[result_label][mid_title]
                if Keywords.experimental not in current_average_mid_dict:
                    current_average_mid_dict[Keywords.experimental] = final_target_experimental_mid_data_dict[
                        result_label][mid_title]
    for result_label, result_specific_plotting_data_dict in final_group_mid_dict.items():
        current_error_bar_data_dict = final_stderr_dict[result_label]
        current_result_mid_prediction_output_direct = '{}/{}'.format(mid_prediction_output_direct, result_label)
        check_and_mkdir_of_direct(current_result_mid_prediction_output_direct)
        if mid_tissue_raw_name_dict is not None:
            for tissue_name, each_tissue_average_data_dict in result_specific_plotting_data_dict.items():
                each_tissue_error_bar_data_dict = current_error_bar_data_dict[tissue_name]
                if result_label not in final_complete_data_dict:
                    final_complete_data_dict[result_label] = {}
                final_complete_data_dict[result_label][tissue_name] = (
                    each_tissue_average_data_dict, each_tissue_error_bar_data_dict)
                current_tissue_mid_prediction_output_direct = '{}/{}'.format(
                    current_result_mid_prediction_output_direct, tissue_name)
                check_and_mkdir_of_direct(current_tissue_mid_prediction_output_direct)
                group_bar_plot(
                    each_tissue_average_data_dict, error_bar_data_dict=each_tissue_error_bar_data_dict,
                    output_direct=current_tissue_mid_prediction_output_direct, ylim=(0, 1))
        else:
            final_complete_data_dict[result_label] = (result_specific_plotting_data_dict, current_error_bar_data_dict)
            group_bar_plot(
                result_specific_plotting_data_dict, error_bar_data_dict=current_error_bar_data_dict,
                output_direct=current_result_mid_prediction_output_direct, ylim=(0, 1))
    figure_raw_data = FigureData(FigureDataKeywords.mid_comparison, experiment_name)
    figure_raw_data.save_data(final_complete_data_dict=final_complete_data_dict)


def reconstruct_and_filter_data_dict(
        final_solution_data_dict, final_flux_name_index_dict, final_mapping_dict, subset_index_dict=None):
    def decouple_result_label_tuple(label_tuple, data_dict, data_array):
        current_label = label_tuple[0]
        if len(label_tuple) == 1:
            data_dict[current_label] = data_array
        else:
            if current_label not in data_dict:
                data_dict[current_label] = {}
            decouple_result_label_tuple(label_tuple[1:], data_dict[current_label], data_array)

    reconstructed_solution_data_dict = {}
    reconstructed_flux_name_index_dict = {}
    common_flux_name_index_dict = None
    for raw_result_label, raw_solution_data_array in final_solution_data_dict.items():
        if subset_index_dict is not None:
            subset_index = subset_index_dict[raw_result_label]
            solution_data_array = raw_solution_data_array[subset_index]
        else:
            solution_data_array = raw_solution_data_array
        # if common_flux_name_index_dict is None:
        #     common_flux_name_index_dict = final_flux_name_index_dict[raw_result_label]
        current_flux_name_index_dict = final_flux_name_index_dict[raw_result_label]
        complete_result_label_tuple = final_mapping_dict[raw_result_label]
        decouple_result_label_tuple(complete_result_label_tuple, reconstructed_solution_data_dict, solution_data_array)
        decouple_result_label_tuple(
            complete_result_label_tuple, reconstructed_flux_name_index_dict, current_flux_name_index_dict)
    return reconstructed_solution_data_dict, reconstructed_flux_name_index_dict


def common_flux_comparison_func(
        current_important_flux_list, common_flux_name_index_dict, current_data_array, data_dict_for_plotting, key_name):
    for flux_name in current_important_flux_list:
        if isinstance(flux_name, str):
            flux_title = flux_name
            flux_index = common_flux_name_index_dict[flux_name]
            calculated_flux_array = current_data_array[:, flux_index]
        elif isinstance(flux_name, tuple) or isinstance(flux_name, list):
            if callable(flux_name[1]):
                flux_title, flux_func = flux_name
                flux_name_value_dict = {
                    tmp_flux_name: current_data_array[:, flux_index]
                    for tmp_flux_name, flux_index in common_flux_name_index_dict.items()}
                calculated_flux_array = flux_func(flux_name_value_dict)
            else:
                flux_title = '{} - {}'.format(flux_name[0], flux_name[1])
                flux_index1 = common_flux_name_index_dict[flux_name[0]]
                flux_index2 = common_flux_name_index_dict[flux_name[1]]
                calculated_flux_array = (
                        current_data_array[:, flux_index1] - current_data_array[:, flux_index2])
        else:
            raise ValueError()
        if flux_title not in data_dict_for_plotting:
            data_dict_for_plotting[flux_title] = {}
        data_dict_for_plotting[flux_title][key_name] = calculated_flux_array


def result_verification(solver_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_mid_data_dict):
    for result_label, solver_obj in solver_dict.items():
        solution_array = final_solution_data_dict[result_label]
        loss_data_array = final_loss_data_dict[result_label]
        predicted_mid_data_dict = final_predicted_mid_data_dict[result_label]
        total_solution_num = solution_array.shape[0]
        calculated_predicted_mid_list = []
        for solution_index in range(total_solution_num):
            current_solution = solution_array[solution_index, :]
            current_loss = loss_data_array[solution_index]
            current_predicted_mid_data_dict = {
                key: value[solution_index] for key, value in predicted_mid_data_dict.items()}
            calculated_loss = solver_obj.obj_eval(current_solution)
            calculated_mid_data_dict = solver_obj.predict(current_solution)
            calculated_predicted_mid_list.append(calculated_mid_data_dict)
            pass

