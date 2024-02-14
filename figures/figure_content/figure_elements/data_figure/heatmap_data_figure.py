from .figure_data_loader import raw_model_data, all_fluxes_relative_error_data
from .config import np, Vector, DataFigureParameterName as ParameterName, FontWeight, \
    default_parameter_extract, sensitivity_heatmap_cbar_axis_label_dict, \
    heatmap_highlight_ellipse_parameter, DataFigureConfig, \
    sensitivity_heatmap_y_axis_labels_generator, net_flux_x_axis_labels_generator, merge_axis_format_dict, \
    CommonFigureString, DataName, ColorBarDataFigure, HeatmapConfig, HeatmapDataFigure

HeatmapValueFormat = HeatmapConfig.HeatmapValueFormat


class DistanceAnalysisColorBarDataFigure(ColorBarDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, scale=1, **kwargs):
        percentage, decimal_num, new_figure_config_dict = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.percentage, ParameterName.decimal_num, ParameterName.figure_config_dict
            ], [False, None, {}], pop=True)
        x_label_format_dict = merge_axis_format_dict(
            {},
            {
                ParameterName.font_size: HeatmapConfig.distance_x_y_label_font_size * scale,
                ParameterName.axis_label_distance: 0.02 * scale,
            },
            new_figure_config_dict, ParameterName.x_label_format_dict)
        x_tick_label_format_dict = merge_axis_format_dict(
            {},
            {
                ParameterName.font_size: HeatmapConfig.distance_x_y_tick_label_font_size * scale,
                ParameterName.axis_tick_label_distance: 0.005 * scale,
                ParameterName.percentage: percentage,
                ParameterName.decimal_num: decimal_num
            },
            new_figure_config_dict, ParameterName.x_tick_label_format_dict)
        figure_config_dict = {
            ParameterName.x_label_format_dict: x_label_format_dict,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
        }

        figure_data_parameter_dict = {
            ParameterName.heatmap_cmap: HeatmapConfig.common_heatmap_cmap,
            ParameterName.figure_config_dict: figure_config_dict,

            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)


class DistanceFluxAnalysisHeatmapDataFigure(HeatmapDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            cbar=False, cbar_figure_data_parameter_dict=None, cbar_bottom_left: Vector = None,
            cbar_size: Vector = None, highlight=False, scale=1, **kwargs):
        # ax_total_bottom_left = Vector(0.1, 0.1)
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        x_label_format_dict = DataFigureConfig.x_label_format_dict_generator(scale)
        x_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_label_font_size * scale,
            ParameterName.axis_label_distance: 0.02 * scale,
        })
        x_tick_label_format_dict = DataFigureConfig.x_tick_label_format_dict_generator(scale)
        x_tick_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_tick_label_font_size * scale,
            ParameterName.axis_tick_label_distance: 0.006 * scale
            # ParameterName.axis_tick_label_distance: 0.02 * scale
        })
        y_label_format_dict = DataFigureConfig.y_label_format_dict_generator(scale)
        y_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_label_font_size * scale,
            ParameterName.axis_label_distance: 0.025 * scale,
        })
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_format_dict_generator(scale)
        y_tick_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_tick_label_font_size * scale,
            ParameterName.axis_tick_label_distance: 0.007 * scale
            # ParameterName.axis_tick_label_distance: 0.02 * scale
        })

        (
            data_matrix, data_lim_pair, data_value_text_format, analyzed_set_size_list, selected_min_loss_size_list
        ) = raw_model_data.return_heatmap_data(**figure_data_parameter_dict)
        # x_label_list = r'$\mathbf{n}$'
        # y_label_list = r'$\mathbf{m}$'
        x_label_list = CommonFigureString.optimization_size_n
        y_label_list = CommonFigureString.selection_size_m
        x_tick_labels_list = analyzed_set_size_list
        y_tick_labels_list = selected_min_loss_size_list

        figure_config_dict = {
            ParameterName.x_label_format_dict: x_label_format_dict,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.y_label_format_dict: y_label_format_dict,
            ParameterName.y_tick_label_format_dict: y_tick_label_format_dict,
            ParameterName.data_value_text_format_dict: {
                ParameterName.font_size: 5,
                ParameterName.z_order: DataFigureConfig.figure_text_z_order,
                ParameterName.basic_number_format_str: data_value_text_format
            },
            ParameterName.im_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
            }
        }
        if cbar:
            assert cbar_bottom_left is not None
            assert cbar_size is not None
            assert cbar_figure_data_parameter_dict is not None
            axis_ticks = raw_model_heatmap_cbar_axis_label_dict(
                data_lim_pair=data_lim_pair, data_matrix=data_matrix, **figure_data_parameter_dict)
            cbar_figure_data_parameter_dict.update({
                ParameterName.x_ticks_list: axis_ticks,
                ParameterName.percentage: data_value_text_format == HeatmapValueFormat.percentage_format
            })
            cbar_config = {
                ParameterName.bottom_left: cbar_bottom_left,
                ParameterName.size: cbar_size,
                ParameterName.scale: scale,
                ParameterName.figure_data_parameter_dict: cbar_figure_data_parameter_dict,
                ParameterName.cbar_class: DistanceAnalysisColorBarDataFigure,
            }
        else:
            cbar_config = None
        if highlight:
            highlight_config = heatmap_highlight_ellipse_parameter(**figure_data_parameter_dict)
        else:
            highlight_config = None

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_total_bottom_left,
            ParameterName.ax_size_list: ax_total_size,
            ParameterName.heatmap_cmap: HeatmapConfig.common_heatmap_cmap,
            ParameterName.data_nested_list: data_matrix,
            ParameterName.figure_config_dict: figure_config_dict,
            ParameterName.data_lim_pair: data_lim_pair,

            ParameterName.x_label_list: x_label_list,
            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_label_list: y_label_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,

            ParameterName.cbar: cbar,
            ParameterName.cbar_config: cbar_config,

            ParameterName.highlight: highlight,
            ParameterName.highlight_config: highlight_config,

            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)


def raw_model_heatmap_cbar_axis_label_dict(
        data_matrix, data_lim_pair, data_name, figure_class, flux_name=None, mean_or_std=ParameterName.mean, **kwargs):
    total_dict = {
        DataName.raw_model_all_data: {
            ParameterName.net_euclidean_distance: {
                None: {
                    ParameterName.mean: np.arange(0, 400.1, 100),
                    ParameterName.std: np.arange(0, 120.1, 20),
                },
            },
            ParameterName.flux_relative_distance: {
                'FBA_c_FBA_c__R': {
                    ParameterName.mean: np.arange(-0.4, 0.41, 0.2),
                    ParameterName.std: np.arange(0, 0.081, 0.02),
                },
                'CS_m': {
                    ParameterName.mean: np.arange(-0.3, 0.31, 0.1),
                    ParameterName.std: np.arange(0, 0.351, 0.05),
                },
            },
        },
        DataName.raw_model_raw_data: {
            ParameterName.net_euclidean_distance: {
                None: {
                    ParameterName.mean: np.arange(0, 500.1, 100),
                    ParameterName.std: np.arange(0, 120.1, 20),
                },
            },
            ParameterName.flux_relative_distance: {
                'FBA_c_FBA_c__R': {
                    ParameterName.mean: np.arange(-0.5, 0.51, 0.25),
                    ParameterName.std: np.arange(0, 0.141, 0.02),
                },
                'CS_m': {
                    ParameterName.mean: np.arange(-0.2, 0.21, 0.1),
                    ParameterName.std: np.arange(0, 0.31, 0.05),
                },
            },
        },
    }
    lower_data_lim = data_lim_pair[0]
    if lower_data_lim is None:
        lower_data_lim = np.nanmin(data_matrix)
    upper_data_lim = data_lim_pair[1]
    if upper_data_lim is None:
        upper_data_lim = np.nanmax(data_matrix)
    try:
        target_axis_label = total_dict[data_name][figure_class][flux_name][mean_or_std]
    except KeyError:
        data_range = upper_data_lim - lower_data_lim
        if data_range < 0.06:
            data_interval = 0.01
        elif data_range <= 0.1:
            data_interval = 0.02
        elif data_range <= 0.18:
            data_interval = 0.025
        elif data_range <= 0.3:
            data_interval = 0.05
        elif data_range <= 0.7:
            data_interval = 0.1
        elif data_range <= 1:
            data_interval = 0.2
        elif data_range <= 1.8:
            data_interval = 0.25
        else:
            raise ValueError(f'Data range: {data_range}')
        negative_side_axis_label = np.arange(0, lower_data_lim, -data_interval)[::-1]
        positive_side_axis_label = np.arange(0, upper_data_lim, data_interval)
        if len(negative_side_axis_label) > 0:
            target_axis_label = np.concatenate([negative_side_axis_label[:-1], positive_side_axis_label])
        else:
            target_axis_label = positive_side_axis_label
        # if mean_or_std == ParameterName.mean:
        #     target_axis_label = np.arange(-0.5, 0.101, 0.25)
        # elif mean_or_std == ParameterName.std:
        #     target_axis_label = np.arange(0, 0.31, 0.05)
        # else:
        #     raise ValueError()
    axis_label_filter = np.ones_like(target_axis_label, dtype=bool)
    axis_label_filter &= target_axis_label >= lower_data_lim
    axis_label_filter &= target_axis_label <= upper_data_lim
    target_axis_label = target_axis_label[axis_label_filter]
    return target_axis_label


class SensitivityAnalysisHeatmapDataFigure(HeatmapDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            cbar=False, cbar_figure_data_parameter_dict=None, cbar_bottom_left: Vector = None,
            cbar_size: Vector = None, scale=1, **kwargs):
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        x_tick_label_format_dict = {
            **DataFigureConfig.flux_x_tick_format_dict,
            ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_tick_label_font_size + 1),
        }
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_format_dict_generator()
        y_tick_label_format_dict.update({
            ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_tick_label_font_size + 2),
            ParameterName.width: 0.08,
            ParameterName.height: 0.015,
            ParameterName.axis_tick_label_distance: 0.008,
            ParameterName.text_box: False,
        })
        common_tick_separator_format_dict = {
            ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio,
        }
        x_tick_separator_format_dict = {
            **DataFigureConfig.flux_x_tick_separator_format_dict,
        }
        y_tick_separator_format_dict = {
            **common_tick_separator_format_dict,
            ParameterName.axis_line_start_distance: 0,
            # ParameterName.axis_line_end_distance: 0.1,
            ParameterName.axis_line_end_distance: 0.2,
        }
        major_y_tick_separator_format_dict = {
            **y_tick_separator_format_dict,
            # ParameterName.axis_line_end_distance: 0.17,
            ParameterName.axis_line_end_distance: 0.35,
        }
        x_tick_separator_label_format_dict = {
            **DataFigureConfig.flux_x_tick_separator_label_format_dict,
            ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_label_font_size - 1),
        }
        y_tick_separator_label_format_dict = {
            **DataFigureConfig.flux_x_tick_separator_label_format_dict,
            ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_label_font_size - 1),
            ParameterName.axis_label_distance: 0.11,
        }
        major_y_tick_separator_label_format_dict = {
            **y_tick_separator_label_format_dict,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.axis_label_distance: 0.24,
            ParameterName.font_size: HeatmapConfig.sensitivity_x_y_label_font_size,
            ParameterName.line_space: 1.5,
        }

        (
            data_matrix, common_flux_name_list, result_label_list
        ) = all_fluxes_relative_error_data.return_data(**figure_data_parameter_dict)
        data_lim_pair, axis_ticks = sensitivity_heatmap_cbar_axis_label_dict(**figure_data_parameter_dict)
        (
            y_tick_labels_list, minor_group_separator_location_array, minor_group_name_location_array,
            minor_group_name_list, major_group_separator_location_array, major_group_name_location_array,
            major_group_name_list,
        ) = sensitivity_heatmap_y_axis_labels_generator(
            result_label_list=result_label_list, **figure_data_parameter_dict)
        (
            x_tick_labels_list, pathway_separator_location_array, pathway_name_location_array, pathway_name_list
        ) = net_flux_x_axis_labels_generator(common_flux_name_list)

        if major_group_separator_location_array is None:
            group_separator_location_array = minor_group_separator_location_array
        elif minor_group_separator_location_array is None:
            group_separator_location_array = major_group_separator_location_array
            y_tick_separator_format_dict = major_y_tick_separator_format_dict
        else:
            group_separator_location_array = np.concatenate(
                [minor_group_separator_location_array, major_group_separator_location_array])
            new_y_tick_separator_format_dict = []
            for _ in minor_group_separator_location_array:
                new_y_tick_separator_format_dict.append(dict(y_tick_separator_format_dict))
            for _ in major_group_separator_location_array:
                new_y_tick_separator_format_dict.append(dict(major_y_tick_separator_format_dict))
            y_tick_separator_format_dict = new_y_tick_separator_format_dict
        if major_group_name_location_array is None:
            group_name_location_array = minor_group_name_location_array
            group_name_list = minor_group_name_list
        elif minor_group_name_location_array is None:
            group_name_location_array = major_group_name_location_array
            group_name_list = major_group_name_list
            y_tick_separator_label_format_dict = major_y_tick_separator_label_format_dict
        else:
            group_name_location_array = np.concatenate(
                [minor_group_name_location_array, major_group_name_location_array])
            group_name_list = [*minor_group_name_list, *major_group_name_list]
            new_y_tick_separator_label_format_dict = []
            for _ in minor_group_name_location_array:
                new_y_tick_separator_label_format_dict.append(dict(y_tick_separator_label_format_dict))
            for _ in major_group_name_location_array:
                new_y_tick_separator_label_format_dict.append(dict(major_y_tick_separator_label_format_dict))
            y_tick_separator_label_format_dict = new_y_tick_separator_label_format_dict

        figure_config_dict = {
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.y_tick_label_format_dict: y_tick_label_format_dict,
            ParameterName.im_param_dict: {
                ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
            },
            ParameterName.x_tick_separator_format_dict: x_tick_separator_format_dict,
            ParameterName.y_tick_separator_format_dict: y_tick_separator_format_dict,
            ParameterName.x_tick_separator_label_format_dict: x_tick_separator_label_format_dict,
            ParameterName.y_tick_separator_label_format_dict: y_tick_separator_label_format_dict,
        }

        tick_separator_dict = {
            ParameterName.x_tick_separator_locs: pathway_separator_location_array,
            ParameterName.x_tick_separator_labels: pathway_name_list,
            ParameterName.x_tick_separator_label_locs: pathway_name_location_array,
            ParameterName.y_tick_separator_locs: group_separator_location_array,
            ParameterName.y_tick_separator_labels: group_name_list,
            ParameterName.y_tick_separator_label_locs: group_name_location_array,
        }
        if cbar:
            assert cbar_bottom_left is not None
            assert cbar_size is not None
            assert cbar_figure_data_parameter_dict is not None
            cbar_figure_data_parameter_dict.update({
                # ParameterName.x_label_list: 'Relative error',
                ParameterName.x_label_list: CommonFigureString.relative_error,
                ParameterName.x_ticks_list: axis_ticks,
                ParameterName.percentage: True,
                ParameterName.figure_config_dict: {
                    ParameterName.x_tick_label_format_dict: {
                        ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_tick_label_font_size + 3),
                        ParameterName.axis_tick_label_distance: 0.008,
                    },
                    ParameterName.x_label_format_dict: {
                        ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_label_font_size + 1),
                        ParameterName.axis_label_distance: 0.026,
                    },
                }
            })
            cbar_config = {
                ParameterName.bottom_left: cbar_bottom_left,
                ParameterName.size: cbar_size,
                ParameterName.scale: scale,
                ParameterName.figure_data_parameter_dict: cbar_figure_data_parameter_dict,
                ParameterName.cbar_class: DistanceAnalysisColorBarDataFigure,
            }
        else:
            cbar_config = None

        figure_data_parameter_dict = {
            ParameterName.ax_bottom_left_list: ax_total_bottom_left,
            ParameterName.ax_size_list: ax_total_size,
            ParameterName.heatmap_cmap: HeatmapConfig.common_heatmap_cmap,
            ParameterName.data_nested_list: data_matrix,
            ParameterName.figure_config_dict: figure_config_dict,
            ParameterName.data_lim_pair: data_lim_pair,

            ParameterName.x_tick_labels_list: x_tick_labels_list,
            ParameterName.y_tick_labels_list: y_tick_labels_list,
            ParameterName.tick_separator_dict_list: tick_separator_dict,

            ParameterName.cbar: cbar,
            ParameterName.cbar_config: cbar_config,

            **figure_data_parameter_dict
        }
        super().__init__(figure_data_parameter_dict, bottom_left, size, scale=scale, **kwargs)
