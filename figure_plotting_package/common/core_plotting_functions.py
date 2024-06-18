from .built_in_packages import enum, defaultdict, it
from .third_party_packages import plt, np, mcolors, cm, mpatches
from .light_weight_functions import round_to_str_with_fixed_point, default_parameter_extract

shape_category_list = ['o', 'v', 's', '^']
random_seed = np.random.default_rng(4536251)


def cmap_listed_mapper_generator(color_list):
    return mcolors.ListedColormap(color_list)


def cmap_mapper_generator(cmap, min_value=None, max_value=None):
    if isinstance(cmap, str):
        cmap_obj = plt.get_cmap(cmap)
    elif isinstance(cmap, mcolors.Colormap):
        cmap_obj = cmap
    else:
        raise ValueError()
    if isinstance(cmap, mcolors.ListedColormap) and min_value is None and max_value is None:
        min_value = 0
        max_value = cmap.N
    norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
    mapper = cm.ScalarMappable(norm=norm, cmap=cmap_obj)
    return mapper, cmap_obj


def axis_numeric_setting(ax, x_lim=None, x_ticks=None, y_lim=None, y_ticks=None, **kwargs):
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    if x_ticks is not None:
        ax.set_xticks(x_ticks)
    if y_ticks is not None:
        ax.set_yticks(y_ticks)


def axis_appearance_setting(
        ax, x_label=None, x_label_format_dict=None, x_tick_labels=None, x_tick_label_format_dict=None,
        y_label=None, y_label_format_dict=None, y_tick_labels=None, y_tick_label_format_dict=None, **kwargs):
    axis_parameter_map = {
        # 'edgecolor': 'color',
        # 'linewidth': 'width',
        'fontsize': 'labelsize',
        'color': 'labelcolor',
        'fontname': 'fontname',
    }
    if x_label is not None:
        if x_label_format_dict is None:
            x_label_format_dict = {}
        ax.set_xlabel(x_label, **x_label_format_dict)
    if x_tick_labels is not None:
        if x_tick_label_format_dict is None:
            x_tick_label_format_dict = {}
        ax.set_xticklabels(x_tick_labels, **x_tick_label_format_dict)
    elif x_tick_label_format_dict is not None:
        # updated_x_tick_label_format_dict = {
        #     axis_parameter_map[key]: value for key, value in x_tick_label_format_dict.items()}
        # ax.tick_params('x', **updated_x_tick_label_format_dict)
        ax.set_xticklabels(ax.get_xticks(), **x_tick_label_format_dict)
        # ax.set_xticklabels(ax.get_xticklabels(), **x_tick_label_format_dict)
    if y_label is not None:
        if y_label_format_dict is None:
            y_label_format_dict = {}
        ax.set_ylabel(y_label, **y_label_format_dict)
    if y_tick_labels is not None:
        if y_tick_label_format_dict is None:
            y_tick_label_format_dict = {}
        ax.set_yticklabels(y_tick_labels, **y_tick_label_format_dict)
    elif y_tick_label_format_dict is not None:
        # updated_y_tick_label_format_dict = {
        #     axis_parameter_map[key]: value for key, value in y_tick_label_format_dict.items()}
        # ax.tick_params('y', **updated_y_tick_label_format_dict)
        ax.set_yticklabels(ax.get_yticks(), **y_tick_label_format_dict)
        # ax.set_yticklabels(ax.get_yticklabels(), **y_tick_label_format_dict)


def violin_box_color_list_generator(
        data_dict, color_dict=None, median_color_dict=None, default_color=None, default_median_color=None,
        default_body_alpha=0.3):
    def decipher_single_color(_color_obj, _default_body_alpha=default_body_alpha):
        _is_dict = False
        if isinstance(_color_obj, dict):
            _is_dict = True
            _pure_color = _color_obj[face_color_str]
            _alpha = None
        elif isinstance(_color_obj, np.ndarray):
            if len(_color_obj) == 3:
                _pure_color = _color_obj
                _alpha = _default_body_alpha
            elif len(_color_obj) == 4:
                _pure_color = _color_obj[:3]
                _alpha = _color_obj[3]
            else:
                raise ValueError()
        elif isinstance(_color_obj, tuple) and len(_color_obj) == 2:
            _pure_color = _color_obj[0]
            _alpha = _color_obj[1]
        else:
            raise ValueError()
        return _is_dict, _pure_color, _alpha

    face_color_str = 'face_color'
    alpha_str = 'alpha'
    edge_color_str = 'edge_color'
    edge_width_str = 'edge_width'

    data_list = data_dict.values()
    data_label_list = data_dict.keys()
    body_color_dict_list = []
    edge_color_dict_list = []
    median_edge_color_dict_list = []
    same_color_median = False
    single_color_array = None
    single_color_alpha = None
    single_median_color_array = None
    if color_dict is not None:
        if isinstance(color_dict, np.ndarray):
            color_dict_array = color_dict
            color_dict = defaultdict(lambda: color_dict_array)
            _, pure_color, alpha = decipher_single_color(color_dict)
            single_color_array = pure_color
            single_color_alpha = alpha
        if median_color_dict is not None:
            if isinstance(median_color_dict, np.ndarray):
                median_color_dict_array = median_color_dict
                median_color_dict = defaultdict(lambda: median_color_dict_array)
                _, pure_median_color, _ = decipher_single_color(median_color_dict)
                single_median_color_array = pure_median_color
        else:
            same_color_median = True
    elif default_color is not None and default_median_color is not None:
        color_dict = defaultdict(lambda: default_color)
        median_color_dict = defaultdict(lambda: default_median_color)
        _, pure_color, alpha = decipher_single_color(default_color)
        _, pure_median_color, _ = decipher_single_color(default_median_color)
        single_color_array = pure_color
        single_color_alpha = alpha
        single_median_color_array = pure_median_color
    else:
        raise ValueError()

    if single_color_array is not None and single_color_alpha is not None:
        body_color_dict_list = [
            {face_color_str: single_color_array, alpha_str: single_color_alpha} for _ in data_label_list]
        edge_color_dict_list = [
            {edge_color_str: body_color_dict[face_color_str]} for body_color_dict in body_color_dict_list]
    else:
        body_color_dict_list = []
        edge_color_dict_list = []
        for key in data_label_list:
            color_obj = color_dict[key]
            is_dict, pure_color, alpha = decipher_single_color(color_obj)
            if is_dict:
                body_color_dict_list.append(dict(color_obj))
            else:
                body_color_dict_list.append({face_color_str: pure_color, alpha_str: alpha})
            edge_color_dict_list.append({edge_color_str: pure_color})
    if same_color_median:
        median_edge_color_dict_list = [
            {edge_color_str: body_color_dict[face_color_str]} for body_color_dict in body_color_dict_list]
    elif single_median_color_array is not None:
        median_edge_color_dict_list = [
            {edge_color_str: single_median_color_array} for _ in data_label_list]
    else:
        median_edge_color_dict_list = []
        for key in data_label_list:
            median_color_obj = median_color_dict[key]
            is_dict, pure_color, _ = decipher_single_color(median_color_obj)
            median_edge_color_dict_list.append({edge_color_str: pure_color})

    # for color in color_list:
    #     if isinstance(color, dict):
    #         body_color_dict_list.append(dict(color))
    #         pure_color = color[face_color_str]
    #     elif isinstance(color, np.ndarray):
    #         if len(color) == 3:
    #             pure_color = color
    #             alpha = 0.3
    #         elif len(color) == 4:
    #             pure_color = color[:3]
    #             alpha = color[3]
    #         else:
    #             raise ValueError()
    #         body_color_dict_list.append({face_color_str: pure_color, alpha_str: alpha})
    #     elif isinstance(color, tuple) and len(color) == 2:
    #         pure_color = color[0]
    #         alpha = color[1]
    #         body_color_dict_list.append({face_color_str: pure_color, alpha_str: alpha})
    #     else:
    #         raise ValueError()
    #     edge_color_dict_list.append({edge_color_str: pure_color, edge_width_str: common_line_width})
    # for median_color in median_color_list:
    #     if isinstance(median_color, dict):
    #         pure_color = median_color[face_color_str]
    #     median_edge_color_dict_list.append({edge_color_str: pure_color, edge_width_str: common_line_width})
    # color_list = [color_dict[key] for key in data_label_list]
    # median_color_list = [median_color_dict[key] for key in data_label_list]
    return data_list, data_label_list, body_color_dict_list, edge_color_dict_list, median_edge_color_dict_list


def heatmap_value_str_generator(decimal_value, str_format):
    if str_format == HeatmapValueFormat.raw_floating_format:
        return round_to_str_with_fixed_point(decimal_value, 4)
        # return '{:.4f}'.format(decimal_value)
    elif str_format == HeatmapValueFormat.percentage_format:
        return f'{round_to_str_with_fixed_point(decimal_value * 100, 1)}%'
        # return '{:.1%}'.format(decimal_value)
    else:
        if 1 < np.abs(decimal_value) < 10:
            return round_to_str_with_fixed_point(decimal_value, 2)
        elif 10 < np.abs(decimal_value) < 100:
            return round_to_str_with_fixed_point(decimal_value, 1)
            # return '{:.1f}'.format(decimal_value)
        elif 100 < np.abs(decimal_value) < 1000:
            return round_to_str_with_fixed_point(decimal_value, 0)
            # return '{:.0f}'.format(decimal_value)
        elif 0.01 < np.abs(decimal_value) < 1:
            return round_to_str_with_fixed_point(decimal_value, 3)
        raw_value_str = '{:.1e}'.format(decimal_value)
        mantissa, exp = raw_value_str.split('e')
        if len(exp) > 3 or exp[1] != '0':
            return raw_value_str
        else:
            return '{}e{}{}'.format(mantissa, exp[0], exp[2])


def heatmap_text_str_list_generator(
        value_number_format, data_matrix_with_nan, col_num, row_num, text_color=('white', 'black'),
        font=None, font_weight=None, font_size=None, z_order=None):
    # if common_text_kw is None:
    #     common_text_kw = {}
    partition = (0.25, 0.75)
    if value_number_format == HeatmapValueFormat.no_text:
        text_str_list = None
    else:
        text_str_list = []
        raw_im_min = np.nanmin(data_matrix_with_nan)
        raw_im_max = np.nanmax(data_matrix_with_nan)
        if raw_im_min < 0:
            max_abs = max(abs(raw_im_min), abs(raw_im_max))
            im_min = -max_abs
            im_max = max_abs
        else:
            im_min = 0
            im_max = raw_im_max
        text_threshold_range = (
            partition[1] * im_min + partition[0] * im_max, partition[0] * im_min + partition[1] * im_max)
        for x in range(col_num):
            for y in range(row_num):
                value = data_matrix_with_nan[y, x]
                if not np.isnan(value):
                    if isinstance(text_color, (list, tuple)) and len(text_color) == 2:
                        current_color = text_color[int(text_threshold_range[0] < value < text_threshold_range[1])]
                    else:
                        current_color = text_color
                    kw = {
                        # **common_text_kw,
                        'fontname': font,
                        'fontsize': font_size,
                        'fontweight': font_weight,
                        'horizontalalignment': 'center',
                        'verticalalignment': 'center',
                        'color': current_color,
                        'zorder': z_order,
                    }
                    text_str_list.append((x, y, heatmap_value_str_generator(value, value_number_format), kw))
    return text_str_list


class HeatmapValueFormat(enum.Enum):
    no_text = 0
    scientific_format = 1
    percentage_format = 2
    raw_floating_format = 3


def heatmap_and_box3d_parameter_preparation(data_dict, percentage=False):
    """
    :param data_dict: Nested dict with y-first, x-second
    :param percentage:
    :return:
    """
    mean_matrix_list = []
    std_matrix_list = []
    for y_label, each_y_data_dict in data_dict.items():
        this_col_mean_list = []
        this_col_std_list = []
        if len(each_y_data_dict) == 0:
            raise ValueError(f'Empty row! {y_label} in\n{data_dict}')
        for x_label, each_location_data_list in each_y_data_dict.items():
            if len(each_location_data_list) == 0:
                this_col_mean_list.append(np.nan)
                this_col_std_list.append(np.nan)
            else:
                this_col_mean_list.append(np.mean(each_location_data_list))
                this_col_std_list.append(np.std(each_location_data_list))
        mean_matrix_list.append(this_col_mean_list)
        std_matrix_list.append(this_col_std_list)
    mean_matrix = np.array(mean_matrix_list)
    std_matrix = np.array(std_matrix_list)
    min_mean_value = np.nanmin(mean_matrix)
    mean_abs_max_value = np.nanmax(np.abs(mean_matrix))
    if min_mean_value > 0:
        mean_lim_pair = (0, None)
    else:
        mean_lim_pair = (-mean_abs_max_value, mean_abs_max_value)
    if percentage:
        mean_value_text_format = HeatmapValueFormat.percentage_format
    else:
        mean_value_text_format = HeatmapValueFormat.scientific_format
    return mean_matrix, std_matrix, mean_lim_pair, mean_value_text_format


def heatmap_plot_wrap_func_with_text(
        ax, data_matrix_with_nan, cmap, min_value=None, max_value=None, z_order=None, alpha=None, text_str_list=None):
    """
    This function repair problems of native stupid heatmap function in matplotlib. Final figure will be exactly at the
    position of ax
    """
    if min_value is None:
        min_value = np.nanmin(data_matrix_with_nan)
    if max_value is None:
        max_value = np.nanmax(data_matrix_with_nan)
    mapper, cmap_obj = cmap_mapper_generator(cmap, min_value=min_value, max_value=max_value)
    y_size, x_size = data_matrix_with_nan.shape
    ax.set_xlim(-0.5, x_size - 0.5)
    ax.set_xticks(np.arange(x_size))
    ax.set_xticklabels([])
    ax.set_ylim(y_size - 0.5, -0.5)
    ax.set_yticks(np.arange(y_size))
    ax.set_yticklabels([])
    for row_index in range(y_size):
        for col_index in range(x_size):
            current_num = data_matrix_with_nan[row_index, col_index]
            if np.isnan(current_num):
                continue
            current_face_color = mapper.to_rgba(current_num)
            if alpha is not None:
                assert 0 <= alpha <= 1
                current_face_color = (*current_face_color[:3], alpha)
            x_anchor_point = col_index - 0.5
            y_anchor_point = row_index - 0.5
            mpl_patch = mpatches.Rectangle(
                (x_anchor_point, y_anchor_point), width=1, height=1, linewidth=None, edgecolor=None,
                facecolor=current_face_color, zorder=z_order)
            current_patch = ax.add_patch(mpl_patch)
    if text_str_list is not None:
        for x, y, value_str, kw in text_str_list:
            ax.text(x, y, value_str, **kw)
    return mapper


def core_heatmap_plotting(
        ax, data_matrix_with_nan, cmap, im_min_value, im_max_value, col_num, row_num, im_param_dict=None,
        text_str_list=None):
    if im_param_dict is None:
        im_param_dict = {}
    im = heatmap_plot_wrap_func_with_text(
        ax, data_matrix_with_nan, cmap=cmap, min_value=im_min_value, max_value=im_max_value,
        text_str_list=text_str_list, **im_param_dict)
    axis_numeric_setting(ax, x_ticks=np.arange(col_num), y_ticks=np.arange(row_num))
    return im


def core_cbar_plotting(ax, plot_obj, cbar_orientation='horizontal', z_order=None, ticks=None):
    norm = plot_obj.norm
    min_value = norm.vmin
    max_value = norm.vmax
    inch_per_square = 0.01
    figure_width, figure_height = ax.figure.get_size_inches()
    *_, ax_relative_width, ax_relative_height = ax.get_position().bounds
    if cbar_orientation == 'horizontal':
        horizontal = True
        set_bar_lim_function = ax.set_xlim
        set_bar_tick_function = ax.set_xticks
        set_bar_tick_label_function = ax.set_xticklabels
        set_empty_tick_function = ax.set_yticks
        axis_square_num = int(np.ceil(figure_width * ax_relative_width / inch_per_square))
    elif cbar_orientation == 'vertical':
        horizontal = False
        set_bar_lim_function = ax.set_xlim
        set_bar_tick_function = ax.set_xticks
        set_bar_tick_label_function = ax.set_xticklabels
        set_empty_tick_function = ax.set_yticks
        axis_square_num = int(np.ceil(figure_height * ax_relative_height / inch_per_square))
    else:
        raise ValueError()
    set_bar_lim_function(min_value, max_value)
    if ticks is not None:
        set_bar_tick_function(ticks)
    set_bar_tick_label_function([])
    set_empty_tick_function([])
    square_width = (max_value - min_value) / axis_square_num
    for variable_value in np.linspace(min_value, max_value, axis_square_num):
        current_face_color = plot_obj.to_rgba(variable_value)
        if horizontal:
            center = (variable_value - 0.5 * square_width, 0)
            width = square_width
            height = 1
        else:
            center = (0, variable_value - 0.5 * square_width)
            width = 1
            height = square_width
        mpl_patch = mpatches.Rectangle(
            center, width=width, height=height, linewidth=None, edgecolor=None,
            facecolor=current_face_color, zorder=z_order)
        current_patch = ax.add_patch(mpl_patch)


def raw_cbar_plotting(plot_obj, cbar_ax=None, ax=None, cbar_location=None, cbar_orientation=None):
    if cbar_ax is not None:
        cbar = cbar_ax.figure.colorbar(plot_obj, cax=cbar_ax, orientation=cbar_orientation)
    elif ax is not None:
        if cbar_location is None:
            ax_size = ax.get_position().size
            if ax_size[0] > ax_size[1]:
                vertical = False
            else:
                vertical = True
            # cbar_location = 'vertical' if vertical else 'horizontal'
            cbar_location = 'right' if vertical else 'bottom'
        cbar = ax.figure.colorbar(plot_obj, ax=ax, location=cbar_location, orientation=cbar_orientation)
    else:
        raise ValueError('cbar_ax and ax cannot be None simultaneously!')
    return cbar


def raw_heatmap_plot_wrap_func(
        ax, data_matrix, cmap, min_value, max_value, z_order=None, alpha=None):
    """
    This stupid function will generate a blank edge on bottom of set axis location, which makes axis unaligned with
    other elements. This adjusted position cannot be moved back by axes.set_position() function
    Only used in simple plotting.
    """
    im = ax.imshow(data_matrix, cmap=cmap, vmin=min_value, vmax=max_value, zorder=z_order, aspect='equal')
    return im


def raw_heat_map_plotting(
        ax, data_matrix_with_nan, cmap, im_min_value, im_max_value, col_num, row_num, im_param_dict=None,
        color_bar=True, cbar_location=None, cbar_y_label='', cbar_y_label_format_dict=None, text_str_list=None):
    if im_param_dict is None:
        im_param_dict = {}
    # im = ax.imshow(data_matrix_with_nan, cmap=cmap, vmin=im_min_value, vmax=im_max_value, **im_param_dict)
    im = raw_heatmap_plot_wrap_func(
        ax, data_matrix_with_nan, cmap=cmap, min_value=im_min_value, max_value=im_max_value, **im_param_dict)
    axis_numeric_setting(ax, x_ticks=np.arange(col_num), y_ticks=np.arange(row_num))
    if color_bar:
        cbar = raw_cbar_plotting(im, ax=ax, cbar_location=cbar_location)
        axis_appearance_setting(cbar.ax, y_label=cbar_y_label, y_label_format_dict=cbar_y_label_format_dict)
    if text_str_list is not None:
        for x, y, value_str, kw in text_str_list:
            ax.text(x, y, value_str, **kw)
    return im


def scatter_plot_wrap_func(
        ax, x_array, y_array, marker_size, marker_color, marker_shape, label=None, edge_width=None, edge_color=None,
        z_order=None, alpha=None):
    if edge_width is None or edge_color is None:
        edge_color = 'none'
    ax.scatter(
        x_array, y_array, s=marker_size, c=marker_color, marker=marker_shape, label=label,
        edgecolors=edge_color, linewidths=edge_width, zorder=z_order, alpha=alpha)


def core_scatter_plotting(
        ax, x_array, y_array, marker_size=None, marker_color=None, marker_shape=None,
        x_lim=None, x_ticks=None, y_lim=None, y_ticks=None, label=None, scatter_param_dict=None,
        cutoff=None, cutoff_param_dict=None, **kwargs):
    if scatter_param_dict is None:
        scatter_param_dict = {}
    scatter_plot_wrap_func(
        ax, x_array, y_array, marker_size, marker_color, marker_shape, label=label, **scatter_param_dict)
    axis_numeric_setting(ax, x_lim, x_ticks, y_lim, y_ticks)
    if cutoff is not None:
        if cutoff_param_dict is None:
            cutoff_param_dict = {}
        core_cutoff_plotting(ax, cutoff, **cutoff_param_dict)


def core_plot_violin_box_plot(
        ax, figure_type, data_list, positions, box_violin_config_dict, cutoff=None, cutoff_param_dict=None,
        emphasized_flux_list=None, x_lim=None, y_lim=None, x_ticks=None, y_ticks=None):
    # TODO: Merge data_list and positions to form like core_single_bar_plot
    def judge_equal_type_with_number(item1, item2):
        if isinstance(item1, (float, int)) and isinstance(item2, (float, int)):
            return True
        else:
            return type(item1) is type(item2)

    def judge_equal_value(item1, item2):
        if isinstance(item1, np.ndarray) and isinstance(item2, np.ndarray):
            return np.any(item1 != item2)
        else:
            return item1 != item2

    def combine_props(props_dict_list):
        final_complete_props_dict = {}
        for prop_dict in props_dict_list:
            for item_name in prop_dict.keys():
                if item_name not in final_complete_props_dict:
                    final_complete_props_dict[item_name] = None
        for index, prop_dict in enumerate(props_dict_list):
            for item_name, final_props_dict_item in final_complete_props_dict.items():
                # final_props_dict_item = final_complete_props_dict[item_name]
                if final_props_dict_item is None:
                    if item_name not in prop_dict:
                        final_complete_props_dict[item_name] = [None]
                    else:
                        final_complete_props_dict[item_name] = prop_dict[item_name]
                else:
                    if item_name not in prop_dict:
                        if isinstance(final_props_dict_item, list):
                            final_props_dict_item.append(None)
                        else:
                            final_complete_props_dict[item_name] = [
                                final_props_dict_item for _ in range(index)] + [None]
                    else:
                        current_prop_item = prop_dict[item_name]
                        if not judge_equal_type_with_number(final_props_dict_item, current_prop_item):
                            if isinstance(final_props_dict_item, list):
                                if final_props_dict_item[-1] is None \
                                        or judge_equal_type_with_number(final_props_dict_item[-1], current_prop_item):
                                    final_props_dict_item.append(current_prop_item)
                                else:
                                    # This will not happen. Item with different type will not be inserted into list
                                    raise ValueError()
                            else:
                                raise ValueError()
                        elif judge_equal_value(final_props_dict_item, current_prop_item):
                            final_complete_props_dict[item_name] = [
                                final_props_dict_item for _ in range(index)] + [current_prop_item]
        return final_complete_props_dict

    def set_parameter_of_obj(obj, current_part_name, edge_width=None, edge_color=None, face_color=None, alpha=None):
        param_dict = {}
        if edge_width is not None:
            param_dict['linewidth'] = edge_width
        if edge_color is not None:
            if current_part_name == min_max_type or current_part_name == median_type:
                param_dict['color'] = edge_color
            else:
                param_dict['edgecolor'] = edge_color
        if face_color is not None:
            param_dict['facecolor'] = face_color
        if alpha is not None:
            param_dict['alpha'] = alpha
        obj.set(**param_dict)

    assert len(data_list) == len(positions)
    # color_list could be inserted into body_props
    # try:
    #     body_props_list = box_violin_config_dict['body_props']
    # except KeyError:
    #     body_props_list = None
    # try:
    #     min_max_props_list = box_violin_config_dict['min_max_props']
    # except KeyError:
    #     min_max_props_list = {}
    # try:
    #     median_props_list = box_violin_config_dict['median_props']
    # except KeyError:
    #     median_props_list = None
    # try:
    #     widths = box_violin_config_dict['column_width']
    # except KeyError:
    #     if figure_type == 'violin':
    #         widths = 0.9
    #     else:
    #         widths = 0.8
    (
        body_props_list, min_max_props_list, median_props_list, widths
    ) = default_parameter_extract(box_violin_config_dict, [
        'body_props', 'min_max_props', 'median_props', 'column_width'
    ], [
        None, {}, None, 0.9 if figure_type == 'violin' else 0.8
    ])

    # edge_width_str = 'linewidth'
    # face_color_str = 'facecolor'
    # edge_color_str = 'edgecolor'
    # color_str = 'color'
    # alpha_str = 'alpha'
    edge_width_str = 'edge_width'
    face_color_str = 'face_color'
    edge_color_str = 'edge_color'
    alpha_str = 'alpha'
    body_type = 'body'
    min_max_type = 'min_max'
    median_type = 'median'
    part_type_dict = {
        'body': body_type,
        'boxes': body_type,
        'cmaxes': min_max_type,
        'cmins': min_max_type,
        'cbars': min_max_type,
        'whiskers': min_max_type,
        'caps': min_max_type,
        'fliers': min_max_type,
        'medians': median_type,
        'cmedians': median_type,
    }

    # for min_max_props_dict in min_max_props_list:
    #     if edge_color_str in min_max_props_dict:
    #         min_max_props_dict[color_str] = min_max_props_dict[edge_color_str]
    #         del min_max_props_dict[edge_color_str]
    # for median_props_dict in median_props_list:
    #     if edge_color_str in median_props_dict:
    #         median_props_dict[color_str] = median_props_dict[edge_color_str]
    #         del median_props_dict[edge_color_str]

    if figure_type == 'violin':
        parts = ax.violinplot(data_list, positions=positions, widths=widths, showmedians=True, showextrema=True)
        min_max_props_dict = combine_props(min_max_props_list)
        for part_name in ['cmaxes', 'cmins', 'cbars', ]:
            # parts[part_name].set(**min_max_props_list)
            # parts[part_name].set_edgecolor(color_list)
            # parts[part_name].set_linewidth(common_line_width)
            # parts[part_name].set(**min_max_props_dict)
            set_parameter_of_obj(parts[part_name], part_type_dict[part_name], **min_max_props_dict)
        # parts['cmedians'].set(**median_props_list)
        median_props_dict = combine_props(median_props_list)
        # parts['cmedians'].set(**median_props_dict)
        set_parameter_of_obj(parts['cmedians'], median_type, **median_props_dict)
        # for part, median_props in zip(parts['cmedians'], median_props_list):
        #     part.set(**median_props)
        # parts['cmedians'].set_edgecolor(median_color_list)
        # parts['cmedians'].set_linewidth(common_line_width)
        for body_part, body_props in zip(parts['bodies'], body_props_list):
            if edge_color_str in body_props:
                del body_props[edge_color_str]
            # body_part.set(**body_props)
            set_parameter_of_obj(body_part, body_type, **body_props)
        # for pc, color in zip(parts['bodies'], color_list):
        #     pc.set_facecolor(color)
        #     pc.set_alpha(body_alpha)
    elif figure_type == 'box':
        parts = ax.boxplot(
            data_list, positions=positions, patch_artist=True, widths=widths, whis=(0, 100))
        for part_name, part_list in parts.items():
            if part_name == 'medians':
                prop_list = median_props_list
            elif part_name == 'boxes':
                for body_prop_dict, min_max_prop_dict in zip(body_props_list, min_max_props_list):
                    if edge_width_str in min_max_prop_dict and edge_width_str not in body_prop_dict:
                        body_prop_dict[edge_width_str] = min_max_prop_dict[edge_width_str]
                    if edge_color_str in min_max_prop_dict and edge_color_str not in body_prop_dict:
                        body_prop_dict[edge_color_str] = min_max_prop_dict[edge_color_str]
                    if alpha_str in body_prop_dict:
                        alpha_value = body_prop_dict.pop(alpha_str)
                        # del body_prop_dict[alpha_str]
                        face_color_value = body_prop_dict[face_color_str]
                        try:
                            body_prop_dict[face_color_str] = face_color_value.add_transparency(alpha_value)
                        except AttributeError:
                            body_prop_dict[face_color_str] = np.array([*face_color_value, alpha_value])
                prop_list = body_props_list
            elif part_name == 'whiskers' or part_name == 'caps':
                prop_list = (prop for prop in min_max_props_list for _ in (0, 1))
            else:
                prop_list = min_max_props_list
            for part, props in zip(part_list, prop_list):
                # part.set(**props)
                set_parameter_of_obj(part, part_type_dict[part_name], **props)
        # for part_name, part_list in parts.items():
        #     if part_name == 'medians':
        #         current_color_list = median_color_list
        #     else:
        #         current_color_list = color_list
        #     repeat = False
        #     if len(part_list) > len(current_color_list):
        #         repeat = True
        #     for index, part in enumerate(part_list):
        #         if repeat:
        #             current_color = current_color_list[int(index / 2)]
        #         else:
        #             current_color = current_color_list[index]
        #         part.set_color(current_color)
        #         if part_name == 'boxes':
        #             face_color = np.hstack([current_color, body_alpha])
        #             part.set_facecolor(face_color)
    if cutoff is not None:
        # ax.axhline(cutoff, linestyle='--', **cutoff_param_dict)
        if cutoff_param_dict is None:
            cutoff_param_dict = {}
        core_cutoff_plotting(ax, cutoff, **cutoff_param_dict)
    x_axis_position = np.arange(1, len(data_list) + 1)
    if emphasized_flux_list is not None:
        ax.plot(x_axis_position, emphasized_flux_list, 'o', markersize=4)
    if x_ticks is None:
        x_ticks = x_axis_position
    if x_lim is None:
        x_lim = [0.3, len(data_list) + 0.7]
    axis_numeric_setting(
        ax, x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks)


def get_twin_axis_numeric_parameters(target_parameter, assert_func):
    try:
        right_target_parameter = target_parameter[1]
        assert assert_func(right_target_parameter)
    except TypeError or AssertionError:
        target_parameter = target_parameter
        right_target_parameter = None
    else:
        target_parameter = target_parameter[0]
    return target_parameter, right_target_parameter


def bar_plot_warp_func(
        ax, x_loc, data_array, width, face_color, label=None, error_bar_data_vector=None, error_bar_color=None,
        cap_size=None, edge_width=None, z_order=None, alpha=None):
    if error_bar_color is None:
        try:
            error_bar_color = face_color.add_transparency(1)
        except AttributeError:
            error_bar_color = face_color
    error_bar_param_dict = {
        'ecolor': error_bar_color,
        'capsize': cap_size,
        'elinewidth': edge_width,
        'capthick': edge_width,
    }
    try:
        alpha_set = face_color.alpha_set
    except AttributeError:
        alpha_set = False
    if alpha_set:
        alpha = None
    ax.bar(
        x_loc, data_array, width=width, label=label,
        color=face_color, yerr=error_bar_data_vector, error_kw=error_bar_param_dict, zorder=z_order, alpha=alpha)


def core_single_ax_bar_plot(
        ax, array_data_dict, color_dict, error_bar_data_dict, array_len,
        bar_total_width, edge, y_lim=None, y_ticks=None, cmap=None, bar_param_dict=None, error_bar_param_dict=None,
        cutoff=None, cutoff_param_dict=None, twin_x_axis=False, max_bar_num_each_group=None,
        raw_data_scatter_dict=None, raw_data_scatter_param_dict=None):
    def right_y_ticks_verification(_right_y_ticks):
        if isinstance(_right_y_ticks, str) and _right_y_ticks == 'default':
            return True
        elif isinstance(_right_y_ticks[0], (int, float, np.int32, np.float64)):
            return True
        return False

    if max_bar_num_each_group is None:
        max_bar_num_each_group = len(array_data_dict)
    if array_data_dict is None:
        bar_unit_width = bar_total_width
    else:
        bar_unit_width = bar_total_width / max_bar_num_each_group
    x_tick_loc = np.arange(array_len) + 0.5
    x_left_loc = x_tick_loc - bar_total_width / 2
    if bar_param_dict is None:
        bar_param_dict = {}
    # input_edge_width_str = 'edge_width'
    # input_cap_size_str = 'cap_size'
    # default_error_bar_dict = {
    #     input_cap_size_str: 3,
    #     input_edge_width_str: 1.5
    # }
    # if error_bar_param_dict is not None:
    #     default_error_bar_dict.update(error_bar_param_dict)
    if error_bar_param_dict is None:
        error_bar_param_dict = {}
    marker_size_label = 'marker_size'
    marker_size = None
    if raw_data_scatter_param_dict is None:
        raw_data_scatter_param_dict = {}
    else:
        raw_data_scatter_param_dict = dict(raw_data_scatter_param_dict)
        if marker_size_label in raw_data_scatter_param_dict:
            marker_size = raw_data_scatter_param_dict.pop(marker_size_label)
    if array_data_dict is not None:
        for index, (data_label, data_value) in enumerate(array_data_dict.items()):
            loc_index = index
            color_index = index
            if twin_x_axis:
                ax_index, data_array, *loc_index_list = data_value
                if len(loc_index_list) > 0:
                    loc_index = loc_index_list[0]
            else:
                ax_index = None
                if isinstance(data_value, tuple) and len(data_value) == 2:
                    data_array, loc_index = data_value
                else:
                    data_array = data_value
            if data_array is None:
                continue
            assert len(data_array) == array_len
            if data_label in color_dict:
                current_color = color_dict[data_label]
            else:
                current_color = cmap.colors[color_index]
            error_bar_vector = None
            if error_bar_data_dict is not None and data_label in error_bar_data_dict:
                error_bar_vector = error_bar_data_dict[data_label]
            x_loc = x_left_loc + loc_index * bar_unit_width + bar_unit_width / 2
            if twin_x_axis:
                current_ax = ax[ax_index]
            else:
                current_ax = ax
            bar_plot_warp_func(
                current_ax, x_loc, data_array, width=bar_unit_width, face_color=current_color, label=data_label,
                **bar_param_dict)
            if error_bar_vector is not None:
                core_error_bar_plotting(
                    current_ax, x_loc, data_array, error_bar_vector, edge_color=it.repeat(current_color),
                    **error_bar_param_dict)
            if raw_data_scatter_dict is not None and data_label in raw_data_scatter_dict:
                raw_data_matrix = raw_data_scatter_dict[data_label]
                assert raw_data_matrix.shape[1] == array_len
                raw_data_x_matrix = (random_seed.random((raw_data_matrix.shape[0], 1)) - 0.5) * bar_unit_width * 0.9 + x_loc
                core_scatter_plotting(
                    current_ax, raw_data_x_matrix.reshape([-1]), raw_data_matrix.reshape([-1]),
                    marker_size=marker_size, marker_color=np.reshape(current_color, (1, -1)),
                    marker_shape='o', scatter_param_dict=raw_data_scatter_param_dict)
    x_lim = [-edge, array_len + edge]
    if twin_x_axis:
        ax, right_ax = ax
        y_lim, right_y_lim = get_twin_axis_numeric_parameters(y_lim, lambda _right_y_lim: len(_right_y_lim) == 2)
        y_ticks, right_y_ticks = get_twin_axis_numeric_parameters(
            y_ticks, right_y_ticks_verification)
        axis_numeric_setting(right_ax, x_lim=x_lim, x_ticks=x_tick_loc, y_lim=right_y_lim, y_ticks=right_y_ticks)
    axis_numeric_setting(ax, x_lim=x_lim, x_ticks=x_tick_loc, y_lim=y_lim, y_ticks=y_ticks)
    if cutoff is not None:
        if cutoff_param_dict is None:
            cutoff_param_dict = {}
        try:
            for cutoff_value in cutoff:
                core_cutoff_plotting(ax, cutoff_value, **cutoff_param_dict)
        except TypeError:
            core_cutoff_plotting(ax, cutoff, **cutoff_param_dict)


def core_line_plotting(
        ax, x_value_array, y_value_array, edge_color=None, edge_width=None, edge_style=None,
        x_lim=None, x_ticks=None, y_lim=None, y_ticks=None, label=None, z_order=None, **kwargs):
    if edge_style is not None:
        edge_style = str(edge_style)
    ax.plot(
        x_value_array, y_value_array, color=edge_color, linewidth=edge_width, linestyle=edge_style, label=label,
        zorder=z_order)
    axis_numeric_setting(ax, x_lim=x_lim, x_ticks=x_ticks, y_lim=y_lim, y_ticks=y_ticks)


def core_error_bar_plotting(
        ax, x_value_array, y_value_array, y_error_bar_array, x_error_bar_array=None,
        edge_color=None, edge_width=None, cap_size=None, label=None, z_order=None, data_location_cap=False, **kwargs):
    """
    If data_point_cap is True,  No data point. Cannot be used solely.
    """

    total_error_bar_num = len(x_value_array)
    if x_error_bar_array is None:
        x_error_bar_array = it.repeat(None)
    if edge_color is None:
        edge_color = it.repeat(None)
    if edge_width is None:
        edge_width = 1.5
    if cap_size is None:
        cap_size = 3
    # for error_bar_index in range(total_error_bar_num):
    for x_value, y_value, y_error_bar, x_error_bar, error_bar_color in zip(
            x_value_array, y_value_array, y_error_bar_array, x_error_bar_array, edge_color):
        # x_value = x_value_array[error_bar_index]
        # y_value = y_value_array[error_bar_index]
        # y_error_bar = y_error_bar_array[error_bar_index]
        # if x_error_bar_array is not None:
        #     x_error_bar = x_error_bar_array[error_bar_index]
        # else:
        #     x_error_bar = None
        # error_bar_color = edge_color[error_bar_index]
        ax.errorbar(
            x_value, y_value, yerr=y_error_bar, xerr=x_error_bar, fmt='none', ecolor=error_bar_color,
            elinewidth=edge_width, capsize=cap_size, capthick=edge_width, label=label, zorder=z_order)
        if data_location_cap:
            ax.errorbar(
                x_value, y_value, yerr=0, fmt='none', ecolor=error_bar_color,
                elinewidth=edge_width, capsize=cap_size, capthick=edge_width, label=label, zorder=z_order)


def core_histogram_plotting(
        ax, x_array=None, bins=None, hist_type=None, density=True,
        x_lim=None, x_ticks=None, y_lim=None, y_ticks=None, label=None,
        alpha=0.3, face_color=None, cutoff=None, cutoff_param_dict=None, **kwargs):
    if x_array is not None:
        n, bins, patches = ax.hist(
            x_array, bins, histtype=hist_type, density=density, facecolor=face_color, alpha=alpha, label=label)
    if cutoff is not None:
        if cutoff_param_dict is None:
            cutoff_param_dict = {}
        # ax.axvline(cutoff, **cutoff_param_dict)
        core_cutoff_plotting(ax, cutoff, axis='x', **cutoff_param_dict)
    axis_numeric_setting(ax, x_lim=x_lim, x_ticks=x_ticks, y_ticks=y_ticks, y_lim=y_lim)


def core_cutoff_plotting(
        ax, value, axis='y', edge_color='orange', edge_style=':', edge_width=1, z_order=None, **kwargs):
    effective_cutoff_param_dict = {
        'color': edge_color,
        'linestyle': str(edge_style),
        'linewidth': edge_width,
        'zorder': z_order,
    }
    if axis == 'x':
        ax.axvline(value, **effective_cutoff_param_dict)
    elif axis == 'y':
        ax.axhline(value, **effective_cutoff_param_dict)
    else:
        raise ValueError()
