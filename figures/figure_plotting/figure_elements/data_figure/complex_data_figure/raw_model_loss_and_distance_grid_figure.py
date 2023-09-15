from ..config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName, TextBox, \
    CommonFigureString
from ..basic_data_figure.violin_box_data_figure import TimeLossGridBoxDataFigure


class LossDistanceGridFigure(CompositeFigure):
    height_to_width_ratio = 0.8

    def __init__(
            self, figure_data_parameter_dict,
            total_width=1, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        self.total_width = total_width
        total_height = total_width * self.height_to_width_ratio
        axis_height = 0.7 * total_width
        bottom_line = 0.03 * total_width
        side_edge = 0.05 * total_width
        interval = 0.05 * total_width
        axis_width = (total_width - 2 * side_edge - interval) / 2
        text_left_offset = 0.05 * total_width
        left_figure_left_edge = side_edge
        right_figure_left_edge = side_edge + axis_width + interval
        subfigure_title_height = 0.03 * total_width
        left_subfigure_title_x_value = left_figure_left_edge + axis_width / 2 + text_left_offset
        right_subfigure_title_x_value = right_figure_left_edge + axis_width / 2 + text_left_offset
        axis_top_y_value = bottom_line + axis_height
        subfigure_title_distance = 0.01 * total_width
        subfigure_title_y_value = axis_top_y_value + subfigure_title_distance + subfigure_title_height / 2
        figure_title_height = 0.03 * total_width
        figure_title_y_value = axis_top_y_value + subfigure_title_distance + 0.03 * total_width + figure_title_height / 2
        figure_title = figure_data_parameter_dict[ParameterName.figure_title]
        common_text_config_dict = {
            ParameterName.font: DataFigureConfig.main_text_font,
            ParameterName.z_order: DataFigureConfig.figure_text_z_order,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.text_box: False,
        }
        subfigure_title_text_config_dict = {
            ParameterName.width: axis_width,
            ParameterName.height: subfigure_title_height,
            **common_text_config_dict,
        }
        figure_title_text_config_dict = {
            ParameterName.string: figure_title,
            ParameterName.center: Vector(total_width / 2 + text_left_offset, figure_title_y_value),
            ParameterName.width: total_width,
            ParameterName.height: figure_title_height,
            **common_text_config_dict,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_label_font_size + 5,
        }

        figure_type = figure_data_parameter_dict.pop(ParameterName.figure_type)
        all_data_figure_parameter_dict = figure_data_parameter_dict.pop(ParameterName.all_data_figure_parameter_dict)
        experimental_data_figure_parameter_dict = figure_data_parameter_dict.pop(
            ParameterName.raw_data_figure_parameter_dict)
        figure_class = figure_data_parameter_dict.pop(ParameterName.figure_class)
        if figure_class is not None:
            experimental_data_figure_parameter_dict[ParameterName.figure_class] = figure_class
            all_data_figure_parameter_dict[ParameterName.figure_class] = figure_class
        all_data_loss_grid_comparison_figure = figure_type(**{
            ParameterName.bottom_left: Vector(left_figure_left_edge, bottom_line),
            ParameterName.size: Vector(axis_width, axis_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.raw_model_all_data,
                **all_data_figure_parameter_dict,
            },
            ParameterName.background: False
        })
        all_data_text_box_obj = TextBox(**{
            ParameterName.string: CommonFigureString.all_available_mid_data,
            ParameterName.center: Vector(left_subfigure_title_x_value, subfigure_title_y_value),
            **subfigure_title_text_config_dict,
        })

        experimental_data_loss_grid_comparison_figure = figure_type(**{
            ParameterName.bottom_left: Vector(right_figure_left_edge, bottom_line),
            ParameterName.size: Vector(axis_width, axis_height),
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: DataName.raw_model_raw_data,
                **experimental_data_figure_parameter_dict,
            },
            ParameterName.background: False
        })
        experimental_data_text_box_obj = TextBox(**{
            ParameterName.string: CommonFigureString.experimental_available_mid_data,
            ParameterName.center: Vector(right_subfigure_title_x_value, subfigure_title_y_value),
            **subfigure_title_text_config_dict,
        })

        figure_title_text_box_obj = TextBox(**figure_title_text_config_dict)
        subfigure_element_dict = {
            'all_data_figure': {
                'title': all_data_text_box_obj,
                'data_figure': all_data_loss_grid_comparison_figure,
            },
            'experimental_data_figure': {
                'title': experimental_data_text_box_obj,
                'data_figure': experimental_data_loss_grid_comparison_figure,
            },
            'title': {
                'title': figure_title_text_box_obj,
            }
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height),
            bottom_left_offset=bottom_left_offset, scale=scale,
            base_z_order=base_z_order, z_order_increment=z_order_increment, background=False, **kwargs)




