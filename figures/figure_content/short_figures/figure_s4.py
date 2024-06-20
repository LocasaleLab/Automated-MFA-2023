from ..common.config import ParameterName, DataName, Keywords, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import kidney_carcinoma_comparison_dict_generator, \
    KidneyCarcinomaAllIndexMaterials, KidneyCarcinomaAllIndexSupMaterials
from ..figure_elements.data_figure.figure_data_loader import raw_flux_value_dict_data
from .short_figure_config import (
    common_result_label_constructor, renal_kidney_name, renal_carcinoma_name, renal_carcinoma_data_set,
    renal_carcinoma_traditional_data_set, common_data_width)

Subfigure = Elements.Subfigure


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'renal_carcinoma_experiment_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.4
        ExperimentDiagram = Elements.ExperimentDiagram
        data_name = DataName.renal_carcinoma_invivo_infusion
        center = ExperimentDiagram.calculate_center(ExperimentDiagram, scale, data_name)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        experiment_diagram = ExperimentDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.03, -0.02),
            ParameterName.scale: scale,
            ParameterName.data_name: data_name,
        })

        subfigure_element_dict = {experiment_diagram.name: experiment_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'renal_carcinoma_loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: renal_carcinoma_data_set,
            ParameterName.name_dict: KidneyCarcinomaAllIndexMaterials.name_dict,
            ParameterName.color_dict: KidneyCarcinomaAllIndexMaterials.color_dict,
            ParameterName.y_lim_list: KidneyCarcinomaAllIndexMaterials.loss_y_lim,
            ParameterName.y_ticks_list: KidneyCarcinomaAllIndexMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: KidneyCarcinomaAllIndexMaterials.loss_y_tick_labels,
        }
        scale = 0.48
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.4,
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


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'renal_carcinoma_mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: renal_carcinoma_data_set,
            ParameterName.result_label: common_result_label_constructor('renal', renal_kidney_name),
            ParameterName.mid_name_list: KidneyCarcinomaAllIndexMaterials.target_mid_name_list,
            ParameterName.name_dict: KidneyCarcinomaAllIndexMaterials.mid_name_dict,
            ParameterName.color_dict: KidneyCarcinomaAllIndexMaterials.mid_color_dict,
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


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'comparison_of_exchange_fluxes_between_renal_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # scale = MetabolicNetworkConfig.common_scale
        scale = 0.5
        kidney_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_carcinoma_data_set, common_result_label_constructor('renal', renal_kidney_name))
        carcinoma_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_carcinoma_data_set, common_result_label_constructor('renal', renal_carcinoma_name))
        # special_metabolite_and_flux_dict = MetabolicNetworkConfig.common_experimental_setting_dict
        condition_name_title_dict = KidneyCarcinomaAllIndexMaterials.name_dict
        reaction_value_dict_for_different_conditions = {
            key: {
                **KidneyCarcinomaAllIndexMaterials.data_flux_network_config_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency,
                ParameterName.reaction_raw_value_dict: reaction_value_dict
            } for key, reaction_value_dict in {
                Keywords.kidney: kidney_reaction_value_dict,
                Keywords.carcinoma: carcinoma_reaction_value_dict
            }.items()
        }

        quad_metabolic_network_comparison = Elements.NetworkMFAResultComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.result_label: [Keywords.kidney, Keywords.carcinoma],
                ParameterName.name_dict: condition_name_title_dict,
                ParameterName.network_type: ParameterName.exchange_network,
                ParameterName.metabolic_network_config_dict: reaction_value_dict_for_different_conditions
            }
        })

        center = quad_metabolic_network_comparison.calculate_center(
            quad_metabolic_network_comparison, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.02, -0)
        quad_metabolic_network_comparison.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            quad_metabolic_network_comparison.name: quad_metabolic_network_comparison}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


FluxComparisonScatterWithTitle = Elements.FluxComparisonScatterWithTitle


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'comparison_of_index_between_kidney_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(
                KidneyCarcinomaAllIndexMaterials, data_set_name=renal_carcinoma_data_set),
        }
        scale = 0.63
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        legend = figure_data_parameter_dict[ParameterName.legend]
        title = None
        flux_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(
            flux_grid_comparison_figure, scale, flux_name_list, legend, title)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(-0.01, -0.01)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'renal_carcinoma_with_traditional_method_loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: renal_carcinoma_traditional_data_set,
            ParameterName.name_dict: KidneyCarcinomaAllIndexMaterials.name_dict,
            ParameterName.color_dict: KidneyCarcinomaAllIndexMaterials.color_dict,
            ParameterName.y_lim_list: KidneyCarcinomaAllIndexMaterials.loss_y_lim,
            ParameterName.y_ticks_list: KidneyCarcinomaAllIndexMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: KidneyCarcinomaAllIndexMaterials.loss_y_tick_labels,
        }
        scale = 0.48
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.4,
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


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'comparison_of_index_between_kidney_and_carcinoma_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(
                KidneyCarcinomaAllIndexSupMaterials, data_set_name=renal_carcinoma_traditional_data_set),
        }
        scale = 0.63
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        legend = figure_data_parameter_dict[ParameterName.legend]
        title = None
        flux_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(
            flux_grid_comparison_figure, scale, flux_name_list, legend, title)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, -0.01)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS4(Figure):
    figure_label = 'short_figure_s4'
    figure_title = 'Figure S4'

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

        subfigure_a_height = 0.2
        subfigure_a_width = 0.4
        subfigure_b_height = 0.2
        subfigure_d_height = 0.23
        subfigure_f_height = 0.25
        subfigure_d_width = 0.52
        subfigure_f_width = 0.45
        figure_layout_list = [
            (subfigure_a_height, [
                (subfigure_a_width, 'a'),
            ]),
            (subfigure_b_height, [
                (subfigure_a_width, 'b'),
            ]),
            (subfigure_d_height, [
                (subfigure_d_width, 'd'),
            ]),
            (subfigure_f_height, [
                (subfigure_f_width, 'f'),
            ]),
        ]

        subfigure_c_width = 1 - subfigure_a_width
        subfigure_c_height = 0.32
        subfigure_c_size = Vector(subfigure_c_width, subfigure_c_height)
        subfigure_c_center = Vector(subfigure_a_width + subfigure_c_width / 2, subfigure_c_height / 2)

        subfigure_e_width = 1 - subfigure_d_width
        subfigure_e_height = 0.3
        subfigure_e_size = Vector(subfigure_e_width, subfigure_e_height)
        subfigure_e_center = Vector(
            subfigure_d_width + subfigure_e_width / 2, subfigure_c_height + subfigure_e_height / 2)

        subfigure_g_width = 1 - subfigure_f_width
        subfigure_g_height = subfigure_e_height - 0.05
        subfigure_g_size = Vector(subfigure_g_width, subfigure_g_height)
        subfigure_g_left = subfigure_f_width
        subfigure_g_top = subfigure_c_height + subfigure_e_height
        subfigure_g_center = Vector(
            subfigure_g_left + subfigure_g_width / 2,
            subfigure_g_top + subfigure_g_height / 2)

        single_subfigure_layout_dict = {
            'c': (subfigure_c_center, subfigure_c_size),
            'e': (subfigure_e_center, subfigure_e_size),
            'g': (subfigure_g_center, subfigure_g_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
