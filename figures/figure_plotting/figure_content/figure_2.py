from ..common.config import ParameterName, Constant
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout, single_subfigure_layout
from ..common.common_figure_materials import MetabolicNetworkConfig, FigureConfig, DataName, \
    ProtocolSearchingMaterials, CommonFigureString

Subfigure = element_dict[ElementName.Subfigure]
MetabolicNetwork = element_dict[ElementName.MetabolicNetwork]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
ProtocolDiagram = element_dict[ElementName.ProtocolDiagram]
MetabolicNetworkWithLegend = element_dict[ElementName.MetabolicNetworkWithLegend]
EuclideanHeatmapScatter = element_dict[ElementName.EuclideanHeatmapScatter]
AllFluxComparisonBarFigure = element_dict[ElementName.AllFluxComparisonBarFigure]

common_data_figure_scale = 0.45
heatmap_fluxes = ('FBA_c - FBA_c__R', 'CS_m')
figure_d_e_g_h_x_offset = 0
figure_d_g_y_offset = 0
figure_e_h_y_offset = 0.01
metabolic_network_center_offset = Vector(0.01, 0)
network_text_y_offset = Vector(0, 0.6)
network_legend_y_offset = Vector(0, 0)


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'simulated_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.32
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, ParameterName.simulated)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.03, 0),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.simulated,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'protocol_diagram_simulated'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.5
        center = ProtocolDiagram.calculate_center(ProtocolDiagram, scale, ParameterName.simulated)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = ProtocolDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset,
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.simulated,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'metabolic_network_all_mid_data_with_legend'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        legend = True
        text_comment_config_dict = {
            **ProtocolSearchingMaterials.all_data_text_comment_config_dict,
            ParameterName.extra_offset: network_text_y_offset,
        }
        title = CommonFigureString.all_available_mid_data
        scale = MetabolicNetworkConfig.common_scale
        center = MetabolicNetworkWithLegend.calculate_center(
            MetabolicNetworkWithLegend, scale, figure_title=title, legend=legend,
            text_comment_config_dict=text_comment_config_dict)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + metabolic_network_center_offset,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.figure_title: title,
            ParameterName.metabolic_network_legend_config_dict: {
                ParameterName.extra_offset: network_legend_y_offset,
            },
            ParameterName.metabolic_network_config_dict: {
                **MetabolicNetworkConfig.common_diagram_network_setting_dict,
                ParameterName.mid_data_metabolite_set: ParameterName.all_data_mode,
                ParameterName.mixed_mid_data_metabolite_set: None,
            },
            ParameterName.metabolic_network_text_comment_config_dict: text_comment_config_dict
        }

        metabolic_network_with_legend_obj = MetabolicNetworkWithLegend(**subfigure_c_config_dict)

        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'combined_distance_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_data_figure_scale
        center = EuclideanHeatmapScatter.calculate_center(EuclideanHeatmapScatter, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_d_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(
                figure_d_e_g_h_x_offset, figure_d_g_y_offset),
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: DataName.raw_model_all_data,
                ParameterName.flux_name: heatmap_fluxes,
            },
        }

        combined_heatmap = EuclideanHeatmapScatter(**subfigure_d_config_dict)
        subfigure_element_dict = {
            combined_heatmap.name: combined_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'all_flux_relative_error_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_data_figure_scale
        center = AllFluxComparisonBarFigure.calculate_center(AllFluxComparisonBarFigure, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_e_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(
                figure_d_e_g_h_x_offset, figure_e_h_y_offset),
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.raw_model_all_data,
            },
        }

        all_flux_comparison_bar_plot = AllFluxComparisonBarFigure(**subfigure_e_config_dict)
        subfigure_element_dict = {all_flux_comparison_bar_plot.name: all_flux_comparison_bar_plot}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'metabolic_network_experimentally_available_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        legend = True
        text_comment_config_dict = {
            **ProtocolSearchingMaterials.experimental_data_text_comment_config_dict,
            ParameterName.extra_offset: network_text_y_offset,
        }
        title = CommonFigureString.experimental_available_mid_data
        scale = MetabolicNetworkConfig.common_scale
        center = MetabolicNetworkWithLegend.calculate_center(
            MetabolicNetworkWithLegend, scale, figure_title=title, legend=legend,
            text_comment_config_dict=text_comment_config_dict)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_e_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + metabolic_network_center_offset,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.figure_title: title,
            ParameterName.metabolic_network_config_dict: MetabolicNetworkConfig.common_diagram_network_setting_dict,
            ParameterName.metabolic_network_legend_config_dict: {
                ParameterName.extra_offset: network_legend_y_offset,
            },
            ParameterName.metabolic_network_text_comment_config_dict: text_comment_config_dict
        }
        metabolic_network_with_legend_obj = MetabolicNetworkWithLegend(**subfigure_e_config_dict)
        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'combined_distance_figure_experimental_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_data_figure_scale
        center = EuclideanHeatmapScatter.calculate_center(EuclideanHeatmapScatter, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_f_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(
                figure_d_e_g_h_x_offset, figure_d_g_y_offset),
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: DataName.raw_model_raw_data,
                ParameterName.flux_name: heatmap_fluxes,
            },
        }

        combined_heatmap = EuclideanHeatmapScatter(**subfigure_f_config_dict)
        subfigure_element_dict = {
            combined_heatmap.name: combined_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'all_flux_relative_error_figure_experimental_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_data_figure_scale
        center = AllFluxComparisonBarFigure.calculate_center(AllFluxComparisonBarFigure, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_g_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(
                figure_d_e_g_h_x_offset, figure_e_h_y_offset),
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.raw_model_raw_data,
            },
        }

        all_flux_comparison_bar_plot = AllFluxComparisonBarFigure(**subfigure_g_config_dict)
        subfigure_element_dict = {all_flux_comparison_bar_plot.name: all_flux_comparison_bar_plot}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure2(element_dict[ElementName.Figure]):
    figure_label = 'figure_2'
    figure_title = 'Figure 2'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            SubfigureF,
            SubfigureG,
            SubfigureH,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_c_f_width = 0.47
        subfigure_c_f_height = 0.33
        subfigure_d_e_g_h_width = 1 - subfigure_c_f_width
        subfigure_d_g_height = 0.155
        subfigure_e_h_height = subfigure_c_f_height - subfigure_d_g_height

        figure_layout_list = [
            (0.23, [
                (0.35, 'a'),
                (0.65, 'b')
            ]),
            (subfigure_c_f_height, [
                (subfigure_c_f_width, 'c'),
            ]),
            (subfigure_c_f_height, [
                (subfigure_c_f_width, 'f'),
            ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)

        subfigure_c_top = figure_layout_list[0][0]
        subfigure_d_e_g_h_center_x = subfigure_c_f_width + subfigure_d_e_g_h_width / 2
        subfigure_d_center_y = subfigure_c_top + subfigure_d_g_height / 2
        subfigure_d_bottom = subfigure_c_top + subfigure_d_g_height
        subfigure_e_center_y = subfigure_d_bottom + subfigure_e_h_height / 2
        subfigure_f_top = subfigure_c_top + subfigure_c_f_height
        subfigure_g_center_y = subfigure_f_top + subfigure_d_g_height / 2
        subfigure_g_bottom = subfigure_f_top + subfigure_d_g_height
        subfigure_h_center_y = subfigure_g_bottom + subfigure_e_h_height / 2
        subfigure_d_center = Vector(subfigure_d_e_g_h_center_x, subfigure_d_center_y)
        subfigure_e_center = Vector(subfigure_d_e_g_h_center_x, subfigure_e_center_y)
        subfigure_g_center = Vector(subfigure_d_e_g_h_center_x, subfigure_g_center_y)
        subfigure_h_center = Vector(subfigure_d_e_g_h_center_x, subfigure_h_center_y)
        subfigure_d_g_size = Vector(subfigure_d_e_g_h_width, subfigure_d_g_height)
        subfigure_e_h_size = Vector(subfigure_d_e_g_h_width, subfigure_e_h_height)

        subfigure_obj_list.extend([
            single_subfigure_layout(
                subfigure_d_center, subfigure_d_g_size, SubfigureD, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
            single_subfigure_layout(
                subfigure_e_center, subfigure_e_h_size, SubfigureE, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
            single_subfigure_layout(
                subfigure_g_center, subfigure_d_g_size, SubfigureG, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
            single_subfigure_layout(
                subfigure_h_center, subfigure_e_h_size, SubfigureH, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
        ])

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
