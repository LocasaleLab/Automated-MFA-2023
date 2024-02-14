from ...common.config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName, TextBox, \
    default_parameter_extract, CommonElementConfig
from ..data_figure.violin_box_data_figure import FluxComparisonViolinBoxDataFigure


class FluxComparisonViolinBoxWithTitleLegend(CompositeFigure):
    height_to_width_ratio = 1

    def __init__(
            self, figure_data_parameter_dict,
            total_width=1, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        try:
            height_to_width_ratio = figure_data_parameter_dict[ParameterName.height_to_width_ratio]
        except KeyError:
            pass
        else:
            self.height_to_width_ratio = height_to_width_ratio
        # try:
        #     figure_title = figure_data_parameter_dict[ParameterName.figure_title]
        # except KeyError:
        #     figure_title = None
        figure_title = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_title, None)
        # try:
        #     legend = figure_data_parameter_dict[ParameterName.legend]
        # except KeyError:
        #     legend = True
        legend = default_parameter_extract(figure_data_parameter_dict, ParameterName.legend, True)

        self.total_width = total_width
        total_height = total_width * self.height_to_width_ratio
        bottom_line = 0.01 * total_width
        top_line = 0.01 * total_width
        side_edge = 0.02 * total_width
        axis_width = total_width - 2 * side_edge
        text_left_offset = 0.05 * total_width
        figure_left_edge = side_edge
        figure_title_height = 0.08 * total_width
        figure_title_distance = 0.01 * total_width
        if figure_title is None:
            axis_legend_height = total_height - bottom_line - top_line
        else:
            # axis_legend_height = 0.87 * total_height
            axis_legend_height = total_height - bottom_line - top_line - figure_title_height - figure_title_distance
        axis_legend_top_y_value = bottom_line + axis_legend_height
        figure_title_y_value = axis_legend_top_y_value + figure_title_distance + figure_title_height / 2
        common_text_config_dict = {
            **CommonElementConfig.common_text_config,
            # ParameterName.font: DataFigureConfig.main_text_font,
            # ParameterName.z_order: DataFigureConfig.figure_text_z_order,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.text_box: False,
        }
        if legend:
            legend_height = 0.05 * total_width
            legend_axis_gap_height = 0.03 * total_width
            axis_height = axis_legend_height - legend_height - legend_axis_gap_height
            legend_y_center = axis_legend_height - legend_height / 2
            legend_config_dict = {
                ParameterName.legend_center: Vector(0.6 * total_width, legend_y_center),
                ParameterName.legend_area_size: Vector(0.8 * total_width, legend_height),
                ParameterName.name_dict: figure_data_parameter_dict.pop(ParameterName.name_dict),
                ParameterName.text_config_dict: {
                    ParameterName.font_size: 10,
                    ParameterName.font_weight: FontWeight.bold
                }
            }
        else:
            axis_height = axis_legend_height
            legend_config_dict = None
        flux_comparison_scatter_figure = FluxComparisonViolinBoxDataFigure(**{
            ParameterName.bottom_left: Vector(figure_left_edge, bottom_line),
            ParameterName.size: Vector(axis_width, axis_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.legend: legend,
                ParameterName.legend_config_dict: legend_config_dict,
                **figure_data_parameter_dict},
            ParameterName.background: False
        })
        subfigure_element_dict = {
            'data_figure': {
                'data_figure': flux_comparison_scatter_figure,
            },
        }
        if figure_title is not None:
            figure_title_text_config_dict = {
                ParameterName.string: figure_title,
                ParameterName.center: Vector(total_width / 2 + text_left_offset, figure_title_y_value),
                ParameterName.width: total_width * 0.8,
                ParameterName.height: figure_title_height,
                **common_text_config_dict,
                ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 1,
            }

            figure_title_text_box_obj = TextBox(**figure_title_text_config_dict)
            subfigure_element_dict.update({
                'title': {
                    'title': figure_title_text_box_obj,
                }
            })
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height),
            bottom_left_offset=bottom_left_offset, scale=scale,
            base_z_order=base_z_order, z_order_increment=z_order_increment, background=False, **kwargs)




