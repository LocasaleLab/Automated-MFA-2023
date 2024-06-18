from ..common.core_plotting_functions import heatmap_text_str_list_generator, \
    core_heatmap_plotting, axis_appearance_setting, core_scatter_plotting, core_single_ax_bar_plot, \
    core_plot_violin_box_plot, core_line_plotting, core_error_bar_plotting, \
    core_histogram_plotting, get_twin_axis_numeric_parameters, raw_cbar_plotting, core_cbar_plotting, \
    HeatmapValueFormat
from ..common.common_functions import round_to_str_with_fixed_point, default_parameter_extract
from .config import Rectangle, Line, Vector, ColorConfig, np, it, transforms, draw_text, clip_angle_to_normal_range
from .config import ParameterName, DataFigureConfig, VerticalAlignment, HorizontalAlignment, Keywords


def heat_map_plotting(
        current_ax, current_transform, data_matrix_with_nan, x_tick_labels, y_tick_labels, lim_pair,
        figure_config_dict, im_param_dict=None, cmap=None,
        x_label=None, y_label=None,
        x_tick_separator_locs=None, x_tick_separator_labels=None, x_tick_separator_label_locs=None,
        y_tick_separator_locs=None, y_tick_separator_labels=None, y_tick_separator_label_locs=None,
        top_x_label=None, right_y_label=None, top_x_tick_labels=None, right_y_tick_labels=None,
        top_x_tick_separator_locs=None, top_x_tick_separator_labels=None, top_x_tick_separator_label_locs=None,
        right_y_tick_separator_locs=None, right_y_tick_separator_labels=None, right_y_tick_separator_label_locs=None,
):
    min_value, max_value = lim_pair
    row_num, col_num = data_matrix_with_nan.shape
    # row_num = len(y_tick_labels)
    # col_num = len(x_tick_labels)
    basic_number_format_str = ParameterName.basic_number_format_str
    data_value_text_format_dict = default_parameter_extract(
        figure_config_dict, ParameterName.data_value_text_format_dict, None)

    if data_value_text_format_dict is not None:
        basic_number_format = data_value_text_format_dict[basic_number_format_str]
        other_text_format_dict = {
            key: value for key, value in data_value_text_format_dict.items() if key != basic_number_format_str}
        text_str_list = heatmap_text_str_list_generator(
            basic_number_format, data_matrix_with_nan, col_num, row_num,
            text_color=ColorConfig.heatmap_inner_text_color_pair, **other_text_format_dict)
    else:
        text_str_list = None
    heatmap_image = core_heatmap_plotting(
        current_ax, data_matrix_with_nan, cmap, min_value, max_value, col_num, row_num, im_param_dict=im_param_dict,
        text_str_list=text_str_list)

    (
        x_label_format_dict,
        x_tick_label_format_dict,
        y_label_format_dict,
        y_tick_label_format_dict,
        top_x_label_format_dict,
        top_x_tick_label_format_dict,
        right_y_label_format_dict,
        right_y_tick_label_format_dict,
    ) = default_parameter_extract(
        figure_config_dict, [
            ParameterName.x_label_format_dict,
            ParameterName.x_tick_label_format_dict,
            ParameterName.y_label_format_dict,
            ParameterName.y_tick_label_format_dict,
            ParameterName.top_x_label_format_dict,
            ParameterName.top_x_tick_label_format_dict,
            ParameterName.right_y_label_format_dict,
            ParameterName.right_y_tick_label_format_dict,
        ], None, repeat_default_value=True)

    draw_axis_tick_and_tick_separator_label(
        current_ax, current_transform, figure_config_dict,
        x_label, x_label_format_dict, x_tick_labels, x_tick_label_format_dict,
        y_label, y_label_format_dict, y_tick_labels, y_tick_label_format_dict,
        x_tick_separator_locs=x_tick_separator_locs, x_tick_separator_labels=x_tick_separator_labels,
        x_tick_separator_label_locs=x_tick_separator_label_locs,
        y_tick_separator_locs=y_tick_separator_locs, y_tick_separator_labels=y_tick_separator_labels,
        y_tick_separator_label_locs=y_tick_separator_label_locs)
    draw_axis_tick_and_tick_separator_label(
        current_ax, current_transform, figure_config_dict,
        top_x_label, top_x_label_format_dict, top_x_tick_labels, top_x_tick_label_format_dict,
        right_y_label, right_y_label_format_dict, right_y_tick_labels, right_y_tick_label_format_dict,
        x_tick_separator_locs=top_x_tick_separator_locs, x_tick_separator_labels=top_x_tick_separator_labels,
        x_tick_separator_label_locs=top_x_tick_separator_label_locs,
        y_tick_separator_locs=right_y_tick_separator_locs, y_tick_separator_labels=right_y_tick_separator_labels,
        y_tick_separator_label_locs=right_y_tick_separator_label_locs, opposite_axis=True)
    return heatmap_image


def cbar_plotting(
        current_ax, current_transform, mapped_image, cbar_orientation, z_order=None,
        x_label=None, x_label_format_dict=None, x_ticks=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_ticks=None, y_tick_labels=None, y_tick_label_format_dict=None,
        top_x_label=None, top_x_label_format_dict=None,
        top_x_ticks=None, top_x_tick_labels=None, top_x_tick_label_format_dict=None,
        right_y_label=None, right_y_label_format_dict=None,
        right_y_ticks=None, right_y_tick_labels=None, right_y_tick_label_format_dict=None,
):
    # cbar = raw_cbar_plotting(mapped_image, cbar_ax=current_ax, cbar_orientation=cbar_orientation)
    if cbar_orientation == ParameterName.horizontal:
        ticks = x_ticks
    elif cbar_orientation == ParameterName.vertical:
        ticks = y_ticks
    else:
        raise ValueError()
    core_cbar_plotting(current_ax, mapped_image, cbar_orientation=cbar_orientation, z_order=z_order, ticks=ticks)
    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, x_label_format_dict=x_label_format_dict,
        x_tick_labels=x_tick_labels, x_tick_label_format_dict=x_tick_label_format_dict,
        y_label=y_label, y_label_format_dict=y_label_format_dict,
        y_tick_labels=y_tick_labels, y_tick_label_format_dict=y_tick_label_format_dict)
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=top_x_label, x_label_format_dict=top_x_label_format_dict,
        x_tick_labels=top_x_tick_labels, x_tick_label_format_dict=top_x_tick_label_format_dict,
        y_label=right_y_label, y_label_format_dict=right_y_label_format_dict,
        y_tick_labels=right_y_tick_labels, y_tick_label_format_dict=right_y_tick_label_format_dict,
        opposite_axis=True)


def each_group_scatter_plotting(
        current_ax, this_group_data_dict, common_scatter_param_dict, common_error_bar_param_dict,
        error_bar, x_lim=None, x_ticks=None, y_lim=None, y_ticks=None, cutoff_value=None, cutoff_param_dict=None,
):
    (
        x_value_array, (y_mean_array, y_std_array), marker_size, marker_color, this_data_scatter_param_dict,
        this_data_error_bar_param_dict
    ) = [
        this_group_data_dict[key] if key in this_group_data_dict else None
        for key in [
            ParameterName.x_value_array, ParameterName.y_value_array, ParameterName.marker_size,
            ParameterName.marker_color, ParameterName.scatter_param_dict, ParameterName.error_bar_param_dict]
    ]
    if this_data_scatter_param_dict is None:
        this_data_scatter_param_dict = {}
    scatter_param_dict = {
        **common_scatter_param_dict,
        **this_data_scatter_param_dict,
    }
    if this_data_error_bar_param_dict is None:
        this_data_error_bar_param_dict = {}
    error_bar_param_dict = {
        **common_error_bar_param_dict,
        **this_data_error_bar_param_dict,
    }
    if marker_size is not None:
        core_scatter_plotting(
            current_ax, x_value_array, y_mean_array, marker_size, marker_color,
            scatter_param_dict=scatter_param_dict, x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks,
            cutoff=cutoff_value, cutoff_param_dict=cutoff_param_dict)
    if error_bar and y_std_array is not None:
        core_error_bar_plotting(
            current_ax, x_value_array, y_mean_array, y_std_array, edge_color=marker_color, **error_bar_param_dict)


def single_scatter_plotting(
        current_ax, current_transform, complete_data_dict, scatter_param_dict=None, x_lim=None, x_ticks=None,
        y_lim=None, y_ticks=None, cutoff_value=None, cutoff_param_dict=None, x_label=None,
        x_label_format_dict=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_tick_labels=None, y_tick_label_format_dict=None,
        error_bar=False, error_bar_param_dict=None, scatter_line=None, line_param_dict=None, **kwargs):
    if scatter_param_dict is None:
        scatter_param_dict = {}
    if error_bar_param_dict is None:
        error_bar_param_dict = {}
    if isinstance(complete_data_dict, list):
        for index, each_complete_data_dict in enumerate(complete_data_dict):
            if index == 0:
                each_group_scatter_plotting(
                    current_ax, each_complete_data_dict, scatter_param_dict, error_bar_param_dict, error_bar,
                    x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks,
                    cutoff_value=cutoff_value, cutoff_param_dict=cutoff_param_dict,)
            else:
                each_group_scatter_plotting(
                    current_ax, each_complete_data_dict, scatter_param_dict, error_bar_param_dict, error_bar)
    elif isinstance(complete_data_dict, dict):
        each_group_scatter_plotting(
            current_ax, complete_data_dict, scatter_param_dict, error_bar_param_dict,
            error_bar, x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks,
            cutoff_value=cutoff_value, cutoff_param_dict=cutoff_param_dict,)
    else:
        raise ValueError()

    if scatter_line is not None:
        if line_param_dict is None:
            line_param_dict = {}
        if isinstance(line_param_dict, dict):
            line_param_dict_iter = it.repeat(line_param_dict)
        elif isinstance(line_param_dict, (list, tuple)) and isinstance(line_param_dict[0], dict):
            line_param_dict_iter = line_param_dict
        else:
            raise ValueError()
        for (x_value_list, y_value_list, *detailed_line_param_dict), common_line_param_dict in zip(
                scatter_line, line_param_dict_iter):
            each_line_param_dict = dict(common_line_param_dict)
            if len(detailed_line_param_dict) > 0:
                each_line_param_dict.update(detailed_line_param_dict[0])
            core_line_plotting(current_ax, x_value_list, y_value_list, **each_line_param_dict)
    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, x_label_format_dict=x_label_format_dict,
        x_tick_labels=x_tick_labels, x_tick_label_format_dict=x_tick_label_format_dict, y_label=y_label,
        y_label_format_dict=y_label_format_dict, y_tick_labels=y_tick_labels,
        y_tick_label_format_dict=y_tick_label_format_dict)


def single_point_variation_plotting(
        current_ax, current_transform, complete_data_dict, x_lim, x_ticks,
        y_lim, y_ticks, line_param_dict, error_bar_param_dict, cutoff_value=None, cutoff_param_dict=None, x_label=None,
        x_label_format_dict=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_tick_labels=None, y_tick_label_format_dict=None, **kwargs):
    def filter_and_plot_y_error_bar(
            current_data_label, raw_x_value_array, raw_y_value_array, raw_error_bar_array_list, edge_color):
        new_error_bar_array_list = []
        new_x_value_array_list = []
        new_y_value_array_list = []
        for raw_x_value, raw_y_value, error_bar_value in zip(
                raw_x_value_array, raw_y_value_array, raw_error_bar_array_list):
            if error_bar_value is not None:
                new_x_value_array_list.append(raw_x_value)
                new_y_value_array_list.append(raw_y_value)
                new_error_bar_array_list.append(error_bar_value)
        new_x_value_array = np.array(new_x_value_array_list)
        new_y_value_array = np.array(new_y_value_array_list)
        new_error_bar_array = np.array(new_error_bar_array_list)
        core_error_bar_plotting(
            current_ax, new_x_value_array, new_y_value_array, new_error_bar_array, label=current_data_label,
            edge_color=edge_color, **error_bar_param_dict)

    if line_param_dict is None:
        line_param_dict = {}
    line_value_dict = {}
    for index, (data_label, current_data_dict) in enumerate(complete_data_dict.items()):
        y_value_data_dict, marker_size, marker_color, scatter_param_dict = [
            current_data_dict[key] if key in current_data_dict else None
            for key in [
                ParameterName.y_value_data_dict, ParameterName.marker_size,
                ParameterName.marker_color, ParameterName.scatter_param_dict]
        ]
        this_data_size = len(y_value_data_dict)
        x_value_array = np.ones(this_data_size) * index
        y_value_array_list = []
        y_error_bar_array_list = []
        for y_value_data_label, (y_value, y_error_bar_value) in y_value_data_dict.items():
            y_value_array_list.append(y_value)
            y_error_bar_array_list.append(y_error_bar_value)
            if y_value_data_label not in line_value_dict:
                line_value_dict[y_value_data_label] = ([], [])
            line_value_dict[y_value_data_label][0].append(index)
            line_value_dict[y_value_data_label][1].append(y_value)
        y_value_array = np.array(y_value_array_list)
        filter_and_plot_y_error_bar(data_label, x_value_array, y_value_array, y_error_bar_array_list, marker_color[0])
        core_scatter_plotting(
            current_ax, x_value_array, y_value_array, marker_size, marker_color, label=data_label,
            scatter_param_dict=scatter_param_dict)
    for data_label, (x_value_list, y_value_list) in line_value_dict.items():
        core_line_plotting(
            current_ax, x_value_list, y_value_list, **line_param_dict)
    core_scatter_plotting(
        current_ax, [], [], x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks,
        cutoff=cutoff_value, cutoff_param_dict=cutoff_param_dict)
    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, x_label_format_dict=x_label_format_dict,
        x_tick_labels=x_tick_labels, x_tick_label_format_dict=x_tick_label_format_dict, y_label=y_label,
        y_label_format_dict=y_label_format_dict, y_tick_labels=y_tick_labels,
        y_tick_label_format_dict=y_tick_label_format_dict)


def single_bar_plotting(
        current_ax, current_transform, current_array_data_dict, current_error_bar_data_dict,
        array_len, figure_config_dict, y_lim=None, y_ticks=None, cutoff_value=None, color_dict=None,
        x_label=None, x_tick_labels=None, y_label=None, y_tick_labels=None,
        twin_x_axis=False, broken_y_axis=None, max_bar_num_each_group=None,
        x_tick_separator_locs=None, x_tick_separator_labels=None, x_tick_separator_label_locs=None,
        y_tick_separator_locs=None, y_tick_separator_labels=None, y_tick_separator_label_locs=None,
        current_raw_scatter_data_dict=None,
        **kwargs):
    def separate_arguments_for_two_axis(argument, total_axis_num=2, extra_value_list=()):
        if argument is None or argument in extra_value_list:
            argument_list = [argument for _ in range(total_axis_num)]
        else:
            assert isinstance(argument, (tuple, list)) and len(argument) == total_axis_num
            # bottom_argument, top_argument = argument
            argument_list = argument
        return argument_list

    assert not twin_x_axis or broken_y_axis is None
    column_width = figure_config_dict[ParameterName.column_width]
    edge = figure_config_dict[ParameterName.edge]
    # cutoff_param_dict = default_parameter_extract(figure_config_dict, ParameterName.cutoff_param_dict, None)
    # bar_param_dict = default_parameter_extract(figure_config_dict, ParameterName.bar_param_dict, None)
    # error_bar_param_dict = default_parameter_extract(figure_config_dict, ParameterName.error_bar_param_dict, None)
    (
        cutoff_param_dict, bar_param_dict, error_bar_param_dict, raw_data_scatter_param_dict,
    ) = default_parameter_extract(
        figure_config_dict, [
            ParameterName.cutoff_param_dict, ParameterName.bar_param_dict, ParameterName.error_bar_param_dict,
            ParameterName.scatter_param_dict,
        ], None, repeat_default_value=True)
    (
        x_label_format_dict,
        x_tick_label_format_dict,
        y_label_format_dict,
        y_tick_label_format_dict
    ) = default_parameter_extract(
        figure_config_dict, [
            ParameterName.x_label_format_dict,
            ParameterName.x_tick_label_format_dict,
            ParameterName.y_label_format_dict,
            ParameterName.y_tick_label_format_dict,
        ], None, repeat_default_value=True)
    if broken_y_axis is not None:
        # current_ax is from bottom to top
        total_y_axis_num = len(current_ax)
        ax_list = separate_arguments_for_two_axis(current_ax, total_axis_num=total_y_axis_num)
        transform_list = separate_arguments_for_two_axis(current_transform, total_axis_num=total_y_axis_num)
        y_lim_list = separate_arguments_for_two_axis(y_lim, total_axis_num=total_y_axis_num)
        y_ticks_list = separate_arguments_for_two_axis(y_ticks, total_axis_num=total_y_axis_num)
        y_tick_labels_list = separate_arguments_for_two_axis(
            y_tick_labels, total_axis_num=total_y_axis_num, extra_value_list=(Keywords.default,))
        y_tick_separator_locs_list = separate_arguments_for_two_axis(
            y_tick_separator_locs, total_axis_num=total_y_axis_num)
        y_tick_separator_labels_list = separate_arguments_for_two_axis(
            y_tick_separator_labels, total_axis_num=total_y_axis_num)
        y_tick_separator_label_locs_list = separate_arguments_for_two_axis(
            y_tick_separator_label_locs, total_axis_num=total_y_axis_num)
        y_label_list = separate_arguments_for_two_axis(y_label, total_axis_num=total_y_axis_num)
        for ax_index, (
                this_ax, this_transform, this_y_lim, this_y_label, this_y_ticks, this_y_tick_labels,
                this_y_tick_separator_locs, this_y_tick_separator_labels, this_y_tick_separator_label_locs
        ) in enumerate(zip(
                ax_list, transform_list, y_lim_list, y_label_list, y_ticks_list, y_tick_labels_list,
                y_tick_separator_locs_list, y_tick_separator_labels_list, y_tick_separator_label_locs_list)):
            core_single_ax_bar_plot(
                this_ax, current_array_data_dict, color_dict, current_error_bar_data_dict, array_len,
                column_width, edge, y_lim=this_y_lim, y_ticks=this_y_ticks,
                bar_param_dict=bar_param_dict, error_bar_param_dict=error_bar_param_dict,
                cutoff=cutoff_value, cutoff_param_dict=cutoff_param_dict,
                max_bar_num_each_group=max_bar_num_each_group, raw_data_scatter_dict=current_raw_scatter_data_dict,
                raw_data_scatter_param_dict=raw_data_scatter_param_dict)
            if ax_index == 0:
                draw_axis_tick_and_tick_separator_label(
                    this_ax, this_transform, figure_config_dict,
                    x_label, x_label_format_dict, x_tick_labels, x_tick_label_format_dict,
                    y_label=this_y_label, y_label_format_dict=y_label_format_dict,
                    y_tick_labels=this_y_tick_labels, y_tick_label_format_dict=y_tick_label_format_dict,
                    x_tick_separator_locs=x_tick_separator_locs, x_tick_separator_labels=x_tick_separator_labels,
                    x_tick_separator_label_locs=x_tick_separator_label_locs,
                    y_tick_separator_locs=this_y_tick_separator_locs,
                    y_tick_separator_labels=this_y_tick_separator_labels,
                    y_tick_separator_label_locs=this_y_tick_separator_label_locs)
            else:
                draw_axis_tick_and_tick_separator_label(
                    this_ax, this_transform, figure_config_dict,
                    y_label=this_y_label, y_label_format_dict=y_label_format_dict,
                    y_tick_labels=this_y_tick_labels, y_tick_label_format_dict=y_tick_label_format_dict,
                    y_tick_separator_locs=this_y_tick_separator_locs,
                    y_tick_separator_labels=this_y_tick_separator_labels,
                    y_tick_separator_label_locs=this_y_tick_separator_label_locs)
    else:
        if current_array_data_dict is not None:
            core_single_ax_bar_plot(
                current_ax, current_array_data_dict, color_dict, current_error_bar_data_dict, array_len,
                column_width, edge, y_lim=y_lim, y_ticks=y_ticks,
                bar_param_dict=bar_param_dict, error_bar_param_dict=error_bar_param_dict,
                cutoff=cutoff_value, cutoff_param_dict=cutoff_param_dict, twin_x_axis=twin_x_axis,
                max_bar_num_each_group=max_bar_num_each_group, raw_data_scatter_dict=current_raw_scatter_data_dict,
                raw_data_scatter_param_dict=raw_data_scatter_param_dict)
        if twin_x_axis:
            current_ax, right_side_ax = current_ax
            if current_array_data_dict is None:
                right_side_ax.set_axis_off()
            else:
                right_y_label = None
                if isinstance(y_label, (tuple, list)):
                    right_y_label = y_label[1]
                    y_label = y_label[0]
                right_y_tick_labels = Keywords.default
                if isinstance(y_tick_labels, (tuple, list)):
                    if (isinstance(y_tick_labels[0], str) and y_tick_labels[0] == Keywords.default) \
                            or isinstance(y_tick_labels[0], (tuple, list)):
                        right_y_tick_labels = y_tick_labels[1]
                        y_tick_labels = y_tick_labels[0]
                if isinstance(y_label_format_dict, (tuple, list)):
                    right_y_label_format_dict = y_label_format_dict[1]
                    y_label_format_dict = y_label_format_dict[0]
                else:
                    right_y_label_format_dict = y_label_format_dict
                if isinstance(y_tick_label_format_dict, (tuple, list)):
                    right_y_tick_label_format_dict = y_tick_label_format_dict[1]
                    y_tick_label_format_dict = y_tick_label_format_dict[0]
                else:
                    right_y_tick_label_format_dict = y_tick_label_format_dict
                axis_appearance_setting(right_side_ax, x_tick_labels=[], y_tick_labels=[])
                draw_axis_label_and_tick_label(
                    right_side_ax, current_transform, y_label=right_y_label,
                    y_label_format_dict=right_y_label_format_dict, y_tick_labels=right_y_tick_labels,
                    y_tick_label_format_dict=right_y_tick_label_format_dict, opposite_axis=True)
        if current_array_data_dict is None:
            current_ax.set_axis_off()
        else:
            draw_axis_tick_and_tick_separator_label(
                current_ax, current_transform, figure_config_dict,
                x_label, x_label_format_dict, x_tick_labels, x_tick_label_format_dict,
                y_label, y_label_format_dict, y_tick_labels, y_tick_label_format_dict,
                x_tick_separator_locs=x_tick_separator_locs, x_tick_separator_labels=x_tick_separator_labels,
                x_tick_separator_label_locs=x_tick_separator_label_locs,
                y_tick_separator_locs=y_tick_separator_locs, y_tick_separator_labels=y_tick_separator_labels,
                y_tick_separator_label_locs=y_tick_separator_label_locs)


def single_violin_box_distribution_plot(
        current_ax, current_transform, data_list, positions, figure_config_dict,
        x_lim=None, x_label=None, x_ticks=None, x_tick_labels=None,
        y_lim=None, y_label=None, y_ticks=None, y_tick_labels=None,
        cutoff=None, emphasized_flux_list=None, figure_type='violin'):
    if cutoff is not None and ParameterName.cutoff_param_dict in figure_config_dict:
        cutoff_param_dict = figure_config_dict[ParameterName.cutoff_param_dict]
    else:
        cutoff_param_dict = None
    box_violin_config_dict = figure_config_dict[ParameterName.box_violin_config_dict]

    core_plot_violin_box_plot(
        current_ax, figure_type, data_list, positions, box_violin_config_dict, cutoff=cutoff,
        cutoff_param_dict=cutoff_param_dict, emphasized_flux_list=emphasized_flux_list, x_lim=x_lim, y_lim=y_lim,
        x_ticks=x_ticks, y_ticks=y_ticks)

    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, y_label=y_label,
        x_tick_labels=x_tick_labels, y_tick_labels=y_tick_labels, **figure_config_dict)


def single_violin_box_scatter_mix_distribution_plot(
        current_ax, current_transform, data_list, position_list, figure_type_list, figure_config_dict,
        x_lim=None, x_label=None, x_ticks=None, x_tick_labels=None,
        y_lim=None, y_label=None, y_ticks=None, y_tick_labels=None):
    box_violin_config_dict = figure_config_dict[ParameterName.box_violin_config_dict]
    scatter_config_dict = figure_config_dict[ParameterName.scatter_param_dict]
    marker_size, marker_color, scatter_param_dict = default_parameter_extract(
        scatter_config_dict,
        [ParameterName.marker_size, ParameterName.marker_color, ParameterName.scatter_param_dict],
        None, repeat_default_value=True)

    for current_figure_type, current_position, current_data_array in zip(figure_type_list, position_list, data_list):
        if current_figure_type == ParameterName.violin or current_figure_type == ParameterName.box:
            assert isinstance(current_position, (int, float))
            core_plot_violin_box_plot(
                current_ax, current_figure_type, [current_data_array], [current_position],
                box_violin_config_dict, x_lim=x_lim, y_lim=y_lim, x_ticks=x_ticks, y_ticks=y_ticks)
        elif current_figure_type == ParameterName.scatter:
            core_scatter_plotting(
                current_ax, current_position, current_data_array,
                marker_size, marker_color, scatter_param_dict=scatter_param_dict,
                x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks)
        else:
            raise ValueError()

    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, y_label=y_label,
        x_tick_labels=x_tick_labels, y_tick_labels=y_tick_labels, **figure_config_dict)


def single_histogram_plot(
        current_ax, current_transform, complete_data_dict, figure_config_dict,
        cutoff=None, x_lim=None, x_label=None, x_ticks=None, x_tick_labels=None,
        y_lim=None, y_label=None, y_ticks=None, y_tick_labels=None):
    if cutoff is not None:
        cutoff_param_dict = figure_config_dict[ParameterName.cutoff_param_dict]
    else:
        cutoff_param_dict = None
    for data_label, current_data_dict in complete_data_dict.items():
        value_array, histogram_param_dict = [
            current_data_dict[key] if key in current_data_dict else None
            for key in [
                ParameterName.x_value_array, ParameterName.histogram_param_dict]
        ]
        core_histogram_plotting(current_ax, value_array, label=data_label, **histogram_param_dict)
    core_histogram_plotting(
        current_ax, x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks,
        cutoff=cutoff, cutoff_param_dict=cutoff_param_dict)
    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, y_label=y_label,
        x_tick_labels=x_tick_labels, y_tick_labels=y_tick_labels, **figure_config_dict)


def set_ax_patch_parameter(ax, parameter_dict):
    def set_parameter(obj, alpha=None, **kwargs):
        final_parameter_dict = {}
        if alpha is not None:
            final_parameter_dict['alpha'] = alpha
        obj.set(**final_parameter_dict)

    set_parameter(ax.patch, **parameter_dict)


def set_ax_spine_parameter(ax, parameter_dict, *, top=True, bottom=True, left=True, right=True):
    def set_parameter(obj, edge_width=None, edge_style=None, edge_color=None, visible=None, **kwargs):
        final_parameter_dict = {}
        if edge_width is not None:
            final_parameter_dict['linewidth'] = edge_width
        if edge_style is not None:
            final_parameter_dict['linestyle'] = edge_style
        if edge_color is not None:
            final_parameter_dict['edgecolor'] = edge_color
        if visible is not None:
            final_parameter_dict['visible'] = visible
        obj.set(**final_parameter_dict)

    if parameter_dict is not None:
        location_list = []
        if top:
            location_list.append(ParameterName.ax_top)
        if bottom:
            location_list.append(ParameterName.ax_bottom)
        if left:
            location_list.append(ParameterName.ax_left)
        if right:
            location_list.append(ParameterName.ax_right)
        for axis in location_list:
            # ax.spines[axis].set(**parameter_dict)
            set_parameter(ax.spines[axis], **parameter_dict)


def set_ax_tick_parameter(ax, parameter_dict, *, top=False, bottom=True, left=True, right=False):
    def set_parameter(
            axis_tick_length=None, edge_width=None, edge_color=None, font_size=None, font_color=None, z_order=None,
            **kwargs):
        final_parameter_dict = {}
        for name, bool_value in zip(
                [ParameterName.ax_top, ParameterName.ax_bottom, ParameterName.ax_left, ParameterName.ax_right],
                [top, bottom, left, right]):
            final_parameter_dict[name] = bool_value
            final_parameter_dict[f'label{name}'] = bool_value
        if axis_tick_length is not None:
            final_parameter_dict['length'] = axis_tick_length
        if edge_width is not None:
            final_parameter_dict['width'] = edge_width
        if edge_color is not None:
            final_parameter_dict['color'] = edge_color
        if font_size is not None:
            final_parameter_dict['labelsize'] = font_size
        if font_color is not None:
            final_parameter_dict['labelcolor'] = font_color
        if z_order is not None:
            final_parameter_dict['zorder'] = z_order
        ax.tick_params(**final_parameter_dict)

    if parameter_dict is None:
        parameter_dict = {}
    # tick_params_dict = {
    #     ParameterName.ax_top: top,
    #     ParameterName.ax_bottom: bottom,
    #     ParameterName.ax_left: left,
    #     ParameterName.ax_right: right,
    #     f'label{ParameterName.ax_top}': top,
    #     f'label{ParameterName.ax_bottom}': bottom,
    #     f'label{ParameterName.ax_left}': left,
    #     f'label{ParameterName.ax_right}': right,
    # }
    # axis_tick_parameter_map = MPLParameterName.axis_tick_parameter_map
    # for key, value in parameter_dict.items():
    #     if key in axis_tick_parameter_map:
    #         new_key = axis_tick_parameter_map[key]
    #     else:
    #         new_key = key
    #     tick_params_dict[new_key] = value
    # ax.tick_params(**tick_params_dict)
    set_parameter(**parameter_dict)


def get_axis_position_and_axis_transform(ax):
    left, bottom, width, height = ax.get_position().bounds
    # current_ax_trans = transforms.Affine2D(matrix=np.array([[width, 0, left], [0, height, bottom], [0, 0, 1]]))
    # Since all plot is based on figure width, but axis height is relative to figure height, therefore the
    # transformed result will be smaller than needed transform (if figure height is larger than width)
    figure_box = ax.figure.bbox
    figure_height_to_width_ratio = figure_box.height / figure_box.width
    current_ax_size_trans = transforms.Affine2D().scale(width, height * figure_height_to_width_ratio)
    return Vector(left, bottom), Vector(width, height), current_ax_size_trans


def draw_parallel_line_along_axis(
        ax, axis_name, ax_axis_trans, complete_ax_transform,
        line_axis_loc_array: np.ndarray, axis_line_end_distance: float, axis_line_start_distance: float = 0,
        opposite_axis=False, **line_config_dict):
    line_num = len(line_axis_loc_array)
    assert axis_line_end_distance > axis_line_start_distance
    if not isinstance(line_axis_loc_array, np.ndarray):
        line_axis_loc_array = np.array(line_axis_loc_array)
    if opposite_axis:
        basic_loc_col_array = np.ones([line_num, 1])
    else:
        basic_loc_col_array = np.zeros([line_num, 1])
    line_axis_loc_col_array = line_axis_loc_array.reshape([-1, 1])
    if axis_name == ParameterName.x:
        axis_coordinate = np.hstack([line_axis_loc_col_array, basic_loc_col_array])
        if opposite_axis:
            start_offset_vector = Vector(0, axis_line_start_distance)
            end_offset_vector = Vector(0, axis_line_end_distance)
        else:
            start_offset_vector = Vector(0, -axis_line_start_distance)
            end_offset_vector = Vector(0, -axis_line_end_distance)
    elif axis_name == ParameterName.y:
        axis_coordinate = np.hstack([basic_loc_col_array, line_axis_loc_col_array])
        if opposite_axis:
            start_offset_vector = Vector(axis_line_start_distance, 0)
            end_offset_vector = Vector(axis_line_end_distance, 0)
        else:
            start_offset_vector = Vector(-axis_line_start_distance, 0)
            end_offset_vector = Vector(-axis_line_end_distance, 0)
    else:
        raise ValueError()
    basic_config_dict = {
        ParameterName.transform: complete_ax_transform,
        **line_config_dict,
    }
    start_row_array = ax_axis_trans.transform(axis_coordinate) + start_offset_vector
    end_row_array = ax_axis_trans.transform(axis_coordinate) + end_offset_vector
    line_obj_list = []
    for start_loc, end_loc in zip(start_row_array, end_row_array):
        current_config_dict = {
            **basic_config_dict,
            ParameterName.start: Vector(array=start_loc),
            ParameterName.end: Vector(array=end_loc),
        }
        line_obj = Line(**current_config_dict)
        line_active_obj = line_obj.draw(ax.figure, parent_ax=ax, parent_transformation=complete_ax_transform)
        line_active_obj.set_clip_on(False)
        line_obj_list.append(line_active_obj)
    return line_obj_list


def draw_text_box(ax, ax_transform, center, width, height, angle=None, **kwargs):
    # if angle is None:
    #     angle = 0
    # elif angle > 90 or angle < -90:
    #     angle = np.sign(angle) * abs(angle) - 90
    # elif angle > 45 or angle < -45:
    #     height, width = width, height
    #     angle = np.sign(angle) * (90 - abs(angle))
    width, height, angle = clip_angle_to_normal_range(width, height, angle)
    text_box_config = {
        ParameterName.center: center,
        ParameterName.width: width,
        ParameterName.height: height,
        ParameterName.angle: angle,
        **DataFigureConfig.common_text_box_config_dict
    }
    text_box_obj = Rectangle(**text_box_config)
    text_box_obj = text_box_obj.draw(ax.figure, parent_ax=ax, parent_transformation=ax_transform)
    text_box_obj.set_clip_on(False)


def draw_text_by_axis_loc(ax, text_content, text_axis_loc_pair, complete_ax_transform, **text_format_dict):
    if text_content is None:
        return None
    text_format_dict = {
        ParameterName.transform: complete_ax_transform,
        **text_format_dict
    }
    bottom_left, size, ax_axis_trans = get_axis_position_and_axis_transform(ax)
    if isinstance(text_content, str):
        assert len(text_axis_loc_pair) == 2
        center = Vector(array=ax_axis_trans.transform(text_axis_loc_pair))
        text_obj = draw_text(ax, center, text_content, **text_format_dict)
    elif isinstance(text_content, (list, tuple)):
        assert (
                isinstance(text_axis_loc_pair, (list, tuple, np.ndarray))
                and len(text_content) == len(text_axis_loc_pair))
        text_obj = []
        for current_text_content, current_text_axis_loc_pair in zip(text_content, text_axis_loc_pair):
            center = Vector(array=ax_axis_trans.transform(current_text_axis_loc_pair))
            text_obj.append(draw_text(ax, center, current_text_content, **text_format_dict))
    else:
        raise TypeError()
    return text_obj


def draw_text_list_along_axis(
        ax, axis_name, ax_axis_trans, complete_ax_transform,
        text_content_list, text_axis_loc_array: np.ndarray, text_axis_distance: float, distance_offset_value,
        text_box=False, opposite_axis=False, **text_format_dict):
    text_list_num = len(text_content_list)
    assert len(text_axis_loc_array) == text_list_num
    if not isinstance(text_axis_loc_array, np.ndarray):
        text_axis_loc_array = np.array(text_axis_loc_array)
    if opposite_axis:
        basic_loc_col_array = np.ones([text_list_num, 1])
    else:
        basic_loc_col_array = np.zeros([text_list_num, 1])
    text_axis_loc_col_array = text_axis_loc_array.reshape([-1, 1])
    if axis_name == ParameterName.x:
        axis_coordinate = np.hstack([text_axis_loc_col_array, basic_loc_col_array])
        if opposite_axis:
            offset_vector = Vector(0, text_axis_distance + distance_offset_value)
            va = VerticalAlignment.baseline
        else:
            offset_vector = Vector(0, -text_axis_distance - distance_offset_value)
            va = VerticalAlignment.top
        ha = HorizontalAlignment.center
    elif axis_name == ParameterName.y:
        axis_coordinate = np.hstack([basic_loc_col_array, text_axis_loc_col_array])
        if opposite_axis:
            offset_vector = Vector(text_axis_distance + distance_offset_value, 0)
        else:
            offset_vector = Vector(-text_axis_distance - distance_offset_value, 0)
        va = VerticalAlignment.baseline
        ha = HorizontalAlignment.center
    else:
        raise ValueError()
    effective_tick_label_format_dict = {
        ParameterName.vertical_alignment: va,
        ParameterName.horizontal_alignment: ha,
        ParameterName.transform: complete_ax_transform,
        **text_format_dict,
    }
    center_row_array = ax_axis_trans.transform(axis_coordinate) + offset_vector
    text_obj_list = []
    for center, text_content in zip(center_row_array, text_content_list):
        text_obj = draw_text(ax, center, text_content, **effective_tick_label_format_dict)
        text_obj_list.append(text_obj)
        if text_box:
            draw_text_box(ax, complete_ax_transform, center, **effective_tick_label_format_dict)
    return text_obj_list


def draw_axis_label_and_tick_label(
        ax, ax_transform, x_label=None, x_label_format_dict=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_tick_labels=None, y_tick_label_format_dict=None,
        opposite_axis=False, **kwargs):
    def determine_decimal_num(tick_array):
        array_step = tick_array[1] - tick_array[0]
        if array_step >= 1:
            decimal_num = 0
        else:
            decimal_num = 0
            while array_step < 10 ** (-decimal_num):
                decimal_num += 1
            if array_step * 10 ** decimal_num % 1 > 0.1:
                decimal_num += 1
        return decimal_num

    def count_tick_label_type(raw_tick_label_list):
        first_item = raw_tick_label_list[0]
        not_digital = False
        first_item_type = type(first_item)
        if not np.isreal(first_item):
            not_digital = True
        elif np.issubdtype(first_item.dtype, np.integer):
            first_item_type = np.integer
        else:
            first_item_type = np.floating
        for raw_tick_label in raw_tick_label_list:
            if not isinstance(raw_tick_label, first_item_type):
                if not_digital or not np.isreal(raw_tick_label):
                    raise ValueError('Type not match!')
                else:
                    first_item_type = float
                    break
        return first_item_type

    def draw_axis_label(
            axis_name, ax_axis_trans, label_text, axis_label_distance, axis_label_location=0.5, **label_format_dict):
        if axis_name == ParameterName.x:
            rotation = None
            if opposite_axis:
                va = VerticalAlignment.baseline
            else:
                va = VerticalAlignment.top
            ha = HorizontalAlignment.center
        elif axis_name == ParameterName.y:
            if opposite_axis:
                rotation = -90
            else:
                rotation = 90
            va = VerticalAlignment.baseline
            ha = HorizontalAlignment.center
        else:
            raise ValueError()
        distance_offset_value = label_format_dict[ParameterName.height] / 2
        label_format_dict = {
            ParameterName.vertical_alignment: va,
            ParameterName.horizontal_alignment: ha,
            ParameterName.angle: rotation,
            **label_format_dict
        }
        text_obj_list = draw_text_list_along_axis(
            ax, axis_name, ax_axis_trans, ax_transform,
            [label_text], np.array([axis_label_location]), axis_label_distance, distance_offset_value,
            opposite_axis=opposite_axis, **label_format_dict)
        return text_obj_list[0]

    def draw_axis_tick_label(
            axis_name, ax_axis_trans, ax_lim, ax_tick_array, tick_label_list, axis_tick_label_distance,
            decimal_num=None, percentage=False, **tick_label_format_dict
    ):
        min_lim = np.min(ax_lim)
        max_lim = np.max(ax_lim)
        ax_tick_array = ax_tick_array[np.logical_and(min_lim <= ax_tick_array, ax_tick_array <= max_lim)]
        if isinstance(tick_label_list, (list, tuple)):
            assert len(ax_tick_array) == len(tick_label_list)
            if percentage:
                if decimal_num is None:
                    decimal_num = 0
                tick_label_list = [
                    f'{round_to_str_with_fixed_point(tick_label * 100, decimal_num)}%'
                    for tick_label in tick_label_list]
            elif decimal_num is not None:
                tick_label_list = [
                    round_to_str_with_fixed_point(tick_label, decimal_num) for tick_label in tick_label_list]
        elif isinstance(tick_label_list, str) and tick_label_list == Keywords.default:
            if percentage:
                if decimal_num is None:
                    decimal_num = 0
                tick_label_list = [
                    f'{round_to_str_with_fixed_point(ax_tick * 100, decimal_num)}%' for ax_tick in ax_tick_array]
            else:
                if decimal_num is None:
                    decimal_num = determine_decimal_num(ax_tick_array)
                tick_label_list = [
                    round_to_str_with_fixed_point(ax_tick, decimal_num) for ax_tick in ax_tick_array]
        ax_range = ax_lim[1] - ax_lim[0]
        if axis_name == ParameterName.x:
            if opposite_axis:
                va = VerticalAlignment.baseline
            else:
                va = VerticalAlignment.top
            ha = HorizontalAlignment.center
            distance_offset_value = tick_label_format_dict[ParameterName.height] / 2
        elif axis_name == ParameterName.y:
            if opposite_axis:
                ha = HorizontalAlignment.left
            else:
                ha = HorizontalAlignment.right
            va = VerticalAlignment.center_baseline
            distance_offset_value = tick_label_format_dict[ParameterName.width] / 2
        else:
            raise ValueError()
        tick_label_format_dict = {
            ParameterName.vertical_alignment: va,
            ParameterName.horizontal_alignment: ha,
            **tick_label_format_dict
        }
        tick_ax_location_array = (ax_tick_array - ax_lim[0]) / ax_range
        text_obj_list = draw_text_list_along_axis(
            ax, axis_name, ax_axis_trans, ax_transform,
            tick_label_list, tick_ax_location_array, axis_tick_label_distance, distance_offset_value,
            opposite_axis=opposite_axis, **tick_label_format_dict)
        return text_obj_list

    bottom_left, size, current_ax_trans = get_axis_position_and_axis_transform(ax)
    if x_label is not None:
        if x_label_format_dict is None:
            x_label_format_dict = {}
        x_label_obj = draw_axis_label(ParameterName.x, current_ax_trans, x_label, **x_label_format_dict)
    else:
        x_label_obj = None
    if y_label is not None:
        if y_label_format_dict is None:
            y_label_format_dict = {}
        y_label_obj = draw_axis_label(ParameterName.y, current_ax_trans, y_label, **y_label_format_dict)
    else:
        y_label_obj = None
    if x_tick_labels is not None:
        current_x_tick_list = ax.get_xticks()
        current_x_lim = ax.get_xlim()
        if x_tick_label_format_dict is None:
            x_tick_label_format_dict = {}
        x_tick_label_obj_list = draw_axis_tick_label(
            ParameterName.x, current_ax_trans, current_x_lim, current_x_tick_list, x_tick_labels,
            **x_tick_label_format_dict)
    else:
        x_tick_label_obj_list = None
    if y_tick_labels is not None:
        current_y_tick_list = ax.get_yticks()
        current_y_lim = ax.get_ylim()
        if y_tick_label_format_dict is None:
            y_tick_label_format_dict = {}
        y_tick_label_obj_list = draw_axis_tick_label(
            ParameterName.y, current_ax_trans, current_y_lim, current_y_tick_list, y_tick_labels,
            **y_tick_label_format_dict)
    else:
        y_tick_label_obj_list = None
    return x_label_obj, x_tick_label_obj_list, y_label_obj, y_tick_label_obj_list


def draw_axis_tick_separator_and_label(
        ax, ax_transform, x_tick_separator_locs=None, x_tick_separator_format_dict=None,
        x_tick_separator_labels=None, x_tick_separator_label_locs=None, x_tick_separator_label_format_dict=None,
        y_tick_separator_locs=None, y_tick_separator_format_dict=None,
        y_tick_separator_labels=None, y_tick_separator_label_locs=None, y_tick_separator_label_format_dict=None,
        opposite_axis=False, **kwargs):
    def draw_single_tick_separator(axis_name, tick_separator_locs, tick_separator_format_dict):
        line_obj_list = draw_parallel_line_along_axis(
            ax, axis_name, current_ax_trans, ax_transform,
            tick_separator_locs, opposite_axis=opposite_axis, **tick_separator_format_dict)
        return line_obj_list

    def draw_single_tick_separator_label(
            axis_name, text_location_offset_label,
            tick_separator_labels, tick_separator_label_locs, tick_separator_label_format_dict):
        tick_separator_label_format_dict = dict(tick_separator_label_format_dict)
        text_axis_distance = tick_separator_label_format_dict.pop(ParameterName.axis_label_distance)
        text_location_offset = tick_separator_label_format_dict[text_location_offset_label] / 2
        text_obj_list = draw_text_list_along_axis(
            ax, axis_name, current_ax_trans, ax_transform,
            tick_separator_labels, tick_separator_label_locs, text_axis_distance, text_location_offset,
            opposite_axis=opposite_axis, **tick_separator_label_format_dict)
        return text_obj_list

    def draw_tick_separators_and_labels_for_one_axis(
            axis_name, text_location_offset_label, tick_separator_locs, tick_separator_format_dict,
            tick_separator_labels, tick_separator_label_locs, tick_separator_label_format_dict):
        if tick_separator_locs is not None:
            if tick_separator_format_dict is None:
                tick_separator_format_dict = {}
            if isinstance(tick_separator_format_dict, dict):
                line_obj_list = draw_single_tick_separator(axis_name, tick_separator_locs, tick_separator_format_dict)
            elif isinstance(tick_separator_format_dict, (tuple, list)):
                assert len(tick_separator_locs) == len(tick_separator_format_dict)
                line_obj_list = []
                for single_tick_separator_loc, single_tick_separator_format_dict in zip(
                        tick_separator_locs, tick_separator_format_dict):
                    line_obj_list.extend(draw_single_tick_separator(
                        axis_name, [single_tick_separator_loc], single_tick_separator_format_dict))
            else:
                raise ValueError()
        else:
            line_obj_list = None
        if tick_separator_labels is not None:
            assert tick_separator_label_locs is not None \
                   and len(tick_separator_labels) == len(tick_separator_label_locs) \
                   and tick_separator_label_format_dict is not None
            if isinstance(tick_separator_label_format_dict, dict):
                text_obj_list = draw_single_tick_separator_label(
                    axis_name, text_location_offset_label, tick_separator_labels, tick_separator_label_locs,
                    tick_separator_label_format_dict)
            elif isinstance(tick_separator_label_format_dict, (tuple, list)):
                assert len(tick_separator_labels) == len(tick_separator_label_format_dict)
                text_obj_list = []
                for (
                        single_tick_separator_label, single_tick_separator_label_loc,
                        single_tick_separator_label_format_dict) in zip(
                        tick_separator_labels, tick_separator_label_locs, tick_separator_label_format_dict):
                    text_obj_list.extend(draw_single_tick_separator_label(
                        axis_name, text_location_offset_label, [single_tick_separator_label],
                        [single_tick_separator_label_loc], single_tick_separator_label_format_dict))
            else:
                raise ValueError()
        else:
            text_obj_list = None
        return line_obj_list, text_obj_list

    bottom_left, size, current_ax_trans = get_axis_position_and_axis_transform(ax)
    # if x_tick_separator_labels is not None:
    #     assert x_tick_separator_label_locs is not None \
    #            and len(x_tick_separator_labels) == len(x_tick_separator_label_locs) \
    #            and x_tick_separator_label_format_dict is not None
    #     x_tick_separator_label_format_dict = dict(x_tick_separator_label_format_dict)
    #     text_axis_distance = x_tick_separator_label_format_dict.pop(ParameterName.axis_label_distance)
    #     height = x_tick_separator_label_format_dict[ParameterName.height]
    #     x_text_obj_list = draw_text_list_along_axis(
    #         ax, ParameterName.x, current_ax_trans, ax_transform,
    #         x_tick_separator_labels, x_tick_separator_label_locs, text_axis_distance, height / 2,
    #         opposite_axis=opposite_axis, **x_tick_separator_label_format_dict)
    # else:
    #     x_text_obj_list = None
    # if x_tick_separator_locs is not None:
    #     if x_tick_separator_format_dict is None:
    #         x_tick_separator_format_dict = {}
    #     x_line_obj_list = draw_parallel_line_along_axis(
    #         ax, ParameterName.x, current_ax_trans, ax_transform,
    #         x_tick_separator_locs, opposite_axis=opposite_axis, **x_tick_separator_format_dict)
    # else:
    #     x_line_obj_list = None
    x_line_obj_list, x_text_obj_list = draw_tick_separators_and_labels_for_one_axis(
        ParameterName.x, ParameterName.height, x_tick_separator_locs, x_tick_separator_format_dict,
        x_tick_separator_labels, x_tick_separator_label_locs, x_tick_separator_label_format_dict)

    # if y_tick_separator_labels is not None:
    #     assert y_tick_separator_label_locs is not None \
    #            and len(y_tick_separator_labels) == len(y_tick_separator_label_locs) \
    #            and y_tick_separator_label_format_dict is not None
    #     y_tick_separator_label_format_dict = dict(y_tick_separator_label_format_dict)
    #     text_axis_distance = y_tick_separator_label_format_dict.pop(ParameterName.axis_label_distance)
    #     width = y_tick_separator_label_format_dict[ParameterName.width]
    #     y_text_obj_list = draw_text_list_along_axis(
    #         ax, ParameterName.y, current_ax_trans, ax_transform,
    #         y_tick_separator_labels, y_tick_separator_label_locs, text_axis_distance, width / 2,
    #         opposite_axis=opposite_axis, **y_tick_separator_label_format_dict)
    # else:
    #     y_text_obj_list = None
    # if y_tick_separator_locs is not None:
    #     if y_tick_separator_format_dict is None:
    #         y_tick_separator_format_dict = {}
    #     y_line_obj_list = draw_parallel_line_along_axis(
    #         ax, ParameterName.y, current_ax_trans, ax_transform,
    #         y_tick_separator_locs, opposite_axis=opposite_axis, **y_tick_separator_format_dict)
    # else:
    #     y_line_obj_list = None
    y_line_obj_list, y_text_obj_list = draw_tick_separators_and_labels_for_one_axis(
        ParameterName.y, ParameterName.width, y_tick_separator_locs, y_tick_separator_format_dict,
        y_tick_separator_labels, y_tick_separator_label_locs, y_tick_separator_label_format_dict)

    return x_text_obj_list, x_line_obj_list, y_text_obj_list, y_line_obj_list


def draw_axis_tick_and_tick_separator_label(
        current_ax, current_transform, figure_config_dict,
        x_label=None, x_label_format_dict=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_tick_labels=None, y_tick_label_format_dict=None,
        x_tick_separator_locs=None, x_tick_separator_labels=None, x_tick_separator_label_locs=None,
        y_tick_separator_locs=None, y_tick_separator_labels=None, y_tick_separator_label_locs=None,
        opposite_axis=False, ):
    (
        x_tick_separator_format_dict,
        x_tick_separator_label_format_dict,
        y_tick_separator_format_dict,
        y_tick_separator_label_format_dict
    ) = default_parameter_extract(
        figure_config_dict, [
            ParameterName.x_tick_separator_format_dict,
            ParameterName.x_tick_separator_label_format_dict,
            ParameterName.y_tick_separator_format_dict,
            ParameterName.y_tick_separator_label_format_dict,
        ], None, repeat_default_value=True)
    axis_appearance_setting(current_ax, x_tick_labels=[], y_tick_labels=[])
    draw_axis_label_and_tick_label(
        current_ax, current_transform, x_label=x_label, x_label_format_dict=x_label_format_dict,
        x_tick_labels=x_tick_labels, x_tick_label_format_dict=x_tick_label_format_dict, y_label=y_label,
        y_label_format_dict=y_label_format_dict, y_tick_labels=y_tick_labels,
        y_tick_label_format_dict=y_tick_label_format_dict, opposite_axis=opposite_axis)
    if x_tick_separator_locs is not None or y_tick_separator_locs is not None:
        draw_axis_tick_separator_and_label(
            current_ax, current_transform,
            x_tick_separator_locs=x_tick_separator_locs, x_tick_separator_format_dict=x_tick_separator_format_dict,
            x_tick_separator_labels=x_tick_separator_labels, x_tick_separator_label_locs=x_tick_separator_label_locs,
            x_tick_separator_label_format_dict=x_tick_separator_label_format_dict,
            y_tick_separator_locs=y_tick_separator_locs, y_tick_separator_format_dict=y_tick_separator_format_dict,
            y_tick_separator_labels=y_tick_separator_labels, y_tick_separator_label_locs=y_tick_separator_label_locs,
            y_tick_separator_label_format_dict=y_tick_separator_label_format_dict, opposite_axis=opposite_axis
        )



