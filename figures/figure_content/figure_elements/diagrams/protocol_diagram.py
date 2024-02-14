from .config import np, Vector, ParameterName, FontWeight
from .config import BentChevronArrow, ChevronArrow, CompositeFigure, Rectangle, TextBox, RoundRectangle
from .config import ZOrderConfig, TextConfig, HorizontalAlignment, VerticalAlignment, \
    ColorConfig, CommonElementConfig, CommonFigureString
from .single_protocol_diagram import InitialDistributionDiagram, LossDistributionDiagram, \
    HorizontalLossDistributionDiagram, AverageDiagram, HorizontalComparisonDiagram, HeatmapDiagram


class ProtocolDiagramConfig(object):
    dim_dict = {
        # total_width, total_height
        ParameterName.vertical: (0.5, 0.65),
        ParameterName.simulated: (1.1, 0.6),
        ParameterName.simulated_reoptimization: (1.1, 0.5),
        ParameterName.sensitivity: (1.1, 0.5),
        ParameterName.experimental: (0.8, 0.54),
    }
    upper_text_common_config_dict = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: 12,
        ParameterName.width: 0.23,
        ParameterName.height: 0.1,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
        ParameterName.font_weight: FontWeight.bold,
        # ParameterName.text_box: True,
        ParameterName.line_space: 1.5
    }
    selected_solution_color = ColorConfig.selected_solution_color
    selected_solution_text_color = ColorConfig.selected_solution_text_color
    averaged_solution_color = ColorConfig.averaged_solution_color
    averaged_solution_text_color = ColorConfig.averaged_solution_text_color
    reoptimized_solution_color = ColorConfig.reoptimized_solution_color
    reoptimized_solution_text_color = ColorConfig.reoptimized_solution_text_color
    final_text_common_config_dict = {
        **upper_text_common_config_dict,
        ParameterName.font_size: upper_text_common_config_dict[ParameterName.font_size] + 2
    }
    chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: CommonElementConfig.normal_chevron_width - 0.01,
    }
    bent_chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: CommonElementConfig.normal_chevron_width - 0.015,
        ParameterName.radius: 0.04,
    }

    class CommonTitleText(object):
        bold_math_m = CommonFigureString.bold_math_m
        bold_math_n = CommonFigureString.bold_math_n
        initial_point = f'Generate ${bold_math_n}$ random\ninitial points'
        optimization = f'Obtain ${bold_math_n}$ optimized\nsolutions'
        selection = f'Select ${bold_math_m}$ solutions\nwith minimal loss'
        selection_best = 'Select one solution\nwith minimal loss'
        final_result = 'Final MFA result'
        average = 'Calculate average of\nselected solutions'
        euclidean_distance = 'Calculate Euclidean\ndistance and relative\nerror of average solution'
        mean_and_std = f'Calculate mean and STD\nof distribution under\ndifferent ${bold_math_m}$ and ${bold_math_n}$'
        repeat_for_distribution = 'Repeat this step to\nobtain distributions'
        re_optimization = 'Optimize again\nfrom averaged solutions'


def height_to_width_ratio_calculation(mode):
    dim_dict = ProtocolDiagramConfig.dim_dict
    total_width, total_height = dim_dict[mode]
    return total_width, total_height


class ProtocolDiagram(CompositeFigure):
    total_width = 1
    total_height = 1

    def __init__(self, mode=ParameterName.simulated, **kwargs):
        total_width, total_height = height_to_width_ratio_calculation(mode)
        self.total_width = total_width
        self.total_height = total_height
        if mode == ParameterName.vertical:
            diagram_generator = vertical_protocol_diagram_generator
        else:
            diagram_generator = protocol_diagram_generator
        text_obj_list, chevron_arrow_obj_list, constructed_obj_list = diagram_generator(mode)
        optimization_diagram_dict = {
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            ParameterName.chevron_arrow: {
                chevron_arrow_obj.name: chevron_arrow_obj for chevron_arrow_obj in chevron_arrow_obj_list},
            ParameterName.constructed_obj: {
                constructed_obj.name: constructed_obj for constructed_obj in constructed_obj_list},
        }
        super().__init__(
            optimization_diagram_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        mode = args[0]
        self.total_width, self.total_height = height_to_width_ratio_calculation(mode)
        return Vector(self.total_width, self.total_height) / 2 * scale


def protocol_diagram_generator(mode):
    text_obj_list = []
    chevron_arrow_obj_list = []
    constructed_obj_list = []
    common_scale = 0.25
    total_width, total_height = height_to_width_ratio_calculation(mode)
    vertical_axis_1 = 0.08
    vertical_axis_2 = 0.256
    vertical_axis_3 = 0.442
    vertical_axis_4 = 0.68
    vertical_axis_5 = 0.98
    # vertical_axis_1 = 0.065
    # vertical_axis_2 = 0.235
    # vertical_axis_3 = 0.41
    # vertical_axis_4 = 0.64
    # vertical_axis_5 = 0.9
    # vertical_axis_2 = 0.11
    # vertical_axis_3 = 0.29
    # vertical_axis_4 = 0.54
    # vertical_axis_5 = 0.85
    common_title_text = ProtocolDiagramConfig.CommonTitleText

    loss_diagram_height_mode = ParameterName.normal
    if mode == ParameterName.simulated_reoptimization:
        upper_text_horizontal_axis = 0.46
        loss_diagram_axis = 0.29
        average_diagram_axis = loss_diagram_axis
        lower_main_axis = 0.05
        horizontal_comparison_diagram_axis = average_diagram_axis - 0.16
        horizontal_comparison_diagram_axis_2 = None
        horizontal_comparison_diagram_axis_3 = None
        loss_diagram_height_mode = ParameterName.low_height
    elif mode == ParameterName.simulated:
        upper_text_horizontal_axis = 0.56
        loss_diagram_axis = 0.36
        average_diagram_axis = 0.40
        lower_main_axis = 0.08
        horizontal_comparison_diagram_axis = average_diagram_axis - 0.16
        horizontal_comparison_diagram_axis_2 = None
        horizontal_comparison_diagram_axis_3 = None
    elif mode == ParameterName.sensitivity:
        upper_text_horizontal_axis = 0.46
        loss_diagram_axis = 0.25
        average_diagram_axis = 0.295
        lower_main_axis = 0.08
        middle_axis = average_diagram_axis - 0.01
        horizontal_comparison_diagram_axis = middle_axis + 0.09
        horizontal_comparison_diagram_axis_2 = middle_axis
        horizontal_comparison_diagram_axis_3 = middle_axis - 0.075
    elif mode == ParameterName.experimental:
        upper_text_horizontal_axis = 0.5
        loss_diagram_axis = 0.29
        average_diagram_axis = 0.33
        horizontal_comparison_diagram_axis = 0.11
        horizontal_comparison_diagram_axis_2 = 0.03
        horizontal_comparison_diagram_axis_3 = None
        lower_main_axis = (horizontal_comparison_diagram_axis + horizontal_comparison_diagram_axis_2) / 2
    else:
        raise ValueError()

    upper_text_1_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.initial_point,
        ParameterName.center: Vector(vertical_axis_1 + 0.005, upper_text_horizontal_axis)
    }
    text_obj_list.append(TextBox(**upper_text_1_config_dict))
    center_of_initial_distribution_diagram = InitialDistributionDiagram.calculate_center(
        InitialDistributionDiagram, common_scale)
    target_center_of_initial_diagram = Vector(vertical_axis_1, loss_diagram_axis + 0.01)
    initial_diagram = InitialDistributionDiagram(
        scale=common_scale,
        bottom_left_offset=target_center_of_initial_diagram - center_of_initial_distribution_diagram)
    constructed_obj_list.append(initial_diagram)

    upper_text_x_shift = 0.015
    upper_text_2_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.optimization,
        ParameterName.center: Vector(vertical_axis_2 + upper_text_x_shift, upper_text_horizontal_axis)
    }
    text_obj_list.append(TextBox(**upper_text_2_config_dict))
    center_of_loss_distribution_diagram = LossDistributionDiagram.calculate_center(
        LossDistributionDiagram, common_scale, mode=ParameterName.loss_data, height=loss_diagram_height_mode)
    target_center_of_loss_diagram_1 = Vector(vertical_axis_2, loss_diagram_axis)
    loss_diagram_1 = LossDistributionDiagram(
        selected=False, mode=ParameterName.loss_data, height=loss_diagram_height_mode, scale=common_scale,
        bottom_left_offset=target_center_of_loss_diagram_1 - center_of_loss_distribution_diagram)
    constructed_obj_list.append(loss_diagram_1)

    chevron_arrow_1_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(target_center_of_initial_diagram.x + 0.06, loss_diagram_axis),
        ParameterName.head: Vector(target_center_of_loss_diagram_1.x - 0.055, loss_diagram_axis),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_1_config))

    upper_text_3_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.selection,
        ParameterName.center: Vector(vertical_axis_3 + upper_text_x_shift, upper_text_horizontal_axis)
    }
    text_obj_list.append(TextBox(**upper_text_3_config_dict))
    target_center_of_loss_diagram_2 = Vector(vertical_axis_3, loss_diagram_axis)
    loss_diagram_2 = LossDistributionDiagram(
        selected=True, mode=ParameterName.loss_data, height=loss_diagram_height_mode, scale=common_scale,
        bottom_left_offset=target_center_of_loss_diagram_2 - center_of_loss_distribution_diagram)
    constructed_obj_list.append(loss_diagram_2)

    chevron_arrow_2_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(target_center_of_loss_diagram_1.x + 0.07, loss_diagram_axis),
        ParameterName.head: Vector(target_center_of_loss_diagram_2.x - 0.055, loss_diagram_axis),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_2_config))

    if mode in {ParameterName.sensitivity, ParameterName.experimental}:
        upper_text_4_string = common_title_text.average
        chevron_arrow_3_y_loc = average_diagram_axis
    elif mode == ParameterName.simulated_reoptimization:
        upper_text_4_string = common_title_text.average
        chevron_arrow_3_y_loc = loss_diagram_axis
    elif mode == ParameterName.simulated:
        upper_text_4_string = common_title_text.euclidean_distance
        chevron_arrow_3_y_loc = loss_diagram_axis
    else:
        raise ValueError()
    upper_text_4_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: upper_text_4_string,
        ParameterName.center: Vector(vertical_axis_4, upper_text_horizontal_axis)
    }
    text_obj_list.append(TextBox(**upper_text_4_config_dict))
    center_of_average_diagram = AverageDiagram.calculate_center(AverageDiagram, common_scale)
    target_center_of_average_diagram = Vector(vertical_axis_4, average_diagram_axis)

    average_diagram = AverageDiagram(
        mode, scale=common_scale,
        bottom_left_offset=target_center_of_average_diagram - center_of_average_diagram)
    constructed_obj_list.append(average_diagram)

    if mode == ParameterName.simulated:
        title_string = 'Relative error'
        center_of_horizontal_comparison_diagram = HorizontalComparisonDiagram.calculate_center(
            HorizontalComparisonDiagram, common_scale, title_string)
        target_center_of_horizontal_comparison_diagram = Vector(vertical_axis_4, horizontal_comparison_diagram_axis)
        horizontal_comparison_diagram = HorizontalComparisonDiagram(
            average_flux_value=0.62, title_string=title_string, flux_index=1, known_flux_value=0.4,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_comparison_diagram - center_of_horizontal_comparison_diagram)
        constructed_obj_list.append(horizontal_comparison_diagram)
    elif mode == ParameterName.experimental:
        title_string = 'Mean and STD of each flux'
        center_of_horizontal_diagram_1 = HorizontalComparisonDiagram.calculate_center(
            HorizontalComparisonDiagram, common_scale, title_string)
        target_center_of_horizontal_diagram_1 = Vector(vertical_axis_4, horizontal_comparison_diagram_axis)
        horizontal_comparison_diagram_1 = HorizontalComparisonDiagram(
            average_flux_value=0.3, title_string=title_string, flux_index=1, standard_deviation=0.1,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_diagram_1 - center_of_horizontal_diagram_1)
        center_of_horizontal_diagram_2 = HorizontalComparisonDiagram.calculate_center(
            HorizontalComparisonDiagram, common_scale, None)
        target_center_of_horizontal_diagram_2 = Vector(vertical_axis_4, horizontal_comparison_diagram_axis_2)
        horizontal_comparison_diagram_2 = HorizontalComparisonDiagram(
            average_flux_value=0.55, title_string=None, flux_index=2, standard_deviation=0.2,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_diagram_2 - center_of_horizontal_diagram_2)
        constructed_obj_list.extend([horizontal_comparison_diagram_1, horizontal_comparison_diagram_2])
    else:
        pass

    chevron_arrow_3_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(target_center_of_loss_diagram_2.x + 0.07, chevron_arrow_3_y_loc),
        ParameterName.head: Vector(target_center_of_average_diagram.x - 0.11, chevron_arrow_3_y_loc),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_3_config))

    distance = 0.1
    left_x_loc = vertical_axis_5 - distance / 2
    right_x_loc = vertical_axis_5 + distance / 2
    if mode == ParameterName.simulated:
        center_of_relative_error = center_of_euclidean_distance = center_of_loss_distribution_diagram
        target_center_of_euclidean_distance = Vector(left_x_loc, loss_diagram_axis)
        target_center_of_relative_error = Vector(right_x_loc, loss_diagram_axis)
        euclidean_distance_distribution_diagram = LossDistributionDiagram(
            mode=ParameterName.net_euclidean_distance, scale=common_scale,
            bottom_left_offset=target_center_of_euclidean_distance - center_of_euclidean_distance)
        relative_error_distribution_diagram = LossDistributionDiagram(
            mode=ParameterName.flux_relative_distance, scale=common_scale,
            bottom_left_offset=target_center_of_relative_error - center_of_relative_error)
        constructed_obj_list.extend([euclidean_distance_distribution_diagram, relative_error_distribution_diagram])
        chevron_arrow_4_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(target_center_of_average_diagram.x + 0.13, loss_diagram_axis),
            ParameterName.head: Vector(left_x_loc - 0.055, loss_diagram_axis),
        }
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_4_config))
        upper_text_5_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: common_title_text.repeat_for_distribution,
            ParameterName.center: Vector(vertical_axis_5, upper_text_horizontal_axis)
        }
        text_obj_list.append(TextBox(**upper_text_5_config_dict))

        heatmap_size = Vector(4, 4)
        center_of_heatmap = HeatmapDiagram.calculate_center(HeatmapDiagram, common_scale, heatmap_size)
        target_mean_heatmap_center = Vector(left_x_loc - 0.06, lower_main_axis)
        target_std_heatmap_center = Vector(right_x_loc - 0.02, lower_main_axis)
        mean_heatmap_diagram = HeatmapDiagram(
            size=heatmap_size, mean_or_std=ParameterName.mean, mode=ParameterName.simulated, scale=common_scale,
            bottom_left_offset=target_mean_heatmap_center - center_of_heatmap)
        std_heatmap_diagram = HeatmapDiagram(
            size=heatmap_size, mean_or_std=ParameterName.std, mode=ParameterName.simulated, scale=common_scale,
            bottom_left_offset=target_std_heatmap_center - center_of_heatmap)
        constructed_obj_list.extend([mean_heatmap_diagram, std_heatmap_diagram])

        chevron_arrow4_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(vertical_axis_5 + 0.01, loss_diagram_axis - 0.15),
            ParameterName.head: Vector(vertical_axis_5 + 0.01, lower_main_axis + 0.075),
        }
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow4_config))

        mean_and_std_text_center_x = vertical_axis_4 - 0.02
        upper_text_6_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: common_title_text.mean_and_std,
            ParameterName.center: Vector(mean_and_std_text_center_x, lower_main_axis + 0.005),
        }
        text_obj_list.append(TextBox(**upper_text_6_config_dict))

        fit_text_center_x = vertical_axis_3 - 0.1
        upper_text_7_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: 'Low mean: fit accurately',
            ParameterName.center: Vector(fit_text_center_x, lower_main_axis + 0.02)
        }
        upper_text_8_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: 'Low STD: fit consistently',
            ParameterName.center: Vector(fit_text_center_x, lower_main_axis - 0.02)
        }
        text_obj_list.extend([TextBox(**upper_text_7_config_dict), TextBox(**upper_text_8_config_dict)])

        chevron_arrow_6_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(mean_and_std_text_center_x - 0.12, lower_main_axis),
            ParameterName.head: Vector(fit_text_center_x + 0.13, lower_main_axis),
        }
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_6_config))
    elif mode == ParameterName.simulated_reoptimization:
        chevron_arrow_4_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(target_center_of_average_diagram.x + 0.13, loss_diagram_axis),
            ParameterName.head: Vector(left_x_loc - 0.055, loss_diagram_axis),
        }
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_4_config))

        upper_text_5_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: common_title_text.re_optimization,
            ParameterName.center: Vector(vertical_axis_5, upper_text_horizontal_axis)
        }
        text_obj_list.append(TextBox(**upper_text_5_config_dict))
        center_of_opti_from_average_diagram = AverageDiagram.calculate_center(AverageDiagram, common_scale)
        target_center_of_opti_from_average_diagram = Vector(vertical_axis_5, average_diagram_axis)
        average_diagram = AverageDiagram(
            ParameterName.optimization_from_average_solutions, scale=common_scale,
            bottom_left_offset=target_center_of_opti_from_average_diagram - center_of_opti_from_average_diagram)
        constructed_obj_list.append(average_diagram)

        arrow_x_value_list = [vertical_axis_3 + upper_text_x_shift, vertical_axis_4, vertical_axis_5]
        # chevron_arrow_tail_y_value = loss_diagram_axis - 0.18
        chevron_arrow_tail_y_value = lower_main_axis + 0.09
        chevron_arrow_head_y_value = lower_main_axis + 0.035
        chevron_arrow_config_list = [{
                **ProtocolDiagramConfig.chevron_config,
                ParameterName.tail_end_center: Vector(arrow_x_value_list[0], chevron_arrow_tail_y_value),
                ParameterName.head: Vector(arrow_x_value_list[0], chevron_arrow_head_y_value),
            },
            {
                **ProtocolDiagramConfig.chevron_config,
                ParameterName.tail_end_center: Vector(arrow_x_value_list[1], chevron_arrow_tail_y_value),
                ParameterName.head: Vector(arrow_x_value_list[1], chevron_arrow_head_y_value),
            },
            {
                **ProtocolDiagramConfig.chevron_config,
                ParameterName.tail_end_center: Vector(arrow_x_value_list[2], chevron_arrow_tail_y_value),
                ParameterName.head: Vector(arrow_x_value_list[2], chevron_arrow_head_y_value),
            }]
        chevron_arrow_obj_list.extend(
            [ChevronArrow(**chevron_arrow_config) for chevron_arrow_config in chevron_arrow_config_list])
        bottom_text_common_config = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.font_size: 15
        }
        bottom_text_config_dict_list = [{
                **bottom_text_common_config,
                ParameterName.font_color: ProtocolDiagramConfig.selected_solution_text_color,
                ParameterName.string: CommonFigureString.selected_solution_wrap,
                ParameterName.center: Vector(arrow_x_value_list[0], lower_main_axis)
            },
            {
                **bottom_text_common_config,
                ParameterName.font_color: ProtocolDiagramConfig.averaged_solution_text_color,
                ParameterName.string: CommonFigureString.averaged_solution_wrap,
                ParameterName.center: Vector(arrow_x_value_list[1], lower_main_axis)
            },
            {
                **bottom_text_common_config,
                ParameterName.font_color: ProtocolDiagramConfig.reoptimized_solution_text_color,
                ParameterName.string: CommonFigureString.reoptimized_solution_wrap,
                ParameterName.center: Vector(arrow_x_value_list[2], lower_main_axis)
            },
        ]
        text_obj_list.extend(
            [TextBox(**bottom_text_config_dict) for bottom_text_config_dict in bottom_text_config_dict_list])
    elif mode == ParameterName.sensitivity:
        title_string = 'Relative error'
        center_of_horizontal_diagram_1 = HorizontalComparisonDiagram.calculate_center(
            HorizontalComparisonDiagram, common_scale, title_string)
        target_center_of_horizontal_diagram_1 = Vector(vertical_axis_5, horizontal_comparison_diagram_axis)
        horizontal_comparison_diagram_1 = HorizontalComparisonDiagram(
            average_flux_value=0.55, title_string=title_string, flux_index=1, known_flux_value=0.78,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_diagram_1 - center_of_horizontal_diagram_1)
        center_of_horizontal_diagram_2 = HorizontalComparisonDiagram.calculate_center(
            HorizontalComparisonDiagram, common_scale, None)
        target_center_of_horizontal_diagram_2 = Vector(vertical_axis_5, horizontal_comparison_diagram_axis_2)
        horizontal_comparison_diagram_2 = HorizontalComparisonDiagram(
            average_flux_value=0.67, title_string=None, flux_index=2, known_flux_value=0.45,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_diagram_2 - center_of_horizontal_diagram_2)
        target_center_of_horizontal_diagram_3 = Vector(vertical_axis_5, horizontal_comparison_diagram_axis_3)
        horizontal_comparison_diagram_3 = HorizontalComparisonDiagram(
            average_flux_value=0.29, title_string=None, flux_index=3, known_flux_value=0.5,
            mode=mode, scale=common_scale,
            bottom_left_offset=target_center_of_horizontal_diagram_3 - center_of_horizontal_diagram_2)
        constructed_obj_list.extend(
            [horizontal_comparison_diagram_1, horizontal_comparison_diagram_2, horizontal_comparison_diagram_3])

        chevron_arrow_4_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(target_center_of_average_diagram.x + 0.125, average_diagram_axis),
            ParameterName.head: Vector(vertical_axis_5 - 0.1, average_diagram_axis),
        }
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_4_config))
        upper_text_5_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: 'Calculate relative error\nbetween average and\nthe known flux',
            ParameterName.center: Vector(vertical_axis_5, upper_text_horizontal_axis)
        }
        text_obj_list.append(TextBox(**upper_text_5_config_dict))

        heatmap_x_loc = vertical_axis_4 + 0.1
        heatmap_size = Vector(4, 8)
        center_of_heatmap = HeatmapDiagram.calculate_center(HeatmapDiagram, common_scale, heatmap_size)
        target_heatmap_center = Vector(heatmap_x_loc, lower_main_axis)
        mean_heatmap_diagram = HeatmapDiagram(
            size=heatmap_size, mode=ParameterName.sensitivity, scale=common_scale,
            bottom_left_offset=target_heatmap_center - center_of_heatmap)
        constructed_obj_list.append(mean_heatmap_diagram)

        upper_text_6_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: 'Plot heatmap of\nrelative errors',
            ParameterName.center: Vector(heatmap_x_loc - 0.185, lower_main_axis + 0.005),
        }
        text_obj_list.append(TextBox(**upper_text_6_config_dict))

        chevron_arrow_5_config = {
            **ProtocolDiagramConfig.bent_chevron_config,
            ParameterName.tail_end_center: Vector(vertical_axis_5 + 0.02, lower_main_axis + 0.08),
            ParameterName.head: Vector(heatmap_x_loc + 0.13, lower_main_axis),
            ParameterName.arrow_head_direction: ParameterName.cw,
        }
        chevron_arrow_obj_list.append(BentChevronArrow(**chevron_arrow_5_config))
    elif mode == ParameterName.experimental:
        upper_text_5_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.string: 'Analysis of each flux\nfrom averaged solutions',
            ParameterName.center: Vector(vertical_axis_3 + 0.03, lower_main_axis + 0.01),
        }
        text_obj_list.append(TextBox(**upper_text_5_config_dict))

        chevron_center = vertical_axis_4 + 0.01
        chevron_arrow_4_top_y = average_diagram_axis - 0.115
        chevron_arrow_4_bottom_y = horizontal_comparison_diagram_axis + 0.05
        chevron_arrow_4_config = {
            **ProtocolDiagramConfig.chevron_config,
            ParameterName.tail_end_center: Vector(chevron_center, chevron_arrow_4_top_y),
            ParameterName.head: Vector(chevron_center, chevron_arrow_4_bottom_y),
        }
        chevron_arrow_text_center_y = (chevron_arrow_4_top_y + chevron_arrow_4_bottom_y) / 2 + 0.005
        chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow_4_config))
        chevron_arrow_text_config_dict = {
            **ProtocolDiagramConfig.upper_text_common_config_dict,
            ParameterName.font_size: ProtocolDiagramConfig.upper_text_common_config_dict[ParameterName.font_size] - 2,
            ParameterName.string: 'Repeat from different\ninitial points',
            ParameterName.center: Vector(chevron_center - 0.1, chevron_arrow_text_center_y),
        }
        text_obj_list.append(TextBox(**chevron_arrow_text_config_dict))
    else:
        raise ValueError()

    return text_obj_list, chevron_arrow_obj_list, constructed_obj_list


def vertical_protocol_diagram_generator(mode):
    text_obj_list = []
    chevron_arrow_obj_list = []
    constructed_obj_list = []
    common_scale = 0.25
    # 0.5, 0.8
    total_width, total_height = height_to_width_ratio_calculation(ParameterName.vertical)
    left_text_vertical_axis = 0.085
    right_main_vertical_axis = 0.335
    horizontal_axis_1 = 0.58
    horizontal_axis_2 = 0.38
    horizontal_axis_3 = 0.18
    horizontal_axis_4 = 0.03
    common_title_text = ProtocolDiagramConfig.CommonTitleText

    left_text_1_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.initial_point,
        ParameterName.center: Vector(left_text_vertical_axis, horizontal_axis_1)
    }
    text_obj_list.append(TextBox(**left_text_1_config_dict))
    center_of_initial_distribution_diagram = InitialDistributionDiagram.calculate_center(
        InitialDistributionDiagram, common_scale)
    target_center_of_initial_diagram = Vector(right_main_vertical_axis, horizontal_axis_1)
    initial_diagram = InitialDistributionDiagram(
        scale=common_scale,
        bottom_left_offset=target_center_of_initial_diagram - center_of_initial_distribution_diagram)
    constructed_obj_list.append(initial_diagram)

    left_text_2_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.optimization,
        ParameterName.center: Vector(left_text_vertical_axis, horizontal_axis_2 + 0.01)
    }
    text_obj_list.append(TextBox(**left_text_2_config_dict))
    center_of_loss_distribution_diagram = HorizontalLossDistributionDiagram.calculate_center(
        HorizontalLossDistributionDiagram, common_scale)
    target_center_of_loss_diagram_1 = Vector(right_main_vertical_axis, horizontal_axis_2)
    loss_diagram_1 = HorizontalLossDistributionDiagram(
        selected=False, mode=ParameterName.loss_data, scale=common_scale,
        bottom_left_offset=target_center_of_loss_diagram_1 - center_of_loss_distribution_diagram)
    constructed_obj_list.append(loss_diagram_1)

    chevron_arrow1_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(right_main_vertical_axis, target_center_of_initial_diagram.y - 0.075),
        ParameterName.head: Vector(right_main_vertical_axis, target_center_of_loss_diagram_1.y + 0.07),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow1_config))

    left_text_3_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.selection_best,
        ParameterName.center: Vector(left_text_vertical_axis, horizontal_axis_3 + 0.01)
    }
    text_obj_list.append(TextBox(**left_text_3_config_dict))
    target_center_of_loss_diagram_2 = Vector(right_main_vertical_axis, horizontal_axis_3)
    loss_diagram_2 = HorizontalLossDistributionDiagram(
        selected=True, mode=ParameterName.loss_data, scale=common_scale,
        bottom_left_offset=target_center_of_loss_diagram_2 - center_of_loss_distribution_diagram)
    constructed_obj_list.append(loss_diagram_2)

    chevron_arrow2_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(right_main_vertical_axis, target_center_of_loss_diagram_1.y - 0.065),
        ParameterName.head: Vector(right_main_vertical_axis, target_center_of_loss_diagram_2.y + 0.07),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow2_config))

    main_text_4_config_dict = {
        **ProtocolDiagramConfig.upper_text_common_config_dict,
        ParameterName.string: common_title_text.final_result,
        ParameterName.center: Vector(right_main_vertical_axis, horizontal_axis_4)
    }
    text_obj_list.append(TextBox(**main_text_4_config_dict))

    chevron_arrow3_config = {
        **ProtocolDiagramConfig.chevron_config,
        ParameterName.tail_end_center: Vector(right_main_vertical_axis, target_center_of_loss_diagram_2.y - 0.065),
        ParameterName.head: Vector(right_main_vertical_axis, horizontal_axis_4 + 0.03),
    }
    chevron_arrow_obj_list.append(ChevronArrow(**chevron_arrow3_config))

    return text_obj_list, chevron_arrow_obj_list, constructed_obj_list
