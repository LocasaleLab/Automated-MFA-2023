from .classes import Color, white_color, black_color
from .third_party_packages import mcolors


class ColorConfig(object):
    cmap = 'coolwarm'

    white_color = white_color
    black_color = black_color
    light_gray = Color(240, 240, 240)
    medium_light_gray = Color(220, 220, 220)
    gray = Color(200, 200, 200)
    cyan = Color(101, 191, 214)
    sky = Color(126, 206, 244)
    light_bright_sky = Color(129, 210, 251)
    deep_sky = Color(93, 192, 241)
    super_light_bright_blue = Color(243, 250, 255)
    super_light_blue = Color(239, 249, 255)
    medium_light_blue = Color(232, 246, 255)
    medium_light_bright_blue = Color(237, 249, 255)
    light_bright_blue = Color(225, 243, 255)
    light_blue = Color(215, 239, 255)
    dark_light_bright_blue = Color(215, 239, 255)
    light_medium_blue = Color(193, 217, 233)
    light_medium_bright_blue = Color(195, 231, 255)
    medium_blue = Color(161, 198, 223)
    medium_bright_blue = Color(175, 217, 245)
    normal_blue = Color(91, 155, 213)
    dark_blue = Color(31, 119, 180)
    # dark_blue = Color(21, 113, 177)
    orange = Color(251, 138, 68)
    bar_orange = Color(255, 127, 14)
    slightly_light_orange = Color(252, 168, 116)
    medium_bright_orange = Color(255, 193, 155)
    medium_orange = Color(252, 175, 128)
    light_medium_bright_orange = Color(255, 205, 175)
    light_bright_orange = Color(255, 224, 205)
    light_orange = Color(253, 208, 180)
    dark_orange = Color(229, 90, 5)
    solid_dark_orange = Color(243, 160, 110, a=1)
    purple = Color(112, 48, 160)
    medium_purple = purple.transparency_mix(0.7)
    light_purple = purple.transparency_mix(0.5)
    green = Color(44, 160, 44)
    light_green = Color(161, 209, 109)
    super_light_green = Color(184, 224, 140)
    yellow = Color(255, 217, 102)
    brown = Color(230, 175, 0)

    # aqua_blue = Color(102, 161, 215)
    # metabolite_blue = Color(148, 188, 223)
    # metabolite_blue = Color(98, 159, 214)
    # metabolite_blue = Color(119, 171, 218)
    metabolite_blue = Color(148, 188, 223)
    gray_orange = Color(238, 141, 82)
    dark_gray_orange = Color(200, 89, 20)
    # metabolite_orange = Color(248, 193, 159)
    metabolite_orange = Color(251, 174, 127)
    # metabolite_orange = Color(251, 178, 133)
    # metabolite_orange = Color(249, 185, 145)
    # metabolite_orange = Color(252, 198, 148)
    # metabolite_sky = Color(157, 214, 243)
    metabolite_sky = Color(121, 200, 239)
    metabolite_dark_blue = Color(105, 151, 191)
    metabolite_darker_blue = Color(94, 142, 186)
    metabolite_green = Color(166, 214, 166)
    metabolite_gold = Color(253, 228, 147)
    metabolite_yellow = Color(253, 228, 147)
    darker_yellow = Color(252, 218, 105)
    mid_red = Color(255, 87, 87)
    mixed_mid_red = Color(242, 118, 118)
    biomass_purple = Color(174, 127, 213)
    reaction_blue = Color(110, 170, 230)
    reaction_green = Color(192, 228, 152)
    reaction_gold = Color(254, 238, 186)
    pink = Color(255, 192, 203)

    lower_alpha_value = 0.2
    base_alpha_value = 0.3
    alpha_for_bar_plot = base_alpha_value + 0.1
    alpha_for_heatmap = base_alpha_value + 0.2
    higher_alpha = 0.6

    # Metabolic network:
    # normal_metabolite_color = cyan
    # input_metabolite_color = deep_sky
    # c13_metabolite_color = light_green
    # mid_metabolite_color = yellow
    # mixed_mid_metabolite_circle_color = Color(255, 87, 87)
    # biomass_metabolite_arrow_color = Color(161, 98, 208)
    normal_metabolite_color = metabolite_blue
    metabolite_text_color = white_color
    # input_metabolite_color = metabolite_sky
    input_metabolite_color = metabolite_dark_blue
    # c13_metabolite_color = metabolite_gold
    c13_metabolite_color = gray_orange
    mid_metabolite_color = medium_bright_orange
    mixed_mid_metabolite_circle_color = mixed_mid_red
    biomass_metabolite_arrow_color = biomass_purple
    metabolite_few_data_set = dark_gray_orange

    # normal_reaction_color = normal_blue
    normal_reaction_color = reaction_blue
    # boundary_reaction_color = super_light_green
    boundary_reaction_color = light_medium_bright_orange
    # cell_network_color = super_light_blue
    cell_network_color = super_light_bright_blue
    # mitochondria_network_color = light_blue
    mitochondria_network_color = light_bright_blue
    subnetwork_text_color = black_color

    to_known_flux_distance_arrow_color = medium_orange
    to_optimal_distance_arrow_color = brown
    to_optimal_distance_arrow_color_with_alpha = to_optimal_distance_arrow_color.transparency_mix(higher_alpha)

    loss_color = purple
    loss_color_with_alpha = loss_color.transparency_mix(higher_alpha)

    # Data figure:
    data_figure_base_color = dark_blue
    data_figure_contrast_color = orange
    heatmap_inner_text_color_pair = (white_color, black_color)
    axis_line_color = black_color
    axis_tick_label_text_color = black_color
    scatter_figure_color_list = [dark_blue, orange, purple]

    random_flux_color = green
    random_flux_color_with_alpha = random_flux_color.transparency_mix(higher_alpha)
    optimized_flux_color = dark_blue
    optimized_flux_color_with_alpha = optimized_flux_color.transparency_mix(higher_alpha)
    # experimental_flux_color = bar_orange
    experimental_flux_color = orange
    experimental_flux_color_with_alpha = experimental_flux_color.transparency_mix(higher_alpha)
    # raw_distance_color = orange
    # net_distance_color = dark_orange
    # net_distance_legend_color = solid_dark_orange
    # raw_distance_color = normal_blue
    # raw_distance_color_with_alpha = raw_distance_color.transparency_mix(higher_alpha)
    # net_distance_color = distance_text_color = net_distance_text_color = dark_blue
    raw_distance_color = darker_yellow
    raw_distance_color_with_alpha = raw_distance_color.transparency_mix(higher_alpha)
    net_distance_color = distance_text_color = brown
    net_distance_legend_color = Color(243, 214, 117).add_transparency(1)
    global_optimum_color = mid_red
    global_optimum_color_with_alpha = mixed_mid_red
    known_flux_color = mixed_mid_red
    known_flux_text_color = mid_red

    cmap_list = [(0, normal_blue), (0.5, light_gray), (1, slightly_light_orange)]
    my_color_map = mcolors.LinearSegmentedColormap.from_list('BlueOrange', cmap_list)

    # different_simulated_distance = purple
    different_simulated_distance = mid_red
    initial_solution_color = random_flux_color_with_alpha
    selected_solution_color = medium_orange
    selected_solution_text_color = orange
    averaged_solution_color = normal_blue
    averaged_solution_text_color = dark_blue
    # reoptimized_solution_color = green
    # reoptimized_solution_color = mid_red
    # reoptimized_solution_text_color = mid_red
    reoptimized_solution_color = medium_purple
    reoptimized_solution_text_color = purple

    blue_white_orange_color_list = [
        dark_blue.transparency_mix(alpha_for_heatmap), white_color,
        dark_orange.transparency_mix(alpha_for_heatmap)]

    @staticmethod
    def check_if_color(color_obj):
        return isinstance(color_obj, Color)


class TextConfig(object):
    main_text_font = 'Calibri'
    # equation_font = 'Computer Modern'


class ZOrderConfig(object):
    default_image_z_order = 0
    default_patch_z_order = 1
    default_axis_z_order = 2.01
    default_text_z_order = 3
    default_legend_z_order = 5
    z_order_increment = 0.01
    default_subfigure_label_z_order = 6

