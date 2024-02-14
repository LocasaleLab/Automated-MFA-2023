from ...common.config import Vector, ParameterName, CompositeFigure, TextBox, ZOrderConfig, TextConfig, \
    default_parameter_extract, \
    CommonElementConfig
from ...common.common_figure_materials import CommonFigureString
from ..data_figure.scatter_data_figure import AccuracyVariationScatterDataFigure


def each_element_location_generation(
        bottom, subplot_height_to_width_ratio, title_gap, title_box_height, top_margin):
    subplot_top = bottom + subplot_height_to_width_ratio
    title_center_y = subplot_top + title_gap + title_box_height / 2
    title_top = subplot_top + title_gap + title_box_height + top_margin
    return subplot_top, title_center_y, title_top


class DistanceVariationScatterFigureConfig(object):
    left = 0
    # total_width = 1.6
    vertical_total_width = 0.52
    lower_scatter_bottom = 0.05
    lower_higher_distance = 0.06
    title_box_height = 0.02
    title_box_y_distance = 0.01
    right_explanation_center_x = 1.3
    right_text_width = 0.5

    scatter_left = 0.043
    scatter_right = 0.025
    scatter_height = 0.13
    horiz_interval = 0.1
    scatter_width = vertical_total_width - scatter_left - scatter_right
    horiz_left_scatter_center = scatter_left + scatter_width / 2
    horiz_right_scatter_left = horiz_left_scatter_center + scatter_width / 2 + horiz_interval
    horiz_right_scatter_center = horiz_right_scatter_left + scatter_width / 2
    horiz_total_width = 2 * scatter_width + horiz_interval + scatter_left + scatter_right
    euclidean_distance_scatter_size = Vector(scatter_width, scatter_height)

    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01
    explanation_left_margin = 0.2

    common_text_config = CommonElementConfig.common_text_config


def return_parameter(horiz_or_vertical, figure_title):
    scatter_left = DistanceVariationScatterFigureConfig.scatter_left
    lower_scatter_bottom = DistanceVariationScatterFigureConfig.lower_scatter_bottom
    scatter_height = DistanceVariationScatterFigureConfig.scatter_height
    title_box_y_distance = DistanceVariationScatterFigureConfig.title_box_y_distance
    title_box_height = DistanceVariationScatterFigureConfig.title_box_height
    lower_topper_distance = DistanceVariationScatterFigureConfig.lower_higher_distance
    scatter_width = DistanceVariationScatterFigureConfig.scatter_width
    if horiz_or_vertical == ParameterName.vertical:
        total_width = DistanceVariationScatterFigureConfig.vertical_total_width
        (
            lower_scatter_top, lower_title_center_y, upper_scatter_bottom
        ) = each_element_location_generation(
            lower_scatter_bottom, scatter_height, title_box_y_distance, title_box_height,
            lower_topper_distance)
        (
            upper_scatter_top, upper_title_center_y, upper_top
        ) = each_element_location_generation(
            upper_scatter_bottom, scatter_height, title_box_y_distance, title_box_height,
            title_box_y_distance)
        # upper_scatter_top = 0.4
        total_height = upper_top  # 0.44
        upper_left_scatter_bottom_left = Vector(scatter_left, upper_scatter_bottom)
        lower_right_scatter_bottom_left = Vector(scatter_left, lower_scatter_bottom)
        upper_left_title_center = Vector(total_width / 2, upper_title_center_y)
        lower_right_title_center = Vector(total_width / 2, lower_title_center_y)
    elif horiz_or_vertical == ParameterName.horizontal:
        total_width = DistanceVariationScatterFigureConfig.horiz_total_width
        (
            scatter_top, title_center_y, total_height
        ) = each_element_location_generation(
            lower_scatter_bottom, scatter_height, title_box_y_distance, title_box_height,
            lower_topper_distance)
        upper_left_scatter_bottom_left = Vector(
            scatter_left, lower_scatter_bottom)
        lower_right_scatter_bottom_left = Vector(
            DistanceVariationScatterFigureConfig.horiz_right_scatter_left, lower_scatter_bottom)
        upper_left_title_center = Vector(
            DistanceVariationScatterFigureConfig.horiz_left_scatter_center, title_center_y)
        lower_right_title_center = Vector(
            DistanceVariationScatterFigureConfig.horiz_right_scatter_center, title_center_y)
    else:
        raise ValueError()
    if figure_title is not None:
        figure_title_center_y_value = (
                total_height - lower_topper_distance + 2 * title_box_y_distance + title_box_height / 2)
        total_height = figure_title_center_y_value + title_box_height / 2 + lower_topper_distance
    else:
        figure_title_center_y_value = total_height
    figure_title_center = Vector(total_width / 2, figure_title_center_y_value)
    return (
        total_width, total_height, scatter_width, upper_left_scatter_bottom_left, lower_right_scatter_bottom_left,
        upper_left_title_center, lower_right_title_center, figure_title_center)


class DistanceVariationScatterFigure(CompositeFigure):
    # total_width = DistanceVariationScatterFigureConfig.total_width
    # total_height = DistanceVariationScatterFigureConfig.total_height
    # height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        horiz_or_vertical = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.horiz_or_vertical, ParameterName.vertical, pop=True)
        data_name = default_parameter_extract(figure_data_parameter_dict, ParameterName.data_name, None)
        figure_title = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_title, None, pop=True)
        (
            total_width, total_height, scatter_width, upper_left_scatter_bottom_left, lower_right_scatter_bottom_left,
            upper_left_title_center, lower_right_title_center, figure_title_center
        ) = return_parameter(horiz_or_vertical, figure_title)
        scatter_size = DistanceVariationScatterFigureConfig.euclidean_distance_scatter_size
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width

        upper_or_left_selection_ratio_data_figure_config_dict = {
            ParameterName.bottom_left: upper_left_scatter_bottom_left,
            ParameterName.size: scatter_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: data_name,
                ParameterName.mode: ParameterName.selection_ratio,
            }
        }
        lower_or_right_optimized_size_data_figure_config_dict = {
            ParameterName.bottom_left: lower_right_scatter_bottom_left,
            ParameterName.size: scatter_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: data_name,
                ParameterName.mode: ParameterName.optimized_size,
            }
        }
        upper_or_left_selection_ratio_data_figure_obj = AccuracyVariationScatterDataFigure(
            **upper_or_left_selection_ratio_data_figure_config_dict)
        lower_or_right_optimized_size_data_figure_obj = AccuracyVariationScatterDataFigure(
            **lower_or_right_optimized_size_data_figure_config_dict)
        title_box_height = DistanceVariationScatterFigureConfig.title_box_height
        common_title_text_config = {
            **DistanceVariationScatterFigureConfig.common_text_config,
            ParameterName.height: title_box_height,
            ParameterName.text_box: False
        }
        sub_title_text_config = {
            **common_title_text_config,
            ParameterName.font_size: 13,
            ParameterName.width: scatter_width,
        }
        title_text_config = {
            **common_title_text_config,
            ParameterName.font_size: 16,
            ParameterName.width: total_width,
        }
        upper_or_left_title_text_config_dict = {
            **sub_title_text_config,
            ParameterName.string: f'Mean to selection ratio ${CommonFigureString.m_over_n}$'
                                  f' $({CommonFigureString.math_m}' r'\geq50)$',
            ParameterName.center: upper_left_title_center
        }
        lower_or_right_title_text_config_dict = {
            **sub_title_text_config,
            ParameterName.string: f'STD to optimization size ${CommonFigureString.math_n}$'
                                  f' $({CommonFigureString.m_over_n}' r'=100^{-1})$',
            ParameterName.center: lower_right_title_center
        }
        text_obj_dict = {
            'upper_title': TextBox(**upper_or_left_title_text_config_dict),
            'lower_title': TextBox(**lower_or_right_title_text_config_dict),
        }
        if figure_title is not None:
            figure_title_text_config_dict = {
                **title_text_config,
                ParameterName.string: figure_title,
                ParameterName.center: figure_title_center
            }
            text_obj_dict['figure_title'] = TextBox(**figure_title_text_config_dict)
        size = Vector(self.total_width, self.total_height)
        distance_variation_scatter_data_figure_dict = {
            ParameterName.text: text_obj_dict,
            'distance_variation_scatter_data_figure': {
                'upper_left_selection_ratio': upper_or_left_selection_ratio_data_figure_obj,
                'lower_right_optimized_size': lower_or_right_optimized_size_data_figure_obj},
        }
        super().__init__(
            distance_variation_scatter_data_figure_dict, Vector(0, 0), size, background=False, **kwargs)


