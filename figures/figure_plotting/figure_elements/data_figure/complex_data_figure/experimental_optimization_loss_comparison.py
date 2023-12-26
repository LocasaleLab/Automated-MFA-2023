from ..config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName, TextBox, \
    CommonFigureString, default_parameter_extract, CommonFigureMaterials, CommonElementConfig
from ..basic_data_figure.violin_box_data_figure import BasicViolinBoxDataFigure, \
    ExperimentalOptimizationLossComparisonBoxDataFigure


class ExperimentalOptimizationLossComparison(CompositeFigure):
    height_to_width_ratio = 0.5
    total_width = 0.5
    total_height = 0.5
    each_row_height = 0.45
    legend_height = 0.05

    def __init__(
            self, figure_data_parameter_dict, total_width=1, **kwargs):
        result_label_layout_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.result_label_layout_list, None)
        if result_label_layout_list is None:
            total_row_num = 1
        else:
            total_row_num = len(result_label_layout_list)
        figure_height = ExperimentalOptimizationLossComparisonBoxDataFigure.calculate_height(
            ExperimentalOptimizationLossComparisonBoxDataFigure, total_row_num)
        total_height = figure_height + self.legend_height
        legend_bottom = figure_height + 0.005
        legend_top = total_height - 0.005

        legend_name_dict, legend_color_dict = default_parameter_extract(
            figure_data_parameter_dict,
            [ParameterName.name_dict, ParameterName.color_dict],
            [CommonFigureMaterials.mid_comparison_name_dict, CommonFigureMaterials.mid_comparison_color_dict]
        )
        legend_config_dict = {
            ParameterName.legend_center: Vector(0.5 * total_width, (legend_top + legend_bottom) / 2),
            ParameterName.legend_area_size: Vector(total_width, legend_top - legend_bottom),
            ParameterName.name_dict: legend_name_dict,
            ParameterName.text_config_dict: {
                ParameterName.font_size: 10,
                ParameterName.font_weight: FontWeight.bold
            }
        }

        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        bottom_line = 0

        common_text_config_dict = {
            **CommonElementConfig.common_text_config,
            # ParameterName.font: DataFigureConfig.main_text_font,
            # ParameterName.z_order: DataFigureConfig.figure_text_z_order,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.text_box: False,
        }

        # experimental_data_figure_parameter_dict = default_parameter_extract(
        #     figure_data_parameter_dict, ParameterName.raw_data_figure_parameter_dict, None, pop=True, force=True)
        figure_class = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_class, ParameterName.box, pop=True)
        # experimental_data_figure_parameter_dict = figure_data_parameter_dict.pop(
        #     ParameterName.raw_data_figure_parameter_dict)
        # figure_class = figure_data_parameter_dict.pop(ParameterName.figure_class)

        experimental_data_loss_grid_comparison_figure = ExperimentalOptimizationLossComparisonBoxDataFigure(**{
            ParameterName.bottom_left: Vector(0, bottom_line),
            ParameterName.size: Vector(total_width, figure_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.color_dict: legend_color_dict,
                ParameterName.figure_class: figure_class,
                ParameterName.result_label_layout_list: result_label_layout_list,
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict,
                **figure_data_parameter_dict,
            },
            ParameterName.background: False
        })

        subfigure_element_dict = {
            'loss_comparison': {
                'loss_comparison': experimental_data_loss_grid_comparison_figure},
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)




