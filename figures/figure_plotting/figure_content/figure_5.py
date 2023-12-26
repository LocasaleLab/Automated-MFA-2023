from ..common.config import ParameterName, Constant, DataName, Keywords
from ..common.classes import Vector
from ..figure_elements.elements import Elements
from .common_functions import calculate_subfigure_layout, \
    single_subfigure_layout
from ..common.common_figure_materials import FigureConfig, ColonCancerRawMaterials, \
    ColonCancerRatioMaterials, calculate_center_bottom_offset, colon_cancer_comparison_dict_generator
from ..figure_elements.data_figure.basic_data_figure.figure_data_loader import raw_flux_value_dict_data


Subfigure = Elements.Subfigure

common_data_figure_scale = 0.7
common_data_width = 0.5
common_network_diagram_scale = 0.55
data_set_name = 'colon_cancer_cell_line'
common_display_cancer_cell_line = 'HCT116-P3'


def common_result_label_constructor(condition):
    if condition == 'high':
        return f'{common_display_cancer_cell_line}__H_average'
    elif condition == 'low':
        return f'{common_display_cancer_cell_line}__L_average'
    else:
        raise ValueError()


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'colon_cancer_experiment_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        ExperimentDiagram = Elements.ExperimentDiagram
        scale = 0.5
        data_name = DataName.colon_cancer_cell_line
        center = ExperimentDiagram.calculate_center(ExperimentDiagram, scale, data_name)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        experiment_diagram = ExperimentDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.02, -0.01),
            ParameterName.scale: scale,
            ParameterName.data_name: data_name,
        })

        subfigure_element_dict = {experiment_diagram.name: experiment_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'metabolic_network_with_legend_for_colon_cancer'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_network_diagram_scale
        legend = True

        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.metabolic_network_config_dict: ColonCancerRawMaterials.diagram_network_config_dict,
        }

        metabolic_network_with_legend_obj = Elements.NormalAndExchangeTwinNetwork(**subfigure_c_config_dict)
        center = metabolic_network_with_legend_obj.calculate_center(
            metabolic_network_with_legend_obj, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        metabolic_network_with_legend_obj.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0, -0.01))

        subfigure_element_dict = {
            metabolic_network_with_legend_obj.name: metabolic_network_with_legend_obj}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'comparison_of_fluxes_between_high_and_low_glucose_condition'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # scale = MetabolicNetworkConfig.common_scale
        scale = common_network_diagram_scale
        high_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            data_set_name, common_result_label_constructor('high'))
        low_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            data_set_name, common_result_label_constructor('low'))

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
                ParameterName.condition: [Keywords.high_glucose, Keywords.low_glucose],
                ParameterName.name_dict: condition_name_title_dict,
                ParameterName.network_type: ParameterName.exchange_network,
                ParameterName.metabolic_network_config_dict: reaction_value_dict_for_different_conditions
            }
        })

        center = quad_metabolic_network_comparison.calculate_center(
            quad_metabolic_network_comparison, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        quad_metabolic_network_comparison.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, 0))

        subfigure_element_dict = {
            quad_metabolic_network_comparison.name: quad_metabolic_network_comparison}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


FluxComparisonScatterWithTitle = Elements.FluxComparisonScatterWithTitle


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'comparison_of_raw_fluxes_between_different_cancer_cell_line'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(ColonCancerRawMaterials)
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


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'comparison_of_index_between_different_cancer_cell_line'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(ColonCancerRatioMaterials)
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


class Figure5(Elements.Figure):
    figure_label = 'figure_5'
    figure_title = 'Figure 5'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            # SubfigureF,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        subfigure_c_width = 0.6
        figure_layout_list = [
            (0.25, [
                (0.4, 'a'),
                (0.6, 'b')
            ]),
            (0.4, [
                (subfigure_c_width, 'c'),
                # (0.6, 'd')
            ]),
            # (0.3, [
            #     (0.5, 'd'),
            #     # (0.5, 'f')
            # ]),
        ]
        subfigure_d_top = figure_layout_list[0][0]
        subfigure_d_e_width = 0.4
        subfigure_d_height = 0.35
        subfigure_e_height = subfigure_d_height * 0.75
        subfigure_d_size = Vector(subfigure_d_e_width, subfigure_d_height)
        subfigure_e_size = Vector(subfigure_d_e_width, subfigure_e_height)
        subfigure_d_e_x_loc = subfigure_c_width + subfigure_d_e_width / 2
        subfigure_d_center_y_loc = subfigure_d_top + subfigure_d_size.y / 2
        subfigure_d_center = Vector(subfigure_d_e_x_loc, subfigure_d_center_y_loc)
        subfigure_e_center_y_loc = subfigure_d_top + subfigure_d_size.y + -0.01 + subfigure_e_size.y / 2
        subfigure_e_center = Vector(subfigure_d_e_x_loc, subfigure_e_center_y_loc)

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_obj_list.extend([
            single_subfigure_layout(
                subfigure_d_center, subfigure_d_size, SubfigureD, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
            single_subfigure_layout(
                subfigure_e_center, subfigure_e_size, SubfigureE, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
        ])
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

