from ...common.config import DataFigureConfig, ParameterName, Vector, FontWeight, CompositeFigure, DataName
from ...common.common_figure_materials import CommonFigureMaterials
from ..data_figure.histogram_data_figure import TimeLossDistanceHistogramDataFigure


class TimeLossStack(CompositeFigure):
    height_to_width_ratio = 0.82

    def __init__(
            self, total_width=1,
            # scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1,
            **kwargs):
        self.total_width = total_width
        bottom_line = 0 * total_width
        running_time_height = 0.24 * total_width
        loss_height = 0.44 * total_width
        loss_top = bottom_line + loss_height
        legend_interval = 0.002 * total_width
        legend_bottom = loss_top + legend_interval
        legend_height = 0.06 * total_width
        legend_top = legend_bottom + legend_height
        legend_center_y = legend_bottom + legend_height / 2
        running_time_interval = 0.04 * total_width
        running_time_bottom = legend_top + running_time_interval
        running_time_top = running_time_bottom + running_time_height
        total_height = running_time_top
        self.height_to_width_ratio = total_height / total_width
        common_color_dict = CommonFigureMaterials.histogram_color_dict
        running_time_config_dict = {
            ParameterName.bottom_left: (0, running_time_bottom),
            ParameterName.size: [total_width, running_time_height],
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.time_data,
                ParameterName.data_name: DataName.hct116_cultured_cell_line,
                ParameterName.color_dict: common_color_dict,
            },
        }
        legend_config_dict = {
            ParameterName.legend_center: Vector(0.5 * total_width, legend_center_y),
            ParameterName.legend_area_size: Vector(total_width, legend_height),
            ParameterName.name_dict: CommonFigureMaterials.time_loss_name_dict,
            ParameterName.text_config_dict: {
                ParameterName.font_size: 10,
                ParameterName.font_weight: FontWeight.bold
            }
        }
        running_loss_config_dict = {
            ParameterName.bottom_left: (0, bottom_line),
            ParameterName.size: [total_width, loss_height],
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.loss_data,
                ParameterName.data_name: DataName.hct116_cultured_cell_line,
                ParameterName.color_dict: common_color_dict,
                ParameterName.legend: True,
                ParameterName.legend_config_dict: legend_config_dict
            },
        }

        subfigure_element_dict = {
            'running_time': {
                'running_time': TimeLossDistanceHistogramDataFigure(**running_time_config_dict)},
            'running_loss': {
                'running_loss': TimeLossDistanceHistogramDataFigure(**running_loss_config_dict)}
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height),
            # bottom_left_offset=bottom_left_offset, scale=scale,
            # base_z_order=base_z_order, z_order_increment=z_order_increment,
            background=False, **kwargs)

