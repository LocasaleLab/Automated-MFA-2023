from ..common.config import ParameterName, Constant, Keywords, DataName
from ..common.common_figure_materials import KidneyCarcinomaRawSupMaterials, FigureConfig, \
    calculate_center_bottom_offset, kidney_carcinoma_comparison_dict_generator, KidneyCarcinomaRatioSupMaterials
from ..figure_elements.elements import Elements
from .common_functions import calculate_subfigure_layout, \
    Vector, single_subfigure_layout
from ..figure_elements.data_figure.basic_data_figure.figure_data_loader import raw_flux_value_dict_data

Subfigure = Elements.Subfigure

common_network_diagram_scale = 0.55
renal_data_set_name = 'renal_carcinoma_invivo_infusion'
renal_kidney_name = 'kidney'
renal_carcinoma_name = 'carcinoma'
renal_kidney_carcinoma_comparison_display_index = 1


def common_result_label_constructor(data_type):
    return f'{data_type}__{renal_kidney_carcinoma_comparison_display_index}_average'


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'mid_comparison'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.data_name: DataName.renal_carcinoma_invivo_infusion,
            ParameterName.result_label: common_result_label_constructor(renal_kidney_name),
            ParameterName.mid_name_list: KidneyCarcinomaRawSupMaterials.target_mid_name_list,
            ParameterName.name_dict: KidneyCarcinomaRawSupMaterials.mid_name_dict,
            ParameterName.color_dict: KidneyCarcinomaRawSupMaterials.mid_color_dict,
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
            ParameterName.data_name: DataName.renal_carcinoma_invivo_infusion,
            # ParameterName.result_label: common_result_label_constructor(renal_kidney_name),
            ParameterName.name_dict: KidneyCarcinomaRawSupMaterials.name_dict,
            ParameterName.color_dict: KidneyCarcinomaRawSupMaterials.color_dict,
            ParameterName.y_lim_list: KidneyCarcinomaRawSupMaterials.loss_y_lim,
            ParameterName.y_ticks_list: KidneyCarcinomaRawSupMaterials.loss_y_ticks,
            ParameterName.y_tick_labels_list: KidneyCarcinomaRawSupMaterials.loss_y_tick_labels,
        }
        scale = 0.7
        mid_comparison_figure = Elements.ExperimentalOptimizationLossComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.total_width: 0.4,
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
        kidney_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_data_set_name, common_result_label_constructor(renal_kidney_name))
        carcinoma_reaction_value_dict = raw_flux_value_dict_data.return_data(
            renal_data_set_name, common_result_label_constructor(renal_carcinoma_name))
        # special_metabolite_and_flux_dict = MetabolicNetworkConfig.common_experimental_setting_dict
        condition_name_title_dict = KidneyCarcinomaRawSupMaterials.name_dict
        reaction_value_dict_for_different_conditions = {
            key: {
                **KidneyCarcinomaRawSupMaterials.data_flux_network_config_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency,
                ParameterName.reaction_raw_value_dict: reaction_value_dict
            } for key, reaction_value_dict in {
                Keywords.kidney: kidney_reaction_value_dict,
                Keywords.carcinoma: carcinoma_reaction_value_dict
            }.items()
        }

        metabolic_network_comparison = Elements.NetworkMFAResultComparison(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.condition: [Keywords.kidney, Keywords.carcinoma],
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
    subfigure_title = 'comparison_of_raw_fluxes_between_kidney_and_carcinoma_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(KidneyCarcinomaRawSupMaterials),
            ParameterName.data_name: DataName.renal_carcinoma_invivo_infusion_traditional_method
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
    subfigure_title = 'comparison_of_index_between_kidney_and_carcinoma_with_traditional_method'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            **kidney_carcinoma_comparison_dict_generator(KidneyCarcinomaRatioSupMaterials),
            ParameterName.data_name: DataName.renal_carcinoma_invivo_infusion_traditional_method,
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


class FigureS4(Elements.Figure):
    figure_label = 'figure_s4'
    figure_title = 'Figure S4'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio
        subfigure_a_b_height = 0.3
        subfigure_d_e_width = 0.4
        subfigure_e_height = 0.25
        subfigure_c_width = 0.6
        subfigure_c_d_height = 0.35
        subfigure_d_e_x_loc = subfigure_c_width + subfigure_d_e_width / 2

        scatter_plot_width = 0.43
        figure_layout_list = [
            (subfigure_a_b_height, [
                (0.55, 'a'),
                (0.45, 'b'),
            ]),
            (subfigure_c_d_height, [
                (subfigure_c_width, 'c'),
                (subfigure_d_e_width, 'd'),
            ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)

        subfigure_e_size = Vector(subfigure_d_e_width, subfigure_e_height)
        subfigure_e_center_y_loc = subfigure_a_b_height + subfigure_c_d_height + -0.01 + subfigure_e_height / 2
        subfigure_e_center = Vector(subfigure_d_e_x_loc, subfigure_e_center_y_loc)

        subfigure_obj_list.extend([
            single_subfigure_layout(
                subfigure_e_center, subfigure_e_size, SubfigureE, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
        ])

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
