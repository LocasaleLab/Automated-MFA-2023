from ..config import Vector, ParameterName
from ..config import CompositeFigure, TextBox, ProtocolSearchingMaterials
from ..config import ZOrderConfig, TextConfig, HorizontalAlignment, VerticalAlignment, FontWeight, CommonElementConfig
from ..basic_data_figure.scatter_data_figure import AccuracyVariationScatterDataFigure
from ..basic_data_figure.bar_data_figure import FluxErrorBarDataFigure

from ...common_functions import initialize_vector_input
from ..config import common_legend_generator, CommonFigureString, default_parameter_extract, DataName


class AllFluxComparisonBarFigureConfig(object):
    left = 0
    # total_width = 1.6
    total_width = 1
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
    title_center_x = 0.55

    title_text_config = {
        **CommonElementConfig.common_text_config,
        ParameterName.font_size: 12,
        ParameterName.width: total_width,
        ParameterName.text_box: False
    }
    main_title_config = {
        **title_text_config,
        ParameterName.font_size: 15,
        ParameterName.font_weight: FontWeight.bold,
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


