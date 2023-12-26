from ...common.config import ParameterName as GeneralParameterName, Keywords, DataName
from ...common.classes import Vector, HorizontalAlignment, VerticalAlignment, FontWeight, \
    TransformDict, LineStyle
from ...common.color import TextConfig, ColorConfig, ZOrderConfig
from ...common.common_figure_materials import CommonFigureMaterials, CommonFigureString, ProtocolSearchingMaterials, \
    CommonElementConfig, ModelDataSensitivityDataFigureConfig, calculate_center_bottom_offset
from ...common.third_party_packages import np, transforms
from ...common.built_in_packages import it, List
from ..basic_shape_elements.elements import CompositeFigure, move_and_scale_for_dict, \
    Rectangle, CompositeFigure, TextBox, Region, DataFigureAxes, Line, Ellipse, common_legend_generator
from ..basic_shape_elements.modified_text import ax_text, draw_text
from ..common_functions import initialize_vector_input, default_parameter_extract, clip_angle_to_normal_range, \
    t_test_of_two_groups


class ParameterName(GeneralParameterName):
    basic_number_format_str = 'basic_number_format'

    mean_or_std = 'mean_or_std'

    # Scatter plot
    edge = 'edge'
    x_value_array = 'x_value_array'
    y_value_array = 'y_value_array'
    y_value_data_dict = 'y_value_data_dict'
    data_label = 'data_label'
    marker_color = 'marker_color'

    cutoff_value_color = 'cutoff_value_color'
    cutoff_dash_width = 'cutoff_dash_width'
    scatter_param_dict = 'scatter_param_dict'
    bar_param_dict = 'bar_param_dict'
    line_param_dict = 'line_param_dict'
    im_param_dict = 'im_param_dict'

    violin = 'violin'
    box = 'box'
    scatter = 'scatter'

    cutoff = 'cutoff'
    cutoff_param_dict = 'cutoff_param_dict'
    box_violin_config_dict = 'box_violin_config_dict'

    data_nested_list = 'data_nested_list'
    positions_list = 'positions_list'
    median_color_dict = 'median_color_dict'
    emphasized_flux_list = 'emphasized_flux_list'
    ax_bottom_left_list = 'ax_bottom_left_list'
    ax_size_list = 'ax_size_list'
    array_len_list = 'array_len_list'
    max_bar_num_each_group = 'max_bar_num_each_group'
    data_figure_text_list = 'data_figure_text_list'

    normal_scatter_figure = 'normal'
    scatter_line_figure = 'scatter_line'
    colon_cancer_scatter_line_figure = 'colon_scatter_line'

    histogram_param_dict = 'histogram_data_figure'
    bins = 'bins'
    hist_type = 'hist_type'
    hist_type_bar = 'bar'
    hist_type_step = 'step'
    hist_type_step_filled = 'stepfilled'
    density = 'density'

    data_value_text_format_dict = 'data_value_text_format_dict'
    heatmap_size = 'heatmap_size'
    heatmap_cmap = 'heatmap_cmap'
    data_lim_pair = 'data_lim_pair'
    highlight = 'highlight'
    highlight_config = 'highlight_config'

    cbar_orientation = 'cbar_orientation'
    cbar_location = 'cbar_location'
    cbar_ax = 'cbar_ax'
    cbar_class = 'cbar_class'
    cbar_figure_data_parameter_dict = 'cbar_figure_data_parameter_dict'
    cbar_bottom_left = 'cbar_bottom_left'
    cbar_size = 'cbar_size'
    cbar_scale = 'cbar_scale'

    net_optimized_diff_vector_list = 'net_optimized_diff_vector_list'


class DataFigureConfig(object):
    legend_z_order = ZOrderConfig.default_legend_z_order
    axis_z_order = ZOrderConfig.default_axis_z_order
    figure_text_z_order = ZOrderConfig.default_text_z_order
    axis_label_z_order = ZOrderConfig.default_axis_z_order

    normal_figure_element_z_order = ZOrderConfig.default_patch_z_order
    cutoff_value_z_order = normal_figure_element_z_order - ZOrderConfig.z_order_increment
    error_bar_behind_z_order = normal_figure_element_z_order - 2 * ZOrderConfig.z_order_increment
    line_z_order = normal_figure_element_z_order - 3 * ZOrderConfig.z_order_increment

    main_text_font = TextConfig.main_text_font
    alpha_for_bar_plot = ColorConfig.alpha_for_bar_plot

    common_text_config = CommonElementConfig.common_text_config

    # common_ax_total_bottom_left = Vector(0.08, 0.11)
    common_ax_total_bottom_left = Vector(0.11, 0.19)
    common_ax_total_size = Vector(1, 1) - common_ax_total_bottom_left

    class GroupDataFigure(object):
        axis_line_width_ratio = 0.5
        # axis_line_width_ratio = 0.8
        axis_tick_len = 2.5
        # axis_tick_len = 3
        x_y_axis_smaller_label_font_size = 7
        x_y_axis_tick_label_font_size = 8
        x_y_axis_label_font_size = 10
        inner_text_font_size = 10
        adjacent_x_label_distance = 0.008
        adjacent_x_tick_label_distance = 0.008
        adjacent_y_label_distance = 0.012
        adjacent_y_tick_label_distance = 0.006
        label_width = 0.1
        label_height = 0.02
        tick_label_width = 0.05
        tick_label_height = 0.01
        p_value_cap_width_ratio = 0.05

    # This labeling parameters are directly fed to .draw function. Therefore, they should be scaled first to
    # obtain correct location in final data figures.
    @staticmethod
    def x_label_format_dict_generator(scale=1):
        return {
            ParameterName.axis_label_distance: 0.005 * scale,
            ParameterName.width: 0.05 * scale,
            ParameterName.height: 0.01 * scale,
        }

    @staticmethod
    def x_tick_label_format_dict_generator(scale=1):
        return {
            ParameterName.axis_tick_label_distance: 0.01 * scale,
            ParameterName.width: 0.05 * scale,
            ParameterName.height: 0.01 * scale,
        }

    @staticmethod
    def y_label_format_dict_generator(scale=1):
        return {
            ParameterName.axis_label_distance: 0.025 * scale,
            ParameterName.width: 0.05 * scale,
            ParameterName.height: 0.01 * scale,
        }

    @staticmethod
    def y_tick_label_format_dict_generator(scale=1):
        return {
            ParameterName.axis_tick_label_distance: 0.006 * scale,
            ParameterName.width: 0.04 * scale,
            ParameterName.height: 0.01 * scale,
        }

    @staticmethod
    def common_axis_param_dict_generator(scale=1):
        axis_format_dict = {
            ParameterName.edge_width: DataFigureConfig.GroupDataFigure.axis_line_width_ratio * scale
        }
        axis_tick_format_dict = {
            **axis_format_dict,
            ParameterName.axis_tick_length: DataFigureConfig.GroupDataFigure.axis_tick_len * scale
        }
        axis_label_format_dict = {
            **DataFigureConfig.common_text_config,
            # ParameterName.font: DataFigureConfig.main_text_font,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.x_y_axis_tick_label_font_size * scale,
            ParameterName.z_order: DataFigureConfig.axis_label_z_order,
        }
        return axis_format_dict, axis_tick_format_dict, axis_label_format_dict

    @staticmethod
    def common_subplot_text_format_dict_generator(scale=1):
        return {
            **DataFigureConfig.common_text_config,
            # ParameterName.font: DataFigureConfig.main_text_font,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.font_size: DataFigureConfig.GroupDataFigure.inner_text_font_size * scale,
            ParameterName.width: 0.05 * scale,
            ParameterName.height: 0.01 * scale,
            # ParameterName.horizontal_alignment: HorizontalAlignment.center,
            # ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        }

    @staticmethod
    def common_error_bar_param_dict_generator(scale=1):
        return {
            ParameterName.cap_size: 1.7 * scale,
            ParameterName.edge_width: 0.5 * scale,
        }

    @staticmethod
    def common_line_param_dict_generator(scale=1):
        return {
            ParameterName.edge_width: 0.15 * scale,
            ParameterName.edge_color: ColorConfig.black_color,
            ParameterName.z_order: DataFigureConfig.line_z_order
        }

    @staticmethod
    def common_axis_line_param_dict_generator(scale=1):
        return {
            ParameterName.edge_width: 0.7 * scale,
            ParameterName.edge_color: ColorConfig.black_color,
            ParameterName.z_order: DataFigureConfig.axis_label_z_order
        }

    common_text_box_config_dict = {
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }

    common_title_config_dict = {
        **common_text_config,
        # ParameterName.font: TextConfig.main_text_font,
        # ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        # ParameterName.horizontal_alignment: HorizontalAlignment.center,
        # ParameterName.z_order: ZOrderConfig.default_text_z_order,
        ParameterName.font_weight: FontWeight.bold,
        # ParameterName.text_box: True,
    }

    common_supplementary_text_config_dict = {
        **common_text_config,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: figure_text_z_order,
    }

    # For flux tick labels
    flux_x_tick_separator_format_dict = {
        ParameterName.edge_width: GroupDataFigure.axis_line_width_ratio,
        ParameterName.axis_line_start_distance: 0,
        # ParameterName.axis_line_end_distance: 0.055,
        ParameterName.axis_line_end_distance: 0.115,
    }
    flux_x_tick_separator_label_format_dict = {
        # ParameterName.font: main_text_font,
        **common_text_config,
        ParameterName.z_order: figure_text_z_order,
        ParameterName.width: 0.1,
        ParameterName.height: 0.02,
        # ParameterName.horizontal_alignment: HorizontalAlignment.center,
        # ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.axis_label_distance: 0.12,
    }
    flux_x_tick_format_dict = {
        **common_text_config,
        ParameterName.axis_tick_label_distance: 0.039,
        ParameterName.width: 0.08,
        ParameterName.height: 0.015,
        ParameterName.angle: -90,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.vertical_alignment: HorizontalAlignment.center,
        ParameterName.text_box: False,
    }
    common_p_value_cap_parameter_dict = {
        ParameterName.edge_width: GroupDataFigure.p_value_cap_width_ratio,
        ParameterName.height: 0.03,
        ParameterName.width: 0.1,
        ParameterName.text_y_offset: 0.03,
        ParameterName.cap_y_offset: 0.02,
    }


mid_carbon_num_dict = {
    'GLC_c': 6,
    'FRU6P_c+GLC6P_c': 6,
    'E4P_c': 4,
    '2PG_c+3PG_c': 3,
    'PEP_c': 3,
    'GLN_c+GLN_m': 5,
    'ASP_c+ASP_m': 4,
    'RIB5P_c': 5,
    'PYR_c+PYR_m': 3,
    'LAC_c': 3,
    '3PG_c': 3,
    'FUM_m': 4,
    'CIT_c+CIT_m+ICIT_m': 4,
    'AKG_c+AKG_m': 5,
    'FRU16BP_c': 6,
    'GLU_c': 5,
    'SUC_m': 4,
}

multiplied_parameter_set = {
    ParameterName.axis_label_distance,
    ParameterName.axis_tick_label_distance,
    ParameterName.cap_size,
    ParameterName.edge_width,
    ParameterName.axis_tick_length,
    # ParameterName.font_weight,
    ParameterName.font_size,
    ParameterName.width,
    ParameterName.height,
    ParameterName.axis_line_start_distance,
    ParameterName.axis_line_end_distance,
}


def merge_axis_format_dict(
        axis_label_format_dict, preset_default_format_dict, new_figure_config_dict, dict_label):
    default_format_dict = {
        **axis_label_format_dict,
        **preset_default_format_dict
    }
    if dict_label in new_figure_config_dict:
        new_format_dict = new_figure_config_dict[dict_label]
        if isinstance(new_format_dict, (tuple, list)):
            result_format_dict = [{
                **default_format_dict,
                **each_new_format_dict
            } for each_new_format_dict in new_format_dict]
        else:
            result_format_dict = {
                **default_format_dict,
                **new_format_dict
            }
    else:
        result_format_dict = default_format_dict
    return result_format_dict


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


def sensitivity_heatmap_cbar_axis_label_dict(data_name, **kwargs):
    if data_name in {DataName.data_sensitivity, DataName.data_sensitivity_with_noise}:
        # return (-1, 1), [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1]
        data_lim = [-1, 1]
        data_tick_interval = 0.2
    else:
        # return (-0.5, 0.5), [-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
        data_lim = [-0.5, 0.5]
        data_tick_interval = 0.1
    data_tick = np.arange(data_lim[0], data_lim[1] + 1e-5, data_tick_interval)
    return data_lim, data_tick


def heatmap_highlight_ellipse_parameter(data_name, **kwargs):
    common_ellipse_config = {
        ParameterName.edge_width: 0.5,
        ParameterName.edge_color: ColorConfig.orange,
        ParameterName.face_color: None,
        ParameterName.z_order: ZOrderConfig.default_legend_z_order,
    }
    config_dict = {
        DataName.raw_model_all_data: {
            ParameterName.center: Vector(6.4, 5.4),
            ParameterName.width: 2,
            ParameterName.height: 5.5,
            ParameterName.angle: -45,
        },
        DataName.raw_model_raw_data: {
            ParameterName.center: Vector(6.5, 3.7),
            ParameterName.width: 3.8,
            ParameterName.height: 3,
            ParameterName.angle: 0,
        }
    }
    target_config_dict = config_dict[data_name]
    target_config_dict.update(common_ellipse_config)
    return target_config_dict


def sensitivity_heatmap_y_axis_labels_generator(data_name, result_label_list, **kwargs):
    def analyze_one_list(_data_name, _current_label_dict, _result_label_list):
        if _data_name in _current_label_dict:
            replace = False
            label_dict_for_current_data = _current_label_dict[_data_name]
        elif _data_name in data_name_replace_dict:
            replace = True
            original_data_name = data_name_replace_dict[_data_name]
            label_dict_for_current_data = _current_label_dict[original_data_name]
        else:
            raise ValueError()

        last_separator_location = 0
        group_id_list = list(label_dict_for_current_data.keys())
        _final_tick_label_list = []
        _group_separator_list = [last_separator_location]
        _group_name_location_list = []
        _group_name_list = []
        current_group_index = 0
        current_group_id = group_id_list[current_group_index]
        current_group_label_dict = label_dict_for_current_data[current_group_id]
        for result_label_index, result_label in enumerate(_result_label_list + [None]):
            next_group = False
            # if result_label in raw_model_data_label_dict:
            #     # if _data_name in data_sensitivity_dict:
            #     #     if result_label == raw_data_label or result_label == raw_data_noise_label:
            #     #         # current_tick_label = 'Experimental data'
            #     #         current_tick_label = CommonFigureString.experimental_data
            #     #     else:
            #     #         # current_tick_label = 'All data'
            #     #         current_tick_label = CommonFigureString.all_data
            #     # else:
            #     #     if _data_name in model_sensitivity_dict or _data_name in model_sensitivity_all_data_dict:
            #     #         # current_tick_label = 'Raw model'
            #     #         current_tick_label = CommonFigureString.raw_model
            #     #     elif _data_name in {DataName.different_flux_range, DataName.different_flux_range_all_data}:
            #     #         # current_tick_label = 'Raw config (Low LB + Medium UB)'
            #     #         current_tick_label = CommonFigureString.raw_config_bound
            #     #     else:
            #     #         # current_tick_label = 'Raw config (GLC only)'
            #     #         current_tick_label = CommonFigureString.raw_config_input_flux
            #     #     new_separator_location = result_label_index + 1
            #     #     _group_separator_list.append(new_separator_location)
            #     #     last_separator_location = new_separator_location
            #     current_tick_label = group_id_name_dict[_data_name][result_label]
            #     _final_tick_label_list.append(current_tick_label)
            #     new_separator_location = result_label_index + 1
            #     _group_separator_list.append(new_separator_location)
            #     last_separator_location = new_separator_location
            # else:
            if result_label is None:
                next_group = True
                current_tick_label = None
            else:
                if replace:
                    result_label = ModelDataSensitivityDataFigureConfig.modify_all_data_to_raw_data(
                        ModelDataSensitivityDataFigureConfig.modify_noise_data_to_raw_data(result_label))
                if result_label not in current_group_label_dict:
                    next_group = True
                    current_tick_label = None
                else:
                    current_tick_label = current_group_label_dict[result_label]
            if next_group:
                new_separator_location = result_label_index
                _group_separator_list.append(new_separator_location)
                if isinstance(current_group_id, str):
                    _group_name_list.append(group_id_name_dict[current_group_id])
                    _group_name_location_list.append((last_separator_location + new_separator_location) / 2)
                last_separator_location = new_separator_location
                if result_label is not None:
                    current_group_index += 1
                    new_group_id = group_id_list[current_group_index]
                    new_group_label_dict = label_dict_for_current_data[new_group_id]
                    if current_tick_label is None:
                        current_tick_label = new_group_label_dict[result_label]
                    _final_tick_label_list.append(current_tick_label)
                    current_group_id = new_group_id
                    current_group_label_dict = new_group_label_dict
            else:
                _final_tick_label_list.append(current_tick_label)
        return _final_tick_label_list, _group_separator_list, _group_name_location_list, _group_name_list

    def multiple_list_raw_model_label_transform(_data_name):
        if _data_name == DataName.model_sensitivity or _data_name == DataName.model_sensitivity_all_data:
            current_tick_label = CommonFigureString.raw_model
        elif _data_name == DataName.config_sensitivity or _data_name == DataName.config_sensitivity_all_data:
            current_tick_label = CommonFigureString.raw_config_bound
        else:
            raise ValueError()
        return current_tick_label

    def analyze_model_sensitivity_multiple_list(_data_name, _current_label_dict, _result_label_list):
        _final_tick_label_list = []
        _minor_group_separator_list = []
        _major_group_separator_list = []
        _minor_group_name_location_list = []
        _minor_group_name_list = []
        _major_group_name_location_list = []
        _major_group_name_list = []
        model_sensitivity_label_dict = _current_label_dict[_data_name]
        previous_total_tick_num = 0
        for current_model_sensitivity_data_label, current_result_label_list in _result_label_list.items():
            if current_model_sensitivity_data_label in raw_model_data_label_dict:
                if len(_major_group_separator_list) == 0:
                    _major_group_separator_list.append(previous_total_tick_num)
                _major_group_separator_list.append(previous_total_tick_num + 1)
                # current_tick_label = multiple_list_raw_model_label_transform(_data_name)
                current_tick_label = group_id_name_dict[current_model_sensitivity_data_label][_data_name]
                _final_tick_label_list.append(current_tick_label)
                current_total_tick_num = 1
            else:
                (
                    current_tick_label_list, current_group_separator_list, current_group_name_location_list,
                    current_group_name_list) = analyze_one_list(
                    current_model_sensitivity_data_label, model_sensitivity_label_dict, current_result_label_list)
                current_total_tick_num = len(current_tick_label_list)
                current_group_separator_list = [
                    current_group_separator + previous_total_tick_num
                    for current_group_separator in current_group_separator_list
                ]
                current_group_name_location_list = [
                    current_group_name_location + previous_total_tick_num
                    for current_group_name_location in current_group_name_location_list
                ]
                _final_tick_label_list.extend(current_tick_label_list)
                _minor_group_separator_list.extend(current_group_separator_list[1:-1])
                if len(_major_group_separator_list) == 0:
                    _major_group_separator_list.append(current_group_separator_list[0])
                _major_group_separator_list.append(current_group_separator_list[-1])
                _minor_group_name_list.extend(current_group_name_list)
                _minor_group_name_location_list.extend(current_group_name_location_list)
                _major_group_name_list.append(group_id_name_dict[current_model_sensitivity_data_label])
                _major_group_name_location_list.append((current_total_tick_num + 2 * previous_total_tick_num) / 2)
            previous_total_tick_num += current_total_tick_num
        return _final_tick_label_list, _minor_group_separator_list, _minor_group_name_location_list, \
            _minor_group_name_list, _major_group_separator_list, _major_group_name_location_list, \
            _major_group_name_list

    def analyze_data_sensitivity_multiple_list(_data_name, _current_label_dict, _result_label_list):
        _final_tick_label_list = []
        _major_group_separator_list = []
        _major_group_name_location_list = []
        _major_group_name_list = []
        data_sensitivity_label_dict = _current_label_dict[data_name]
        previous_total_tick_num = 0
        for current_data_sensitivity_data_label, current_result_label_list in _result_label_list.items():
            (
                current_tick_label_list, *_) = analyze_one_list(
                current_data_sensitivity_data_label, data_sensitivity_label_dict, current_result_label_list)

        _minor_group_separator_list = None
        _minor_group_name_location_list = None
        _minor_group_name_list = None
        return _final_tick_label_list, _minor_group_separator_list, _minor_group_name_location_list, \
            _minor_group_name_list, _major_group_separator_list, _major_group_name_location_list, \
            _major_group_name_list

    data_name_replace_dict = {
        DataName.merge_reversible_reaction_all_data: DataName.merge_reversible_reaction,
        DataName.combine_consecutive_reactions_all_data: DataName.combine_consecutive_reactions,
        DataName.prune_branches_all_data: DataName.prune_branches,
        DataName.data_sensitivity_with_noise: DataName.data_sensitivity,
        DataName.different_constant_flux_all_data: DataName.different_constant_flux,
        DataName.different_constant_flux_with_noise: DataName.different_constant_flux,
        DataName.different_constant_flux_with_noise_all_data: DataName.different_constant_flux,
        DataName.different_flux_range_all_data: DataName.different_flux_range,
    }
    current_label_dict = ModelDataSensitivityDataFigureConfig.label_dict
    raw_model_data_label_dict = ModelDataSensitivityDataFigureConfig.raw_model_data_label_dict
    raw_data_label = ModelDataSensitivityDataFigureConfig.raw_data_result_label
    raw_data_noise_label = ModelDataSensitivityDataFigureConfig.raw_data_noise_result_label
    model_sensitivity_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
    model_sensitivity_all_data_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_all_data_dict
    data_sensitivity_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_label_dict
    group_id_name_dict = ModelDataSensitivityDataFigureConfig.group_id_name_dict

    if data_name == DataName.different_constant_flux_with_noise:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_model_sensitivity_multiple_list(
            DataName.config_sensitivity, current_label_dict, result_label_list)
    elif data_name in {
            DataName.model_sensitivity, DataName.model_sensitivity_all_data,
            DataName.config_sensitivity, DataName.config_sensitivity_all_data}:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_model_sensitivity_multiple_list(
            data_name, current_label_dict, result_label_list)
    elif data_name in {DataName.data_sensitivity, DataName.data_sensitivity_with_noise}:
        # (
        #     final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
        #     minor_group_name_list, major_group_separator_list, major_group_name_location_list,
        #     major_group_name_list) = analyze_data_sensitivity_multiple_list(
        #     data_name, current_label_dict, result_label_list)

        (
            final_tick_label_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_one_list(data_name, current_label_dict, result_label_list)
        minor_group_separator_list = None
        minor_group_name_location_list = None
        minor_group_name_list = None
    else:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list) = analyze_one_list(data_name, current_label_dict, result_label_list)
        major_group_separator_list = None
        major_group_name_location_list = None
        major_group_name_list = None

    total_item_num = len(final_tick_label_list)
    if minor_group_name_list is not None:
        minor_group_separator_array = (total_item_num - np.array(minor_group_separator_list)) / total_item_num
        minor_group_name_location_array = (total_item_num - np.array(minor_group_name_location_list)) / total_item_num
    else:
        minor_group_separator_array = None
        minor_group_name_location_array = None
    if major_group_separator_list is not None:
        major_group_separator_location_array = (total_item_num - np.array(major_group_separator_list)) / total_item_num
        major_group_name_location_array = (total_item_num - np.array(major_group_name_location_list)) / total_item_num
    else:
        major_group_separator_location_array = None
        major_group_name_location_array = None
    return final_tick_label_list, minor_group_separator_array, minor_group_name_location_array, minor_group_name_list, \
        major_group_separator_location_array, major_group_name_location_array, major_group_name_list


def sensitivity_heatmap_x_axis_labels_generator(flux_id_list):
    # group_id_name_dict = {
    #     'glycolysis': 'Glycolysis',
    #     'ser_gly': 'Ser-Gly',
    #     'tca': 'TCA cycle',
    #     'aa': 'AA',
    #     'ppp': 'PPP',
    #     'exchange': 'Transfer and\nexchange fluxes',
    # }
    x_tick_label_dict = ModelDataSensitivityDataFigureConfig.x_tick_label_dict
    group_id_name_dict = ModelDataSensitivityDataFigureConfig.group_id_name_dict

    group_id_list = list(x_tick_label_dict.keys())
    x_tick_label_list = []
    current_group_index = 0
    last_separator_location = 0
    group_separator_list = [last_separator_location]
    group_name_location_list = []
    group_name_list = []
    current_group_id = group_id_list[current_group_index]
    current_group_label_dict = x_tick_label_dict[current_group_id]
    for flux_index, flux_id in enumerate(flux_id_list + [None]):
        if flux_id is None or flux_id not in current_group_label_dict:
            new_separator_location = flux_index
            group_separator_list.append(new_separator_location)
            group_name_location_list.append((last_separator_location + new_separator_location) / 2)
            group_name_list.append(group_id_name_dict[current_group_id])
            last_separator_location = new_separator_location
            if flux_id is not None:
                current_group_index += 1
                new_group_id = group_id_list[current_group_index]
                new_group_label_dict = x_tick_label_dict[new_group_id]
                x_tick_label_list.append(new_group_label_dict[flux_id])
                current_group_id = new_group_id
                current_group_label_dict = new_group_label_dict
        else:
            x_tick_label_list.append(current_group_label_dict[flux_id])
    total_item_num = len(x_tick_label_list)
    group_separator_array = np.array(group_separator_list) / total_item_num
    group_name_location_array = np.array(group_name_location_list) / total_item_num
    return x_tick_label_list, group_separator_array, group_name_location_array, group_name_list
