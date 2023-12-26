from ..common.config import ParameterName, Constant, DataName, np
from ..common.classes import Vector
from ..figure_elements.elements import Elements

from .common_functions import calculate_subfigure_layout
from ..common.common_figure_materials import FigureConfig, CommonFigureString, calculate_center_bottom_offset, \
    CommonFigureMaterials
from .figure_3 import obtain_and_process_data_sensitivity_data, evenly_distributed_all_case_list, \
    evenly_distributed_labels_list, evenly_distributed_few_data_list, evenly_distributed_few_data_labels_list, \
    remove_pathway_all_case_list, remove_pathway_labels_list, \
    compartmentalization_all_case_list, compartmentalization_labels_list


Subfigure = Elements.Subfigure
common_data_figure_scale = 0.46
# common_data_figure_scale = 0.2
common_data_width = 1
subfigure_a_b_offset = Vector(0.01, -0.01)
subfigure_c_d_offset = Vector(0, -0.01)
subfigure_c_d_scale = 0.4


all_net_flux_comparison_scale = 0.35
OptimizedAllFluxComparisonBarDataFigure = Elements.OptimizedAllFluxComparisonBarDataFigure
common_optimized_size = 20000
common_selection_size = 100


def evenly_distributed_mid_data_obj_generator(subfigure_bottom_left, subfigure_size, selected_solutions):
    figure_data_parameter_dict = {
        ParameterName.figure_title: CommonFigureString.smaller_data_size,
        ParameterName.data_name: DataName.data_sensitivity,
        ParameterName.optimized_size: common_optimized_size,
        ParameterName.selection_size: common_selection_size,
        ParameterName.subplot_name_list: evenly_distributed_labels_list,
        ParameterName.text_axis_loc_pair: Vector(0.4, 0.92),
        ParameterName.selected: selected_solutions,
    }
    obtain_and_process_data_sensitivity_data(
        figure_data_parameter_dict, evenly_distributed_all_case_list, raw_flux_vector=True,
        selected_solutions=selected_solutions)
    scale = all_net_flux_comparison_scale
    flux_diff_vector_figure = OptimizedAllFluxComparisonBarDataFigure(**{
        ParameterName.bottom_left_offset: subfigure_bottom_left,
        ParameterName.scale: scale,
        ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
    })
    center = flux_diff_vector_figure.calculate_center(
        scale, **figure_data_parameter_dict)
    center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
    flux_diff_vector_figure.move_and_scale(
        bottom_left_offset=center_bottom_offset)
    return flux_diff_vector_figure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'flux_diff_vector_evenly_distributed_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = evenly_distributed_mid_data_obj_generator(
            subfigure_bottom_left, subfigure_size, True)

        subfigure_element_dict = {
            flux_diff_vector_figure.name:
                flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'flux_diff_vector_evenly_distributed_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = evenly_distributed_mid_data_obj_generator(
            subfigure_bottom_left, subfigure_size, False)

        subfigure_element_dict = {
            flux_diff_vector_figure.name: flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


def remove_pathway_mid_data_obj_generator(subfigure_bottom_left, subfigure_size, selected_solutions):
    figure_data_parameter_dict = {
        ParameterName.figure_title: CommonFigureString.data_without_pathway,
        ParameterName.data_name: DataName.data_sensitivity,
        ParameterName.optimized_size: common_optimized_size,
        ParameterName.selection_size: common_selection_size,
        ParameterName.subplot_name_list: remove_pathway_labels_list,
        ParameterName.text_axis_loc_pair: Vector(0.35, 0.92),
        ParameterName.selected: selected_solutions,
    }
    obtain_and_process_data_sensitivity_data(
        figure_data_parameter_dict, remove_pathway_all_case_list, raw_flux_vector=True,
        selected_solutions=selected_solutions)
    scale = all_net_flux_comparison_scale
    flux_diff_vector_figure = OptimizedAllFluxComparisonBarDataFigure(**{
        ParameterName.bottom_left_offset: subfigure_bottom_left,
        ParameterName.scale: scale,
        ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
    })
    center = flux_diff_vector_figure.calculate_center(
        scale, **figure_data_parameter_dict)
    center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
    flux_diff_vector_figure.move_and_scale(
        bottom_left_offset=center_bottom_offset)
    return flux_diff_vector_figure


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'flux_diff_vector_remove_pathway_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = remove_pathway_mid_data_obj_generator(
            subfigure_bottom_left, subfigure_size, True)
        subfigure_element_dict = {flux_diff_vector_figure.name: flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'flux_diff_vector_remove_pathway_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = remove_pathway_mid_data_obj_generator(
            subfigure_bottom_left, subfigure_size, False)
        subfigure_element_dict = {flux_diff_vector_figure.name: flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


def compartmentalization_data_obj_generator(subfigure_bottom_left, subfigure_size, selected_solutions):
    figure_data_parameter_dict = {
        ParameterName.figure_title: CommonFigureString.compartmental_data,
        ParameterName.data_name: DataName.data_sensitivity,
        ParameterName.optimized_size: common_optimized_size,
        ParameterName.selection_size: common_selection_size,
        ParameterName.subplot_name_list: compartmentalization_labels_list,
        ParameterName.selected: selected_solutions,
    }
    obtain_and_process_data_sensitivity_data(
        figure_data_parameter_dict, compartmentalization_all_case_list, raw_flux_vector=True,
        selected_solutions=selected_solutions)
    scale = all_net_flux_comparison_scale
    flux_diff_vector_figure = OptimizedAllFluxComparisonBarDataFigure(**{
        ParameterName.bottom_left_offset: subfigure_bottom_left,
        ParameterName.scale: scale,
        ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
    })
    center = flux_diff_vector_figure.calculate_center(
        scale, **figure_data_parameter_dict)
    center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
    flux_diff_vector_figure.move_and_scale(
        bottom_left_offset=center_bottom_offset)
    return flux_diff_vector_figure


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'flux_diff_vector_compartmentalization_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = compartmentalization_data_obj_generator(
            subfigure_bottom_left, subfigure_size, True)
        subfigure_element_dict = {flux_diff_vector_figure.name: flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'flux_diff_vector_compartmentalization_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        flux_diff_vector_figure = compartmentalization_data_obj_generator(
            subfigure_bottom_left, subfigure_size, False)
        subfigure_element_dict = {flux_diff_vector_figure.name: flux_diff_vector_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'flux_relative_error_evenly_distributed_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.smaller_data_size,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.subplot_name_list: evenly_distributed_few_data_labels_list,
            ParameterName.text_axis_loc_pair: Vector(0.4, 0.92)
        }
        obtain_and_process_data_sensitivity_data(
            figure_data_parameter_dict, evenly_distributed_few_data_list, flux_relative_distance=True)
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(
            scale, **figure_data_parameter_dict)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS3(Elements.Figure):
    figure_label = 'figure_s3'
    figure_title = 'Figure S3'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            SubfigureF,
            SubfigureG,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        figure_layout_list = [
            (0.325, [
                (0.5, 'a'),
                (0.5, 'b')
            ]),
            (0.275, [
                (0.5, 'c'),
                (0.5, 'd')
            ]),
            (0.225, [
                (0.5, 'e'),
                (0.5, 'f')
            ]),
            (0.16, [
                (0.5, 'g'),
            ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

