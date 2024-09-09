from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from common_and_plotting_functions.config import FigureDataKeywords

from .third_party_packages import np
from .plotting_functions import group_violin_box_distribution_plot, group_bar_plot, multi_row_col_bar_plot
from .config import Keywords, Color, random_seed, FigureData
from .functions import mid_name_process, add_empty_obj


def experimental_data_plotting_func_template(
        target_emu_name_nested_list, major_minor_key_analysis_func,
        major_key_file_name_func=lambda major_key: f'target_metabolites_{major_key}_labeling'):
    def sort_dict_and_remove_sorting_index(raw_dict):
        ordered_list = list(raw_dict.items())
        ordered_list.sort(key=lambda x: x[1][0])
        new_dict = {}
        for key, (value_index, value) in ordered_list:
            new_dict[key] = value
        return new_dict

    def convert_tmp_data_to_final_data_dict(tmp_data_dict):
        final_data_dict = {}
        for major_key, each_major_key_tmp_data_dict in tmp_data_dict.items():
            final_data_dict[major_key] = {}
            for metabolite_name, each_metabolite_data_dict in each_major_key_tmp_data_dict.items():
                final_data_dict[major_key][metabolite_name] = sort_dict_and_remove_sorting_index(
                    each_metabolite_data_dict)
        return final_data_dict

    def experimental_data_plotting(
            complete_experimental_mid_data_obj_dict, complete_result_information_dict, output_direct):
        tmp_mid_data_dict = {}
        tmp_raw_data_dict = {}
        color_dict = {}
        for result_label, experimental_mid_data_obj_dict in complete_experimental_mid_data_obj_dict.items():
            result_information_dict = complete_result_information_dict[result_label]
            major_key, minor_key_list, minor_key_str, current_color, order_index = major_minor_key_analysis_func(
                result_information_dict)
            if minor_key_list[-1] == Keywords.average:
                continue
            for metabolite_name, mid_data_obj in experimental_mid_data_obj_dict.items():
                current_tmp_mid_data_dict = add_empty_obj(tmp_mid_data_dict, dict, major_key, metabolite_name)
                current_tmp_raw_data_dict = add_empty_obj(tmp_raw_data_dict, dict, major_key, metabolite_name)
                current_tmp_mid_data_dict[minor_key_str] = (order_index, mid_data_obj.data_vector)
                current_tmp_raw_data_dict[minor_key_str] = (order_index, mid_data_obj.raw_data_vector)
                if minor_key_str not in color_dict:
                    color_dict[minor_key_str] = current_color
        mid_data_dict_for_plotting = convert_tmp_data_to_final_data_dict(tmp_mid_data_dict)
        raw_data_dict_for_plotting = convert_tmp_data_to_final_data_dict(tmp_raw_data_dict)

        target_row_num = len(target_emu_name_nested_list)
        target_col_num = len(target_emu_name_nested_list[0])
        for major_key, each_labeling_mid_data_dict_for_plotting in mid_data_dict_for_plotting.items():
            each_labeling_raw_data_dict_for_plotting = raw_data_dict_for_plotting[major_key]
            for raw_data in (False, True):
                if raw_data:
                    parent_direct = 'raw_data'
                    complete_data_dict = each_labeling_raw_data_dict_for_plotting
                    ylim = (0, None)
                else:
                    parent_direct = 'mid_data'
                    complete_data_dict = each_labeling_mid_data_dict_for_plotting
                    ylim = (0, 1)
                current_title = major_key_file_name_func(major_key)
                current_cell_line_output_direct = '{}/{}'.format(output_direct, parent_direct)
                check_and_mkdir_of_direct(current_cell_line_output_direct)
                multi_row_col_bar_plot(
                    complete_data_dict, target_emu_name_nested_list, target_row_num, target_col_num,
                    error_bar_data_dict=None, color_dict=color_dict, title_dict=None,
                    output_direct=current_cell_line_output_direct, current_title=current_title, ylim=ylim,
                    xlabel_list=None, figsize=None, legend=False)

    return experimental_data_plotting


def select_solutions(loss_array, loss_percentile=None, select_num=None, index_start=0):
    index_array = np.argsort(loss_array)
    total_num = loss_array.shape[0]
    target_num = total_num
    if loss_percentile is not None:
        target_num = int(loss_percentile * total_num + 0.9999)
    elif select_num is not None:
        target_num = select_num
    filtered_index = index_array[:target_num]
    return filtered_index + index_start


def time_distribution_plotting(
        experiment_name, time_data_dict, output_direct=None, subset_index_dict=None, parallel_num=None):
    filtered_time_data_dict = {}
    if parallel_num is not None:
        for result_label, time_data_array in time_data_dict.items():
            time_data_dict[result_label] = time_data_array / parallel_num
    if output_direct is not None:
        group_violin_box_distribution_plot(
            {'time_distribution': time_data_dict}, nested_color_dict=None,
            nested_median_color_dict=None, cutoff_dict=None, title_dict=None,
            output_direct=output_direct, ylim=None, xaxis_rotate=True,
            figsize=None, figure_type='box')
        if subset_index_dict is not None:
            for result_label, time_array in time_data_dict.items():
                filtered_index = subset_index_dict[result_label]
                filtered_time_data_dict[result_label] = time_array[filtered_index]
            group_violin_box_distribution_plot(
                {'filtered_time_distribution': filtered_time_data_dict}, nested_color_dict=None,
                nested_median_color_dict=None, cutoff_dict=None, title_dict=None,
                output_direct=output_direct, ylim=None, xaxis_rotate=True,
                figsize=None, figure_type='box')
    if output_direct is not None:
        figure_raw_data = FigureData(FigureDataKeywords.time_data_distribution, experiment_name)
        figure_raw_data.save_data(
            time_data_dict=time_data_dict, filtered_time_data_dict=filtered_time_data_dict)


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
            filtered_index = select_solutions(loss_array, loss_percentile, select_num)
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


def mid_name_list_generator_for_multiple_labeling_substrate(raw_metabolite_list, labeling_substrate_name_list):
    final_metabolite_list = []
    for labeling_substrate_name in labeling_substrate_name_list:
        for raw_metabolite_row in raw_metabolite_list:
            combined_metabolite_row = []
            for raw_metabolite_name in raw_metabolite_row:
                if raw_metabolite_name is None:
                    combined_metabolite_name = None
                else:
                    combined_metabolite_name = f'{labeling_substrate_name}_{raw_metabolite_name}'
                combined_metabolite_row.append(combined_metabolite_name)
            final_metabolite_list.append(combined_metabolite_row)
    return final_metabolite_list


def experimental_mid_prediction(
        experiment_name, complex_predicted_data_dict, final_target_experimental_mid_data_dict,
        mid_prediction_output_direct, subset_index_dict=None, mid_tissue_raw_name_dict=None, direct_plotting=False):
    final_group_mid_all_data_point_dict = {}
    final_group_mid_dict = {}
    final_stderr_dict = {}
    for data_label, raw_final_predicted_data_dict in complex_predicted_data_dict.items():
        for result_label, result_specific_predicted_data_dict in raw_final_predicted_data_dict.items():
            if result_label not in final_group_mid_all_data_point_dict:
                final_group_mid_dict[result_label] = {}
                final_stderr_dict[result_label] = {}
                final_group_mid_all_data_point_dict[result_label] = {}
            for mid_title, current_predicted_data_array_list in result_specific_predicted_data_dict.items():
                if mid_tissue_raw_name_dict is not None:
                    tissue_name, raw_metabolite_name = mid_tissue_raw_name_dict[mid_title]
                    if raw_metabolite_name not in final_group_mid_all_data_point_dict[result_label]:
                        final_group_mid_dict[result_label][raw_metabolite_name] = {}
                        final_stderr_dict[result_label][raw_metabolite_name] = {}
                        final_group_mid_all_data_point_dict[result_label][raw_metabolite_name] = {}
                    if tissue_name not in final_group_mid_all_data_point_dict[result_label][raw_metabolite_name]:
                        final_group_mid_dict[result_label][raw_metabolite_name][tissue_name] = {}
                        final_stderr_dict[result_label][raw_metabolite_name][tissue_name] = {}
                        final_group_mid_all_data_point_dict[result_label][raw_metabolite_name][tissue_name] = {}
                    current_average_mid_dict = final_group_mid_dict[result_label][raw_metabolite_name][tissue_name]
                    current_stderr_mid_dict = final_stderr_dict[result_label][raw_metabolite_name][tissue_name]
                    current_mid_data_point_dict = final_group_mid_all_data_point_dict[
                        result_label][raw_metabolite_name][tissue_name]
                else:
                    if mid_title not in final_group_mid_all_data_point_dict[result_label]:
                        final_group_mid_dict[result_label][mid_title] = {}
                        final_stderr_dict[result_label][mid_title] = {}
                        final_group_mid_all_data_point_dict[result_label][mid_title] = {}
                    current_average_mid_dict = final_group_mid_dict[result_label][mid_title]
                    current_stderr_mid_dict = final_stderr_dict[result_label][mid_title]
                    current_mid_data_point_dict = final_group_mid_all_data_point_dict[result_label][mid_title]
                current_predicted_data_array = np.array(current_predicted_data_array_list)
                if subset_index_dict is not None:
                    target_predicted_data_array = current_predicted_data_array[subset_index_dict[result_label], :]
                else:
                    target_predicted_data_array = current_predicted_data_array
                current_average_mid_dict[data_label] = target_predicted_data_array.mean(axis=0)
                current_stderr_mid_dict[data_label] = target_predicted_data_array.std(axis=0)
                current_mid_data_point_dict[data_label] = target_predicted_data_array
    for data_label, raw_final_predicted_data_dict in complex_predicted_data_dict.items():
        for result_label, result_specific_predicted_data_dict in raw_final_predicted_data_dict.items():
            for mid_title in result_specific_predicted_data_dict.keys():
                if mid_tissue_raw_name_dict is not None:
                    tissue_name, raw_metabolite_name = mid_tissue_raw_name_dict[mid_title]
                    # current_average_mid_dict = final_group_mid_dict[result_label][raw_metabolite_name][tissue_name]
                    current_mid_data_point_dict = final_group_mid_all_data_point_dict[result_label][raw_metabolite_name][tissue_name]
                else:
                    # current_average_mid_dict = final_group_mid_dict[result_label][mid_title]
                    current_mid_data_point_dict = final_group_mid_all_data_point_dict[result_label][mid_title]
                if Keywords.experimental not in current_mid_data_point_dict:
                    current_mid_data_point_dict[Keywords.experimental] = final_target_experimental_mid_data_dict[
                        result_label][mid_title].reshape([1, -1])
    for result_label, result_specific_plotting_data_dict in final_group_mid_all_data_point_dict.items():
        current_average_mid_dict = final_group_mid_dict[result_label]
        current_error_bar_data_dict = final_stderr_dict[result_label]
        current_result_mid_prediction_output_direct = '{}/{}'.format(mid_prediction_output_direct, result_label)
        check_and_mkdir_of_direct(current_result_mid_prediction_output_direct)
        if mid_tissue_raw_name_dict is not None:
            for tissue_name, each_tissue_all_data_point_dict in result_specific_plotting_data_dict.items():
                each_tissue_error_bar_data_dict = current_error_bar_data_dict[tissue_name]
                each_tissue_average_data_dict = current_average_mid_dict[tissue_name]
                # if result_label not in final_complete_data_dict:
                #     final_complete_data_dict[result_label] = {}
                # final_complete_data_dict[result_label][tissue_name] = (
                #     each_tissue_average_data_dict, each_tissue_error_bar_data_dict)
                current_tissue_mid_prediction_output_direct = '{}/{}'.format(
                    current_result_mid_prediction_output_direct, tissue_name)
                check_and_mkdir_of_direct(current_tissue_mid_prediction_output_direct)
                if direct_plotting:
                    group_bar_plot(
                        each_tissue_average_data_dict, error_bar_data_dict=each_tissue_error_bar_data_dict,
                        output_direct=current_tissue_mid_prediction_output_direct, ylim=(0, 1))
        else:
            # final_complete_data_dict[result_label] = (result_specific_plotting_data_dict, current_error_bar_data_dict)
            if direct_plotting:
                group_bar_plot(
                    result_specific_plotting_data_dict, error_bar_data_dict=current_error_bar_data_dict,
                    output_direct=current_result_mid_prediction_output_direct, ylim=(0, 1))
    figure_raw_data = FigureData(FigureDataKeywords.mid_comparison, experiment_name)
    figure_raw_data.save_data(final_complete_data_dict=final_group_mid_all_data_point_dict)


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
        current_important_flux_list, common_flux_name_index_dict, current_data_array, data_dict_for_plotting, key_name,
        reversible_flux_title_constructor=None):
    def default_reversible_flux_title_constructor(flux_name_0, flux_name_1):
        return f'{flux_name_0} - {flux_name_1}'

    if reversible_flux_title_constructor is None:
        reversible_flux_title_constructor = default_reversible_flux_title_constructor
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
                # flux_title = '{} - {}'.format(flux_name[0], flux_name[1])
                flux_title = reversible_flux_title_constructor(*flux_name)
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


def multiple_repeat_result_processing(
        solver_dict, final_solution_data_dict, final_loss_data_dict, final_predicted_mid_data_dict,
        repeat_division_num=1, each_optimization_num=None, loss_percentile=None, select_num=None):
    def index_start_end_generator(total_num, batch_num, optimization_num, start_index=0):
        if optimization_num is not None:
            base_num = optimization_num
            if batch_num is None:
                batch_num = total_num // base_num
        else:
            base_num = total_num // batch_num
        remainder = total_num % base_num
        size_list = [base_num] * batch_num
        current_start_index = start_index
        for current_size in size_list:
            current_end_index = current_start_index + current_size
            yield current_start_index, current_end_index
            current_start_index = current_end_index

    new_loss_data_dict = {}
    new_final_solution_data_dict = {}
    new_final_predicted_mid_data_dict = {}

    for result_label, loss_array in final_loss_data_dict.items():
        if isinstance(repeat_division_num, dict):
            this_result_repeat_division = repeat_division_num[result_label]
        elif isinstance(repeat_division_num, int):
            this_result_repeat_division = repeat_division_num
        elif repeat_division_num is None:
            this_result_repeat_division = None
        else:
            raise TypeError
        if isinstance(each_optimization_num, dict):
            this_result_optimization_num = each_optimization_num[result_label]
        elif isinstance(each_optimization_num, int):
            this_result_optimization_num = each_optimization_num
        elif each_optimization_num is None:
            this_result_optimization_num = None
        else:
            raise TypeError
        solver_obj = solver_dict[result_label]
        solution_array = final_solution_data_dict[result_label]
        predicted_mid_data_dict = final_predicted_mid_data_dict[result_label]
        new_loss_list = []
        new_solution_list = []
        new_mid_data_dict = {}
        total_solution_num = len(loss_array)
        for index_start, index_end in index_start_end_generator(
                total_solution_num, this_result_repeat_division, this_result_optimization_num):
            this_repeat_loss_array = loss_array[index_start:index_end]
            filtered_index = select_solutions(this_repeat_loss_array, loss_percentile, select_num, index_start)
            mean_solution_array = np.mean(solution_array[filtered_index, :], 0)
            calculated_loss = solver_obj.obj_eval(mean_solution_array)
            calculated_mid_data_dict = solver_obj.predict(mean_solution_array)
            new_solution_list.append(mean_solution_array)
            new_loss_list.append(calculated_loss)
            for mid_title, predicted_mid_array in calculated_mid_data_dict.items():
                processed_mid_title = mid_name_process(mid_title)
                if processed_mid_title not in new_mid_data_dict:
                    new_mid_data_dict[processed_mid_title] = []
                new_mid_data_dict[processed_mid_title].append(predicted_mid_array)
        new_loss_data_dict[result_label] = np.array(new_loss_list)
        new_final_solution_data_dict[result_label] = np.array(new_solution_list)
        new_final_predicted_mid_data_dict[result_label] = new_mid_data_dict

    return new_final_solution_data_dict, new_loss_data_dict, new_final_predicted_mid_data_dict


def traditional_method_result_selection(
        final_solution_data_dict, final_loss_data_dict, final_predicted_mid_data_dict, each_case_result_num,
        repeat_time_each_analyzed_set=1, select_num=1):
    new_loss_data_dict = {}
    new_final_solution_data_dict = {}
    new_final_predicted_mid_data_dict = {}
    total_selected_num_in_all_repeat = each_case_result_num * repeat_time_each_analyzed_set
    for result_label, loss_array in final_loss_data_dict.items():
        total_solution_num = len(loss_array)
        solution_array = final_solution_data_dict[result_label]
        predicted_mid_data_dict = final_predicted_mid_data_dict[result_label]
        all_random_selected_index_array = random_seed.choice(total_solution_num, total_selected_num_in_all_repeat)
        filtered_index_list = []
        for repeat_index in range(repeat_time_each_analyzed_set):
            current_random_selected_index = all_random_selected_index_array[
                repeat_index * each_case_result_num:repeat_index * each_case_result_num + each_case_result_num]
            filtered_local_index = select_solutions(loss_array[current_random_selected_index], select_num=select_num)
            filtered_index_list.extend(current_random_selected_index[filtered_local_index])
        filtered_index = np.array(filtered_index_list)
        new_loss_data_dict[result_label] = loss_array[filtered_index]
        new_final_solution_data_dict[result_label] = solution_array[filtered_index, :]
        new_mid_data_dict = {}
        for mid_title, predicted_mid_array in predicted_mid_data_dict.items():
            processed_mid_title = mid_name_process(mid_title)
            new_mid_data_dict[processed_mid_title] = [predicted_mid_array[index_i] for index_i in filtered_index]
        new_final_predicted_mid_data_dict[result_label] = new_mid_data_dict
    return new_final_solution_data_dict, new_loss_data_dict, new_final_predicted_mid_data_dict
