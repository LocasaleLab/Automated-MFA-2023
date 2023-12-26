from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.elements import Elements

from .common_functions import calculate_subfigure_layout, single_subfigure_layout
from ..common.common_figure_materials import FigureConfig, calculate_center_bottom_offset, CommonFigureString

Subfigure = Elements.Subfigure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.hct116_cultured_cell_line,
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
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, 0.005)
        hct116_cultured_cell_line_mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_mid_comparison_figure.name: hct116_cultured_cell_line_mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'visualization_of_random_and_optimized_solutions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        RandomOptimizedFluxLayout = Elements.RandomOptimizedFluxLayout
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


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_best_optimized_solution,
            ParameterName.data_name: DataName.hct116_cultured_cell_line,
        }
        scale = 0.4
        hct116_cultured_cell_line_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = hct116_cultured_cell_line_flux_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
        hct116_cultured_cell_line_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_flux_error_bar_comparison_figure.name:
                hct116_cultured_cell_line_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


common_random_optimized_figure_scale = 0.6


class SubfigureD(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'distance_between_global_and_local_optima_sqaured_loss'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_random_optimized_figure_scale

        running_time_and_loss_config_dict = {
            ParameterName.total_width: 0.8,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale
        }
        random_optimized_loss_distance_obj = Elements.RandomOptimizedLossDistanceComparison(
            **running_time_and_loss_config_dict)

        center = random_optimized_loss_distance_obj.calculate_center(random_optimized_loss_distance_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.005)
        random_optimized_loss_distance_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            random_optimized_loss_distance_obj.name: random_optimized_loss_distance_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class FigureS1(Elements.Figure):
    figure_label = 'figure_s1'
    figure_title = 'Figure S1'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            # SubfigureD,
            # SubfigureE,
            # SubfigureF,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_a_width = 0.5
        subfigure_a_height = 0.32
        subfigure_c_width = 1 - subfigure_a_width
        subfigure_c_height = 0.53
        subfigure_c_center = Vector(subfigure_a_width + subfigure_c_width / 2, subfigure_c_height / 2)
        subfigure_c_size = Vector(subfigure_c_width, subfigure_c_height)
        subfigure_b_height = 0.2

        figure_layout_list = [
            (subfigure_a_height, [
                (subfigure_a_width, 'a')]),
            (subfigure_b_height, [
                (subfigure_a_width, 'b')]),
            # (0.25, [(0.55, 'c'), (0.45, 'd')]),
            # (0.25, [(0.44, 'e'), (0.56, 'f')]),
        ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_obj_list.extend([
            single_subfigure_layout(
                subfigure_c_center, subfigure_c_size, SubfigureC, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
        ])

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
