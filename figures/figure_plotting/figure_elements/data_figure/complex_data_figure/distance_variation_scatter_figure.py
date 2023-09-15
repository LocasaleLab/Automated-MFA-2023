from ..config import Vector, ParameterName
from ..config import CompositeFigure, TextBox
from ..config import ZOrderConfig, TextConfig, HorizontalAlignment, VerticalAlignment, FontWeight
from ..basic_data_figure.scatter_data_figure import AccuracyVariationScatterDataFigure

from ...common_functions import initialize_vector_input
from ..config import common_legend_generator, CommonFigureString, default_parameter_extract


def each_element_location_generation(
        bottom, subplot_height_to_width_ratio, title_gap, title_box_height, top_margin):
    subplot_top = bottom + subplot_height_to_width_ratio
    title_center_y = subplot_top + title_gap + title_box_height / 2
    title_top = subplot_top + title_gap + title_box_height + top_margin
    return subplot_top, title_center_y, title_top


class DistanceVariationScatterFigureConfig(object):
    left = 0
    # total_width = 1.6
    total_width = 0.52
    lower_scatter_bottom = 0.05
    lower_higher_distance = 0.06
    title_box_height = 0.02
    title_box_y_distance = 0.01
    right_explanation_center_x = 1.3
    right_text_width = 0.5

    scatter_left = 0.043
    scatter_right = 0.025
    scatter_height = 0.13
    scatter_width = total_width - scatter_left - scatter_right
    euclidean_distance_scatter_size = Vector(scatter_width, scatter_height)

    (
        lower_scatter_top, lower_title_center_y, upper_scatter_bottom
    ) = each_element_location_generation(
        lower_scatter_bottom, scatter_height, title_box_y_distance, title_box_height,
        lower_higher_distance)
    (
        upper_scatter_top, upper_title_center_y, upper_top
    ) = each_element_location_generation(
        upper_scatter_bottom, scatter_height, title_box_y_distance, title_box_height,
        title_box_y_distance)
    # upper_scatter_top = 0.4
    total_height = upper_top  # 0.44

    # legend_center_y = upper_top + legend_gap + legend_height / 2
    # legend_center_x = total_width / 2 + 0.05
    # legend_center = Vector(legend_center_x, legend_center_y)
    # legend_size = Vector(2 * total_width - legend_center_x * 2, legend_height)
    # total_height = upper_top + legend_gap + legend_height
    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01
    explanation_left_margin = 0.2

    upper_title_center = Vector(total_width / 2, upper_title_center_y)
    lower_title_center = Vector(total_width / 2, lower_title_center_y)
    common_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }
    title_text_config = {
        **common_text_config,
        ParameterName.font_size: 15,
        ParameterName.width: total_width,
        ParameterName.height: title_box_height,
        # ParameterName.font_weight: FontWeight.bold,
        ParameterName.text_box: False
    }
    # legend_config_dict = {
    #     ParameterName.legend_center: legend_center,
    #     ParameterName.legend_area_size: legend_size,
    #     # ParameterName.horiz_or_vertical: ParameterName.horizontal,
    #     ParameterName.horiz_or_vertical: ParameterName.vertical,
    #     ParameterName.shape: ParameterName.circle,
    #     ParameterName.alpha: None,
    #     ParameterName.location_config_dict: {
    #         # ParameterName.total_horiz_edge_ratio: 0.2,
    #         # ParameterName.col_horiz_edge_ratio: 0.2,
    #         ParameterName.total_verti_edge_ratio: 0.1,
    #         ParameterName.row_verti_edge_ratio: 0.8,
    #     },
    #     ParameterName.text_config_dict: {
    #         ParameterName.font_size: legend_font_size,
    #         ParameterName.font_weight: FontWeight.bold
    #     }
    # }


class DistanceVariationScatterFigure(CompositeFigure):
    total_width = DistanceVariationScatterFigureConfig.total_width
    total_height = DistanceVariationScatterFigureConfig.total_height
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        data_name = default_parameter_extract(figure_data_parameter_dict, ParameterName.data_name, None)
        scatter_left = DistanceVariationScatterFigureConfig.scatter_left
        upper_scatter_bottom = DistanceVariationScatterFigureConfig.upper_scatter_bottom
        lower_scatter_bottom = DistanceVariationScatterFigureConfig.lower_scatter_bottom
        scatter_size = DistanceVariationScatterFigureConfig.euclidean_distance_scatter_size

        upper_selection_ratio_data_figure_config_dict = {
            ParameterName.bottom_left: Vector(scatter_left, upper_scatter_bottom),
            ParameterName.size: scatter_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: data_name,
                ParameterName.mode: ParameterName.selection_ratio,
            }
        }
        lower_optimized_size_data_figure_config_dict = {
            ParameterName.bottom_left: Vector(scatter_left, lower_scatter_bottom),
            ParameterName.size: scatter_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: data_name,
                ParameterName.mode: ParameterName.optimized_size,
            }
        }
        upper_selection_ratio_data_figure_obj = AccuracyVariationScatterDataFigure(
            **upper_selection_ratio_data_figure_config_dict)
        lower_optimized_size_data_figure_obj = AccuracyVariationScatterDataFigure(
            **lower_optimized_size_data_figure_config_dict)

        upper_title_text_config_dict = {
            **DistanceVariationScatterFigureConfig.title_text_config,
            ParameterName.string: f'Mean to selection ratio ${CommonFigureString.m_over_n}$'
                                  f' $({CommonFigureString.math_m}' r'\geq50)$',
            ParameterName.center: DistanceVariationScatterFigureConfig.upper_title_center
        }
        lower_title_text_config_dict = {
            **DistanceVariationScatterFigureConfig.title_text_config,
            ParameterName.string: f'STD to optimization size ${CommonFigureString.math_n}$'
                                  f' $({CommonFigureString.m_over_n}' r'=100^{-1})$',
            ParameterName.center: DistanceVariationScatterFigureConfig.lower_title_center
        }
        text_obj_dict = {
            'upper_title': TextBox(**upper_title_text_config_dict),
            'lower_title': TextBox(**lower_title_text_config_dict),
        }
        # legend_obj = common_legend_generator(
        #     DistanceVariationScatterFigureConfig.legend_config_dict,
        #     OptimumDistributionDiagramConfig.optimum_with_random_color_dict)
        size = Vector(self.total_width, self.total_height)
        distance_variation_scatter_data_figure_dict = {
            ParameterName.text: text_obj_dict,
            'distance_variation_scatter_data_figure': {
                'upper_selection_ratio': upper_selection_ratio_data_figure_obj,
                'lower_optimized_size': lower_optimized_size_data_figure_obj},
            # ParameterName.chevron_arrow: chevron_obj_dict,
            # ParameterName.legend: {ParameterName.legend: legend_obj},
        }
        super().__init__(
            distance_variation_scatter_data_figure_dict, Vector(0, 0), size, background=False, **kwargs)


