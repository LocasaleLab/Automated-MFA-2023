from ..common.config import ParameterName, Constant, Keywords, DataName
from ..common.common_figure_materials import ColonCancerRawMaterials, FigureConfig
from ..figure_elements.element_dict import ElementName, element_dict
from ..common.color import ColorConfig
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout, \
    Vector, single_subfigure_layout
from ..figure_elements.data_figure.basic_data_figure.figure_data_loader import raw_flux_value_dict_data
from .figure_5 import common_result_label_constructor


Subfigure = element_dict[ElementName.Subfigure]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
MetabolicNetworkWithLegend = element_dict[ElementName.MetabolicNetworkWithLegend]
FluxComparisonScatterWithTitle = element_dict[ElementName.FluxComparisonScatterWithTitle]
ExperimentDiagram = element_dict[ElementName.ExperimentDiagram]

common_network_diagram_scale = 0.55
data_set_name = 'colon_cancer_cell_line'

ExchangeNetworkMFAResultComparison = element_dict[ElementName.NetworkMFAResultComparison]
MIDComparisonGridBarWithLegendDataFigure = element_dict[ElementName.MIDComparisonGridBarWithLegendDataFigure]
ExperimentalOptimizationLossComparison = element_dict[ElementName.ExperimentalOptimizationLossComparison]


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.colon_cancer_cell_line,
            ParameterName.result_label: common_result_label_constructor('high'),
            ParameterName.mid_name_list: ColonCancerRawMaterials.target_mid_name_list,
            ParameterName.name_dict: ColonCancerRawMaterials.mid_name_dict,
            ParameterName.color_dict: ColonCancerRawMaterials.mid_color_dict,
        }
        scale = 0.5
        mid_comparison_figure = MIDComparisonGridBarWithLegendDataFigure(**{
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
            ParameterName.name_dict: ColonCancerRawMaterials.name_dict,
            ParameterName.color_dict: ColonCancerRawMaterials.color_dict,
            ParameterName.y_lim_list: ColonCancerRawMaterials.loss_y_lim,
            ParameterName.y_ticks_list: ColonCancerRawMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: ColonCancerRawMaterials.loss_y_tick_labels,
        }
        scale = 0.7
        mid_comparison_figure = ExperimentalOptimizationLossComparison(**{
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

        metabolic_network_comparison = ExchangeNetworkMFAResultComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.condition: [Keywords.high_glucose, Keywords.low_glucose],
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


class FigureS6(element_dict[ElementName.Figure]):
    figure_label = 'figure_s6'
    figure_title = 'Figure S6'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        figure_layout_list = [
            (0.4, [
                (0.5, 'a'),
                (0.5, 'b'),
            ]),
            (0.4, [
                (1, 'c'),
            ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
