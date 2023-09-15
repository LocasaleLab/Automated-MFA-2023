from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import heat_map_plotting, cbar_plotting, HeatmapValueFormat
from .figure_data_loader import raw_model_data, all_fluxes_relative_error_data
from ..config import np, DataFigureConfig, ParameterName, Vector, Ellipse, HorizontalAlignment, VerticalAlignment, \
    FontWeight, Keywords, ColorConfig, merge_axis_format_dict, raw_model_heatmap_cbar_axis_label_dict, \
    sensitivity_heatmap_cbar_axis_label_dict, heatmap_highlight_ellipse_parameter, \
    sensitivity_heatmap_y_axis_labels_generator, sensitivity_heatmap_x_axis_labels_generator, \
    default_parameter_extract, CommonFigureString, DataName


class HeatmapConfig(object):
    # common_heatmap_cmap = 'coolwarm'
    common_heatmap_cmap = ColorConfig.my_color_map
    cbar_orientation = ParameterName.horizontal

    distance_x_y_label_font_size = 10
    distance_x_y_tick_label_font_size = 7
    sensitivity_x_y_label_font_size = 11
    sensitivity_x_y_tick_label_font_size = 7


def cbar_generator(cbar_config_dict):
    area_bottom_left = cbar_config_dict[ParameterName.bottom_left]
    area_size = cbar_config_dict[ParameterName.size]
    figure_data_parameter_dict = cbar_config_dict[ParameterName.figure_data_parameter_dict]
    scale = cbar_config_dict[ParameterName.scale]
    cbar_class = cbar_config_dict[ParameterName.cbar_class]
    return figure_data_parameter_dict, area_bottom_left, area_size, scale, cbar_class


class ColorBarDataFigure(DataFigure):
    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, scale=1, **kwargs):
        self.figure_data_parameter_dict = figure_data_parameter_dict
        try:
            ax_total_bottom_left = figure_data_parameter_dict[ParameterName.ax_total_bottom_left]
        except KeyError:
            ax_total_bottom_left = Vector(0, 0)
        try:
            ax_total_size = figure_data_parameter_dict[ParameterName.ax_total_size]
        except KeyError:
            ax_total_size = Vector(1, 1)
        try:
            cbar_orientation = figure_data_parameter_dict[ParameterName.cbar_orientation]
        except KeyError:
            cbar_orientation = HeatmapConfig.cbar_orientation
        self.cbar_orientation = cbar_orientation
        try:
            new_figure_config_dict = figure_data_parameter_dict[ParameterName.figure_config_dict]
        except KeyError:
            new_figure_config_dict = {}
        try:
            x_ticks = figure_data_parameter_dict[ParameterName.x_ticks_list]
        except KeyError:
            x_ticks = Keywords.default
        try:
            x_label = figure_data_parameter_dict[ParameterName.x_label_list]
        except KeyError:
            x_label = None

        (
            axis_format_dict, axis_tick_format_dict, axis_label_format_dict
        ) = DataFigureConfig.common_axis_param_dict_generator(scale)

        self.x_ticks = x_ticks
        self.x_tick_labels = Keywords.default
        self.x_label = x_label
        figure_config_dict = {
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
        }

        super().__init__(
            bottom_left, size, [ax_total_bottom_left], [ax_total_size],
            axis_spine_format_dict=axis_format_dict, axis_tick_format_dict=axis_tick_format_dict,
            figure_config_dict=figure_config_dict, scale=scale, background=False, **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None, mapped_image=None):
        if mapped_image is None:
            """Prevent be drawn independently"""
            return None
        ((data_figure_axis, data_figure_transform),) = super().draw(fig, parent_ax, parent_transformation)
        cbar_plotting(
            data_figure_axis, data_figure_transform, mapped_image, self.cbar_orientation,
            x_label=self.x_label, x_ticks=self.x_ticks, x_tick_labels=self.x_tick_labels, **self.figure_config_dict)


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


class BasicHeatmapDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector = None, size: Vector = None, scale=1, **kwargs):
        self.figure_data_parameter_dict = figure_data_parameter_dict
        (
            main_ax_bottom_left,
            main_ax_size,
            self.heatmap_cmap,
            self.data_matrix,
            self.data_lim_pair,
            new_figure_config_dict,
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.heatmap_cmap,
            ParameterName.data_nested_list,
            ParameterName.data_lim_pair,
            ParameterName.figure_config_dict,
        ]]

        (
            axis_format_dict, axis_tick_format_dict, axis_label_format_dict
        ) = DataFigureConfig.common_axis_param_dict_generator(scale)
        figure_config_dict = {
            **{
                key: new_figure_config_dict[key] for key in [
                    ParameterName.im_param_dict, ParameterName.data_value_text_format_dict,
                    ParameterName.x_tick_separator_format_dict, ParameterName.x_tick_separator_label_format_dict,
                    ParameterName.y_tick_separator_format_dict, ParameterName.y_tick_separator_label_format_dict,
                ] if key in new_figure_config_dict
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_width_height_distance_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }

        (
            self.x_label,
            self.x_tick_labels_list,
            self.y_label,
            self.y_tick_labels_list,
        ) = [
            figure_data_parameter_dict[key]
            if key in figure_data_parameter_dict and figure_data_parameter_dict[key] is not None
            else None
            for key in (
                ParameterName.x_label_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_label_list,
                ParameterName.y_tick_labels_list,
            )]

        self.tick_separator_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.tick_separator_dict_list, {})

        if ParameterName.cbar in figure_data_parameter_dict:
            cbar = figure_data_parameter_dict[ParameterName.cbar]
        else:
            cbar = False
        self.cbar = cbar
        if cbar:
            cbar_config_dict = figure_data_parameter_dict[ParameterName.cbar_config]
            (
                cbar_figure_data_parameter_dict, cbar_area_bottom_left, cbar_area_size, cbar_scale,
                cbar_class) = cbar_generator(cbar_config_dict)
            self.cbar_obj = cbar_class(
                cbar_figure_data_parameter_dict, bottom_left=cbar_area_bottom_left, size=cbar_area_size,
                scale=cbar_scale)
        else:
            self.cbar_obj = None
        if ParameterName.highlight in figure_data_parameter_dict:
            highlight = figure_data_parameter_dict[ParameterName.highlight]
        else:
            highlight = False
        self.highlight = highlight
        self.highlight_obj = None
        if highlight:
            highlight_config_dict = figure_data_parameter_dict[ParameterName.highlight_config]
            self.highlight_obj = Ellipse(**highlight_config_dict)

        super().__init__(
            bottom_left, size, [main_ax_bottom_left], [main_ax_size],
            axis_spine_format_dict=axis_format_dict, axis_tick_format_dict=axis_tick_format_dict,
            figure_config_dict=figure_config_dict, color_bar_obj=self.cbar_obj,
            scale=scale, **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        # *_, ax_and_transform_list, _ = super().draw(fig, parent_ax, parent_transformation)
        ((data_figure_axis, data_figure_transform),) = super().draw(fig, parent_ax, parent_transformation)
        # The tick_separator_dict must be written to this format since tick separator format dict must be included in
        # self.figure_config_dict to keep scale.
        heatmap_image = heat_map_plotting(
            data_figure_axis, data_figure_transform, self.data_matrix,
            self.x_tick_labels_list, self.y_tick_labels_list, self.data_lim_pair,
            figure_config_dict=self.figure_config_dict, x_label=self.x_label, y_label=self.y_label,
            cmap=self.heatmap_cmap, **self.tick_separator_dict)
        if self.cbar:
            self.cbar_obj.draw(fig, parent_ax, parent_transformation, mapped_image=heatmap_image)
        if self.highlight:
            self.highlight_obj.draw(fig, data_figure_axis, data_figure_axis.transData)


class DistanceFluxAnalysisHeatmapDataFigure(BasicHeatmapDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            cbar=False, cbar_figure_data_parameter_dict=None, cbar_bottom_left: Vector = None,
            cbar_size: Vector = None, highlight=False, scale=1, **kwargs):
        # ax_total_bottom_left = Vector(0.1, 0.1)
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        x_label_format_dict = DataFigureConfig.x_label_width_height_distance_dict_generator(scale)
        x_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_label_font_size * scale,
            ParameterName.axis_label_distance: 0.02 * scale,
        })
        x_tick_label_format_dict = DataFigureConfig.x_tick_label_width_height_distance_dict_generator(scale)
        x_tick_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_tick_label_font_size * scale,
            ParameterName.axis_tick_label_distance: 0.006 * scale
            # ParameterName.axis_tick_label_distance: 0.02 * scale
        })
        y_label_format_dict = DataFigureConfig.y_label_width_height_distance_dict_generator(scale)
        y_label_format_dict.update({
            ParameterName.font_size: HeatmapConfig.distance_x_y_label_font_size * scale,
            ParameterName.axis_label_distance: 0.025 * scale,
        })
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_width_height_distance_dict_generator(scale)
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


class SensitivityAnalysisHeatmapDataFigure(BasicHeatmapDataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            cbar=False, cbar_figure_data_parameter_dict=None, cbar_bottom_left: Vector = None,
            cbar_size: Vector = None, scale=1, **kwargs):
        ax_total_bottom_left = Vector(0, 0)
        ax_total_size = Vector(1, 1) - ax_total_bottom_left
        # x_tick_label_format_dict = {
        #     ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_tick_label_font_size + 1),
        #     ParameterName.axis_tick_label_distance: 0.039,
        #     ParameterName.width: 0.08,
        #     ParameterName.height: 0.015,
        #     ParameterName.angle: -90,
        #     ParameterName.horizontal_alignment: HorizontalAlignment.left,
        #     ParameterName.vertical_alignment: HorizontalAlignment.center,
        #     ParameterName.text_box: False,
        # }
        x_tick_label_format_dict = {
            **DataFigureConfig.flux_x_tick_format_dict,
            ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_tick_label_font_size + 1),
        }
        y_tick_label_format_dict = DataFigureConfig.y_tick_label_width_height_distance_dict_generator()
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
        # x_tick_separator_format_dict = {
        #     **common_tick_separator_format_dict,
        #     ParameterName.axis_line_start_distance: 0,
        #     ParameterName.axis_line_end_distance: 0.055,
        # }
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
        # common_tick_separator_label_format_dict = {
        #     ParameterName.font_size: (HeatmapConfig.sensitivity_x_y_label_font_size - 1),
        #     ParameterName.width: 0.1,
        #     ParameterName.height: 0.02,
        #     ParameterName.horizontal_alignment: HorizontalAlignment.center,
        #     ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        # }
        # x_tick_separator_label_format_dict = {
        #     **common_tick_separator_label_format_dict,
        #     ParameterName.axis_label_distance: 0.12,
        # }
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
        ) = sensitivity_heatmap_x_axis_labels_generator(common_flux_name_list)

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
