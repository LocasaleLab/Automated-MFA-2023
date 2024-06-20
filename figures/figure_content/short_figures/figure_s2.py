from ..common.config import ParameterName, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import CommonFigureString, DataName, ProtocolSearchingMaterials, \
    MetabolicNetworkConfig, CommonFigureMaterials

from .short_figure_config import (
    raw_model_all_data_name, raw_model_all_data_with_glns_m,
    all_data_optimized_size, all_data_selection_size, all_data_traditional_optimized_size,
    all_net_flux_comparison_scale, common_data_figure_scale
)

mid_name_dict, mid_color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
    CommonFigureMaterials, with_traditional_method=True, with_simulated_mid_data=True, wrap_name=True,
    traditional_double_wrap=False)


Subfigure = Elements.Subfigure


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
                subfigure_bottom_left + center_bottom_offset + Vector(0.03, -0.01)),
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
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: raw_model_all_data_name,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.traditional_optimized_size: all_data_traditional_optimized_size,
            ParameterName.color_dict: mid_color_dict,
            ParameterName.name_dict: mid_name_dict,
            ParameterName.mid_name_list: CommonFigureMaterials.all_data_mid_name_list,
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
    subfigure_title = 'combined_distance_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.add_availability(
                CommonFigureString.performance_metric, ParameterName.all_data_mode),
            ParameterName.figure_type: LossDistanceGridBoxDataFigure,
            ParameterName.data_name: raw_model_all_data_name,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.traditional_optimized_size: all_data_traditional_optimized_size,
            ParameterName.optimized: False,
            ParameterName.with_traditional_method: True,
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
                calculate_center_bottom_offset(center, subfigure_size) + Vector(0.005, 0))
        loss_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            loss_distance_comparison_figure.name: loss_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


OptimizedAllFluxComparisonBarDataFigure = Elements.OptimizedAllFluxComparisonBarDataFigure


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            # ParameterName.figure_title: CommonFigureString.difference_from_known_flux,
            ParameterName.figure_title: CommonFigureString.add_availability(
                CommonFigureString.difference_from_known_flux, ParameterName.all_data_mode),
            ParameterName.data_name: raw_model_all_data_name,
            ParameterName.with_re_optimization: False,
            ParameterName.with_traditional_method: True,
            ParameterName.with_glns_m: raw_model_all_data_with_glns_m,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.traditional_optimized_size: all_data_traditional_optimized_size,
        }
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(
            scale, with_traditional_method=True)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'flux_relative_error_comparison_all_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.add_availability(
                CommonFigureString.relative_error_to_known_flux, ParameterName.all_data_mode),
            ParameterName.data_name: raw_model_all_data_name,
            ParameterName.flux_relative_distance: True,
            ParameterName.with_re_optimization: False,
            ParameterName.with_traditional_method: True,
            ParameterName.with_glns_m: raw_model_all_data_with_glns_m,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.traditional_optimized_size: all_data_traditional_optimized_size,
        }
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_relative_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_relative_error_bar_comparison_figure.calculate_center(
            scale, with_traditional_method=True)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_all_data_flux_relative_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_relative_error_bar_comparison_figure.name:
                raw_model_all_data_flux_relative_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS2(Figure):
    figure_label = 'short_figure_s2'
    figure_title = 'Figure S2'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            # SubfigureF,
            # SubfigureG,
            # SubfigureH,
            # SubfigureI,
            # SubfigureJ,
        ]

        subfigure_a_height = 0.22

        subfigure_a_width = 0.45
        subfigure_b_width = 1 - subfigure_a_width
        subfigure_c_d_e_width = 0.5
        subfigure_d_width = 0.5
        subfigure_e_width = 1 - subfigure_d_width

        subfigure_b_height = 0.32
        subfigure_c_height = 0.2
        subfigure_d_height = 0.3

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

        subfigure_c_top = subfigure_a_height
        subfigure_b_center_x = subfigure_a_width + subfigure_b_width / 2
        subfigure_b_center_y = subfigure_b_height / 2
        subfigure_b_center = Vector(subfigure_b_center_x, subfigure_b_center_y)
        subfigure_b_size = Vector(subfigure_b_width, subfigure_b_height)
        subfigure_f_g_h_center_x = subfigure_c_d_e_width + subfigure_e_width / 2
        subfigure_e_height = subfigure_d_height
        subfigure_e_center_y = subfigure_b_height + subfigure_e_height / 2
        subfigure_e_center = Vector(subfigure_f_g_h_center_x, subfigure_e_center_y)

        subfigure_e_size = Vector(subfigure_e_width, subfigure_e_height)

        single_subfigure_layout_dict = {
            'b': (subfigure_b_center, subfigure_b_size),
            'e': (subfigure_e_center, subfigure_e_size),
            # 'f': (subfigure_f_center, subfigure_f_size),
            # 'f': (subfigure_f_center, subfigure_f_size),
            # 'g': (subfigure_g_center, subfigure_g_size),
            # 'h': (subfigure_h_center, subfigure_h_size),
            # 'i': (subfigure_i_center, subfigure_i_size),
            # 'j': (subfigure_j_center, subfigure_j_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
