from ..common.config import ParameterName as GeneralParameterName
from ..common.classes import Vector, HorizontalAlignment, VerticalAlignment, FontWeight, \
    LineStyle
from ..common.color import TextConfig, ColorConfig, ZOrderConfig
from ..common.common_figure_materials import CommonElementConfig
from ..common.built_in_packages import it, List
from ..common.third_party_packages import np
from ..common.common_functions import clip_angle_to_normal_range, initialize_vector_input, default_parameter_extract

from ..basic_shape_elements import CompositeFigure, DataFigureAxes, Ellipse, move_and_scale_for_dict, \
    common_legend_generator, Rectangle, Line, transforms, draw_text


class Keywords(object):
    default = 'default'


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
    each_correlation = 'correlation'
    complete_correlation = 'complete_correlation'

    cmap_mapper = 'cmap_mapper'
    cmap_name = 'cmap_name'
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
        p_value_cap_width_ratio = 0.45

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

x_tick_label_dict = {
    'glycolysis': {
        'HEX_c': 'HEX_c',
        'PGI_c__R_PGI_c': 'PGI_c Rnet',
        'PFK_c': 'PFK_c',
        'FBA_c_FBA_c__R': 'FBA_c net',
        'TPI_c_TPI_c__R': 'TPI_c net',
        'GAPD_c_GAPD_c__R': 'GAPD_c net',
        'PGK_c_PGK_c__R': 'PGK_c net',
        'PGM_c_PGM_c__R': 'PGM_c net',
        'ENO_c_ENO_c__R': 'ENO_c net',
        'PYK_c': 'PYK_c',
        'LDH_c_LDH_c__R': 'LDH_c net',
        'PEPCK_c': 'PEPCK_c',
        'ACITL_c': 'ACITL_c',
        'MDH_c__R_MDH_c': 'MDH_c Rnet',
        'ME2_c': 'ME2_c',
        'LIPID_c': 'LIPID_c',
    },
    'ser_gly': {
        'PHGDH_PSAT_PSP_c': 'PHGDH_c',
        'SHMT_c_SHMT_c__R': 'SHMT_c net',
        'SER_input': 'SER_input',
        'GLY_input': 'GLY_input',
    },
    'tca': {
        'PDH_m': 'PDH_m',
        'CS_m': 'CS_m',
        'ACONT_m_ACONT_m__R': 'ACONT_m net',
        'ICDH_m': 'ICDH_m',
        'AKGD_m': 'AKGD_m',
        'SUCOAS_m': 'SUCOAS_m',
        'SUCD_m_SUCD_m__R': 'SUCD_m net',
        'FUMH_m_FUMH_m__R': 'FUMH_m net',
        'MDH_m_MDH_m__R': 'MDH_m net',
        'PC_m': 'PC_m',
    },
    'aa': {
        'GLUD_m_GLUD_m__R': 'GLUD_m net',
        'GLND_m': 'GLND_m',
        'GLNS_c': 'GLNS_c',
        'ASPTA_m_ASPTA_m__R': 'ASPTA_m net',
        'AS_c': 'AS_c',
        'ASPTA_c_ASPTA_c__R': 'ASPTA_c net',
    },
    'ppp': {
        'G6PDH2R_PGL_GND_c': 'G6PDH2R_c',
        'RPI_c_RPI_c__R': 'RPI_c net',
        'RPE_c_RPE_c__R': 'RPE_c net',
        'TKT1_c_TKT1_c__R': 'TKT1_c net',
        'TKT2_c_TKT2_c__R': 'TKT2_c net',
        'TALA_c_TALA_c__R': 'TALA_c net',
        'Salvage_c': 'Salvage',
    },
    'exchange': {
        'PYR_trans_PYR_trans__R': 'PYR_trans net',
        'ASPGLU_m__R_ASPGLU_m': 'ASPGLU_m Rnet',
        'AKGMAL_m__R_AKGMAL_m': 'AKGMAL_m Rnet',
        'CIT_trans__R_CIT_trans': 'CIT_trans Rnet',
        'GLN_trans_GLN_trans__R': 'GLN_trans net',
        'GLU_trans__R_GLU_trans': 'GLU_trans Rnet',
        'GLC_input': 'GLC_input',
        'GLN_input': 'GLN_input',
        'ASP_input': 'ASP_input',
        'LAC_output': 'LAC_output',
        'ALA_input': 'ALA_input',
        'GPT_c_GPT_c__R': 'GPT_c net',
        'BIOMASS_REACTION': 'Biomass',
    },
}

new_x_tick_label_dict = {
    'glycolysis': {
        'HEX_c': 'HEX_c',
        'PGI_c__R_PGI_c': 'PGI_c Rnet',
        'PFK_c': 'PFK_c',
        'FBA_c_FBA_c__R': 'FBA_c net',
        'TPI_c_TPI_c__R': 'TPI_c net',
        'GAPD_c_GAPD_c__R': 'GAPD_c net',
        'PGK_c_PGK_c__R': 'PGK_c net',
        'PGM_c_PGM_c__R': 'PGM_c net',
        'ENO_c_ENO_c__R': 'ENO_c net',
        'PYK_c': 'PYK_c',
        'LDH_c_LDH_c__R': 'LDH_c net',
        'PEPCK_c': 'PEPCK_c',
        'ACITL_c': 'ACITL_c',
        'MDH_c__R_MDH_c': 'MDH_c Rnet',
        'ME2_c': 'ME2_c',
        'LIPID_c': 'LIPID_c',
    },
    'ser_gly': {
        'PHGDH_PSAT_PSP_c': 'PHGDH_c',
        'SHMT_c_SHMT_c__R': 'SHMT_c net',
        'SER_input': 'SER_input',
        'GLY_input': 'GLY_input',
    },
    'tca': {
        'PDH_m': 'PDH_m',
        'CS_m': 'CS_m',
        'ACONT_m_ACONT_m__R': 'ACONT_m net',
        'ICDH_m': 'ICDH_m',
        'AKGD_m': 'AKGD_m',
        'SUCOAS_m': 'SUCOAS_m',
        'SUCD_m_SUCD_m__R': 'SUCD_m net',
        'FUMH_m_FUMH_m__R': 'FUMH_m net',
        'MDH_m_MDH_m__R': 'MDH_m net',
        'PC_m': 'PC_m',
    },
    'aa': {
        'GLUD_m_GLUD_m__R': 'GLUD_m net',
        'GLND_m': 'GLND_m',
        'GLNS_c': 'GLNS_c',
        'GLNS_m': 'GLNS_m',
        'ASPTA_m_ASPTA_m__R': 'ASPTA_m net',
        'AS_c': 'AS_c',
        'ASPTA_c_ASPTA_c__R': 'ASPTA_c net',
    },
    'ppp': {
        'G6PDH2R_PGL_GND_c': 'G6PDH2R_c',
        'RPI_c_RPI_c__R': 'RPI_c net',
        'RPE_c_RPE_c__R': 'RPE_c net',
        'TKT1_c_TKT1_c__R': 'TKT1_c net',
        'TKT2_c_TKT2_c__R': 'TKT2_c net',
        'TALA_c_TALA_c__R': 'TALA_c net',
        'Salvage_c': 'Salvage',
    },
    'exchange': {
        'PYR_trans_PYR_trans__R': 'PYR_trans net',
        'ASPGLU_m__R_ASPGLU_m': 'ASPGLU_m Rnet',
        'AKGMAL_m__R_AKGMAL_m': 'AKGMAL_m Rnet',
        'CIT_trans__R_CIT_trans': 'CIT_trans Rnet',
        'GLN_trans_GLN_trans__R': 'GLN_trans net',
        'GLU_trans__R_GLU_trans': 'GLU_trans Rnet',
        'GLC_input': 'GLC_input',
        'GLN_input': 'GLN_input',
        'ASP_input': 'ASP_input',
        'LAC_output': 'LAC_output',
        'ALA_input': 'ALA_input',
        'GPT_c_GPT_c__R': 'GPT_c net',
        'BIOMASS_REACTION': 'Biomass',
    },
}


# 'PGI_c__R_PGI_c': 'PGI_c Rnet',

group_id_name_dict = {
    'glycolysis': 'Glycolysis',
    'ser_gly': 'Ser-Gly',
    'tca': 'TCA cycle',
    'aa': 'AA',
    'ppp': 'PPP',
    'exchange': 'Transfer and\nexchange fluxes',
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
        axis_label_format_dict, preset_default_format_dict, new_figure_config_dict, dict_label, pop=False):
    def format_dict_iter_generator(format_dict, final_repeat):
        if isinstance(format_dict, (tuple, list)):
            final_repeat[0] = True
            format_dict_iter = format_dict
        else:
            format_dict_iter = it.repeat(format_dict)
        return format_dict_iter

    final_repeat = [False]
    new_format_dict = default_parameter_extract(new_figure_config_dict, dict_label, {}, pop=pop)
    axis_label_format_dict_iter = format_dict_iter_generator(axis_label_format_dict, final_repeat)
    preset_default_format_dict_iter = format_dict_iter_generator(preset_default_format_dict, final_repeat)
    new_format_dict_iter = format_dict_iter_generator(new_format_dict, final_repeat)
    if not final_repeat[0]:
        result_format_dict = {
            **axis_label_format_dict,
            **preset_default_format_dict,
            **new_format_dict,
        }
    else:
        result_format_dict = []
        for each_axis_label_format_dict, each_preset_default_format_dict, each_new_format_dict in zip(
                axis_label_format_dict_iter, preset_default_format_dict_iter, new_format_dict_iter):
            result_format_dict.append({
                **each_axis_label_format_dict,
                **each_preset_default_format_dict,
                **each_new_format_dict,
            })
    return result_format_dict


def merge_complete_config_dict(complete_figure_config_dict, update_figure_config_dict):
    def is_danger_type(raw_obj):
        return isinstance(raw_obj, (tuple, list, dict))

    modified_figure_config_dict = dict(complete_figure_config_dict)
    for update_key, update_dict in update_figure_config_dict.items():
        if update_key not in modified_figure_config_dict:
            modified_figure_config_dict[update_key] = update_dict
        else:
            current_dict = modified_figure_config_dict[update_key]
            current_danger_type = is_danger_type(current_dict)
            update_danger_type = is_danger_type(update_dict)
            if not current_danger_type or update_dict is None:
                modified_figure_config_dict[update_key] = update_dict
            elif current_danger_type and update_danger_type:
                modified_figure_config_dict[update_key] = merge_axis_format_dict(
                    current_dict, update_dict, {}, '')
            else:
                raise ValueError()
    return modified_figure_config_dict


def net_flux_x_axis_labels_generator(flux_id_list, with_glns_m=False):
    # group_id_name_dict = {
    #     'glycolysis': 'Glycolysis',
    #     'ser_gly': 'Ser-Gly',
    #     'tca': 'TCA cycle',
    #     'aa': 'AA',
    #     'ppp': 'PPP',
    #     'exchange': 'Transfer and\nexchange fluxes',
    # }
    if with_glns_m:
        # real_x_tick_label_dict = {key: dict(each_dict) for key, each_dict in x_tick_label_dict.items()}
        # real_x_tick_label_dict['aa']['GLNS_m'] = 'GLNS_m'
        real_x_tick_label_dict = new_x_tick_label_dict
    else:
        real_x_tick_label_dict = x_tick_label_dict
    group_id_list = list(real_x_tick_label_dict.keys())
    x_tick_label_list = []
    current_group_index = 0
    last_separator_location = 0
    group_separator_list = [last_separator_location]
    group_name_location_list = []
    group_name_list = []
    current_group_id = group_id_list[current_group_index]
    current_group_label_dict = real_x_tick_label_dict[current_group_id]
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
                new_group_label_dict = real_x_tick_label_dict[new_group_id]
                x_tick_label_list.append(new_group_label_dict[flux_id])
                current_group_id = new_group_id
                current_group_label_dict = new_group_label_dict
        else:
            x_tick_label_list.append(current_group_label_dict[flux_id])
    total_item_num = len(x_tick_label_list)
    group_separator_array = np.array(group_separator_list) / total_item_num
    group_name_location_array = np.array(group_name_location_list) / total_item_num
    return x_tick_label_list, group_separator_array, group_name_location_array, group_name_list


def generate_violin_config_dict(column_width, box_body_alpha, line_width, main_color_list, median_color_list):
    return {
        ParameterName.column_width: column_width,
        ParameterName.body_props: [{
            ParameterName.face_color: main_color,
            ParameterName.alpha: box_body_alpha
        } for main_color in main_color_list],
        ParameterName.min_max_props: [{
            ParameterName.edge_color: main_color,
            ParameterName.edge_width: line_width
        } for main_color in main_color_list],
        ParameterName.median_props: [{
            ParameterName.edge_color: median_color,
            ParameterName.edge_width: line_width
        } for median_color in median_color_list],
    }


def expand_one_axis_dict(figure_data_parameter_dict):
    ax_bottom_left = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.ax_bottom_left_list, Vector(0, 0), pop=True)
    ax_size = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.ax_size_list, Vector(1, 1), pop=True)
    x_lim = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.x_lim_list, None, pop=True)
    x_label = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.x_label_list, None, pop=True)
    x_ticks = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.x_ticks_list, None, pop=True)
    x_tick_labels = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.x_tick_labels_list, Keywords.default, pop=True)
    y_lim = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.y_lim_list, None, pop=True)
    y_label = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.y_label_list, None, pop=True)
    y_ticks = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.y_ticks_list, None, pop=True)
    y_tick_labels = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.y_tick_labels_list, Keywords.default, pop=True)
    supplementary_text_list = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.supplementary_text_list, None, pop=True)
    supplementary_text_loc_list = default_parameter_extract(
        figure_data_parameter_dict, ParameterName.supplementary_text_loc_list, None, pop=True)
    expanded_axis_related_dict = {
        ParameterName.ax_bottom_left_list: [ax_bottom_left],
        ParameterName.ax_size_list: [ax_size],
        ParameterName.x_lim_list: [x_lim],
        ParameterName.x_label_list: [x_label],
        ParameterName.x_ticks_list: [x_ticks],
        ParameterName.x_tick_labels_list: [x_tick_labels],
        ParameterName.y_lim_list: [y_lim],
        ParameterName.y_ticks_list: [y_ticks],
        ParameterName.y_label_list: [y_label],
        ParameterName.y_tick_labels_list: [y_tick_labels],
        ParameterName.supplementary_text_list: [supplementary_text_list],
        ParameterName.supplementary_text_loc_list: [supplementary_text_loc_list],
    }
    return expanded_axis_related_dict
