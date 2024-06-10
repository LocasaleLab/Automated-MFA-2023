from ...common.config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName, \
    default_parameter_extract
from ...common.common_figure_materials import CommonFigureMaterials
from ..data_figure.bar_data_figure import MIDComparisonGridBarDataFigure


class MIDComparisonGridBarWithLegendDataFigure(CompositeFigure):
    height_to_width_ratio = 0.8
    legend_height = 0.06

    def __init__(
            self, figure_data_parameter_dict, total_width=1, **kwargs):
        self.total_width = total_width
        mid_name_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.mid_name_list, CommonFigureMaterials.default_mid_name_list)
        legend_name_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.name_dict, CommonFigureMaterials.mid_comparison_name_dict)
        legend_color_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.color_dict, CommonFigureMaterials.mid_comparison_color_dict)
        specific_legend_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.legend_config_dict, {}, pop=True)
        total_row_num = len(mid_name_list)
        figure_height = MIDComparisonGridBarDataFigure.calculate_height(MIDComparisonGridBarDataFigure, total_row_num)
        total_height = figure_height + self.legend_height
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        bottom_line = 0
        legend_bottom = figure_height + 0.005
        legend_top = total_height - 0.005
        legend_config_dict = {
            ParameterName.legend_center: Vector(0.5 * total_width, (legend_top + legend_bottom) / 2),
            ParameterName.legend_area_size: Vector(total_width, legend_top - legend_bottom),
            ParameterName.name_dict: legend_name_dict,
            ParameterName.text_config_dict: {
                ParameterName.font_size: 10,
                ParameterName.font_weight: FontWeight.bold
            },
            **specific_legend_config_dict,
        }

        mid_comparison_config_dict = {
            ParameterName.bottom_left: (0, bottom_line),
            ParameterName.size: Vector(total_width, figure_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.color_dict: legend_color_dict,
                ParameterName.mid_name_list: mid_name_list,
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict,
                ParameterName.size: Vector(total_width, figure_height),
                **figure_data_parameter_dict,
            },
        }

        subfigure_element_dict = {
            'mid_comparison': {
                'mid_comparison': MIDComparisonGridBarDataFigure(**mid_comparison_config_dict)},
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height),
            background=False, **kwargs)




