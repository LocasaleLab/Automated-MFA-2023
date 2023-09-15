from .config import np, Vector, Keyword, ParameterName
from .config import CompositeFigure, TextBox
from .config import ZOrderConfig, TextConfig, HorizontalAlignment, VerticalAlignment, FontWeight, \
    OptimumDistributionDiagram, OptimumDistributionDiagramConfig, CommonElementConfig, ChevronArrow

from ...common_functions import initialize_vector_input
from ..config import common_legend_generator


def each_element_location_generation(
        bottom, subplot_height_to_width_ratio, title_gap, title_box_height, top_margin):
    subplot_top = bottom + subplot_height_to_width_ratio
    title_center_y = subplot_top + title_gap + title_box_height / 2
    title_top = subplot_top + title_gap + title_box_height + top_margin
    return subplot_top, title_center_y, title_top


class OptimumDistributionComparisonDiagramConfig(object):
    scale = 0.9
    left = 0
    # total_width = 1.6
    total_width = 0.95
    lower_bottom = 0
    title_box_height = 0.04
    explanation_text_box_height = 0.2
    title_box_y_distance = 0.03
    left_column_width = 0.7
    legend_gap = 0
    # legend_height = 0.04
    legend_height = 0.15
    legend_font_size = 20
    chevron_center_x = 0.88
    chevron_width = 0.09
    chevron_x_tail = chevron_center_x - chevron_width / 2
    chevron_x_head = chevron_center_x + chevron_width / 2
    right_explanation_center_x = 1.3
    right_text_width = 0.5

    subplot_total_height = OptimumDistributionDiagram.total_height * scale
    subplot_total_width = OptimumDistributionDiagram.total_width * scale
    (
        lower_box_top, lower_title_center_y, upper_bottom
    ) = each_element_location_generation(
        lower_bottom, subplot_total_height, title_box_y_distance, title_box_height,
        title_box_y_distance)
    lower_explanation_text_center_y = (lower_bottom + lower_box_top) / 2 + 0.03
    (
        upper_box_top, upper_title_center_y, upper_top
    ) = each_element_location_generation(
        upper_bottom, subplot_total_height, title_box_y_distance, title_box_height,
        title_box_y_distance)
    upper_explanation_text_center_y = (upper_bottom + upper_box_top) / 2 + 0.03

    legend_center_y = upper_top + legend_gap + legend_height / 2
    legend_center_x = total_width / 2 + 0.05
    legend_center = Vector(legend_center_x, legend_center_y)
    legend_size = Vector(2 * total_width - legend_center_x * 2, legend_height)
    total_height = upper_top + legend_gap + legend_height
    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01
    explanation_left_margin = 0.2

    upper_title_center = Vector(subplot_total_width / 2, upper_title_center_y)
    lower_title_center = Vector(subplot_total_width / 2, lower_title_center_y)
    upper_explanation_text_center = Vector(right_explanation_center_x, upper_explanation_text_center_y)
    lower_explanation_text_center = Vector(right_explanation_center_x, lower_explanation_text_center_y)
    common_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }
    title_text_config = {
        **common_text_config,
        ParameterName.font_size: 23,
        ParameterName.width: left_column_width,
        ParameterName.height: title_box_height,
        # ParameterName.font_weight: FontWeight.bold,
        ParameterName.text_box: False
    }
    explanation_text_config = {
        **common_text_config,
        ParameterName.font_size: 25,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.width: right_text_width,
        ParameterName.height: explanation_text_box_height,
        ParameterName.line_space: 2,
        ParameterName.text_box: False,
    }
    chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: CommonElementConfig.normal_chevron_width + 0.01
    }
    lower_chevron_config = {
        **chevron_config,
        ParameterName.tail_end_center: Vector(chevron_x_tail, lower_explanation_text_center_y),
        ParameterName.head: Vector(chevron_x_head, lower_explanation_text_center_y),
    }
    upper_chevron_config = {
        **chevron_config,
        ParameterName.tail_end_center: Vector(chevron_x_tail, upper_explanation_text_center_y),
        ParameterName.head: Vector(chevron_x_head, upper_explanation_text_center_y),
    }
    legend_config_dict = {
        ParameterName.legend_center: legend_center,
        ParameterName.legend_area_size: legend_size,
        ParameterName.name_dict: OptimumDistributionDiagramConfig.optimum_name_dict,
        # ParameterName.horiz_or_vertical: ParameterName.horizontal,
        ParameterName.horiz_or_vertical: ParameterName.vertical,
        ParameterName.shape: ParameterName.circle,
        ParameterName.alpha: None,
        ParameterName.location_config_dict: {
            # ParameterName.total_horiz_edge_ratio: 0.2,
            # ParameterName.col_horiz_edge_ratio: 0.2,
            ParameterName.total_verti_edge_ratio: 0.1,
            ParameterName.row_verti_edge_ratio: 0.8,
        },
        ParameterName.text_config_dict: {
            ParameterName.font_size: legend_font_size,
            ParameterName.font_weight: FontWeight.bold
        }
    }


class OptimumDistributionComparisonDiagram(CompositeFigure):
    total_width = OptimumDistributionComparisonDiagramConfig.total_width
    total_height = OptimumDistributionComparisonDiagramConfig.total_height
    height_to_width_ratio = total_height / total_width

    def __init__(self, **kwargs):
        common_left = OptimumDistributionComparisonDiagramConfig.left
        upper_bottom = OptimumDistributionComparisonDiagramConfig.upper_bottom
        lower_bottom = OptimumDistributionComparisonDiagramConfig.lower_bottom
        title_box_y_distance = OptimumDistributionComparisonDiagramConfig.title_box_y_distance
        common_optimum_distribution_diagram_config = {
            ParameterName.scale: OptimumDistributionComparisonDiagramConfig.scale,
            ParameterName.base_z_order: OptimumDistributionComparisonDiagramConfig.child_diagram_base_z_order,
            ParameterName.z_order_increment: OptimumDistributionComparisonDiagramConfig.child_diagram_z_order_increment
        }
        upper_optimum_distribution_diagram_config_dict = {
            **common_optimum_distribution_diagram_config,
            ParameterName.distribution_type: ParameterName.one_dominant_global_optimum,
            ParameterName.bottom_left_offset: Vector(common_left, upper_bottom),
        }
        lower_optimum_distribution_diagram_config_dict = {
            **common_optimum_distribution_diagram_config,
            ParameterName.distribution_type: ParameterName.multiple_similar_local_optima,
            ParameterName.bottom_left_offset: Vector(common_left, lower_bottom),
        }
        upper_optimum_distribution_diagram_obj = OptimumDistributionDiagram(
            **upper_optimum_distribution_diagram_config_dict)
        lower_optimum_distribution_diagram_obj = OptimumDistributionDiagram(
            **lower_optimum_distribution_diagram_config_dict)

        upper_title_text_config_dict = {
            **OptimumDistributionComparisonDiagramConfig.title_text_config,
            ParameterName.string: 'One dominant global optimum landscape',
            ParameterName.center: OptimumDistributionComparisonDiagramConfig.upper_title_center
        }
        lower_title_text_config_dict = {
            **OptimumDistributionComparisonDiagramConfig.title_text_config,
            ParameterName.string: 'Multiple similar local optima landscape',
            ParameterName.center: OptimumDistributionComparisonDiagramConfig.lower_title_center
        }
        # upper_explanation_text_config_dict = {
        #     **OptimumDistributionComparisonDiagramConfig.explanation_text_config,
        #     ParameterName.string: 'Local optimal point are either\nnear to global optimum with similar loss\n'
        #                           'or far from that with higher loss',
        #     ParameterName.center: OptimumDistributionComparisonDiagramConfig.upper_explanation_text_center
        # }
        # lower_explanation_text_config_dict = {
        #     **OptimumDistributionComparisonDiagramConfig.explanation_text_config,
        #     ParameterName.string: 'Local optimal point may be\nfar from global optimum with similar loss',
        #     ParameterName.center: OptimumDistributionComparisonDiagramConfig.lower_explanation_text_center
        # }
        text_obj_dict = {
            'upper_title': TextBox(**upper_title_text_config_dict),
            'lower_title': TextBox(**lower_title_text_config_dict),
            # 'upper_explanation': TextBox(**upper_explanation_text_config_dict),
            # 'lower_explanation': TextBox(**lower_explanation_text_config_dict),
        }
        # chevron_obj_dict = {
        #     'upper_arrow': ChevronArrow(**OptimumDistributionComparisonDiagramConfig.lower_chevron_config),
        #     'bottom_arrow': ChevronArrow(**OptimumDistributionComparisonDiagramConfig.upper_chevron_config),
        # }

        legend_obj = common_legend_generator(
            OptimumDistributionComparisonDiagramConfig.legend_config_dict,
            OptimumDistributionDiagramConfig.optimum_with_random_color_dict)
        size = Vector(self.total_width, self.total_height)
        optimum_distribution_comparison_diagram_dict = {
            ParameterName.text: text_obj_dict,
            ParameterName.optimum_distribution_diagram: {
                'upper_optimum_distribution': upper_optimum_distribution_diagram_obj,
                'lower_optimum_distribution': lower_optimum_distribution_diagram_obj},
            # ParameterName.chevron_arrow: chevron_obj_dict,
            ParameterName.legend: {ParameterName.legend: legend_obj},
        }
        super().__init__(
            optimum_distribution_comparison_diagram_dict, Vector(0, 0), size, background=False, **kwargs)


