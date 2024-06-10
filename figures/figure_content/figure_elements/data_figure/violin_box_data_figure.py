from .config import DataFigureConfig, DataFigureParameterName as ParameterName, Vector, it, Keywords, \
    np, default_parameter_extract, VerticalAlignment, merge_axis_format_dict, ColorConfig, \
    CommonFigureString, ViolinBoxDataFigure, generate_violin_config_dict
from .figure_data_loader import raw_model_data, flux_comparison_data, loss_data


class TimeLossGridBoxDataFigure(ViolinBoxDataFigure):
    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        ax_total_bottom_left = Vector(0.12, 0.03)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        ax_interval = Vector(0.01, 0.015)

        # try:
        #     common_y_lim = figure_data_parameter_dict.pop(ParameterName.common_y_lim)
        # except KeyError:
        #     common_y_lim = (0, None)
        common_y_lim = default_parameter_extract(figure_data_parameter_dict, ParameterName.common_y_lim, (0, None))
        try:
            default_y_tick_labels = figure_data_parameter_dict[ParameterName.default_y_tick_label_list]
            y_ticks = [float(default_y_tick_label) for default_y_tick_label in default_y_tick_labels]
        except KeyError:
            default_y_tick_labels = Keywords.default
            y_ticks = None

        (
            (raw_loss_value_dict, loss_of_mean_solution_dict), max_loss_value, analyzed_set_size_list,
            selected_min_loss_size_list) = raw_model_data.return_scatter_data(
            figure_class=ParameterName.loss_data, **figure_data_parameter_dict)

        common_line_width = 0.5
        main_color = ColorConfig.normal_blue
        box_body_alpha = 0.3
        median_color = ColorConfig.orange
        data_nested_list = []
        positions_list = []
        # y_lim = (0, max_loss_value * 1.1)
        # y_lim = (0, 0.6)
        # y_lim = (0, 0.6)

        x_label_list = []
        x_ticks_list = []
        y_label_list = []
        x_tick_labels_list = []
        y_ticks_list = []
        y_tick_labels_list = []

        row_num = len(selected_min_loss_size_list)
        col_num = len(analyzed_set_size_list)
        ax_size = (ax_total_size - Vector(col_num - 1, row_num - 1) * ax_interval) / Vector(col_num, row_num)
        ax_bottom_left_list = []
        ax_size_list = []
        # Axes should start from top-left and execute row-first.
        for row_index, selected_min_loss in enumerate(selected_min_loss_size_list):
            for col_index, analyzed_set_size in enumerate(analyzed_set_size_list):
                try:
                    target_nested_list = raw_loss_value_dict[selected_min_loss][analyzed_set_size]
                except KeyError:
                    target_list = []
                else:
                    try:
                        target_list = np.concatenate(target_nested_list)
                    except ValueError:
                        target_list = target_nested_list
                raw_loss_array = [target_list]
                data_nested_list.append(raw_loss_array)
                positions_list.append([1])
                if col_index == 0:
                    y_label_list.append(selected_min_loss)
                    y_tick_labels_list.append(default_y_tick_labels)
                    y_ticks_list.append(y_ticks)
                else:
                    y_label_list.append(None)
                    y_tick_labels_list.append(None)
                    y_ticks_list.append([])
                if row_index != row_num - 1:
                    x_label_list.append(None)
                else:
                    x_label_list.append(analyzed_set_size)
                x_tick_labels_list.append(None)
                current_bottom_left = ax_total_bottom_left + (ax_size + ax_interval) * Vector(
                    col_index, row_num - row_index - 1)
                ax_bottom_left_list.append(current_bottom_left)
                ax_size_list.append(ax_size)
                x_ticks_list.append([])

        figure_config_dict = {
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.005,
            },
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.03,
            },
            ParameterName.box_violin_config_dict: generate_violin_config_dict(
                0.6, box_body_alpha, common_line_width, [main_color], [median_color])
        }

        figure_data_parameter_dict = {
            ParameterName.figure_type: ParameterName.box,
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.legend_center: None,
            ParameterName.legend_area_size: None,
            ParameterName.color_dict: None,
            ParameterName.name_dict: None,
            ParameterName.legend: False,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.data_nested_list: data_nested_list,
            ParameterName.positions_list: positions_list,
            ParameterName.cutoff: None,
            ParameterName.emphasized_flux_list: None,
            ParameterName.y_lim_list: it.repeat(common_y_lim),
            ParameterName.x_label_list: x_label_list,
            ParameterName.x_ticks_list: x_ticks_list,
            ParameterName.y_label_list: y_label_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, **kwargs)


class FluxComparisonViolinBoxDataFigure(ViolinBoxDataFigure):
    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        ax_total_bottom_left = Vector(0.12, 0.03)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        ax_interval = Vector(0.045, 0.035)

        (
            common_x_label, common_y_label,
            preset_y_lim_list, preset_y_ticks_list, preset_x_lim_list,
            display_flux_name_dict, display_group_name_dict, figure_type
        ) = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.common_x_label, ParameterName.common_y_label,
                ParameterName.y_lim_list, ParameterName.y_ticks_list, ParameterName.x_lim_list,
                ParameterName.display_flux_name_dict, ParameterName.display_group_name_dict, ParameterName.figure_type
            ], [
                'Cell type', 'Flux value',
                None, None, None,
                {}, {}, ParameterName.box
            ], pop=True)
        color_dict = figure_data_parameter_dict.pop(ParameterName.color_dict)
        final_flux_comparison_data_dict, _ = flux_comparison_data.return_data(**figure_data_parameter_dict)

        text_axis_loc_pair = Vector(0.5, 1.07)
        common_line_width = 0.5
        column_width = 0.7
        gap_inside_column = 0.1
        box_body_alpha = 0.3
        flux_title_text_format_dict = {
            **DataFigureConfig.common_subplot_text_format_dict_generator(),
            ParameterName.font_size: 9,
        }

        data_nested_list = []
        positions_list = []
        x_label_list = []
        x_ticks_list = []
        x_tick_labels_list = []
        y_label_list = []
        y_ticks_list = []
        y_tick_labels_list = []

        flux_name_nested_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        row_num = len(flux_name_nested_list)
        ax_row_size = (ax_total_size.y - (row_num - 1) * ax_interval.y) / row_num

        x_lim_list = []
        y_lim_list = []
        ax_bottom_left_list = []
        ax_size_list = []
        flux_name_list = []
        color_list = None
        min_column_width = np.inf

        for row_index, row_list in enumerate(flux_name_nested_list):
            this_row_axis_num = len(row_list)
            this_row_axis_col_width = (ax_total_size.x - (this_row_axis_num - 1) * ax_interval.x) / this_row_axis_num
            this_row_bottom_left = ax_total_bottom_left + \
                Vector(0, (ax_row_size + ax_interval.y) * (row_num - row_index - 1))
            for _ in range(this_row_axis_num):
                ax_size_list.append(Vector(this_row_axis_col_width, ax_row_size))
                ax_bottom_left_list.append(this_row_bottom_left)
                this_row_bottom_left = this_row_bottom_left + Vector(this_row_axis_col_width + ax_interval.x, 0)
            for col_index, flux_name in enumerate(row_list):
                current_ax_data_list = []
                current_ax_position_list = []
                current_ax_color_list = []
                current_flux_data_dict = final_flux_comparison_data_dict[flux_name]
                current_x_tick_labels = []
                group_class_dict = {}
                for group_data_dict in current_flux_data_dict.values():
                    group_class_dict.update(group_data_dict)
                max_class_num = len(group_class_dict)
                total_group_num = len(current_flux_data_dict)
                each_column_width_inside_group = \
                    column_width / (max_class_num + gap_inside_column * (max_class_num - 1))
                absolute_gap = each_column_width_inside_group * gap_inside_column
                min_column_width = np.minimum(min_column_width, each_column_width_inside_group)
                # In this part, group is different patient/sample, while class is different condition.
                for group_index, (group_name, group_data_dict) in enumerate(current_flux_data_dict.items()):
                    group_location = group_index + 1
                    for class_index, class_name in enumerate(group_class_dict.keys()):
                        data_array = group_data_dict[class_name]
                        current_ax_data_list.append(data_array)
                        current_ax_position_list.append(
                            group_location - column_width / 2 +
                            (each_column_width_inside_group + absolute_gap) * class_index +
                            each_column_width_inside_group / 2)
                        current_ax_color_list.append(color_dict[class_name])
                    if group_name in display_group_name_dict:
                        display_group_name = display_group_name_dict[group_name]
                    else:
                        display_group_name = group_name
                    current_x_tick_labels.append(display_group_name)

                if flux_name in display_flux_name_dict:
                    display_flux_name = display_flux_name_dict[flux_name]
                else:
                    display_flux_name = flux_name
                flux_name_list.append(display_flux_name)
                x_ticks_list.append(list(range(1, total_group_num + 1)))
                data_nested_list.append(current_ax_data_list)
                positions_list.append(current_ax_position_list)
                y_tick_labels_list.append(Keywords.default)
                if preset_x_lim_list is not None:
                    x_lim = preset_x_lim_list[row_index][col_index]
                else:
                    x_lim = (0.5, total_group_num + 0.5)
                x_lim_list.append(x_lim)
                if preset_y_lim_list is not None:
                    y_lim = preset_y_lim_list[row_index][col_index]
                else:
                    y_lim = None
                y_lim_list.append(y_lim)
                if color_list is None:
                    color_list = current_ax_color_list
                if row_index == row_num - 1:
                    x_tick_labels_list.append(current_x_tick_labels)
                    x_label_list.append(common_x_label)
                else:
                    x_tick_labels_list.append(None)
                    x_label_list.append(None)
                if col_index == 0:
                    y_label_list.append(common_y_label)
                else:
                    y_label_list.append(None)
                if preset_y_ticks_list is not None:
                    y_ticks = preset_y_ticks_list[row_index][col_index]
                else:
                    y_ticks = None
                y_ticks_list.append(y_ticks)

        figure_config_dict = {
            ParameterName.x_tick_label_format_dict: {
                ParameterName.font_size: 7
            },
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.03,
                ParameterName.font_size: 10
            },
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.04,
                ParameterName.font_size: 10
            },
            ParameterName.box_violin_config_dict: generate_violin_config_dict(
                min_column_width, box_body_alpha, common_line_width, color_list, color_list),
            ParameterName.subplot_name_text_format_dict: flux_title_text_format_dict,
        }

        figure_data_parameter_dict = {
            ParameterName.figure_type: figure_type,
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.legend_center: None,
            ParameterName.legend_area_size: None,
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: None,
            ParameterName.legend: False,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.data_nested_list: data_nested_list,
            ParameterName.positions_list: positions_list,
            ParameterName.cutoff: None,
            ParameterName.emphasized_flux_list: None,
            ParameterName.x_lim_list: x_lim_list,
            ParameterName.y_lim_list: y_lim_list,
            ParameterName.x_label_list: x_label_list,
            ParameterName.x_ticks_list: x_ticks_list,
            ParameterName.y_label_list: y_label_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
            ParameterName.subplot_name_list: flux_name_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, **kwargs)


class ExperimentalOptimizationLossComparisonBoxDataFigure(ViolinBoxDataFigure):
    ax_interval = Vector(0.015, 0.03)        # (horizontal, vertical)
    each_row_figure_height = 0.4

    @staticmethod
    def calculate_height(self, row_num):
        return self.each_row_figure_height * row_num + (row_num - 1) * self.ax_interval.y

    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        ax_interval = self.ax_interval / size
        ax_row_size = self.each_row_figure_height / size.y
        ax_total_bottom_left = Vector(0, 0)
        ax_total_width = 1

        (
            common_x_label, common_y_label, preset_y_lim_list, preset_y_ticks_list, preset_y_tick_labels_list,
            preset_x_lim_list, display_group_name_dict, figure_type
        ) = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.common_x_label, ParameterName.common_y_label,
                ParameterName.y_lim_list, ParameterName.y_ticks_list, ParameterName.y_tick_labels_list,
                ParameterName.x_lim_list,
                ParameterName.display_group_name_dict, ParameterName.figure_type
            ], [
                CommonFigureString.patient_id, CommonFigureString.loss,
                None, None, Keywords.default, None,
                {}, ParameterName.box
            ], pop=True)
        color_dict = figure_data_parameter_dict.pop(ParameterName.color_dict)
        result_label_layout_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.result_label_layout_list, None)
        _, filtered_loss_data_dict = loss_data.return_data(**figure_data_parameter_dict)
        if result_label_layout_list is None:
            result_label_layout_list = [['']]
            filtered_loss_data_dict = {(0, 0): filtered_loss_data_dict}
            row_num = 1
            if preset_y_lim_list is not None:
                preset_y_lim_list = [[preset_y_lim_list]]
            if preset_y_ticks_list is not None:
                preset_y_ticks_list = [[preset_y_ticks_list]]
            if preset_y_tick_labels_list is not Keywords.default:
                preset_y_tick_labels_list = [[preset_y_tick_labels_list]]
        else:
            row_num = len(result_label_layout_list)

        text_axis_loc_pair = Vector(0.5, 1.07)
        common_line_width = 0.5
        column_width = 0.7
        gap_inside_column = 0.1
        box_body_alpha = 0.3
        flux_title_text_format_dict = {
            **DataFigureConfig.common_subplot_text_format_dict_generator(),
            ParameterName.font_size: 9,
        }

        data_nested_list = []
        positions_list = []
        x_label_list = []
        x_ticks_list = []
        x_tick_labels_list = []
        y_label_list = []
        y_ticks_list = []
        y_tick_labels_list = []

        x_lim_list = []
        y_lim_list = []
        ax_bottom_left_list = []
        ax_size_list = []
        color_list = None
        min_column_width = np.inf

        for row_index, row_list in enumerate(result_label_layout_list):
            this_row_axis_num = len(row_list)
            this_row_axis_col_width = (ax_total_width - (this_row_axis_num - 1) * ax_interval.x) / this_row_axis_num
            this_row_bottom_left = ax_total_bottom_left + \
                Vector(0, (ax_row_size + ax_interval.y) * (row_num - row_index - 1))
            for _ in range(this_row_axis_num):
                ax_size_list.append(Vector(this_row_axis_col_width, ax_row_size))
                ax_bottom_left_list.append(this_row_bottom_left)
                this_row_bottom_left = this_row_bottom_left + Vector(this_row_axis_col_width + ax_interval.x, 0)
            for col_index, result_label in enumerate(row_list):
                current_ax_data_list = []
                current_ax_position_list = []
                current_ax_color_list = []
                current_loss_data_dict = filtered_loss_data_dict[(row_index, col_index)]
                current_x_tick_labels = []
                group_class_dict = {}
                for group_data_dict in current_loss_data_dict.values():
                    group_class_dict.update(group_data_dict)
                max_class_num = len(group_class_dict)
                total_group_num = len(current_loss_data_dict)
                each_column_width_inside_group = \
                    column_width / (max_class_num + gap_inside_column * (max_class_num - 1))
                absolute_gap = each_column_width_inside_group * gap_inside_column
                min_column_width = np.minimum(min_column_width, each_column_width_inside_group)
                # In this part, group is different patient/sample, while class is different condition.
                for group_index, (group_name, group_data_dict) in enumerate(current_loss_data_dict.items()):
                    group_location = group_index + 1
                    for class_index, class_name in enumerate(group_class_dict.keys()):
                        data_array = group_data_dict[class_name]
                        current_ax_data_list.append(data_array)
                        current_ax_position_list.append(
                            group_location - column_width / 2 +
                            (each_column_width_inside_group + absolute_gap) * class_index +
                            each_column_width_inside_group / 2)
                        current_ax_color_list.append(color_dict[class_name])
                    if group_name in display_group_name_dict:
                        display_group_name = display_group_name_dict[group_name]
                    else:
                        display_group_name = group_name
                    current_x_tick_labels.append(display_group_name)

                x_ticks_list.append(list(range(1, total_group_num + 1)))
                data_nested_list.append(current_ax_data_list)
                positions_list.append(current_ax_position_list)
                # y_tick_labels_list.append(Keywords.default)
                if preset_y_tick_labels_list != Keywords.default:
                    y_tick_labels_list.append(preset_y_tick_labels_list[row_index][col_index])
                else:
                    y_tick_labels_list.append(Keywords.default)
                if preset_x_lim_list is not None:
                    x_lim = preset_x_lim_list[row_index][col_index]
                else:
                    x_lim = (0.5, total_group_num + 0.5)
                x_lim_list.append(x_lim)
                if preset_y_lim_list is not None:
                    y_lim = preset_y_lim_list[row_index][col_index]
                else:
                    y_lim = None
                y_lim_list.append(y_lim)
                if color_list is None:
                    color_list = current_ax_color_list
                if row_index == row_num - 1:
                    x_tick_labels_list.append(current_x_tick_labels)
                    x_label_list.append(common_x_label)
                else:
                    x_tick_labels_list.append(None)
                    x_label_list.append(None)
                if col_index == 0:
                    y_label_list.append(common_y_label)
                else:
                    y_label_list.append(None)
                if preset_y_ticks_list is not None:
                    y_ticks = preset_y_ticks_list[row_index][col_index]
                else:
                    y_ticks = None
                y_ticks_list.append(y_ticks)

        figure_config_dict = {
            ParameterName.x_tick_label_format_dict: {
                ParameterName.font_size: 9
            },
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.03,
                ParameterName.font_size: 10
            },
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.04,
                ParameterName.font_size: 10
            },
            ParameterName.box_violin_config_dict: generate_violin_config_dict(
                min_column_width, box_body_alpha, common_line_width, color_list, color_list),
            ParameterName.subplot_name_text_format_dict: flux_title_text_format_dict,
        }

        figure_data_parameter_dict = {
            ParameterName.figure_type: figure_type,
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.legend_center: None,
            ParameterName.legend_area_size: None,
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: None,
            ParameterName.legend: False,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.data_nested_list: data_nested_list,
            ParameterName.positions_list: positions_list,
            ParameterName.cutoff: None,
            ParameterName.emphasized_flux_list: None,
            ParameterName.x_lim_list: x_lim_list,
            ParameterName.y_lim_list: y_lim_list,
            ParameterName.x_label_list: x_label_list,
            ParameterName.x_ticks_list: x_ticks_list,
            ParameterName.y_label_list: y_label_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, **kwargs)


class LossDistanceGridBoxDataFigure(ViolinBoxDataFigure):
    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, scale=1, **kwargs):
        ax_total_bottom_left = Vector(0.12, 0.03)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        ax_interval = Vector(0.01, 0.015)

        common_y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim, (0, None), pop=True)
        default_y_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.default_y_tick_label_list, Keywords.default, pop=True)
        if default_y_tick_labels != Keywords.default:
            y_ticks = [float(default_y_tick_label) for default_y_tick_label in default_y_tick_labels]
        else:
            y_ticks = None

        figure_data_tuple = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_data, None, pop=True)
        if figure_data_tuple is None:
            figure_data_tuple = raw_model_data.return_scatter_data(**figure_data_parameter_dict)
        (
            value_dict_list, max_value, complete_analyzed_set_size_list,
            complete_selected_min_loss_size_list) = figure_data_tuple
        with_re_optimization = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized, True, pop=True)
        if not with_re_optimization and len(value_dict_list) == 3:
            value_dict_list = value_dict_list[:2]
        with_traditional_method = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_traditional_method, False, pop=True)
        traditional_selected_size = 1
        traditional_optimized_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.traditional_optimized_size, None)
        target_analyzed_set_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized_size, complete_analyzed_set_size_list, pop=True)
        if isinstance(target_analyzed_set_list, (int, np.int32)):
            target_analyzed_set_list = [target_analyzed_set_list]
        target_selected_min_loss_size_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.selection_size, complete_selected_min_loss_size_list, pop=True)
        if isinstance(target_selected_min_loss_size_list, (int, np.int32)):
            target_selected_min_loss_size_list = [target_selected_min_loss_size_list]
        color_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.color_dict, None, pop=True)
        data_set_num = len(value_dict_list)
        if with_traditional_method:
            data_set_num += 1
            assert traditional_optimized_size is not None
        common_x_tick_label_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.x_tick_labels_list, None, pop=True)
        if common_x_tick_label_list is not None:
            x_tick_num = len(common_x_tick_label_list)
            assert data_set_num % x_tick_num == 0
            tick_data_set_ratio = data_set_num // x_tick_num
        else:
            tick_data_set_ratio = 1
        common_y_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_label, None, pop=True)
        if color_dict is None:
            main_color_list = [ColorConfig.normal_blue] * data_set_num
            median_color_list = [ColorConfig.orange] * data_set_num
        else:
            if len(color_dict) == data_set_num:
                main_color_list = list(color_dict.values())
                median_color_list = list(color_dict.values())
            else:
                color_list = default_parameter_extract(
                    figure_data_parameter_dict, ParameterName.color, None, force=True, pop=True)
                assert len(color_list) == data_set_num
                main_color_list = color_list
                median_color_list = color_list

        common_line_width = 0.5
        box_body_alpha = 0.3
        common_x_lim = [0.5, data_set_num + 0.5]
        data_nested_list = []
        positions_list = []
        # y_lim = (0, max_value * 1.1)
        # y_lim = (0, 0.6)
        # y_lim = (0, 0.6)

        x_label_list = []
        x_ticks_list = []
        y_label_list = []
        x_tick_labels_list = []
        y_ticks_list = []
        y_tick_labels_list = []

        row_num = len(target_selected_min_loss_size_list)
        col_num = len(target_analyzed_set_list)
        ax_size = (ax_total_size - Vector(col_num - 1, row_num - 1) * ax_interval) / Vector(col_num, row_num)
        ax_bottom_left_list = []
        ax_size_list = []
        # Axes should start from top-left and execute row-first.
        for row_index, selected_size in enumerate(target_selected_min_loss_size_list):
            for col_index, analyzed_set_size in enumerate(target_analyzed_set_list):
                try:
                    if with_traditional_method:
                        current_value_list = [
                            value_dict_list[0][traditional_selected_size][traditional_optimized_size]
                        ]
                    else:
                        current_value_list = []
                    current_value_list.extend([
                        value_dict[selected_size][analyzed_set_size] for value_dict in value_dict_list])
                except KeyError:
                    raw_value_list = [[] for _ in value_dict_list]
                else:
                    raw_value_list = []
                    for value_list in current_value_list:
                        try:
                            raw_value_list.append(np.concatenate(value_list))
                        except ValueError:
                            raw_value_list.append(value_list)
                data_nested_list.append(raw_value_list)
                current_positions = list(range(1, data_set_num + 1))
                positions_list.append(current_positions)
                if col_index == 0:
                    if common_x_tick_label_list is None:
                        y_label_list.append(selected_size)
                    else:
                        y_label_list.append(common_y_label)
                    y_tick_labels_list.append(default_y_tick_labels)
                    y_ticks_list.append(y_ticks)
                else:
                    y_label_list.append(None)
                    y_tick_labels_list.append(None)
                    y_ticks_list.append([])
                if row_index != row_num - 1:
                    x_label_list.append(None)
                    x_tick_labels_list.append(None)
                else:
                    if common_x_tick_label_list is None:
                        x_label_list.append(analyzed_set_size)
                        x_tick_labels_list.append(None)
                    else:
                        x_label_list.append(None)
                        x_tick_labels_list.append(common_x_tick_label_list)
                if common_x_tick_label_list is None:
                    x_ticks_list.append([])
                else:
                    if tick_data_set_ratio > 1:
                        current_positions = [
                            (2 * i + tick_data_set_ratio - 1) / tick_data_set_ratio
                            for i in range(1, data_set_num + 1, tick_data_set_ratio)]
                    x_ticks_list.append(current_positions)
                current_bottom_left = ax_total_bottom_left + (ax_size + ax_interval) * Vector(
                    col_index, row_num - row_index - 1)
                ax_bottom_left_list.append(current_bottom_left)
                ax_size_list.append(ax_size)

        figure_config_dict = {
            ParameterName.x_label_format_dict: merge_axis_format_dict({
                ParameterName.axis_label_distance: 0.005,
            }, {}, figure_data_parameter_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict({
                ParameterName.axis_tick_label_distance: 0.01,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.font_size: (DataFigureConfig.GroupDataFigure.x_y_axis_tick_label_font_size + 2) * scale
            }, {}, figure_data_parameter_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict({
                ParameterName.axis_label_distance: 0.03,
            }, {}, figure_data_parameter_dict, ParameterName.y_label_format_dict),
            ParameterName.box_violin_config_dict: generate_violin_config_dict(
                0.6, box_body_alpha, common_line_width, main_color_list, median_color_list),
            # ParameterName.scatter_param_dict: {
            #     ParameterName.marker_size: 0.2,
            #     ParameterName.marker_color: [ColorConfig.data_figure_base_color],
            # },
        }

        figure_data_parameter_dict = {
            ParameterName.figure_type: ParameterName.box,
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: None,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.data_nested_list: data_nested_list,
            ParameterName.positions_list: positions_list,
            ParameterName.cutoff: None,
            ParameterName.emphasized_flux_list: None,
            ParameterName.x_lim_list: it.repeat(common_x_lim),
            ParameterName.y_lim_list: it.repeat(common_y_lim),
            ParameterName.x_label_list: x_label_list,
            ParameterName.x_ticks_list: x_ticks_list,
            ParameterName.y_label_list: y_label_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
            **figure_data_parameter_dict,
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)

