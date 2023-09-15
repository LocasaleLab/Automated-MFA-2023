from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict
from ..common.color import ColorConfig

from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout
from ..common.common_figure_materials import FigureConfig, CommonFigureString, CommonFigureMaterials

Subfigure = element_dict[ElementName.Subfigure]
MIDComparisonGridBarWithLegendDataFigure = element_dict[ElementName.MIDComparisonGridBarWithLegendDataFigure]
TimeLossGridBoxDataFigure = element_dict[ElementName.TimeLossGridBoxDataFigure]
GridScatterDataFigure = element_dict[ElementName.GridScatterDataFigure]
LossDistanceGridFigure = element_dict[ElementName.LossDistanceGridFigure]
ProtocolAllFluxHeatmap = element_dict[ElementName.ProtocolAllFluxHeatmap]
common_data_figure_scale = 0.48
# common_data_figure_scale = 0.2
common_data_width = 1
subfigure_a_b_offset = Vector(0, -0.01)
subfigure_c_d_offset = Vector(0, -0.01)
subfigure_c_d_scale = 0.9


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.loss,
            ParameterName.figure_class: None,
            ParameterName.figure_type: TimeLossGridBoxDataFigure,
            ParameterName.raw_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.25],
                ParameterName.default_y_tick_label_list: [0, 0.1, 0.2],
            },
            ParameterName.all_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.65],
                ParameterName.default_y_tick_label_list: [0, 0.2, 0.4, 0.6],
            }
        }
        scale = common_data_figure_scale
        loss_grid_comparison_figure = LossDistanceGridFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_grid_comparison_figure.calculate_center(loss_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        loss_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_a_b_offset)

        subfigure_element_dict = {
            loss_grid_comparison_figure.name: loss_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'euclidean_scatter_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.euclidean_distance,
            ParameterName.figure_class: ParameterName.net_euclidean_distance,
            ParameterName.figure_type: GridScatterDataFigure,
            ParameterName.raw_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 650],
                ParameterName.default_y_tick_label_list: [0, 200, 400, 600]
            },
            ParameterName.all_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 500],
                ParameterName.default_y_tick_label_list: [0, 200, 400]
            }
        }
        scale = common_data_figure_scale
        loss_grid_comparison_figure = LossDistanceGridFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_grid_comparison_figure.calculate_center(loss_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        loss_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_a_b_offset)

        subfigure_element_dict = {
            loss_grid_comparison_figure.name: loss_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'flux_relative_error_figure_all_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.flux_name_list: CommonFigureMaterials.protocol_sensitivity_display_flux_list,
            ParameterName.figure_title: CommonFigureString.all_available_mid_data,
            ParameterName.data_name: DataName.raw_model_all_data,
        }
        scale = subfigure_c_d_scale
        all_flux_heatmap_figure = ProtocolAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = all_flux_heatmap_figure.calculate_center(all_flux_heatmap_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        all_flux_heatmap_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_c_d_offset)

        subfigure_element_dict = {
            all_flux_heatmap_figure.name: all_flux_heatmap_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'flux_relative_error_figure_experimental_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.flux_name_list: CommonFigureMaterials.protocol_sensitivity_display_flux_list,
            ParameterName.figure_title: CommonFigureString.experimental_available_mid_data,
            ParameterName.data_name: DataName.raw_model_raw_data,
        }
        scale = subfigure_c_d_scale
        all_flux_heatmap_figure = ProtocolAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = all_flux_heatmap_figure.calculate_center(all_flux_heatmap_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        all_flux_heatmap_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_c_d_offset)

        subfigure_element_dict = {
            all_flux_heatmap_figure.name: all_flux_heatmap_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS2(element_dict[ElementName.Figure]):
    figure_label = 'figure_s2'
    figure_title = 'Figure S2'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            # SubfigureE,
            # SubfigureF,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_c_d_height = 0.26
        figure_layout_list = [
            (0.3, [(0.5, 'a'), (0.5, 'b')]),
            (subfigure_c_d_height, [(1, 'c')]),
            (subfigure_c_d_height, [(1, 'd')]),
            # (0.25, [(0.44, 'e'), (0.56, 'f')]),
        ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

