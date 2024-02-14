from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import heat_map_plotting, cbar_plotting, HeatmapValueFormat
from .config import DataFigureConfig, ParameterName, Vector, Ellipse, Keywords, ColorConfig, \
    merge_axis_format_dict, default_parameter_extract, HorizontalAlignment, VerticalAlignment


class HeatmapConfig(object):
    # common_heatmap_cmap = 'coolwarm'
    common_heatmap_cmap = ColorConfig.my_color_map
    cbar_orientation = ParameterName.horizontal

    distance_x_y_label_font_size = 10
    distance_x_y_tick_label_font_size = 7
    sensitivity_x_y_label_font_size = 11
    sensitivity_x_y_tick_label_font_size = 7
    HeatmapValueFormat = HeatmapValueFormat


def cbar_generator(cbar_config_dict):
    area_bottom_left = cbar_config_dict[ParameterName.bottom_left]
    area_size = cbar_config_dict[ParameterName.size]
    figure_data_parameter_dict = cbar_config_dict[ParameterName.figure_data_parameter_dict]
    scale = cbar_config_dict[ParameterName.scale]
    cbar_class = cbar_config_dict[ParameterName.cbar_class]
    return figure_data_parameter_dict, area_bottom_left, area_size, scale, cbar_class


def hidden_axis(
        axis_format_dict, axis_tick_format_dict, hidden_axis_tick=False, hidden_axis_boundary=False):
    if hidden_axis_tick or hidden_axis_boundary:
        axis_tick_format_dict.update({
            ParameterName.edge_width: 0,
            ParameterName.axis_tick_length: 0
        })
        if hidden_axis_boundary:
            axis_format_dict[ParameterName.edge_width] = 0


class ColorBarDataFigure(DataFigure):
    def __init__(self, figure_data_parameter_dict, bottom_left: Vector, size: Vector, scale=1, **kwargs):
        self.figure_data_parameter_dict = figure_data_parameter_dict
        self.cbar_orientation = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.cbar_orientation, HeatmapConfig.cbar_orientation, pop=True)
        self.cmap_mapper = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.cmap_mapper, None, pop=True)
        new_figure_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_config_dict, {}, pop=True)

        ax_total_bottom_left, ax_total_size = default_parameter_extract(
            figure_data_parameter_dict,
            [ParameterName.ax_total_bottom_left, ParameterName.ax_total_size],
            [Vector(0, 0), Vector(1, 1)])

        (
            axis_format_dict, axis_tick_format_dict, axis_label_format_dict
        ) = DataFigureConfig.common_axis_param_dict_generator(scale)
        hidden_axis_tick = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.hidden_axis_tick, False)
        hidden_axis_boundary = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.hidden_axis_boundary, False)
        hidden_axis(axis_format_dict, axis_tick_format_dict, hidden_axis_tick, hidden_axis_boundary)

        self.x_ticks = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.x_ticks_list, Keywords.default, pop=True)
        self.x_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.x_tick_labels_list, Keywords.default, pop=True)
        self.x_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.x_label_list, None, pop=True)
        self.top_x_tick_labels = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.top_x_tick_labels_list, None, pop=True)
        self.top_x_label = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.top_x_label_list, None, pop=True)
        x_label_format_dict = merge_axis_format_dict(
            axis_label_format_dict, DataFigureConfig.x_label_format_dict_generator(scale),
            new_figure_config_dict, ParameterName.x_label_format_dict)
        top_x_label_format_dict = merge_axis_format_dict(
            {}, x_label_format_dict,
            new_figure_config_dict, ParameterName.top_x_label_format_dict)
        x_tick_label_format_dict = merge_axis_format_dict(
            axis_label_format_dict, DataFigureConfig.x_tick_label_format_dict_generator(scale),
            new_figure_config_dict, ParameterName.x_tick_label_format_dict)
        top_x_tick_label_format_dict = merge_axis_format_dict(
            {}, x_tick_label_format_dict,
            new_figure_config_dict, ParameterName.top_x_tick_label_format_dict)
        figure_config_dict = {
            ParameterName.x_label_format_dict: x_label_format_dict,
            ParameterName.top_x_label_format_dict: top_x_label_format_dict,
            ParameterName.x_tick_label_format_dict: x_tick_label_format_dict,
            ParameterName.top_x_tick_label_format_dict: top_x_tick_label_format_dict,
        }

        super().__init__(
            bottom_left, size, [ax_total_bottom_left], [ax_total_size],
            axis_spine_format_dict=axis_format_dict, axis_tick_format_dict=axis_tick_format_dict,
            figure_config_dict=figure_config_dict, scale=scale, background=False, **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None, mapped_image=None):
        if mapped_image is None:
            if self.cmap_mapper is not None:
                mapped_image = self.cmap_mapper
            else:
                """Prevent be drawn independently"""
                return None
        ((data_figure_axis, data_figure_transform),) = super().draw(fig, parent_ax, parent_transformation)
        cbar_plotting(
            data_figure_axis, data_figure_transform, mapped_image, self.cbar_orientation,
            x_label=self.x_label, x_ticks=self.x_ticks, x_tick_labels=self.x_tick_labels,
            top_x_label=self.top_x_label, top_x_tick_labels=self.top_x_tick_labels, **self.figure_config_dict)


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
        hidden_axis_tick = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.hidden_axis_tick, False)
        hidden_axis_boundary = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.hidden_axis_boundary, False)
        hidden_axis(axis_format_dict, axis_tick_format_dict, hidden_axis_tick, hidden_axis_boundary)

        figure_config_dict = {
            **{
                key: new_figure_config_dict[key] for key in [
                    ParameterName.im_param_dict, ParameterName.data_value_text_format_dict,
                    ParameterName.x_tick_separator_format_dict, ParameterName.x_tick_separator_label_format_dict,
                    ParameterName.y_tick_separator_format_dict, ParameterName.y_tick_separator_label_format_dict,
                ] if key in new_figure_config_dict
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_format_dict_generator(scale),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }
        figure_config_dict.update({
            ParameterName.top_x_label_format_dict: merge_axis_format_dict(
                figure_config_dict[ParameterName.x_label_format_dict], {},
                new_figure_config_dict, ParameterName.top_x_label_format_dict),
            ParameterName.top_x_tick_label_format_dict: merge_axis_format_dict(
                figure_config_dict[ParameterName.x_tick_label_format_dict], {
                    ParameterName.horizontal_alignment: HorizontalAlignment.left
                },
                new_figure_config_dict, ParameterName.top_x_tick_label_format_dict),
            ParameterName.right_y_label_format_dict: merge_axis_format_dict(
                figure_config_dict[ParameterName.y_label_format_dict], {},
                new_figure_config_dict, ParameterName.right_y_label_format_dict),
            ParameterName.right_y_tick_label_format_dict: merge_axis_format_dict(
                figure_config_dict[ParameterName.y_tick_label_format_dict], {
                    ParameterName.horizontal_alignment: HorizontalAlignment.left
                },
                new_figure_config_dict, ParameterName.right_y_tick_label_format_dict),
        })

        (
            self.x_label,
            self.x_tick_labels_list,
            self.y_label,
            self.y_tick_labels_list,
            self.top_x_label,
            self.top_x_tick_labels_list,
            self.right_y_label,
            self.right_y_tick_labels_list,
        ) = [
            figure_data_parameter_dict[key]
            if key in figure_data_parameter_dict and figure_data_parameter_dict[key] is not None
            else None
            for key in (
                ParameterName.x_label_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_label_list,
                ParameterName.y_tick_labels_list,
                ParameterName.top_x_label_list,
                ParameterName.top_x_tick_labels_list,
                ParameterName.right_y_label_list,
                ParameterName.right_y_tick_labels_list,
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
            top_x_label=self.top_x_label, right_y_label=self.right_y_label,
            top_x_tick_labels=self.top_x_tick_labels_list, right_y_tick_labels=self.right_y_tick_labels_list,
            cmap=self.heatmap_cmap, **self.tick_separator_dict)
        if self.cbar:
            self.cbar_obj.draw(fig, parent_ax, parent_transformation, mapped_image=heatmap_image)
        if self.highlight:
            self.highlight_obj.draw(fig, data_figure_axis, data_figure_axis.transData)

