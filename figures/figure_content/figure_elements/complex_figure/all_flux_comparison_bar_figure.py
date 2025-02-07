from ...common.config import Vector, ParameterName, CommonElementConfig, CompositeFigure, TextBox
from ...common.common_figure_materials import ProtocolSearchingMaterials
from ..data_figure.config import CommonFigureString, default_parameter_extract, DataName
from ..data_figure.bar_data_figure import FluxErrorBarDataFigure, HCT116OptimizedFluxErrorBarDataFigure, \
    SimulatedDataOptimizedFluxErrorBarDataFigure, DataSensitivityOptimizedFluxErrorBarDataFigure, \
    AveragedReoptimizdDifferenceFluxErrorBarDataFigure
from ..diagrams.flux_sloppiness_diagram import MultipleFluxSloppinessDiagram


class AllFluxComparisonBarFigureConfig(object):
    left = 0
    # total_width = 1.6
    total_width = 1
    total_width_with_sloppiness_diagram = 1.2
    bar_axis_bottom = 0.16
    bar_axis_height = 0.18
    bar_axis_top = bar_axis_bottom + bar_axis_height  # 0.34
    subtitle_axis_distance = 0.01
    subtitle_height = 0.02
    subtitle_center_y = bar_axis_top + subtitle_axis_distance + subtitle_height / 2  # 0.37
    main_title_height = 0.04
    main_title_center_y = subtitle_center_y + subtitle_height / 2 + main_title_height / 2
    main_title_top = 0
    total_height = main_title_center_y + main_title_height / 2 + main_title_top    # 0.41

    bar_axis_left = 0.04
    bar_axis_right = 0.02
    bar_axis_width = total_width - bar_axis_left - bar_axis_right
    bar_axis_size = Vector(bar_axis_width, bar_axis_height)
    bar_axis_left_with_sloppiness_diagram = 0.24
    title_center_x = 0.55

    title_text_config = {
        **CommonElementConfig.common_text_config,
        ParameterName.font_size: 12,
        ParameterName.width: total_width,
        ParameterName.text_box: False
    }
    main_title_config = {
        **title_text_config,
        ParameterName.font_size: 17,
        ParameterName.height: main_title_height,
        ParameterName.center: Vector(title_center_x, main_title_center_y)
    }
    subtitle_config = {
        **title_text_config,
        ParameterName.height: subtitle_height,
        ParameterName.center: Vector(title_center_x, subtitle_center_y)
    }


class AllFluxComparisonBarFigure(CompositeFigure):
    total_width = AllFluxComparisonBarFigureConfig.total_width
    total_height = AllFluxComparisonBarFigureConfig.total_height
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, None, pop=True)
        if data_name == DataName.raw_model_all_data:
            optimization_size = ProtocolSearchingMaterials.all_data_target_optimization_size
            selection_size = ProtocolSearchingMaterials.all_data_target_selection_size
        elif data_name == DataName.raw_model_raw_data:
            optimization_size = ProtocolSearchingMaterials.experimental_data_target_optimization_size
            selection_size = ProtocolSearchingMaterials.experimental_data_target_selection_size
        else:
            raise ValueError()
        bar_axis_left = AllFluxComparisonBarFigureConfig.bar_axis_left
        bar_axis_bottom = AllFluxComparisonBarFigureConfig.bar_axis_bottom
        bar_axis_size = AllFluxComparisonBarFigureConfig.bar_axis_size

        all_flux_error_bar_data_figure_config_dict = {
            ParameterName.bottom_left: Vector(bar_axis_left, bar_axis_bottom),
            ParameterName.size: bar_axis_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.optimized_size: optimization_size,
                ParameterName.selection_size: selection_size,
            }
        }
        all_flux_error_bar_data_figure_obj = FluxErrorBarDataFigure(
            **all_flux_error_bar_data_figure_config_dict)

        main_title_text_config_dict = {
            **AllFluxComparisonBarFigureConfig.main_title_config,
            ParameterName.string: f'Relative error of all fluxes',
        }
        subtitle_text_config_dict = {
            **AllFluxComparisonBarFigureConfig.subtitle_config,
            ParameterName.string: f'${CommonFigureString.math_n} = {optimization_size}$, '
                                  f'${CommonFigureString.math_m} = {selection_size}$, '
                                  f'${CommonFigureString.m_over_n} = {int(optimization_size/selection_size)}' r'^{-1}$',
        }
        text_obj_dict = {
            'main_title': TextBox(**main_title_text_config_dict),
            'sub_title': TextBox(**subtitle_text_config_dict),
        }
        size = Vector(self.total_width, self.total_height)
        distance_variation_scatter_data_figure_dict = {
            ParameterName.text: text_obj_dict,
            'all_flux_error_bar_data_figure': {
                'all_flux_error_bar_data_figure': all_flux_error_bar_data_figure_obj,
            },
        }
        super().__init__(
            distance_variation_scatter_data_figure_dict, Vector(0, 0), size, background=False, **kwargs)


class OptimizedAllFluxComparisonBarDataFigure(CompositeFigure):
    total_width = AllFluxComparisonBarFigureConfig.total_width
    total_height = 1.2
    title_height = 0.05
    each_row_gap_height = 0.015
    top_height = 0.05
    top_height_with_subtitle = 0.06
    subtitle_height = 0.03
    bar_axis_left = AllFluxComparisonBarFigureConfig.bar_axis_left
    bar_axis_bottom = AllFluxComparisonBarFigureConfig.bar_axis_bottom
    bar_axis_width = AllFluxComparisonBarFigureConfig.bar_axis_width
    bar_axis_height = AllFluxComparisonBarFigureConfig.bar_axis_height

    @staticmethod
    def calculate_bar_height(self, row_num):
        bar_height = (
            self.each_row_gap_height * (row_num - 1) + self.bar_axis_height * row_num)
        return bar_height

    @staticmethod
    def calculate_total_height(self, bar_row_num):
        total_bar_axis_height = self.calculate_bar_height(self, bar_row_num)
        if self.figure_subtitle is None:
            top_height = self.top_height
            title_height = top_height
            title_center_y = self.bar_axis_bottom + total_bar_axis_height + top_height / 2
            subtitle_center_y = title_center_y
            subtitle_height = title_height
        else:
            top_height = self.top_height_with_subtitle
            subtitle_height = self.subtitle_height
            title_height = top_height - subtitle_height
            subtitle_center_y = self.bar_axis_bottom + total_bar_axis_height + subtitle_height / 2
            title_center_y = subtitle_center_y + subtitle_height / 2 + title_height / 2
        total_height = self.bar_axis_bottom + total_bar_axis_height + top_height
        return total_height, title_center_y, title_height, subtitle_center_y, subtitle_height

    def calculate_center(self, scale, *args, **kwargs):
        bar_row_num = self.target_class.calculate_row_num(self.target_class, **kwargs)
        total_height, *_ = self.calculate_total_height(self, bar_row_num)
        total_width = self.total_width
        return Vector(total_width, total_height) * scale / 2

    def __init__(self, figure_data_parameter_dict, **kwargs):
        bar_axis_height = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.ax_height, None, pop=True)
        if bar_axis_height is not None:
            self.bar_axis_height = bar_axis_height
        data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, None, pop=True)
        if data_name in {
                DataName.hct116_cultured_cell_line, DataName.hct116_cultured_cell_line_squared_loss,
                DataName.hct116_cultured_cell_line_with_glns_m}:
            target_class = HCT116OptimizedFluxErrorBarDataFigure
        elif data_name in {
                DataName.optimization_from_solutions_raw_data, DataName.optimization_from_solutions_all_data,
                DataName.raw_model_raw_data, DataName.raw_model_all_data,
                DataName.raw_model_with_glns_m_raw_data, DataName.raw_model_with_glns_m_all_data,
        }:
            diff_between_averaged_and_re_optimized = default_parameter_extract(
                figure_data_parameter_dict, ParameterName.optimized, False)
            if diff_between_averaged_and_re_optimized:
                target_class = AveragedReoptimizdDifferenceFluxErrorBarDataFigure
            else:
                target_class = SimulatedDataOptimizedFluxErrorBarDataFigure
        elif data_name in {DataName.data_sensitivity}:
            target_class = DataSensitivityOptimizedFluxErrorBarDataFigure
        else:
            raise ValueError()
        self.target_class = target_class
        figure_title = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_title, None)
        figure_subtitle = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_subtitle, None)
        self.figure_subtitle = figure_subtitle

        bar_axis_width = self.bar_axis_width
        with_sloppiness_diagram = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_sloppiness_diagram, False, pop=True)
        if with_sloppiness_diagram:
            self.total_width = AllFluxComparisonBarFigureConfig.total_width_with_sloppiness_diagram
            self.bar_axis_left = AllFluxComparisonBarFigureConfig.bar_axis_left_with_sloppiness_diagram
        total_width = self.total_width
        bar_axis_left = self.bar_axis_left

        bar_row_num = target_class.calculate_row_num(target_class, **figure_data_parameter_dict)
        total_bar_axis_height = self.calculate_bar_height(self, bar_row_num)
        (
            total_height, title_center_y, title_height, subtitle_center_y,
            subtitle_height) = self.calculate_total_height(self, bar_row_num)
        title_center_x = bar_axis_left + bar_axis_width / 2
        title_center = Vector(title_center_x, title_center_y)
        subtitle_center = Vector(title_center_x, subtitle_center_y)
        self.total_height = total_height
        bar_axis_bottom = self.bar_axis_bottom
        bar_axis_size = Vector(bar_axis_width, total_bar_axis_height)

        bar_y_interval = self.each_row_gap_height / total_bar_axis_height

        optimized_flux_comparison_config_dict = {
            ParameterName.bottom_left: Vector(bar_axis_left, bar_axis_bottom),
            ParameterName.size: bar_axis_size,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.ax_interval: bar_y_interval,
                ParameterName.data_name: data_name,
                **figure_data_parameter_dict,
            }
        }

        subfigure_element_dict = {
            'optimized_flux_comparison': {
                'optimized_flux_comparison': target_class(**optimized_flux_comparison_config_dict)},
        }
        if with_sloppiness_diagram:
            sloppiness_config_dict = {
                ParameterName.scale: total_bar_axis_height,
                ParameterName.bottom_left_offset: Vector(0, bar_axis_bottom),
                ParameterName.figure_data_parameter_dict: {
                    ParameterName.horiz_or_vertical: ParameterName.vertical,
                    ParameterName.ax_interval: bar_y_interval,
                    ParameterName.data_name: ParameterName.all_data_mode,
                    ParameterName.figure_title: [
                        CommonFigureString.selected_solution,
                        CommonFigureString.averaged_solution,
                        CommonFigureString.reoptimized_solution]
                }
            }
            subfigure_element_dict['flux_sloppiness_diagram'] = {
                'flux_sloppiness_diagram': MultipleFluxSloppinessDiagram(**sloppiness_config_dict)
            }
        if figure_title is not None:
            main_title_text_config_dict = {
                **AllFluxComparisonBarFigureConfig.main_title_config,
                ParameterName.string: figure_title,
                ParameterName.width: total_width,
                ParameterName.height: title_height,
                ParameterName.center: title_center
            }
            subfigure_element_dict['title'] = {'title': TextBox(**main_title_text_config_dict)}
        if figure_subtitle is not None:
            main_title_text_config_dict = {
                **AllFluxComparisonBarFigureConfig.subtitle_config,
                ParameterName.string: figure_subtitle,
                ParameterName.width: total_width,
                ParameterName.height: subtitle_height,
                ParameterName.center: subtitle_center
            }
            subfigure_element_dict['subtitle'] = {'subtitle': TextBox(**main_title_text_config_dict)}

        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)

