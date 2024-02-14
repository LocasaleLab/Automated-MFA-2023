from ..figure_elements.data_figure.figure_data_loader import best_solution_data

from ..common.config import DataName, ParameterName, Figure, Vector, calculate_center_bottom_offset
from ..common.common_figure_materials import MetabolicNetworkConfig, PHGDHRawMaterials, \
    CommonFigureString
from ..common.elements import Elements

Subfigure = Elements.Subfigure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'data_acquisition_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        DataAcquisitionDiagram = Elements.DataAcquisitionDiagram
        scale = 0.38
        center = DataAcquisitionDiagram.calculate_center(DataAcquisitionDiagram, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = DataAcquisitionDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0, -0.01),
            ParameterName.scale: scale
        })
        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'optimization_process_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        OptimizationDiagram = Elements.OptimizationDiagram
        scale = 0.32
        mode = ParameterName.experimental
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, mode)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        optimization_process_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0, -0.01),
            ParameterName.scale: scale,
            ParameterName.mode: mode,
        })
        subfigure_element_dict = {
            optimization_process_diagram.name: optimization_process_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


MetabolicNetworkWithLegend = Elements.MetabolicNetworkWithLegend


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'metabolic_network_with_legend'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        legend = True
        scale = MetabolicNetworkConfig.common_scale
        center = MetabolicNetworkWithLegend.calculate_center(MetabolicNetworkWithLegend, scale, legend=legend)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)

        # special_metabolite_and_flux_dict = MetabolicNetworkConfig.common_diagram_network_setting_dict
        special_metabolite_and_flux_dict = PHGDHRawMaterials.diagram_network_config_dict
        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(0.05, 0),
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.metabolic_network_config_dict: special_metabolite_and_flux_dict
        }

        metabolic_network_with_legend_obj = MetabolicNetworkWithLegend(**subfigure_c_config_dict)
        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'running_time_and_loss_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.7

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.5463,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        running_time_and_loss_obj = Elements.TimeLossStack(**running_time_and_loss_config_dict)

        center = running_time_and_loss_obj.calculate_center(running_time_and_loss_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.005)
        running_time_and_loss_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            running_time_and_loss_obj.name: running_time_and_loss_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'protocol_diagram_vertical'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.5

        vertical_protocol_diagram = Elements.ProtocolDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.vertical,
        })

        center = vertical_protocol_diagram.calculate_center(vertical_protocol_diagram, scale, ParameterName.vertical)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.02, -0.005)
        vertical_protocol_diagram.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            vertical_protocol_diagram.name: vertical_protocol_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'metabolic_network_with_best_solution'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = MetabolicNetworkConfig.common_scale
        center = MetabolicNetworkWithLegend.calculate_center(MetabolicNetworkWithLegend, scale)
        bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        best_loss_data, best_solution_vector, flux_name_index_dict = best_solution_data.return_data(
            DataName.hct116_cultured_cell_line)
        current_reaction_value_dict = {
            flux_name: best_solution_vector[flux_index] for flux_name, flux_index in flux_name_index_dict.items()}

        metabolic_network_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left + bottom_offset + Vector(0.01, 0),
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


common_random_optimized_figure_scale = 0.6


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'distance_between_global_and_local_optima'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_random_optimized_figure_scale

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.8,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        random_optimized_loss_distance_obj = Elements.RandomOptimizedLossDistanceWithDiagramComparison(
            **running_time_and_loss_config_dict)

        center = random_optimized_loss_distance_obj.calculate_center(random_optimized_loss_distance_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.005)
        random_optimized_loss_distance_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            random_optimized_loss_distance_obj.name: random_optimized_loss_distance_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_best_optimized_solution,
            ParameterName.data_name: DataName.hct116_cultured_cell_line,
            ParameterName.with_single_optimized_solutions: False,
            ParameterName.with_unoptimized_set: False,
        }
        scale = 0.4
        hct116_cultured_cell_line_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = hct116_cultured_cell_line_flux_error_bar_comparison_figure.calculate_center(
            scale, **figure_data_parameter_dict)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
        hct116_cultured_cell_line_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_flux_error_bar_comparison_figure.name:
                hct116_cultured_cell_line_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureI(Subfigure):
    subfigure_label = 'i'
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
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
        flux_sloppiness_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_sloppiness_figure.name:
                flux_sloppiness_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure1(Figure):
    figure_label = 'figure_1'
    figure_title = 'Figure 1'

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
        ]

        figure_layout_list = [
            (0.16, [(0.55, 'a'), (0.45, 'b')]),
            (0.27, [(0.5, 'c'), (0.5, 'd')]),
            (0.27, [
                (0.28, 'e'),
                (0.4, 'f'),
                (0.32, 'i'),
            ]),
            (0.2, [
                (0.5, 'g'),
                (0.5, 'h'),
            ]),
        ]
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, {}, figure_title=self.figure_title)
