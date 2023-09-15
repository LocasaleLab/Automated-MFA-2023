from ..common.config import ParameterName, Constant, DataName
from ..common.common_figure_materials import CommonFigureMaterials, MouseComparisonMaterials, \
    LungCancerComparisonMaterials, MultipleTumorRawMaterials, MultipleTumorRatioMaterials, FigureConfig, \
    CommonFigureString
from ..figure_elements.element_dict import ElementName, element_dict
from ..common.color import ColorConfig
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout, \
    Vector, single_subfigure_layout

Subfigure = element_dict[ElementName.Subfigure]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
MetabolicNetworkWithLegend = element_dict[ElementName.MetabolicNetworkWithLegend]
FluxComparisonScatterWithTitle = element_dict[ElementName.FluxComparisonScatterWithTitle]
ExperimentDiagram = element_dict[ElementName.ExperimentDiagram]

# common_data_figure_scale = FigureConfig.common_data_figure_scale
common_data_figure_scale = 0.8
common_data_width = 0.5


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'experimental_data_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.45
        data_name = DataName.multiple_tumor
        center = ExperimentDiagram.calculate_center(ExperimentDiagram, scale, data_name)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        experiment_diagram = ExperimentDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.01, -0.01),
            ParameterName.scale: scale,
            ParameterName.data_name: data_name,
        })

        subfigure_element_dict = {experiment_diagram.name: experiment_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


def multiple_tumor_comparison_dict_generator(config_class):
    common_multiple_tumor_comparison_dict = {
        ParameterName.data_name: DataName.multiple_tumor,
        ParameterName.comparison_name: '',
        ParameterName.flux_name_list: config_class.flux_name_location_list,
        ParameterName.mean: False,
        ParameterName.display_flux_name_dict: config_class.display_flux_name_dict,
        ParameterName.y_lim_list: config_class.y_lim_list,
        ParameterName.y_ticks_list: config_class.y_ticks_list,
        ParameterName.display_group_name_dict: config_class.class_display_name_dict,
        # ParameterName.name_dict: config_class.name_dict,
        ParameterName.color_dict: config_class.color_dict,
        ParameterName.common_x_label: 'Tumor type',
        ParameterName.compare_one_by_one: False,
        ParameterName.scatter_line: False,
        ParameterName.error_bar: True,
        ParameterName.column_width: 1,
        ParameterName.class_width: 0.6,
    }
    return common_multiple_tumor_comparison_dict


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'comparison_between_multiple_tumor_raw_flux'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            # ParameterName.height_to_width_ratio: 1.2,
            # ParameterName.figure_title: Title.comparison_between_different_tumor,
            **multiple_tumor_comparison_dict_generator(MultipleTumorRawMaterials),
        }
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        scale = common_data_figure_scale
        flux_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(flux_grid_comparison_figure, scale, flux_name_list)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'comparison_between_multiple_tumor_ratio'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            # ParameterName.height_to_width_ratio: 0.8,
            # ParameterName.figure_title: Title.comparison_between_different_tumor,
            **multiple_tumor_comparison_dict_generator(MultipleTumorRatioMaterials),
        }
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        scale = common_data_figure_scale
        flux_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(flux_grid_comparison_figure, scale, flux_name_list)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'comparison_between_normal_lung_tumor_patients'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        # figure_data_parameter_dict = {
        #     ParameterName.figure_title: Title.comparison_between_normal_lung_tumor_patients,
        #     ParameterName.data_name: ParameterName.lung_tumor_invivo_infusion,
        #     ParameterName.comparison_name: 'human',
        #     ParameterName.flux_name_location_nested_list: CommonFigureMaterials.common_flux_location_nested_list,
        # }
        figure_data_parameter_dict = {
            ParameterName.height_to_width_ratio: 1,
            ParameterName.figure_title: CommonFigureString.comparison_between_normal_lung_tumor_patients,
            ParameterName.data_name: DataName.lung_tumor_invivo_infusion,
            ParameterName.comparison_name: 'human',
            ParameterName.flux_name_list: LungCancerComparisonMaterials.flux_name_location_list,
            ParameterName.mean: False,
            ParameterName.display_flux_name_dict: LungCancerComparisonMaterials.display_flux_name_dict,
            ParameterName.y_lim_list: LungCancerComparisonMaterials.y_lim_list,
            ParameterName.y_ticks_list: LungCancerComparisonMaterials.y_ticks_list,
            ParameterName.display_group_name_dict: LungCancerComparisonMaterials.class_display_name_dict,
            ParameterName.color_dict: LungCancerComparisonMaterials.color_dict,
        }
        scale = common_data_figure_scale
        loss_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = loss_grid_comparison_figure.calculate_center(loss_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        loss_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            loss_grid_comparison_figure.name: loss_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'comparison_between_normal_flank_tumor'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        figure_data_parameter_dict = {
            ParameterName.height_to_width_ratio: 1,
            ParameterName.figure_title: CommonFigureString.comparison_between_normal_flank_tumor,
            ParameterName.data_name: DataName.lung_tumor_invivo_infusion,
            ParameterName.comparison_name: 'mouse_lung_vs_tumor',
            ParameterName.flux_name_list: MouseComparisonMaterials.flux_name_location_list,
            ParameterName.mean: False,
            ParameterName.display_flux_name_dict: MouseComparisonMaterials.display_flux_name_dict,
            ParameterName.y_lim_list: MouseComparisonMaterials.y_lim_list,
            ParameterName.y_ticks_list: MouseComparisonMaterials.y_ticks_list,
            ParameterName.display_group_name_dict: MouseComparisonMaterials.class_display_name_dict,
            ParameterName.color_dict: MouseComparisonMaterials.color_dict,
        }
        scale = common_data_figure_scale
        flux_grid_comparison_figure = FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: common_data_width,
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })

        center = flux_grid_comparison_figure.calculate_center(flux_grid_comparison_figure, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        flux_grid_comparison_figure.move_and_scale(bottom_left_offset=center_bottom_offset)

        subfigure_element_dict = {
            flux_grid_comparison_figure.name: flux_grid_comparison_figure}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS5(element_dict[ElementName.Figure]):
    figure_label = 'figure_s5'
    figure_title = 'Figure S5'

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

        scatter_plot_width = 0.43
        figure_layout_list = [
            (0.2, [
                # (0.45, 'c'),
                (0.9, 'a')
            ]),
            (0.4, [
                (scatter_plot_width, 'b'),
                # (0.5, 'c'),
                # (0.5, 'd')
            ]),
            # (0.3, [
            #     (0.45, 'e'),
            #     # (0.5, 'f')
            # ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)

        subfigure_c_top = figure_layout_list[0][0]
        subfigure_c_size = Vector(scatter_plot_width, 0.285)
        subfigure_c_center = Vector(1.5 * scatter_plot_width, subfigure_c_top + subfigure_c_size.y / 2)

        subfigure_obj_list.extend([
            single_subfigure_layout(
                subfigure_c_center, subfigure_c_size, SubfigureC, height_to_width_ratio, top_margin_ratio,
                side_margin_ratio),
        ])

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)
