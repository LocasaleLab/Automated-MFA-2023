from ...common.config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, TextBox, \
    default_parameter_extract
from ..data_figure.scatter_data_figure import FluxComparisonScatterDataFigure


class FluxComparisonScatterWithTitle(CompositeFigure):
    height_to_width_ratio = 0.8
    each_row_height = 0.15
    each_row_gap_height = 0.028
    each_col_gap_width = 0.033
    legend_area_height = 0.04
    title_area_height = 0.04
    upper_distance = 0.02
    bottom_tick_label_height = 0.04
    left_tick_label_width = 0.06
    right_edge_width = 0.02
    text_left_offset = 0.02

    @staticmethod
    def get_row_num(flux_name_list):
        scatter_row_num = len(flux_name_list)
        return scatter_row_num

    @staticmethod
    def calculate_scatter_height(self, row_num):
        return self.each_row_height * row_num + self.each_row_gap_height * (row_num - 1)

    @staticmethod
    def calculate_total_height(self, scatter_height, legend, figure_title):
        return scatter_height + self.bottom_tick_label_height + self.upper_distance + \
            (self.legend_area_height if legend else 0) + (self.title_area_height if figure_title is not None else 0)

    @staticmethod
    def calculate_center(self, scale, *args):
        legend = False
        figure_title = None
        if len(args) == 1:
            flux_name_list = args[0]
        elif len(args) == 2:
            flux_name_list, legend = args
        elif len(args) == 3:
            flux_name_list, legend, figure_title = args
        else:
            raise ValueError()
        scatter_height = self.calculate_scatter_height(self, self.get_row_num(flux_name_list))
        total_height = self.calculate_total_height(self, scatter_height, legend, figure_title)
        return Vector(self.total_width, total_height) * scale / 2

    def __init__(
            self, figure_data_parameter_dict,
            total_width=1, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        try:
            height_to_width_ratio = figure_data_parameter_dict.pop(ParameterName.height_to_width_ratio)
        except KeyError:
            pass
        else:
            self.height_to_width_ratio = height_to_width_ratio
        # try:
        #     figure_title = figure_data_parameter_dict.pop(ParameterName.figure_title)
        # except KeyError:
        #     figure_title = None
        # try:
        #     legend = figure_data_parameter_dict[ParameterName.legend]
        # except KeyError:
        #     legend = False
        figure_title = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_title, None, pop=True)
        legend = default_parameter_extract(figure_data_parameter_dict, ParameterName.legend, False)
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]

        self.total_width = total_width
        legend_area_height = self.legend_area_height
        title_area_height = self.title_area_height
        each_row_gap_height = self.each_row_gap_height
        each_col_gap_width = self.each_col_gap_width
        bottom_tick_label_height = self.bottom_tick_label_height
        left_tick_label_width = self.left_tick_label_width
        right_edge_width = self.right_edge_width
        text_left_offset = self.text_left_offset
        upper_distance = self.upper_distance
        row_num = self.get_row_num(flux_name_list)
        # total_height = total_width * self.height_to_width_ratio
        scatter_height = self.calculate_scatter_height(self, row_num)
        scatter_width = total_width - left_tick_label_width - right_edge_width
        scatter_bottom_left = Vector(left_tick_label_width, bottom_tick_label_height)
        scatter_interval_y = each_row_gap_height / scatter_height
        scatter_interval_x = each_col_gap_width / scatter_width
        scatter_interval = Vector(scatter_interval_x, scatter_interval_y)

        total_height = self.calculate_total_height(self, scatter_height, legend, figure_title)
        # bottom_line = 0.01 * total_width
        # top_line = 0.01 * total_width
        # side_edge = 0.02 * total_width
        # axis_width = total_width - 2 * side_edge
        # text_left_offset = 0.05 * total_width
        # figure_left_edge = side_edge
        # figure_title_height = 0.08 * total_width
        # figure_title_distance = 0.04 * total_width
        # if figure_title is None:
        #     axis_legend_height = total_height - bottom_line - top_line
        # else:
        #     # axis_height = 0.87 * total_height
        #     axis_legend_height = total_height - bottom_line - top_line - figure_title_height - figure_title_distance

        current_top_y_value = bottom_tick_label_height + scatter_height + upper_distance
        if legend:
            # legend_height = 0.06 * total_width
            # legend_axis_gap_height = 0.05 * total_width
            # axis_height = axis_legend_height - legend_height - legend_axis_gap_height
            legend_y_center = current_top_y_value + legend_area_height / 2
            current_top_y_value += legend_area_height
            legend_config_dict = {
                ParameterName.legend_center: Vector(0.55 * total_width, legend_y_center),
                ParameterName.legend_area_size: Vector(0.8 * total_width, legend_area_height),
                ParameterName.name_dict: figure_data_parameter_dict.pop(ParameterName.name_dict),
                ParameterName.text_config_dict: {
                    ParameterName.font_size: 8.5,
                    ParameterName.font_weight: FontWeight.bold
                }
            }
        else:
            # axis_height = axis_legend_height
            legend_config_dict = None
        common_text_config_dict = {
            **DataFigureConfig.common_title_config_dict,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.text_box: False,
        }
        if figure_title is not None:
            figure_title_y_value = current_top_y_value + title_area_height / 2
            current_top_y_value += title_area_height
            figure_title_text_config_dict = {
                ParameterName.string: figure_title,
                ParameterName.center: Vector(total_width / 2 + text_left_offset, figure_title_y_value),
                ParameterName.width: total_width * 0.8,
                ParameterName.height: title_area_height,
                **common_text_config_dict,
                ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 1,
            }

            figure_title_text_box_obj = TextBox(**figure_title_text_config_dict)
            # figure_title_y_value = axis_top_y_value + figure_title_distance + figure_title_height / 2
        else:
            figure_title_text_box_obj = None

        flux_comparison_scatter_figure = FluxComparisonScatterDataFigure(**{
            ParameterName.bottom_left: scatter_bottom_left,
            ParameterName.size: Vector(scatter_width, scatter_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.ax_interval: scatter_interval,
                ParameterName.legend: legend,
                ParameterName.legend_config_dict: legend_config_dict,
                **figure_data_parameter_dict
            },
        })
        subfigure_element_dict = {
            'data_figure': {
                'data_figure': flux_comparison_scatter_figure,
            },
        }
        if figure_title:
            subfigure_element_dict.update({
                'title': {
                    'title': figure_title_text_box_obj,
                }
            })
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height),
            bottom_left_offset=bottom_left_offset, scale=scale,
            base_z_order=base_z_order, z_order_increment=z_order_increment, background=False, **kwargs)




