from ..config import DataFigureConfig, ParameterName, Vector, it, Keywords, merge_axis_format_dict, np, \
    mid_carbon_num_dict, CommonFigureMaterials, common_legend_generator, default_parameter_extract, \
    sensitivity_heatmap_x_axis_labels_generator, DataName, ColorConfig, LineStyle, CommonFigureString
from ..config import HorizontalAlignment, VerticalAlignment
from ...common_functions import initialize_vector_input, symmetrical_lim_tick_generator_with_zero
from .figure_data_loader import mid_comparison_data, embedded_flux_data, raw_model_data
from .data_figure_plotting_and_data_output_generator import draw_text_by_axis_loc, single_bar_plotting

from .data_figure import DataFigure


GroupDataFigure = DataFigureConfig.GroupDataFigure
common_data_label = ''


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
                    ParameterName.subplot_name_text_format_dict,
                    ParameterName.x_tick_separator_format_dict, ParameterName.x_tick_separator_label_format_dict,
                    ParameterName.y_tick_separator_format_dict, ParameterName.y_tick_separator_label_format_dict,
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
                (current_mid_array_data_dict, current_mid_error_bar_data_dict),
                (current_ax, current_transform), array_len, cutoff_value,
                y_label, y_lim, x_label, x_tick_label_list, y_ticks, y_tick_label_list, tick_separator_dict) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.array_len_list,
                self.cutoff_value_list, self.y_label_list, self.y_lim_list,
                self.x_label_list, self.x_tick_labels_list, self.y_ticks_list, self.y_tick_labels_list,
                self.tick_separator_dict_list):
            single_bar_plotting(
                current_ax, current_transform, current_mid_array_data_dict, current_mid_error_bar_data_dict,
                array_len, self.figure_config_dict, y_lim=y_lim, y_ticks=y_ticks, cutoff_value=cutoff_value,
                color_dict=self.color_dict, x_label=x_label, x_tick_labels=x_tick_label_list, y_label=y_label,
                y_tick_labels=y_tick_label_list, twin_x_axis=self.twin_x_axis, broken_y_axis=self.broken_y_axis,
                max_bar_num_each_group=self.max_bar_num_each_group, **tick_separator_dict)
        if self.subplot_name_list is not None:
            # for subplot_name, (current_ax, current_transform) in zip(self.subplot_name_list, ax_and_transform_list):
            for subplot_name, (current_ax, current_transform) in zip(
                    self.subplot_name_list, self.hidden_data_axes_transform_list):
                draw_text_by_axis_loc(
                    current_ax, subplot_name, self.text_axis_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.subplot_name_text_format_dict])


class MIDComparisonGridBarDataFigure(BasicBarDataFigure):
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
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        absolute_total_size = initialize_vector_input(size)
        ax_interval = self.ax_interval / absolute_total_size
        ax_row_size = self.each_row_figure_height / absolute_total_size.y
        # ax_total_bottom_left = self.ax_total_bottom_left / absolute_total_size
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = self.ax_total_size / absolute_total_size
        ax_total_width = 1
        default_y_tick_label_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.default_y_tick_label_list,
            ['0.00', '0.25', '0.50', '0.75', '1.00']
        )
        default_y_tick_list = [float(y_tick_label) for y_tick_label in default_y_tick_label_list]

        x_tick_label_format_dict = DataFigureConfig.x_tick_label_format_dict_generator(scale)
        x_tick_label_format_dict[ParameterName.axis_tick_label_distance] = 0.005 * scale
        y_label_format_dict = DataFigureConfig.y_label_format_dict_generator(scale)
        y_label_format_dict[ParameterName.axis_label_distance] = 0.04 * scale
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_format_dict_generator(scale)
        y_tick_label_format_dict[ParameterName.axis_tick_label_distance] = 0.008 * scale

        text_axis_loc_pair = Vector(0.5, 0.9)
        subplot_name_text_format_dict = DataFigureConfig.common_subplot_text_format_dict_generator(scale)
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
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(scale),
            ParameterName.subplot_name_text_format_dict: subplot_name_text_format_dict,
        }

        if ParameterName.color_dict in figure_data_parameter_dict:
            color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        else:
            color_dict = CommonFigureMaterials.mid_comparison_color_dict

        mid_name_location_array_list = figure_data_parameter_dict[ParameterName.mid_name_list]
        mean_data_dict, error_bar_data_dict = mid_comparison_data.return_data(**figure_data_parameter_dict)
        array_len_list = []
        mid_name_data_error_bar_array_dict_pair_list = []
        mid_name_list = []
        ax_bottom_left_list = []
        ax_size_list = []
        row_num = len(mid_name_location_array_list)
        # ax_row_size = (ax_total_size.y - (row_num - 1) * ax_interval.y) / row_num
        total_height = self.calculate_height(self, row_num)
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
                    mid_array_dict = mean_data_dict[mid_name]
                    array_len = len(mid_array_dict.values().__iter__().__next__())
                    error_bar_array_dict = error_bar_data_dict[mid_name]
                    if len(mid_array_dict) > 1:
                        mid_array_revised_dict = {
                            color_class_key: mid_array_dict[color_class_key]
                            for color_class_key in color_dict.keys()
                            if color_class_key in mid_array_dict
                        }
                    else:
                        mid_array_revised_dict = mid_array_dict
                    mid_name_data_error_bar_array_dict_pair_list.append((mid_array_revised_dict, error_bar_array_dict))
                    mid_name_list.append(mid_name)
                elif isinstance(mid_name, int) or mid_name not in mean_data_dict:
                    if isinstance(mid_name, int):
                        array_len = mid_name
                    elif mid_name in mid_carbon_num_dict:
                        array_len = mid_carbon_num_dict[mid_name]
                    else:
                        array_len = None
                        for short_mid_name in mid_carbon_num_dict.keys():
                            if short_mid_name in mid_name:
                                array_len = mid_carbon_num_dict[short_mid_name]
                                break
                        if array_len is None:
                            raise ValueError(f'Length of MID {mid_name} cannot be found!')
                    mid_name_data_error_bar_array_dict_pair_list.append((None, None))
                    mid_name_list.append(None)
                else:
                    raise ValueError()
                array_len_list.append(array_len)
                this_row_array_len_list.append(array_len)
                total_array_len_this_row += array_len
                x_tick_labels_list.append([f'm+{mid_index}' for mid_index in range(array_len)])
                if col_index == 0:
                    y_label_list.append(CommonFigureString.relative_ratio)
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
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.subplot_name_list: mid_name_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,

            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_lim_list: it.repeat((0, 1)),
            ParameterName.y_label_list: y_label_list,
            ParameterName.y_ticks_list: y_ticks_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,

            ParameterName.legend: False,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)


class DistanceAndLossDataFigureConfig(object):
    separated_optimized_solution_num = 5
    collected_optimized_solution_num_list = [20, 100]


class DistanceAndLossBarDataFigure(BasicBarDataFigure):
    @staticmethod
    def distance_or_loss_filtering(
            optimized_value_array, unoptimized_value_array, separated_optimized_solution_num,
            collected_optimized_solution_num_list):
        separated_optimized_value_array = optimized_value_array[:separated_optimized_solution_num]
        mean_value_list = []
        std_value_list = []
        for each_separated_value in separated_optimized_value_array:
            mean_value_list.append(each_separated_value)
            std_value_list.append(np.nan)
        for collected_optimized_solution_num in collected_optimized_solution_num_list:
            collected_value_array = optimized_value_array[:collected_optimized_solution_num]
            mean_value_list.append(np.mean(collected_value_array))
            std_value_list.append(np.std(collected_value_array))

        mean_value_list.append(np.mean(unoptimized_value_array))
        std_value_list.append(np.std(unoptimized_value_array))

        mean_value_array = np.array(mean_value_list)
        std_value_array = np.array(std_value_list)
        return mean_value_array, std_value_array

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        # ax_total_bottom_left = DataFigureConfig.common_ax_total_bottom_left
        # ax_total_size = DataFigureConfig.common_ax_total_size
        default_ax_total_bottom_left = Vector(0.09, 0.19)
        default_ax_total_size = Vector(0.78, 1 - default_ax_total_bottom_left.y)
        ax_total_bottom_left = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_bottom_left, default_ax_total_bottom_left)
        ax_total_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_size, default_ax_total_size)
        color_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.color_dict, CommonFigureMaterials.distance_and_loss_color_dict)

        common_label_width = GroupDataFigure.label_width * scale
        common_label_height = GroupDataFigure.label_height * scale
        common_tick_label_text_size = GroupDataFigure.x_y_axis_tick_label_font_size * scale

        figure_config_dict = {
            ParameterName.column_width: 0.7,
            ParameterName.edge: 0.05,
            ParameterName.x_label_format_dict: {
                ParameterName.axis_label_distance: 0.025 * scale,
                ParameterName.width: common_label_width,
                ParameterName.height: common_label_height,
                ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size * scale,
                ParameterName.axis_label_location: 0.41666
            },
            ParameterName.x_tick_label_format_dict: {
                ParameterName.axis_tick_label_distance: 0.005 * scale,
                ParameterName.width: common_label_width,
                ParameterName.height: common_label_height,
                ParameterName.font_size: GroupDataFigure.x_y_axis_smaller_label_font_size * scale,
            },
            ParameterName.y_label_format_dict: (
                {
                    ParameterName.axis_label_distance: 0.028 * scale,
                    ParameterName.width: common_label_width,
                    ParameterName.height: common_label_height,
                    ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size * scale,
                    ParameterName.font_color: color_dict[ParameterName.loss]
                },
                {
                    ParameterName.axis_label_distance: 0.043 * scale,
                    ParameterName.width: common_label_width,
                    ParameterName.height: common_label_height,
                    ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size * scale,
                    ParameterName.font_color: color_dict[ParameterName.net_distance]
                }
            ),
            ParameterName.y_tick_label_format_dict:
            (
                {
                    ParameterName.axis_tick_label_distance: 0.008 * scale,
                    ParameterName.font_size: common_tick_label_text_size,
                    ParameterName.font_color: color_dict[ParameterName.loss]
                },
                {
                    ParameterName.axis_tick_label_distance: 0.008 * scale,
                    ParameterName.font_size: common_tick_label_text_size,
                    ParameterName.font_color: color_dict[ParameterName.net_distance]
                }
            ),
            ParameterName.bar_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(scale)
        }

        *_, separated_distance_and_loss_dict, _ = embedded_flux_data.return_data(**figure_data_parameter_dict)
        (
            difference_vector_to_optimized_flux_solution, raw_distance_to_optimized_flux_solution,
            filtered_net_distance_to_optimized_flux_solution, optimized_loss_array) = separated_distance_and_loss_dict[
            ParameterName.optimized]
        (
            difference_vector_to_unoptimized_flux_solution, raw_distance_to_unoptimized_flux_solution,
            filtered_net_distance_to_unoptimized_flux_solution, unoptimized_loss_array) = separated_distance_and_loss_dict[
            ParameterName.unoptimized]

        separated_optimized_solution_num = DistanceAndLossDataFigureConfig.separated_optimized_solution_num
        collected_optimized_solution_num_list = DistanceAndLossDataFigureConfig.collected_optimized_solution_num_list
        array_len = separated_optimized_solution_num + len(collected_optimized_solution_num_list) + 1

        distance_y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim_2, (0, 3600))
        distance_y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval_2, 1000)
        distance_y_tick = np.arange(*distance_y_lim, distance_y_tick_interval)

        loss_mean_array, loss_std_array = self.distance_or_loss_filtering(
            optimized_loss_array, unoptimized_loss_array,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        raw_distance_mean_array, raw_distance_std_array = self.distance_or_loss_filtering(
            raw_distance_to_optimized_flux_solution, raw_distance_to_unoptimized_flux_solution,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        net_distance_mean_array, net_distance_std_array = self.distance_or_loss_filtering(
            filtered_net_distance_to_optimized_flux_solution, filtered_net_distance_to_unoptimized_flux_solution,
            separated_optimized_solution_num, collected_optimized_solution_num_list)
        data_array_dict = {
            ParameterName.loss: (0, loss_mean_array, 0),
            ParameterName.distance: (1, raw_distance_mean_array, 1),
            ParameterName.net_distance: (1, net_distance_mean_array, 1),
        }
        data_error_bar_array_dict = {
            ParameterName.loss: loss_std_array,
            ParameterName.distance: raw_distance_std_array,
            ParameterName.net_distance: net_distance_std_array,
        }

        x_tick_labels = [
            CommonFigureString.best,
            *[f'{CommonFigureString.number}{index + 2}' for index in range(separated_optimized_solution_num - 1)],
            *[f'{CommonFigureString.top} {collected_num}' for collected_num in collected_optimized_solution_num_list],
            CommonFigureString.random_fluxes_wrap
        ]

        loss_y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim, (0, 22))
        loss_y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval, 5)
        loss_y_tick = np.arange(*loss_y_lim, loss_y_tick_interval)

        y_lim = (loss_y_lim, distance_y_lim)
        y_ticks = (loss_y_tick, distance_y_tick)
        y_labels = (CommonFigureString.loss, CommonFigureString.euclidean_distance)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: [(data_array_dict, data_error_bar_array_dict)],
            ParameterName.array_len_list: [array_len],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_label_list: [CommonFigureString.optimized_solution],
            ParameterName.x_tick_labels_list: [x_tick_labels],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_label_list: [y_labels],
            ParameterName.y_ticks_list: [y_ticks],
            ParameterName.y_tick_labels_list: [(Keywords.default, Keywords.default)],

            ParameterName.max_bar_num_each_group: 2,
            ParameterName.legend: False,
            ParameterName.twin_x_axis: True,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale, # twin_x_axis=True,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            background=False, **kwargs)


class CommonFluxErrorBarDataFigure(BasicBarDataFigure):
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
        ) = sensitivity_heatmap_x_axis_labels_generator(common_flux_name_list)
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

        subplot_name_text_format_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_text_format_dict,
            DataFigureConfig.common_subplot_text_format_dict_generator())

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


class FluxErrorBarDataFigure(CommonFluxErrorBarDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        data_name = default_parameter_extract(figure_data_parameter_dict, ParameterName.data_name, None)
        target_optimization_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized_size, None, pop=True)
        target_selection_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.selection_size, None, pop=True)
        y_label = 'Relative error'
        if data_name == DataName.raw_model_all_data:
            bottom_y_lim = [-0.3, 0.41]
            top_y_lim = [0.8, 1.8]
            y_lim = [bottom_y_lim, top_y_lim]
            y_ticks = [np.arange(*bottom_y_lim, 0.1), [1, 1.5]]
            cutoff_value_list = [-0.1, 0.1]
        elif data_name == DataName.raw_model_raw_data:
            bottom_y_lim = [-0.4, 0.41]
            top_y_lim = [0.8, 1.7]
            y_lim = [bottom_y_lim, top_y_lim]
            y_ticks = [np.arange(*bottom_y_lim, 0.1), [1, 1.5]]
            cutoff_value_list = [-0.2, 0.2]
        else:
            raise ValueError()
        y_tick_labels = [['{:.0%}'.format(y_tick) for y_tick in each_ax_y_ticks] for each_ax_y_ticks in y_ticks]
        broken_y_axis_ratio = [0.79, 0.84]

        (
            mean_data_matrix_list, std_data_matrix_list, common_flux_name_list, analyzed_set_size_list,
            selected_min_loss_size_list) = raw_model_data.return_all_flux_data(**figure_data_parameter_dict)
        target_analyzed_index = analyzed_set_size_list.index(target_optimization_size)
        target_selected_index = selected_min_loss_size_list.index(target_selection_size)
        mean_target_data_array = np.array([
            mean_data_matrix[target_selected_index][target_analyzed_index]
            for mean_data_matrix in mean_data_matrix_list])
        std_target_data_array = np.array([
            std_data_matrix[target_selected_index][target_analyzed_index]
            for std_data_matrix in std_data_matrix_list])

        data_array_dict = {common_data_label: mean_target_data_array, }
        data_error_bar_array_dict = {common_data_label: std_target_data_array, }
        color_dict = {common_data_label: CommonFigureMaterials.default_flux_error_bar_color}

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: [(data_array_dict, data_error_bar_array_dict)],
            ParameterName.flux_name_list: common_flux_name_list,
            ParameterName.cutoff: [cutoff_value_list],

            ParameterName.common_y_lim: y_lim,
            ParameterName.common_y_label: y_label,
            ParameterName.y_ticks_list: y_ticks,
            ParameterName.default_y_tick_label_list: y_tick_labels,
            ParameterName.y_label_format_dict: {ParameterName.axis_label_location: 0.65,},

            ParameterName.broken_y_axis: broken_y_axis_ratio,
            **figure_data_parameter_dict
        }

        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class CommonDifferenceFluxErrorBarDataFigure(CommonFluxErrorBarDataFigure):
    ax_total_bottom_left = Vector(0, 0)
    ax_total_size = Vector(1, 1) - ax_total_bottom_left
    ax_y_interval = 0.015

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        bar_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0, self.ax_y_interval))
        flux_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_name_list, None, force=True)
        relative_error = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_relative_distance, False, pop=True)

        data_nested_list = []
        vector_array_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.net_optimized_diff_vector_list, None, force=True, pop=True)
        data_label_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_label, it.repeat(common_data_label), pop=True)
        subplot_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_list, None, pop=True)
        text_axis_loc_pair = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.text_axis_loc_pair, Vector(0.5, 0.9), pop=True)

        _, select_average_reoptimize_color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
            CommonFigureMaterials, with_reoptimization=True, different_simulated_data=True)
        color_dict = {
            common_data_label: CommonFigureMaterials.default_flux_error_bar_color,
            **select_average_reoptimize_color_dict,
        }

        for current_vector_array, data_label in zip(vector_array_list, data_label_list):
            current_vector_dim = len(np.shape(current_vector_array))
            if current_vector_dim == 1:
                mean_diff_vector = current_vector_array
                std_diff_vector = np.nan * np.ones_like(current_vector_array)
            elif current_vector_dim == 2:
                mean_diff_vector = np.mean(current_vector_array, axis=0)
                std_diff_vector = np.std(current_vector_array, axis=0)
            else:
                raise ValueError()
            data_nested_list.append((
                {data_label: mean_diff_vector, },
                {data_label: std_diff_vector, },
            ))

        total_axis_num = len(data_nested_list)
        ax_total_bottom_left_list = []
        ax_total_size_list = []
        ax_y_interval = bar_interval
        ax_total_size = self.ax_total_size
        ax_total_bottom_left = self.ax_total_bottom_left
        ax_height = (1 - ax_y_interval * (total_axis_num - 1)) / total_axis_num
        for index in range(total_axis_num - 1, -1, -1):
            ax_bottom_left = Vector(
                ax_total_bottom_left.x, ax_total_bottom_left.y + (ax_height + ax_y_interval) * index)
            ax_total_bottom_left_list.append(ax_bottom_left)
            ax_total_size_list.append(Vector(ax_total_size.x, ax_height))
        y_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_lim, None, pop=True)
        y_ticks = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_ticks_list, None, pop=True)
        y_abs_lim = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_abs_lim, 350.0001, pop=True)
        y_tick_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_interval, 100, pop=True)
        y_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.common_y_label, CommonFigureString.difference, pop=True
        )
        if y_lim is None and y_ticks is None:
            y_lim, y_ticks = symmetrical_lim_tick_generator_with_zero(y_abs_lim, None, y_tick_interval)
        elif y_lim is None or y_ticks is None:
            raise ValueError()
        cutoff_value_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.cutoff, None, pop=True)
        y_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.y_tick_labels_list, None, pop=True)
        if y_tick_labels is None:
            y_tick_labels = []
            if relative_error:
                label_format_str = '{:.0%}'
            else:
                label_format_str = '{:.0f}'
            for y_tick in y_ticks:
                try:
                    each_ax_y_ticks = y_tick
                    current_y_tick_label = [label_format_str.format(y_tick) for y_tick in each_ax_y_ticks]
                except TypeError:
                    current_y_tick_label = label_format_str.format(y_tick)
                y_tick_labels.append(current_y_tick_label)

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_total_bottom_left_list,
            ParameterName.ax_size_list: ax_total_size_list,
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: data_nested_list,
            ParameterName.flux_name_list: flux_name_list,
            ParameterName.cutoff: cutoff_value_list,

            ParameterName.common_y_lim: y_lim,
            ParameterName.common_y_label: y_label,
            ParameterName.y_ticks_list: y_ticks,
            ParameterName.default_y_tick_label_list: y_tick_labels,

            ParameterName.subplot_name_list: subplot_name_list,
            ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            **figure_data_parameter_dict
        }

        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class HCT116OptimizedFluxErrorBarDataFigure(CommonDifferenceFluxErrorBarDataFigure):

    separated_optimized_solution_num = DistanceAndLossDataFigureConfig.separated_optimized_solution_num
    collected_optimized_solution_num_list = DistanceAndLossDataFigureConfig.collected_optimized_solution_num_list

    @staticmethod
    def calculate_row_num(
            self, with_single_optimized_solutions=True, with_collected_optimized_set=True, with_unoptimized_set=True,
            **kwargs):
        total_row_num = 0
        if with_single_optimized_solutions:
            total_row_num += self.separated_optimized_solution_num - 1
        if with_collected_optimized_set:
            total_row_num += len(self.collected_optimized_solution_num_list)
        if with_unoptimized_set:
            total_row_num += 1
        return total_row_num

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        bar_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0, self.ax_y_interval))
        *_, separated_distance_and_loss_dict, flux_name_list = embedded_flux_data.return_data(
            **figure_data_parameter_dict)
        net_target_optimized_diff_vector, *_ = separated_distance_and_loss_dict[ParameterName.optimized]
        net_target_unoptimized_diff_vector, *_ = separated_distance_and_loss_dict[ParameterName.unoptimized]
        self.with_single_optimized_solutions = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_single_optimized_solutions, True)
        self.with_collected_optimized_set = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_collected_optimized_set, True)
        self.with_unoptimized_set = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_unoptimized_set, True)

        separated_optimized_solution_num = self.separated_optimized_solution_num
        collected_optimized_solution_num_list = self.collected_optimized_solution_num_list

        net_optimized_diff_vector_list = []
        subplot_name_list = []
        if self.with_single_optimized_solutions:
            net_optimized_diff_vector_list.extend([
                current_optimized_net_diff_vector_array
                for current_optimized_net_diff_vector_array
                in net_target_optimized_diff_vector[1:separated_optimized_solution_num, :]
            ])
            subplot_name_list.extend([
                f'{CommonFigureString.number}{index + 2} best solution'
                for index in range(separated_optimized_solution_num - 1)])
        if self.with_collected_optimized_set:
            for collected_num_index, collected_num in enumerate(collected_optimized_solution_num_list):
                net_optimized_diff_vector_list.append(net_target_optimized_diff_vector[:collected_num, :])
                subplot_name_list.append(f'{CommonFigureString.top} {collected_num}')
        if self.with_unoptimized_set:
            net_optimized_diff_vector_list.append(net_target_unoptimized_diff_vector)
            subplot_name_list.append(CommonFigureString.random_fluxes)

        y_abs_lim = 350.0001
        y_tick_interval = 100

        figure_data_parameter_dict = {
            ParameterName.net_optimized_diff_vector_list: net_optimized_diff_vector_list,
            ParameterName.ax_interval: bar_interval,
            ParameterName.flux_name_list: flux_name_list,

            ParameterName.y_abs_lim: y_abs_lim,
            ParameterName.y_tick_interval: y_tick_interval,

            ParameterName.subplot_name_list: subplot_name_list,
            **figure_data_parameter_dict
        }

        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class SimulatedDataOptimizedFluxErrorBarDataFigure(CommonDifferenceFluxErrorBarDataFigure):
    @staticmethod
    def calculate_row_num(self, **kwargs):
        return 3

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, **kwargs):
        bar_interval = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_interval, Vector(0, self.ax_y_interval))
        relative_error = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_relative_distance, False)
        data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, None, force=True)
        target_optimized_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized_size, None, force=True, pop=True)
        target_selection_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.selection_size, None, force=True, pop=True)
        subplot_name_list = [
            CommonFigureString.selected_solution, CommonFigureString.averaged_solution,
            CommonFigureString.reoptimized_solution]
        data_label_list = [
            ParameterName.selected, ParameterName.averaged, ParameterName.optimized]
        if relative_error:
            (
                (initial_raw_selected_relative_error_dict, initial_averaged_relative_error_dict,
                 raw_selected_relative_error_dict), flux_name_list, analyzed_set_size_list, selected_min_loss_size_list
            ) = raw_model_data.return_all_flux_data(**figure_data_parameter_dict)
            net_optimized_diff_vector_list = [
                initial_raw_selected_relative_error_dict[target_selection_size][target_optimized_size],
                initial_averaged_relative_error_dict[target_selection_size][target_optimized_size],
                raw_selected_relative_error_dict[target_selection_size][target_optimized_size],]
            if data_name in {DataName.raw_model_all_data, DataName.optimization_from_solutions_all_data}:
                cutoff_value_list = [-0.1, 0.1]
            elif data_name in {DataName.raw_model_raw_data, DataName.optimization_from_solutions_raw_data}:
                cutoff_value_list = [-0.2, 0.2]
            else:
                raise ValueError()
            bottom_y_lim = [-1.0, -0.34]
            middle_y_lim, middle_y_ticks = symmetrical_lim_tick_generator_with_zero(
                0.32, 0.32, 0.1)
            top_y_lim = [0.34, 1.1]
            y_lim = [bottom_y_lim, middle_y_lim, top_y_lim]
            y_ticks = [[-1.0, -0.5], middle_y_ticks, [0.5, 1.0]]
            y_label = [None, CommonFigureString.relative_error, None]
            # broken_y_axis_ratio = [(0, 0.79), (0.84, 1)]
            broken_y_axis_ratio = [(0, 0.16), (0.21, 0.79), (0.84, 1)]
            extra_figure_data_parameter_dict = {
                ParameterName.broken_y_axis: broken_y_axis_ratio,
                ParameterName.common_y_lim: y_lim,
                ParameterName.common_y_label: y_label,
                ParameterName.y_ticks_list: y_ticks,
                ParameterName.cutoff: cutoff_value_list,
                ParameterName.y_label_format_dict: {ParameterName.axis_label_location: 0.65,},
            }
        else:
            (
                (initial_raw_selected_diff_vector_dict, initial_averaged_diff_vector_dict,
                    raw_selected_diff_vector_dict), flux_name_list, analyzed_set_size_list, selected_min_loss_size_list
            ) = raw_model_data.return_diff_vector_data(**figure_data_parameter_dict)
            net_optimized_diff_vector_list = [
                initial_raw_selected_diff_vector_dict[target_selection_size][target_optimized_size],
                initial_averaged_diff_vector_dict[target_selection_size][target_optimized_size],
                raw_selected_diff_vector_dict[target_selection_size][target_optimized_size],]
            y_abs_lim = 100.0001
            y_tick_interval = 50
            extra_figure_data_parameter_dict = {
                ParameterName.y_abs_lim: y_abs_lim,
                ParameterName.y_tick_interval: y_tick_interval,
            }

        figure_data_parameter_dict = {
            ParameterName.net_optimized_diff_vector_list: net_optimized_diff_vector_list,
            ParameterName.ax_interval: bar_interval,
            ParameterName.flux_name_list: flux_name_list,
            ParameterName.data_label: data_label_list,

            ParameterName.subplot_name_list: subplot_name_list,
            **extra_figure_data_parameter_dict,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)


class DataSensitivityOptimizedFluxErrorBarDataFigure(CommonDifferenceFluxErrorBarDataFigure):
    @staticmethod
    def calculate_row_num(self, figure_data, **kwargs):
        try:
            data_num = self.data_num
        except AttributeError:
            data_dict_list, *_ = figure_data
            data_num = len(data_dict_list)
        return data_num

    def __init__(self, figure_data_parameter_dict, **kwargs):
        target_optimized_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized_size, None, force=True, pop=True)
        target_selection_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.selection_size, None, force=True, pop=True)
        subplot_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.subplot_name_list, None, force=True, pop=True)
        figure_data = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_data, None, pop=True)
        relative_error = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.flux_relative_distance, False)
        net_optimized_diff_vector_list = []
        selected_solutions = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.selected, False, pop=True)
        if selected_solutions:
            data_label = ParameterName.selected
        else:
            data_label = ParameterName.averaged
        data_label_list = it.repeat(data_label)

        data_dict_list, flux_name_list, *_ = figure_data
        self.data_num = len(data_dict_list)
        for data_dict in data_dict_list:
            current_diff_vector = data_dict[target_selection_size][target_optimized_size]
            net_optimized_diff_vector_list.append(current_diff_vector)
        if relative_error:
            cutoff_value_list = [-0.3, 0.3]
            bottom_y_lim = [-1, -0.7]
            middle_y_lim, middle_y_ticks = symmetrical_lim_tick_generator_with_zero(
                0.75, 0.65, 0.3)
            top_y_lim = [0.8, 1.5]
            y_lim = [bottom_y_lim, middle_y_lim, top_y_lim]
            # y_lim = [middle_y_lim, top_y_lim]
            y_ticks = [[-1.0, -0.8], middle_y_ticks, [1.0, 1.5]]
            y_label = [None, CommonFigureString.relative_error, None]
            broken_y_axis_ratio = [(0, 0.16), (0.21, 0.79), (0.84, 1)]
            # broken_y_axis_ratio = [(0, 0.79), (0.84, 1)]
            y_tick_labels = []
            label_format_str = '{:.0%}'
            for each_ax_y_ticks in y_ticks:
                current_y_tick_label = [label_format_str.format(y_tick) for y_tick in each_ax_y_ticks]
                y_tick_labels.append(current_y_tick_label)
            y_tick_labels[-1][-1] = f'>{y_tick_labels[-1][-1]}'
            y_tick_labels[0][0] = f'<{y_tick_labels[0][0]}'
            text_axis_loc_pair = default_parameter_extract(
                figure_data_parameter_dict, ParameterName.text_axis_loc_pair, Vector(0.35, 0.92), pop=True)
            extra_figure_data_parameter_dict = {
                ParameterName.broken_y_axis: broken_y_axis_ratio,
                ParameterName.common_y_lim: y_lim,
                ParameterName.common_y_label: y_label,
                ParameterName.y_ticks_list: y_ticks,
                ParameterName.y_tick_labels_list: y_tick_labels,
                ParameterName.cutoff: cutoff_value_list,
                ParameterName.y_label_format_dict: {ParameterName.axis_label_location: 0.65,},
                ParameterName.text_axis_loc_pair: text_axis_loc_pair,
            }
            # extra_figure_data_parameter_dict = {
            #     ParameterName.common_y_lim: middle_y_lim,
            #     ParameterName.common_y_label: CommonFigureString.relative_error,
            #     ParameterName.y_ticks_list: middle_y_ticks,
            #     ParameterName.cutoff: cutoff_value_list,
            # }
        else:
            bottom_y_lim = [-230, -130]
            middle_y_lim, middle_y_ticks = symmetrical_lim_tick_generator_with_zero(
                120, 120, 50)
            top_y_lim = [130, 230]
            y_lim = [bottom_y_lim, middle_y_lim, top_y_lim]
            y_ticks = [[-200, -150], middle_y_ticks, [150, 200]]
            y_label = [None, CommonFigureString.difference, None]
            broken_y_axis_ratio = [(0, 0.16), (0.21, 0.79), (0.84, 1)]
            extra_figure_data_parameter_dict = {
                ParameterName.broken_y_axis: broken_y_axis_ratio,
                ParameterName.common_y_lim: y_lim,
                ParameterName.common_y_label: y_label,
                ParameterName.y_ticks_list: y_ticks,
                ParameterName.y_label_format_dict: {ParameterName.axis_label_location: 0.65,},
            }

            # y_abs_lim = 200.0001
            # y_tick_interval = 50
            # extra_figure_data_parameter_dict = {
            #     ParameterName.y_abs_lim: y_abs_lim,
            #     ParameterName.y_tick_interval: y_tick_interval,
            # }

        figure_data_parameter_dict = {
            ParameterName.net_optimized_diff_vector_list: net_optimized_diff_vector_list,
            ParameterName.flux_name_list: flux_name_list,
            ParameterName.data_label: data_label_list,

            ParameterName.subplot_name_list: subplot_name_list,
            **extra_figure_data_parameter_dict,
            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, **kwargs)

