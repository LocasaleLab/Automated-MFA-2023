from ..common.config import DataName, ParameterName, Figure, Vector, calculate_center_bottom_offset
from ..common.common_figure_materials import MetabolicNetworkConfig, PHGDHRawMaterials, \
    CommonFigureString
from ..common.elements import Elements

from ..figure_elements.data_figure.figure_data_loader import best_solution_data
from .short_figure_config import hct_116_data_name

Subfigure = Elements.Subfigure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: hct_116_data_name,
            ParameterName.result_label: 'HCT116_WQ2101__ctrl__1',
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


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'running_time_and_loss_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.47

        running_time_and_loss_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.total_width: 0.5,
                ParameterName.data_name: hct_116_data_name,
                ParameterName.time_data_figure_parameter_dict: {
                    # ParameterName.x_ticks_list: [0, 1, 2, 3, 4],
                    # ParameterName.common_y_lim: (0, 1.11),
                    # ParameterName.y_tick_interval: 0.25,
                },
                ParameterName.loss_data_figure_parameter_dict: {
                    # ParameterName.common_y_lim: (0, 4.01),
                    # ParameterName.y_tick_interval: 1,
                },
            }
        }
        running_time_and_loss_obj = Elements.TimeLossStack(**running_time_and_loss_config_dict)

        center = running_time_and_loss_obj.calculate_center(running_time_and_loss_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.005, -0.01)
        running_time_and_loss_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            running_time_and_loss_obj.name: running_time_and_loss_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'protocol_diagram_vertical'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.45

        vertical_protocol_diagram = Elements.ProtocolDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.vertical,
        })

        center = vertical_protocol_diagram.calculate_center(vertical_protocol_diagram, scale, ParameterName.vertical)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.02, -0.01)
        vertical_protocol_diagram.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            vertical_protocol_diagram.name: vertical_protocol_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


MetabolicNetworkWithLegend = Elements.MetabolicNetworkWithLegend


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'metabolic_network_with_best_solution'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = MetabolicNetworkConfig.common_scale
        center = MetabolicNetworkWithLegend.calculate_center(MetabolicNetworkWithLegend, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        best_loss_data, best_solution_vector, flux_name_index_dict = best_solution_data.return_data(
            hct_116_data_name)
        current_reaction_value_dict = {
            flux_name: best_solution_vector[flux_index] for flux_name, flux_index in flux_name_index_dict.items()}

        metabolic_network_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(-0.02, -0.005),
            ParameterName.scale: scale,
            ParameterName.metabolic_network_config_dict: {
                **PHGDHRawMaterials.data_flux_network_setting_dict,
                ParameterName.reaction_raw_value_dict: current_reaction_value_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency,
            }
        }

        metabolic_network_with_best_solution_obj = MetabolicNetworkWithLegend(**metabolic_network_config_dict)
        subfigure_element_dict = {
            metabolic_network_with_best_solution_obj.name: metabolic_network_with_best_solution_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_best_optimized_solution,
            ParameterName.data_name: hct_116_data_name,
            # ParameterName.with_glns_m: with_glns_m,
        }
        scale = 0.43
        hct116_cultured_cell_line_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = hct116_cultured_cell_line_flux_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, 0)
        hct116_cultured_cell_line_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_flux_error_bar_comparison_figure.name:
                hct116_cultured_cell_line_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'flux_sloppiness_selected_solutions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        sloppiness_diagram_scale = 0.3

        figure_data_parameter_dict = {
            ParameterName.mode: ParameterName.raw_optimized,
            ParameterName.figure_title: CommonFigureString.flux_sloppiness_wrap,
        }
        scale = sloppiness_diagram_scale
        flux_sloppiness_figure = Elements.FluxSloppinessDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = flux_sloppiness_figure.calculate_center(flux_sloppiness_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(-0.02, 0)
        flux_sloppiness_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_sloppiness_figure.name:
                flux_sloppiness_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS1(Figure):
    figure_label = 'short_figure_s1'
    figure_title = 'Figure S1'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            SubfigureF,
        ]

        subfigure_a_width = 0.45
        subfigure_a_height = 0.32
        subfigure_e_width = 0.5
        subfigure_e_height = 0.58
        subfigure_c_center = Vector(subfigure_a_width + subfigure_e_width / 2, subfigure_e_height / 2)
        subfigure_d_f_width = 1 - subfigure_e_width
        subfigure_b_c_height = 0.25
        subfigure_d_height = 0.28
        subfigure_f_height = 0.25
        subfigure_b_width = 0.25
        subfigure_c_width = 0.25
        subfigure_d_width = 0.3
        subfigure_b_size = Vector(subfigure_b_width, subfigure_b_c_height)
        subfigure_c_size = Vector(subfigure_c_width, subfigure_b_c_height)
        subfigure_d_size = Vector(subfigure_d_f_width, subfigure_d_height)
        subfigure_f_size = Vector(subfigure_d_f_width, subfigure_f_height)
        subfigure_b_center = Vector(subfigure_a_width + subfigure_b_width / 2, subfigure_b_c_height / 2)
        subfigure_c_center = Vector(subfigure_a_width + subfigure_b_width + subfigure_c_width / 2, subfigure_b_c_height / 2)
        subfigure_d_center = Vector(subfigure_e_width + subfigure_d_f_width / 2, subfigure_b_c_height + subfigure_d_height / 2)
        subfigure_f_center = Vector(subfigure_e_width + subfigure_d_f_width / 2, subfigure_b_c_height + subfigure_d_height + subfigure_f_height / 2)

        figure_layout_list = [
            (subfigure_a_height, [
                (subfigure_a_width, 'a')]),
            (subfigure_e_height, [
                (subfigure_e_width, 'e')]),
            # (0.25, [(0.55, 'c'), (0.45, 'd')]),
            # (0.25, [(0.44, 'e'), (0.56, 'f')]),
        ]

        single_subfigure_layout_dict = {
            'b': (subfigure_b_center, subfigure_b_size),
            'c': (subfigure_c_center, subfigure_c_size),
            'd': (subfigure_d_center, subfigure_d_size),
            'f': (subfigure_f_center, subfigure_f_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
