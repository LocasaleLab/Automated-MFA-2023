from .built_in_packages import defaultdict
from .third_party_packages import plt, np
from .config import Color
from common_and_plotting_functions.functions import replace_invalid_file_name
from figure_plotting_package.common.core_plotting_functions import axis_appearance_setting, HeatmapValueFormat, \
    core_plot_violin_box_plot, core_single_ax_bar_plot, raw_heat_map_plotting, \
    violin_box_color_list_generator, heatmap_text_str_list_generator, core_scatter_plotting, raw_cbar_plotting
from figure_plotting_package.common.classes import Vector


def group_scatter_color_generator(
        complete_embedded_matrix, complete_obj_vector, category_start_end_index_dict,
        min_obj_value=None, max_obj_value=None):
    max_alpha = 1
    min_alpha = 0.2
    cmap_name = 'Set2'

    if min_obj_value is None:
        min_obj_value = np.min(complete_obj_vector)
    if max_obj_value is None:
        max_obj_value = np.max(complete_obj_vector)
    if min_obj_value is not None or max_obj_value is not None:
        complete_obj_vector = complete_obj_vector.clip(min_obj_value, max_obj_value)

    # To make the node with the smallest obj as the darkest one
    alpha_value_vector = min_alpha + (max_alpha - min_alpha) * (
            (max_obj_value - complete_obj_vector) / (max_obj_value - min_obj_value))
    cmap_colors = plt.get_cmap(cmap_name).colors
    scatter_data_dict = {}
    for index, (category_name, (start_index, end_index)) in enumerate(category_start_end_index_dict.items()):
        rgb_color_array = np.ones([end_index - start_index, 3]) * cmap_colors[index]
        rgba_complete_color_array = np.hstack([
            rgb_color_array, alpha_value_vector[start_index:end_index].reshape([-1, 1])])
        scatter_data_dict[category_name] = (
            complete_embedded_matrix[start_index:end_index, :], rgba_complete_color_array)
    return scatter_data_dict


def scatter_plot_for_simulated_result(
        scatter_data_dict, embedded_simulated_flux=None, figsize=None, output_direct=None, color_mapper=None):
    fig, ax = plt.subplots(figsize=figsize)
    # cmap = 'viridis'
    default_size = 3
    default_shape = 'o'
    default_setting = [default_size, default_shape]
    for label_name, (embedded_flux_array, color_value_array, *other_settings) in scatter_data_dict.items():
        try:
            marker_size = other_settings[0]
        except IndexError:
            marker_size = default_size
        else:
            if marker_size is None:
                marker_size = default_size
        try:
            marker_shape = other_settings[1]
        except IndexError:
            marker_shape = default_shape
        else:
            if marker_shape is None:
                marker_shape = default_shape
        core_scatter_plotting(
            ax, embedded_flux_array[:, 0], embedded_flux_array[:, 1], marker_size=marker_size,
            marker_shape=marker_shape, marker_color=color_value_array, label=label_name)
    if embedded_simulated_flux is not None:
        ax.plot(embedded_simulated_flux[0], embedded_simulated_flux[1], '+', color='orange', markersize=10)
    if color_mapper is not None:
        # user_defined_cbar_plotting(ax, color_mapper)
        raw_cbar_plotting(color_mapper, ax=ax)
    # ax.set_xticks(x_axis_position)
    # ax.set_xticklabels(tissue_label_list)
    # ax.set_title(current_title)
    # fig2 = plt.figure()
    # ax2 = fig2.add_subplot(111)
    # ax2.imshow(plt.get_cmap(cmap))
    if len(scatter_data_dict) > 1:
        ax.legend()
    if output_direct:
        fig.savefig(f'{output_direct}/embedded_figure.pdf', dpi=fig.dpi)


def multi_row_col_scatter_plot_for_result_selection(
        complete_data_dict, x_label_index_dict, y_label_index_dict, figure_title, output_direct=None,
        cutoff_value=None, ylim=None, figsize=None):
    base_y_size = 3
    base_x_size = 2
    column_width = 0.5
    edge = 0.1
    marker_size = 5

    row_num = len(y_label_index_dict)
    col_num = len(x_label_index_dict)

    if figsize is None:
        figsize = (base_x_size * col_num, base_y_size * row_num)
    if ylim is None:
        ylim = (0, None)
    fig = plt.figure(figsize=figsize)
    for y_label, current_y_data_dict in complete_data_dict.items():
        for x_label, current_subplot_data_array in current_y_data_dict.items():
            x_label_index = x_label_index_dict[x_label]
            y_label_index = y_label_index_dict[y_label]
            subplot_index = y_label_index * col_num + x_label_index + 1
            current_ax = fig.add_subplot(row_num, col_num, subplot_index)
            random_x_value = (np.random.random(len(current_subplot_data_array)) - 0.5) * column_width
            ##################### Deprecated #############################
            # current_ax.scatter(random_x_value, current_subplot_data_array, s=marker_size)
            # if y_label_index == row_num - 1:
            #     current_ax.set_xlabel(x_label)
            # current_ax.set_xticks([])
            # if x_label_index == 0:
            #     current_ax.set_ylabel(y_label)
            # else:
            #     current_ax.set_yticks([])
            # current_ax.set_xlim((-column_width / 2 - edge, column_width / 2 + edge))
            # current_ax.set_ylim(ylim)
            # if cutoff_value is not None:
            #     current_ax.axhline(cutoff_value, linestyle='--', color=Color.orange)
            ##################### Deprecated #############################
            if x_label_index == 0:
                y_ticks = None
                display_y_label = y_label
            else:
                y_ticks = []
                display_y_label = None
            if y_label_index != row_num - 1:
                display_x_label = None
            else:
                display_x_label = x_label
            # if x_label_index == 0:
            #     y_ticks = None
            # else:
            #     y_ticks = []
            #     y_label = None
            # if y_label_index != row_num - 1:
            #     x_label = None
            core_scatter_plotting(
                current_ax, random_x_value, current_subplot_data_array, marker_size,
                x_lim=(-column_width / 2 - edge, column_width / 2 + edge), x_ticks=[],
                y_lim=ylim, y_ticks=y_ticks, cutoff=cutoff_value, cutoff_param_dict={
                    'linestyle': '--', 'color': Color.orange
                })
            axis_appearance_setting(current_ax, x_label=display_x_label, y_label=display_y_label)
    fig.suptitle(figure_title)
    if output_direct is not None:
        current_title = replace_invalid_file_name(figure_title)
        fig.savefig('{}/scatter_plot_{}.png'.format(output_direct, current_title), dpi=fig.dpi)


def heat_map_plotting(
        data_matrix_with_nan, x_label_list, y_label_list, figure_title, output_direct,
        min_value=None, max_value=None, figsize=None, value_number_format=HeatmapValueFormat.no_text,
        cmap=None, xaxis_rotate=False):
    if cmap is None:
        cmap = 'coolwarm'
    text_colors = ('white', 'black')
    # text_colors = ("black", "black")

    row_num = len(y_label_list)
    col_num = len(x_label_list)
    base_y_size = 1
    base_x_size = 1

    if figsize is None:
        figsize = (base_x_size * col_num, base_y_size * row_num + 1)
    if row_num <= col_num:
        cbar_location = 'bottom'
    else:
        cbar_location = 'right'
    text_str_list = heatmap_text_str_list_generator(value_number_format, data_matrix_with_nan, col_num, row_num)

    fig, ax = plt.subplots(figsize=figsize)
    cbar_y_label_format_dict = {
        'rotation': -90,
        'verticalalignment': 'bottom'
    }
    raw_heat_map_plotting(
        ax, data_matrix_with_nan, cmap, min_value, max_value, col_num, row_num, color_bar=True,
        cbar_location=cbar_location, cbar_y_label_format_dict=cbar_y_label_format_dict, text_str_list=text_str_list)

    x_label_format_dict = {}
    if xaxis_rotate:
        x_label_format_dict['rotation'] = 20
    axis_appearance_setting(
        ax, x_tick_labels=x_label_list, x_tick_label_format_dict=x_label_format_dict, y_tick_labels=y_label_list)
    ax.set_title(figure_title)

    ##################### Deprecated #############################
    # im = ax.imshow(data_matrix_with_nan, cmap=cmap, vmin=min_value, vmax=max_value)
    # ax.set_xticks(np.arange(col_num))
    # if xaxis_rotate:
    #     rotate = 20
    # else:
    #     rotate = None
    # ax.set_xticklabels(x_label_list, rotation=rotate)
    # ax.set_yticks(np.arange(row_num))
    # ax.set_yticklabels(y_label_list)
    # ax.set_title(figure_title)
    # if row_num <= col_num:
    #     cbar_location = 'bottom'
    # else:
    #     cbar_location = 'right'
    # cbar = ax.figure.colorbar(im, ax=ax, location=cbar_location)
    # cbar.ax.set_ylabel('', rotation=-90, va='bottom')
    # if value_text != HeatmapValueFormat.no_text:
    #     kw = dict(
    #         horizontalalignment="center", verticalalignment="center")
    #     im_min = im.norm.vmin
    #     im_max = im.norm.vmax
    #     text_threshold_range = (0.75 * im_min + 0.25 * im_max, 0.25 * im_min + 0.75 * im_max)
    #     for x in range(col_num):
    #         for y in range(row_num):
    #             value = data_matrix_with_nan[y, x]
    #             if not np.isnan(value):
    #                 kw.update(color=text_colors[int(text_threshold_range[0] < value < text_threshold_range[1])])
    #                 im.axes.text(x, y, value_str_generator(value, value_text), **kw)
    #
    # if xaxis_rotate:
    #     rotate = 20
    # else:
    #     rotate = None
    # ax.set_xticklabels(x_label_list, rotation=rotate)
    # ax.set_yticklabels(y_label_list)
    ##################### Deprecated #############################
    if output_direct is not None:
        current_title = replace_invalid_file_name(figure_title)
        fig.savefig('{}/heatmap_plot_{}.png'.format(output_direct, current_title), dpi=fig.dpi)


def box_plot_3d(
        mean_matrix, lb_matrix, ub_matrix, x_label_list, y_label_list, figure_title, output_direct,
        z_lim=None, cutoff=0, figsize=None):
    box_size = 0.7
    bar_color = Color.blue
    bar_alpha = Color.alpha_for_bar_plot
    edge_color = Color.blue
    cutoff_color = Color.orange
    cutoff_alpha = Color.alpha_value

    row_num, col_num = mean_matrix.shape
    _x = np.arange(col_num)
    _y = np.arange(row_num)
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    flat_mean_matrix = mean_matrix.ravel()
    flat_lb_matrix = lb_matrix.ravel()
    flat_ub_matrix = ub_matrix.ravel()

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(
        x, y, flat_lb_matrix, box_size, box_size, flat_mean_matrix - flat_lb_matrix,
        color=bar_color, alpha=bar_alpha, edgecolor=edge_color, shade=True)
    ax.bar3d(
        x, y, flat_mean_matrix, box_size, box_size, flat_ub_matrix - flat_mean_matrix,
        color=bar_color, alpha=bar_alpha, edgecolor=edge_color, shade=True)
    cutoff_matrix = cutoff * np.ones_like(_xx)
    ax.plot_surface(_xx, _yy, cutoff_matrix, color=cutoff_color, alpha=cutoff_alpha)
    ax.set_xticks(_x)
    ax.set_xticklabels(x_label_list)
    ax.set_yticks(_y)
    ax.set_yticklabels(y_label_list)
    ax.set_zlim(z_lim)

    ax.set_title(figure_title)
    if output_direct is not None:
        current_title = replace_invalid_file_name(figure_title)
        fig.savefig('{}/3d_box_plot_{}.png'.format(output_direct, current_title), dpi=fig.dpi)


def group_violin_box_distribution_plot(
        nested_data_dict, nested_color_dict=None, nested_median_color_dict=None, cutoff_dict=None,
        emphasized_flux_dict=None, title_dict=None, output_direct=None, ylim=None, xaxis_rotate=False, figsize=None,
        figure_type='violin'):
    """
    Plot violin graph for distributions of a set of data_and_models.

    :param alpha:
    :param figure_type:
    :param xaxis_rotate:
    :param emphasized_flux_dict:
    :param nested_data_dict:
    :param nested_color_dict:
    :param nested_median_color_dict:
    :param title_dict:
    :param output_direct:
    :param ylim:
    :param figsize:
    :return:
    """

    common_line_width = 0.7
    default_figure_unit_width = 0.5
    figure_height = 5
    face_color_str = 'face_color'
    alpha_str = 'alpha'
    edge_color_str = 'edge_color'
    edge_width_str = 'edge_width'

    if title_dict is None:
        title_dict = {}
    if emphasized_flux_dict is None:
        emphasized_flux_dict = {}
    if cutoff_dict is None:
        cutoff_dict = {}

    cutoff_param_dict = {edge_color_str: Color.orange}

    for data_title, data_dict in nested_data_dict.items():
        if data_title in title_dict:
            current_title = title_dict[data_title]
        else:
            current_title = data_title

        if figsize is None:
            data_len = len(data_dict)
            if data_len == 1:
                data_len = 3
            elif data_len < 6:
                data_len = 6
            figsize = (data_len * default_figure_unit_width, figure_height)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        # if nested_color_dict is not None:
        #     this_nested_color_dict = nested_color_dict[data_title]
        # else:
        #     this_nested_color_dict = None
        # if nested_median_color_dict is not None:
        #     this_nested_median_color_dict = nested_median_color_dict[data_title]
        # else:
        #     this_nested_median_color_dict = None
        (
            data_list, data_label_list, body_color_dict_list, edge_color_dict_list, median_edge_color_dict_list
        ) = violin_box_color_list_generator(
            data_dict, nested_color_dict, nested_median_color_dict, Color.blue, Color.orange)

        box_violin_config_dict = {
            # 'body_props': [{face_color_str: color, alpha_str: 0.3} for color in color_list],
            # 'min_max_props': [{edge_color_str: color, edge_width_str: common_line_width} for color in color_list],
            # 'median_props': [{edge_color_str: color, edge_width_str: common_line_width} for color in median_color_list],
            'body_props': body_color_dict_list,
            'min_max_props': [
                {**color_dict, edge_width_str: common_line_width} for color_dict in edge_color_dict_list],
            'median_props': [
                {**color_dict, edge_width_str: common_line_width} for color_dict in median_edge_color_dict_list],
        }

        if data_title in cutoff_dict:
            cutoff = cutoff_dict[data_title]
        else:
            cutoff = None
        if data_title in emphasized_flux_dict:
            emphasized_flux_list = [emphasized_flux_dict[data_title][data_label] for data_label in data_label_list]
        else:
            emphasized_flux_list = None
        core_plot_violin_box_plot(
            ax, figure_type, data_list, np.arange(1, len(data_list) + 1), box_violin_config_dict,
            cutoff=cutoff, cutoff_param_dict=cutoff_param_dict, emphasized_flux_list=emphasized_flux_list, y_lim=ylim)

        x_label_format_dict = {'fontsize': 7}
        if xaxis_rotate:
            if isinstance(xaxis_rotate, bool):
                angle = 13
            elif isinstance(xaxis_rotate, (float, int)):
                angle = xaxis_rotate
            else:
                raise ValueError()
            x_label_format_dict['rotation'] = angle
        axis_appearance_setting(
            ax, x_tick_labels=data_label_list, x_tick_label_format_dict=x_label_format_dict)

        if output_direct:
            current_title = replace_invalid_file_name(current_title)
            fig.savefig("{}/{}_plot_{}.pdf".format(output_direct, figure_type, current_title), dpi=fig.dpi)


def single_axis_bar_plot(
        ax, array_data_dict, color_dict, error_bar_data_dict, current_title,
        array_len, bar_total_width, edge, cmap, ylim, xlabel_list, legend=True):
    bar_param_dict = {
        'alpha': Color.alpha_for_bar_plot
    }
    core_single_ax_bar_plot(
        ax, array_data_dict, color_dict, error_bar_data_dict, array_len,
        bar_total_width, edge, ylim, cmap=cmap, bar_param_dict=bar_param_dict)
    ax.set_title(current_title)
    if xlabel_list is None:
        xlabel_list = []
    if len(xlabel_list) != 0 and len(xlabel_list) != array_len:
        raise ValueError()
    ax.set_xticklabels(xlabel_list)
    if legend:
        ax.legend()


def group_bar_plot(
        complete_data_dict, error_bar_data_dict=None, color_dict=None,
        title_dict=None, output_direct=None, ylim=(0, 1), xlabel_list=None):
    def is_number(obj):
        return isinstance(obj, int) or isinstance(obj, float)

    def single_layer_array(input_obj):
        return (
                is_number(input_obj) or
                (isinstance(input_obj, np.ndarray) and len(input_obj.shape) == 1))

    def nested_array_list(input_obj):
        return (
                (isinstance(input_obj, list) and is_number(input_obj[0])) or
                isinstance(input_obj, list) and isinstance(input_obj[0], np.ndarray))

    edge = 0.05
    bar_total_width = 0.5
    cmap = plt.get_cmap('tab10')

    if error_bar_data_dict is None:
        error_bar_data_dict = {}
    if title_dict is None:
        title_dict = {}
    if color_dict is None:
        color_dict = {}

    for emu_name, data_dict in complete_data_dict.items():
        if emu_name in title_dict:
            current_title = title_dict[emu_name]
        else:
            current_title = emu_name

        if emu_name in error_bar_data_dict:
            current_error_bar_data_dict = error_bar_data_dict[emu_name]
        else:
            current_error_bar_data_dict = {}

        ##################### Deprecated #############################
        # first_data_vector = list(data_dict.values())[0]
        # if nested_array_list(first_data_vector):
        #     if is_number(first_data_vector[0]):
        #         array_len = 1
        #     else:
        #         array_len = len(first_data_vector[0])
        # elif single_layer_array(first_data_vector):
        #     if is_number(first_data_vector):
        #         array_len = 1
        #     else:
        #         array_len = len(first_data_vector)
        # else:
        #     raise TypeError("Not recognized input: {}".format(first_data_vector))
        ##################### Deprecated #############################

        first_data_vector = iter(data_dict.values()).__next__()
        array_len = len(first_data_vector)

        fig, ax = plt.subplots()
        single_axis_bar_plot(
            ax, data_dict, color_dict, current_error_bar_data_dict, current_title,
            array_len, bar_total_width, edge, cmap, ylim, xlabel_list, legend=True)

        if output_direct:
            current_title = replace_invalid_file_name(current_title)
            fig.savefig("{}/bar_plot_{}.png".format(output_direct, current_title), dpi=fig.dpi)


def multi_row_col_bar_plot(
        complete_data_dict, target_emu_name_nested_list, row_num, col_num, error_bar_data_dict=None, color_dict=None,
        title_dict=None, output_direct=None, current_title='', ylim=(0, 1), xlabel_list=None, figsize=None,
        legend=True):
    base_row_size = 6
    base_col_size = 6
    edge = 0.05
    bar_total_width = 0.5
    cmap = plt.get_cmap('tab10')

    if error_bar_data_dict is None:
        error_bar_data_dict = {}
    if title_dict is None:
        title_dict = {}
    if color_dict is None:
        color_dict = {}

    if figsize is None:
        figsize = (base_col_size * col_num, base_row_size * row_num)

    assert len(target_emu_name_nested_list) == row_num
    fig = plt.figure(figsize=figsize)

    subplot_index = 0
    for row_index, emu_name_row_list in enumerate(target_emu_name_nested_list):
        assert len(emu_name_row_list) == col_num
        for col_index, emu_name in enumerate(emu_name_row_list):
            valid = True
            data_dict = {}
            subplot_index += 1
            if emu_name is None:
                valid = False
            try:
                data_dict = complete_data_dict[emu_name]
            except KeyError:
                valid = False
            if valid:
                if emu_name in title_dict:
                    subplot_title = title_dict[emu_name]
                else:
                    subplot_title = emu_name
                if emu_name in error_bar_data_dict:
                    current_error_bar_data_dict = error_bar_data_dict[emu_name]
                else:
                    current_error_bar_data_dict = {}

                # first_data_vector = list(data_dict.values())[0]
                if len(data_dict) == 0:
                    continue
                first_data_vector = iter(data_dict.values()).__next__()
                array_len = len(first_data_vector)
                current_ax = fig.add_subplot(row_num, col_num, subplot_index)
                single_axis_bar_plot(
                    current_ax, data_dict, color_dict, current_error_bar_data_dict, subplot_title,
                    array_len, bar_total_width, edge, cmap, ylim, xlabel_list, legend=legend)
    # fig.suptitle(title)
    if output_direct:
        current_title = replace_invalid_file_name(current_title)
        fig.savefig("{}/multi_bar_plot_{}.pdf".format(output_direct, current_title), dpi=fig.dpi)


def group_box_distribution_plot(
        nested_data_dict, output_direct=None, title_dict=None, broken_yaxis=None):
    """
    Plot box graph for distributions of a set of data_and_models.

    :param nested_data_dict: Dict of the data_and_models set, in which key is their name and value is data_and_models array.
    :param output_direct: Save path for the whole figure.
    :param title_dict: Figure title.
    :param broken_yaxis: Deprecated. Whether y-axis is broken.
    :return: None
    """

    def color_edges(box_parts):
        for part_name, part_list in box_parts.items():
            if part_name == 'medians':
                current_color = Color.orange
            else:
                current_color = Color.blue
            for part in part_list:
                part.set_color(current_color)

    if title_dict is None:
        title_dict = {}

    for data_title, data_dict in nested_data_dict.items():
        if data_title in title_dict:
            current_title = title_dict[data_title]
        else:
            current_title = data_title
        data_list_for_box = data_dict.values()
        tissue_label_list = data_dict.keys()
        x_axis_position = np.arange(1, len(tissue_label_list) + 1)

        if broken_yaxis is None:
            fig, ax = plt.subplots()
            parts = ax.boxplot(data_list_for_box, whis=(0, 100))
            color_edges(parts)
            ax.set_xticks(x_axis_position)
            ax.set_xticklabels(tissue_label_list)
            ax.set_title(current_title)
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            parts1 = ax1.boxplot(data_list_for_box, whis='range')
            parts2 = ax2.boxplot(data_list_for_box, whis='range')
            color_edges(parts1)
            color_edges(parts2)
            ax1.set_ylim([broken_yaxis[1], None])
            ax2.set_ylim([-50, broken_yaxis[0]])
            ax1.spines['bottom'].set_visible(False)
            ax2.spines['top'].set_visible(False)
            ax1.xaxis.tick_top()
            ax2.set_xticks(x_axis_position)
            ax2.set_xticklabels(tissue_label_list)
            ax1.set_title(current_title)
        if output_direct:
            fig.savefig("{}/box_plot_{}.png".format(output_direct, current_title), dpi=fig.dpi)


class FigurePlotting(object):
    def __init__(self, ParameterName, Elements):
        self.ParameterName = ParameterName
        self.Figure = Elements.Figure
        self.Elements = Elements
        self.default_figure_size = Vector(8.5, 8.5)

    def _common_draw_function(
            self, figure_name, target_obj, figure_output_direct, figure_size=None):
        if figure_size is None:
            figure_size = self.default_figure_size
        if isinstance(target_obj, (tuple, list)):
            other_obj_list = target_obj
        else:
            other_obj_list = [target_obj]
        current_figure = self.Figure(
            figure_name, other_obj_list=other_obj_list, figure_size=figure_size,
            figure_output_direct=figure_output_direct)
        current_figure.draw()

    def metabolic_flux_model_function(
            self, figure_output_direct, figure_name,
            input_metabolite_set, c13_labeling_metabolite_set, mid_data_metabolite_set, mixed_mid_data_metabolite_set,
            biomass_metabolite_set, boundary_flux_set, current_reaction_value_dict=None, infusion=False,
            figure_size=None):
        ParameterName = self.ParameterName
        experimental_setting_dict = {
            ParameterName.input_metabolite_set: input_metabolite_set,
            ParameterName.c13_labeling_metabolite_set: c13_labeling_metabolite_set,
            ParameterName.mid_data_metabolite_set: mid_data_metabolite_set,
            ParameterName.mixed_mid_data_metabolite_set: mixed_mid_data_metabolite_set,
            ParameterName.biomass_metabolite_set: biomass_metabolite_set,
            ParameterName.boundary_flux_set: boundary_flux_set,
        }
        metabolic_network_config_dict = {
            ParameterName.bottom_left_offset: Vector(0.1, 0.1),
            ParameterName.scale: 0.8,
            ParameterName.infusion: infusion,
            **experimental_setting_dict
        }
        if current_reaction_value_dict is not None:
            metabolic_network_config_dict.update({
                ParameterName.reaction_raw_value_dict: current_reaction_value_dict,
                ParameterName.visualize_flux_value: ParameterName.transparency
            })
        metabolic_network_obj = self.Elements.MetabolicNetwork(**metabolic_network_config_dict)
        self._common_draw_function(
            figure_name, metabolic_network_obj, figure_output_direct, figure_size)

    def mid_prediction_function(
            self, data_name, result_label, mid_name_list, output_direct, figure_config_dict, figure_size=None):
        ParameterName = self.ParameterName
        current_mid_comparison_figure_config_dict = {
            # ParameterName.bottom_left: Vector(0.15, 0.05),
            # ParameterName.size: Vector(1, 0.8),
            ParameterName.bottom_left_offset: Vector(0.15, 0.05),
            ParameterName.scale: 0.7,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.legend: False,
                ParameterName.data_name: data_name,
                ParameterName.result_label: result_label,
                ParameterName.mid_name_list: mid_name_list,
            },
        }
        try:
            new_figure_data_parameter_dict = figure_config_dict.pop(ParameterName.figure_data_parameter_dict)
        except KeyError:
            new_figure_data_parameter_dict = {}
        current_mid_comparison_figure_config_dict[ParameterName.figure_data_parameter_dict].update(
            new_figure_data_parameter_dict)
        current_mid_comparison_figure_config_dict.update(figure_config_dict)
        mid_comparison_figure = self.Elements.MIDComparisonGridBarWithLegendDataFigure(
            **current_mid_comparison_figure_config_dict)
        # output_file_path = f'{output_direct}/{result_label}.pdf'
        # if figure_size is None:
        #     figure_size = self.default_figure_size
        # current_figure = self.Figure(
        #     result_label, other_obj_list=[mid_comparison_figure], figure_size=figure_size,
        #     figure_output_direct=output_direct)
        # current_figure.draw()
        self._common_draw_function(
            result_label, mid_comparison_figure, output_direct, figure_size)

    def multi_tumor_figure_plotting(
            self, data_name, flux_location_nested_list, output_direct, figure_size):
        ParameterName = self.ParameterName

        figure_data_parameter_dict = {
            ParameterName.data_name: ParameterName.multiple_tumor,
            ParameterName.comparison_name: '',
            ParameterName.flux_name_list: flux_location_nested_list,
            ParameterName.color_dict: {
                'kidney': 'blue',
                'lung': 'orange',
                'brain': 'purple',
            }
        }
        loss_grid_comparison_figure = self.Elements.FluxComparisonScatterWithTitle(**{
            ParameterName.total_width: 0.4,
            ParameterName.bottom_left_offset: Vector(0.15, 0.15),
            ParameterName.scale: 2,
            ParameterName.figure_data_parameter_dict: figure_data_parameter_dict,
        })
        figure_name = f'grid_flux_comparison_{data_name}'
        # current_figure = self.Figure(
        #     figure_name, other_obj_list=[loss_grid_comparison_figure], figure_size=figure_size,
        #     figure_output_direct=output_direct)
        # current_figure.draw()
        self._common_draw_function(
            figure_name, loss_grid_comparison_figure, output_direct, figure_size)

