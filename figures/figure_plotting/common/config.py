import numpy as np

from common_and_plotting_functions.functions import default_parameter_extract

float_type = 'float64'
axis_for_test = False


class Direct(object):
    figures_output_direct = 'figures/figures'
    figure_data_output_direct = 'figures/figure_data'


class Keywords(object):
    none = 'none'
    content = 'content'
    name = 'name'
    type = 'type'
    parameters = 'parameters'
    default = 'default'

    kidney = 'kidney'
    carcinoma = 'carcinoma'
    brain = 'brain'
    lung = 'lung'
    flank = 'flank'
    tumor = 'tumor'
    all_tissue = 'all_tissue'

    high_glucose = 'H'
    low_glucose = 'L'

    general = 'general'
    serum = 'serum'
    liver = 'liver'
    heart = 'heart'
    vastus_muscle = 'vastus_muscle'
    soleus_muscle = 'soleus_muscle'
    gastroc_muscle = 'gastroc_muscle'
    brown_adipose = 'brown_adipose'
    po_adipose = 'periovarian_adipose'
    sq_adipose = 'sub_q_fat'


class DataName(object):
    raw_model_raw_data = 'raw_model_raw_data'
    raw_model_all_data = 'raw_model_all_data'

    raw_data_result_label = 'raw_model__raw_data'
    all_data_result_label = 'raw_model__all_data'
    raw_data_noise_result_label = 'raw_model__raw_data_noise'
    all_data_noise_result_label = 'raw_model__all_data_noise'

    model_sensitivity = 'model_sensitivity'
    model_sensitivity_all_data = 'model_sensitivity_all_data'
    merge_reversible_reaction = 'merge_reversible_reaction'
    merge_reversible_reaction_all_data = 'merge_reversible_reaction_all_data'
    combine_consecutive_reactions = 'combine_consecutive_reactions'
    combine_consecutive_reactions_all_data = 'combine_consecutive_reactions_all_data'
    prune_branches = 'prune_branches'
    prune_branches_all_data = 'prune_branches_all_data'

    data_sensitivity = 'data_sensitivity'
    data_sensitivity_with_noise = 'data_sensitivity_with_noise'
    smaller_data_size = 'smaller_data_size'
    medium_data_plus = 'medium_data_plus'
    medium_data = 'medium_data'
    few_data = 'few_data'
    data_without_pathway = 'data_without_pathway'
    data_without_ppp = 'data_without_ppp'
    data_without_aa = 'data_without_aa'
    data_without_tca = 'data_without_tca'
    medium_data_without_combination = 'data_without_combination'
    compartmental_data = 'data_with_compartments'
    # experimental_non_compartmental_data = 'experimental_available_non-compartmental_data'

    config_sensitivity = 'config_sensitivity'
    config_sensitivity_all_data = 'config_sensitivity_all_data'
    different_flux_range = 'different_flux_range'
    different_flux_range_all_data = 'different_flux_range_all_data'
    different_constant_flux = 'different_constant_flux'
    different_constant_flux_all_data = 'different_constant_flux_all_data'
    different_constant_flux_with_noise = 'different_constant_flux_with_noise'
    different_constant_flux_with_noise_all_data = 'different_constant_flux_with_noise_all_data'

    colon_cancer_cell_line = 'colon_cancer_cell_line'
    renal_carcinoma_invivo_infusion = 'renal_carcinoma_invivo_infusion'
    lung_tumor_invivo_infusion = 'lung_tumor_invivo_infusion'
    hct116_cultured_cell_line = 'hct116_cultured_cell_line'
    multiple_tumor = 'multiple_tumor'


class ParameterName(object):
    # Basic shape parameter
    name = 'name'
    shape = 'shape'
    circle = 'circle'
    rectangle = 'rectangle'
    height_to_width_ratio = 'height_to_width_ratio'
    bottom_left = 'bottom_left'
    size = 'size'
    width = 'width'
    color = 'color'
    height = 'height'
    center = 'center'
    alpha = 'alpha'
    edge_width = 'edge_width'
    edge_style = 'edge_style'
    edge_color = 'edge_color'
    face_color = 'face_color'
    fill = 'fill'
    z_order = 'z_order'
    join_style = 'join_style'
    path_step_list = 'path_step_list'
    closed = 'closed'
    cw = 'cw'
    ccw = 'ccw'
    square_bottom_left_point = 'square_bottom_left_point'
    figure_title = 'figure_title'
    figure_title_config_dict = 'figure_title_config_dict'
    subfigure = 'subfigure'
    subfigure_label = 'subfigure_label'
    background = 'background'
    transform = 'transform'
    start = 'start'
    end = 'end'
    patch = 'patch'

    # Text
    text = 'text'
    string = 'string'
    font = 'font'
    font_size = 'font_size'
    font_color = 'font_color'
    font_weight = 'font_weight'
    font_style = 'font_style'
    horizontal = 'horizontal'
    vertical = 'vertical'
    horizontal_alignment = 'horizontal_alignment'
    vertical_alignment = 'vertical_alignment'
    angle = 'angle'
    line_space = 'line_space'

    # Arrow
    tail = 'tail'
    mid = 'mid'
    head = 'head'
    radius = 'radius'
    theta_head = 'theta_head'
    theta_tail = 'theta_tail'
    head_len_width_ratio = 'head_len_width_ratio'
    head_arrow = 'head_arrow'
    tail_arrow = 'tail_arrow'
    stem_location = 'stem_location'
    terminal_location = 'terminal_location'
    arrow = 'arrow'
    dash = 'dash'
    head_width = 'head_width'
    stem_width = 'stem_width'
    gap_line_pair_list = 'gap_line_pair_list'
    dash_solid_empty_width = 'dash_solid_empty_width'
    transition_point_list = 'transition_point_list'
    branch_list = 'branch_list'
    text_box = 'text_box'
    text_box_config = 'text_box_config'
    tail_end_center = 'tail_end_center'
    theta_tail_end_center = 'theta_tail_end_center'
    arrow_head_direction = 'arrow_head_direction'
    left_tail = 'left_tail'
    right_tail = 'right_tail'

    x_label_format_dict = 'x_label_format_dict'
    y_label_format_dict = 'y_label_format_dict'
    x_tick_label_format_dict = 'x_tick_label_format_dict'
    y_tick_label_format_dict = 'y_tick_label_format_dict'
    x_tick_separator_format_dict = 'x_tick_separator_format_dict'
    y_tick_separator_format_dict = 'y_tick_separator_format_dict'
    x_tick_separator_label_format_dict = 'x_tick_separator_label_format_dict'
    y_tick_separator_label_format_dict = 'y_tick_separator_label_format_dict'

    other_obj = 'other_obj'

    # Axis
    axis = 'axis'
    x = 'x'
    y = 'y'
    ax_top = 'top'
    ax_bottom = 'bottom'
    ax_left = 'left'
    ax_right = 'right'
    axis_tick_label_distance = 'axis_tick_label_distance'
    axis_label_distance = 'axis_label_distance'
    axis_label_location = 'axis_label_location'
    axis_tick_length = 'axis_tick_length'
    axis_line_start_distance = 'axis_line_start_distance'
    axis_line_end_distance = 'axis_line_end_distance'
    ax_total_bottom_left = 'ax_total_bottom_left'
    ax_total_size = 'ax_total_size'
    ax_interval = 'ax_interval'
    legend_center = 'legend_ax_bottom_left'
    legend_area_size = 'legend_ax_size'
    percentage = 'percentage'
    decimal_num = 'decimal_num'
    twin_x_axis = 'twin_x_axis'
    broken_y_axis = 'broken_y_axis'
    broken_point_y_lim = 'broken_point_y_lim'

    total_width = 'total_width'
    scale = 'scale'
    bottom_left_offset = 'bottom_left_offset'
    base_z_order = 'base_z_order'
    z_order_increment = 'z_order_increment'
    cap_size = 'cap_size'       # For error bar
    data_location_cap = 'data_location_cap'

    # Metabolic network
    network_type = 'network_type'
    normal_network = 'normal_network'
    exchange_network = 'exchange_network'
    input_metabolite_set = 'input_metabolite_set'
    c13_labeling_metabolite_set = 'c13_labeling_metabolite_set'
    mid_data_metabolite_set = 'mid_data_metabolite_set'
    mixed_mid_data_metabolite_set = 'mixed_mid_data_metabolite_set'
    biomass_metabolite_set = 'biomass_metabolite_set'
    boundary_flux_set = 'boundary_flux_set'
    display_flux_name = 'display_flux_name'
    reaction_text_dict = 'reaction_text_dict'
    reaction_text_config_dict = 'reaction_text_config_dict'
    reaction_raw_value_dict = 'reaction_raw_value_dict'
    extra_parameter_dict = 'extra_parameter_dict'
    all_data_mode = 'all_data_mode'
    all_mixed_data_mode = 'all_mixed_data_mode'
    infusion = 'infusion'
    text_label = 'text_label'
    visualize_flux_value = 'visualize_flux_value'
    transparency = 'transparency'
    absolute_value_output_value_dict = 'absolute_value_output_value_dict'
    metabolic_network_config_dict = 'metabolic_network_config_dict'
    metabolic_network_legend_config_dict = 'metabolic_network_legend_config_dict'
    metabolic_network_text_comment_config_dict = 'metabolic_network_text_comment_config_dict'
    hidden_metabolite_set = 'hidden_metabolite_set'
    hidden_reaction_set = 'hidden_reaction_set'
    metabolite_data_sensitivity_state_dict = 'metabolite_data_sensitivity_state_dict'
    reaction_data_sensitivity_state_dict = 'reaction_data_sensitivity_state_dict'
    extra_offset = 'extra_offset'
    reaction_flux_num = 'reaction_flux_num'
    total_flux_num = 'total_flux_num'
    total_mid_num = 'total_mid_num'
    mid_metabolite_num = 'mid_metabolite_num'
    small_network = 'small_network'
    zoom_in_box = 'zoom_in_box'

    # Reaction parameters
    class_name = 'class_name'
    reaction_name = 'reaction_name'
    reversible = 'reversible'
    boundary_flux = 'boundary_flux'

    # Diagram specific parameter
    mode = 'mode'
    simulated = 'simulated'
    experimental = 'experimental'
    sensitivity = 'sensitivity'
    random_optimized_comparison = 'random_optimized_comparison'
    distribution_type = 'distribution_type'
    global_optimum = 'global_optimum'
    local_optimum = 'local_optimum'
    one_dominant_global_optimum = 'one_dominant_global_optimum'
    multiple_similar_local_optima = 'multiple_similar_local_optima'
    repeats = 'repeats'
    loss = 'loss'
    distance = 'distance'
    optimized = 'optimized'
    unoptimized = 'unoptimized'

    # Data figure specific parameter
    data_name = 'data_name'
    figure_class = 'figure_class'
    figure_type = 'figure_type'
    all_flux = 'all_flux'
    net_euclidean_distance = 'net_euclidean_distance'
    flux_absolute_distance = 'flux_absolute_distance'
    flux_relative_distance = 'flux_relative_distance'
    time_data = 'time_data'
    loss_data = 'loss_data'
    solution_distance_data = 'solution_distance_data'
    comparison_name = 'comparison_name'
    mean = 'mean'
    std = 'std'
    flux_name = 'flux_name'
    marker_size = 'marker_size'
    column_width = 'column_width'
    class_width = 'class_width'
    color_dict = 'color_dict'
    selection_size = 'selection_size'
    selection_ratio = 'selection_ratio'
    optimized_size = 'optimized_size'

    figure_config_dict = 'figure_config_dict'
    result_label = 'result_label'
    result_label_layout_list = 'result_label_layout_list'
    mid_name_list = 'mid_name_list'
    flux_name_list = 'flux_name_list'
    display_flux_name_dict = 'display_flux_name_dict'
    display_group_name_dict = 'display_group_name_dict'
    cell_line_name_list = 'cell_line_name_list'
    flux_name_location_nested_list = 'flux_name_location_nested_list'
    figure_data_parameter_dict = 'figure_data_parameter_dict'
    raw_data_figure_parameter_dict = 'raw_data_figure_parameter_dict'
    all_data_figure_parameter_dict = 'all_data_figure_parameter_dict'
    compare_one_by_one = 'compare_one_by_one'

    x_lim_list = 'x_lim_list'
    common_x_label = 'common_x_label'
    x_label_list = 'x_label_list'
    x_ticks_list = 'x_ticks_list'
    x_tick_labels_list = 'x_tick_labels_list'
    y_lim_list = 'y_lim_list'
    common_y_label = 'common_y_label'
    y_label_list = 'y_label_list'
    y_ticks_list = 'y_ticks_list'
    y_tick_labels_list = 'y_tick_labels_list'

    tick_separator_dict_list = 'tick_separator_dict_list'
    x_tick_separator_locs = 'x_tick_separator_locs'
    x_tick_separator_labels = 'x_tick_separator_labels'
    x_tick_separator_label_locs = 'x_tick_separator_label_locs'
    y_tick_separator_locs = 'y_tick_separator_locs'
    y_tick_separator_labels = 'y_tick_separator_labels'
    y_tick_separator_label_locs = 'y_tick_separator_label_locs'

    body_props = 'body_props'
    min_max_props = 'min_max_props'
    median_props = 'median_props'

    data_figure_axes = 'data_figure_axes'
    legend = 'legend'
    name_dict = 'name_dict'
    horiz_or_vertical = 'horiz_or_vertical'

    default_y_tick_label_list = 'default_y_tick_label_list'
    common_y_lim = 'common_y_lim'

    legend_type = 'legend_type'
    patch_legend = 'patch_legend'
    legend_config_dict = 'legend_config_dict'
    text_config_dict = 'text_config_dict'
    total_horiz_edge_ratio = 'total_horiz_edge_ratio'
    col_horiz_edge_ratio = 'col_horiz_edge_ratio'
    total_verti_edge_ratio = 'total_verti_edge_ratio'
    row_verti_edge_ratio = 'row_verti_edge_ratio'
    legend_patch_config_dict = 'legend_patch_config_dict'
    location_config_dict = 'location_config_dict'

    error_bar = 'error_bar'
    error_bar_param_dict = 'error_bar_param_dict'
    scatter_line = 'scatter_line'

    cbar = 'cbar'
    cbar_config = 'cbar_config'

    # Published data parameters
    multiple_tumor = DataName.multiple_tumor
    condition = 'condition'


# class MPLParameterName(ParameterName):
#     # Basic shape
#     face_color = 'facecolor'
#     edge_color = 'edgecolor'
#
#     # Text
#     font = 'fontname'
#     font_size = 'fontsize'
#     font_color = 'color'
#     font_style = 'fontstyle'
#     font_weight = 'fontweight'
#     horizontal_alignment = 'horizontalalignment'
#     vertical_alignment = 'verticalalignment'
#     rotation = 'rotation'
#     rotation_mode = 'rotation_mode'
#     z_order = 'zorder'
#     edge_style = 'linestyle'
#     edge_width = 'linewidth'
#     transform = 'transform'
#
#     error_bar_color = 'ecolor'
#     error_bar_capsize = 'capsize'
#     error_bar_line_width = 'elinewidth'
#     error_bar_line_width2 = 'capthick'
#
#     axis_tick_label_font_size = 'labelsize'
#     axis_tick_label_font_color = 'labelcolor'
#     axis_tick_color = 'color'
#     axis_tick_width = 'width'
#     axis_tick_length = 'length'
#     axis_tick_parameter_map = {
#         edge_color: axis_tick_color,
#         edge_width: axis_tick_width,
#         font_size: axis_tick_label_font_size,
#         font_color: axis_tick_label_font_color
#     }


class Constant(object):
    # default_figure_size = (12, 6)        # with unit inches
    default_figure_size = (8.5, 11)     # with unit inches
    square_figure_size = (8.5, 8.5)
    plotting_eps = 1e-9
    point_size_constant = 1 / 72        # with unit inches
    shape_parameter_unit = 1 / 100      # for better

    computation_eps = 1e-10


def figure_path_generator(figure_name):
    return '{}/{}.pdf'.format(Direct.figures_output_direct, figure_name)


def figure_data_path_generator(figure_name):
    return '{}/{}.xlsx'.format(Direct.figure_data_output_direct, figure_name)


def numbered_even_sequence(start, step, num):
    return np.arange(num) * step + start
