from ..config import DataFigureConfig, ParameterName, Vector, ColorConfig, Keywords, np, move_and_scale_for_dict, \
    merge_axis_format_dict, it, common_legend_generator, default_parameter_extract, CommonFigureString, \
    VerticalAlignment, LineStyle, DataName, ProtocolSearchingMaterials, t_test_of_two_groups
from .figure_data_loader import raw_model_data, flux_comparison_data, embedded_flux_data
from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import draw_text_by_axis_loc, single_scatter_plotting

GroupDataFigure = DataFigureConfig.GroupDataFigure
scatter_line_diagram_str = 'scatter_line_diagram'


class BasicScatterDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        new_figure_config_dict = figure_data_parameter_dict[ParameterName.figure_config_dict]
        (
            ax_bottom_left_list,
            ax_size_list,
            color_dict,
            self.complete_data_dict_list,
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.color_dict,
            ParameterName.data_nested_list,
        ]]
        self.complete_scatter_line_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.scatter_line, it.repeat(None))

        (
            axis_format_dict, axis_tick_format_dict,
            axis_label_format_dict) = DataFigureConfig.common_axis_param_dict_generator()
        figure_config_dict = {
            **{
                key: new_figure_config_dict[key] if key in new_figure_config_dict else {}
                for key in [
                    ParameterName.cutoff_param_dict, ParameterName.subplot_name_text_format_dict,
                    ParameterName.error_bar_param_dict, ParameterName.scatter_param_dict,
                    ParameterName.line_param_dict, ParameterName.supplementary_text_format_dict,
                ]
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }

        (
            self.emphasized_flux_list,
            self.subplot_name_list,
            self.text_axis_loc_pair,
        ) = [
            figure_data_parameter_dict[key] if key in figure_data_parameter_dict else None
            for key in (
                ParameterName.emphasized_flux_list,
                ParameterName.subplot_name_list,
                ParameterName.text_axis_loc_pair,
            )]
        self.supplementary_text_list, self.supplementary_text_loc_list = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.supplementary_text_list,
                ParameterName.supplementary_text_loc_list,
            ], None, repeat_default_value=True)

        (
            self.cutoff_value_list,
            self.x_lim_list,
            self.x_label_list,
            self.x_ticks_list,
            self.x_tick_labels_list,
            self.y_lim_list,
            self.y_label_list,
            self.y_ticks_list,
            self.y_tick_labels_list,
            self.figure_type
        ) = [
            figure_data_parameter_dict[key]
            if key in figure_data_parameter_dict and figure_data_parameter_dict[key] is not None
            else it.repeat(None)
            for key in (
                ParameterName.cutoff,
                ParameterName.x_lim_list,
                ParameterName.x_label_list,
                ParameterName.x_ticks_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_lim_list,
                ParameterName.y_label_list,
                ParameterName.y_ticks_list,
                ParameterName.y_tick_labels_list,
                ParameterName.figure_type
            )]
        self.error_bar = default_parameter_extract(figure_data_parameter_dict, ParameterName.error_bar, False)

        if ParameterName.legend in figure_data_parameter_dict:
            legend = figure_data_parameter_dict[ParameterName.legend]
        else:
            legend = False
        if legend:
            legend_config_dict = figure_data_parameter_dict[ParameterName.legend_config_dict]
            legend_obj = common_legend_generator(legend_config_dict, color_dict)
        else:
            legend_obj = None

        super().__init__(
            bottom_left, size, ax_bottom_left_list, ax_size_list,
            axis_spine_format_dict=axis_format_dict, axis_tick_format_dict=axis_tick_format_dict,
            figure_config_dict=figure_config_dict, legend_obj=legend_obj, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        ax_and_transform_list = super().draw(fig, parent_ax, parent_transformation)
        for (
                complete_data_dict, (current_ax, current_transform), x_lim, x_label, x_ticks, x_tick_labels, y_lim,
                y_label, y_ticks, y_tick_labels, cutoff_value, scatter_line) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.x_lim_list, self.x_label_list,
                self.x_ticks_list, self.x_tick_labels_list, self.y_lim_list, self.y_label_list, self.y_ticks_list,
                self.y_tick_labels_list, self.cutoff_value_list, self.complete_scatter_line_list):
            single_scatter_plotting(
                current_ax, current_transform, complete_data_dict, x_lim=x_lim, x_ticks=x_ticks, x_label=x_label,
                x_tick_labels=x_tick_labels, y_lim=y_lim, y_ticks=y_ticks,
                y_label=y_label, y_tick_labels=y_tick_labels, cutoff_value=cutoff_value,
                scatter_line=scatter_line, error_bar=self.error_bar, **self.figure_config_dict)
        if self.subplot_name_list is not None:
            for subplot_name, (current_ax, current_transform) in zip(self.subplot_name_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, subplot_name, self.text_axis_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.subplot_name_text_format_dict])
        if self.supplementary_text_list is not None:
            for supplementary_text, supplementary_loc, (current_ax, current_transform) in zip(
                    self.supplementary_text_list, self.supplementary_text_loc_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, supplementary_text, supplementary_loc, current_transform,
                    **self.figure_config_dict[ParameterName.supplementary_text_format_dict]
                )

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        super().move_and_scale(
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)
        for data_dict in self.complete_data_dict_list:
            move_and_scale_for_dict(data_dict, scale=scale)


def common_figure_config_dict_generator(axis_label_format_dict, scale=1):
    return {
        ParameterName.x_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.x_label_format_dict_generator(scale),
        },
        ParameterName.x_tick_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.x_tick_label_format_dict_generator(scale),
        },
        ParameterName.y_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.y_label_format_dict_generator(scale),
            ParameterName.axis_label_distance: 0.03 * scale,
        },
        ParameterName.y_tick_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.y_tick_label_format_dict_generator(scale),
        },
        ParameterName.scatter_param_dict: {
            ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
        }
    }


class GridScatterDataFigure(BasicScatterDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        ax_total_bottom_left = Vector(0.11, 0.03)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        ax_interval = Vector(0.01, 0.015)  # (horizontal, vertical)

        # try:
        #     scale = figure_data_parameter_dict[ParameterName.scale]
        # except KeyError:
        #     scale = 1
        try:
            default_y_tick_label_list = figure_data_parameter_dict[ParameterName.default_y_tick_label_list]
        except KeyError:
            default_y_tick_label_list = Keywords.default
            default_y_tick_list = None
        else:
            default_y_tick_list = [float(num_str) for num_str in default_y_tick_label_list]
        try:
            y_lim = figure_data_parameter_dict.pop(ParameterName.common_y_lim)
        except KeyError:
            y_lim = None

        column_width = 0.9
        marker_size = 0.2
        marker_color = ColorConfig.data_figure_base_color
        cutoff_param_dict = {
            ParameterName.axis: ParameterName.y,
            ParameterName.edge_style: '--',
            ParameterName.edge_color: ColorConfig.data_figure_contrast_color,
            ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio,
            ParameterName.z_order: DataFigureConfig.cutoff_value_z_order,
        }
        figure_config_dict = {
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.03,
            },
            ParameterName.cutoff_param_dict: cutoff_param_dict,
        }
        (
            (_, data_dict), max_y_lim, x_label_index_dict, y_label_index_dict
        ) = raw_model_data.return_scatter_data(**figure_data_parameter_dict)
        scatter_y_lim_pair = (0, max_y_lim)
        common_y_lim = scatter_y_lim_pair if y_lim is None else y_lim

        row_num = len(y_label_index_dict)
        col_num = len(x_label_index_dict)
        ax_size = (ax_total_size - Vector(col_num - 1, row_num - 1) * ax_interval) / Vector(col_num, row_num)
        ax_bottom_left_list = []
        ax_size_list = []

        display_x_label_list = []
        display_y_label_list = []
        y_ticks_list = []
        y_tick_labels_list = []
        complete_data_dict_list = []
        for y_label, row_index in y_label_index_dict.items():
            for x_label, col_index in x_label_index_dict.items():
                current_subplot_data_array = data_dict[y_label][x_label]
                random_x_value = (np.random.random(len(current_subplot_data_array)) - 0.5) * column_width
                complete_data_dict = {
                    ParameterName.x_value_array: random_x_value,
                    ParameterName.y_value_array: (current_subplot_data_array, None),
                    ParameterName.marker_size: marker_size,
                    ParameterName.marker_color: [marker_color],  # To avoid warning from matplotlib
                }
                # complete_data_dict_list.append({'': complete_data_dict})
                complete_data_dict_list.append(complete_data_dict)
                if col_index == 0:
                    y_ticks = default_y_tick_list
                    y_tick_label = default_y_tick_label_list
                    display_y_label = y_label
                else:
                    y_ticks = []
                    y_tick_label = None
                    display_y_label = None
                if row_index != row_num - 1:
                    display_x_label = None
                else:
                    display_x_label = x_label
                display_x_label_list.append(display_x_label)
                display_y_label_list.append(display_y_label)
                y_ticks_list.append(y_ticks)
                y_tick_labels_list.append(y_tick_label)
                current_bottom_left = ax_total_bottom_left + (ax_size + ax_interval) * Vector(
                    col_index, row_num - row_index - 1)
                ax_bottom_left_list.append(current_bottom_left)
                ax_size_list.append(ax_size)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.color_dict: None,
            ParameterName.data_nested_list: complete_data_dict_list,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_lim_list: it.repeat((-0.8, 0.8)),
            ParameterName.x_label_list: display_x_label_list,
            ParameterName.x_ticks_list: it.repeat([]),
            ParameterName.y_lim_list: it.repeat(common_y_lim),
            ParameterName.y_label_list: display_y_label_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
            ParameterName.cutoff: it.repeat(0),

            ParameterName.legend: False,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)


def general_flux_layout_generator(
        ax_total_bottom_left, ax_total_size, ax_interval, final_flux_comparison_data_dict, flux_name_location_list,
        common_x_label, common_y_label, preset_y_lim_list, preset_y_ticks_list, preset_x_lim_list, display_name_dict,
        column_width, class_width, marker_size, color_dict, scatter_param_dict, compare_one_by_one=False,
        with_scatter_line=False, scatter_line_param_dict=None, complete_p_value_y_value_list=None,
        p_value_cap_param_dict=None):
    row_num = len(flux_name_location_list)
    ax_row_size = (ax_total_size.y - (row_num - 1) * ax_interval.y) / row_num
    flux_name_list = []
    ax_bottom_left_list = []
    ax_size_list = []
    display_x_label_list = []
    display_y_label_list = []
    x_lim_list = []
    x_ticks_list = []
    x_tick_labels_list = []
    y_lim_list = []
    y_ticks_list = []
    y_tick_labels_list = []
    complete_scatter_line_list = []
    complete_plotting_data_dict_list = []
    if complete_p_value_y_value_list is not None:
        complete_p_value_text_list = []
        complete_p_value_text_loc_list = []
    else:
        complete_p_value_text_list = None
        complete_p_value_text_loc_list = None
    for row_index, row_list in enumerate(flux_name_location_list):
        total_array_len_this_row = 0
        this_row_array_len_list = []
        this_row_axis_num = len(row_list)
        for col_index, flux_name in enumerate(row_list):
            flux_name_list.append(flux_name)
            current_flux_data_dict = final_flux_comparison_data_dict[flux_name]
            if complete_p_value_y_value_list is not None:
                current_p_value_y_value = complete_p_value_y_value_list[row_index][col_index]
            else:
                current_p_value_y_value = None
            maximal_value = 0
            minimal_value = 0
            total_group_num = len(current_flux_data_dict)
            current_x_value_list = []
            current_mean_y_value_list = []
            current_std_y_value_list = []
            current_market_color_list = []
            current_x_ticks_list = []
            added_x_ticks_set = set()
            this_col_len = None
            raw_scatter_line_xy_list = []
            current_flux_data_dict_by_class = {}
            p_value_list = []
            group_center_x_value_list = []
            if compare_one_by_one:
                for group_index, (group_name, current_group_value_obj) in enumerate(current_flux_data_dict.items()):
                    total_class_num = len(current_group_value_obj)
                    if current_p_value_y_value is not None:
                        assert total_class_num == 2
                    current_group_center_value = group_index
                    this_group_scatter_line_xy_list = []
                    sample_pair_list = []
                    for class_index, (class_name, current_class_value_list) in enumerate(
                            current_group_value_obj.items()):
                        maximal_value = np.maximum(maximal_value, np.max(current_class_value_list))
                        minimal_value = np.minimum(minimal_value, np.min(current_class_value_list))
                        if len(current_class_value_list) >= 3:
                            current_std = np.std(current_class_value_list)
                        else:
                            current_std = None
                        current_mean = np.mean(current_class_value_list)
                        sample_pair_list.append(current_class_value_list)
                        each_class_column_width = column_width / total_class_num
                        current_class_center_x_value = (class_index + 0.5) * each_class_column_width \
                            - 0.5 * column_width
                        if this_col_len is None:
                            this_col_len = total_group_num
                        current_x_value = current_class_center_x_value + current_group_center_value
                        if with_scatter_line:
                            this_group_scatter_line_xy_list.append((current_x_value, current_mean))
                        if group_name not in added_x_ticks_set:
                            current_x_ticks_list.append(current_group_center_value)
                            added_x_ticks_set.add(group_name)
                        current_x_value_list.append(current_x_value)
                        current_mean_y_value_list.append(current_mean)
                        current_std_y_value_list.append(current_std)
                        current_market_color_list.append(color_dict[class_name])
                    if with_scatter_line:
                        raw_scatter_line_xy_list.append(this_group_scatter_line_xy_list)
                    if current_p_value_y_value is not None:
                        group_center_x_value_list.append(current_group_center_value)
                        p_value_list.append(t_test_of_two_groups(*sample_pair_list))
            else:
                for group_index, (group_name, current_group_value_obj) in enumerate(current_flux_data_dict.items()):
                    for class_name, current_class_value_list in current_group_value_obj.items():
                        if class_name not in current_flux_data_dict_by_class:
                            current_flux_data_dict_by_class[class_name] = {}
                        current_flux_data_dict_by_class[class_name][group_index] = current_class_value_list
                complete_class_num = len(current_flux_data_dict_by_class)
                if current_p_value_y_value is not None:
                    raise ValueError()
                each_class_column_width = column_width / complete_class_num
                for class_index, (class_name, current_class_data_dict) in enumerate(
                        current_flux_data_dict_by_class.items()):
                    current_class_center_x_value = (class_index + 0.5) * each_class_column_width - 0.5 * column_width
                    if this_col_len is None:
                        this_col_len = complete_class_num
                    current_group_num = len(current_class_data_dict)
                    each_data_point_width = each_class_column_width / current_group_num
                    current_color = color_dict[class_name]
                    for group_index, (group_name, current_group_value_list) in enumerate(
                            current_class_data_dict.items()):
                        current_x_value = (
                            (group_index + 0.5) * each_data_point_width - 0.5 * each_class_column_width
                                ) * class_width + current_class_center_x_value
                        current_mean = np.mean(current_group_value_list)
                        if len(current_group_value_list) >= 3:
                            current_std = np.std(current_group_value_list)
                        else:
                            current_std = None
                        current_x_value_list.append(current_x_value)
                        current_mean_y_value_list.append(current_mean)
                        current_std_y_value_list.append(current_std)
                        current_market_color_list.append(current_color)
                    current_x_ticks_list.append(current_class_center_x_value)
            current_tissue_data_dict = {
                ParameterName.x_value_array: np.array(current_x_value_list),
                ParameterName.y_value_array: (np.array(current_mean_y_value_list), np.array(current_std_y_value_list)),
                ParameterName.marker_size: marker_size,
                ParameterName.marker_color: current_market_color_list,
                ParameterName.scatter_param_dict: scatter_param_dict,
            }
            complete_plotting_data_dict_list.append(current_tissue_data_dict)
            x_ticks_list.append(current_x_ticks_list)
            if preset_x_lim_list is not None:
                x_lim = preset_x_lim_list[row_index][col_index]
            else:
                if compare_one_by_one:
                    x_lim = (-0.5, current_x_ticks_list[-1] + 0.5)
                else:
                    x_lim = (-0.5, 0.5)
            x_lim_list.append(x_lim)
            if preset_y_lim_list is not None:
                y_lim = preset_y_lim_list[row_index][col_index]
            else:
                y_lim = None
            y_lim_list.append(y_lim)
            if preset_y_ticks_list is not None:
                y_ticks = preset_y_ticks_list[row_index][col_index]
            else:
                y_ticks = None
            y_ticks_list.append(y_ticks)
            y_tick_labels_list.append(Keywords.default)
            this_row_array_len_list.append(this_col_len)
            total_array_len_this_row += this_col_len
            if col_index == 0:
                display_y_label = common_y_label
            else:
                display_y_label = None
            if row_index != row_num - 1:
                x_tick_labels = None
                display_x_label = None
            else:
                if compare_one_by_one:
                    x_tick_labels = [
                        display_name_dict[group_name] if group_name in display_name_dict else group_name
                        for group_name in current_flux_data_dict.keys()
                    ]
                else:
                    x_tick_labels = [
                        display_name_dict[class_name] if class_name in display_name_dict else class_name
                        for class_name in current_flux_data_dict_by_class.keys()
                    ]
                display_x_label = common_x_label
            x_tick_labels_list.append(x_tick_labels)
            display_x_label_list.append(display_x_label)
            display_y_label_list.append(display_y_label)
            current_scatter_line_list = []
            if with_scatter_line:
                reshaped_scatter_line_list = []
                for scatter_line_pair in raw_scatter_line_xy_list:
                    reshaped_scatter_line_list.append([*np.array(scatter_line_pair).T, scatter_line_param_dict])
                current_scatter_line_list.extend(reshaped_scatter_line_list)
            if current_p_value_y_value is not None:
                (
                    p_value_text_list, p_value_text_loc_list, p_value_cap_list
                ) = p_value_parameter_list_generator(
                    group_center_x_value_list, current_p_value_y_value, p_value_list, x_lim, y_lim,
                    dict(p_value_cap_param_dict))
                current_scatter_line_list.extend(p_value_cap_list)
                complete_p_value_text_list.append(p_value_text_list)
                complete_p_value_text_loc_list.append(p_value_text_loc_list)
            if len(current_scatter_line_list) == 0:
                current_scatter_line_list = None
            complete_scatter_line_list.append(current_scatter_line_list)
        unit_array_len_size = (ax_total_size.x - (this_row_axis_num - 1) * ax_interval.x) / total_array_len_this_row
        this_row_bottom_left = ax_total_bottom_left + \
                               Vector(0, (ax_row_size + ax_interval.y) * (row_num - row_index - 1))
        for current_array_len in this_row_array_len_list:
            this_ax_col_len = current_array_len * unit_array_len_size
            ax_size_list.append(Vector(this_ax_col_len, ax_row_size))
            ax_bottom_left_list.append(this_row_bottom_left)
            this_row_bottom_left = this_row_bottom_left + Vector(this_ax_col_len + ax_interval.x, 0)
    return ax_bottom_left_list, ax_size_list, complete_plotting_data_dict_list, flux_name_list, x_lim_list, \
        display_x_label_list, x_ticks_list, x_tick_labels_list, y_lim_list, display_y_label_list, y_ticks_list, \
        y_tick_labels_list, complete_scatter_line_list, complete_p_value_text_list, complete_p_value_text_loc_list


def pure_flux_layout_generator(
        ax_total_bottom_left, ax_total_size, ax_interval, final_flux_comparison_data_dict, flux_name_location_list,
        scatter_line_figure, common_y_label, preset_y_lim_list, preset_y_ticks_list, preset_x_lim_list,
        display_group_name_dict, column_width, marker_size, color_dict, scatter_param_dict,
        compare_one_by_one=False):
    row_num = len(flux_name_location_list)
    ax_row_size = (ax_total_size.y - (row_num - 1) * ax_interval.y) / row_num
    flux_name_list = []
    ax_bottom_left_list = []
    ax_size_list = []
    display_x_label_list = []
    display_y_label_list = []
    x_lim_list = []
    x_ticks_list = []
    x_tick_labels_list = []
    y_lim_list = []
    y_ticks_list = []
    y_tick_labels_list = []
    complete_plotting_data_dict_list = []
    for row_index, row_list in enumerate(flux_name_location_list):
        total_array_len_this_row = 0
        this_row_array_len_list = []
        this_row_axis_num = len(row_list)
        for col_index, flux_name in enumerate(row_list):
            flux_name_list.append(flux_name)
            current_flux_data_dict = final_flux_comparison_data_dict[flux_name]
            plotting_data_dict = {}
            maximal_value = 0
            minimal_value = 0
            for index, (tissue_name, current_tissue_value_obj) in enumerate(current_flux_data_dict.items()):
                if scatter_line_figure:
                    current_y_value_data_dict = {}
                    for patient_id, current_patient_value_list in current_tissue_value_obj.items():
                        maximal_value = np.maximum(maximal_value, np.max(current_patient_value_list))
                        minimal_value = np.minimum(minimal_value, np.min(current_patient_value_list))
                        if len(current_patient_value_list) >= 3:
                            current_std = np.std(current_patient_value_list)
                        else:
                            current_std = None
                        current_mean = np.mean(current_patient_value_list)
                        current_y_value_data_dict[patient_id] = (current_mean, current_std)
                    current_tissue_data_dict = {
                        ParameterName.y_value_data_dict: current_y_value_data_dict,
                        ParameterName.marker_size: marker_size,
                        ParameterName.marker_color: [color_dict[tissue_name]],  # To avoid warning from matplotlib
                        ParameterName.scatter_param_dict: scatter_param_dict,
                    }
                else:
                    value_array = np.array(current_tissue_value_obj)
                    maximal_value = np.maximum(maximal_value, np.max(value_array))
                    point_num = len(value_array)
                    random_x_value = np.linspace(-0.5, 0.5, point_num) * column_width + index
                    current_tissue_data_dict = {
                        ParameterName.x_value_array: random_x_value,
                        ParameterName.y_value_array: value_array,
                        ParameterName.marker_size: marker_size,
                        ParameterName.marker_color: [color_dict[tissue_name]],  # To avoid warning from matplotlib
                        ParameterName.scatter_param_dict: scatter_param_dict,
                    }
                plotting_data_dict[tissue_name] = current_tissue_data_dict
            complete_plotting_data_dict_list.append(plotting_data_dict)
            this_col_len = len(current_flux_data_dict)
            x_ticks_list.append(list(range(this_col_len)))
            if preset_x_lim_list is not None:
                x_lim = preset_x_lim_list[row_index][col_index]
            else:
                x_lim = (-0.5, this_col_len - 0.5)
            x_lim_list.append(x_lim)
            if preset_y_lim_list is not None:
                y_lim = preset_y_lim_list[row_index][col_index]
            else:
                y_lim = None
            y_lim_list.append(y_lim)
            # y_lim_list.append((minimal_value * 1.2, maximal_value * 1.2))
            if preset_y_ticks_list is not None:
                y_ticks = preset_y_ticks_list[row_index][col_index]
            else:
                y_ticks = None
            y_ticks_list.append(y_ticks)
            y_tick_labels_list.append(Keywords.default)
            this_row_array_len_list.append(this_col_len)
            total_array_len_this_row += this_col_len
            if col_index == 0:
                # y_ticks = default_y_tick_list
                # y_tick_label = default_y_tick_label_list
                display_y_label = common_y_label
            else:
                # y_ticks = []
                # y_tick_label = None
                display_y_label = None
            if row_index != row_num - 1:
                x_tick_labels = None
            else:
                x_tick_labels = [
                    display_group_name_dict[group_name] if group_name in display_group_name_dict else group_name
                    for group_name in current_flux_data_dict.keys()
                ]
            x_tick_labels_list.append(x_tick_labels)
            display_y_label_list.append(display_y_label)
            display_x_label_list.append(None)
        unit_array_len_size = (ax_total_size.x - (this_row_axis_num - 1) * ax_interval.x) / total_array_len_this_row
        this_row_bottom_left = ax_total_bottom_left + \
                               Vector(0, (ax_row_size + ax_interval.y) * (row_num - row_index - 1))
        for current_array_len in this_row_array_len_list:
            this_ax_col_len = current_array_len * unit_array_len_size
            ax_size_list.append(Vector(this_ax_col_len, ax_row_size))
            ax_bottom_left_list.append(this_row_bottom_left)
            this_row_bottom_left = this_row_bottom_left + Vector(this_ax_col_len + ax_interval.x, 0)
    return ax_bottom_left_list, ax_size_list, complete_plotting_data_dict_list, flux_name_list, x_lim_list, \
        display_x_label_list, x_ticks_list, x_tick_labels_list, y_lim_list, display_y_label_list, y_ticks_list, \
        y_tick_labels_list


def colon_scatter_line_figure(
        ax_total_bottom_left, ax_total_size, ax_interval, final_flux_comparison_data_dict, flux_name_list,
        cell_line_name_list, default_y_tick_list, default_y_tick_label_list, marker_size, marker_color_list,
        scatter_param_dict):
    row_num = len(flux_name_list)
    col_num = len(cell_line_name_list)
    ax_size = (ax_total_size - Vector(col_num - 1, row_num - 1) * ax_interval) / Vector(col_num, row_num)

    ax_bottom_left_list = []
    ax_size_list = []
    display_x_label_list = []
    display_y_label_list = []
    x_lim_list = []
    x_ticks_list = []
    x_tick_labels_list = []
    y_lim_list = []
    y_ticks_list = []
    y_tick_labels_list = []
    complete_plotting_data_dict_list = []
    for row_index, flux_name in enumerate(flux_name_list):
        for col_index, cell_line_name in enumerate(cell_line_name_list):
            current_flux_data_dict = final_flux_comparison_data_dict[flux_name][cell_line_name]
            plotting_data_dict = {}
            maximal_value = 0
            minimal_value = 0
            for index, (glucose_level_key, current_glucose_data_list) in enumerate(current_flux_data_dict.items()):
                value_array = np.array(current_glucose_data_list)
                point_num = len(value_array)
                random_x_value = np.linspace(-0.5, 0.5, point_num) * 0.1 + index
                maximal_value = np.maximum(maximal_value, np.max(value_array))
                minimal_value = np.minimum(minimal_value, np.min(value_array))
                current_tissue_data_dict = {
                    ParameterName.x_value_array: random_x_value,
                    ParameterName.y_value_array: value_array,
                    ParameterName.marker_size: marker_size,
                    ParameterName.marker_color: [marker_color_list[index]],  # To avoid warning from matplotlib
                    ParameterName.scatter_param_dict: scatter_param_dict,
                }
                plotting_data_dict[glucose_level_key] = current_tissue_data_dict
            complete_plotting_data_dict_list.append(plotting_data_dict)
            this_col_len = len(current_flux_data_dict)
            x_ticks_list.append(list(range(this_col_len)))
            x_lim_list.append((-0.5, this_col_len - 0.5))
            y_lim_list.append((minimal_value * 1.2, maximal_value * 1.2))
            if col_index == 0:
                y_ticks = default_y_tick_list
                y_tick_label = default_y_tick_label_list
                display_y_label = flux_name
            else:
                y_ticks = []
                y_tick_label = None
                display_y_label = None
            if row_index != row_num - 1:
                x_tick_labels = None
                display_x_label = None
            else:
                x_tick_labels = list(current_flux_data_dict.keys())
                display_x_label = cell_line_name
            display_x_label_list.append(display_x_label)
            x_tick_labels_list.append(x_tick_labels)
            display_y_label_list.append(display_y_label)
            y_ticks_list.append(y_ticks)
            y_tick_labels_list.append(y_tick_label)

            current_bottom_left = ax_total_bottom_left + (ax_size + ax_interval) * Vector(
                col_index, row_num - row_index - 1)
            ax_bottom_left_list.append(current_bottom_left)
            ax_size_list.append(ax_size)
    return ax_bottom_left_list, ax_size_list, complete_plotting_data_dict_list, x_lim_list, display_x_label_list, \
        x_ticks_list, x_tick_labels_list, y_lim_list, display_y_label_list, y_ticks_list, y_tick_labels_list


def p_value_parameter_list_generator(
        p_value_x_value_list, p_value_y_value_list, p_value_list, x_lim, y_lim, p_value_cap_param_dict):
    cap_y_height = p_value_cap_param_dict.pop(ParameterName.height)
    cap_x_width = p_value_cap_param_dict.pop(ParameterName.width)
    text_y_offset = p_value_cap_param_dict.pop(ParameterName.text_y_offset)
    cap_y_offset = p_value_cap_param_dict.pop(ParameterName.cap_y_offset)

    if x_lim is None:
        x_lim = (0, 1)
    if y_lim is None:
        y_lim = (0, 1)

    if isinstance(p_value_y_value_list, (int, float)):
        p_value_y_value_list = it.repeat(p_value_y_value_list)
    elif isinstance(p_value_y_value_list, (list, tuple)):
        assert len(p_value_x_value_list) == len(p_value_y_value_list)
    else:
        raise ValueError()
    p_value_text_loc_list = []
    p_value_cap_start_end_list = []
    for x_value, y_value in zip(p_value_x_value_list, p_value_y_value_list):
        if y_value > 0.5:
            text_y_value = y_value + text_y_offset
            cap_horiz_y_value = y_value - cap_y_offset
            cap_vertical_y_value = cap_horiz_y_value - cap_y_height
        else:
            text_y_value = y_value - text_y_offset
            cap_horiz_y_value = y_value + cap_y_offset
            cap_vertical_y_value = cap_horiz_y_value + cap_y_height
        cap_horiz_y_value = y_lim[0] + cap_horiz_y_value * (y_lim[1] - y_lim[0])
        cap_vertical_y_value = y_lim[0] + cap_vertical_y_value * (y_lim[1] - y_lim[0])
        cap_horiz_left_x_value = x_value - cap_x_width / 2 * (x_lim[1] - x_lim[0])
        cap_horiz_right_x_value = x_value + cap_x_width / 2 * (x_lim[1] - x_lim[0])
        text_x_value = (x_value - x_lim[0]) / (x_lim[1] - x_lim[0])
        cap_start_end_x_y_pair = [
            [cap_horiz_left_x_value, cap_horiz_left_x_value, cap_horiz_right_x_value, cap_horiz_right_x_value],
            [cap_vertical_y_value, cap_horiz_y_value, cap_horiz_y_value, cap_vertical_y_value]
        ]
        p_value_cap_start_end_list.append([*cap_start_end_x_y_pair, p_value_cap_param_dict])
        p_value_text_loc_list.append(Vector(text_x_value, text_y_value))
    p_value_text_list = []
    for p_value in p_value_list:
        if p_value < 0.001:
            p_value_text = '<0.001'
        else:
            p_value_text = '{:.3f}'.format(p_value)
        p_value_text_list.append(p_value_text)
    return p_value_text_list, p_value_text_loc_list, p_value_cap_start_end_list


class FluxComparisonScatterDataFigure(BasicScatterDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        # ax_total_bottom_left = Vector(0.1, 0.06)
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left

        ax_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0.06, 0.06))
        common_y_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_label, None)
        common_x_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_x_label, None, pop=True)
        preset_y_lim_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_lim_list, None, pop=True)
        preset_y_ticks_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_ticks_list, None, pop=True)
        preset_x_lim_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.x_lim_list, None, pop=True)
        display_flux_name_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.display_flux_name_dict, {}, pop=True)
        display_group_name_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.display_group_name_dict, {}, pop=True)
        compare_one_by_one = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.compare_one_by_one, False, pop=True)
        column_width = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.column_width, 0.5, pop=True)
        class_width = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.class_width, 1, pop=True)
        marker_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.marker_size, 8, pop=True)
        new_figure_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_config_dict, {}, pop=True)
        complete_p_value_y_value_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.p_value_y_value_list, None, pop=True)
        p_value_cap_param_dict = {
            **DataFigureConfig.common_p_value_cap_parameter_dict,
            **default_parameter_extract(
                figure_data_parameter_dict, ParameterName.p_value_cap_parameter_dict,
                {}, pop=True)
        }
        supplementary_text_format_dict = {
            **DataFigureConfig.common_supplementary_text_config_dict,
            ParameterName.font_size: 5,
            ParameterName.width: 0.1,
            ParameterName.height: 0.05,
            **default_parameter_extract(
                figure_data_parameter_dict, ParameterName.supplementary_text_format_dict,
                {}, pop=True)
        }

        color_dict = figure_data_parameter_dict.pop(ParameterName.color_dict)
        text_axis_loc_pair = Vector(0.5, 1.08)
        flux_title_text_format_dict = {
            **DataFigureConfig.common_subplot_text_format_dict_generator(),
            # ParameterName.font_size: 9,
            ParameterName.font_size: 7,
        }

        final_flux_comparison_data_dict, scatter_line_figure = flux_comparison_data.return_data(
            **figure_data_parameter_dict)
        scatter_param_dict = {
            ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
        }
        scatter_line_param_dict = {
            **DataFigureConfig.common_line_param_dict_generator(),
            ParameterName.z_order: DataFigureConfig.line_z_order
        }
        figure_config_dict = {
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                {}, {
                    ParameterName.axis_label_distance: 0.04
                }, new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                {}, {
                    ParameterName.axis_tick_label_distance: 0.008
                }, new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                {}, {
                    ParameterName.axis_label_distance: 0.025
                }, new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.subplot_name_text_format_dict: flux_title_text_format_dict,
            ParameterName.error_bar_param_dict: {
                **DataFigureConfig.common_error_bar_param_dict_generator(),
                ParameterName.cap_size: 2.5,
                ParameterName.edge_width: 0.5,
                ParameterName.z_order: DataFigureConfig.error_bar_behind_z_order
            },
            ParameterName.line_param_dict: {
                **DataFigureConfig.common_line_param_dict_generator(),
                ParameterName.z_order: DataFigureConfig.line_z_order
            },
            ParameterName.supplementary_text_format_dict: supplementary_text_format_dict
        }
        try:
            with_scatter_line = figure_data_parameter_dict.pop(ParameterName.scatter_line)
        except KeyError:
            with_scatter_line = False

        flux_name_location_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        if common_y_label is None:
            common_y_label = 'Flux value'
        (
            ax_bottom_left_list, ax_size_list, complete_plotting_data_dict_list, flux_name_list, x_lim_list,
            display_x_label_list, x_ticks_list, x_tick_labels_list, y_lim_list, display_y_label_list, y_ticks_list,
            y_tick_labels_list, complete_scatter_line_list, complete_p_value_text_list, complete_p_value_text_loc_list
        ) = general_flux_layout_generator(
            ax_total_bottom_left, ax_total_size, ax_interval, final_flux_comparison_data_dict, flux_name_location_list,
            common_x_label, common_y_label, preset_y_lim_list, preset_y_ticks_list, preset_x_lim_list,
            display_group_name_dict, column_width, class_width, marker_size, color_dict, scatter_param_dict,
            compare_one_by_one=compare_one_by_one, with_scatter_line=with_scatter_line,
            scatter_line_param_dict=scatter_line_param_dict,
            complete_p_value_y_value_list=complete_p_value_y_value_list,
            p_value_cap_param_dict=p_value_cap_param_dict)
        subplot_name_list = [
            display_flux_name_dict[flux_name] if flux_name in display_flux_name_dict else flux_name
            for flux_name in flux_name_list]

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: complete_plotting_data_dict_list,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_lim_list: x_lim_list,
            ParameterName.x_label_list: display_x_label_list,
            ParameterName.x_ticks_list: x_ticks_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_lim_list: y_lim_list,
            ParameterName.y_label_list: display_y_label_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,

            ParameterName.legend: False,
            ParameterName.scatter_line: complete_scatter_line_list,
            ParameterName.subplot_name_list: subplot_name_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            ParameterName.supplementary_text_list: complete_p_value_text_list,
            ParameterName.supplementary_text_loc_list: complete_p_value_text_loc_list,
            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, **kwargs)


class EmbeddedSolutionScatterDataFigure(BasicScatterDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        ax_total_bottom_left = Vector(0.1, 0.1)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left

        marker_size = 0.8 * scale
        color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        embedded_flux_data_dict, *_ = embedded_flux_data.return_data(
            **figure_data_parameter_dict)

        common_text_config = {
            ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.width: GroupDataFigure.label_width,
            ParameterName.height: GroupDataFigure.label_height,
        }
        figure_config_dict = {
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: GroupDataFigure.adjacent_y_label_distance,
                **common_text_config
            },
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: GroupDataFigure.adjacent_x_label_distance,
                **common_text_config
            }
        }

        complete_data_dict = {}
        x_min = y_min = np.inf
        x_max = y_max = -np.inf
        x_value_array_list = []
        y_value_array_list = []
        marker_color_list = []
        for data_label, embedded_flux_array in embedded_flux_data_dict.items():
            x_value_array = embedded_flux_array[:, 0]
            y_value_array = embedded_flux_array[:, 1]
            x_min = np.minimum(x_min, np.min(x_value_array))
            x_max = np.maximum(x_max, np.max(x_value_array))
            y_min = np.minimum(y_min, np.min(y_value_array))
            y_max = np.maximum(y_max, np.max(y_value_array))
            current_label_data_dict = {
                ParameterName.x_value_array: x_value_array,
                ParameterName.y_value_array: y_value_array,
                ParameterName.marker_size: marker_size,
                ParameterName.marker_color: [color_dict[data_label]],  # To avoid warning from matplotlib
                ParameterName.scatter_param_dict: {
                    ParameterName.alpha: 0.8,
                    ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
                }
            }
            complete_data_dict[data_label] = current_label_data_dict
            x_value_array_list.append(x_value_array)
            y_value_array_list.append(y_value_array)
            marker_color_list.extend([color_dict[data_label]] * len(x_value_array))

        current_tissue_data_dict = {
            ParameterName.x_value_array: np.concatenate(x_value_array_list),
            ParameterName.y_value_array: (np.concatenate(y_value_array_list), None),
            ParameterName.marker_size: marker_size,
            ParameterName.marker_color: marker_color_list,  # To avoid warning from matplotlib
            ParameterName.scatter_param_dict: {
                ParameterName.alpha: 0.8,
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
            },
        }
        x_lim = Vector(x_min, x_max) + Vector(-1, 1) * 0.1 * (x_max - x_min)
        y_lim = Vector(y_min, y_max) + Vector(-1, 1) * 0.1 * (y_max - y_min)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: None,
            ParameterName.data_nested_list: [current_tissue_data_dict],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_lim_list: [x_lim],
            ParameterName.x_ticks_list: [[]],
            ParameterName.x_label_list: ['PC 1'],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_ticks_list: [[]],
            ParameterName.y_label_list: ['PC 2'],

            ParameterName.legend: False,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)


class AccuracyVariationScatterDataFigure(BasicScatterDataFigure):
    class Config(object):
        edge_width = 0.9
        marker_size = 2.5

        common_line_param_dict = {
            **DataFigureConfig.common_line_param_dict_generator(),
            ParameterName.edge_width: edge_width,
            ParameterName.z_order: DataFigureConfig.line_z_order,
        }
        connect_line_param_dict = {
            **common_line_param_dict,
            ParameterName.edge_color: ColorConfig.orange,
        }
        dash_line_param_dict = {
            **common_line_param_dict,
            ParameterName.edge_style: LineStyle.thin_dash,
            ParameterName.edge_color: ColorConfig.medium_blue,
        }
        scatter_param_dict = {
            ParameterName.alpha: 0.8,
            ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
        }

    @staticmethod
    def x_value_mapping(mode, raw_x_value):
        if mode == ParameterName.selection_ratio:
            return -np.log10(raw_x_value)
        elif mode == ParameterName.optimized_size:
            return np.log10(raw_x_value / 100)
        else:
            raise ValueError()

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, scale=1, **kwargs):
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left

        selection_ratio_minimal_selected_size = 50
        # minimal_selection_ratio = 50 / 10000
        minimal_selection_ratio = 0
        target_selection_ratio_in_optimized_size = 1 / 100

        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, ParameterName.selection_ratio)
        marker_color = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.marker_color, ColorConfig.normal_blue)
        y_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_labels_list, Keywords.default)
        data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, None)

        basic_num_array = np.array([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000])
        if mode == ParameterName.selection_ratio:
            mean_or_std = ParameterName.mean
            default_y_label = CommonFigureString.mean
            default_x_label = CommonFigureString.selection_ratio_m_over_n
            raw_x_ticks = 1 / basic_num_array
            x_tick_labels = ['1$^{-1}$'] + [f'{basic_num}' r'$^{-1}$' for basic_num in basic_num_array[1:]]
            all_data_y_lim = [0, 450]
            all_data_y_ticks = [0, 100, 200, 300, 400]
            all_data_raw_threshold = ProtocolSearchingMaterials.all_data_target_selection_ratio
            experimental_data_y_lim = [0, 600]
            experimental_y_ticks = [0, 200, 400, 600]
            experimental_data_raw_threshold = ProtocolSearchingMaterials.experimental_data_target_selection_ratio
            x_lim = [-0.1, 3.1]
            x_tick_label_format_dict = {
                ParameterName.axis_tick_label_distance: 0.003,
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
                ParameterName.text_box: False,
                ParameterName.height: 0.015,
            }
        else:
            mean_or_std = ParameterName.std
            default_y_label = CommonFigureString.std
            default_x_label = CommonFigureString.optimization_size_n
            raw_x_ticks = 100 * basic_num_array[:-1]
            x_tick_labels = [str(x_tick) for x_tick in raw_x_ticks]
            all_data_y_lim = [0, 140]
            # all_data_y_ticks = [0, 20, 40, 60, 80, 100]
            all_data_y_ticks = np.arange(*all_data_y_lim, 30)
            all_data_raw_threshold = ProtocolSearchingMaterials.all_data_target_optimization_size
            experimental_data_y_lim = [0, 150.001]
            experimental_y_ticks = np.arange(*experimental_data_y_lim, 30)
            experimental_data_raw_threshold = ProtocolSearchingMaterials.experimental_data_target_optimization_size
            x_lim = [-0.1, 2.8]
            x_tick_label_format_dict = {
                ParameterName.axis_tick_label_distance: 0.005,
                ParameterName.height: 0.02,
            }
        x_ticks = self.x_value_mapping(mode, raw_x_ticks)
        y_label = default_parameter_extract(figure_data_parameter_dict, ParameterName.y_label_list, default_y_label)
        x_label = default_parameter_extract(figure_data_parameter_dict, ParameterName.x_label_list, default_x_label)
        (
            data_matrix, data_lim_pair, data_value_text_format, analyzed_set_size_list, selected_min_loss_size_list
        ) = raw_model_data.return_heatmap_data(**figure_data_parameter_dict, mean_or_std=mean_or_std)
        value_index_dict = {}
        for analyzed_set_index, analyzed_size in enumerate(analyzed_set_size_list):
            for selected_size_index, selected_size in enumerate(selected_min_loss_size_list):
                current_selection_ratio = selected_size / analyzed_size
                current_matrix_value = data_matrix[selected_size_index][analyzed_set_index]
                if np.isnan(current_matrix_value):
                    continue
                if mode == ParameterName.selection_ratio:
                    if selected_size >= selection_ratio_minimal_selected_size:
                        if current_selection_ratio >= minimal_selection_ratio:
                            x_location = self.x_value_mapping(mode, current_selection_ratio)
                            # x_location = x_value_mapping_dict[current_selection_ratio]
                            if x_location not in value_index_dict:
                                value_index_dict[x_location] = []
                            value_index_dict[x_location].append(current_matrix_value)
                elif mode == ParameterName.optimized_size:
                    if current_selection_ratio == target_selection_ratio_in_optimized_size:
                        x_location = self.x_value_mapping(mode, analyzed_size)
                        # x_location = x_value_mapping_dict[analyzed_size]
                        if analyzed_size not in value_index_dict:
                            value_index_dict[x_location] = []
                        value_index_dict[x_location].append(current_matrix_value)
                else:
                    raise ValueError()

        label_text_config = {
            ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.width: GroupDataFigure.label_width,
            ParameterName.height: GroupDataFigure.label_height,
        }
        tick_label_text_config = {
            ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size - 1,
            ParameterName.width: GroupDataFigure.tick_label_width,
        }
        figure_config_dict = {
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.035,
                **label_text_config
            },
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.02,
                **label_text_config
            },
            ParameterName.x_tick_label_format_dict: {
                **x_tick_label_format_dict,
                **tick_label_text_config
            },
            ParameterName.y_tick_label_format_dict: {
                ParameterName.axis_tick_label_distance: 0.007,
                **tick_label_text_config
            },
        }

        marker_size = self.Config.marker_size
        marker_size_list = []
        data_point_x_value_list = []
        data_point_y_value_list = []
        scatter_line_x_value_list = []
        scatter_line_y_value_list = []
        scatter_line_pair_list = []
        max_y_value = 0
        for current_x_value, current_y_value_list in value_index_dict.items():
            data_value_num = len(current_y_value_list)
            for current_y_value in current_y_value_list:
                data_point_x_value_list.append(current_x_value)
                data_point_y_value_list.append(current_y_value)
                max_y_value = max(current_y_value, max_y_value)
            marker_size_list.extend([marker_size] * data_value_num)
            scatter_line_x_value_list.append(current_x_value)
            if mode == ParameterName.selection_ratio:
                mean_y_value = np.mean(current_y_value_list)
                data_point_x_value_list.append(current_x_value)
                data_point_y_value_list.append(mean_y_value)
                marker_size_list.append(0)
                scatter_line_y_value_list.append(mean_y_value)
                scatter_line_pair_list.append((current_x_value, mean_y_value))
            elif mode == ParameterName.optimized_size:
                scatter_line_y_value_list.append(current_y_value_list[0])
                scatter_line_pair_list.append((current_x_value, current_y_value_list[0]))
            else:
                raise ValueError()
        if data_name == DataName.raw_model_all_data:
            y_lim = all_data_y_lim
            y_ticks = all_data_y_ticks
            x_threshold = self.x_value_mapping(mode, all_data_raw_threshold)
        elif data_name == DataName.raw_model_raw_data:
            y_lim = experimental_data_y_lim
            y_ticks = experimental_y_ticks
            x_threshold = self.x_value_mapping(mode, experimental_data_raw_threshold)
        else:
            raise ValueError()
        scatter_line_pair_list.sort(key=lambda x: x[0])
        threshold_dash_line_list = [(x_threshold, x_threshold), y_lim]

        scatter_line_list = [[i for i in zip(*scatter_line_pair_list)], threshold_dash_line_list]
        # This copy is necessary to prevent modification by scale
        line_param_dict_list = [dict(self.Config.connect_line_param_dict), dict(self.Config.dash_line_param_dict)]

        current_data_dict = {
            ParameterName.x_value_array: np.array(data_point_x_value_list),
            ParameterName.y_value_array: (np.array(data_point_y_value_list), None),
            ParameterName.marker_size: np.array(marker_size_list),
            ParameterName.marker_color: [marker_color],  # To avoid warning from matplotlib
            ParameterName.scatter_param_dict: {**self.Config.scatter_param_dict},  # This copy is necessary to
                                                                                   # prevent modification by scale
        }
        figure_config_dict[ParameterName.line_param_dict] = line_param_dict_list

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: None,
            ParameterName.data_nested_list: [current_data_dict],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_lim_list: [x_lim],
            ParameterName.x_ticks_list: [x_ticks],
            ParameterName.x_label_list: [x_label],
            ParameterName.x_tick_labels_list: [x_tick_labels],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_ticks_list: [y_ticks],
            ParameterName.y_tick_labels_list: [y_tick_labels],
            ParameterName.y_label_list: [y_label],

            ParameterName.scatter_line: [scatter_line_list],

            ParameterName.legend: False,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)

