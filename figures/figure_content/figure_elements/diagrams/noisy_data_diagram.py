from .config import np, Keywords, Vector, ParameterName, ZOrderConfig, TextConfig, HorizontalAlignment, \
    VerticalAlignment, ColorConfig
from .config import BentChevronArrow, ChevronArrow, CompositeFigure, TextBox
from .config import MIDDiagram, CommonElementConfig


class NoisyDataDiagramConfig(object):
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
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: normal_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.z_order: text_z_order,
        # ParameterName.text_box: True,
    }

    mid_title_text_common_config_dict = {
        **document_text_config,
        ParameterName.font_size: 10,
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


class NoisyDataDiagram(CompositeFigure):
    total_width = 1.2
    total_height = 0.5
    height_to_width_ratio = total_height / total_width

    def __init__(self, **kwargs):
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = noisy_data_diagram_generator()
        size = Vector(self.total_width, self.total_height)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, **kwargs)


def generate_evenly_distributed_mid_diagram(
        element_config_list, text_config_list, x_mid_location, data_y_vector, primary_data_array, noise_data_array,
        color_name, mid_diagram_scale, title_text_common_config_dict):
    mid_carbon_num = len(primary_data_array[0])
    primary_data_previous_center_loc = MIDDiagram.calculate_center(
        MIDDiagram, mid_diagram_scale, mid_carbon_num)
    for mid_data_index, primary_mid_data_vector in enumerate(primary_data_array):
        if noise_data_array is not None:
            noise_data_vector = noise_data_array[mid_data_index]
            mid_data_vector = np.array([primary_mid_data_vector, noise_data_vector])
        else:
            mid_data_vector = primary_mid_data_vector
        target_center_vector = Vector(x_mid_location, data_y_vector[mid_data_index])
        predicted_mid_diagram_bottom_left_offset = target_center_vector - primary_data_previous_center_loc
        final_experimental_mid_diagram_dict = {
            ParameterName.data_vector: mid_data_vector,
            ParameterName.scale: mid_diagram_scale,
            ParameterName.color_name: color_name,
            ParameterName.bottom_left_offset: predicted_mid_diagram_bottom_left_offset,
            ParameterName.base_z_order: NoisyDataDiagramConfig.child_diagram_base_z_order,
            ParameterName.z_order_increment: NoisyDataDiagramConfig.child_diagram_z_order_increment
        }
        element_config_list.append((MIDDiagram, final_experimental_mid_diagram_dict))
        text_config_list.append({
            **title_text_common_config_dict,
            ParameterName.string: f'Metabolite {mid_data_index + 1}',
            ParameterName.center: target_center_vector + Vector(0, 0.056),
        })


def noisy_data_diagram_generator():
    main_horiz_axis = 0.22

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    upper_horiz_axis = main_horiz_axis + 0.12
    bottom_horiz_axis = main_horiz_axis - 0.12
    text_horiz_axis = main_horiz_axis + 0.23

    vert_axis_list = [0.11, 0.43, 0.75, 1.08]

    chevron_start_end_x_value_list = [
        Vector(0.22, 0.32),
        Vector(0.54, 0.64),
        Vector(0.86, 0.96),
    ]

    primary_data_array = np.array([
        [0.60, 0.049, 0.051, 0.3],
        [0.37, 0.052, 0.048, 0.53],
        [0.22, 0.043, 0.057, 0.68],
    ])
    noise_data_array = np.array([
        [-0.12, -0.009, 0.006, 0.1],
        [-0.08, 0.005, -0.003, 0.09],
        [0.11, -0.002, -0.008, -0.1]
    ])
    absolute_noise_array = np.abs(noise_data_array)
    primary_data_exclude_noise_array = primary_data_array + np.clip(noise_data_array, None, 0)
    data_include_noise_array = primary_data_array + noise_data_array

    mid_diagram_scale = 0.08
    top_text_distance = 0.015
    mid_data_y_vector = [upper_horiz_axis, main_horiz_axis, bottom_horiz_axis]
    mid_data_height = mid_diagram_scale * MIDDiagram.total_height
    top_text_y_value = upper_horiz_axis + mid_data_height / 2 + top_text_distance

    other_element_config_list = []

    text_config_list = [
        {
            ParameterName.string: 'Precise simulated data',
            ParameterName.center: Vector(vert_axis_list[0], text_horiz_axis),
            **NoisyDataDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Introducing random noise\nand normalization',
            ParameterName.center: Vector(vert_axis_list[1], text_horiz_axis),
            **NoisyDataDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Noisy simulated data',
            ParameterName.center: Vector(vert_axis_list[2], text_horiz_axis),
            **NoisyDataDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'MFA and\nfollowing analysis',
            ParameterName.center: Vector(vert_axis_list[3], main_horiz_axis),
            **NoisyDataDiagramConfig.document_text_config,
        },
    ]

    generate_evenly_distributed_mid_diagram(
        other_element_config_list, text_config_list, vert_axis_list[0], mid_data_y_vector, primary_data_array, None,
        Keywords.blue, mid_diagram_scale, NoisyDataDiagramConfig.mid_title_text_common_config_dict)

    chevron_1_config = {
        ParameterName.tail_end_center: Vector(chevron_start_end_x_value_list[0][0], main_horiz_axis),
        ParameterName.head: Vector(chevron_start_end_x_value_list[0][1], main_horiz_axis),
        **NoisyDataDiagramConfig.chevron_config,
    }

    generate_evenly_distributed_mid_diagram(
        other_element_config_list, text_config_list, vert_axis_list[1], mid_data_y_vector,
        primary_data_exclude_noise_array, absolute_noise_array, [Keywords.blue, Keywords.gray],
        mid_diagram_scale, NoisyDataDiagramConfig.mid_title_text_common_config_dict)

    chevron_2_config = {
        ParameterName.tail_end_center: Vector(chevron_start_end_x_value_list[1][0], main_horiz_axis),
        ParameterName.head: Vector(chevron_start_end_x_value_list[1][1], main_horiz_axis),
        **NoisyDataDiagramConfig.chevron_config,
    }

    generate_evenly_distributed_mid_diagram(
        other_element_config_list, text_config_list, vert_axis_list[2], mid_data_y_vector, data_include_noise_array,
        None, Keywords.orange, mid_diagram_scale, NoisyDataDiagramConfig.mid_title_text_common_config_dict)

    chevron_3_config = {
        ParameterName.tail_end_center: Vector(chevron_start_end_x_value_list[2][0], main_horiz_axis),
        ParameterName.head: Vector(chevron_start_end_x_value_list[2][1], main_horiz_axis),
        **NoisyDataDiagramConfig.chevron_config,
    }

    chevron_arrow_config_list = [chevron_1_config, chevron_2_config, chevron_3_config]

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
