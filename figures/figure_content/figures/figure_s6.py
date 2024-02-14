from ..common.config import ParameterName, DataName, Keywords, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import ColonCancerRawSupMaterials, \
    colon_cancer_comparison_dict_generator, ColonCancerRatioSupMaterials
from ..figure_elements.data_figure.figure_data_loader import raw_flux_value_dict_data
from .figure_5 import common_result_label_constructor


Subfigure = Elements.Subfigure

common_network_diagram_scale = 0.55
data_set_name = 'colon_cancer_cell_line'


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.colon_cancer_cell_line,
            ParameterName.result_label: common_result_label_constructor('high'),
            ParameterName.mid_name_list: ColonCancerRawSupMaterials.target_mid_name_list,
            ParameterName.name_dict: ColonCancerRawSupMaterials.mid_name_dict,
            ParameterName.color_dict: ColonCancerRawSupMaterials.mid_color_dict,
        }
        scale = 0.5
        mid_comparison_figure = Elements.MIDComparisonGridBarWithLegendDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.9,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = mid_comparison_figure.calculate_center(mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, -0.003)
        mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_figure.name: mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'loss_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.colon_cancer_cell_line,
            ParameterName.name_dict: ColonCancerRawSupMaterials.name_dict,
            ParameterName.color_dict: ColonCancerRawSupMaterials.color_dict,
            ParameterName.y_lim_list: ColonCancerRawSupMaterials.loss_y_lim,
            ParameterName.y_ticks_list: ColonCancerRawSupMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: ColonCancerRawSupMaterials.loss_y_tick_labels,
        }
        scale = 0.7
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.6,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = mid_comparison_figure.calculate_center(mid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0.01, -0.003)
        mid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            mid_comparison_figure.name: mid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'comparison_of_exchange_fluxes_between_renal_and_carcinoma'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # scale = MetabolicNetworkConfig.common_scale
        scale = common_network_diagram_scale
        high_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            DataName.colon_cancer_cell_line, common_result_label_constructor('high'))
        low_glucose_reaction_value_dict = raw_flux_value_dict_data.return_data(
            DataName.colon_cancer_cell_line, common_result_label_constructor('low'))
        # special_metabolite_and_flux_dict = MetabolicNetworkConfig.common_experimental_setting_dict
        condition_name_title_dict = ColonCancerRawSupMaterials.name_dict
        reaction_value_dict_for_different_conditions = {
            key: {
                **ColonCancerRawSupMaterials.data_flux_network_config_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency,
                ParameterName.reaction_raw_value_dict: reaction_value_dict
            } for key, reaction_value_dict in {
                Keywords.high_glucose: high_glucose_reaction_value_dict,
                Keywords.low_glucose: low_glucose_reaction_value_dict
            }.items()
        }

        metabolic_network_comparison = Elements.NetworkMFAResultComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.result_label: [Keywords.high_glucose, Keywords.low_glucose],
                ParameterName.name_dict: condition_name_title_dict,
                ParameterName.network_type: ParameterName.normal_network,
                ParameterName.metabolic_network_config_dict: reaction_value_dict_for_different_conditions
            }
        })

        center = metabolic_network_comparison.calculate_center(
            metabolic_network_comparison, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        metabolic_network_comparison.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, 0.01))

        subfigure_element_dict = {
            metabolic_network_comparison.name: metabolic_network_comparison}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


common_data_figure_scale = 0.7
common_data_width = 0.5
FluxComparisonScatterWithTitle = Elements.FluxComparisonScatterWithTitle


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'comparison_of_raw_fluxes_between_different_cancer_cell_line_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(ColonCancerRawSupMaterials),
            ParameterName.data_name: DataName.colon_cancer_cell_line_traditional_method,
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
    subfigure_title = 'comparison_of_index_between_different_cancer_cell_line_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **colon_cancer_comparison_dict_generator(ColonCancerRatioSupMaterials),
            ParameterName.data_name: DataName.colon_cancer_cell_line_traditional_method,
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


class FigureS6(Figure):
    figure_label = 'figure_s6'
    figure_title = 'Figure S6'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
        ]

        subfigure_a_b_height = 0.3
        subfigure_d_e_width = 0.4
        subfigure_e_height = 0.25
        subfigure_c_width = 0.6
        subfigure_c_d_height = 0.35
        subfigure_d_e_x_loc = subfigure_c_width + subfigure_d_e_width / 2

        figure_layout_list = [
            (subfigure_a_b_height, [
                (0.5, 'a'),
                (0.5, 'b'),
            ]),
            (subfigure_c_d_height, [
                (subfigure_c_width, 'c'),
                (subfigure_d_e_width, 'd'),
            ]),
        ]

        subfigure_e_size = Vector(subfigure_d_e_width, subfigure_e_height)
        subfigure_e_center_y_loc = subfigure_a_b_height + subfigure_c_d_height + -0.01 + subfigure_e_height / 2
        subfigure_e_center = Vector(subfigure_d_e_x_loc, subfigure_e_center_y_loc)

        single_subfigure_layout_dict = {
            'e': (subfigure_e_center, subfigure_e_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)
