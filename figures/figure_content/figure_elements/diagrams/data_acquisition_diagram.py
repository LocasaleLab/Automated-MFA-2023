from .config import np, Vector, ParameterName, ZOrderConfig, VerticalAlignment, ColorConfig
from .config import BentChevronArrow, ChevronArrow, CompositeFigure, TextBox, RoundRectangle
from .config import MIDDiagram, CulturedCell, Mice, Human, CarbonBackbone, CommonElementConfig


class DataAcquisitionDiagramConfig(object):
    normal_document_size = CommonElementConfig.normal_document_size
    smaller_document_size = normal_document_size - 1
    smallest_document_size = normal_document_size - 4

    text_z_order = CommonElementConfig.text_z_order
    background_z_order = ZOrderConfig.default_patch_z_order
    child_diagram_base_z_order = CommonElementConfig.child_diagram_base_z_order
    child_diagram_z_order_increment = CommonElementConfig.child_diagram_z_order_increment

    document_text_width = 0.18
    document_text_width2 = 0.12
    document_text_height = 0.06
    document_text_height2 = 0.04
    smaller_document_text_height = 0.04

    document_text_config = {
        **CommonElementConfig.common_text_config,
        # ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: normal_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
        # ParameterName.horizontal_alignment: HorizontalAlignment.center,
        # ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        # ParameterName.z_order: text_z_order,
        # ParameterName.text_box: True,
    }

    normal_chevron_width = CommonElementConfig.normal_chevron_width
    chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: normal_chevron_width - 0.015
    }
    bend_chevron_to_main_distance = normal_chevron_width / 2 + 0.015
    bend_chevron_config = {
        **chevron_config,
        ParameterName.radius: 0.03,
        ParameterName.width: normal_chevron_width - 0.02
    }

    predicted_mid_text_config_dict = {
        **document_text_config,
        ParameterName.font_size: smallest_document_size,
        ParameterName.width: document_text_width2,
        ParameterName.height: smaller_document_text_height,
    }

    final_experimental_mid_text_config = {
        **document_text_config,
        ParameterName.font_size: smaller_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height2,
        ParameterName.vertical_alignment: VerticalAlignment.top,
    }

    final_experimental_mid_background_config = {
        ParameterName.radius: 0.05,
        ParameterName.width: document_text_width,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.super_light_blue,
        ParameterName.z_order: background_z_order
    }

    background_rectangle_config_dict = {
        ParameterName.face_color: ColorConfig.light_gray,
        ParameterName.edge_width: None,
        ParameterName.z_order: 0
    }


class DataAcquisitionDiagram(CompositeFigure):
    total_width = 1.2
    height_to_width_ratio = 0.5

    def __init__(self, horiz_or_vertical=ParameterName.horizontal, **kwargs):
        if horiz_or_vertical == ParameterName.horizontal:
            (
                total_width, total_height, text_obj_list, chevron_arrow_obj_list, constructed_obj_list
            ) = data_acquisition_horizontal_diagram_generator()
        elif horiz_or_vertical == ParameterName.vertical:
            (
                total_width, total_height, text_obj_list, chevron_arrow_obj_list, constructed_obj_list
            ) = data_acquisition_vertical_diagram_generator()
        else:
            raise ValueError()
        height_to_width_ratio = total_height / total_width
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = height_to_width_ratio
        size = Vector(total_width, total_height)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, background=False, **kwargs)


def title_text_config_list_generator(common_axis_location, different_axis_location_list, direction):
    if direction == ParameterName.x:
        text_axis_location_list = [
            Vector(different_axis_location, common_axis_location)
            for different_axis_location in different_axis_location_list
        ]
    elif direction == ParameterName.y:
        text_axis_location_list = [
            Vector(common_axis_location, different_axis_location)
            for different_axis_location in different_axis_location_list
        ]
    else:
        raise ValueError()

    title_text_config_list = [
        {
            ParameterName.string: 'Uniformly\n$\mathregular{^{13}}$C-labeled\nglucose',
            ParameterName.center: text_axis_location_list[0],
            **DataAcquisitionDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Labeling\nexperiments',
            ParameterName.center: text_axis_location_list[1],
            **DataAcquisitionDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Mass\nspectrometry',
            ParameterName.center: text_axis_location_list[2],
            **DataAcquisitionDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Experimental\nMID data',
            ParameterName.center: text_axis_location_list[3],
            **DataAcquisitionDiagramConfig.document_text_config,
        },
    ]
    return title_text_config_list


class BranchArrowMode(object):
    branch = 'branch'
    merge = 'merge'
    parallel = 'parallel'


def one_to_three_branch_arrow(
        orientation_axis_name, tail_loc, head_loc, main_axis_loc, side_axis_distance,
        bend_chevron_to_main_distance=0, mode=BranchArrowMode.parallel,
        config_class=DataAcquisitionDiagramConfig):
    if orientation_axis_name == ParameterName.x:
        if head_loc > tail_loc:
            direction = 1
        else:
            direction = -1
    elif orientation_axis_name == ParameterName.y:
        if head_loc > tail_loc:
            direction = -1
        else:
            direction = 1
    else:
        raise ValueError()
    upper_axis_loc = main_axis_loc + direction * side_axis_distance
    bottom_axis_loc = main_axis_loc - direction * side_axis_distance
    upper_chevron_gaped_start_value = main_axis_loc + direction * bend_chevron_to_main_distance
    bottom_chevron_gaped_start_value = main_axis_loc - direction * bend_chevron_to_main_distance
    bend_start = 0.6 * tail_loc + 0.4 * head_loc
    bend_end = 0.5 * tail_loc + 0.5 * head_loc
    if orientation_axis_name == ParameterName.x:
        main_arrow_tail_head_pair = [Vector(tail_loc, main_axis_loc), Vector(head_loc, main_axis_loc)]
    elif orientation_axis_name == ParameterName.y:
        main_arrow_tail_head_pair = [Vector(main_axis_loc, tail_loc), Vector(main_axis_loc, head_loc)]
    else:
        raise ValueError()
    main_arrow_config_dict = {
        ParameterName.tail_end_center: main_arrow_tail_head_pair[0],
        ParameterName.head: main_arrow_tail_head_pair[1],
        **config_class.chevron_config,
    }
    if mode == BranchArrowMode.parallel:
        if orientation_axis_name == ParameterName.x:
            upper_arrow_tail_head_pair = [
                Vector(tail_loc, upper_axis_loc), Vector(head_loc, upper_axis_loc)]
            bottom_arrow_tail_head_pair = [
                Vector(tail_loc, bottom_axis_loc), Vector(head_loc, bottom_axis_loc)]
        elif orientation_axis_name == ParameterName.y:
            upper_arrow_tail_head_pair = [
                Vector(upper_axis_loc, tail_loc), Vector(upper_axis_loc, head_loc)]
            bottom_arrow_tail_head_pair = [
                Vector(bottom_axis_loc, tail_loc), Vector(bottom_axis_loc, head_loc)]
        else:
            raise ValueError()
        chevron_obj_group = [
            main_arrow_config_dict,
            {
                ParameterName.tail_end_center: upper_arrow_tail_head_pair[0],
                ParameterName.head: upper_arrow_tail_head_pair[1],
                **config_class.chevron_config,
            },
            {
                ParameterName.tail_end_center: bottom_arrow_tail_head_pair[0],
                ParameterName.head: bottom_arrow_tail_head_pair[1],
                **config_class.chevron_config,
            }
        ]
    else:
        if mode == BranchArrowMode.branch:
            if orientation_axis_name == ParameterName.x:
                upper_arrow_tail_head_pair = [
                    Vector(bend_start, upper_chevron_gaped_start_value), Vector(head_loc, upper_axis_loc)]
                bottom_arrow_tail_head_pair = [
                    Vector(bend_start, bottom_chevron_gaped_start_value), Vector(head_loc, bottom_axis_loc)]
            elif orientation_axis_name == ParameterName.y:
                upper_arrow_tail_head_pair = [
                    Vector(upper_chevron_gaped_start_value, bend_start), Vector(upper_axis_loc, head_loc)]
                bottom_arrow_tail_head_pair = [
                    Vector(bottom_chevron_gaped_start_value, bend_start), Vector(bottom_axis_loc, head_loc)]
            else:
                raise ValueError()
            specific_dict = {
                ParameterName.tail_arrow: False,
            }
        elif mode == BranchArrowMode.merge:
            if orientation_axis_name == ParameterName.x:
                upper_arrow_tail_head_pair = [
                    Vector(tail_loc, upper_axis_loc), Vector(bend_end, upper_chevron_gaped_start_value)]
                bottom_arrow_tail_head_pair = [
                    Vector(tail_loc, bottom_axis_loc), Vector(bend_end, bottom_chevron_gaped_start_value)]
            elif orientation_axis_name == ParameterName.y:
                upper_arrow_tail_head_pair = [
                    Vector(upper_axis_loc, tail_loc), Vector(upper_chevron_gaped_start_value, bend_end)]
                bottom_arrow_tail_head_pair = [
                    Vector(bottom_axis_loc, tail_loc), Vector(bottom_chevron_gaped_start_value, bend_end)]
            else:
                raise ValueError()
            specific_dict = {
                ParameterName.head_arrow: False,
            }
        else:
            raise ValueError()
        chevron_obj_group = [
            main_arrow_config_dict,
            {
                ParameterName.tail_end_center: upper_arrow_tail_head_pair[0],
                ParameterName.head: upper_arrow_tail_head_pair[1],
                **config_class.bend_chevron_config,
                ParameterName.arrow_head_direction: ParameterName.cw,
                **specific_dict,
            },
            {
                ParameterName.tail_end_center: bottom_arrow_tail_head_pair[0],
                ParameterName.head: bottom_arrow_tail_head_pair[1],
                **config_class.bend_chevron_config,
                ParameterName.arrow_head_direction: ParameterName.ccw,
                **specific_dict,
            }
        ]
    return chevron_obj_group


def carbon_diagram_generator(carbon_labeling_diagram_target_center, carbon_labeling_scale):
    carbon_labeling_diagram_current_center = CarbonBackbone.calculate_center(CarbonBackbone, carbon_labeling_scale)
    carbon_backbone_element_config_list = [
        (
            CarbonBackbone,
            {
                ParameterName.carbon_num: 6,
                ParameterName.scale: carbon_labeling_scale,
                ParameterName.bottom_left_offset:
                    carbon_labeling_diagram_target_center - carbon_labeling_diagram_current_center,
                ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
                ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
            }
        ),
    ]
    return carbon_backbone_element_config_list


def experiment_diagram_generator(
        cultured_cell_target_center, cultured_cell_scale, cultured_cell_text_center,
        mice_target_center, mice_scale, mice_text_center,
        human_target_center, human_scale, human_text_center):
    cultured_cell_current_center = CulturedCell.calculate_center(CulturedCell, cultured_cell_scale)
    mice_current_center = Mice.calculate_center(Mice, mice_scale)
    human_current_center = Human.calculate_center(Human, human_scale)
    diagram_list = [
        (
            CulturedCell,
            {
                ParameterName.scale: cultured_cell_scale,
                ParameterName.bottom_left_offset: cultured_cell_target_center - cultured_cell_current_center,
                ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
                ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
            }
        ),
        (
            Mice,
            {
                ParameterName.scale: mice_scale,
                ParameterName.bottom_left_offset: mice_target_center - mice_current_center,
                ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
                ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
            }
        ),
        (
            Human,
            {
                ParameterName.scale: human_scale,
                ParameterName.bottom_left_offset: human_target_center - human_current_center,
                ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
                ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
            }
        ),
    ]
    text_list = [
        {
            ParameterName.string: 'Cultured cell labeling',
            ParameterName.center: cultured_cell_text_center,
            **DataAcquisitionDiagramConfig.predicted_mid_text_config_dict
        },
        {
            ParameterName.string: 'Animal infusion',
            ParameterName.center: mice_text_center,
            **DataAcquisitionDiagramConfig.predicted_mid_text_config_dict
        },
        {
            ParameterName.string: 'Patient infusion',
            ParameterName.center: human_text_center,
            **DataAcquisitionDiagramConfig.predicted_mid_text_config_dict
        },
    ]
    return diagram_list, text_list


def primary_mid_data_diagram_generator(
        primary_data_mid_diagram_scale, primary_data_center_x_list, primary_data_center_y_list, text_center_list):
    mid_diagram_list = []
    text_config_list = []
    primary_data_vector_list = [
        [0.26, 0.049, 0.051, 0.64],
        [0.37, 0.052, 0.048, 0.53],
        [0.22, 0.043, 0.057, 0.68],
        [0.31, 0.053, 0.047, 0.59],
        [0.27, 0.048, 0.052, 0.63],
        [0.35, 0.056, 0.044, 0.55]
    ]
    row_num = len(primary_data_center_y_list)
    col_num = len(primary_data_center_x_list)
    primary_data_carbon_num = len(primary_data_vector_list[0])
    primary_data_previous_center_loc = MIDDiagram.calculate_center(
        MIDDiagram, primary_data_mid_diagram_scale, primary_data_carbon_num)
    for mid_data_index, primary_data_vector in enumerate(primary_data_vector_list):
        row_index = mid_data_index // col_num
        col_index = mid_data_index % col_num
        target_center_vector = Vector(primary_data_center_x_list[col_index], primary_data_center_y_list[row_index])
        predicted_mid_diagram_bottom_left_offset = target_center_vector - primary_data_previous_center_loc
        final_experimental_mid_diagram_dict = {
            ParameterName.data_vector: np.array(primary_data_vector),
            ParameterName.scale: primary_data_mid_diagram_scale,
            ParameterName.bottom_left_offset: predicted_mid_diagram_bottom_left_offset,
            ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
            ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
        }
        mid_diagram_list.append((MIDDiagram, final_experimental_mid_diagram_dict))
    text_config_list.extend([
        {
            ParameterName.string: 'Lactate',
            ParameterName.center: text_center_list[0],
            **DataAcquisitionDiagramConfig.predicted_mid_text_config_dict
        },
        {
            ParameterName.string: 'Pyruvate',
            ParameterName.center: text_center_list[1],
            **DataAcquisitionDiagramConfig.predicted_mid_text_config_dict
        },
    ])
    return mid_diagram_list, text_config_list


def final_experimental_mid_diagram_generator(final_mid_diagram_target_center):
    mid_diagram_list = []
    text_config_list = []
    final_experimental_mid_diagram_scale = 0.1
    final_experimental_mid_data_vector = np.array([0.3, 0.05, 0.05, 0.6])
    final_mid_diagram_center_x = final_mid_diagram_target_center.x
    final_mid_diagram_center_y = final_mid_diagram_target_center.y
    final_mid_diagram_height = MIDDiagram.total_height * final_experimental_mid_diagram_scale
    final_mid_text_distance = 0.01
    final_mid_text_height = DataAcquisitionDiagramConfig.document_text_height2
    final_mid_total_height = final_mid_diagram_height + final_mid_text_distance + final_mid_text_height
    final_mid_diagram_target_y_value = (
            final_mid_diagram_center_y + (final_mid_text_distance + final_mid_text_height) / 2) - 0.005
    final_mid_bar_plot_target_center = Vector(final_mid_diagram_center_x, final_mid_diagram_target_y_value)
    final_mid_diagram_previous_center = MIDDiagram.calculate_center(
        MIDDiagram, final_experimental_mid_diagram_scale, len(final_experimental_mid_data_vector))
    predicted_mid_diagram_bottom_left_offset = final_mid_bar_plot_target_center - final_mid_diagram_previous_center
    final_experimental_mid_diagram_dict = {
        ParameterName.data_vector: final_experimental_mid_data_vector,
        ParameterName.scale: final_experimental_mid_diagram_scale,
        ParameterName.bottom_left_offset: predicted_mid_diagram_bottom_left_offset,
        ParameterName.base_z_order: DataAcquisitionDiagramConfig.child_diagram_base_z_order,
        ParameterName.z_order_increment: DataAcquisitionDiagramConfig.child_diagram_z_order_increment
    }
    mid_diagram_list.append((MIDDiagram, final_experimental_mid_diagram_dict))
    final_mid_text_center = Vector(
        final_mid_diagram_center_x,
        final_mid_diagram_center_y - (final_mid_diagram_height + final_mid_text_distance) / 2 - 0.005
    )
    text_config_list.append({
        ParameterName.string: 'Experimental\nMID data',
        ParameterName.center: final_mid_text_center,
        **DataAcquisitionDiagramConfig.final_experimental_mid_text_config,
    })
    final_mid_background_config_dict = {
        ParameterName.center: final_mid_diagram_target_center,
        ParameterName.height: final_mid_total_height + 0.06,
        **DataAcquisitionDiagramConfig.final_experimental_mid_background_config,
    }
    mid_diagram_list.append((RoundRectangle, final_mid_background_config_dict))
    return mid_diagram_list, text_config_list


def common_final_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list):
    text_obj_list = []
    for text_config_dict in text_config_list:
        text_obj = TextBox(**text_config_dict)
        text_obj_list.append(text_obj)
    chevron_obj_list = []
    for chevron_arrow_config_dict in chevron_arrow_config_list:
        if ParameterName.radius in chevron_arrow_config_dict:
            chevron_class = BentChevronArrow
        else:
            chevron_class = ChevronArrow
        chevron_arrow_obj = chevron_class(**chevron_arrow_config_dict)
        chevron_obj_list.append(chevron_arrow_obj)
    other_element_obj_list = []
    for other_element_class, other_element_config in other_element_config_list:
        other_element_obj = other_element_class(**other_element_config)
        other_element_obj_list.append(other_element_obj)
    return text_obj_list, chevron_obj_list, other_element_obj_list


def data_acquisition_horizontal_diagram_generator():
    total_width = 1.2
    total_height = 0.6
    main_horiz_axis = 0.43 * total_height
    current_direction = ParameterName.x

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    upper_bottom_to_main_axis_distance = 0.12
    upper_horiz_axis = main_horiz_axis + upper_bottom_to_main_axis_distance
    bottom_horiz_axis = main_horiz_axis - upper_bottom_to_main_axis_distance
    text_horiz_axis = main_horiz_axis + 0.23

    vert_axis_list = [0.1 * total_width, 0.32 * total_width, 0.58 * total_width, 0.9 * total_width]

    chevron_start_end_x_value_list = [
        Vector(0.13, 0.25) * total_width,
        Vector(0.39, 0.47) * total_width,
        Vector(0.69, 0.81) * total_width
    ]

    other_element_config_list = []

    text_config_list = title_text_config_list_generator(text_horiz_axis, vert_axis_list, current_direction)

    bend_chevron_to_main_distance = DataAcquisitionDiagramConfig.bend_chevron_to_main_distance

    chevron_obj_group_1 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[0], main_horiz_axis, upper_bottom_to_main_axis_distance,
        bend_chevron_to_main_distance=bend_chevron_to_main_distance, mode=BranchArrowMode.branch)

    chevron_obj_group_2 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[1], main_horiz_axis, upper_bottom_to_main_axis_distance,
        mode=BranchArrowMode.parallel)

    chevron_obj_group_3 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[2], main_horiz_axis, upper_bottom_to_main_axis_distance,
        bend_chevron_to_main_distance=bend_chevron_to_main_distance, mode=BranchArrowMode.merge)
    chevron_arrow_config_list = [*chevron_obj_group_1, *chevron_obj_group_2, *chevron_obj_group_3]

    carbon_labeling_scale = 0.1
    carbon_labeling_diagram_target_center = Vector(vert_axis_list[0] - 0.01, main_horiz_axis)

    other_element_config_list.extend(
        carbon_diagram_generator(carbon_labeling_diagram_target_center, carbon_labeling_scale))

    cultured_cell_scale = 0.1
    mice_scale = 0.1
    human_scale = 0.1
    labeling_experiments_x_value = vert_axis_list[1]
    cultured_cell_target_center = Vector(labeling_experiments_x_value, upper_horiz_axis - 0.01)
    mice_target_center = Vector(labeling_experiments_x_value, main_horiz_axis - 0.005)
    human_target_center = Vector(labeling_experiments_x_value, bottom_horiz_axis - 0.02)

    cultured_cell_text_center = cultured_cell_target_center + Vector(0, 0.05)
    mice_text_center = mice_target_center + Vector(0, 0.065)
    human_text_center = human_target_center + Vector(0, 0.07)

    experiment_diagram_list, experiment_diagram_text_list = experiment_diagram_generator(
        cultured_cell_target_center, cultured_cell_scale, cultured_cell_text_center,
        mice_target_center, mice_scale, mice_text_center,
        human_target_center, human_scale, human_text_center
    )
    other_element_config_list.extend(experiment_diagram_list)
    text_config_list.extend(experiment_diagram_text_list)

    primary_data_common_x_value = vert_axis_list[2]
    primary_data_mid_diagram_scale = 0.08
    primary_data_vertical_gap = 0.03

    top_text_distance = 0.015
    primary_data_width = primary_data_mid_diagram_scale
    primary_data_x_vector = Vector(-1, 1) * (
            primary_data_width + primary_data_vertical_gap) / 2 + primary_data_common_x_value
    primary_data_y_vector = [upper_horiz_axis, main_horiz_axis, bottom_horiz_axis]
    primary_data_height = primary_data_mid_diagram_scale * MIDDiagram.total_height
    top_text_y_value = upper_horiz_axis + primary_data_height / 2 + top_text_distance

    primary_data_mid_diagram_list, primary_data_text_config_list = primary_mid_data_diagram_generator(
        primary_data_mid_diagram_scale, primary_data_x_vector, primary_data_y_vector,
        [Vector(primary_data_x, top_text_y_value) for primary_data_x in primary_data_x_vector])
    other_element_config_list.extend(primary_data_mid_diagram_list)
    text_config_list.extend(primary_data_text_config_list)

    (
        final_experimental_mid_diagram_list, final_experimental_mid_diagram_text_config_list
    ) = final_experimental_mid_diagram_generator(Vector(vert_axis_list[3], main_horiz_axis))
    other_element_config_list.extend(final_experimental_mid_diagram_list)
    text_config_list.extend(final_experimental_mid_diagram_text_config_list)

    (
        text_obj_list, chevron_obj_list, other_element_obj_list
    ) = common_final_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)
    return total_width, total_height, text_obj_list, chevron_obj_list, other_element_obj_list


def data_acquisition_vertical_diagram_generator():
    total_width = 0.7
    total_height = 1.1
    main_vert_axis = 0.45
    current_direction = ParameterName.y

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    left_right_to_main_axis_distance = 0.15
    right_vert_axis = main_vert_axis + left_right_to_main_axis_distance
    left_vert_axis = main_vert_axis - left_right_to_main_axis_distance
    text_vert_axis = main_vert_axis - 0.35

    horiz_axis_list = [1.05, 0.78, 0.48, 0.12]

    chevron_start_end_x_value_list = [
        Vector(0.97, 0.85),
        Vector(0.70, 0.61),
        Vector(0.34, 0.22),
    ]
    other_element_config_list = []

    text_config_list = title_text_config_list_generator(text_vert_axis, horiz_axis_list, current_direction)

    bend_chevron_to_main_distance = DataAcquisitionDiagramConfig.bend_chevron_to_main_distance
    chevron_obj_group_1 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[0], main_vert_axis, left_right_to_main_axis_distance,
        bend_chevron_to_main_distance=bend_chevron_to_main_distance, mode=BranchArrowMode.branch)

    chevron_obj_group_2 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[1], main_vert_axis, left_right_to_main_axis_distance,
        mode=BranchArrowMode.parallel)

    chevron_obj_group_3 = one_to_three_branch_arrow(
        current_direction, *chevron_start_end_x_value_list[2], main_vert_axis, left_right_to_main_axis_distance,
        bend_chevron_to_main_distance=bend_chevron_to_main_distance, mode=BranchArrowMode.merge)
    chevron_arrow_config_list = [*chevron_obj_group_1, *chevron_obj_group_2, *chevron_obj_group_3]

    carbon_labeling_scale = 0.1
    carbon_labeling_diagram_target_center = Vector(main_vert_axis, horiz_axis_list[0] - 0.01)
    other_element_config_list.extend(
        carbon_diagram_generator(carbon_labeling_diagram_target_center, carbon_labeling_scale))

    common_diagram_scale = 0.1
    labeling_experiments_y_value = horiz_axis_list[1]
    cultured_cell_target_center = Vector(left_vert_axis, labeling_experiments_y_value)
    mice_target_center = Vector(main_vert_axis, labeling_experiments_y_value)
    human_target_center = Vector(right_vert_axis, labeling_experiments_y_value)
    text_y_value = labeling_experiments_y_value + 0.07
    experiment_diagram_list, experiment_diagram_text_list = experiment_diagram_generator(
        cultured_cell_target_center, common_diagram_scale, Vector(cultured_cell_target_center.x, text_y_value),
        mice_target_center, common_diagram_scale, Vector(mice_target_center.x, text_y_value),
        human_target_center, common_diagram_scale, Vector(human_target_center.x, text_y_value)
    )
    other_element_config_list.extend(experiment_diagram_list)
    text_config_list.extend(experiment_diagram_text_list)

    primary_data_common_y_value = horiz_axis_list[2]
    primary_data_mid_diagram_scale = 0.08
    primary_data_vertical_gap = 0.03
    left_text_distance = 0.05
    primary_data_width = primary_data_mid_diagram_scale
    primary_data_height = primary_data_mid_diagram_scale * MIDDiagram.total_height
    primary_data_y_vector = Vector(-1, 1) * (
            primary_data_height + primary_data_vertical_gap) / 2 + primary_data_common_y_value
    primary_data_x_vector = [left_vert_axis, main_vert_axis, right_vert_axis]
    left_text_x_value = left_vert_axis - primary_data_width / 2 - left_text_distance

    primary_data_mid_diagram_list, primary_data_text_config_list = primary_mid_data_diagram_generator(
        primary_data_mid_diagram_scale, primary_data_x_vector, primary_data_y_vector,
        [Vector(left_text_x_value, primary_data_y) for primary_data_y in primary_data_y_vector])
    other_element_config_list.extend(primary_data_mid_diagram_list)
    text_config_list.extend(primary_data_text_config_list)

    (
        final_experimental_mid_diagram_list, final_experimental_mid_diagram_text_config_list
    ) = final_experimental_mid_diagram_generator(Vector(main_vert_axis, horiz_axis_list[3]))
    other_element_config_list.extend(final_experimental_mid_diagram_list)
    text_config_list.extend(final_experimental_mid_diagram_text_config_list)

    (
        text_obj_list, chevron_obj_list, other_element_obj_list
    ) = common_final_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)
    return total_width, total_height, text_obj_list, chevron_obj_list, other_element_obj_list



