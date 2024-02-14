from ..common.config import ParameterName, DataName, np, Vector, calculate_center_bottom_offset, Figure
from ..common.elements import Elements
from ..common.common_figure_materials import CommonFigureString, CommonFigureMaterials

from ..figure_elements.data_figure.figure_data_loader import raw_model_data


Subfigure = Elements.Subfigure
common_data_figure_scale = 0.4
common_data_width = 1
all_net_flux_comparison_scale = 0.35

SensitivityDiagram = Elements.SensitivityDiagram
SingleLossOrDistanceFigure = Elements.SingleLossOrDistanceFigure
common_sensitivity_diagram_scale = 0.35
common_optimized_size = 20000
optimized_size_50000 = 50000
common_selection_size = 100
selection_size_50 = 50
selection_size_20 = 20
selection_size_10 = 10
selection_size_5 = 5
evenly_distributed_ax_width = 0.7
remove_pathway_ax_width = 0.56
compartmentalization_ax_width = 0.6
ax_common_height = 0.2


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'sensitivity_analysis_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.28
        OptimizationDiagram = Elements.OptimizationDiagram
        mode = ParameterName.data_sensitivity

        optimization_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.mode: mode,
            ParameterName.background: False,
        })

        center = optimization_diagram.calculate_center(optimization_diagram, scale, mode)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        optimization_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.03, -0.015))

        subfigure_element_dict = {
            optimization_diagram.name: optimization_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'protocol_diagram_sensitivity'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.45
        mode = ParameterName.sensitivity

        data_sensitivity_generator_diagram = Elements.DataSensitivityGeneratorDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.mode: mode,
        })

        center = data_sensitivity_generator_diagram.calculate_center(data_sensitivity_generator_diagram, scale, mode)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        data_sensitivity_generator_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, -0.005))

        subfigure_element_dict = {
            data_sensitivity_generator_diagram.name: data_sensitivity_generator_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'data_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.smaller_data_size
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, -0.02))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


def obtain_and_process_data_sensitivity_data(
        figure_data_parameter_dict, all_case_list, loss_adjusted_factor_list=None, raw_flux_vector=False,
        selected_solutions=False, flux_relative_distance=False):
    if flux_relative_distance:
        (
            value_dict_list, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list
        ) = raw_model_data.return_all_flux_data(**figure_data_parameter_dict)
        second_parameter = flux_name_list
        value_dict_list = value_dict_list[1:]
    elif raw_flux_vector:
        (
            value_dict_list, flux_name_list, analyzed_set_size_list, selected_min_loss_size_list
        ) = raw_model_data.return_diff_vector_data(**figure_data_parameter_dict)
        second_parameter = flux_name_list
        if selected_solutions:
            value_dict_list = value_dict_list[:1]
        else:
            value_dict_list = value_dict_list[1:]
    else:
        (
            value_dict_list, max_value, analyzed_set_size_list,
            selected_min_loss_size_list) = raw_model_data.return_scatter_data(**figure_data_parameter_dict)
        second_parameter = max_value
    new_value_dict_list = []
    value_dict_num = len(value_dict_list)
    modified_value_dict_list = []
    for value_dict in value_dict_list:
        modified_value_dict = {}
        for case_name_obj, case_content in value_dict.items():
            modified_value_dict[str(case_name_obj)] = case_content
        modified_value_dict_list.append(modified_value_dict)
    for case_index, (case_name, *parameter_pair) in enumerate(all_case_list):
        if len(parameter_pair) == 0:
            current_optimized_size = common_optimized_size
            current_selection_size = common_selection_size
        else:
            current_optimized_size, current_selection_size = parameter_pair
        for value_dict_index, modified_value_dict in enumerate(modified_value_dict_list):
            current_total_index = value_dict_num * case_index + value_dict_index
            while len(new_value_dict_list) <= current_total_index:
                new_value_dict_list.append({})
            new_value_dict = new_value_dict_list[current_total_index]
            current_nested_list = modified_value_dict[case_name][current_selection_size][current_optimized_size]
            if np.ndim(current_nested_list) == 2 and len(current_nested_list) == 1:
                current_nested_list = current_nested_list[0]
            if loss_adjusted_factor_list is not None:
                current_nested_list = [
                    current_value * loss_adjusted_factor_list[case_index] for current_value in current_nested_list]
            if common_selection_size not in new_value_dict:
                new_value_dict[common_selection_size] = {}
            new_value_dict[common_selection_size][common_optimized_size] = current_nested_list
    figure_data_parameter_dict[ParameterName.figure_data] = (
        new_value_dict_list, second_parameter, analyzed_set_size_list,
        selected_min_loss_size_list
    )


(
    common_select_average_name_dict, common_select_average_color_dict
) = CommonFigureMaterials.select_average_solution_name_color_dict(CommonFigureMaterials, wrap_name=False)

evenly_distributed_all_case_list = [
    ('raw_data',),
    ('medium_data',),
    ('medium_data', common_optimized_size, selection_size_10),
    # ('medium_data', optimized_size_50000, selection_size_20),
    ('few_data',),
    ('few_data', common_optimized_size, selection_size_10),
]
evenly_distributed_adjusted_factor_list = [21 / 21, 21 / 13, 21 / 7]
evenly_distributed_wrap_labels_list = [
    f'{CommonFigureString.experimental_available_mid_data_wrap}\nSelect 100\nfrom 20000',
    f'{CommonFigureString.medium_data}\nSelect 100\nfrom 20000',
    f'{CommonFigureString.medium_data}\nSelect 10\nfrom 20000',
    # f'{CommonFigureString.medium_data}_50k_20',
    f'{CommonFigureString.few_data}\nSelect 100\nfrom 20000',
    f'{CommonFigureString.few_data}\nSelect 100\nfrom 20000',
]
evenly_distributed_labels_list = [
    f'{CommonFigureString.experimental_available_mid_data}, select 100 from 20000',
    f'{CommonFigureString.medium_data}, select 100 from 20000',
    f'{CommonFigureString.medium_data}, select 10 from 20000',
    # f'{CommonFigureString.medium_data}_50k_20',
    CommonFigureString.few_data,
    f'{CommonFigureString.few_data}, select 10 from 20000',
]
evenly_distributed_medium_data_list = evenly_distributed_all_case_list[:3]
evenly_distributed_medium_data_labels_list = evenly_distributed_labels_list[:3]
evenly_distributed_few_data_list = evenly_distributed_all_case_list[3:]
evenly_distributed_few_data_labels_list = evenly_distributed_labels_list[3:]
# distance_title = CommonFigureString.net_euclidean_distance
distance_title = CommonFigureString.distance_to_known_flux


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'loss_comparison_evenly_distributed_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        color_list = [
            common_select_average_color_dict[key]
            for key in [ParameterName.selected, ParameterName.averaged] * len(evenly_distributed_all_case_list)
        ]

        figure_data_parameter_dict = {
            ParameterName.ax_total_size: Vector(evenly_distributed_ax_width, ax_common_height),
            ParameterName.figure_title: distance_title,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.x_tick_labels_list: evenly_distributed_wrap_labels_list,
            ParameterName.color_dict: common_select_average_color_dict,
            ParameterName.color: color_list,
            ParameterName.legend: True,
            ParameterName.name_dict: common_select_average_name_dict,
            ParameterName.figure_class: ParameterName.net_euclidean_distance,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.common_y_lim: [0, 2000],
            ParameterName.default_y_tick_label_list: [0, 500, 1000, 1500, 2000]
        }
        obtain_and_process_data_sensitivity_data(figure_data_parameter_dict, evenly_distributed_all_case_list)
        scale = common_data_figure_scale
        data_sensitivity_comparison_figure = SingleLossOrDistanceFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = data_sensitivity_comparison_figure.calculate_center(data_sensitivity_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        data_sensitivity_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            data_sensitivity_comparison_figure.name: data_sensitivity_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'flux_relative_error_evenly_distributed_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.relative_error_to_known_flux,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.subplot_name_list: evenly_distributed_medium_data_labels_list,
            ParameterName.text_axis_loc_pair: Vector(0.4, 0.92)
        }
        obtain_and_process_data_sensitivity_data(
            figure_data_parameter_dict, evenly_distributed_medium_data_list, flux_relative_distance=True)
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(
            scale, **figure_data_parameter_dict)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, 0.01)
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'data_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.data_without_pathway
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, -0.01))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


remove_pathway_all_case_list = [
    ('raw_data', ), ('data_without_ppp', ), ('data_without_aa', ), ('data_without_tca', )]
remove_pathway_adjusted_factor_list = [21 / 21, 21 / 13, 21 / 7]
remove_pathway_labels_list = [
    CommonFigureString.complete_data,
    CommonFigureString.data_without_ppp,
    CommonFigureString.data_without_aa,
    CommonFigureString.data_without_tca,
]


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'loss_comparison_remove_pathway'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        adjusted_factor_list = None
        color_list = [
            common_select_average_color_dict[key]
            for key in [ParameterName.selected, ParameterName.averaged] * len(remove_pathway_all_case_list)
        ]

        figure_data_parameter_dict = {
            ParameterName.ax_total_size: Vector(remove_pathway_ax_width, ax_common_height),
            ParameterName.figure_title: distance_title,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.x_tick_labels_list: remove_pathway_labels_list,
            ParameterName.color_dict: common_select_average_color_dict,
            ParameterName.color: color_list,
            ParameterName.name_dict: common_select_average_name_dict,
            ParameterName.legend: True,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.figure_class: ParameterName.net_euclidean_distance,
            ParameterName.common_y_lim: [0, 1500],
            ParameterName.default_y_tick_label_list: [0, 500, 1000, 1500]
        }
        obtain_and_process_data_sensitivity_data(figure_data_parameter_dict, remove_pathway_all_case_list)
        scale = common_data_figure_scale
        data_sensitivity_comparison_figure = SingleLossOrDistanceFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = data_sensitivity_comparison_figure.calculate_center(data_sensitivity_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        data_sensitivity_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            data_sensitivity_comparison_figure.name: data_sensitivity_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'flux_relative_error_remove_pathway_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.relative_error_to_known_flux,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.subplot_name_list: remove_pathway_labels_list
        }
        obtain_and_process_data_sensitivity_data(
            figure_data_parameter_dict, remove_pathway_all_case_list, flux_relative_distance=True)
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        center = raw_model_all_data_flux_error_bar_comparison_figure.calculate_center(
            scale, **figure_data_parameter_dict)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size) + Vector(0, -0.01)
        raw_model_all_data_flux_error_bar_comparison_figure.move_and_scale(
            bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            raw_model_all_data_flux_error_bar_comparison_figure.name:
                raw_model_all_data_flux_error_bar_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureI(Subfigure):
    subfigure_label = 'i'
    subfigure_title = 'data_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.compartmental_data
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, -0.01))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


compartmentalization_all_case_list = [('all_data', ), ('data_without_combination', ), ('raw_data', )]
compartmentalization_labels_list = [
    CommonFigureString.all_compartmentalized_data,
    CommonFigureString.experimental_compartmentalized_data,
    CommonFigureString.experimental_mixed_data,]
compartmentalization_wrap_labels_list = [
    CommonFigureString.all_compartmentalized_data_wrap,
    CommonFigureString.experimental_compartmentalized_data_wrap,
    CommonFigureString.experimental_mixed_data_wrap,]


class SubfigureJ(Subfigure):
    subfigure_label = 'j'
    subfigure_title = 'loss_comparison_compartmentalization'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # adjusted_factor_list = [21 / 21, 21 / 13, 21 / 7]
        adjusted_factor_list = None
        color_list = [
            common_select_average_color_dict[key]
            for key in [ParameterName.selected, ParameterName.averaged] * len(compartmentalization_all_case_list)
        ]
        figure_data_parameter_dict = {
            ParameterName.ax_total_size: Vector(compartmentalization_ax_width, ax_common_height),
            ParameterName.figure_title: distance_title,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.x_tick_labels_list: compartmentalization_wrap_labels_list,
            ParameterName.color_dict: common_select_average_color_dict,
            ParameterName.name_dict: common_select_average_name_dict,
            ParameterName.color: color_list,
            ParameterName.legend: True,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.figure_class: ParameterName.net_euclidean_distance,
            ParameterName.common_y_lim: [0, 1000],
            ParameterName.default_y_tick_label_list: [0, 500, 1000]
        }
        obtain_and_process_data_sensitivity_data(figure_data_parameter_dict, compartmentalization_all_case_list)
        scale = common_data_figure_scale
        data_sensitivity_comparison_figure = SingleLossOrDistanceFigure(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = data_sensitivity_comparison_figure.calculate_center(data_sensitivity_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        data_sensitivity_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            data_sensitivity_comparison_figure.name: data_sensitivity_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureK(Subfigure):
    subfigure_label = 'k'
    subfigure_title = 'flux_relative_error_compartmentalization_mid_data'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.figure_title: CommonFigureString.relative_error_to_known_flux,
            ParameterName.data_name: DataName.data_sensitivity,
            ParameterName.flux_relative_distance: True,
            ParameterName.optimized_size: common_optimized_size,
            ParameterName.selection_size: common_selection_size,
            ParameterName.subplot_name_list: compartmentalization_labels_list,
            ParameterName.text_axis_loc_pair: Vector(0.5, 0.92)
        }
        obtain_and_process_data_sensitivity_data(
            figure_data_parameter_dict, compartmentalization_all_case_list, flux_relative_distance=True)
        scale = all_net_flux_comparison_scale
        raw_model_all_data_flux_error_bar_comparison_figure = Elements.OptimizedAllFluxComparisonBarDataFigure(**{
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


class Figure3(Figure):
    figure_label = 'figure_3'
    figure_title = 'Figure 3'

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
            SubfigureJ,
            SubfigureK,
        ]

        # figure_size = Constant.default_figure_size
        # height_to_width_ratio = figure_size[1] / figure_size[0]
        # top_margin_ratio = FigureConfig.top_margin_ratio
        # side_margin_ratio = FigureConfig.side_margin_ratio

        left_column_width = 0.45
        right_column_width = 0.55
        right_column_center_x = left_column_width + right_column_width / 2

        a_b_row_height = 0.2
        evenly_distributed_diagram_height = 0.11
        remove_pathway_diagram_height = 0.13
        diagram_height_2 = 0.13
        net_distance_figure_height = 0.13
        evenly_distributed_height = evenly_distributed_diagram_height + net_distance_figure_height
        remove_pathway_height = remove_pathway_diagram_height + net_distance_figure_height
        compartmental_mid_height = diagram_height_2 + net_distance_figure_height
        evenly_distributed_size = Vector(right_column_width, evenly_distributed_height)
        evenly_distributed_center_y = a_b_row_height + evenly_distributed_height / 2
        evenly_distributed_center = Vector(right_column_center_x, evenly_distributed_center_y)
        remove_pathway_size = Vector(right_column_width, remove_pathway_height)
        remove_pathway_center_y = evenly_distributed_center_y + evenly_distributed_height / 2 + remove_pathway_height / 2
        remove_pathway_center = Vector(right_column_center_x, remove_pathway_center_y)
        compartmental_mid_size = Vector(right_column_width, compartmental_mid_height)
        compartmental_mid_center_y = remove_pathway_center_y + remove_pathway_height / 2 + compartmental_mid_height / 2
        compartmental_mid_center = Vector(right_column_center_x, compartmental_mid_center_y)

        figure_layout_list = [
            (a_b_row_height, [
                (left_column_width, 'a'),
                (right_column_width, 'b')
            ]),
            (evenly_distributed_diagram_height, [
                (left_column_width, 'c'),
            ]),
            (net_distance_figure_height, [
                (left_column_width, 'd')
            ]),
            (remove_pathway_diagram_height, [
                (left_column_width, 'f'),
            ]),
            (net_distance_figure_height, [
                (left_column_width, 'g'),
            ]),
            (diagram_height_2, [
                (left_column_width, 'i'),
            ]),
            (net_distance_figure_height, [
                (left_column_width, 'j')
            ]),
        ]

        single_subfigure_layout_dict = {
            'e': (evenly_distributed_center, evenly_distributed_size),
            'h': (remove_pathway_center, remove_pathway_size),
            'k': (compartmental_mid_center, compartmental_mid_size),
        }
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, single_subfigure_layout_dict,
            figure_title=self.figure_title)

