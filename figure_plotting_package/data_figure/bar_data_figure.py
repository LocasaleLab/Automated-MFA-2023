from .config import (
    DataFigureConfig, ParameterName, Vector, it, Keywords, merge_axis_format_dict, np,
    mid_carbon_num_dict, common_legend_generator, default_parameter_extract, CommonElementConfig,
    net_flux_x_axis_labels_generator, ColorConfig, LineStyle, merge_complete_config_dict, expand_one_axis_dict,
    HorizontalAlignment, VerticalAlignment
)
from .data_figure_plotting_and_data_output_generator import draw_text_by_axis_loc, single_bar_plotting

from .data_figure import DataFigure


GroupDataFigure = DataFigureConfig.GroupDataFigure


class BarConfig(object):
    distance_x_y_label_font_size = 10
    distance_x_y_tick_label_font_size = 7


class BasicBarDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        (
            ax_bottom_left_list,
            ax_size_list,
            color_dict,
            self.complete_data_dict_list,
            self.array_len_list,
            new_figure_config_dict
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.color_dict,
            ParameterName.data_nested_list,
            ParameterName.array_len_list,
            ParameterName.figure_config_dict,
        ]]
        self.color_dict = color_dict
        twin_x_axis = default_parameter_extract(figure_data_parameter_dict, ParameterName.twin_x_axis, False)
        broken_y_axis = default_parameter_extract(figure_data_parameter_dict, ParameterName.broken_y_axis, None)

        (
            axis_format_dict, axis_tick_format_dict, axis_label_format_dict
        ) = DataFigureConfig.common_axis_param_dict_generator(scale)
        figure_config_dict = {
            **{
                key: new_figure_config_dict[key] for key in [
                    ParameterName.column_width, ParameterName.edge, ParameterName.cutoff_param_dict,
                    ParameterName.bar_param_dict, ParameterName.error_bar_param_dict,
                    ParameterName.scatter_param_dict, ParameterName.subplot_name_text_format_dict,
                    ParameterName.x_tick_separator_format_dict, ParameterName.x_tick_separator_label_format_dict,
                    ParameterName.y_tick_separator_format_dict, ParameterName.y_tick_separator_label_format_dict,
                    ParameterName.supplementary_text_format_dict,
                ] if key in new_figure_config_dict
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }

        (
            self.subplot_name_list,
            self.text_axis_loc_pair,
            self.max_bar_num_each_group,
        ) = default_parameter_extract(figure_data_parameter_dict, [
                ParameterName.subplot_name_list,
                ParameterName.text_axis_loc_pair,
                ParameterName.max_bar_num_each_group,
            ], None, repeat_default_value=True)
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
            )]

        self.tick_separator_dict_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.tick_separator_dict_list, it.repeat({}))

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
            twin_x_axis=twin_x_axis, broken_y_axis=broken_y_axis, **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        ax_and_transform_list = super().draw(fig, parent_ax, parent_transformation)
        for (
                (current_mid_array_data_dict, current_mid_error_bar_data_dict, *current_raw_scatter_data_dict_list),
                (current_ax, current_transform), array_len, cutoff_value,
                y_label, y_lim, x_label, x_tick_label_list, y_ticks, y_tick_label_list, tick_separator_dict) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.array_len_list,
                self.cutoff_value_list, self.y_label_list, self.y_lim_list,
                self.x_label_list, self.x_tick_labels_list, self.y_ticks_list, self.y_tick_labels_list,
                self.tick_separator_dict_list):
            if len(current_raw_scatter_data_dict_list) > 0:
                current_raw_scatter_data_dict = current_raw_scatter_data_dict_list[0]
            else:
                current_raw_scatter_data_dict = None
            single_bar_plotting(
                current_ax, current_transform, current_mid_array_data_dict, current_mid_error_bar_data_dict,
                array_len, self.figure_config_dict, y_lim=y_lim, y_ticks=y_ticks, cutoff_value=cutoff_value,
                color_dict=self.color_dict, x_label=x_label, x_tick_labels=x_tick_label_list, y_label=y_label,
                y_tick_labels=y_tick_label_list, twin_x_axis=self.twin_x_axis, broken_y_axis=self.broken_y_axis,
                max_bar_num_each_group=self.max_bar_num_each_group,
                current_raw_scatter_data_dict=current_raw_scatter_data_dict, **tick_separator_dict)
        if self.subplot_name_list is not None:
            # for subplot_name, (current_ax, current_transform) in zip(self.subplot_name_list, ax_and_transform_list):
            for subplot_name, (current_ax, current_transform) in zip(
                    self.subplot_name_list, self.hidden_data_axes_transform_list):
                draw_text_by_axis_loc(
                    current_ax, subplot_name, self.text_axis_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.subplot_name_text_format_dict])
        if self.supplementary_text_list is not None:
            for supplementary_text, supplementary_loc, (current_ax, current_transform) in zip(
                    self.supplementary_text_list, self.supplementary_text_loc_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, supplementary_text, supplementary_loc, current_transform,
                    **self.figure_config_dict[ParameterName.supplementary_text_format_dict])


class BasicMIDComparisonGridBarDataFigure(BasicBarDataFigure):
    # ax_total_bottom_left = Vector(0.05, 0.03)
    ax_total_bottom_left = Vector(0, 0)
    ax_total_size = Vector(1, 1) - ax_total_bottom_left
    ax_interval = Vector(0.015, 0.03)        # (horizontal, vertical)
    each_row_figure_height = 0.185

    @staticmethod
    def calculate_height(self, row_num):
        return self.each_row_figure_height * row_num + (row_num - 1) * self.ax_interval.y

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, **kwargs):
        absolute_total_size = size
        ax_interval = self.ax_interval / absolute_total_size
        ax_row_size = self.each_row_figure_height / absolute_total_size.y
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = self.ax_total_size / absolute_total_size
        ax_total_width = 1
        default_y_tick_label_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.default_y_tick_label_list,
            ['0.00', '0.25', '0.50', '0.75', '1.00']
        )
        default_y_tick_list = [float(y_tick_label) for y_tick_label in default_y_tick_label_list]
        common_y_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_label, 'Relative ratio')

        x_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.x_tick_label_format_dict_generator(scale),
            {ParameterName.axis_tick_label_distance: 0.005 * scale},
            figure_data_parameter_dict, ParameterName.x_tick_label_format_dict, pop=True)
        y_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_label_format_dict_generator(scale),
            {ParameterName.axis_label_distance: 0.04 * scale},
            figure_data_parameter_dict, ParameterName.y_label_format_dict, pop=True)
        y_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_tick_label_format_dict_generator(scale),
            {ParameterName.axis_tick_label_distance: 0.008 * scale},
            figure_data_parameter_dict, ParameterName.y_tick_label_format_dict, pop=True)
        bar_param_dict = merge_axis_format_dict(
            {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            {},
            figure_data_parameter_dict, ParameterName.bar_param_dict, pop=True
        )
        error_bar_param_dict = merge_axis_format_dict(
            DataFigureConfig.common_error_bar_param_dict_generator(scale),
            {},
            figure_data_parameter_dict, ParameterName.error_bar_param_dict, pop=True
        )
        raw_data_scatter_param_dict = {
            ParameterName.marker_size: 0.2, }
        text_axis_loc_pair = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.text_axis_loc_pair, Vector(0.5, 0.9), pop=True)
        subplot_name_text_format_dict = merge_axis_format_dict(
            DataFigureConfig.common_subplot_text_format_dict_generator(scale),
            {},
            figure_data_parameter_dict, ParameterName.subplot_name_text_format_dict, pop=True)
        specific_figure_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_config_dict, {}, pop=True)
        general_figure_config_dict = {
            ParameterName.column_width: 0.5,
            ParameterName.edge: 0.05,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.y_label_format_dict: y_label_format_dict,
            ParameterName.y_tick_label_format_dict: y_tick_label_format_dict,
            ParameterName.bar_param_dict: bar_param_dict,
            ParameterName.error_bar_param_dict: error_bar_param_dict,
            ParameterName.scatter_param_dict: raw_data_scatter_param_dict,
            ParameterName.subplot_name_text_format_dict: subplot_name_text_format_dict,
        }
        complete_figure_config_dict = merge_complete_config_dict(
            general_figure_config_dict, specific_figure_config_dict)
        color_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.color_dict, None, force=True, pop=True)
        legend = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.legend, False, pop=True)

        mid_name_location_array_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.mid_name_list, None, force=True, pop=True)
        mean_data_dict, error_bar_data_dict, *all_data_point_dict_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_data, None, force=True, pop=True)
        if len(all_data_point_dict_list) > 0:
            all_data_point_dict = all_data_point_dict_list[0]
        else:
            all_data_point_dict = None
        subplot_name_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_dict, {}, pop=True)
        array_len_list = []
        mid_name_data_error_bar_array_dict_pair_list = []
        subplot_name_list = []
        ax_bottom_left_list = []
        ax_size_list = []
        row_num = len(mid_name_location_array_list)
        y_label_list = []
        x_tick_labels_list = []
        y_tick_labels_list = []
        y_ticks_list = []
        for row_index, row_list in enumerate(mid_name_location_array_list):
            total_array_len_this_row = 0
            this_row_array_len_list = []
            this_row_axis_num = len(row_list)
            for col_index, mid_name in enumerate(row_list):
                if isinstance(mid_name, str) and mid_name in mean_data_dict:
                    mean_mid_array_dict = mean_data_dict[mid_name]
                    array_len = None
                    for mid_array in mean_mid_array_dict.values():
                        if mid_array is not None:
                            array_len = len(mid_array)
                            break
                    if len(mean_mid_array_dict) > 1:
                        mid_array_revised_dict = {
                            color_class_key: mean_mid_array_dict[color_class_key]
                            for color_class_key in color_dict.keys()
                            if color_class_key in mean_mid_array_dict
                        }
                    else:
                        mid_array_revised_dict = mean_mid_array_dict
                    if error_bar_data_dict is not None:
                        error_bar_array_dict = error_bar_data_dict[mid_name]
                    else:
                        error_bar_array_dict = None
                    if all_data_point_dict is not None:
                        all_data_point_array_dict = all_data_point_dict[mid_name]
                    else:
                        all_data_point_array_dict = None
                    mid_name_data_error_bar_array_dict_pair_list.append(
                        (mid_array_revised_dict, error_bar_array_dict, all_data_point_array_dict))
                    if mid_name in subplot_name_dict:
                        subplot_name = subplot_name_dict[mid_name]
                    else:
                        subplot_name = mid_name
                    subplot_name_list.append(subplot_name)
                elif mid_name is None or isinstance(mid_name, int) or mid_name not in mean_data_dict:
                    if isinstance(mid_name, int):
                        array_len = mid_name
                    elif mid_name in mid_carbon_num_dict:
                        array_len = mid_carbon_num_dict[mid_name]
                    elif mid_name is None:
                        array_len = 5
                    else:
                        array_len = None
                        for short_mid_name in mid_carbon_num_dict.keys():
                            if short_mid_name in mid_name:
                                array_len = mid_carbon_num_dict[short_mid_name]
                                break
                        if array_len is None:
                            raise ValueError(f'Length of MID {mid_name} cannot be found!')
                    mid_name_data_error_bar_array_dict_pair_list.append((None, None, None))
                    subplot_name_list.append(None)
                else:
                    raise ValueError()
                array_len_list.append(array_len)
                this_row_array_len_list.append(array_len)
                total_array_len_this_row += array_len
                x_tick_labels_list.append([f'm+{mid_index}' for mid_index in range(array_len)])
                if col_index == 0:
                    y_label_list.append(common_y_label)
                    y_tick_labels_list.append(default_y_tick_label_list)
                else:
                    y_label_list.append(None)
                    y_tick_labels_list.append(None)
                y_ticks_list.append(default_y_tick_list)
            unit_array_len_size = (ax_total_width - (this_row_axis_num - 1) * ax_interval.x) / total_array_len_this_row
            this_row_bottom_left = ax_total_bottom_left + \
                Vector(0, (ax_row_size + ax_interval.y) * (row_num - row_index - 1))
            for current_array_len in this_row_array_len_list:
                this_ax_col_len = current_array_len * unit_array_len_size
                ax_size_list.append(Vector(this_ax_col_len, ax_row_size))
                ax_bottom_left_list.append(this_row_bottom_left)
                this_row_bottom_left = this_row_bottom_left + Vector(this_ax_col_len + ax_interval.x, 0)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: mid_name_data_error_bar_array_dict_pair_list,
            ParameterName.array_len_list: array_len_list,
            ParameterName.figure_config_dict: complete_figure_config_dict,

            ParameterName.subplot_name_list: subplot_name_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,

            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_lim_list: it.repeat((0, 1)),
            ParameterName.y_label_list: y_label_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,

            ParameterName.legend: legend,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)


class BasicFluxErrorBarDataFigure(BasicBarDataFigure):
    class Config(object):
        sensitivity_x_y_tick_label_font_size = 7

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        (
            ax_bottom_left_list, ax_size_list, data_nested_list, color_dict, common_flux_name_list
        ) = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.ax_bottom_left_list, ParameterName.ax_size_list,
                ParameterName.data_nested_list, ParameterName.color_dict, ParameterName.flux_name_list],
            None, pop=True, repeat_default_value=True, force=True)
        with_glns_m = default_parameter_extract(figure_data_parameter_dict, ParameterName.with_glns_m, False)
        (
            common_y_lim, y_ticks, y_label, y_tick_labels, broken_y_axis_ratio, cutoff_value_list
        ) = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.common_y_lim,
                ParameterName.y_ticks_list,
                ParameterName.common_y_label,
                ParameterName.default_y_tick_label_list,
                ParameterName.broken_y_axis,
                ParameterName.cutoff],
            None, pop=True, repeat_default_value=True)

        total_ax_num = len(ax_bottom_left_list)

        (
            x_tick_labels, pathway_separator_location_array, pathway_name_location_array, pathway_name_list
        ) = net_flux_x_axis_labels_generator(common_flux_name_list, with_glns_m=with_glns_m)
        specific_tick_separator_dict = {
            ParameterName.x_tick_separator_locs: pathway_separator_location_array,
            ParameterName.x_tick_separator_labels: pathway_name_list,
            ParameterName.x_tick_separator_label_locs: pathway_name_location_array,
        }
        x_tick_label_list = [None] * (total_ax_num - 1) + [x_tick_labels]
        x_tick_separator_dict_list = [{}] * (total_ax_num - 1) + [specific_tick_separator_dict]

        x_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.flux_x_tick_format_dict,
            {ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size},
            figure_data_parameter_dict, ParameterName.x_tick_label_format_dict)
        x_tick_separator_format_dict = merge_axis_format_dict(
            DataFigureConfig.flux_x_tick_separator_format_dict,
            {},
            figure_data_parameter_dict, ParameterName.x_tick_separator_format_dict)
        x_tick_separator_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.flux_x_tick_separator_label_format_dict,
            {ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size},
            figure_data_parameter_dict, ParameterName.x_tick_separator_label_format_dict)
        y_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_label_format_dict_generator(),
            {
                ParameterName.axis_label_distance: 0.04,
                ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size},
            figure_data_parameter_dict, ParameterName.y_label_format_dict)
        y_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_tick_label_format_dict_generator(),
            {ParameterName.axis_tick_label_distance: 0.008},
            figure_data_parameter_dict, ParameterName.y_tick_label_format_dict)

        cutoff_format_dict = {
            ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio,
            ParameterName.edge_color: ColorConfig.normal_blue,
            ParameterName.z_order: DataFigureConfig.line_z_order,
            ParameterName.edge_style: LineStyle.thin_dash,
        }

        general_subplot_name_text_format_dict = DataFigureConfig.common_subplot_text_format_dict_generator()
        specific_subplot_name_text_format_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_text_format_dict,
            {})
        subplot_name_text_format_dict = merge_complete_config_dict(
            general_subplot_name_text_format_dict, specific_subplot_name_text_format_dict)

        figure_config_dict = {
            ParameterName.column_width: 0.5,
            ParameterName.edge: 0.05,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.y_label_format_dict: y_label_format_dict,
            ParameterName.y_tick_label_format_dict: y_tick_label_format_dict,
            ParameterName.bar_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(),
            ParameterName.cutoff_param_dict: cutoff_format_dict,
            ParameterName.x_tick_separator_format_dict: x_tick_separator_format_dict,
            ParameterName.x_tick_separator_label_format_dict: x_tick_separator_label_format_dict,
            ParameterName.subplot_name_text_format_dict: subplot_name_text_format_dict,
        }

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: data_nested_list,
            ParameterName.array_len_list: it.repeat(len(common_flux_name_list)),
            ParameterName.figure_config_dict: figure_config_dict,
            ParameterName.cutoff: it.repeat(cutoff_value_list),

            ParameterName.x_tick_labels_list: x_tick_label_list,
            ParameterName.tick_separator_dict_list: x_tick_separator_dict_list,
            ParameterName.y_lim_list: it.repeat(common_y_lim),
            ParameterName.y_label_list: it.repeat(y_label),
            ParameterName.y_ticks_list: it.repeat(y_ticks),
            ParameterName.y_tick_labels_list: it.repeat(y_tick_labels),

            ParameterName.legend: False,
            ParameterName.broken_y_axis: broken_y_axis_ratio,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class BasicSingleBarDataFigure(BasicBarDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        array_len = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.array_len_list, None, force=True, pop=True)

        x_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.x_label_format_dict_generator(),
            {
                ParameterName.axis_label_distance: 0.03,
                ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size},
            figure_data_parameter_dict, ParameterName.x_label_format_dict)
        x_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.x_tick_label_format_dict_generator(),
            {ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size},
            figure_data_parameter_dict, ParameterName.x_tick_label_format_dict)
        y_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_label_format_dict_generator(),
            {
                ParameterName.axis_label_distance: 0.05,
                ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size},
            figure_data_parameter_dict, ParameterName.y_label_format_dict)
        y_tick_label_format_dict = merge_axis_format_dict(
            DataFigureConfig.y_tick_label_format_dict_generator(),
            {ParameterName.axis_tick_label_distance: 0.008},
            figure_data_parameter_dict, ParameterName.y_tick_label_format_dict)

        general_figure_config_dict = {
            ParameterName.column_width: 0.5,
            ParameterName.edge: 0.05,
            ParameterName.x_label_format_dict: x_label_format_dict,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.y_label_format_dict: y_label_format_dict,
            ParameterName.y_tick_label_format_dict: y_tick_label_format_dict,
            ParameterName.bar_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(),
            ParameterName.supplementary_text_format_dict: {
                **CommonElementConfig.common_text_config,
                ParameterName.font_size: 10,
                ParameterName.width: 0.05,
                ParameterName.height: 0.05,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            }
        }
        specific_figure_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_config_dict, {}, pop=True)
        complete_figure_config_dict = merge_complete_config_dict(
            general_figure_config_dict, specific_figure_config_dict)
        expanded_axis_parameter_dict = expand_one_axis_dict(figure_data_parameter_dict)
        figure_data_parameter_dict = {
            ParameterName.array_len_list: [array_len],
            ParameterName.figure_config_dict: complete_figure_config_dict,

            **expanded_axis_parameter_dict,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)
