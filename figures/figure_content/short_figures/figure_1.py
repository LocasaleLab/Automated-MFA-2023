from ..common.config import DataName, ParameterName, Figure, Vector, calculate_center_bottom_offset, Keywords
from ..common.common_figure_materials import CommonFigureString, ColonCancerRawMaterials, \
    colon_cancer_comparison_dict_generator, ColonCancerAllIndexMaterials
from ..common.elements import Elements
from ..figure_elements.data_figure.figure_data_loader import raw_flux_value_dict_data
from .short_figure_config import (
    common_result_label_constructor, raw_model_raw_data_name,
    raw_data_optimized_size, raw_data_selection_size, raw_data_traditional_optimized_size,
    colon_cancer_data_set, hct_116_data_name, raw_model_raw_data_with_glns_m)


Subfigure = Elements.Subfigure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'data_acquisition_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        DataAcquisitionDiagram = Elements.DataAcquisitionDiagram
        scale = 0.33
        center = DataAcquisitionDiagram.calculate_center(DataAcquisitionDiagram, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = DataAcquisitionDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0, -0.01),
            ParameterName.scale: scale
        })
        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'optimization_process_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        OptimizationDiagram = Elements.OptimizationDiagram
        scale = 0.32
        mode = ParameterName.experimental
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, mode)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        optimization_process_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(-0.01, -0.01),
            ParameterName.scale: scale,
            ParameterName.mode: mode,
        })
        subfigure_element_dict = {
            optimization_process_diagram.name: optimization_process_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'metabolic_network_with_legend_for_colon_cancer'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.58
        legend = True

        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.metabolic_network_config_dict: ColonCancerRawMaterials.diagram_network_config_dict,
        }

        metabolic_network_with_legend_obj = Elements.NormalAndExchangeTwinNetwork(**subfigure_c_config_dict)
        center = metabolic_network_with_legend_obj.calculate_center(
            metabolic_network_with_legend_obj, scale, legend=legend)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.005, 0.01)
        metabolic_network_with_legend_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'distance_between_global_and_local_optima'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.52

        running_time_and_loss_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: hct_116_data_name,
                ParameterName.total_width: 0.6,
                ParameterName.horiz_or_vertical: ParameterName.vertical,
                ParameterName.common_y_lim: (0, 21),
                ParameterName.common_y_lim_2: (0, 3600),
                ParameterName.y_tick_interval_2: 1000
            }
        }
        random_optimized_loss_distance_obj = Elements.RandomOptimizedLossDistanceWithDiagramComparison(
            **running_time_and_loss_config_dict)

        center = random_optimized_loss_distance_obj.calculate_center(random_optimized_loss_distance_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(-0.02, -0.017)
        random_optimized_loss_distance_obj.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            random_optimized_loss_distance_obj.name: random_optimized_loss_distance_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


ProtocolDiagram = Elements.ProtocolDiagram


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'protocol_diagram_simulated'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.45
        center = ProtocolDiagram.calculate_center(ProtocolDiagram, scale, ParameterName.simulated_without_reoptimization)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = ProtocolDiagram(**{
            ParameterName.bottom_left_offset: (
                subfigure_bottom_left + center_bottom_offset + Vector(0.02, -0.02)),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.simulated_without_reoptimization,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'flux_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.difference_from_known_flux,
            ParameterName.data_name: raw_model_raw_data_name,
            ParameterName.with_re_optimization: False,
            ParameterName.with_traditional_method: True,
            ParameterName.with_glns_m: raw_model_raw_data_with_glns_m,
            ParameterName.optimized_size: raw_data_optimized_size,
            ParameterName.selection_size: raw_data_selection_size,
            ParameterName.traditional_optimized_size: raw_data_traditional_optimized_size,
        }
        scale = 0.48
        raw_model_all_data_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(
            scale, **figure_data_parameter_dict)
        center_bottom_offset = (
            calculate_center_bottom_offset(center, subfigure_size) +
            Vector(-0.01, -0.01))
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'colon_cancer_experiment_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        ExperimentDiagram = Elements.ExperimentDiagram
        scale = 0.35
        data_name = DataName.colon_cancer_cell_line
        center = ExperimentDiagram.calculate_center(ExperimentDiagram, scale, data_name)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        experiment_diagram = ExperimentDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.04, -0.005),
            ParameterName.scale: scale,
            ParameterName.data_name: data_name,
        })

        subfigure_element_dict = {experiment_diagram.name: experiment_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'comparison_of_fluxes_between_high_and_low_glucose_condition'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.52
        high_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            colon_cancer_data_set, common_result_label_constructor('colon_cancer', 'high'))
        low_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            colon_cancer_data_set, common_result_label_constructor('colon_cancer', 'low'))

        condition_name_title_dict = ColonCancerRawMaterials.name_dict
        reaction_value_dict_for_different_conditions = {
            key: {
                **ColonCancerRawMaterials.data_flux_network_config_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency,
                ParameterName.reaction_raw_value_dict: reaction_value_dict
            } for key, reaction_value_dict in {
                Keywords.high_glucose: high_glucose_reaction_value_dict,
                Keywords.low_glucose: low_glucose_reaction_value_dict
            }.items()
        }

        quad_metabolic_network_comparison = Elements.NetworkMFAResultComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.result_label: [Keywords.high_glucose, Keywords.low_glucose],
                ParameterName.name_dict: condition_name_title_dict,
                ParameterName.network_type: ParameterName.exchange_network,
                ParameterName.metabolic_network_config_dict: reaction_value_dict_for_different_conditions
            }
        })

        center = quad_metabolic_network_comparison.calculate_center(
            quad_metabolic_network_comparison, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        quad_metabolic_network_comparison.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.02, -0.005))

        subfigure_element_dict = {
            quad_metabolic_network_comparison.name: quad_metabolic_network_comparison}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureI(Subfigure):
    subfigure_label = 'i'
    subfigure_title = 'comparison_of_index_between_different_cancer_cell_line'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(ColonCancerAllIndexMaterials, colon_cancer_data_set),
        }
        scale = 0.65
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        legend = figure_data_parameter_dict[ParameterName.legend]
        title = None
        flux_grid_comparison_figure = Elements.FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: 0.5,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(
            flux_grid_comparison_figure, scale, flux_name_list, legend, title)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(-0.01, -0)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure1(Figure):
    figure_label = 'short_figure_1'
    figure_title = 'Figure 1'

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
            SubfigureI,
        ]

        subfigure_a_width = 0.55
        subfigure_a_height = 0.15
        subfigure_b_width = 1 - subfigure_a_width
        subfigure_b_height = 0.16
        subfigure_c_width = 0.6
        subfigure_c_height = 0.29
        subfigure_d_width = 1 - subfigure_c_width
        subfigure_d_height = 0.26

        subfigure_e_width = 0.4
        subfigure_f_width = 1 - subfigure_e_width
        subfigure_g_width = subfigure_e_width
        subfigure_h_width = 0.55
        subfigure_i_width = 1 - subfigure_h_width

        subfigure_e_height = 0.2
        subfigure_f_height = 0.32
        subfigure_g_height = 0.12
        subfigure_h_height = 0.2
        subfigure_i_height = 0.23

        subfigure_b_center = Vector(
            subfigure_a_width + subfigure_b_width / 2, subfigure_b_height / 2)
        subfigure_b_size = Vector(subfigure_b_width, subfigure_b_height)

        subfigure_d_top = subfigure_b_height
        subfigure_d_center = Vector(
            subfigure_c_width + subfigure_d_width / 2, subfigure_d_top + subfigure_d_height / 2)
        subfigure_d_size = Vector(subfigure_d_width, subfigure_d_height)

        subfigure_f_top = subfigure_d_top + subfigure_d_height + 0.01
        subfigure_f_center = Vector(
            subfigure_e_width + subfigure_f_width / 2, subfigure_f_top + subfigure_f_height / 2)
        subfigure_f_size = Vector(subfigure_f_width, subfigure_f_height)

        subfigure_i_top = subfigure_f_top + subfigure_f_height
        subfigure_i_center = Vector(
            subfigure_h_width + subfigure_i_width / 2, subfigure_i_top + subfigure_i_height / 2)
        subfigure_i_size = Vector(subfigure_i_width, subfigure_i_height)

        figure_layout_list = [
            (subfigure_a_height, [(subfigure_a_width, 'a')]),
            (subfigure_c_height, [(subfigure_c_width, 'c')]),
            (subfigure_e_height, [
                (subfigure_e_width, 'e'),
            ]),
            (subfigure_g_height, [
                (subfigure_g_width, 'g'),
            ]),
            (subfigure_h_height, [
                (subfigure_h_width, 'h'),
            ]),
        ]

        single_subfigure_layout_dict = {
            'b': (subfigure_b_center, subfigure_b_size),
            'd': (subfigure_d_center, subfigure_d_size),
            'f': (subfigure_f_center, subfigure_f_size),
            'i': (subfigure_i_center, subfigure_i_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
