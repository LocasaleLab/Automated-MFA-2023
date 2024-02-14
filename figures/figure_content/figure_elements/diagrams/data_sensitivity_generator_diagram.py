from .config import CompositeFigure, ParameterName, Vector, DataName, CommonFigureString, \
    FontWeight, ColorConfig, common_legend_generator
from .network_diagram import NetworkDiagram

from .data_acquisition_diagram import one_to_three_branch_arrow, BranchArrowMode, DataAcquisitionDiagramConfig, \
    common_final_constructor


class DataSensitivityGeneratorDiagramConfig(DataAcquisitionDiagramConfig):
    bend_chevron_config = {
        **DataAcquisitionDiagramConfig.bend_chevron_config,
        ParameterName.radius: 0.04,
    }
    title_text_common_config = {
        **DataAcquisitionDiagramConfig.document_text_config,
        ParameterName.font_size: 15,
        ParameterName.font_weight: FontWeight.bold,
    }
    main_text_common_config = {
        **DataAcquisitionDiagramConfig.document_text_config,
        ParameterName.font_size: 12,
    }

    common_legend_config_dict = {
        ParameterName.horiz_or_vertical: ParameterName.vertical,
        ParameterName.text_config_dict: {
            ParameterName.font_size: 10,
            ParameterName.font_weight: FontWeight.bold
        },
        ParameterName.location_config_dict: {
            ParameterName.total_verti_edge_ratio: 0.1,
            ParameterName.row_verti_edge_ratio: 0.9,
        },
    }
    legend_name_dict = {
        ParameterName.mid: 'Metabolites with MID',
        ParameterName.normal: 'Other metabolites',
    }
    legend_color_dict = {
        ParameterName.mid: ColorConfig.mid_metabolite_color,
        ParameterName.normal: ColorConfig.normal_metabolite_color,
    }


class DataSensitivityGeneratorDiagram(CompositeFigure):
    total_width = 1

    def __init__(self, **kwargs):
        (
            total_width, total_height, text_obj_list, chevron_arrow_obj_list, constructed_obj_list,
            diagram_legend_config_dict
        ) = data_sensitivity_generator_diagram_generator()
        height_to_width_ratio = total_height / total_width
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = height_to_width_ratio
        size = Vector(total_width, total_height)
        figure_legend_obj = common_legend_generator(
            diagram_legend_config_dict, DataSensitivityGeneratorDiagramConfig.legend_color_dict)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
            ParameterName.legend: {ParameterName.legend: figure_legend_obj},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), size, background=False, **kwargs)


def data_sensitivity_generator_diagram_generator():
    total_width = 1
    total_height = 0.5

    chevron_start_end_x_value = Vector(0.23, 0.38)
    left_diagram_axis_x_value = 0.12
    right_diagram_axis_x_value = 0.45
    text_axis_x_value = 0.75
    main_horiz_axis = 0.25
    upper_bottom_to_main_axis_distance_chevron = 0.15
    upper_bottom_to_main_axis_distance = 0.17
    legend_center = Vector(left_diagram_axis_x_value - 0.05, main_horiz_axis + 0.15)
    legend_size = Vector(0.25, 0.1)

    bend_chevron_to_main_distance = DataSensitivityGeneratorDiagramConfig.bend_chevron_to_main_distance

    chevron_arrow_config_list = one_to_three_branch_arrow(
        ParameterName.x, *chevron_start_end_x_value, main_horiz_axis, upper_bottom_to_main_axis_distance_chevron,
        bend_chevron_to_main_distance=bend_chevron_to_main_distance, mode=BranchArrowMode.branch,
        config_class=DataSensitivityGeneratorDiagramConfig)
    left_network_scale = 0.15
    right_network_scale = 0.1
    network_mode_list = [
        DataName.data_sensitivity,
        DataName.smaller_data_size,
        DataName.data_without_pathway,
        DataName.medium_data_without_combination,
    ]
    horiz_axis_list = [
        main_horiz_axis + upper_bottom_to_main_axis_distance,
        main_horiz_axis,
        main_horiz_axis - upper_bottom_to_main_axis_distance]
    network_diagram_target_center_list = [
        Vector(left_diagram_axis_x_value, main_horiz_axis - 0.05),
        Vector(right_diagram_axis_x_value, main_horiz_axis + upper_bottom_to_main_axis_distance),
        Vector(right_diagram_axis_x_value, main_horiz_axis),
        Vector(right_diagram_axis_x_value, main_horiz_axis - upper_bottom_to_main_axis_distance),
    ]
    network_diagram_pair_list = []
    for index, (network_mode, network_target_center) in enumerate(
            zip(network_mode_list, network_diagram_target_center_list)):
        if index == 0:
            network_scale = left_network_scale
        else:
            network_scale = right_network_scale
        current_center = NetworkDiagram.calculate_center(NetworkDiagram, network_scale, network_mode)
        network_diagram_config_dict = {
            ParameterName.mode: network_mode,
            ParameterName.bottom_left_offset: network_target_center - current_center,
            ParameterName.scale: network_scale,
        }
        network_diagram_pair_list.append((NetworkDiagram, network_diagram_config_dict))

    other_element_config_list = [
        *network_diagram_pair_list,
    ]
    title_text_y_offset = 0.03
    main_text_y_offset = -0.03
    text_width = 0.2
    title_text_height = 0.1
    main_text_height = 0.1
    title_string_list = [
        CommonFigureString.smaller_data_size_with_order_prefix,
        CommonFigureString.data_without_pathway_with_order_prefix,
        CommonFigureString.compartmental_data_with_order_prefix]
    main_string_list = [
        'MIDs can be measured\nevenly in all pathways',
        'MIDs from a specific pathway\nis not available',
        'MIDs of compartmentalized\nmetabolites are measured together']
    text_config_list = []
    for title_string, text_y_value in zip(title_string_list, horiz_axis_list):
        text_config_list.append({
            **DataSensitivityGeneratorDiagramConfig.title_text_common_config,
            ParameterName.width: text_width,
            ParameterName.height: title_text_height,
            ParameterName.string: title_string,
            ParameterName.center: Vector(text_axis_x_value, text_y_value + title_text_y_offset)
        })
    for main_string, text_y_value in zip(main_string_list, horiz_axis_list):
        text_config_list.append({
            **DataSensitivityGeneratorDiagramConfig.main_text_common_config,
            ParameterName.width: text_width,
            ParameterName.height: main_text_height,
            ParameterName.string: main_string,
            ParameterName.center: Vector(text_axis_x_value, text_y_value + main_text_y_offset)
        })
    (
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list
    ) = common_final_constructor(text_config_list, chevron_arrow_config_list, other_element_config_list)

    diagram_legend_config_dict = {
        **DataSensitivityGeneratorDiagramConfig.common_legend_config_dict,
        ParameterName.legend_center: legend_center,
        ParameterName.legend_area_size: legend_size,
        ParameterName.name_dict: DataSensitivityGeneratorDiagramConfig.legend_name_dict,
        ParameterName.shape: ParameterName.circle,
        ParameterName.alpha: None,
    }

    return total_width, total_height, text_obj_list, chevron_arrow_obj_list, constructed_obj_list, \
        diagram_legend_config_dict


