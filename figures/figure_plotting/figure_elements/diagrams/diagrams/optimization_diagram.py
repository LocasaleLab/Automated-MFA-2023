from .config import np, Vector, Keyword, ParameterName, FontWeight
from .config import ArcChevronArrow, ChevronArrow, CompositeFigure, Rectangle, TextBox, RoundRectangle
from .config import MIDDiagram, NetworkDiagram, ZOrderConfig, TextConfig, HorizontalAlignment, VerticalAlignment, \
    ColorConfig, CommonElementConfig, CommonFigureString

from ...common_functions import initialize_vector_input


class OptimizationDiagramConfig(object):
    simulated_height_to_width_ratio = 0.75
    # simulated_height_to_width_ratio = 0.8
    sensitivity_height_to_width_ratio = 0.95
    experimental_height_to_width_ratio = 0.65
    bottom_z_order = ZOrderConfig.default_image_z_order
    normal_document_size = CommonElementConfig.normal_document_size
    smaller_document_size = CommonElementConfig.smaller_document_size
    larger_document_size = CommonElementConfig.larger_document_size
    bottom_document_size = CommonElementConfig.bottom_document_size
    icon_text_size = CommonElementConfig.icon_text_size
    text_z_order = CommonElementConfig.text_z_order
    child_diagram_base_z_order = CommonElementConfig.child_diagram_base_z_order
    child_diagram_z_order_increment = CommonElementConfig.child_diagram_z_order_increment
    equation_text_size = 30

    document_text_width = 0.25
    document_text_height = 0.06

    document_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: normal_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
        ParameterName.vertical_alignment: VerticalAlignment.top,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: text_z_order,
        # ParameterName.text_box: True
    }
    bottom_document_text_config = {
        # ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: bottom_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.z_order: text_z_order,
        # ParameterName.text_box: True
    }

    equation_text_width = 0.12
    equation_text_height = 0.04
    equation_text_config = {
        ParameterName.font_size: equation_text_size,
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
    normal_chevron_width = CommonElementConfig.normal_chevron_width
    arc_chevron_width = CommonElementConfig.arc_chevron_width
    chevron_config = CommonElementConfig.chevron_config

    # simulated_background_config_dict = {
    #     ParameterName.text: TextConfig.main_text_font,
    #     ParameterName.radius: 0.02,
    #     # ParameterName.face_color: ColorConfig.medium_light_blue,
    #     ParameterName.face_color: ColorConfig.medium_light_bright_blue,
    #     ParameterName.edge_width: None,
    #     ParameterName.z_order: bottom_z_order
    # }
    simulated_background_config_dict = CommonElementConfig.simulated_background_config_dict

    no_1_string = CommonFigureString.no_1_string
    no_2_string = CommonFigureString.no_2_string
    no_3_string = CommonFigureString.no_3_string
    sensitivity_box_config_dict = {
        ParameterName.edge_width: 2,
        ParameterName.face_color: None,
        ParameterName.edge_color: ColorConfig.normal_blue,
        ParameterName.z_order: text_z_order,
    }
    sensitivity_box_text_config_dict = {
        ParameterName.font_size: icon_text_size,
        ParameterName.font_color: ColorConfig.normal_blue,
        # ParameterName.font_weight: FontWeight.bold,
        ParameterName.width: 0.05,
        ParameterName.height: 0.05,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: text_z_order,
    }
    sensitivity_text_center_top_left_corner_distance = Vector(0.03, 0.03)


def height_to_width_ratio_calculation(mode):
    if mode == ParameterName.simulated:
        height_to_width_ratio = OptimizationDiagramConfig.simulated_height_to_width_ratio
    elif mode == ParameterName.sensitivity:
        height_to_width_ratio = OptimizationDiagramConfig.sensitivity_height_to_width_ratio
    elif mode == ParameterName.experimental:
        height_to_width_ratio = OptimizationDiagramConfig.experimental_height_to_width_ratio
    else:
        raise ValueError()
    return height_to_width_ratio


class OptimizationDiagram(CompositeFigure):
    total_width = 1

    def __init__(self, mode=ParameterName.simulated, **kwargs):
        height_to_width_ratio = height_to_width_ratio_calculation(mode)
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = optimization_diagram_generator(mode)
        size = Vector(1, height_to_width_ratio)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        mode = args[0]
        self.height_to_width_ratio = height_to_width_ratio_calculation(mode)
        return super().calculate_center(self, scale)


def network_model_and_text(
        network_model_center_y_loc, network_model_text_content, network_model_text_y_offset,
        network_model_scale, network_model_height, network_text_diagram_distance, network_model_x_loc,
        child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list, other_element_config_list):
    network_model_text_y_loc = network_model_center_y_loc + network_model_text_y_offset
    network_model_text_config = {
        ParameterName.string: network_model_text_content,
        ParameterName.center: Vector(
            network_model_x_loc - network_model_scale / 2 - network_text_diagram_distance,
            network_model_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
        ParameterName.font_size: OptimizationDiagramConfig.smaller_document_size
    }
    text_config_list.extend([network_model_text_config])
    scaled_raw_network_model_center = Vector(1, network_model_height) / 2 * network_model_scale
    target_network_model_center = Vector(network_model_x_loc, network_model_center_y_loc)
    network_model_bottom_left_offset = target_network_model_center - scaled_raw_network_model_center
    network_model_config = {
        ParameterName.data_vector: np.array([0.3, 0.05, 0.05, 0.6]),
        ParameterName.scale: network_model_scale,
        ParameterName.bottom_left_offset: network_model_bottom_left_offset,
        ParameterName.base_z_order: child_diagram_base_z_order,
        ParameterName.z_order_increment: child_diagram_z_order_increment
    }
    other_element_config_list.append((NetworkDiagram, network_model_config))


def predicted_mid_and_text(
        experimental_mid_y_loc, experimental_text_content, experimental_text_y_offset,
        mid_diagram_scale, document_text_height, scaled_raw_mid_diagram_center, experimental_mid_x_loc,
        child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list, other_element_config_list):
    experimental_mid_text_y_loc = experimental_mid_y_loc + experimental_text_y_offset \
                                  + MIDDiagram.total_height * mid_diagram_scale / 2 + document_text_height / 2
    experimental_mid_text_config = {
        ParameterName.string: experimental_text_content,
        ParameterName.center: Vector(experimental_mid_x_loc, experimental_mid_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
        ParameterName.font_size: OptimizationDiagramConfig.smaller_document_size
    }
    text_config_list.extend([experimental_mid_text_config])
    target_experimental_mid_diagram_center = Vector(experimental_mid_x_loc, experimental_mid_y_loc)
    experimental_mid_data_vector = np.array([0.4, 0.05, 0.05, 0.5])
    experimental_mid_diagram_bottom_left_offset = target_experimental_mid_diagram_center - scaled_raw_mid_diagram_center
    experimental_mid_diagram_config = {
        ParameterName.data_vector: experimental_mid_data_vector,
        ParameterName.color_name: Keyword.orange,
        ParameterName.scale: mid_diagram_scale,
        ParameterName.bottom_left_offset: experimental_mid_diagram_bottom_left_offset,
        ParameterName.base_z_order: child_diagram_base_z_order,
        ParameterName.z_order_increment: child_diagram_z_order_increment
    }
    other_element_config_list.append((MIDDiagram, experimental_mid_diagram_config))
    return experimental_mid_text_y_loc


def sensitivity_box_text(
        center, width, height, label_content, text_config_list, other_element_config_list):
    box_config_dict = {
        ParameterName.center: center,
        ParameterName.width: width,
        ParameterName.height: height,
        **OptimizationDiagramConfig.sensitivity_box_config_dict,
    }
    text_center = center + Vector(-1, 1) * (
            Vector(width, height) / 2 - OptimizationDiagramConfig.sensitivity_text_center_top_left_corner_distance)
    text_config_dict = {
        ParameterName.string: label_content,
        ParameterName.center: text_center,
        **OptimizationDiagramConfig.sensitivity_box_text_config_dict,
    }
    text_config_list.append(text_config_dict)
    other_element_config_list.append((Rectangle, box_config_dict))


def optimization_diagram_generator(mode):
    height_to_width_ratio = height_to_width_ratio_calculation(mode)
    if mode == ParameterName.simulated:
        main_horiz_axis = 0.57 * height_to_width_ratio
        # main_horiz_axis = 0.534 * height_to_width_ratio
    elif mode == ParameterName.sensitivity:
        main_horiz_axis = 0.43 * height_to_width_ratio
    else:
        main_horiz_axis = 0.63 * height_to_width_ratio

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    main_vert_axis = 0.6
    left_most_vert_axis = main_vert_axis - 0.5  # 0.13
    left_1_vert_axis = main_vert_axis - 0.3  # 0.32
    right_2_vert_axis = main_vert_axis + 0.3  # 0.88

    simulated_text_y_location = height_to_width_ratio - 0.03
    # upper_horiz_axis = main_horiz_axis + 0.24
    upper_horiz_axis = height_to_width_ratio - 0.0825
    # upper_horiz_axis = main_horiz_axis + 0.36
    middle_network_model_center_y_loc = main_horiz_axis + 0.12
    top_network_model_center_y_loc = upper_horiz_axis - 0.12
    middle_experimental_mid_y_loc = main_horiz_axis + 0.09
    top_experimental_mid_y_loc = upper_horiz_axis - 0.04
    bottom_1_horiz_axis = main_horiz_axis - 0.2
    optimization_chevron_arc_y_loc = main_horiz_axis + 0.11
    optimization_chevron_radius = main_horiz_axis + 0.4 - optimization_chevron_arc_y_loc
    bottom_2_horiz_axis = optimization_chevron_arc_y_loc - optimization_chevron_radius
    bottom_most_horiz_axis = bottom_1_horiz_axis - 0.15

    document_equation_text_distance = 0.02
    equation_text_height = OptimizationDiagramConfig.equation_text_height
    document_text_height = OptimizationDiagramConfig.document_text_height
    document_text_width = OptimizationDiagramConfig.document_text_width

    child_diagram_base_z_order = OptimizationDiagramConfig.child_diagram_base_z_order
    child_diagram_z_order_increment = OptimizationDiagramConfig.child_diagram_z_order_increment

    text_config_list = []
    chevron_arrow_config_list = []
    other_element_config_list = []

    if mode == ParameterName.simulated or mode == ParameterName.sensitivity:
        background_top = height_to_width_ratio
        if mode == ParameterName.sensitivity:
            background_height = 0.3
        else:
            background_height = 0.2925
        # background_bottom = height_to_width_ratio - 0.2925
        background_bottom = background_top - background_height
        # background_bottom = main_horiz_axis + 0.03
        background_left = 0.03
        background_right = 0.88
        simulated_background_config_dict = {
            ParameterName.center: Vector(
                (background_left + background_right) / 2, (background_bottom + background_top) / 2),
            ParameterName.width: (background_right - background_left),
            ParameterName.height: (background_top - background_bottom),
            **OptimizationDiagramConfig.simulated_background_config_dict,
        }
        other_element_config_list.append((RoundRectangle, simulated_background_config_dict))
        text_config_list.append({
            ParameterName.string: 'Simulated Data Generation',
            ParameterName.center: Vector(0.4, simulated_text_y_location),
            **OptimizationDiagramConfig.bottom_document_text_config,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            ParameterName.horizontal_alignment: HorizontalAlignment.center,
        })

    main_horiz_axis_document_text_y_loc = main_horiz_axis - equation_text_height / 2 - \
                                          document_equation_text_distance - document_text_height / 2
    initial_flux_text_config = {
        ParameterName.string: 'Random\ninitial flux',
        ParameterName.center: Vector(left_most_vert_axis, main_horiz_axis_document_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
    }
    initial_flux_equation_config = {
        # ParameterName.string: r'$\mathbf{v}_0$',
        ParameterName.string: f'${CommonFigureString.initial_flux}$',
        ParameterName.center: Vector(left_most_vert_axis, main_horiz_axis),
        **OptimizationDiagramConfig.equation_text_config,
    }
    text_config_list.extend([initial_flux_text_config, initial_flux_equation_config])
    normal_equation_text_side_distance = 0.05
    chevron_arrow1_config = {
        ParameterName.tail_end_center: Vector(left_most_vert_axis + normal_equation_text_side_distance,
                                              main_horiz_axis),
        ParameterName.head: Vector(left_1_vert_axis - normal_equation_text_side_distance, main_horiz_axis),
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow_config_list.append(chevron_arrow1_config)

    flux_vector_text_config = {
        ParameterName.string: 'Flux vector',
        ParameterName.center: Vector(left_1_vert_axis, main_horiz_axis_document_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
    }
    flux_vector_equation_config = {
        # ParameterName.string: r'$\mathbf{v}$',
        ParameterName.string: f'${CommonFigureString.flux_vector}$',
        ParameterName.center: Vector(left_1_vert_axis, main_horiz_axis),
        **OptimizationDiagramConfig.equation_text_config,
    }
    text_config_list.extend([flux_vector_text_config, flux_vector_equation_config])
    if mode == ParameterName.sensitivity:
        sensitivity_box_text(
            Vector(left_1_vert_axis, main_horiz_axis - 0.023),
            0.13, 0.1, OptimizationDiagramConfig.no_3_string,
            text_config_list, other_element_config_list)

    network_model_scale = 0.15
    network_model_height = NetworkDiagram.height_to_width_ratio
    network_text_diagram_distance = 0.025
    predicted_mid_side_distance = 0.09
    # middle_network_model_center_y_loc = main_horiz_axis + network_model_height * network_model_scale / 2 + 0.03
    # middle_network_model_center_y_loc = (main_horiz_axis + upper_horiz_axis) / 2
    chevron_arrow_2_tail_x_loc = left_1_vert_axis + normal_equation_text_side_distance
    chevron_arrow_2_head_x_loc = main_vert_axis - predicted_mid_side_distance
    network_model_x_loc = (chevron_arrow_2_tail_x_loc + chevron_arrow_2_head_x_loc) / 2 + 0.01
    if mode == ParameterName.simulated:
        network_model_text_content = 'Network\nmodel'
        network_model_text_y_offset = -0.015
    elif mode == ParameterName.sensitivity:
        network_model_text_content = 'Modified\nnetwork\nmodel'
        network_model_text_y_offset = 0
        sensitivity_box_text(
            Vector(network_model_x_loc - 0.04, middle_network_model_center_y_loc),
            0.25, 0.185, OptimizationDiagramConfig.no_1_string,
            text_config_list, other_element_config_list)
    else:
        network_model_text_content = 'Network\nmodel'
        network_model_text_y_offset = -0.015
    network_model_and_text(
        middle_network_model_center_y_loc, network_model_text_content, network_model_text_y_offset,
        network_model_scale, network_model_height, network_text_diagram_distance, network_model_x_loc,
        child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list, other_element_config_list)

    chevron_arrow2_config = {
        ParameterName.tail_end_center: Vector(chevron_arrow_2_tail_x_loc, main_horiz_axis),
        ParameterName.head: Vector(chevron_arrow_2_head_x_loc, main_horiz_axis),
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow_config_list.append(chevron_arrow2_config)

    predicted_mid_text_config = {
        ParameterName.string: 'Predicted MIDs of\ntarget metabolites',
        ParameterName.center: Vector(main_vert_axis, main_horiz_axis_document_text_y_loc - 0.01),
        **OptimizationDiagramConfig.document_text_config,
        ParameterName.font_size: OptimizationDiagramConfig.smaller_document_size,
    }
    text_config_list.extend([predicted_mid_text_config])
    predicted_mid_main_horiz_distance = 0.01
    mid_diagram_scale = 0.1
    predicted_mid_data_vector = np.array([0.3, 0.05, 0.05, 0.6])
    scaled_raw_mid_diagram_center = Vector(
        MIDDiagram.each_bar_total_width * len(predicted_mid_data_vector),
        MIDDiagram.total_height) / 2 * mid_diagram_scale
    target_predicted_mid_diagram_center = Vector(
        main_vert_axis,
        main_horiz_axis_document_text_y_loc + document_text_height / 2 + predicted_mid_main_horiz_distance
        + mid_diagram_scale * 1.0 / 2
    )
    predicted_mid_diagram_bottom_left_offset = target_predicted_mid_diagram_center - scaled_raw_mid_diagram_center
    predicted_mid_diagram_dict = {
        ParameterName.data_vector: predicted_mid_data_vector,
        ParameterName.scale: mid_diagram_scale,
        ParameterName.bottom_left_offset: predicted_mid_diagram_bottom_left_offset,
        ParameterName.base_z_order: child_diagram_base_z_order,
        ParameterName.z_order_increment: child_diagram_z_order_increment
    }
    other_element_config_list.append((MIDDiagram, predicted_mid_diagram_dict))

    chevron_arrow_3_tail_x_loc = main_vert_axis + predicted_mid_side_distance
    chevron_arrow_3_head_x_loc = right_2_vert_axis - normal_equation_text_side_distance - 0.01
    if mode == ParameterName.simulated:
        experimental_text_content = 'Simulated MIDs of\ntarget metabolites'
        experimental_text_y_offset = -0.01
    elif mode == ParameterName.sensitivity:
        experimental_text_content = 'Selected simulated\nMIDs of target\nmetabolites'
        experimental_text_y_offset = 0.01
    else:
        experimental_text_content = 'Experimental MIDs of\ntarget metabolites'
        experimental_text_y_offset = -0.01
    experimental_mid_x_loc = (chevron_arrow_3_tail_x_loc + chevron_arrow_3_head_x_loc) / 2
    experimental_mid_text_y_loc = predicted_mid_and_text(
        middle_experimental_mid_y_loc, experimental_text_content, experimental_text_y_offset,
        mid_diagram_scale, document_text_height, scaled_raw_mid_diagram_center, experimental_mid_x_loc,
        child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list, other_element_config_list
    )
    if mode == ParameterName.sensitivity:
        sensitivity_box_text(
            Vector(experimental_mid_x_loc, middle_experimental_mid_y_loc + 0.06),
            0.18, 0.24, OptimizationDiagramConfig.no_2_string,
            text_config_list, other_element_config_list)

    chevron_arrow3_config = {
        ParameterName.tail_end_center: Vector(main_vert_axis + predicted_mid_side_distance, main_horiz_axis),
        ParameterName.head: Vector(right_2_vert_axis - normal_equation_text_side_distance - 0.01, main_horiz_axis),
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow_config_list.append(chevron_arrow3_config)

    loss_function_text_config = {
        ParameterName.string: CommonFigureString.loss_function_str,
        ParameterName.center: Vector(right_2_vert_axis, main_horiz_axis_document_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
    }
    loss_function_equation_config = {
        # ParameterName.string: r'$\mathit{L}\mathbf{\left(v\right)}$',
        ParameterName.string: f'${CommonFigureString.loss_function}$',
        ParameterName.center: Vector(right_2_vert_axis, main_horiz_axis),
        **OptimizationDiagramConfig.equation_text_config,
    }
    text_config_list.extend([loss_function_text_config, loss_function_equation_config])

    optimal_flux_vector_text_y_loc = bottom_1_horiz_axis - equation_text_height / 2 + 0.005 \
        - document_equation_text_distance - document_text_height / 2
    optimal_flux_vector_text_config = {
        ParameterName.string: 'Optimal flux vectors\n(Final loss)',
        ParameterName.center: Vector(left_1_vert_axis, optimal_flux_vector_text_y_loc),
        **OptimizationDiagramConfig.document_text_config,
    }
    optimal_flux_vector_equation_config = {
        ParameterName.string: f'${CommonFigureString.optimal_flux_vector}{CommonFigureString.left_parenthesis}'
                              f'{CommonFigureString.final_loss}{CommonFigureString.right_parenthesis}$',
        ParameterName.center: Vector(left_1_vert_axis, bottom_1_horiz_axis),
        **OptimizationDiagramConfig.optimal_flux_and_loss_text_config,
    }
    text_config_list.extend([optimal_flux_vector_text_config, optimal_flux_vector_equation_config])
    chevron_distance = 0.03
    chevron_arrow4_config = {
        ParameterName.tail_end_center: Vector(
            left_1_vert_axis,
            main_horiz_axis_document_text_y_loc + 0.02 - chevron_distance),
        ParameterName.head: Vector(left_1_vert_axis, bottom_1_horiz_axis + chevron_distance + 0.005),
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow_config_list.append(chevron_arrow4_config)

    arc_chevron_width = OptimizationDiagramConfig.arc_chevron_width
    optimization_algorithm_text_config = {
        ParameterName.string: 'Optimization algorithm',
        ParameterName.center: Vector(main_vert_axis, bottom_2_horiz_axis - arc_chevron_width - 0.02),
        **OptimizationDiagramConfig.document_text_config,
        ParameterName.font_size: OptimizationDiagramConfig.larger_document_size
    }
    text_config_list.extend([optimization_algorithm_text_config])
    optimization_chevron_arc_config = {
        ParameterName.center: Vector(main_vert_axis, optimization_chevron_arc_y_loc),
        ParameterName.radius: optimization_chevron_radius,
        ParameterName.theta_tail_end_center: -40,
        ParameterName.theta_head: -140,
        **OptimizationDiagramConfig.chevron_config,
        ParameterName.width: arc_chevron_width
    }
    chevron_arrow_config_list.append(optimization_chevron_arc_config)

    chevron_head_len_width_ratio = OptimizationDiagramConfig.chevron_config[ParameterName.head_len_width_ratio]
    chevron_width = OptimizationDiagramConfig.normal_chevron_width
    chevron_head_len = chevron_width * chevron_head_len_width_ratio
    # 0.5 is parallel with chevron arrow edge
    chevron_arrow_slope1 = 0.25 / chevron_head_len_width_ratio
    if mode == ParameterName.simulated or mode == ParameterName.sensitivity:
        if mode == ParameterName.sensitivity:
            simulated_arrow_horiz_axis = upper_horiz_axis
            simulated_chevron_arrow_break_x_loc = main_vert_axis + 0.055
        elif mode == ParameterName.simulated:
            simulated_arrow_horiz_axis = upper_horiz_axis
            simulated_chevron_arrow_break_x_loc = main_vert_axis + 0.055
        else:
            raise ValueError()

        known_flux_vector_x_loc = left_most_vert_axis
        simulated_chevron_arrow_break_point_coordinate = Vector(
            simulated_chevron_arrow_break_x_loc, simulated_arrow_horiz_axis)
        chevron_break_upper_point = Vector(
            simulated_chevron_arrow_break_x_loc - chevron_head_len, simulated_arrow_horiz_axis + chevron_width / 2)
        simulated_chevron_arrow2_start_location = chevron_break_upper_point \
            - Vector(1, 1 / chevron_arrow_slope1).unit_vector() * chevron_width / 2

        simulated_chevron_arrow1_config = {
            ParameterName.tail_end_center: Vector(known_flux_vector_x_loc + normal_equation_text_side_distance,
                                                  simulated_arrow_horiz_axis),
            ParameterName.head: simulated_chevron_arrow_break_point_coordinate,
            **OptimizationDiagramConfig.chevron_config,
        }
        chevron_arrow_config_list.append(simulated_chevron_arrow1_config)
        if mode == ParameterName.sensitivity:
            current_network_model_text = 'Raw\nnetwork\nmodel'
            current_network_model_text_y_offset = 0
            network_model_and_text(
                top_network_model_center_y_loc, current_network_model_text, current_network_model_text_y_offset,
                network_model_scale, network_model_height, network_text_diagram_distance, network_model_x_loc,
                child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list,
                other_element_config_list)
            current_experimental_text_content = 'Simulated MIDs of\ntarget metabolites'
            predicted_mid_and_text(
                top_experimental_mid_y_loc, current_experimental_text_content, -0.01,
                mid_diagram_scale, document_text_height, scaled_raw_mid_diagram_center, experimental_mid_x_loc,
                child_diagram_base_z_order, child_diagram_z_order_increment, text_config_list, other_element_config_list
            )
            sensitivity_chevron_arrow_x_loc = experimental_mid_x_loc
            sensitivity_chevron_arrow_start_y_loc = top_experimental_mid_y_loc \
                                                    - MIDDiagram.total_height * mid_diagram_scale / 2 - 0.015
            sensitivity_chevron_arrow_end_y_loc = experimental_mid_text_y_loc \
                                                  + document_text_height / 2 + 0.015
            sensitivity_chevron_arrow_config = {
                ParameterName.tail_end_center: Vector(
                    sensitivity_chevron_arrow_x_loc, sensitivity_chevron_arrow_start_y_loc),
                ParameterName.head: Vector(
                    sensitivity_chevron_arrow_x_loc, sensitivity_chevron_arrow_end_y_loc),
                **OptimizationDiagramConfig.chevron_config,
            }
            chevron_arrow_config_list.append(sensitivity_chevron_arrow_config)
        elif mode == ParameterName.simulated:
            simulated_chevron_arrow2_end_y_loc = experimental_mid_text_y_loc + document_text_height / 2 + 0.015
            simulated_chevron_arrow_dy = simulated_chevron_arrow2_end_y_loc - simulated_chevron_arrow2_start_location.y
            simulated_chevron_arrow2_end_location = simulated_chevron_arrow2_start_location + \
                                                    Vector(-1 / chevron_arrow_slope1, 1) * simulated_chevron_arrow_dy
            simulated_chevron_arrow2_config = {
                ParameterName.tail_end_center: simulated_chevron_arrow2_start_location,
                ParameterName.head: simulated_chevron_arrow2_end_location,
                **OptimizationDiagramConfig.chevron_config,
            }
            chevron_arrow_config_list.append(simulated_chevron_arrow2_config)

        known_flux_vector_text_config = {
            ParameterName.string: 'Known flux\nvector',
            ParameterName.center: Vector(
                known_flux_vector_x_loc,
                simulated_arrow_horiz_axis - equation_text_height / 2 -
                document_equation_text_distance - document_text_height / 2),
            **OptimizationDiagramConfig.document_text_config,
        }
        known_flux_vector_equation_config = {
            # ParameterName.string: r'$\mathbf{v^\prime}$',
            ParameterName.string: CommonFigureString.known_flux,
            ParameterName.center: Vector(known_flux_vector_x_loc, simulated_arrow_horiz_axis),
            **OptimizationDiagramConfig.equation_text_config,
        }
        text_config_list.extend([known_flux_vector_text_config, known_flux_vector_equation_config])

    chevron_arrow_slope2 = 0.45 / chevron_head_len_width_ratio
    process_text_left_x_loc = main_vert_axis - 0.13
    chevron_arrow_5_break_point_x_loc = left_1_vert_axis + 0.09
    chevron_arrow_5_1_start_y_loc = optimal_flux_vector_text_y_loc - 0.035
    chevron_arrow_5_break_point_coordinate = Vector(chevron_arrow_5_break_point_x_loc, bottom_most_horiz_axis)
    chevron_break_bottom_point = Vector(
        chevron_arrow_5_break_point_x_loc, bottom_most_horiz_axis - chevron_width / 2)
    chevron_arrow_5_1_end_location = chevron_break_bottom_point \
                                     + Vector(1, 1 / chevron_arrow_slope2).unit_vector() * chevron_width / 2 \
                                     + Vector(1, chevron_arrow_slope2).unit_vector() * Vector(1, -1) * chevron_head_len
    delta_y = chevron_arrow_5_1_start_y_loc - chevron_arrow_5_1_end_location.y
    chevron_arrow_5_1_start_coordinate = chevron_arrow_5_1_end_location + Vector(-1 / chevron_arrow_slope2, 1) * delta_y
    chevron_arrow5_1_config = {
        ParameterName.tail_end_center: chevron_arrow_5_1_start_coordinate,
        ParameterName.head: chevron_arrow_5_1_end_location,
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow5_2_config = {
        ParameterName.tail_end_center: chevron_arrow_5_break_point_coordinate,
        ParameterName.head: Vector(process_text_left_x_loc - 0.01, bottom_most_horiz_axis),
        **OptimizationDiagramConfig.chevron_config,
    }
    chevron_arrow_config_list.extend([chevron_arrow5_1_config, chevron_arrow5_2_config])

    text_center_x_loc = process_text_left_x_loc + document_text_width / 2
    if mode == ParameterName.simulated:
        normal_text_content = 'Compared with known flux vector'
        process_text1_config = {
            ParameterName.string: normal_text_content,
            ParameterName.center: Vector(text_center_x_loc, bottom_most_horiz_axis),
            **OptimizationDiagramConfig.bottom_document_text_config,
        }
        equation_text_size = OptimizationDiagramConfig.equation_text_size
        process_text2_config = {
            # ParameterName.string: r'$\mathbf{v^\prime}$',
            ParameterName.string: CommonFigureString.known_flux,
            ParameterName.center: Vector(
                text_center_x_loc + OptimizationDiagramConfig.bottom_document_size * len(normal_text_content) * 0.00091,
                bottom_most_horiz_axis + equation_text_size * 0.00013),
            **OptimizationDiagramConfig.bottom_document_text_config,
            ParameterName.font_size: equation_text_size
        }
        text_config_list.extend([process_text1_config, process_text2_config])
    else:
        process_text_config = {
            ParameterName.string: 'Analyses of flux solution',
            ParameterName.center: Vector(text_center_x_loc, bottom_most_horiz_axis),
            **OptimizationDiagramConfig.bottom_document_text_config,
        }
        text_config_list.append(process_text_config)

    text_obj_list = []
    for text_config_dict in text_config_list:
        # move_and_scale_parameter_dict(text_config_dict, scale, bottom_left_offset)
        text_obj = TextBox(**text_config_dict)
        text_obj_list.append(text_obj)
    chevron_obj_list = []
    for chevron_arrow_config_dict in chevron_arrow_config_list:
        # move_and_scale_parameter_dict(chevron_arrow_config_dict, scale, bottom_left_offset)
        if ParameterName.radius in chevron_arrow_config_dict:
            chevron_class = ArcChevronArrow
        else:
            chevron_class = ChevronArrow
        chevron_arrow_obj = chevron_class(**chevron_arrow_config_dict)
        chevron_obj_list.append(chevron_arrow_obj)
    other_element_obj_list = []
    for other_element_class, other_element_config in other_element_config_list:
        # move_and_scale_parameter_dict(other_element_config, scale, bottom_left_offset)
        other_element_obj = other_element_class(**other_element_config)
        other_element_obj_list.append(other_element_obj)
    return text_obj_list, chevron_obj_list, other_element_obj_list
