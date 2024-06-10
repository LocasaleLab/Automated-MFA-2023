from ..common.config import ParameterName, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import CommonFigureString, DataName, ProtocolSearchingMaterials, \
    MetabolicNetworkConfig

Subfigure = Elements.Subfigure

common_data_figure_scale = 0.45
all_net_flux_comparison_scale = 0.4
heatmap_fluxes = ('FBA_c - FBA_c__R', 'CS_m')
figure_a_b_y_offset = -0.01
figure_c_d_e_f_x_offset = 0.005
figure_g_h_i_j_x_offset = -0.005
figure_e_f_x_offset = 0.01
figure_d_g_y_offset = 0
figure_e_h_y_offset = 0.01
metabolic_network_center_offset = Vector(0.01, -0.005)
network_text_y_offset = Vector(0, 0.6)
network_legend_y_offset = Vector(0, 0)


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'simulated_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        OptimizationDiagram = Elements.OptimizationDiagram

        scale = 0.32
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, ParameterName.simulated)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: (
                subfigure_bottom_left + center_bottom_offset + Vector(0.03, figure_a_b_y_offset)),
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
        ProtocolDiagram = Elements.ProtocolDiagram

        scale = 0.5
        center = ProtocolDiagram.calculate_center(ProtocolDiagram, scale, ParameterName.simulated_reoptimization)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = ProtocolDiagram(**{
            ParameterName.bottom_left_offset: (
                subfigure_bottom_left + center_bottom_offset + Vector(0, figure_a_b_y_offset)),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.simulated_reoptimization,
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
        MetabolicNetworkWithLegend = Elements.MetabolicNetworkWithLegend
        legend = True
        text_comment_config_dict = {
            **ProtocolSearchingMaterials.all_data_text_comment_config_dict,
            ParameterName.extra_offset: network_text_y_offset,
        }
        title = CommonFigureString.all_available_mid_data
        scale = 0.29
        center = MetabolicNetworkWithLegend.calculate_center(
            MetabolicNetworkWithLegend, scale, figure_title=title, legend=legend,
            text_comment_config_dict=text_comment_config_dict)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: (
                    subfigure_bottom_left + bottom_offset + metabolic_network_center_offset +
                    Vector(figure_c_d_e_f_x_offset, 0)),
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


LossDistanceSinglePairFigure = Elements.LossDistanceSinglePairFigure
LossDistanceGridBoxDataFigure = Elements.LossDistanceGridBoxDataFigure


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'combined_distance_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.performance_metric,
            ParameterName.figure_type: LossDistanceGridBoxDataFigure,
            ParameterName.data_name: DataName.optimization_from_solutions_all_data,
            ParameterName.optimized_size: 20000,
            ParameterName.selection_size: 100,
            ParameterName.optimized: True,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.02],
                ParameterName.default_y_tick_label_list: [0, 0.005, 0.01, 0.015, 0.02],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 500],
                ParameterName.default_y_tick_label_list: [0, 100, 200, 300, 400, 500]
            }
        }
        scale = common_data_figure_scale
        loss_distance_comparison_figure = LossDistanceSinglePairFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_distance_comparison_figure.calculate_center(loss_distance_comparison_figure, scale)
        center_bottom_offset = (
                calculate_center_bottom_offset(center, subfigure_size) + Vector(figure_c_d_e_f_x_offset, 0))
        loss_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            loss_distance_comparison_figure.name: loss_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        OptimizedAllFluxComparisonBarDataFigure = Elements.OptimizedAllFluxComparisonBarDataFigure
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_known_flux,
            ParameterName.data_name: DataName.optimization_from_solutions_all_data,
            ParameterName.optimized_size: 20000,
            ParameterName.selection_size: 100,
        }
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) +
            Vector(figure_c_d_e_f_x_offset + figure_e_f_x_offset, 0))
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'combined_distance_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_data_figure_scale
        subfigure_d_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.raw_model_all_data,
                ParameterName.horiz_or_vertical: ParameterName.horizontal,
                ParameterName.figure_title: CommonFigureString.net_euclidean_distance_to_parameters,
            },
        }
        combined_heatmap = Elements.DistanceVariationScatterFigure(**subfigure_d_config_dict)

        center = combined_heatmap.calculate_center(combined_heatmap, scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) +
            Vector(figure_c_d_e_f_x_offset + figure_e_f_x_offset, figure_d_g_y_offset))
        combined_heatmap.move_and_scale(bottom_left_offset=center_bottom_offset)
        subfigure_element_dict = {combined_heatmap.name: combined_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'mid_brief_comparison_table'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.3
        mid_comparison_table = Elements.AllExperimentalMIDBriefComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {},
        })

        center = mid_comparison_table.calculate_center(mid_comparison_table, scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01 + figure_g_h_i_j_x_offset, 0))
        mid_comparison_table.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_table.name: mid_comparison_table}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'combined_distance_figure_raw_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.performance_metric,
            ParameterName.figure_type: LossDistanceGridBoxDataFigure,
            ParameterName.data_name: DataName.optimization_from_solutions_raw_data,
            ParameterName.optimized_size: 20000,
            ParameterName.selection_size: 100,
            ParameterName.optimized: True,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.23],
                ParameterName.default_y_tick_label_list: [0, 0.05, 0.1, 0.15, 0.2],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 500],
                ParameterName.default_y_tick_label_list: [0, 100, 200, 300, 400, 500]
            }
        }
        scale = common_data_figure_scale
        loss_distance_comparison_figure = LossDistanceSinglePairFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_distance_comparison_figure.calculate_center(loss_distance_comparison_figure, scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) + Vector(figure_g_h_i_j_x_offset, 0))
        loss_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            loss_distance_comparison_figure.name: loss_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureI(Subfigure):
    subfigure_label = 'i'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        OptimizedAllFluxComparisonBarDataFigure = Elements.OptimizedAllFluxComparisonBarDataFigure
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_known_flux,
            ParameterName.data_name: DataName.optimization_from_solutions_raw_data,
            ParameterName.optimized_size: 20000,
            ParameterName.selection_size: 100,
        }
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) + Vector(figure_g_h_i_j_x_offset, -0.01))
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureJ(Subfigure):
    subfigure_label = 'j'
    subfigure_title = 'sloppiness_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.ax_interval: 0,
            ParameterName.data_name: ParameterName.all_data_mode,
            ParameterName.scale: 1,
            ParameterName.figure_title: [
                CommonFigureString.selected_solution,
                CommonFigureString.averaged_solution,
                CommonFigureString.reoptimized_solution]
        }
        scale = 0.4
        flux_sloppiness_diagram = Elements.MultipleFluxSloppinessDiagram(**{
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict
        })
        center = flux_sloppiness_diagram.calculate_center(flux_sloppiness_diagram, scale)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) + Vector(figure_g_h_i_j_x_offset, 0))
        flux_sloppiness_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_sloppiness_diagram.name:
                flux_sloppiness_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure2(Figure):
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
            SubfigureI,
            SubfigureJ,
        ]

        # figure_size = Constant.default_figure_size
        # height_to_width_ratio = figure_size[1] / figure_size[0]
        # top_margin_ratio = FigureConfig.top_margin_ratio
        # side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_a_b_height = 0.2

        subfigure_c_width = 0.5
        subfigure_d_width = 0.5
        subfigure_e_width = 0.5
        subfigure_f_width = 0.55
        subfigure_g_width = subfigure_c_width
        subfigure_h_width = subfigure_d_width
        subfigure_i_width = subfigure_e_width
        subfigure_j_width = 0.48

        subfigure_c_height = 0.23
        subfigure_d_height = 0.17
        subfigure_e_height = 0.25
        subfigure_f_height = 0.1
        subfigure_g_height = 0.13
        subfigure_h_height = 0.18
        subfigure_i_height = 0.28
        subfigure_j_height = 0.18

        figure_layout_list = [
            (subfigure_a_b_height, [
                (0.35, 'a'),
                (0.65, 'b')
            ]),
            (subfigure_c_height, [
                (subfigure_c_width, 'c'),
            ]),
            (subfigure_d_height, [
                (subfigure_d_width, 'd'),
            ]),
            (subfigure_e_height, [
                (subfigure_e_width, 'e'),
            ]),
            (subfigure_f_height, [
                (subfigure_f_width, 'f'),
            ]),
            # (subfigure_g_height, [
            #     (subfigure_g_width, 'g'),
            # ]),
            # (subfigure_h_height, [
            #     (subfigure_h_width, 'h'),
            # ]),
        ]

        # subfigure_e_center_x = subfigure_c_width + subfigure_e_width / 2
        # subfigure_f_center_x = subfigure_d_width + subfigure_f_width / 2
        # subfigure_e_center_y = subfigure_c_top + subfigure_e_height / 2
        # subfigure_f_top = subfigure_c_top + subfigure_e_height
        # subfigure_f_center_y = subfigure_f_top + subfigure_f_height / 2
        # subfigure_f_bottom = subfigure_f_top + subfigure_f_height
        # subfigure_e_center = Vector(subfigure_e_center_x, subfigure_e_center_y)
        # subfigure_e_size = Vector(subfigure_e_width, subfigure_e_height)
        # subfigure_f_center = Vector(subfigure_f_center_x, subfigure_f_center_y)
        # subfigure_f_size = Vector(subfigure_f_width, subfigure_f_height)

        # subfigure_i_center_x = subfigure_g_width + subfigure_i_width / 2
        # subfigure_j_center_x = subfigure_h_width + subfigure_j_width / 2
        # subfigure_i_center_y = subfigure_f_bottom + subfigure_i_height / 2
        # subfigure_i_bottom = subfigure_f_bottom + subfigure_i_height

        subfigure_c_top = subfigure_a_b_height
        subfigure_g_center_x = subfigure_c_width + subfigure_g_width / 2
        subfigure_h_center_x = subfigure_d_width + subfigure_h_width / 2
        subfigure_g_center_y = subfigure_c_top + subfigure_g_height / 2
        subfigure_h_top = subfigure_c_top + subfigure_g_height
        subfigure_h_center_y = subfigure_h_top + subfigure_h_height / 2
        subfigure_h_bottom = subfigure_h_top + subfigure_h_height
        subfigure_g_center = Vector(subfigure_g_center_x, subfigure_g_center_y)
        subfigure_g_size = Vector(subfigure_g_width, subfigure_g_height)
        subfigure_h_center = Vector(subfigure_h_center_x, subfigure_h_center_y)
        subfigure_h_size = Vector(subfigure_h_width, subfigure_h_height)

        subfigure_i_center_x = subfigure_e_width + subfigure_i_width / 2
        subfigure_j_center_x = subfigure_f_width + subfigure_j_width / 2 - 0.03
        subfigure_i_center_y = subfigure_h_bottom + subfigure_i_height / 2
        subfigure_i_bottom = subfigure_h_bottom + subfigure_i_height
        subfigure_j_center_y = subfigure_i_bottom + subfigure_j_height / 2
        subfigure_i_center = Vector(subfigure_i_center_x, subfigure_i_center_y)
        subfigure_i_size = Vector(subfigure_i_width, subfigure_i_height)
        subfigure_j_center = Vector(subfigure_j_center_x, subfigure_j_center_y)
        subfigure_j_size = Vector(subfigure_j_width, subfigure_j_height)

        single_subfigure_layout_dict = {
            # 'e': (subfigure_e_center, subfigure_e_size),
            # 'f': (subfigure_f_center, subfigure_f_size),
            'g': (subfigure_g_center, subfigure_g_size),
            'h': (subfigure_h_center, subfigure_h_size),
            'i': (subfigure_i_center, subfigure_i_size),
            'j': (subfigure_j_center, subfigure_j_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
