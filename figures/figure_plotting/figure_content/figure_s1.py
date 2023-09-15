from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict

from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout
from ..common.common_figure_materials import FigureConfig

Subfigure = element_dict[ElementName.Subfigure]
MIDComparisonGridBarWithLegendDataFigure = element_dict[ElementName.MIDComparisonGridBarWithLegendDataFigure]


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.hct116_cultured_cell_line,
            ParameterName.result_label: 'HCT116_WQ2101__ctrl__1',
        }
        scale = 0.7
        hct116_cultured_cell_line_mid_comparison_figure = MIDComparisonGridBarWithLegendDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + Vector(0, 0.002),
            ParameterName.total_width: 1.2,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = hct116_cultured_cell_line_mid_comparison_figure.calculate_center(
            hct116_cultured_cell_line_mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.005)
        hct116_cultured_cell_line_mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            hct116_cultured_cell_line_mid_comparison_figure.name: hct116_cultured_cell_line_mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS1(element_dict[ElementName.Figure]):
    figure_label = 'figure_s1'
    figure_title = 'Figure S1'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            # SubfigureB,
            # SubfigureC,
            # SubfigureD,
            # SubfigureE,
            # SubfigureF,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        figure_layout_list = [
            (0.55, [(1, 'a')]),
            # (0.25, [(0.55, 'c'), (0.45, 'd')]),
            # (0.25, [(0.44, 'e'), (0.56, 'f')]),
        ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
