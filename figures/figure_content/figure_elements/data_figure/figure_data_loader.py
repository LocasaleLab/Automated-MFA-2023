from common_and_plotting_functions.config import FigureDataKeywords

from .config import np, DataFigureParameterName as ParameterName, DataName, ModelDataSensitivityDataFigureConfig, \
    Direct, Keywords, BasicFigureData, heatmap_and_box3d_parameter_preparation


class RawModelAnalysisFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.raw_model_distance
    optimization_from_averaged_solutions_set = {
        DataName.optimization_from_solutions_raw_data,
        DataName.optimization_from_solutions_all_data,
        DataName.optimization_from_solutions_batched_raw_data,
        DataName.optimization_from_solutions_batched_all_data
    }
    optimization_from_batched_predefined_flux_set = {
        DataName.optimization_from_batched_raw_data,
        DataName.optimization_from_batched_all_data,
        DataName.optimization_from_solutions_batched_raw_data,
        DataName.optimization_from_solutions_batched_all_data
    }

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name, figure_class, flux_name=None, calculate_mean=True, optimized=False):
        target_items = None
        processed = False
        if data_name in self.processed_data_dict:
            if figure_class in self.processed_data_dict[data_name]:
                if figure_class == ParameterName.net_euclidean_distance or figure_class == ParameterName.loss_data:
                    processed = True
                    target_items = self.processed_data_dict[data_name][figure_class]
                elif flux_name in self.processed_data_dict[data_name][figure_class]:
                    processed = True
                    target_items = self.processed_data_dict[data_name][figure_class][flux_name]
            else:
                self.processed_data_dict[data_name][figure_class] = {}
        else:
            self.processed_data_dict[data_name] = {}
        if not processed:
            current_data_obj = self._return_figure_data(data_name)
            x_label_index_dict = current_data_obj.x_label_index_dict
            y_label_index_dict = current_data_obj.y_label_index_dict
            analyzed_set_size_list = current_data_obj.analyzed_set_size_list
            selected_min_loss_size_list = current_data_obj.selected_min_loss_size_list
            common_flux_name_list = current_data_obj.common_flux_name_list
            all_flux = False
            if figure_class == ParameterName.loss_data:
                max_loss_value = current_data_obj.max_loss_value
                raw_loss_value_dict = current_data_obj.raw_loss_value_dict
                if data_name in self.optimization_from_averaged_solutions_set:
                    loss_of_initial_raw_selected_solutions_dict = current_data_obj.loss_of_initial_raw_selected_solutions_dict
                    loss_of_initial_averaged_solutions_dict = current_data_obj.loss_of_initial_averaged_solutions_dict
                    data_tuple = (
                        loss_of_initial_raw_selected_solutions_dict,
                        loss_of_initial_averaged_solutions_dict, raw_loss_value_dict)
                else:
                    loss_of_mean_solution_dict = current_data_obj.loss_of_mean_solution_dict
                    data_tuple = (raw_loss_value_dict, loss_of_mean_solution_dict)
                target_items = (
                    data_tuple, max_loss_value, analyzed_set_size_list,
                    selected_min_loss_size_list)
            elif figure_class == ParameterName.raw_flux_diff_vector:
                raw_selected_diff_vector_dict = current_data_obj.raw_selected_diff_vector_dict
                flux_name_list = current_data_obj.common_flux_name_list
                if data_name in self.optimization_from_averaged_solutions_set:
                    if optimized:
                        diff_vector_between_averaged_and_reoptimized_dict = \
                            current_data_obj.diff_vector_between_averaged_and_reoptimized_dict
                        data_tuple = (diff_vector_between_averaged_and_reoptimized_dict, )
                    else:
                        initial_raw_selected_diff_vector_dict = current_data_obj.initial_raw_selected_diff_vector_dict
                        initial_averaged_diff_vector_dict = current_data_obj.initial_averaged_diff_vector_dict
                        data_tuple = (
                            initial_raw_selected_diff_vector_dict,
                            initial_averaged_diff_vector_dict, raw_selected_diff_vector_dict)
                else:
                    selected_averaged_diff_vector_dict = current_data_obj.selected_averaged_diff_vector_dict
                    data_tuple = (raw_selected_diff_vector_dict, selected_averaged_diff_vector_dict)
                target_items = (data_tuple, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list)
            elif figure_class == ParameterName.flux_relative_distance and flux_name == ParameterName.all_flux:
                all_selected_net_relative_error_dict = current_data_obj.net_all_selected_relative_error_dict
                flux_name_list = current_data_obj.common_flux_name_list
                if data_name in self.optimization_from_averaged_solutions_set:
                    initial_raw_selected_relative_error_dict = current_data_obj.net_relative_error_of_initial_raw_selected_dict
                    initial_averaged_relative_error_dict = current_data_obj.net_relative_error_of_initial_averaged_solutions_dict
                    data_tuple = (
                        initial_raw_selected_relative_error_dict,
                        initial_averaged_relative_error_dict, all_selected_net_relative_error_dict)
                else:
                    selected_averaged_net_relative_error_dict = current_data_obj.net_selected_averaged_relative_error_dict
                    data_tuple = (all_selected_net_relative_error_dict, selected_averaged_net_relative_error_dict)
                target_items = (data_tuple, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list)
            else:
                if figure_class == ParameterName.net_euclidean_distance:
                    # data_dict = current_data_obj.final_net_euclidian_distance_dict
                    maximal_euclidian_distance = current_data_obj.maximal_net_euclidian_distance
                    all_distance_data_dict = current_data_obj.final_net_all_select_euclidian_distance_dict
                    if data_name in self.optimization_from_averaged_solutions_set:
                        net_euclidian_distance_of_initial_raw_selected_dict = (
                            current_data_obj.net_euclidian_distance_of_initial_raw_selected_dict)
                        net_euclidian_distance_of_initial_averaged_solutions_dict = (
                            current_data_obj.net_euclidian_distance_of_initial_averaged_solutions_dict)
                        data_dict = (
                            net_euclidian_distance_of_initial_raw_selected_dict,
                            net_euclidian_distance_of_initial_averaged_solutions_dict, all_distance_data_dict)
                    else:
                        distance_of_mean_data_dict = current_data_obj.final_net_euclidian_distance_dict
                        data_dict = (all_distance_data_dict, distance_of_mean_data_dict)
                    if data_name in self.optimization_from_batched_predefined_flux_set:
                        net_distance_between_different_simulated_flux_dict = (
                            current_data_obj.net_distance_between_different_simulated_flux_dict)
                        data_dict = (net_distance_between_different_simulated_flux_dict, *data_dict)
                    scatter_y_lim_pair = (0, maximal_euclidian_distance * 1.1)
                    percentage = False
                    # maximal_euclidian_distance = current_data_obj.maximal_net_euclidian_distance * 1.1
                    # target_items = (
                    #     (raw_distance_data_dict, distance_of_mean_data_dict), maximal_euclidian_distance,
                    #     analyzed_set_size_list, selected_min_loss_size_list)
                elif figure_class == ParameterName.raw_distance:
                    maximal_euclidian_distance = current_data_obj.maximal_raw_euclidian_distance
                    all_distance_data_dict = current_data_obj.final_raw_all_select_euclidian_distance_dict
                    if data_name in self.optimization_from_averaged_solutions_set:
                        euclidian_distance_of_initial_raw_selected_dict = (
                            current_data_obj.raw_euclidian_distance_of_initial_raw_selected_dict)
                        euclidian_distance_of_initial_averaged_solutions_dict = (
                            current_data_obj.raw_euclidian_distance_of_initial_averaged_solutions_dict)
                        data_dict = (
                            euclidian_distance_of_initial_raw_selected_dict,
                            euclidian_distance_of_initial_averaged_solutions_dict, all_distance_data_dict)
                    else:
                        distance_of_mean_data_dict = current_data_obj.final_raw_euclidian_distance_dict
                        data_dict = (all_distance_data_dict, distance_of_mean_data_dict)
                    if data_name in self.optimization_from_batched_predefined_flux_set:
                        distance_between_different_simulated_flux_dict = (
                            current_data_obj.raw_distance_between_different_simulated_flux_dict)
                        data_dict = (distance_between_different_simulated_flux_dict, *data_dict)
                    scatter_y_lim_pair = (0, maximal_euclidian_distance * 1.1)
                    percentage = False
                elif figure_class == ParameterName.flux_absolute_distance:
                    data_dict = current_data_obj.final_flux_absolute_distance_dict[flux_name]
                    y_lim = current_data_obj.absolute_y_lim_dict[flux_name]
                    scatter_y_lim_pair = (-y_lim, y_lim)
                    percentage = True
                elif figure_class == ParameterName.flux_relative_distance:
                    if flux_name == ParameterName.all_flux:
                        all_flux = True
                        data_dict = current_data_obj.final_flux_relative_distance_dict
                        scatter_y_lim_pair = (None, None)
                    else:
                        data_dict = current_data_obj.final_flux_relative_distance_dict[flux_name]
                        y_lim = current_data_obj.relative_y_lim_dict[flux_name]
                        scatter_y_lim_pair = (-y_lim, y_lim)
                    percentage = True
                else:
                    raise ValueError()
                if all_flux:
                    mean_matrix = []
                    std_matrix = []
                    for each_flux_name in common_flux_name_list:
                        each_mean_matrix, each_std_matrix, *_ = heatmap_and_box3d_parameter_preparation(
                            data_dict[each_flux_name])
                        mean_matrix.append(each_mean_matrix)
                        std_matrix.append(each_std_matrix)
                    heatmap_mean_lim_pair = None
                    std_value_text_format = mean_value_text_format = None
                elif calculate_mean:
                    if isinstance(data_dict, tuple):
                        mean_data_dict = data_dict[1]
                    else:
                        mean_data_dict = data_dict
                    (
                        mean_matrix, std_matrix, heatmap_mean_lim_pair,
                        mean_value_text_format) = heatmap_and_box3d_parameter_preparation(mean_data_dict, percentage)
                    # std_value_text_format = HeatmapValueFormat.scientific_format
                    std_value_text_format = mean_value_text_format
                else:
                    mean_matrix = std_matrix = None
                    heatmap_mean_lim_pair = (None, None)
                    mean_value_text_format = std_value_text_format = ''
                heatmap_std_lim_pair = (0, None)
                target_items = (mean_matrix, heatmap_mean_lim_pair, mean_value_text_format), \
                    (std_matrix, heatmap_std_lim_pair, std_value_text_format), \
                    analyzed_set_size_list, selected_min_loss_size_list, common_flux_name_list, \
                    data_dict, scatter_y_lim_pair, x_label_index_dict, y_label_index_dict
            self.processed_data_dict[data_name][figure_class] = target_items
        return target_items

    def return_loss_data(self, data_name, figure_class, **kwargs):
        (
            raw_loss_value_dict, max_loss_value, analyzed_set_size_list,
            selected_min_loss_size_list) = self._figure_data_preprocess(data_name, figure_class)
        return raw_loss_value_dict, max_loss_value, analyzed_set_size_list, \
            selected_min_loss_size_list

    def return_diff_vector_data(self, data_name, optimized=False, **kwargs):
        (
            data_dict, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list
        ) = self._figure_data_preprocess(
            data_name, figure_class=ParameterName.raw_flux_diff_vector, optimized=optimized)
        return data_dict, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list

    def return_heatmap_data(
            self, data_name, figure_class, flux_name=None, mean_or_std=ParameterName.mean, **kwargs):
        (
            mean_parameter_list, std_parameter_list, analyzed_set_size_list, selected_min_loss_size_list,
            *_) = self._figure_data_preprocess(data_name, figure_class, flux_name)
        if mean_or_std == ParameterName.mean:
            data_matrix, data_lim_pair, data_value_text_format = mean_parameter_list
        elif mean_or_std == ParameterName.std:
            data_matrix, data_lim_pair, data_value_text_format = std_parameter_list
        else:
            raise ValueError()
        return data_matrix, data_lim_pair, data_value_text_format, analyzed_set_size_list, selected_min_loss_size_list

    def return_scatter_data(self, data_name, figure_class, flux_name=None, **kwargs):
        (
            *_, data_dict, scatter_y_lim_pair,
            x_label_index_dict, y_label_index_dict) = self._figure_data_preprocess(
            data_name, figure_class, flux_name, calculate_mean=False)
        return data_dict, scatter_y_lim_pair, x_label_index_dict, y_label_index_dict

    def return_all_flux_data_old(self, data_name, **kwargs):
        (
            mean_parameter_list, std_parameter_list, analyzed_set_size_list, selected_min_loss_size_list,
            common_flux_name_list, *_) = self._figure_data_preprocess(
            data_name, figure_class=ParameterName.flux_relative_distance, flux_name=ParameterName.all_flux)
        mean_data_matrix_list, *_ = mean_parameter_list
        std_data_matrix_list, *_ = std_parameter_list
        return mean_data_matrix_list, std_data_matrix_list, common_flux_name_list, analyzed_set_size_list, \
            selected_min_loss_size_list

    def return_all_flux_data(self, data_name, **kwargs):
        (
            *_, data_dict, scatter_y_lim_pair,
            x_label_index_dict, y_label_index_dict) = self._figure_data_preprocess(
            data_name, figure_class=ParameterName.flux_relative_distance, flux_name=ParameterName.all_flux)
        return data_dict, scatter_y_lim_pair, x_label_index_dict, y_label_index_dict


raw_model_data = RawModelAnalysisFigureData()


class LossFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.loss_data_comparison

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def return_data(self, data_name, result_label_layout_list=None, **kwargs):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            loss_data_dict = current_data_obj.loss_data_dict
            filtered_loss_data_dict = current_data_obj.filtered_loss_data_dict
            if data_name == DataName.renal_carcinoma_invivo_infusion:
                loss_data_dict = self._process_kidney_carcinoma_comparison_data(loss_data_dict)
                filtered_loss_data_dict = self._process_kidney_carcinoma_comparison_data(filtered_loss_data_dict)
            elif data_name == DataName.colon_cancer_cell_line:
                loss_data_dict = self._process_colon_cancer_cell_line_comparison_data(loss_data_dict)
                filtered_loss_data_dict = self._process_colon_cancer_cell_line_comparison_data(filtered_loss_data_dict)
            self.processed_data_dict[data_name] = (loss_data_dict, filtered_loss_data_dict)
        else:
            loss_data_dict, filtered_loss_data_dict = self.processed_data_dict[data_name]
        if result_label_layout_list is not None:
            updated_loss_data_dict = {}
            updated_filtered_loss_data_dict = {}
            for row_index, row_data_label_list in enumerate(result_label_layout_list):
                for col_index, data_label_list in enumerate(row_data_label_list):
                    current_loss_data_dict = {data_label: loss_data_dict[data_label] for data_label in data_label_list}
                    current_filtered_loss_data_dict = {
                        data_label: filtered_loss_data_dict[data_label] for data_label in data_label_list}
                    updated_loss_data_dict[(row_index, col_index)] = current_loss_data_dict
                    updated_filtered_loss_data_dict[(row_index, col_index)] = current_filtered_loss_data_dict
            loss_data_dict = updated_loss_data_dict
            filtered_loss_data_dict = updated_filtered_loss_data_dict
        return loss_data_dict, filtered_loss_data_dict

    @staticmethod
    def _process_kidney_carcinoma_comparison_data(raw_data_dict):
        new_data_dict = {}
        for data_label, data_vector in raw_data_dict.items():
            group_name, patient_id_str = data_label.split('__')
            if group_name == Keywords.kidney or group_name == Keywords.carcinoma:
                patient_id = patient_id_str[0]
                if patient_id not in new_data_dict:
                    new_data_dict[patient_id] = {}
                new_data_dict[patient_id][group_name] = data_vector
        return new_data_dict

    @staticmethod
    def _process_colon_cancer_cell_line_comparison_data(raw_data_dict):
        new_data_dict = {}
        for data_label, data_vector in raw_data_dict.items():
            cell_line, condition_str = data_label.split('__')
            condition = condition_str[0]
            if cell_line not in new_data_dict:
                new_data_dict[cell_line] = {}
            new_data_dict[cell_line][condition] = data_vector
        return new_data_dict


loss_data = LossFigureData()


class TimeFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.time_data_distribution

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def return_data(self, data_name, **kwargs):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            time_data_dict = current_data_obj.time_data_dict
            self.processed_data_dict[data_name] = time_data_dict
        else:
            time_data_dict = self.processed_data_dict[data_name]
        return time_data_dict


time_data = TimeFigureData()


class MIDComparisonFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.mid_comparison

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name, result_label):
        if data_name not in self.processed_data_dict:
            self.processed_data_dict[data_name] = self._return_figure_data(data_name).final_complete_data_dict
        current_mean_data_dict, current_error_bar_data_dict = self.processed_data_dict[data_name][result_label]
        return current_mean_data_dict, current_error_bar_data_dict

    def return_data(self, data_name, result_label, **kwargs):
        return self._figure_data_preprocess(data_name, result_label)


mid_comparison_data = MIDComparisonFigureData()


class FluxComparisonFigureData(BasicFigureData):
    data_prefix = FigureDataKeywords.flux_comparison

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}
        self.renal_carcinoma_data_set = {
            DataName.renal_carcinoma_invivo_infusion,
            DataName.renal_carcinoma_invivo_infusion_traditional_method,
            DataName.renal_carcinoma_invivo_infusion_squared_loss
        }
        self.colon_cancer_data_set = {
            DataName.colon_cancer_cell_line,
            DataName.colon_cancer_cell_line_traditional_method,
            DataName.colon_cancer_cell_line_squared_loss
        }

    def _data_reader(self, data_name, comparison_name):
        data_obj = self._return_figure_data(data_name)
        return data_obj.final_dict_for_comparison[comparison_name], \
            data_obj.final_key_name_parameter_dict[comparison_name]

    def _common_data_loader(self, data_name, comparison_name='', mean=True):
        final_flux_data_dict = {}
        need_process = False
        scatter_line_figure = False
        if data_name in self.processed_data_dict:
            loaded_item = self.processed_data_dict[data_name]
            if comparison_name in loaded_item:
                final_flux_data_dict, scatter_line_figure = loaded_item[comparison_name]
            else:
                need_process = True
        else:
            self.processed_data_dict[data_name] = {}
            need_process = True
        if need_process:
            if data_name == DataName.multiple_tumor:
                final_flux_data_dict = self._multiple_tumor_flux_comparison_data_preprocess()
                scatter_line_figure = ParameterName.normal_scatter_figure
            elif (data_name == DataName.lung_tumor_invivo_infusion and comparison_name == 'human') or \
                    (data_name in self.renal_carcinoma_data_set and comparison_name == 'tumor_vs_kidney'):
                final_flux_data_dict = self._point_to_point_flux_comparison_data_preprocess(
                    data_name, comparison_name, mean, same_patient=True)
                scatter_line_figure = ParameterName.scatter_line_figure
            elif data_name in self.colon_cancer_data_set:
                final_flux_data_dict = self._point_to_point_flux_comparison_data_preprocess(
                    data_name, comparison_name, mean)
                scatter_line_figure = ParameterName.colon_cancer_scatter_line_figure
            else:
                final_flux_data_dict = self._normal_flux_comparison_data_preprocess(data_name, comparison_name)
                scatter_line_figure = ParameterName.normal_scatter_figure
            self.processed_data_dict[data_name][comparison_name] = final_flux_data_dict, scatter_line_figure
        return final_flux_data_dict, scatter_line_figure

    def _normal_flux_comparison_data_preprocess(self, data_name, comparison_name):
        flux_comparison_data_dict, key_name_parameter_dict = self._data_reader(data_name, comparison_name)
        final_flux_comparison_data_dict = {}
        for flux_title, each_flux_data_dict in flux_comparison_data_dict.items():
            if flux_title not in final_flux_comparison_data_dict:
                final_flux_comparison_data_dict[flux_title] = {}
            for key_name, each_key_flux_data_array in each_flux_data_dict.items():
                tissue_name, patient_key, index_num = key_name_parameter_dict[key_name]
                if tissue_name not in final_flux_comparison_data_dict[flux_title]:
                    final_flux_comparison_data_dict[flux_title][tissue_name] = []
                current_mean = each_key_flux_data_array.mean()
                final_flux_comparison_data_dict[flux_title][tissue_name].append(current_mean)
        return final_flux_comparison_data_dict

    def _point_to_point_flux_comparison_data_preprocess(self, data_name, comparison_name, mean=True, same_patient=False):
        flux_comparison_data_dict, key_name_parameter_dict = self._data_reader(data_name, comparison_name)
        final_flux_comparison_data_dict = {}
        for flux_title, each_flux_data_dict in flux_comparison_data_dict.items():
            if flux_title not in final_flux_comparison_data_dict:
                final_flux_comparison_data_dict[flux_title] = {}
            for key_name, each_key_flux_data_array in each_flux_data_dict.items():
                if same_patient:
                    tissue_name, patient_key, index_num = key_name_parameter_dict[key_name]
                    condition_name1 = patient_key
                    condition_name2 = tissue_name
                else:
                    cell_line_name, treatment_name, index_num = key_name_parameter_dict[key_name]
                    condition_name1 = cell_line_name
                    condition_name2 = treatment_name
                if condition_name1 not in final_flux_comparison_data_dict[flux_title]:
                    final_flux_comparison_data_dict[flux_title][condition_name1] = {}
                if condition_name2 not in final_flux_comparison_data_dict[flux_title][condition_name1]:
                    final_flux_comparison_data_dict[flux_title][condition_name1][condition_name2] = []
                if mean:
                    current_mean = each_key_flux_data_array.mean()
                    final_flux_comparison_data_dict[flux_title][condition_name1][condition_name2].append(current_mean)
                else:
                    final_flux_comparison_data_dict[flux_title][condition_name1][condition_name2].extend(
                        each_key_flux_data_array)
        return final_flux_comparison_data_dict

    def _multiple_tumor_flux_comparison_data_preprocess(self):
        lung_tumor_flux_comparison_data_dict, lung_tumor_key_name_parameter_dict = self._data_reader(
            DataName.lung_tumor_invivo_infusion, 'human')
        current_lung_tumor_name = 'tumor'
        target_lung_tumor_name = 'lung'
        current_kidney_tumor_name = 'carcinoma'
        target_kidney_tumor_name = 'kidney'
        current_brain_tumor_name = 'brain'
        target_name_order = [target_kidney_tumor_name, target_lung_tumor_name, current_brain_tumor_name]
        raw_flux_comparison_data_dict = {}
        for flux_title, each_flux_data_dict in lung_tumor_flux_comparison_data_dict.items():
            if flux_title not in raw_flux_comparison_data_dict:
                raw_flux_comparison_data_dict[flux_title] = {}
            for key_name, each_key_flux_data_array in each_flux_data_dict.items():
                tissue_name, patient_key, index_num = lung_tumor_key_name_parameter_dict[key_name]
                if tissue_name == current_lung_tumor_name:
                    if target_lung_tumor_name not in raw_flux_comparison_data_dict[flux_title]:
                        raw_flux_comparison_data_dict[flux_title][target_lung_tumor_name] = []
                    # raw_flux_comparison_data_dict[
                    #     flux_title][target_lung_tumor_name][(patient_key, index_num)] = each_key_flux_data_array
                    # current_mean = each_key_flux_data_array.mean()
                    # raw_flux_comparison_data_dict[flux_title][target_lung_tumor_name].append(current_mean)
                    raw_flux_comparison_data_dict[flux_title][target_lung_tumor_name].append(each_key_flux_data_array)
        renal_flux_comparison_data_dict, renal_key_name_parameter_dict = self._data_reader(
            DataName.renal_carcinoma_invivo_infusion, 'kidney_tumor_vs_brain')
        for flux_title, each_flux_data_dict in renal_flux_comparison_data_dict.items():
            if flux_title not in raw_flux_comparison_data_dict:
                raw_flux_comparison_data_dict[flux_title] = {}
            for key_name, each_key_flux_data_array in each_flux_data_dict.items():
                tissue_name, patient_key, index_num = renal_key_name_parameter_dict[key_name]
                if tissue_name == current_kidney_tumor_name:
                    target_tissue_name = target_kidney_tumor_name
                elif tissue_name == current_brain_tumor_name:
                    target_tissue_name = current_brain_tumor_name
                else:
                    target_tissue_name = None
                if target_tissue_name is not None:
                    if target_tissue_name not in raw_flux_comparison_data_dict[flux_title]:
                        raw_flux_comparison_data_dict[flux_title][target_tissue_name] = []
                    # raw_flux_comparison_data_dict[
                    #     flux_title][current_brain_tumor_name][(patient_key, index_num)] = each_key_flux_data_array
                    # current_mean = each_key_flux_data_array.mean()
                    # raw_flux_comparison_data_dict[flux_title][target_tissue_name].append(current_mean)
                    raw_flux_comparison_data_dict[flux_title][target_tissue_name].append(each_key_flux_data_array)
        final_flux_comparison_data_dict = {}
        for flux_title, each_flux_data_dict in raw_flux_comparison_data_dict.items():
            final_flux_comparison_data_dict[flux_title] = {}
            for target_tissue_name in target_name_order:
                current_flux_dict = final_flux_comparison_data_dict[flux_title]
                for index, data_array in enumerate(raw_flux_comparison_data_dict[flux_title][target_tissue_name]):
                    if index not in current_flux_dict:
                        current_flux_dict[index] = {}
                    current_flux_dict[index][target_tissue_name] = data_array
                    # final_flux_comparison_data_dict[flux_title][target_tissue_name] = \
                    #     raw_flux_comparison_data_dict[flux_title][target_tissue_name]
        return final_flux_comparison_data_dict

    def return_data(self, data_name, comparison_name, mean=True, **kwargs):
        return self._common_data_loader(data_name, comparison_name, mean)


flux_comparison_data = FluxComparisonFigureData()


class BestSolutionData(BasicFigureData):
    data_prefix = FigureDataKeywords.best_solution

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            best_loss_data = current_data_obj.best_loss_data
            best_solution_vector = current_data_obj.best_solution_vector
            flux_name_index_dict = current_data_obj.flux_name_index_dict
            self.processed_data_dict[data_name] = (best_loss_data, best_solution_vector, flux_name_index_dict)
        else:
            best_loss_data, best_solution_vector, flux_name_index_dict = self.processed_data_dict[data_name]
        return best_loss_data, best_solution_vector, flux_name_index_dict

    def return_data(self, data_name, **kwargs):
        return self._figure_data_preprocess(data_name)


best_solution_data = BestSolutionData()


class EmbeddedFluxData(BasicFigureData):
    data_prefix = FigureDataKeywords.embedding_visualization

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name):
        if data_name in self.processed_data_dict:
            content_tuple = self.processed_data_dict[data_name]
        else:
            current_data_obj = self._return_figure_data(data_name)
            embedded_flux_data_dict = current_data_obj.embedded_flux_data_dict
            complete_distance_dict = current_data_obj.complete_distance_dict
            separated_distance_and_loss_dict = current_data_obj.separated_distance_and_loss_dict
            flux_name_list = current_data_obj.flux_name_list
            content_tuple = (
                embedded_flux_data_dict, complete_distance_dict, separated_distance_and_loss_dict, flux_name_list)
            self.processed_data_dict[data_name] = content_tuple
        return content_tuple
        # if data_name not in self.processed_data_dict:
        # else:
        #     (
        #         embedded_flux_data_dict, complete_distance_dict, separated_distance_and_loss_dict
        #     ) = self.processed_data_dict[data_name]
        # return embedded_flux_data_dict, complete_distance_dict, separated_distance_and_loss_dict

    def return_data(self, data_name, **kwargs):
        return self._figure_data_preprocess(data_name)


embedded_flux_data = EmbeddedFluxData()


class RawFluxValueData(BasicFigureData):
    data_prefix = FigureDataKeywords.raw_flux_value_dict

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _figure_data_preprocess(self, data_name, result_label):
        if data_name not in self.processed_data_dict:
            current_data_obj = self._return_figure_data(data_name)
            raw_flux_value_dict = current_data_obj.raw_flux_value_dict
            self.processed_data_dict[data_name] = raw_flux_value_dict
        else:
            raw_flux_value_dict = self.processed_data_dict[data_name]
        return raw_flux_value_dict[result_label]

    def return_data(self, data_name, result_label, **kwargs):
        return self._figure_data_preprocess(data_name, result_label)


raw_flux_value_dict_data = RawFluxValueData()


class AllFluxRelativeErrorData(BasicFigureData):
    data_prefix = FigureDataKeywords.all_fluxes_relative_error

    def __init__(self):
        super().__init__()
        self.processed_data_dict = {}

    def _single_preprocess(self, data_name):
        current_data_obj = self._return_figure_data(data_name)
        data_matrix = current_data_obj.distance_matrix
        common_flux_name_list = current_data_obj.common_flux_name_list
        result_label_list = current_data_obj.result_label_list
        return data_matrix, common_flux_name_list, result_label_list

    def _load_data_sensitivity_data(self, data_name):
        data_sensitivity_label_dict = ModelDataSensitivityDataFigureConfig.label_dict[DataName.data_sensitivity]
        raw_data_matrix, common_flux_name_list, \
            raw_result_label_list = self._single_preprocess(data_name)
        final_data_matrix_list = []
        result_label_list = []
        result_label_index_dict = {
            ModelDataSensitivityDataFigureConfig.modify_noise_data_to_raw_data(result_label): label_index
            for label_index, result_label in enumerate(raw_result_label_list)}
        total_result_label_dict = {}
        for group_id, each_group_result_label_dict in data_sensitivity_label_dict.items():
            for result_label in each_group_result_label_dict.keys():
                final_data_matrix_list.append(raw_data_matrix[result_label_index_dict[result_label], :])
            total_result_label_dict[group_id] = list(each_group_result_label_dict.keys())
            result_label_list.extend(each_group_result_label_dict.keys())
        data_matrix = np.array(final_data_matrix_list)
        item_tuple = (data_matrix, common_flux_name_list, result_label_list)
        return item_tuple

    def _load_and_merge_multiple_data(self, data_name_dict, raw_result_label):
        total_data_matrix_list = []
        total_result_label_dict = {}
        common_flux_name_list = None
        raw_result_array_list = []
        for current_data_name in data_name_dict.keys():
            current_data_matrix, current_common_flux_name_list, \
                current_result_label_list = self._single_preprocess(current_data_name)
            try:
                raw_result_index = current_result_label_list.index(raw_result_label)
            except ValueError:
                pass
            else:
                current_raw_result_array = current_data_matrix[raw_result_index]
                raw_result_array_list.append(current_raw_result_array)
                current_data_matrix = np.delete(current_data_matrix, raw_result_index, axis=0)
                del current_result_label_list[raw_result_index]
            if common_flux_name_list is None:
                common_flux_name_list = current_common_flux_name_list
            total_result_label_dict[current_data_name] = current_result_label_list
            total_data_matrix_list.append(current_data_matrix)
        if len(raw_result_array_list) != 0:
            final_raw_result_array = np.mean(raw_result_array_list, axis=0)
            total_data_matrix_list = [final_raw_result_array.reshape([1, -1]), *total_data_matrix_list]
            result_label = ModelDataSensitivityDataFigureConfig.modify_noise_data_to_raw_data(raw_result_label)
            # new_total_result_label_dict = {raw_result_label: raw_result_label, **total_result_label_dict}
            new_total_result_label_dict = {result_label: result_label, **total_result_label_dict}
            total_result_label_dict = new_total_result_label_dict
        total_data_matrix = np.concatenate(total_data_matrix_list, axis=0)
        item_tuple = (total_data_matrix, common_flux_name_list, total_result_label_dict)
        return item_tuple

    def _figure_data_preprocess(self, data_name):
        if data_name not in self.processed_data_dict:
            if data_name in {DataName.model_sensitivity, DataName.model_sensitivity_all_data}:
                model_sensitivity_data_name_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
                # total_data_matrix_list = []
                # total_result_label_dict = {}
                # common_flux_name_list = None
                # for model_sensitivity_data_name in model_sensitivity_data_name_dict.keys():
                #     current_data_matrix, current_common_flux_name_list, \
                #         current_result_label_list = self._single_preprocess(model_sensitivity_data_name)
                #     if common_flux_name_list is None:
                #         common_flux_name_list = current_common_flux_name_list
                #     total_result_label_dict[model_sensitivity_data_name] = current_result_label_list
                #     total_data_matrix_list.append(current_data_matrix)
                # total_data_matrix = np.concatenate(total_data_matrix_list, axis=0)
                # item_tuple = (total_data_matrix, common_flux_name_list, total_result_label_dict)
                if data_name == DataName.model_sensitivity:
                    raw_model_data_label = ModelDataSensitivityDataFigureConfig.raw_data_result_label
                else:
                    raw_model_data_label = ModelDataSensitivityDataFigureConfig.all_data_result_label
                item_tuple = self._load_and_merge_multiple_data(model_sensitivity_data_name_dict, raw_model_data_label)
            elif data_name in {DataName.data_sensitivity, DataName.data_sensitivity_with_noise}:
                item_tuple = self._load_data_sensitivity_data(data_name)
            elif data_name in {
                    DataName.config_sensitivity, DataName.config_sensitivity_all_data,
                    DataName.different_constant_flux_with_noise}:
                config_sensitivity_data_name_dict = ModelDataSensitivityDataFigureConfig.config_sensitivity_dict
                if data_name == DataName.different_constant_flux_with_noise:
                    raw_model_data_label = ModelDataSensitivityDataFigureConfig.raw_data_noise_result_label
                    config_sensitivity_data_name_dict = \
                        ModelDataSensitivityDataFigureConfig.config_sensitivity_constant_flux_with_noise_only_dict
                elif data_name == DataName.config_sensitivity:
                    raw_model_data_label = ModelDataSensitivityDataFigureConfig.raw_data_result_label
                elif data_name == DataName.config_sensitivity_all_data:
                    raw_model_data_label = ModelDataSensitivityDataFigureConfig.all_data_result_label
                else:
                    raise ValueError()
                item_tuple = self._load_and_merge_multiple_data(config_sensitivity_data_name_dict, raw_model_data_label)
            else:
                item_tuple = self._single_preprocess(data_name)
            self.processed_data_dict[data_name] = item_tuple
        else:
            item_tuple = self.processed_data_dict[data_name]
        return item_tuple

    def return_data(self, data_name, **kwargs):
        return self._figure_data_preprocess(data_name)


all_fluxes_relative_error_data = AllFluxRelativeErrorData()
