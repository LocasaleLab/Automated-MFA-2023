from ..config import DataFigureConfig, ParameterName, Vector, Keywords, np, it, common_legend_generator, \
    default_parameter_extract, CommonFigureString, FontWeight, LineStyle, ColorConfig, \
    HorizontalAlignment, VerticalAlignment
from .figure_data_loader import time_data, loss_data, embedded_flux_data
from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import single_histogram_plot, draw_text_by_axis_loc

GroupDataFigure = DataFigureConfig.GroupDataFigure


class HistogramDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):

        new_figure_config_dict = figure_data_parameter_dict[ParameterName.figure_config_dict]
        (
            ax_bottom_left_list,
            ax_size_list,
            color_dict,
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.color_dict,
        ]]

        # scale = figure_data_parameter_dict[ParameterName.scale]

        (
            self.complete_data_dict_list,
            self.cutoff,
            self.text_list,
        ) = [
            figure_data_parameter_dict[key] if key in figure_data_parameter_dict else None
            for key in (
                ParameterName.data_nested_list,
                ParameterName.cutoff,
                ParameterName.data_figure_text_list,
            )]

        (
            axis_format_dict, axis_tick_format_dict,
            axis_label_format_dict) = DataFigureConfig.common_axis_param_dict_generator(scale)
        text_config_dict = default_parameter_extract(new_figure_config_dict, ParameterName.text_config_dict, {})
        cutoff_param_dict = default_parameter_extract(new_figure_config_dict, ParameterName.cutoff_param_dict, {})
        figure_config_dict = {
            ParameterName.x_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.x_label_width_height_distance_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.x_label_format_dict]
                    if ParameterName.x_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.x_tick_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.x_tick_label_format_dict]
                    if ParameterName.x_tick_label_format_dict in new_figure_config_dict else {}),
            },
            ParameterName.y_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.y_label_width_height_distance_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.y_label_format_dict]
                    if ParameterName.y_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.y_tick_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.y_tick_label_width_height_distance_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.y_tick_label_format_dict]
                    if ParameterName.y_tick_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.cutoff_param_dict: cutoff_param_dict,
            ParameterName.text_config_dict: text_config_dict,
        }

        (
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
                ParameterName.x_lim_list,
                ParameterName.x_label_list,
                ParameterName.x_ticks_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_lim_list,
                ParameterName.y_label_list,
                ParameterName.y_ticks_list,
                ParameterName.y_tick_labels_list,
            )]

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
        pass

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        ax_and_transform_list = super().draw(fig, parent_ax, parent_transformation)
        for (
                complete_data_dict, (current_ax, current_transform), x_lim, x_label, x_ticks, x_tick_labels, y_lim,
                y_label, y_ticks, y_tick_labels) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.x_lim_list, self.x_label_list,
                self.x_ticks_list, self.x_tick_labels_list, self.y_lim_list, self.y_label_list, self.y_ticks_list,
                self.y_tick_labels_list):
            single_histogram_plot(
                current_ax, current_transform, complete_data_dict,
                cutoff=self.cutoff, x_lim=x_lim, x_label=x_label,
                x_ticks=x_ticks, x_tick_labels=x_tick_labels, y_lim=y_lim, y_label=y_label, y_ticks=y_ticks,
                y_tick_labels=y_tick_labels, figure_config_dict=self.figure_config_dict)
        if self.text_list is not None:
            for (text_content, text_loc_pair), (current_ax, current_transform) in zip(
                    self.text_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, text_content, text_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.text_config_dict])


def common_figure_config(scale):
    common_label_width = GroupDataFigure.label_width * scale
    common_label_height = GroupDataFigure.label_height * scale
    common_label_text_size = GroupDataFigure.x_y_axis_label_font_size * scale
    common_tick_label_text_size = GroupDataFigure.x_y_axis_tick_label_font_size * scale
    cutoff_common_color = ColorConfig.orange

    figure_config_dict = {
        ParameterName.x_label_format_dict: {
            ParameterName.axis_label_distance: 0.023 * scale,
            ParameterName.width: common_label_width,
            ParameterName.height: common_label_height,
            ParameterName.font_size: common_label_text_size,
        },
        ParameterName.x_tick_label_format_dict: {
            ParameterName.axis_tick_label_distance: 0.008 * scale,
            ParameterName.font_size: common_tick_label_text_size,
        },
        ParameterName.y_label_format_dict: {
            ParameterName.axis_label_distance: 0.038 * scale,
            ParameterName.width: common_label_width,
            ParameterName.height: common_label_height,
            ParameterName.font_size: common_label_text_size,
        },
        ParameterName.y_tick_label_format_dict: {
            ParameterName.axis_tick_label_distance: 0.006 * scale,
            ParameterName.font_size: common_tick_label_text_size,
        },
        ParameterName.text_config_dict: {
            ParameterName.font: DataFigureConfig.main_text_font,
            ParameterName.font_size: common_tick_label_text_size,
            ParameterName.font_color: cutoff_common_color,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.width: 0.05,
            ParameterName.height: 0.02,
            ParameterName.horizontal_alignment: HorizontalAlignment.left,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        },
        ParameterName.cutoff_param_dict: {
            ParameterName.edge_style: LineStyle.thin_dash,
            ParameterName.edge_width: 0.8,
            ParameterName.edge_color: cutoff_common_color,
        }
    }
    common_histogram_param_dict = {
        ParameterName.hist_type: ParameterName.hist_type_step_filled,
        ParameterName.density: True,
        ParameterName.alpha: 0.3,
    }
    return figure_config_dict, common_histogram_param_dict


class TimeLossDistanceHistogramDataFigure(HistogramDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        # ax_total_bottom_left = Vector(0.05, 0.05)
        # ax_total_size = Vector(0.95, 0.95)
        # ax_total_bottom_left = DataFigureConfig.common_ax_total_bottom_left
        ax_total_bottom_left = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_bottom_left,
            DataFigureConfig.common_ax_total_bottom_left)
        # ax_total_size = DataFigureConfig.common_ax_total_size
        ax_total_size = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_total_size,
            DataFigureConfig.common_ax_total_size
        )
        ax_bottom_left_list = [ax_total_bottom_left]
        ax_size_list = [ax_total_size]

        figure_config_dict, common_histogram_param_dict = common_figure_config(scale)

        figure_class = figure_data_parameter_dict[ParameterName.figure_class]
        color_dict = figure_data_parameter_dict[ParameterName.color_dict]
        data_config_dict = {}
        cutoff = None
        text_list = None
        if figure_class == ParameterName.time_data:
            time_data_dict = time_data.return_data(**figure_data_parameter_dict)
            data_dict = time_data_dict
            x_label = CommonFigureString.average_running_time
            # x_ticks_list = [5, 10, 15, 20, 25]
            x_ticks_list = [0, 1, 2, 3, 4, 5]
            x_lim = None
            # y_lim = (0, 0.17)
            # y_ticks_list = [0, 0.05, 0.1, 0.15]
            y_lim = (0, 0.71)
            y_ticks_list = [0, 0.2, 0.4, 0.6]
            y_tick_labels_list = ['{:.2f}'.format(num) for num in y_ticks_list]
            bin_num = 50
            min_raw_data = np.inf
            max_raw_data = 0
            total_data_list = []
            for index, (data_label, data_array) in enumerate(data_dict.items()):
                current_histogram_param_dict = dict(common_histogram_param_dict)
                current_histogram_param_dict.update({
                    ParameterName.face_color: color_dict[data_label]
                })
                min_raw_data = np.minimum(min_raw_data, np.min(data_array))
                max_raw_data = np.maximum(max_raw_data, np.max(data_array))
                data_config_dict[data_label] = {
                    ParameterName.x_value_array: data_array,
                    ParameterName.histogram_param_dict: current_histogram_param_dict
                }
                total_data_list.extend(data_array)
            data_range = max_raw_data - min_raw_data
            min_bound = np.maximum(0, min_raw_data - data_range * 0.05)
            max_bound = max_raw_data + data_range * 0.05
            bin_location = np.linspace(min_bound, max_bound, bin_num)
            cutoff = np.median(total_data_list)
            text_x_location = (cutoff - min_bound) / (max_bound - min_bound) + 0.07
            text_location = Vector(text_x_location, 0.85)
            text_content = 'Median: {:.2f}'.format(cutoff)
            text_list = [(text_content, text_location)]
        elif figure_class == ParameterName.loss_data:
            _, filtered_loss_data_dict = loss_data.return_data(**figure_data_parameter_dict)
            data_dict = filtered_loss_data_dict
            # x_label = 'Final loss $\mathbf{L^*}$'
            x_label = CommonFigureString.final_loss_with_equation
            x_ticks_list = [0, 5, 10, 15, 20, 25, 30]
            x_lim = (0, None)
            y_lim = (0, 1.8)
            y_ticks_list = [0, 0.5, 1, 1.5]
            y_tick_labels_list = ['{:.1f}'.format(num) for num in y_ticks_list]
            bin_num = 40
            minimal_zone_len = 0.15
            total_bin_list = []
            for index, (data_label, data_array) in enumerate(data_dict.items()):
                current_histogram_param_dict = dict(common_histogram_param_dict)
                current_histogram_param_dict.update({
                    ParameterName.face_color: color_dict[data_label]
                })
                lower_bound = np.min(data_array)
                upper_bound = np.max(data_array)
                bin_num = int(np.ceil(np.minimum(bin_num, (upper_bound - lower_bound) / minimal_zone_len)))
                current_bins = np.linspace(lower_bound, upper_bound, bin_num)
                total_bin_list.append(current_bins)
                data_config_dict[data_label] = {
                    ParameterName.x_value_array: data_array,
                    ParameterName.histogram_param_dict: current_histogram_param_dict
                }
            bin_location = np.concatenate(total_bin_list)
            bin_location.sort()
        elif figure_class == ParameterName.solution_distance_data:
            _, complete_distance_dict, _ = embedded_flux_data.return_data(**figure_data_parameter_dict)
            x_label = 'Euclidean distance within each group'
            # x_ticks_list = [0, 5, 10, 15, 20, 25, 30]
            # x_lim = (0, None)
            # y_lim = (0, 1.8)
            x_ticks_list = None
            x_lim = (0, 5000)
            y_lim = (0, 14e-4)
            y_ticks_list = [0, 5e-4, 1e-3]
            y_tick_labels_list = ['0', '5e-4', '10e-4']
            bin_num = 50
            min_raw_data = np.inf
            max_raw_data = 0
            for index, (data_label, data_array) in enumerate(complete_distance_dict.items()):
                current_histogram_param_dict = dict(common_histogram_param_dict)
                current_histogram_param_dict.update({
                    ParameterName.face_color: color_dict[data_label]
                })
                min_raw_data = np.minimum(min_raw_data, np.min(data_array))
                max_raw_data = np.maximum(max_raw_data, np.max(data_array))
                data_config_dict[data_label] = {
                    ParameterName.x_value_array: data_array,
                    ParameterName.histogram_param_dict: current_histogram_param_dict
                }
            data_range = max_raw_data - min_raw_data
            min_bound = np.maximum(0, min_raw_data - data_range * 0.05)
            max_bound = max_raw_data + data_range * 0.05
            bin_location = np.linspace(min_bound, max_bound, bin_num)
        else:
            raise ValueError()
        if x_ticks_list is None:
            x_tick_labels_list = Keywords.default
        else:
            x_tick_labels_list = [str(x_tick) for x_tick in x_ticks_list]
        for data_label, current_data_dict in data_config_dict.items():
            current_data_dict[ParameterName.histogram_param_dict].update({ParameterName.bins: bin_location})
        y_label = 'Density'

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_bottom_left_list,
            ParameterName.ax_size_list: ax_size_list,
            ParameterName.legend_center: None,
            ParameterName.legend_area_size: None,
            ParameterName.color_dict: color_dict,
            ParameterName.legend: False,
            ParameterName.figure_config_dict: figure_config_dict,

            ParameterName.data_nested_list: [data_config_dict],
            ParameterName.cutoff: cutoff,
            ParameterName.data_figure_text_list: text_list,
            ParameterName.emphasized_flux_list: None,
            ParameterName.x_lim_list: [x_lim],
            ParameterName.y_lim_list: [y_lim],
            ParameterName.x_label_list: [x_label],
            ParameterName.y_label_list: [y_label],
            ParameterName.x_ticks_list: [x_ticks_list],
            ParameterName.y_ticks_list: [y_ticks_list],
            ParameterName.x_tick_labels_list: [x_tick_labels_list],
            ParameterName.y_tick_labels_list: [y_tick_labels_list],
            **figure_data_parameter_dict
        }
        super().__init__(
            figure_data_parameter_dict, bottom_left, size, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)
