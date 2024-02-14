from ..common.config import ParameterName, DataName, Keywords, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import KidneyCarcinomaRatioMaterials, \
    KidneyCarcinomaRawMaterials, kidney_carcinoma_comparison_dict_generator
from ..figure_elements.data_figure.figure_data_loader import raw_flux_value_dict_data

Subfigure = Elements.Subfigure

# common_data_figure_scale = FigureConfig.common_data_figure_scale
common_network_diagram_scale = 0.55
common_data_figure_scale = 0.7
renal_data_set_name = 'renal_carcinoma_invivo_infusion'
renal_kidney_name = 'kidney'
renal_carcinoma_name = 'carcinoma'
renal_brain_name = 'brain'
renal_kidney_carcinoma_comparison_display_index = 1
renal_brain_display_index = 1
lung_patient_name = 'K1031'
common_data_width = 0.5


def common_result_label_constructor(condition, data_type):
    if condition == 'renal':
        if data_type == renal_brain_name:
            return f'brain__{renal_brain_display_index}_average'
        else:
            return f'{data_type}__{renal_kidney_carcinoma_comparison_display_index}_average'
    elif condition == 'lung':
        return f'human__{lung_patient_name}_tumor_average'
    else:
        raise ValueError()


ExperimentDiagram = Elements.ExperimentDiagram


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'renal_carcinoma_experiment_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.45
        data_name = DataName.renal_carcinoma_invivo_infusion
        center = ExperimentDiagram.calculate_center(ExperimentDiagram, scale, data_name)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        experiment_diagram = ExperimentDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.01, -0.02),
            ParameterName.scale: scale,
            ParameterName.data_name: data_name,
        })

        subfigure_element_dict = {experiment_diagram.name: experiment_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


OptimizationDiagram = Elements.OptimizationDiagram


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'experimental_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.33
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, ParameterName.experimental)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.02, -0.01),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.experimental,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


ProtocolDiagram = Elements.ProtocolDiagram


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'protocol_diagram_experimental'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.5
        center = ProtocolDiagram.calculate_center(OptimizationDiagram, scale, ParameterName.experimental)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = ProtocolDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0, 0),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.experimental,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


MetabolicNetworkWithLegend = Elements.MetabolicNetworkWithLegend


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'complex_metabolic_network'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_network_diagram_scale

        legend = True
        subfigure_d_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.metabolic_network_config_dict:
                KidneyCarcinomaRawMaterials.diagram_network_config_dict,
        }
        metabolic_network_with_legend_obj = Elements.NormalAndExchangeTwinNetwork(**subfigure_d_config_dict)

        center = metabolic_network_with_legend_obj.calculate_center(
            metabolic_network_with_legend_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        metabolic_network_with_legend_obj.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0, -0.01))

        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


FluxComparisonScatterWithTitle = Elements.FluxComparisonScatterWithTitle


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'comparison_of_raw_fluxes_between_kidney_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(KidneyCarcinomaRawMaterials),
        }
        scale = common_data_figure_scale
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
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'comparison_of_exchange_fluxes_between_renal_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # scale = MetabolicNetworkConfig.common_scale
        scale = common_network_diagram_scale
        kidney_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_data_set_name, common_result_label_constructor('renal', renal_kidney_name))
        carcinoma_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_data_set_name, common_result_label_constructor('renal', renal_carcinoma_name))
        # special_metabolite_and_flux_dict = MetabolicNetworkConfig.common_experimental_setting_dict
        condition_name_title_dict = KidneyCarcinomaRawMaterials.name_dict
        reaction_value_dict_for_different_conditions = {
            key: {
                **KidneyCarcinomaRawMaterials.data_flux_network_config_dict,
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
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        quad_metabolic_network_comparison.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, 0.01))

        subfigure_element_dict = {
            quad_metabolic_network_comparison.name: quad_metabolic_network_comparison}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'comparison_of_index_between_kidney_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(KidneyCarcinomaRatioMaterials),
        }
        scale = common_data_figure_scale
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
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure4(Figure):
    figure_label = 'figure_4'
    figure_title = 'Figure 4'

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

        subfigure_d_height = 0.32
        subfigure_f_height = 0.3
        subfigure_d_f_width = 0.6
        figure_layout_list = [
            (0.2, [
                (0.24, 'a'),
                (0.28, 'b'),
                (0.48, 'c')
            ]),
            (subfigure_d_height, [
                (subfigure_d_f_width, 'd'),
                # (0.55, 'd')
            ]),
            # (0.3, [
            #     (0.5, 'e'),
            #     (0.5, 'f')
            # ]),
        ]

        subfigure_e_top = figure_layout_list[0][0]
        subfigure_e_g_width = 0.4
        subfigure_e_height = 0.35
        # subfigure_g_height = 0.3
        subfigure_g_height = subfigure_e_height * 0.75

        subfigure_e_size = Vector(subfigure_e_g_width, subfigure_e_height)
        subfigure_e_g_x_loc = subfigure_d_f_width + subfigure_e_g_width / 2
        subfigure_e_center_y_loc = subfigure_e_top + subfigure_e_size.y / 2
        subfigure_e_center = Vector(subfigure_e_g_x_loc, subfigure_e_center_y_loc)
        subfigure_g_size = Vector(subfigure_e_g_width, subfigure_g_height)
        subfigure_g_center_y_loc = subfigure_e_top + subfigure_e_size.y + -0.01 + subfigure_g_size.y / 2
        subfigure_g_center = Vector(subfigure_e_g_x_loc, subfigure_g_center_y_loc)

        subfigure_f_top = figure_layout_list[0][0] + figure_layout_list[1][0]
        subfigure_f_size = Vector(subfigure_d_f_width, subfigure_f_height)
        subfigure_f_center = Vector(subfigure_d_f_width / 2, subfigure_f_top + subfigure_f_size.y / 2)

        single_subfigure_layout_dict = {
            'e': (subfigure_e_center, subfigure_e_size),
            'f': (subfigure_f_center, subfigure_f_size),
            'g': (subfigure_g_center, subfigure_g_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
