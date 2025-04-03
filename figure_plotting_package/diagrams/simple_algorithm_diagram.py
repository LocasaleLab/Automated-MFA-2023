from .config import warnings, np, Vector, ParameterName, ZOrderConfig, ColorConfig, JoinStyle, VerticalAlignment, \
    HorizontalAlignment, common_text_config_dict
from .config import (
    CompositeFigure, Rectangle, TextBox, ArcChevronArrow, ChevronArrow, ChevronArrowArcEnd, RoundRectangle)


class SimpleAlgorithmDiagramConfig(object):
    simulated_height_to_width_ratio = 0.75
    sensitivity_height_to_width_ratio = 0.95
    experimental_height_to_width_ratio = 0.65
    bottom_z_order = ZOrderConfig.default_image_z_order
    normal_document_size = 17
    larger_document_size = normal_document_size + 2
    icon_text_size = 25
    text_z_order = ZOrderConfig.default_text_z_order
    equation_text_size = 30

    document_text_width = 0.25
    document_text_height = 0.06

    document_text_config = {
        **common_text_config_dict,
        ParameterName.font_size: larger_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
    }

    equation_text_width = 0.12
    equation_text_height = 0.04
    equation_text_config = {
        ParameterName.font_size: 30,
        ParameterName.width: equation_text_width,
        ParameterName.height: equation_text_height,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: text_z_order,
        # ParameterName.text_box: True
    }
    optimal_flux_and_loss_text_config = {
        **equation_text_config,
        ParameterName.font_size: equation_text_size - 3
    }
    normal_chevron_width = 0.06
    arc_chevron_width = 0.06
    chevron_config = {
        ParameterName.head_len_width_ratio: 0.4,
        ParameterName.width: normal_chevron_width,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.light_bright_sky,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order,
    }
    background_config = {
        ParameterName.edge_width: None,
        ParameterName.radius: 0.13,
        ParameterName.z_order: ZOrderConfig.default_image_z_order,
        ParameterName.face_color: ColorConfig.medium_light_blue,
    }


class SimpleAlgorithmDiagram(CompositeFigure):
    total_width = 0.55
    total_height = 0.9
    height_to_width_ratio = total_height / total_width

    def __init__(self, **kwargs):
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = optimization_diagram_generator(
            self.total_width, self.total_height)
        size = Vector(self.total_width, self.total_height)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, background=False, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) / 2 * scale


def optimization_diagram_generator(total_width, total_height):
    text_config_list = []
    chevron_arrow_config_list = []
    other_element_config_list = []

    main_x_loc = 0.275
    main_y_loc = 0.45
    arc_center = Vector(main_x_loc, main_y_loc)
    arc_radius = 0.12
    arc_chevron_width = SimpleAlgorithmDiagramConfig.arc_chevron_width
    chevron_arc_radius = arc_radius + arc_chevron_width / 2 + 0.015
    initial_center = Vector(main_x_loc, main_y_loc + 0.33)
    initial_arrow_end_center = arc_center + Vector(0, arc_radius - 0.05)
    flux_vector_center = Vector(main_x_loc - 0.115, main_y_loc + 0.075)
    loss_center = Vector(main_x_loc + 0.11, main_y_loc - 0.1)
    optimal_flux_center = Vector(main_x_loc, main_y_loc - 0.365)
    optimal_arrow_start_center = arc_center + Vector(0, -arc_radius + 0.05)
    prediction_text_center = arc_center + Vector(arc_radius + 0.05, arc_radius + 0.02)
    optimization_text_center = arc_center + Vector(-arc_radius - 0.05, -arc_radius - 0.02)

    initial_flux_text_config = {
        ParameterName.string: 'Random initial flux',
        ParameterName.center: initial_center + Vector(0, 0.04),
        **SimpleAlgorithmDiagramConfig.document_text_config,
    }
    initial_flux_equation_config = {
        ParameterName.string: r'$\mathbf{v}_0$',
        ParameterName.center: initial_center,
        **SimpleAlgorithmDiagramConfig.equation_text_config,
    }
    text_config_list.extend([initial_flux_text_config, initial_flux_equation_config])
    chevron_arrow_config_list.append({
        ParameterName.tail_end_center: initial_center + Vector(0, -0.05),
        ParameterName.head: initial_arrow_end_center,
        ParameterName.center: arc_center,
        ParameterName.radius: chevron_arc_radius,
        ParameterName.tail_or_head: ParameterName.head,
        **SimpleAlgorithmDiagramConfig.chevron_config,
    })

    flux_vector_text_config = {
        ParameterName.string: 'Flux vector',
        ParameterName.center: flux_vector_center + Vector(0, 0.03),
        **SimpleAlgorithmDiagramConfig.document_text_config,
    }
    flux_vector_equation_config = {
        ParameterName.string: r'$\mathbf{v}$',
        ParameterName.center: flux_vector_center,
        **SimpleAlgorithmDiagramConfig.equation_text_config,
    }
    text_config_list.extend([flux_vector_text_config, flux_vector_equation_config])

    loss_function_text_config = {
        ParameterName.string: 'Loss value',
        ParameterName.center: loss_center + Vector(0, 0.04),
        **SimpleAlgorithmDiagramConfig.document_text_config,
    }
    loss_function_equation_config = {
        ParameterName.string: r'$\mathit{L}\mathrm{(}\mathbf{v}\mathrm{)}$',
        ParameterName.center: loss_center,
        **SimpleAlgorithmDiagramConfig.equation_text_config,
    }
    text_config_list.extend([loss_function_text_config, loss_function_equation_config])

    optimal_flux_vector_text_config = {
        ParameterName.string: 'Optimal flux vectors (Final loss)',
        ParameterName.center: optimal_flux_center + Vector(0, 0.05),
        **SimpleAlgorithmDiagramConfig.document_text_config,
    }
    optimal_flux_vector_equation_config = {
        ParameterName.string: r'$\mathbf{v}\mathit{^*}\mathrm{(}\mathit{L^*}\mathrm{)}$',
        ParameterName.center: optimal_flux_center,
        **SimpleAlgorithmDiagramConfig.optimal_flux_and_loss_text_config,
    }
    text_config_list.extend([optimal_flux_vector_text_config, optimal_flux_vector_equation_config])
    chevron_arrow_config_list.append({
        ParameterName.tail_end_center: optimal_arrow_start_center,
        ParameterName.head: optimal_flux_center + Vector(0, 0.08),
        ParameterName.center: arc_center,
        ParameterName.radius: chevron_arc_radius,
        ParameterName.tail_or_head: ParameterName.tail,
        **SimpleAlgorithmDiagramConfig.chevron_config,
    })

    optimization_algorithm_text_config = {
        ParameterName.string: 'Optimization\nalgorithm',
        ParameterName.center: optimization_text_center,
        **SimpleAlgorithmDiagramConfig.document_text_config,
        ParameterName.font_size: SimpleAlgorithmDiagramConfig.normal_document_size
    }
    text_config_list.extend([optimization_algorithm_text_config])
    chevron_arrow_config_list.append({
        **SimpleAlgorithmDiagramConfig.chevron_config,
        ParameterName.center: arc_center,
        ParameterName.radius: arc_radius,
        ParameterName.theta_tail_end_center: 115,
        ParameterName.theta_head: -20,
        ParameterName.width: arc_chevron_width
    })

    optimization_algorithm_text_config = {
        ParameterName.string: 'Prediction\nalgorithm',
        ParameterName.center: prediction_text_center,
        **SimpleAlgorithmDiagramConfig.document_text_config,
        ParameterName.font_size: SimpleAlgorithmDiagramConfig.normal_document_size
    }
    text_config_list.extend([optimization_algorithm_text_config])
    chevron_arrow_config_list.append({
        **SimpleAlgorithmDiagramConfig.chevron_config,
        ParameterName.center: arc_center,
        ParameterName.radius: arc_radius,
        ParameterName.theta_tail_end_center: -65,
        ParameterName.theta_head: -200,
        ParameterName.width: arc_chevron_width
    })
    other_element_config_list.append((RoundRectangle, {
        **SimpleAlgorithmDiagramConfig.background_config,
        ParameterName.center: Vector(total_width, total_height) / 2,
        ParameterName.width: total_width * 0.95,
        ParameterName.height: total_height * 0.95,
    }))

    text_obj_list = []
    for text_config_dict in text_config_list:
        text_obj = TextBox(**text_config_dict)
        text_obj_list.append(text_obj)
    chevron_obj_list = []
    for chevron_arrow_config_dict in chevron_arrow_config_list:
        if ParameterName.tail_or_head in chevron_arrow_config_dict:
            chevron_class = ChevronArrowArcEnd
        elif ParameterName.radius in chevron_arrow_config_dict:
            chevron_class = ArcChevronArrow
        else:
            chevron_class = ChevronArrow
        chevron_arrow_obj = chevron_class(**chevron_arrow_config_dict)
        chevron_obj_list.append(chevron_arrow_obj)
    other_element_obj_list = []
    for other_element_class, other_element_config in other_element_config_list:
        other_element_obj = other_element_class(**other_element_config)
        other_element_obj_list.append(other_element_obj)
    return text_obj_list, chevron_obj_list, other_element_obj_list


class AlgorithmOutlineDiagramConfig(object):
    normal_chevron_width = 0.08
    arc_chevron_width = 0.07
    chevron_config = {
        ParameterName.head_len_width_ratio: 0.4,
        ParameterName.width: arc_chevron_width,
        ParameterName.edge_width: 6,
        ParameterName.edge_color: ColorConfig.black_color,
        ParameterName.face_color: None,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order,
    }


class AlgorithmOutlineDiagram(CompositeFigure):
    total_width = 0.3
    total_height = 0.45
    height_to_width_ratio = total_height / total_width

    def __init__(self, **kwargs):
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = outline_diagram_generator(
            self.total_width, self.total_height)
        size = Vector(self.total_width, self.total_height)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, background=False, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) / 2 * scale


def outline_diagram_generator(total_width, total_height):
    text_config_list = []
    chevron_arrow_config_list = []
    other_element_config_list = []

    main_x_loc = 0.15
    main_y_loc = 0.23
    arc_center = Vector(main_x_loc, main_y_loc)
    arc_radius = 0.08
    arc_chevron_width = AlgorithmOutlineDiagramConfig.arc_chevron_width
    # chevron_arc_radius = arc_radius + arc_chevron_width / 2 + 0.015
    chevron_arc_radius = arc_radius + arc_chevron_width / 2
    initial_arrow_start_center = Vector(main_x_loc, main_y_loc + 0.20)
    initial_arrow_end_center = arc_center + Vector(0, arc_radius - 0.06)
    optimal_arrow_start_center = arc_center + Vector(0, -arc_radius + 0.06)
    optimal_arrow_end_center = Vector(main_x_loc, main_y_loc - 0.205)

    chevron_arrow_config_list.extend([{
        **AlgorithmOutlineDiagramConfig.chevron_config,
        ParameterName.tail_end_center: initial_arrow_start_center,
        ParameterName.head: initial_arrow_end_center,
        ParameterName.center: arc_center,
        ParameterName.radius: chevron_arc_radius,
        ParameterName.tail_or_head: ParameterName.head,
        ParameterName.width: AlgorithmOutlineDiagramConfig.normal_chevron_width,
    }, {
        **AlgorithmOutlineDiagramConfig.chevron_config,
        ParameterName.tail_end_center: optimal_arrow_start_center,
        ParameterName.head: optimal_arrow_end_center,
        ParameterName.center: arc_center,
        ParameterName.radius: chevron_arc_radius,
        ParameterName.tail_or_head: ParameterName.tail,
        ParameterName.width: AlgorithmOutlineDiagramConfig.normal_chevron_width,
    }, {
        **AlgorithmOutlineDiagramConfig.chevron_config,
        ParameterName.center: arc_center,
        ParameterName.radius: arc_radius,
        ParameterName.theta_tail_end_center: 150,
        ParameterName.theta_head: -50,
        ParameterName.width: arc_chevron_width
    }, {
        **AlgorithmOutlineDiagramConfig.chevron_config,
        ParameterName.center: arc_center,
        ParameterName.radius: arc_radius,
        ParameterName.theta_tail_end_center: -30,
        ParameterName.theta_head: -230,
        ParameterName.width: arc_chevron_width
    }])

    text_obj_list = []
    for text_config_dict in text_config_list:
        text_obj = TextBox(**text_config_dict)
        text_obj_list.append(text_obj)
    chevron_obj_list = []
    for chevron_arrow_config_dict in chevron_arrow_config_list:
        if ParameterName.tail_or_head in chevron_arrow_config_dict:
            chevron_class = ChevronArrowArcEnd
        elif ParameterName.radius in chevron_arrow_config_dict:
            chevron_class = ArcChevronArrow
        else:
            chevron_class = ChevronArrow
        chevron_arrow_obj = chevron_class(**chevron_arrow_config_dict)
        chevron_obj_list.append(chevron_arrow_obj)
    other_element_obj_list = []
    for other_element_class, other_element_config in other_element_config_list:
        other_element_obj = other_element_class(**other_element_config)
        other_element_obj_list.append(other_element_obj)
    return text_obj_list, chevron_obj_list, other_element_obj_list
