from ..common.config import ParameterName, Constant, DataName, Keywords
from ..common.classes import Vector
from ..common.color import ColorConfig
from ..figure_elements.element_dict import ElementName, element_dict
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout, \
    single_subfigure_layout
from ..common.common_figure_materials import MetabolicNetworkConfig, FigureConfig, \
    CommonFigureMaterials, ColonCancerRawMaterials, ColonCancerRatioMaterials, CommonFigureString
from ..figure_elements.data_figure.basic_data_figure.figure_data_loader import raw_flux_value_dict_data


Subfigure = element_dict[ElementName.Subfigure]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
MetabolicNetworkWithLegend = element_dict[ElementName.MetabolicNetworkWithLegend]
FluxComparisonScatterWithTitle = element_dict[ElementName.FluxComparisonScatterWithTitle]
FluxComparisonViolinBoxWithTitleLegend = element_dict[ElementName.FluxComparisonViolinBoxWithTitleLegend]
QuadMetabolicNetworkComparison = element_dict[ElementName.QuadMetabolicNetworkComparison]
ExperimentDiagram = element_dict[ElementName.ExperimentDiagram]
MetabolicNetworkWithExchangeFlux = element_dict[ElementName.NormalAndExchangeTwinNetwork]
MetabolicNetworkMFAResultComparison = element_dict[ElementName.NormalAndExchangeNetworkMFAResultComparison]
NetworkMFAResultComparison = element_dict[ElementName.NetworkMFAResultComparison]

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
        # scale = MetabolicNetworkConfig.common_scale
        scale = common_network_diagram_scale
        legend = True
        # center = MetabolicNetworkWithLegend.calculate_center(MetabolicNetworkWithLegend, scale, legend=legend)
        # bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0)

        subfigure_c_config_dict = {
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.legend: legend,
            ParameterName.metabolic_network_config_dict: ColonCancerRawMaterials.diagram_network_config_dict,
            # ParameterName.metabolic_network_legend_config_dict: {},
        }

        metabolic_network_with_legend_obj = MetabolicNetworkWithExchangeFlux(**subfigure_c_config_dict)
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

        quad_metabolic_network_comparison = NetworkMFAResultComparison(**{
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


def colon_cancer_comparison_dict_generator(config_class):
    common_kidney_carcinoma_comparison_dict = {
        # ParameterName.figure_title: Title.comparison_between_normal_flank_tumor,
        ParameterName.data_name: DataName.colon_cancer_cell_line,
        ParameterName.comparison_name: 'high_low_glucose',
        ParameterName.mean: False,
        ParameterName.flux_name_list: config_class.flux_name_location_list,
        ParameterName.display_flux_name_dict: config_class.display_flux_name_dict,
        ParameterName.y_lim_list: config_class.y_lim_list,
        ParameterName.y_ticks_list: config_class.y_ticks_list,
        ParameterName.display_group_name_dict: config_class.cell_line_display_name_dict,
        ParameterName.name_dict: config_class.name_dict,
        ParameterName.color_dict: config_class.color_dict,
        ParameterName.legend: True,
        ParameterName.common_x_label: CommonFigureString.cell_line,
        ParameterName.compare_one_by_one: True,
        ParameterName.scatter_line: False,
        ParameterName.error_bar: True,
        ParameterName.figure_config_dict: {
            ParameterName.x_tick_label_format_dict: {
                ParameterName.font_size: 5
            },
            ParameterName.y_label_format_dict: {
                ParameterName.axis_label_distance: 0.035
            }
        }
    }
    return common_kidney_carcinoma_comparison_dict


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
            # ParameterName.figure_title: Title.comparison_between_normal_flank_tumor,
            # ParameterName.height_to_width_ratio: 0.7,
            # ParameterName.data_name: DataName.colon_cancer_cell_line,
            # ParameterName.comparison_name: 'high_low_glucose',
            # ParameterName.mean: False,
            # ParameterName.flux_name_list: ColonCancerRatioMaterials.flux_name_location_list,
            # ParameterName.display_flux_name_dict: ColonCancerRatioMaterials.display_flux_name_dict,
            # ParameterName.y_lim_list: ColonCancerRatioMaterials.y_lim_list,
            # ParameterName.y_ticks_list: ColonCancerRatioMaterials.y_ticks_list,
            # ParameterName.display_group_name_dict: ColonCancerRatioMaterials.cell_line_display_name_dict,
            # ParameterName.name_dict: ColonCancerRatioMaterials.name_dict,
            # ParameterName.color_dict: ColonCancerRatioMaterials.color_dict,
            # ParameterName.legend: True,
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


class Figure5(element_dict[ElementName.Figure]):
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
