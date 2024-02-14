from .config import DataFigureConfig, ParameterName, Vector, it, common_legend_generator, \
    default_parameter_extract
from .data_figure import DataFigure
from .data_figure_plotting_and_data_output_generator import single_histogram_plot, draw_text_by_axis_loc

GroupDataFigure = DataFigureConfig.GroupDataFigure


class BasicHistogramDataFigure(DataFigure):
    def __init__(
            self, figure_data_parameter_dict, bottom_left: Vector, size: Vector,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):

        new_figure_config_dict = figure_data_parameter_dict[ParameterName.figure_config_dict]
        (
            ax_bottom_left_list,
            ax_size_list,
            color_dict,
        ) = [figure_data_parameter_dict[key] for key in [
            ParameterName.ax_bottom_left_list,
            ParameterName.ax_size_list,
            ParameterName.color_dict,
        ]]

        # scale = figure_data_parameter_dict[ParameterName.scale]

        (
            self.complete_data_dict_list,
            self.cutoff,
            self.text_list,
        ) = [
            figure_data_parameter_dict[key] if key in figure_data_parameter_dict else None
            for key in (
                ParameterName.data_nested_list,
                ParameterName.cutoff,
                ParameterName.data_figure_text_list,
            )]

        (
            axis_format_dict, axis_tick_format_dict,
            axis_label_format_dict) = DataFigureConfig.common_axis_param_dict_generator(scale)
        text_config_dict = default_parameter_extract(new_figure_config_dict, ParameterName.text_config_dict, {})
        cutoff_param_dict = default_parameter_extract(new_figure_config_dict, ParameterName.cutoff_param_dict, {})
        figure_config_dict = {
            ParameterName.x_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.x_label_format_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.x_label_format_dict]
                    if ParameterName.x_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.x_tick_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.x_tick_label_format_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.x_tick_label_format_dict]
                    if ParameterName.x_tick_label_format_dict in new_figure_config_dict else {}),
            },
            ParameterName.y_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.y_label_format_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.y_label_format_dict]
                    if ParameterName.y_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.y_tick_label_format_dict: {
                **axis_label_format_dict,
                **DataFigureConfig.y_tick_label_format_dict_generator(scale),
                **(
                    new_figure_config_dict[ParameterName.y_tick_label_format_dict]
                    if ParameterName.y_tick_label_format_dict in new_figure_config_dict else {}
                ),
            },
            ParameterName.cutoff_param_dict: cutoff_param_dict,
            ParameterName.text_config_dict: text_config_dict,
        }

        (
            self.x_lim_list,
            self.x_label_list,
            self.x_ticks_list,
            self.x_tick_labels_list,
            self.y_lim_list,
            self.y_label_list,
            self.y_ticks_list,
            self.y_tick_labels_list,
        ) = [
            figure_data_parameter_dict[key]
            if key in figure_data_parameter_dict and figure_data_parameter_dict[key] is not None
            else it.repeat(None)
            for key in (
                ParameterName.x_lim_list,
                ParameterName.x_label_list,
                ParameterName.x_ticks_list,
                ParameterName.x_tick_labels_list,
                ParameterName.y_lim_list,
                ParameterName.y_label_list,
                ParameterName.y_ticks_list,
                ParameterName.y_tick_labels_list,
            )]

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
        pass

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        ax_and_transform_list = super().draw(fig, parent_ax, parent_transformation)
        for (
                complete_data_dict, (current_ax, current_transform), x_lim, x_label, x_ticks, x_tick_labels, y_lim,
                y_label, y_ticks, y_tick_labels) in zip(
                self.complete_data_dict_list, ax_and_transform_list, self.x_lim_list, self.x_label_list,
                self.x_ticks_list, self.x_tick_labels_list, self.y_lim_list, self.y_label_list, self.y_ticks_list,
                self.y_tick_labels_list):
            single_histogram_plot(
                current_ax, current_transform, complete_data_dict,
                cutoff=self.cutoff, x_lim=x_lim, x_label=x_label,
                x_ticks=x_ticks, x_tick_labels=x_tick_labels, y_lim=y_lim, y_label=y_label, y_ticks=y_ticks,
                y_tick_labels=y_tick_labels, figure_config_dict=self.figure_config_dict)
        if self.text_list is not None:
            for (text_content, text_loc_pair), (current_ax, current_transform) in zip(
                    self.text_list, ax_and_transform_list):
                draw_text_by_axis_loc(
                    current_ax, text_content, text_loc_pair, current_transform,
                    **self.figure_config_dict[ParameterName.text_config_dict])

