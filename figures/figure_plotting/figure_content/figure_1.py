from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout
from ..common.common_figure_materials import MetabolicNetworkConfig, FigureConfig, PHGDHRawMaterials
from ..figure_elements.data_figure.basic_data_figure.figure_data_loader import best_solution_data

Subfigure = element_dict[ElementName.Subfigure]
CompositeFigure = element_dict[ElementName.CompositeFigure]
DataAcquisitionDiagram = element_dict[ElementName.DataAcquisitionDiagram]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
ProtocolDiagram = element_dict[ElementName.ProtocolDiagram]
TimeLossStack = element_dict[ElementName.TimeLossStack]
MetabolicNetwork = element_dict[ElementName.MetabolicNetwork]
MetabolicNetworkWithLegend = element_dict[ElementName.MetabolicNetworkWithLegend]
RandomOptimizedFluxLayout = element_dict[ElementName.RandomOptimizedFluxLayout]
RandomOptimizedLossDistanceComparison = element_dict[ElementName.RandomOptimizedLossDistanceComparison]
OptimumDistributionComparisonDiagram = element_dict[ElementName.OptimumDistributionComparisonDiagram]
common_data_figure_scale = FigureConfig.common_data_figure_scale


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'data_acquisition_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
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
        scale = common_data_figure_scale

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.5463,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        running_time_and_loss_obj = TimeLossStack(**running_time_and_loss_config_dict)

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

        vertical_protocol_diagram = ProtocolDiagram(**{
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


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'optimum_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.25

        optimum_distribution_comparison_diagram_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        optimum_distribution_comparison_comparison_obj = OptimumDistributionComparisonDiagram(
            **optimum_distribution_comparison_diagram_config_dict)

        center = optimum_distribution_comparison_comparison_obj.calculate_center(
            optimum_distribution_comparison_comparison_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
        optimum_distribution_comparison_comparison_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            optimum_distribution_comparison_comparison_obj.name: optimum_distribution_comparison_comparison_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


common_random_optimized_figure_scale = 0.6


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'visualization_of_random_and_optimized_solutions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_random_optimized_figure_scale

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.7,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        random_optimized_flux_comparison_obj = RandomOptimizedFluxLayout(**running_time_and_loss_config_dict)

        center = random_optimized_flux_comparison_obj.calculate_center(random_optimized_flux_comparison_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.02, -0.005)
        random_optimized_flux_comparison_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            random_optimized_flux_comparison_obj.name: random_optimized_flux_comparison_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureI(Subfigure):
    subfigure_label = 'i'
    subfigure_title = 'distance_between_global_and_local_optima'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_random_optimized_figure_scale

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.8,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        random_optimized_loss_distance_obj = RandomOptimizedLossDistanceComparison(
            **running_time_and_loss_config_dict)

        center = random_optimized_loss_distance_obj.calculate_center(random_optimized_loss_distance_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.005)
        random_optimized_loss_distance_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            random_optimized_loss_distance_obj.name: random_optimized_loss_distance_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class Figure1(element_dict[ElementName.Figure]):
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

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        figure_layout_list = [
            (0.16, [(0.55, 'a'), (0.45, 'b')]),
            (0.27, [(0.5, 'c'), (0.5, 'd')]),
            (0.27, [
                (0.28, 'e'),
                (0.4, 'f'),
                (0.32, 'g'),
            ]),
            (0.2, [
                (0.43, 'h'),
                (0.58, 'i'),
            ]),
        ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
