from ...common.config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, TextBox, \
    default_parameter_extract, CommonElementConfig
from ...common.common_figure_materials import CommonFigureString, CommonFigureMaterials
from ..data_figure.violin_box_data_figure import LossDistanceGridBoxDataFigure


class CommonLossDistanceConfig(object):
    legend_height = 0.05
    subfigure_title_height = 0.03
    subfigure_title_y_distance = 0.005
    figure_title_height = 0.03

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) * scale / 2


class LossDistanceGridFigure(CommonLossDistanceConfig, CompositeFigure):
    height_to_width_ratio = 0.8
    total_width = 1
    total_height = 0.8
    ax_height = 0.72
    ax_bottom = 0.01
    ax_left_side = 0.015
    ax_right_side = 0.01
    ax_interval = 0.015
    axis_width_offset = 0.05 * total_width
    subfigure_title_font_size = DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size
    title_font_size = DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 5

    def __init__(self, figure_data_parameter_dict, **kwargs):
        axis_height = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.height, self.ax_height, pop=True)
        self.ax_height = axis_height
        total_width = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.total_width, self.total_width, pop=True)
        self.total_width = total_width
        bottom_line = self.ax_bottom
        axis_top_y_value = bottom_line + axis_height
        subfigure_title_height = self.subfigure_title_height
        figure_title_height = self.figure_title_height
        subfigure_title_y_value = axis_top_y_value + self.subfigure_title_y_distance + subfigure_title_height / 2
        subfigure_title_top = subfigure_title_y_value + subfigure_title_height / 2
        legend = default_parameter_extract(figure_data_parameter_dict, ParameterName.legend, False, pop=True)
        legend_height = self.legend_height
        if legend:
            legend_center_y = subfigure_title_top + legend_height / 2 - 0.01
            legend_top = legend_center_y + legend_height / 2
            figure_title_y_value = legend_top + figure_title_height / 2
            total_height = legend_top + figure_title_height
        else:
            legend_center_y = 0
            figure_title_y_value = subfigure_title_top + figure_title_height / 2
            total_height = subfigure_title_top + figure_title_height
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        different_simulated_data = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.different_simulated_distance, False, pop=True)

        left_side_edge = self.ax_left_side
        right_side_edge = self.ax_right_side
        interval = self.ax_interval
        axis_width = (total_width - left_side_edge - right_side_edge - interval) / 2
        axis_width_offset = self.axis_width_offset
        if different_simulated_data:
            left_axis_width = axis_width - axis_width_offset
            right_axis_width = axis_width + axis_width_offset
        else:
            left_axis_width = right_axis_width = axis_width
        left_figure_size = Vector(left_axis_width, axis_height)
        right_figure_size = Vector(right_axis_width, axis_height)
        left_figure_left_edge = left_side_edge
        right_figure_left_edge = left_side_edge + left_axis_width + interval
        # text_left_offset = 0.05
        text_left_offset = 0.05
        left_subfigure_title_x_value = left_figure_left_edge + left_axis_width * (0.5 + text_left_offset)
        right_subfigure_title_x_value = right_figure_left_edge + right_axis_width * (0.5 + text_left_offset)
        figure_title_center = Vector(total_width * (0.5 + text_left_offset), figure_title_y_value)

        figure_title = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_title, None, force=True, pop=True)
        common_text_config_dict = {
            **CommonElementConfig.common_text_config,
            ParameterName.text_box: False,
        }
        subfigure_title_text_config_dict = {
            **common_text_config_dict,
            ParameterName.height: subfigure_title_height,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.font_size: self.subfigure_title_font_size,
        }
        figure_title_text_config_dict = {
            **common_text_config_dict,
            ParameterName.string: figure_title,
            ParameterName.center: figure_title_center,
            ParameterName.width: total_width,
            ParameterName.height: figure_title_height,
            ParameterName.font_size: self.title_font_size,
        }

        loss_data_figure_parameter_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.loss_data_figure_parameter_dict, None,
            force=True, pop=True)
        net_distance_data_figure_parameter_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.net_distance_data_figure_parameter_dict, None,
            force=True, pop=True)
        if legend:
            name_dict = default_parameter_extract(figure_data_parameter_dict, ParameterName.name_dict, None, pop=True)
            if name_dict is None:
                name_dict = default_parameter_extract(
                    net_distance_data_figure_parameter_dict, ParameterName.name_dict,
                    None, force=True, pop=True)
            legend_config_dict = {
                ParameterName.legend_center: Vector(0.5 * total_width, legend_center_y),
                ParameterName.legend_area_size: Vector(total_width, legend_height),
                ParameterName.name_dict: name_dict,
                ParameterName.text_config_dict: {
                    ParameterName.font_size: 10,
                    ParameterName.font_weight: FontWeight.bold
                }
            }
            net_distance_data_figure_parameter_dict.update({
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict,
            })
        figure_type = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_type, LossDistanceGridBoxDataFigure, pop=True)
        loss_grid_comparison_figure = figure_type(**{
            ParameterName.bottom_left: Vector(left_figure_left_edge, bottom_line),
            ParameterName.size: left_figure_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.loss_data,
                **figure_data_parameter_dict,
                **loss_data_figure_parameter_dict,
            },
            ParameterName.background: False
        })
        loss_text_box_obj = TextBox(**{
            ParameterName.string: CommonFigureString.loss,
            ParameterName.center: Vector(left_subfigure_title_x_value, subfigure_title_y_value),
            ParameterName.width: left_axis_width,
            **subfigure_title_text_config_dict,
        })

        distance_grid_comparison_figure = figure_type(**{
            ParameterName.bottom_left: Vector(right_figure_left_edge, bottom_line),
            ParameterName.size: right_figure_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                **figure_data_parameter_dict,
                **net_distance_data_figure_parameter_dict,
            },
            ParameterName.background: False
        })
        distance_text_box_obj = TextBox(**{
            # ParameterName.string: CommonFigureString.net_euclidean_distance,
            ParameterName.string: CommonFigureString.distance_to_known_flux,
            ParameterName.center: Vector(right_subfigure_title_x_value, subfigure_title_y_value),
            ParameterName.width: right_axis_width,
            **subfigure_title_text_config_dict,
        })

        figure_title_text_box_obj = TextBox(**figure_title_text_config_dict)
        subfigure_element_dict = {
            'all_data_figure': {
                'title': loss_text_box_obj,
                'data_figure': loss_grid_comparison_figure,
            },
            'experimental_data_figure': {
                'title': distance_text_box_obj,
                'data_figure': distance_grid_comparison_figure,
            },
            'title': {
                'title': figure_title_text_box_obj,
            }
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)


class LossDistanceSinglePairFigure(LossDistanceGridFigure):
    total_width = 0.7
    ax_height = 0.3
    subfigure_title_font_size = DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 2

    def __init__(self, figure_data_parameter_dict, **kwargs):
        total_width = default_parameter_extract(figure_data_parameter_dict, ParameterName.total_width, self.total_width)
        ax_height = default_parameter_extract(figure_data_parameter_dict, ParameterName.ax_height, self.ax_height)
        self.total_width = total_width
        self.ax_height = ax_height
        with_reoptimization = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.optimized, True, pop=True)
        different_simulated_data = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.different_simulated_distance, False)
        loss_name_dict, loss_color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
            CommonFigureMaterials, with_reoptimization)
        net_distance_name_dict, net_distance_color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
            CommonFigureMaterials, with_reoptimization, different_simulated_data)
        if ParameterName.x_tick_labels_list not in figure_data_parameter_dict:
            if ParameterName.x_tick_labels_list not in figure_data_parameter_dict[
                    ParameterName.loss_data_figure_parameter_dict]:
                figure_data_parameter_dict[ParameterName.loss_data_figure_parameter_dict].update({
                    ParameterName.x_tick_labels_list: list(loss_name_dict.values()),
                    ParameterName.color_dict: loss_color_dict,
                    ParameterName.name_dict: loss_name_dict,
                })
            if ParameterName.x_tick_labels_list not in figure_data_parameter_dict[
                    ParameterName.net_distance_data_figure_parameter_dict]:
                figure_data_parameter_dict[ParameterName.net_distance_data_figure_parameter_dict].update({
                    ParameterName.x_tick_labels_list: list(net_distance_name_dict.values()),
                    ParameterName.color_dict: net_distance_color_dict,
                    ParameterName.name_dict: net_distance_name_dict,
                })
        super().__init__(figure_data_parameter_dict, **kwargs)


class SingleLossOrDistanceFigure(CommonLossDistanceConfig, CompositeFigure):
    height_to_width_ratio = 0.8
    total_width = 0.5
    ax_bottom = 0.01
    ax_left_side = 0.015
    ax_right_side = 0.01
    ax_height = 0.3
    title_ax_interval = 0.005
    figure_title_font_size = DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 5
    subfigure_title_font_size = DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size
    total_height = ax_height + title_ax_interval + CommonLossDistanceConfig.figure_title_height
    ax_width = total_width - ax_left_side - ax_right_side

    def __init__(self, figure_data_parameter_dict, **kwargs):
        bottom_line = self.ax_bottom
        ax_total_size = default_parameter_extract(figure_data_parameter_dict, ParameterName.ax_total_size, None)
        left_side_edge = self.ax_left_side
        right_side_edge = self.ax_right_side
        title_ax_interval = self.title_ax_interval
        title_height = self.figure_title_height
        figure_subtitle_height = self.subfigure_title_height
        legend = default_parameter_extract(figure_data_parameter_dict, ParameterName.legend, False, pop=True)
        legend_height = self.legend_height
        figure_subtitle = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_subtitle, None, pop=True)
        if ax_total_size is not None:
            ax_width, ax_height = ax_total_size
            self.ax_height = ax_height
            self.ax_width = ax_width
            self.total_width = left_side_edge + ax_width + right_side_edge
            self.total_height = bottom_line + ax_height + title_ax_interval + title_height
            figure_size = ax_total_size
        else:
            figure_size = Vector(self.ax_width, self.ax_height)
        if legend:
            # self.total_height += legend_height
            legend_center_y = bottom_line + self.ax_height + title_ax_interval / 2 + legend_height / 2 - 0.005
            current_top = legend_center_y + title_ax_interval / 2 + legend_height / 2 - 0.005
        else:
            legend_center_y = 0
            current_top = bottom_line + self.ax_height + title_ax_interval / 2
        if figure_subtitle is not None:
            figure_subtitle_y_value = current_top + figure_subtitle_height / 2
            current_top += figure_subtitle_height / 2 + 0.007
        else:
            figure_subtitle_y_value = 0
        figure_title_y_value = current_top + title_ax_interval / 2 + title_height / 2
        self.total_height = figure_title_y_value + title_height / 2 + 0.001
        # if legend:
        #     self.total_height += legend_height
        #     legend_center_y = bottom_line + self.ax_height + title_ax_interval / 2 + legend_height / 2 - 0.01
        #     legend_top = legend_center_y + title_ax_interval / 2 + legend_height / 2
        #     figure_title_y_value = legend_top + title_height / 2
        # else:
        #     legend_center_y = 0
        #     figure_title_y_value = bottom_line + self.ax_height + title_ax_interval + title_height / 2
        total_width = self.total_width
        text_left_offset = 0.03
        left_figure_left_edge = left_side_edge
        figure_subtitle_center = Vector(total_width / 2 + text_left_offset, figure_subtitle_y_value)
        figure_title_center = Vector(total_width / 2 + text_left_offset, figure_title_y_value)

        if legend:
            name_dict = default_parameter_extract(figure_data_parameter_dict, ParameterName.name_dict, None, pop=True)
            if name_dict is None:
                name_dict = default_parameter_extract(
                    figure_data_parameter_dict, ParameterName.name_dict,
                    None, force=True, pop=True)
            legend_config_dict = {
                ParameterName.legend_center: Vector(0.5 * total_width, legend_center_y),
                ParameterName.legend_area_size: Vector(total_width, legend_height),
                ParameterName.name_dict: name_dict,
                ParameterName.text_config_dict: {
                    ParameterName.font_size: 10,
                    ParameterName.font_weight: FontWeight.bold
                }
            }
            figure_data_parameter_dict.update({
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict,
            })

        figure_type = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_type, LossDistanceGridBoxDataFigure, pop=True)
        figure_class = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_class, ParameterName.loss_data)
        if figure_class == ParameterName.loss_data:
            common_y_label = CommonFigureString.loss
        elif figure_class in {ParameterName.net_euclidean_distance, ParameterName.raw_distance}:
            common_y_label = CommonFigureString.distance
        else:
            raise ValueError()
        figure_data_parameter_dict.update({
            ParameterName.common_y_label: common_y_label,
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.04,
            },
        })
        target_data_comparison_figure = figure_type(**{
            ParameterName.bottom_left: Vector(left_figure_left_edge, bottom_line),
            ParameterName.size: figure_size,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict
        })

        figure_title = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_title, None, force=True, pop=True)
        common_text_config_dict = {
            **CommonElementConfig.common_text_config,
            ParameterName.text_box: False,
        }
        figure_subtitle_text_config_dict = {
            **common_text_config_dict,
            ParameterName.string: figure_subtitle,
            ParameterName.center: figure_subtitle_center,
            ParameterName.width: total_width,
            ParameterName.height: figure_subtitle_height,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.font_size: self.subfigure_title_font_size,
        }
        figure_title_text_config_dict = {
            **common_text_config_dict,
            ParameterName.string: figure_title,
            ParameterName.center: figure_title_center,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.font_size: self.figure_title_font_size,
            # ParameterName.font_weight: FontWeight.bold,
        }

        figure_title_text_box_obj = TextBox(**figure_title_text_config_dict)
        subfigure_element_dict = {
            'data_figure': {
                'title': figure_title_text_box_obj,
                'data_figure': target_data_comparison_figure,
            },
        }
        if figure_subtitle is not None:
            subfigure_element_dict['data_figure']['subtitle'] = TextBox(**figure_subtitle_text_config_dict)
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, self.total_height), background=False, **kwargs)


