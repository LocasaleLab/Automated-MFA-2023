from ..config import DataFigureConfig, ParameterName, Vector, it, Keywords, merge_axis_format_dict, np, \
    mid_carbon_num_dict, CommonFigureMaterials, common_legend_generator, default_parameter_extract, \
    sensitivity_heatmap_x_axis_labels_generator, DataName, ColorConfig, LineStyle, CommonFigureString
from ..config import HorizontalAlignment, VerticalAlignment
from ...common_functions import initialize_vector_input
from .figure_data_loader import mid_comparison_data, embedded_flux_data, raw_model_data
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
                    ParameterName.subplot_name_text_format_dict,
                    ParameterName.x_tick_separator_format_dict, ParameterName.x_tick_separator_label_format_dict,
                    ParameterName.y_tick_separator_format_dict, ParameterName.y_tick_separator_label_format_dict,
                ] if key in new_figure_config_dict
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }

        (
            self.subplot_name_list,
            self.text_axis_loc_pair,
        ) = [
            figure_data_parameter_dict[key] if key in figure_data_parameter_dict else None
            for key in (
                ParameterName.subplot_name_list,
                ParameterName.text_axis_loc_pair,
            )]

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
                **tick_separator_dict)
        if self.subplot_name_list is not None:
            for subplot_name, (current_ax, current_transform) in zip(self.subplot_name_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, subplot_name, self.text_axis_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.subplot_name_text_format_dict])


class MIDComparisonGridBarDataFigure(BasicBarDataFigure):
    ax_total_bottom_left = Vector(0.05, 0.03)
    ax_total_size = Vector(1, 1) - ax_total_bottom_left
    ax_interval = Vector(0.015, 0.03)        # (horizontal, vertical)
    each_row_figure_height = 0.185

    @staticmethod
    def calculate_height(self, row_num):
        return self.each_row_figure_height * row_num + (row_num - 1) * self.ax_interval.y

    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        # ax_total_bottom_left = self.ax_total_bottom_left
        # ax_total_size = self.ax_total_size
        # ax_interval = self.ax_interval
        # try:
        #     default_y_tick_label_list = figure_data_parameter_dict[ParameterName.default_y_tick_label_list]
        # except KeyError:
        #     # default_y_tick_label_list = ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0']
        #     default_y_tick_label_list = ['0.00', '0.25', '0.50', '0.75', '1.00']
        # absolute_total_size = default_parameter_extract(
        #     figure_data_parameter_dict, ParameterName.size, None, force=True)
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

        x_tick_label_format_dict = DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale)
        x_tick_label_format_dict[ParameterName.axis_tick_label_distance] = 0.005 * scale
        y_label_format_dict = DataFigureConfig.y_label_width_height_distance_dict_generator(scale)
        y_label_format_dict[ParameterName.axis_label_distance] = 0.04 * scale
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_width_height_distance_dict_generator(scale)
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
                    mid_name_data_error_bar_array_dict_pair_list.append((mid_array_dict, error_bar_array_dict))
                    mid_name_list.append(mid_name)
                elif isinstance(mid_name, int) or mid_name not in mean_data_dict:
                    if isinstance(mid_name, int):
                        array_len = mid_name
                    else:
                        array_len = mid_carbon_num_dict[mid_name]
                    mid_name_data_error_bar_array_dict_pair_list.append((None, None))
                    mid_name_list.append(None)
                else:
                    raise ValueError()
                array_len_list.append(array_len)
                this_row_array_len_list.append(array_len)
                total_array_len_this_row += array_len
                x_tick_labels_list.append([f'm+{mid_index}' for mid_index in range(array_len)])
                if col_index == 0:
                    y_label_list.append('Relative ratio')
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

        if ParameterName.color_dict in figure_data_parameter_dict:
            color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        else:
            color_dict = CommonFigureMaterials.mid_comparison_color_dict

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


class DistanceAndLossBarDataFigure(BasicBarDataFigure):
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
        # if ParameterName.color_dict in figure_data_parameter_dict:
        #     color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        # else:
        #     color_dict = CommonFigureMaterials.distance_and_loss_color_dict
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
                    ParameterName.font_color: color_dict[ParameterName.distance]
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
                    ParameterName.font_color: color_dict[ParameterName.distance]
                }
            ),
            ParameterName.bar_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order,
                ParameterName.alpha: DataFigureConfig.alpha_for_bar_plot
            },
            ParameterName.error_bar_param_dict: DataFigureConfig.common_error_bar_param_dict_generator(scale)
        }

        *_, separated_distance_and_loss_dict = embedded_flux_data.return_data(**figure_data_parameter_dict)
        distance_to_optimized_flux_solution, optimized_loss_array = separated_distance_and_loss_dict[
            ParameterName.optimized]
        distance_to_unoptimized_flux_solution, unoptimized_loss_array = separated_distance_and_loss_dict[
            ParameterName.unoptimized]
        # optimized_solution_num = len(distance_to_optimized_flux_solution)
        separated_optimized_solution_num = 5
        collected_optimized_solution_num = 100
        separated_distance_array = distance_to_optimized_flux_solution[:separated_optimized_solution_num]
        separated_optimized_loss = optimized_loss_array[:separated_optimized_solution_num]
        collected_distance_array = distance_to_optimized_flux_solution[:collected_optimized_solution_num]
        collected_loss_array = optimized_loss_array[:collected_optimized_solution_num]
        mean_distance_to_optimized_flux_solution = np.mean(collected_distance_array)
        mean_optimized_loss = np.mean(collected_loss_array)
        std_distance_to_optimized_flux_solution = np.std(collected_distance_array)
        std_optimized_loss = np.std(collected_loss_array)
        # array_len = optimized_solution_num + 1
        array_len = separated_optimized_solution_num + 2
        mean_distance_to_unoptimized_flux_solution = np.mean(distance_to_unoptimized_flux_solution)
        mean_unoptimized_loss = np.mean(unoptimized_loss_array)
        std_distance_to_unoptimized_flux_solution = np.std(distance_to_unoptimized_flux_solution)
        std_unoptimized_loss = np.std(unoptimized_loss_array)
        data_array_dict = {
            ParameterName.loss: (0, np.concatenate([
                separated_optimized_loss,
                [mean_optimized_loss, mean_unoptimized_loss]])),
            ParameterName.distance: (1, np.concatenate([
                separated_distance_array,
                [mean_distance_to_optimized_flux_solution, mean_distance_to_unoptimized_flux_solution]])),
        }
        data_error_bar_array_dict = {
            ParameterName.loss: np.concatenate([
                [np.nan] * separated_optimized_solution_num,
                [std_optimized_loss, std_unoptimized_loss]]),
            ParameterName.distance: np.concatenate([
                [np.nan] * separated_optimized_solution_num,
                [std_distance_to_optimized_flux_solution, std_distance_to_unoptimized_flux_solution]]),
        }
        x_tick_labels = [
            'Best',
            *[f'No.{index + 2}' for index in range(separated_optimized_solution_num - 1)],
            'Top 100',
            'Random\nfluxes'
        ]
        y_lim = ((0, 22), (0, 3600))
        # y_labels = ('Loss', 'Euclidean distance to\nbest optimized solutions')
        y_labels = (CommonFigureString.loss, CommonFigureString.euclidean_distance)
        y_ticks = ((0, 5, 10, 15, 20), (0, 1000, 2000, 3000))

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: [(data_array_dict, data_error_bar_array_dict)],
            ParameterName.array_len_list: [array_len],
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.x_label_list: ['Optimized solution'],
            ParameterName.x_tick_labels_list: [x_tick_labels],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_label_list: [y_labels],
            ParameterName.y_ticks_list: [y_ticks],
            ParameterName.y_tick_labels_list: [(Keywords.default, Keywords.default)],

            ParameterName.legend: False,
            ParameterName.twin_x_axis: True,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale, # twin_x_axis=True,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            background=False, **kwargs)


class FluxErrorBarDataFigure(BasicBarDataFigure):
    class Config(object):
        sensitivity_x_y_tick_label_font_size = 7

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
        (
            x_tick_labels, pathway_separator_location_array, pathway_name_location_array, pathway_name_list
        ) = sensitivity_heatmap_x_axis_labels_generator(common_flux_name_list)
        target_analyzed_index = analyzed_set_size_list.index(target_optimization_size)
        target_selected_index = selected_min_loss_size_list.index(target_selection_size)
        mean_target_data_array = np.array([
            mean_data_matrix[target_selected_index][target_analyzed_index]
            for mean_data_matrix in mean_data_matrix_list])
        std_target_data_array = np.array([
            std_data_matrix[target_selected_index][target_analyzed_index]
            for std_data_matrix in std_data_matrix_list])

        # x_tick_label_format_dict = {
        #     ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size,
        #     ParameterName.axis_tick_label_distance: 0.039,
        #     ParameterName.width: 0.08,
        #     ParameterName.height: 0.015,
        #     ParameterName.angle: -90,
        #     ParameterName.horizontal_alignment: HorizontalAlignment.left,
        #     ParameterName.vertical_alignment: HorizontalAlignment.center,
        #     ParameterName.text_box: False,
        # }
        x_tick_label_format_dict = {
            **DataFigureConfig.flux_x_tick_format_dict,
            ParameterName.font_size: GroupDataFigure.x_y_axis_tick_label_font_size,
        }
        x_tick_separator_format_dict = {
            **DataFigureConfig.flux_x_tick_separator_format_dict,
            # ParameterName.axis_line_end_distance: 0.05,
        }
        x_tick_separator_label_format_dict = {
            **DataFigureConfig.flux_x_tick_separator_label_format_dict,
            ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
        }
        y_label_format_dict = {
            **DataFigureConfig.y_label_width_height_distance_dict_generator(),
            ParameterName.axis_label_distance: 0.04,
            ParameterName.axis_label_location: 0.65,
            ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
        }
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_width_height_distance_dict_generator()
        y_tick_label_format_dict[ParameterName.axis_tick_label_distance] = 0.008

        # x_tick_separator_format_dict = {
        #     ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio,
        #     ParameterName.axis_line_start_distance: 0,
        #     ParameterName.axis_line_end_distance: 0.05,
        # }
        # common_tick_separator_label_format_dict = {
        #     ParameterName.font_size: GroupDataFigure.x_y_axis_label_font_size,
        #     ParameterName.width: 0.1,
        #     ParameterName.height: 0.02,
        #     ParameterName.horizontal_alignment: HorizontalAlignment.center,
        #     ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        # }
        # x_tick_separator_label_format_dict = {
        #     **common_tick_separator_label_format_dict,
        #     ParameterName.axis_label_distance: 0.12,
        # }
        cutoff_format_dict = {
            ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio,
            ParameterName.edge_color: ColorConfig.normal_blue,
            ParameterName.z_order: DataFigureConfig.line_z_order,
            ParameterName.edge_style: LineStyle.thin_dash,
        }

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
        }

        common_data_label = ''
        data_array_dict = {common_data_label: mean_target_data_array, }
        data_error_bar_array_dict = {common_data_label: std_target_data_array, }
        color_dict = {common_data_label: CommonFigureMaterials.mid_comparison_color_dict[ParameterName.optimized]}

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: [ax_total_bottom_left],
            ParameterName.ax_size_list: [ax_total_size],
            ParameterName.color_dict: color_dict,
            ParameterName.data_nested_list: [(data_array_dict, data_error_bar_array_dict)],
            ParameterName.array_len_list: [len(common_flux_name_list)],
            ParameterName.figure_config_dict: figure_config_dict,
            ParameterName.cutoff: [cutoff_value_list],

            ParameterName.x_tick_labels_list: [x_tick_labels],
            ParameterName.tick_separator_dict_list: [{
                ParameterName.x_tick_separator_locs: pathway_separator_location_array,
                ParameterName.x_tick_separator_labels: pathway_name_list,
                ParameterName.x_tick_separator_label_locs: pathway_name_location_array,
            }],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.y_label_list: [y_label],
            ParameterName.y_ticks_list: [y_ticks],
            ParameterName.y_tick_labels_list: [y_tick_labels],

            ParameterName.legend: False,
            ParameterName.broken_y_axis: broken_y_axis_ratio,
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, **kwargs)

