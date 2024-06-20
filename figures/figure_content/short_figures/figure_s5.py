from ..common.config import ParameterName, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import ColonCancerAllIndexSupMaterials, colon_cancer_comparison_dict_generator
from .short_figure_config import (
    common_result_label_constructor, colon_cancer_data_set, colon_cancer_traditional_data_set, common_data_width)

Subfigure = Elements.Subfigure
subfigure_a_c_loss_scale = 0.45
subfigure_a_c_loss_total_width = 0.6


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'colon_cancer_loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: colon_cancer_data_set,
            ParameterName.name_dict: ColonCancerAllIndexSupMaterials.name_dict,
            ParameterName.color_dict: ColonCancerAllIndexSupMaterials.color_dict,
            ParameterName.y_lim_list: ColonCancerAllIndexSupMaterials.loss_y_lim,
            ParameterName.y_ticks_list: ColonCancerAllIndexSupMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: ColonCancerAllIndexSupMaterials.loss_y_tick_labels,
        }
        scale = subfigure_a_c_loss_scale
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: subfigure_a_c_loss_total_width,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = mid_comparison_figure.calculate_center(mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.02, 0.01)
        mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_figure.name: mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'colon_cancer_mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: colon_cancer_data_set,
            ParameterName.result_label: common_result_label_constructor('colon_cancer', 'high'),
            ParameterName.mid_name_list: ColonCancerAllIndexSupMaterials.target_mid_name_list,
            ParameterName.name_dict: ColonCancerAllIndexSupMaterials.mid_name_dict,
            ParameterName.color_dict: ColonCancerAllIndexSupMaterials.mid_color_dict,
        }
        scale = 0.45
        mid_comparison_figure = Elements.MIDComparisonGridBarWithLegendDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.9,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = mid_comparison_figure.calculate_center(mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.003)
        mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_figure.name: mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'colon_cancer_with_traditional_method_loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: colon_cancer_traditional_data_set,
            ParameterName.name_dict: ColonCancerAllIndexSupMaterials.name_dict,
            ParameterName.color_dict: ColonCancerAllIndexSupMaterials.color_dict,
            ParameterName.y_lim_list: ColonCancerAllIndexSupMaterials.loss_y_lim,
            ParameterName.y_ticks_list: ColonCancerAllIndexSupMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: ColonCancerAllIndexSupMaterials.loss_y_tick_labels,
        }
        scale = subfigure_a_c_loss_scale
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: subfigure_a_c_loss_total_width,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = mid_comparison_figure.calculate_center(mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.03, 0.005)
        mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_figure.name: mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'comparison_of_index_between_high_and_low_colon_cancer_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(
                ColonCancerAllIndexSupMaterials, data_set_name=colon_cancer_traditional_data_set),
        }
        scale = 0.6
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        legend = figure_data_parameter_dict[ParameterName.legend]
        title = None
        flux_grid_comparison_figure = Elements.FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(
            flux_grid_comparison_figure, scale, flux_name_list, legend, title)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS5(Figure):
    figure_label = 'short_figure_s5'
    figure_title = 'Figure S5'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
        ]

        subfigure_a_height = 0.28
        subfigure_a_width = 0.45
        subfigure_b_width = 1 - subfigure_a_width
        subfigure_b_height = 0.28
        subfigure_c_height = subfigure_a_height
        subfigure_c_width = subfigure_a_width
        subfigure_d_width = 1 - subfigure_c_width
        subfigure_d_height = 0.28

        figure_layout_list = [
            (subfigure_a_height, [
                (subfigure_a_width, 'a'),
            ]),
            (subfigure_c_height, [
                (subfigure_c_width, 'c'),
            ]),
        ]

        subfigure_b_size = Vector(subfigure_b_width, subfigure_b_height)
        subfigure_b_center = Vector(subfigure_a_width + subfigure_b_width / 2, subfigure_b_height / 2)

        subfigure_d_size = Vector(subfigure_d_width, subfigure_d_height)
        subfigure_d_center = Vector(
            subfigure_c_width + subfigure_d_width / 2, subfigure_b_height + subfigure_d_height / 2)

        single_subfigure_layout_dict = {
            'b': (subfigure_b_center, subfigure_b_size),
            'd': (subfigure_d_center, subfigure_d_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
