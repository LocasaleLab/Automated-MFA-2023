from ..common.config import ParameterName, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import CommonFigureString, DataName, ProtocolSearchingMaterials, \
    MetabolicNetworkConfig

from .short_figure_config import (
    raw_model_raw_data_name, raw_data_optimized_size, raw_data_selection_size, raw_data_traditional_optimized_size,
    raw_model_raw_data_with_glns_m)
from .figure_s2 import mid_color_dict, mid_name_dict


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
            calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, 0))
        mid_comparison_table.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_table.name: mid_comparison_table}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'mid_comparison_raw_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: raw_model_raw_data_name,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.traditional_optimized_size: raw_data_traditional_optimized_size,
            ParameterName.color_dict: mid_color_dict,
            ParameterName.name_dict: mid_name_dict,
            ParameterName.legend_config_dict: {ParameterName.grid_shape: (1, 4)}
        }
        scale = 0.4
        hct116_cultured_cell_line_mid_comparison_figure = Elements.MIDComparisonGridBarWithLegendDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 1,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = hct116_cultured_cell_line_mid_comparison_figure.calculate_center(
            hct116_cultured_cell_line_mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.015, 0.005)
        hct116_cultured_cell_line_mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_mid_comparison_figure.name: hct116_cultured_cell_line_mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


LossDistanceSinglePairFigure = Elements.LossDistanceSinglePairFigure
LossDistanceGridBoxDataFigure = Elements.LossDistanceGridBoxDataFigure


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'combined_distance_figure_raw_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.add_availability(
                CommonFigureString.performance_metric, ParameterName.experimental),
            ParameterName.figure_type: Elements.LossDistanceGridBoxDataFigure,
            ParameterName.data_name: raw_model_raw_data_name,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.traditional_optimized_size: raw_data_traditional_optimized_size,
            ParameterName.optimized: False,
            ParameterName.with_traditional_method: True,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.21],
                ParameterName.default_y_tick_label_list: [0, 0.05, 0.1, 0.15, 0.2],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 500],
                ParameterName.default_y_tick_label_list: [0, 100, 200, 300, 400, 500]
            }
        }
        scale = 0.45
        loss_distance_comparison_figure = Elements.LossDistanceSinglePairFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_distance_comparison_figure.calculate_center(loss_distance_comparison_figure, scale)
        center_bottom_offset = (
                calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0))
        loss_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            loss_distance_comparison_figure.name: loss_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'flux_relative_error_comparison_raw_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.add_availability(
                CommonFigureString.relative_error_to_known_flux, ParameterName.experimental),
            ParameterName.data_name: raw_model_raw_data_name,
            ParameterName.flux_relative_distance: True,
            ParameterName.with_re_optimization: False,
            ParameterName.with_traditional_method: True,
            ParameterName.with_glns_m: raw_model_raw_data_with_glns_m,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.traditional_optimized_size: raw_data_traditional_optimized_size,
        }
        scale = all_net_flux_comparison_scale
        raw_model_raw_data_flux_relative_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_raw_data_flux_relative_error_bar_comparison_figure.calculate_center(
            scale, with_traditional_method=True)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_raw_data_flux_relative_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_raw_data_flux_relative_error_bar_comparison_figure.name:
                raw_model_raw_data_flux_relative_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'sloppiness_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.ax_interval: 0,
            ParameterName.data_name: ParameterName.all_data_mode,
            ParameterName.with_re_optimization: False,
            ParameterName.scale: 1,
            ParameterName.figure_title: [
                CommonFigureString.selected_solution,
                CommonFigureString.averaged_solution]
        }
        scale = 0.35
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


class FigureS3(Figure):
    figure_label = 'short_figure_s3'
    figure_title = 'Supplementary Figure 3'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
        ]

        subfigure_a_height = 0.13

        subfigure_a_width = 0.45
        subfigure_b_width = 1 - subfigure_a_width
        subfigure_c_d_e_width = 0.5
        subfigure_d_width = 0.5
        subfigure_e_width = 1 - subfigure_d_width

        subfigure_b_height = 0.32
        subfigure_c_height = 0.2
        subfigure_d_height = 0.3
        subfigure_e_height = 0.2

        figure_layout_list = [
            (subfigure_a_height, [
                (subfigure_a_width, 'a'),
            ]),
            (subfigure_c_height, [
                (subfigure_c_d_e_width, 'c'),
            ]),
            (subfigure_d_height, [
                (subfigure_d_width, 'd'),
            ]),
        ]

        subfigure_b_center_x = subfigure_a_width + subfigure_b_width / 2
        subfigure_b_center_y = subfigure_b_height / 2
        subfigure_b_center = Vector(subfigure_b_center_x, subfigure_b_center_y)
        subfigure_b_size = Vector(subfigure_b_width, subfigure_b_height)
        subfigure_e_center_x = subfigure_c_d_e_width + subfigure_e_width / 2
        subfigure_e_center_y = subfigure_b_height + subfigure_e_height / 2
        subfigure_e_center = Vector(subfigure_e_center_x, subfigure_e_center_y)
        subfigure_e_size = Vector(subfigure_e_width, subfigure_e_height)

        single_subfigure_layout_dict = {
            'b': (subfigure_b_center, subfigure_b_size),
            'e': (subfigure_e_center, subfigure_e_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
