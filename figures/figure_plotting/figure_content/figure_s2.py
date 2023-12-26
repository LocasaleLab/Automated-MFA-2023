from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.elements import Elements

from .common_functions import calculate_subfigure_layout
from ..common.common_figure_materials import FigureConfig, CommonFigureString, CommonFigureMaterials, \
    calculate_center_bottom_offset

Subfigure = Elements.Subfigure
common_data_figure_scale = 0.46
# common_data_figure_scale = 0.2
common_data_width = 1
subfigure_a_b_offset = Vector(0.01, -0.01)
subfigure_c_d_offset = Vector(0, -0.01)
subfigure_c_d_scale = 0.9


all_net_flux_comparison_scale = 0.35
OptimizedAllFluxComparisonBarDataFigure = Elements.OptimizedAllFluxComparisonBarDataFigure
all_data_optimized_size = 20000
all_data_selection_size = 100
raw_data_optimized_size = 20000
raw_data_selection_size = 100


wrap_name_dict, _ = CommonFigureMaterials.select_average_solution_name_color_dict(
    CommonFigureMaterials, with_reoptimization=True, wrap_name=True)
raw_distance_x_label_list = list(wrap_name_dict.values())


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'raw_distance_figure_all_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.all_available_mid_data,
            ParameterName.figure_class: ParameterName.raw_distance,
            ParameterName.data_name: DataName.optimization_from_solutions_all_data,
            ParameterName.common_y_lim: [1000, 4000],
            ParameterName.default_y_tick_label_list: [1000, 2000, 3000, 4000],
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: name_dict,
            ParameterName.x_tick_labels_list: raw_distance_x_label_list,
        }
        scale = common_data_figure_scale
        raw_distance_comparison_figure = Elements.SingleLossOrDistanceFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = raw_distance_comparison_figure.calculate_center(raw_distance_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        raw_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_distance_comparison_figure.name: raw_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'raw_distance_figure_raw_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.experimental_available_mid_data,
            ParameterName.figure_class: ParameterName.raw_distance,
            ParameterName.data_name: DataName.optimization_from_solutions_raw_data,
            ParameterName.common_y_lim: [1000, 4000],
            ParameterName.default_y_tick_label_list: [1000, 2000, 3000, 4000],
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: name_dict,
            ParameterName.x_tick_labels_list: raw_distance_x_label_list,
        }
        scale = common_data_figure_scale
        raw_distance_comparison_figure = Elements.SingleLossOrDistanceFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = raw_distance_comparison_figure.calculate_center(raw_distance_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        raw_distance_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_distance_comparison_figure.name: raw_distance_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'flux_relative_error_comparison_all_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.relative_error_to_known_flux,
            ParameterName.figure_subtitle: CommonFigureString.optimization_selection_title_constructor(
                all_data_optimized_size, all_data_selection_size),
            ParameterName.data_name: DataName.optimization_from_solutions_all_data,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
        }
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_relative_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_relative_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_all_data_flux_relative_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_relative_error_bar_comparison_figure.name:
                raw_model_all_data_flux_relative_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'flux_relative_error_comparison_raw_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.relative_error_to_known_flux,
            ParameterName.figure_subtitle: CommonFigureString.optimization_selection_title_constructor(
                raw_data_optimized_size, raw_data_selection_size),
            ParameterName.data_name: DataName.optimization_from_solutions_raw_data,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
        }
        scale = all_net_flux_comparison_scale
        raw_model_raw_data_flux_relative_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_raw_data_flux_relative_error_bar_comparison_figure.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_raw_data_flux_relative_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_raw_data_flux_relative_error_bar_comparison_figure.name:
                raw_model_raw_data_flux_relative_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)



LossDistanceSinglePairFigure = Elements.LossDistanceSinglePairFigure
batched_simulated_figure_total_width = 1


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'optimization_from_batched_simulated_all_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.all_available_mid_data,
            ParameterName.data_name: DataName.optimization_from_solutions_batched_all_data,
            ParameterName.optimized: True,
            ParameterName.different_simulated_distance: True,
            ParameterName.total_width: batched_simulated_figure_total_width,
            ParameterName.optimized_size: all_data_optimized_size,
            ParameterName.selection_size: all_data_selection_size,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.03],
                ParameterName.default_y_tick_label_list: [0, 0.01, 0.02, 0.03],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 1300],
                ParameterName.default_y_tick_label_list: [0, 400, 800, 1200]
            }
        }
        scale = common_data_figure_scale
        optimization_from_batched_simulated_data = LossDistanceSinglePairFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = optimization_from_batched_simulated_data.calculate_center(optimization_from_batched_simulated_data, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        optimization_from_batched_simulated_data.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            optimization_from_batched_simulated_data.name: optimization_from_batched_simulated_data}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'optimization_from_batched_simulated_raw_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.experimental_available_mid_data,
            ParameterName.data_name: DataName.optimization_from_solutions_batched_raw_data,
            ParameterName.optimized: True,
            ParameterName.different_simulated_distance: True,
            ParameterName.total_width: batched_simulated_figure_total_width,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.4],
                ParameterName.default_y_tick_label_list: [0, 0.1, 0.2, 0.3, 0.4],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 1300],
                ParameterName.default_y_tick_label_list: [0, 400, 800, 1200]
            }
        }
        scale = common_data_figure_scale
        optimization_from_batched_simulated_data = LossDistanceSinglePairFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = optimization_from_batched_simulated_data.calculate_center(optimization_from_batched_simulated_data, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        optimization_from_batched_simulated_data.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            optimization_from_batched_simulated_data.name: optimization_from_batched_simulated_data}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


LossDistanceGridFigure = Elements.LossDistanceGridFigure
name_dict, color_dict = CommonFigureMaterials.select_average_solution_name_color_dict(
    CommonFigureMaterials, with_reoptimization=True, wrap_name=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'all_data_loss_distance_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.all_available_mid_data,
            ParameterName.data_name: DataName.optimization_from_solutions_all_data,
            ParameterName.legend: True,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.65],
                ParameterName.default_y_tick_label_list: [0, 0.2, 0.4, 0.6],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 850],
                ParameterName.default_y_tick_label_list: [0, 400, 800]
            },
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: name_dict,
        }
        scale = common_data_figure_scale
        loss_distance_grid_comparison_figure = LossDistanceGridFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_distance_grid_comparison_figure.calculate_center(loss_distance_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        loss_distance_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_a_b_offset)

        subfigure_element_dict = {
            loss_distance_grid_comparison_figure.name: loss_distance_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'raw_data_loss_distance_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.experimental_available_mid_data,
            ParameterName.data_name: DataName.optimization_from_solutions_raw_data,
            ParameterName.legend: True,
            ParameterName.loss_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 0.9],
                ParameterName.default_y_tick_label_list: [0, 0.4, 0.8],
            },
            ParameterName.net_distance_data_figure_parameter_dict: {
                ParameterName.common_y_lim: [0, 850],
                ParameterName.default_y_tick_label_list: [0, 400, 800]
            },
            ParameterName.color_dict: color_dict,
            ParameterName.name_dict: name_dict,
        }
        scale = common_data_figure_scale
        loss_distance_grid_comparison_figure = LossDistanceGridFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_distance_grid_comparison_figure.calculate_center(loss_distance_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        loss_distance_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset + subfigure_a_b_offset)

        subfigure_element_dict = {
            loss_distance_grid_comparison_figure.name: loss_distance_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS2(Elements.Figure):
    figure_label = 'figure_s2'
    figure_title = 'Figure S2'

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
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_c_d_height = 0.26
        figure_layout_list = [
            (0.13, [(0.5, 'a'), (0.5, 'e')]),
            (0.26, [(0.5, 'b'), (0.5, 'f')]),
            (0.21, [(0.5, 'c'), (0.5, 'g')]),
            (0.3, [(0.5, 'd'), (0.5, 'h')]),
            # (subfigure_c_d_height, [(1, 'c')]),
            # (subfigure_c_d_height, [(1, 'd')]),
            # (0.25, [(0.44, 'e'), (0.56, 'f')]),
        ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

