from .config import DataFigureConfig, ParameterName, Vector, move_and_scale_for_dict, \
    merge_axis_format_dict, it, common_legend_generator, default_parameter_extract
from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import draw_text_by_axis_loc, single_scatter_plotting

GroupDataFigure = DataFigureConfig.GroupDataFigure
scatter_line_diagram_str = 'scatter_line_diagram'


class BasicScatterDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        new_figure_config_dict = figure_data_parameter_dict[ParameterName.figure_config_dict]
        (
            ax_bottom_left_list,
            ax_size_list,
            color_dict,
            self.complete_data_dict_list,
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.color_dict,
            ParameterName.data_nested_list,
        ]]
        self.complete_scatter_line_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.scatter_line, it.repeat(None))

        (
            axis_format_dict, axis_tick_format_dict,
            axis_label_format_dict) = DataFigureConfig.common_axis_param_dict_generator()
        figure_config_dict = {
            **{
                key: new_figure_config_dict[key] if key in new_figure_config_dict else {}
                for key in [
                    ParameterName.cutoff_param_dict, ParameterName.subplot_name_text_format_dict,
                    ParameterName.error_bar_param_dict, ParameterName.scatter_param_dict,
                    ParameterName.line_param_dict, ParameterName.supplementary_text_format_dict,
                ]
            },
            ParameterName.x_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.x_label_format_dict),
            ParameterName.x_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.x_tick_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.x_tick_label_format_dict),
            ParameterName.y_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.y_label_format_dict),
            ParameterName.y_tick_label_format_dict: merge_axis_format_dict(
                axis_label_format_dict, DataFigureConfig.y_tick_label_format_dict_generator(),
                new_figure_config_dict, ParameterName.y_tick_label_format_dict),
        }

        (
            self.emphasized_flux_list,
            self.subplot_name_list,
            self.text_axis_loc_pair,
        ) = [
            figure_data_parameter_dict[key] if key in figure_data_parameter_dict else None
            for key in (
                ParameterName.emphasized_flux_list,
                ParameterName.subplot_name_list,
                ParameterName.text_axis_loc_pair,
            )]
        self.supplementary_text_list, self.supplementary_text_loc_list = default_parameter_extract(
            figure_data_parameter_dict, [
                ParameterName.supplementary_text_list,
                ParameterName.supplementary_text_loc_list,
            ], None, repeat_default_value=True)

        (
            self.cutoff_value_list,
            self.x_lim_list,
            self.x_label_list,
            self.x_ticks_list,
            self.x_tick_labels_list,
            self.y_lim_list,
            self.y_label_list,
            self.y_ticks_list,
            self.y_tick_labels_list,
            self.figure_type
        ) = [
            figure_data_parameter_dict[key]
            if key in figure_data_parameter_dict and figure_data_parameter_dict[key] is not None
            else it.repeat(None)
            for key in (
                ParameterName.cutoff,
                ParameterName.x_lim_list,
                ParameterName.x_label_list,
                ParameterName.x_ticks_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_lim_list,
                ParameterName.y_label_list,
                ParameterName.y_ticks_list,
                ParameterName.y_tick_labels_list,
                ParameterName.figure_type
            )]
        self.error_bar = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.error_bar, False)

        if ParameterName.legend in figure_data_parameter_dict:
            legend = figure_data_parameter_dict[ParameterName.legend]
        else:
            legend = False
        if legend:
            legend_config_dict = figure_data_parameter_dict[ParameterName.legend_config_dict]
            legend_obj = common_legend_generator(legend_config_dict, color_dict)
        else:
            legend_obj = None

        super().__init__(
            bottom_left, size, ax_bottom_left_list, ax_size_list,
            axis_spine_format_dict=axis_format_dict, axis_tick_format_dict=axis_tick_format_dict,
            figure_config_dict=figure_config_dict, legend_obj=legend_obj, scale=scale,
            bottom_left_offset=bottom_left_offset, base_z_order=base_z_order, z_order_increment=z_order_increment,
            **kwargs)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        ax_and_transform_list = super().draw(fig, parent_ax, parent_transformation)
        for (
                complete_data_dict, (current_ax, current_transform), x_lim, x_label, x_ticks, x_tick_labels, y_lim,
                y_label, y_ticks, y_tick_labels, cutoff_value, scatter_line) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.x_lim_list, self.x_label_list,
                self.x_ticks_list, self.x_tick_labels_list, self.y_lim_list, self.y_label_list, self.y_ticks_list,
                self.y_tick_labels_list, self.cutoff_value_list, self.complete_scatter_line_list):
            single_scatter_plotting(
                current_ax, current_transform, complete_data_dict, x_lim=x_lim, x_ticks=x_ticks, x_label=x_label,
                x_tick_labels=x_tick_labels, y_lim=y_lim, y_ticks=y_ticks,
                y_label=y_label, y_tick_labels=y_tick_labels, cutoff_value=cutoff_value,
                scatter_line=scatter_line, error_bar=self.error_bar, **self.figure_config_dict)
        if self.subplot_name_list is not None:
            for subplot_name, (current_ax, current_transform) in zip(self.subplot_name_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, subplot_name, self.text_axis_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.subplot_name_text_format_dict])
        if self.supplementary_text_list is not None:
            for supplementary_text, supplementary_loc, (current_ax, current_transform) in zip(
                    self.supplementary_text_list, self.supplementary_text_loc_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, supplementary_text, supplementary_loc, current_transform,
                    **self.figure_config_dict[ParameterName.supplementary_text_format_dict])

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        super().move_and_scale(
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)
        for data_dict in self.complete_data_dict_list:
            if isinstance(data_dict, dict):
                move_and_scale_for_dict(data_dict, scale=scale)
            elif isinstance(data_dict, list):
                for each_data_dict in data_dict:
                    move_and_scale_for_dict(each_data_dict, scale=scale)
            else:
                raise ValueError()
        for scatter_line in self.complete_scatter_line_list:
            if scatter_line is not None:
                for _, _, *detailed_line_param_dict in scatter_line:
                    if len(detailed_line_param_dict) > 0:
                        move_and_scale_for_dict(detailed_line_param_dict[0], scale=scale)
        pass


def common_figure_config_dict_generator(axis_label_format_dict, scale=1):
    return {
        ParameterName.x_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.x_label_format_dict_generator(scale),
        },
        ParameterName.x_tick_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.x_tick_label_format_dict_generator(scale),
        },
        ParameterName.y_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.y_label_format_dict_generator(scale),
            ParameterName.axis_label_distance: 0.03 * scale,
        },
        ParameterName.y_tick_label_format_dict: {
            **axis_label_format_dict,
            **DataFigureConfig.y_tick_label_format_dict_generator(scale),
        },
        ParameterName.scatter_param_dict: {
            ParameterName.z_order: DataFigureConfig.normal_figure_element_z_order
        }
    }

