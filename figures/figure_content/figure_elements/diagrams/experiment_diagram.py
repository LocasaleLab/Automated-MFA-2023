from .config import np, Vector, ParameterName, ZOrderConfig, TextConfig, HorizontalAlignment, \
    VerticalAlignment, FontStyle, ColorConfig, DataName, FontWeight
from .config import BentChevronArrow, ChevronArrow, CompositeFigure, Rectangle, TextBox, RoundRectangle
from .config import MIDDiagram, NetworkDiagram, CulturedCell, Mice, Human, CarbonBackbone, CommonElementConfig


class ExperimentDiagramConfig(object):
    total_size_dict = {
        DataName.renal_carcinoma_invivo_infusion: Vector(0.5, 0.5),
        DataName.multiple_tumor: Vector(1, 0.52),
        DataName.colon_cancer_cell_line: Vector(0.8, 0.5),
    }

    normal_document_size = CommonElementConfig.normal_document_size
    smaller_document_size = normal_document_size - 3
    smallest_document_size = normal_document_size - 4

    document_text_width = 0.18
    document_text_width2 = 0.12
    document_text_height = 0.06
    document_text_height2 = 0.04
    smaller_document_text_height = 0.04

    human_diagram_scale = 0.15
    cultured_cell_scale = 0.2

    document_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: smaller_document_size,
        ParameterName.width: document_text_width,
        ParameterName.height: document_text_height,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.z_order: CommonElementConfig.text_z_order,
        # ParameterName.text_box: True,
    }

    normal_chevron_width = CommonElementConfig.normal_chevron_width
    bend_chevron_to_main_distance = normal_chevron_width / 2 + 0.013
    chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: normal_chevron_width - 0.015
    }
    bend_chevron_config = {
        **chevron_config,
        ParameterName.radius: 0.03,
        ParameterName.width: normal_chevron_width - 0.019
    }
    common_human_diagram_config = {
        ParameterName.scale: human_diagram_scale,
        ParameterName.base_z_order: ZOrderConfig.default_patch_z_order,
        ParameterName.z_order_increment: ZOrderConfig.z_order_increment
    }
    common_cultured_cell_diagram_config = {
        ParameterName.scale: cultured_cell_scale,
        ParameterName.base_z_order: ZOrderConfig.default_patch_z_order,
        ParameterName.z_order_increment: ZOrderConfig.z_order_increment
    }


class ExperimentDiagram(CompositeFigure):
    @staticmethod
    def calculate_total_size(data_name):
        return ExperimentDiagramConfig.total_size_dict[data_name]

    @staticmethod
    def calculate_center(self, scale, *args):
        data_name = args[0]
        return self.calculate_total_size(data_name) * scale / 2

    def __init__(self, data_name, **kwargs):
        total_size = self.calculate_total_size(data_name)
        if data_name == DataName.renal_carcinoma_invivo_infusion:
            layout_function = kidney_carcinoma_experiment_diagram_generator
        elif data_name == DataName.multiple_tumor:
            layout_function = multi_tumor_experiment_diagram_generator
        elif data_name == DataName.colon_cancer_cell_line:
            layout_function = colon_cancer_experiment_diagram_generator
        else:
            raise ValueError()

        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = layout_function()
        experiment_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(experiment_diagram_dict, Vector(0, 0), total_size, background=False, **kwargs)


def obj_list_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list):
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


def kidney_carcinoma_experiment_diagram_generator():
    # total width = 0.5, total height = 0.5
    total_width, total_height = ExperimentDiagramConfig.total_size_dict[DataName.renal_carcinoma_invivo_infusion]

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    upper_horiz_axis = 0.35
    upper_text_horiz_axis = upper_horiz_axis + 0.11
    middle_text_horiz_axis = 0.19
    bottom_text_horiz_axis = 0.05

    left_vert_axis = 0.1
    middle_right_vert_axis = 0.35
    middle_left_vert_axis = 0.25
    right_vert_axis = 0.45

    text_config_list = [
        {
            ParameterName.string: 'Patient with\nkidney tumor',
            ParameterName.center: Vector(left_vert_axis, upper_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Infuse with U-$\mathregular{^{13}}$C-glucose\nfor ~2.5 hours',
            ParameterName.center: Vector(middle_right_vert_axis, upper_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Normal\nkidney tissue',
            ParameterName.center: Vector(middle_left_vert_axis, middle_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Kidney\ntumors',
            ParameterName.center: Vector(right_vert_axis, middle_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Mass spectrometry',
            ParameterName.center: Vector(middle_right_vert_axis, bottom_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Data from Courtney et al,\nCell Metabolism, 2018',
            ParameterName.center: Vector(left_vert_axis + 0.01, bottom_text_horiz_axis + 0.03),
            **ExperimentDiagramConfig.document_text_config,
            ParameterName.font_size: ExperimentDiagramConfig.smallest_document_size,
            ParameterName.horizontal_alignment: HorizontalAlignment.left,
            ParameterName.font_style: FontStyle.italic
        },
    ]

    normal_chevron_width = 0.07
    upper_chevron_middle = (left_vert_axis + middle_right_vert_axis) / 2
    upper_chevron_tail_x_value = upper_chevron_middle - normal_chevron_width / 2
    upper_chevron_head_x_value = upper_chevron_middle + normal_chevron_width / 2
    chevron_config_dict_1 = {
        ParameterName.tail_end_center: Vector(upper_chevron_tail_x_value, upper_horiz_axis),
        ParameterName.head: Vector(upper_chevron_head_x_value, upper_horiz_axis),
        **ExperimentDiagramConfig.chevron_config,
    }

    split_merge_chevron_middle = (middle_left_vert_axis + right_vert_axis) / 2
    left_chevron_inner_x_value = split_merge_chevron_middle - 0.03
    right_chevron_inner_x_value = split_merge_chevron_middle + 0.03
    left_chevron_outer_x_value = middle_left_vert_axis + 0.03
    right_chevron_outer_x_value = right_vert_axis - 0.03
    upper_chevron_upper_y_value = upper_horiz_axis - 0.09
    upper_chevron_bottom_y_value = middle_text_horiz_axis + 0.03
    bottom_chevron_upper_y_value = middle_text_horiz_axis - 0.05
    bottom_chevron_bottom_y_value = bottom_text_horiz_axis + 0.04

    split_merge_chevron_config_dict_list = [
        {
            ParameterName.tail_end_center: Vector(left_chevron_inner_x_value, upper_chevron_upper_y_value),
            ParameterName.head: Vector(left_chevron_outer_x_value, upper_chevron_bottom_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(right_chevron_inner_x_value, upper_chevron_upper_y_value),
            ParameterName.head: Vector(right_chevron_outer_x_value, upper_chevron_bottom_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(left_chevron_outer_x_value, bottom_chevron_upper_y_value),
            ParameterName.head: Vector(left_chevron_inner_x_value, bottom_chevron_bottom_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(right_chevron_outer_x_value, bottom_chevron_upper_y_value),
            ParameterName.head: Vector(right_chevron_inner_x_value, bottom_chevron_bottom_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
    ]

    chevron_arrow_config_list = [chevron_config_dict_1, *split_merge_chevron_config_dict_list]

    human_current_center = Human.calculate_center(Human, ExperimentDiagramConfig.human_diagram_scale)
    kidney_tumor_label = 'Kidney tumor'
    human_config_list = [
        {
            **ExperimentDiagramConfig.common_human_diagram_config,
            ParameterName.bottom_left_offset: Vector(left_vert_axis, upper_horiz_axis) - human_current_center,
            ParameterName.infusion: False,
            ParameterName.text_label: kidney_tumor_label,
        },
        {
            **ExperimentDiagramConfig.common_human_diagram_config,
            ParameterName.bottom_left_offset: Vector(middle_right_vert_axis, upper_horiz_axis) - human_current_center,
            ParameterName.text_label: kidney_tumor_label,
        }
    ]
    other_element_config_list = [(Human, human_config) for human_config in human_config_list]
    return obj_list_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)


def multi_tumor_experiment_diagram_generator():
    # total width = 1, total height = 0.4
    total_width, total_height = ExperimentDiagramConfig.total_size_dict[DataName.multiple_tumor]

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    upper_horiz_axis = 0.38
    middle_horiz_axis = 0.24
    bottom_horiz_axis = 0.1
    upper_text_horiz_axis = upper_horiz_axis + 0.11
    horiz_axis_list = [upper_horiz_axis, middle_horiz_axis, bottom_horiz_axis]

    left_vert_axis = 0.1
    middle_left_vert_axis = 0.4
    middle_right_vert_axis = 0.6
    right_vert_axis = 0.9

    text_config_list = [
        {
            ParameterName.string: 'Different patients with\ndifferent tumors',
            ParameterName.center: Vector(left_vert_axis, upper_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Infuse with U-$\mathregular{^{13}}$C-glucose\nfor ~2.5 hours',
            ParameterName.center: Vector(middle_left_vert_axis, upper_text_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Kidney\ntumors',
            ParameterName.center: Vector(middle_right_vert_axis, upper_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Lung\ntumors',
            ParameterName.center: Vector(middle_right_vert_axis, middle_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Brain\ntumors',
            ParameterName.center: Vector(middle_right_vert_axis, bottom_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        {
            ParameterName.string: 'Mass spectrometry',
            ParameterName.center: Vector(right_vert_axis, middle_horiz_axis),
            **ExperimentDiagramConfig.document_text_config,
        },
        # {
        #     ParameterName.string: 'Data from Courtney et al, Cell Metabolism, 2018 and Faubert et al, Cell, 2017',
        #     ParameterName.center: Vector(left_vert_axis + 0.01, bottom_horiz_axis - 0.08),
        #     **ExperimentDiagramConfig.document_text_config,
        #     ParameterName.font_size: ExperimentDiagramConfig.smallest_document_size,
        #     ParameterName.horizontal_alignment: HorizontalAlignment.left,
        #     ParameterName.font_style: FontStyle.italic
        # },
    ]

    normal_chevron_len = 0.07
    half_normal_chevron_len = normal_chevron_len / 2
    left_chevron_middle = (left_vert_axis + middle_left_vert_axis) / 2
    middle_left_chevron_middle = (middle_left_vert_axis + middle_right_vert_axis) / 2
    middle_right_chevron_middle = (middle_right_vert_axis + right_vert_axis) / 2 - 0.015
    half_middle_right_chevron_len = 0.07
    left_chevron_start_end_x_value_pair = (
        left_chevron_middle - half_normal_chevron_len,
        left_chevron_middle + half_normal_chevron_len
    )
    middle_left_chevron_start_end_x_value_pair = (
        middle_left_chevron_middle - half_normal_chevron_len,
        middle_left_chevron_middle + half_normal_chevron_len
    )
    middle_right_chevron_start_end_x_value_pair = (
        middle_right_chevron_middle - half_middle_right_chevron_len,
        middle_right_chevron_middle + half_middle_right_chevron_len
    )
    bent_chevron_end_x_loc = middle_right_chevron_middle
    bend_chevron_to_main_distance = ExperimentDiagramConfig.bend_chevron_to_main_distance
    bent_chevron_start_end_y_value_pair = (
        middle_horiz_axis + bend_chevron_to_main_distance,
        middle_horiz_axis - bend_chevron_to_main_distance,
    )

    left_chevron_config_list = [
        {
            ParameterName.tail_end_center: Vector(left_chevron_start_end_x_value_pair[0], horiz_axis),
            ParameterName.head: Vector(left_chevron_start_end_x_value_pair[1], horiz_axis),
            **ExperimentDiagramConfig.chevron_config,
        }
        for horiz_axis in horiz_axis_list
    ]
    middle_left_chevron_config_list = [
        {
            ParameterName.tail_end_center: Vector(middle_left_chevron_start_end_x_value_pair[0], horiz_axis),
            ParameterName.head: Vector(middle_left_chevron_start_end_x_value_pair[1], horiz_axis),
            **ExperimentDiagramConfig.chevron_config,
        }
        for horiz_axis in horiz_axis_list
    ]

    merge_chevron_config_group = [
        {
            ParameterName.tail_end_center: Vector(middle_right_chevron_start_end_x_value_pair[0], middle_horiz_axis),
            ParameterName.head: Vector(middle_right_chevron_start_end_x_value_pair[1], middle_horiz_axis),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(middle_right_chevron_start_end_x_value_pair[0], upper_horiz_axis),
            ParameterName.head: Vector(bent_chevron_end_x_loc, bent_chevron_start_end_y_value_pair[0]),
            **ExperimentDiagramConfig.bend_chevron_config,
            ParameterName.head_arrow: False,
            ParameterName.arrow_head_direction: ParameterName.cw
        },
        {
            ParameterName.tail_end_center: Vector(middle_right_chevron_start_end_x_value_pair[0], bottom_horiz_axis),
            ParameterName.head: Vector(bent_chevron_end_x_loc, bent_chevron_start_end_y_value_pair[1]),
            **ExperimentDiagramConfig.bend_chevron_config,
            ParameterName.head_arrow: False,
            ParameterName.arrow_head_direction: ParameterName.ccw
        }
    ]

    chevron_arrow_config_list = left_chevron_config_list + middle_left_chevron_config_list + merge_chevron_config_group

    human_text_label_list = ['Kidney tumor', 'Lung tumor', 'Brain tumor']
    human_current_center = Human.calculate_center(Human, ExperimentDiagramConfig.human_diagram_scale)
    left_human_config_list = [
        {
            **ExperimentDiagramConfig.common_human_diagram_config,
            ParameterName.infusion: False,
            ParameterName.text_label: text_label,
            ParameterName.bottom_left_offset: Vector(left_vert_axis, horiz_axis) - human_current_center,
        }
        for text_label, horiz_axis in zip(human_text_label_list, horiz_axis_list)
    ]
    middle_left_human_config_list = [
        {
            **ExperimentDiagramConfig.common_human_diagram_config,
            ParameterName.text_label: text_label,
            ParameterName.bottom_left_offset: Vector(middle_left_vert_axis, horiz_axis) - human_current_center,
        }
        for text_label, horiz_axis in zip(human_text_label_list, horiz_axis_list)
    ]

    human_config_list = left_human_config_list + middle_left_human_config_list
    other_element_config_list = [(Human, human_config) for human_config in human_config_list]
    return obj_list_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)


def colon_cancer_experiment_diagram_generator():
    # total width = 0.5, total height = 0.5
    total_width, total_height = ExperimentDiagramConfig.total_size_dict[DataName.colon_cancer_cell_line]

    # width = 1, height = height_to_width_ratio, all absolute number are relative to width
    upper_horiz_axis = 0.3
    upper_text_horiz_axis = upper_horiz_axis + 0.08
    main_horiz_axis = 0.2
    main_text_horiz_axis = main_horiz_axis + 0.09
    bottom_horiz_axis = 0.1
    middle_text_horiz_axis = 0.19
    bottom_text_horiz_axis = 0.05

    left_vert_axis = 0.12
    middle_vert_axis = 0.42
    right_vert_axis = 0.7

    current_text_config = {
        **ExperimentDiagramConfig.document_text_config,
        ParameterName.font_size: ExperimentDiagramConfig.normal_document_size - 1,
    }
    text_config_list = [
        {
            ParameterName.string: '8 colon cancer\ncell lines',
            ParameterName.center: Vector(left_vert_axis, main_text_horiz_axis),
            **current_text_config,
        },
        {
            ParameterName.string: 'RPMI media with\nU-$\mathregular{^{13}}$C-glucose at normal\nconcentration (11.1 mM)',
            ParameterName.center: Vector(middle_vert_axis, upper_horiz_axis),
            **current_text_config,
        },
        {
            ParameterName.string: 'RPMI media with\nU-$\mathregular{^{13}}$C-glucose at low\nconcentration (0.5 mM)',
            ParameterName.center: Vector(middle_vert_axis, bottom_horiz_axis),
            **current_text_config,
        },
        {
            ParameterName.string: 'Incubate for 24 h',
            ParameterName.center: Vector(middle_vert_axis, upper_text_horiz_axis),
            ParameterName.font_weight: FontWeight.bold,
            **current_text_config,
            ParameterName.font_size: ExperimentDiagramConfig.normal_document_size + 2,
        },
        {
            ParameterName.string: 'Mass spectrometry',
            ParameterName.center: Vector(right_vert_axis, main_horiz_axis),
            **current_text_config,
        },
    ]

    normal_chevron_width = 0.07
    left_chevron_pair_left_x_value = left_vert_axis + 0.11
    left_chevron_pair_right_x_value = middle_vert_axis - 0.13
    right_chevron_pair_left_x_value = middle_vert_axis + 0.14
    right_chevron_pair_right_x_value = right_vert_axis - 0.08
    upper_chevron_inner_y_value = main_horiz_axis + 0.045
    bottom_chevron_inner_y_value = main_horiz_axis - 0.045
    upper_chevron_outer_y_value = upper_horiz_axis - 0.02
    bottom_chevron_outer_y_value = bottom_horiz_axis + 0.02

    split_merge_chevron_config_dict_list = [
        {
            ParameterName.tail_end_center: Vector(left_chevron_pair_left_x_value, upper_chevron_inner_y_value),
            ParameterName.head: Vector(left_chevron_pair_right_x_value, upper_chevron_outer_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(left_chevron_pair_left_x_value, bottom_chevron_inner_y_value),
            ParameterName.head: Vector(left_chevron_pair_right_x_value, bottom_chevron_outer_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(right_chevron_pair_left_x_value, upper_chevron_outer_y_value),
            ParameterName.head: Vector(right_chevron_pair_right_x_value, upper_chevron_inner_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
        {
            ParameterName.tail_end_center: Vector(right_chevron_pair_left_x_value, bottom_chevron_outer_y_value),
            ParameterName.head: Vector(right_chevron_pair_right_x_value, bottom_chevron_inner_y_value),
            **ExperimentDiagramConfig.chevron_config,
        },
    ]

    chevron_arrow_config_list = split_merge_chevron_config_dict_list

    cultured_cell_center = CulturedCell.calculate_center(CulturedCell, ExperimentDiagramConfig.cultured_cell_scale)
    cultured_cell_config_list = [
        {
            **ExperimentDiagramConfig.common_cultured_cell_diagram_config,
            ParameterName.bottom_left_offset: Vector(left_vert_axis, main_horiz_axis) - cultured_cell_center,
        },
    ]
    other_element_config_list = [
        (CulturedCell, cultured_cell_config) for cultured_cell_config in cultured_cell_config_list]
    return obj_list_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)

