from ..config import np, DataName, Vector, ColorConfig, ZOrderConfig, CommonFigureString, CommonElementConfig, \
    DataSensitivityMetabolicNetworkConfig, MetaboliteConfig, ReactionConfig, SensitivityConfig, \
    ParameterName, FontWeight, HorizontalAlignment, VerticalAlignment, numbered_even_sequence, \
    ChevronArrow, RoundRectangle

from .common_functions import arrange_text_by_row


def metabolic_sensitivity_network_layout_generator(
        metabolite_list, reaction_list, text_config_list, mode=DataName.merge_reversible_reaction):
    def plot_metabolite_with_reversible_reaction(
            x_loc, top_metabolite_y_loc, metabolite_distance, target_metabolite_list,
            target_reaction_tuple_list, reaction_string_tuple_list):
        y_loc_list = [top_metabolite_y_loc - metabolite_distance * i for i, _ in enumerate(target_metabolite_list)]
        for target_y_loc, target_metabolite_obj in zip(y_loc_list, target_metabolite_list):
            target_metabolite_obj.set_center(Vector(x_loc, target_y_loc))
        reaction_y_loc_list = [
            (y_loc + y_loc_list[y_loc_index + 1]) / 2 for y_loc_index, y_loc in enumerate(y_loc_list[:-1])]
        for reaction_y_loc, target_reaction_tuple, reaction_string_tuple in zip(
                reaction_y_loc_list, target_reaction_tuple_list, reaction_string_tuple_list):
            if len(target_reaction_tuple) == 1:
                target_reaction_obj = target_reaction_tuple[0]
                reaction_string = reaction_string_tuple[0]
                target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(x_loc, reaction_y_loc + reversible_reaction_tail_offset),
                    Vector(x_loc, reaction_y_loc - reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **left_text_config,
                    ParameterName.string: reaction_string,
                    ParameterName.center: Vector(x_loc - reaction_text_distance, reaction_y_loc)
                })
            elif len(target_reaction_tuple) == 2:
                forward_target_reaction_obj, backward_target_reaction_obj = target_reaction_tuple
                forward_reaction_string, backward_reaction_string = reaction_string_tuple
                forward_reaction_x_loc = x_loc - reversible_reaction_distance / 2
                backward_reaction_x_loc = x_loc + reversible_reaction_distance / 2
                forward_target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(forward_reaction_x_loc, reaction_y_loc + reversible_reaction_tail_offset),
                    Vector(forward_reaction_x_loc, reaction_y_loc - reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **left_text_config,
                    ParameterName.string: forward_reaction_string,
                    ParameterName.center: Vector(forward_reaction_x_loc - reaction_text_distance, reaction_y_loc)
                })
                backward_target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(backward_reaction_x_loc, reaction_y_loc - reversible_reaction_tail_offset),
                    Vector(backward_reaction_x_loc, reaction_y_loc + reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **right_text_config,
                    ParameterName.string: backward_reaction_string,
                    ParameterName.center: Vector(backward_reaction_x_loc + reaction_text_distance, reaction_y_loc)
                })
            else:
                raise ValueError()

    chevron_config_list = []
    # common_left_vert_axis = 0.15
    # common_right_vert_axis = 0.35
    # common_middle_vert_axis = 0.25
    common_left_vert_axis = 0.1
    common_right_vert_axis = 0.3
    common_middle_vert_axis = 0.2
    reversible_reaction_distance = 0.013
    reversible_reaction_tail_offset = 0.022
    reversible_reaction_head_offset = 0.024
    reaction_text_distance = 0.035
    common_metabolite_distance = 0.08
    right_document_str = None
    right1_document_str = None
    right2_document_str = None
    right1_vert_axis = None
    right2_vert_axis = None
    upper2_horiz_axis = None
    left_branch_vert_axis = None
    right1_branch_vert_axis = None
    if mode == DataName.merge_reversible_reaction:
        total_width = 0.4
        total_height = 0.35
        left_vert_axis = common_left_vert_axis
        right_vert_axis = common_right_vert_axis
        middle_vert_axis = common_middle_vert_axis
        main_horiz_axis = 0.1
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance / 2
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance / 2
        left_upper_text_horiz_axis = upper_horiz_axis + 0.045
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.035
        title_axis = total_height - 0.04
        # title_str = 'Merge reversible reactions'
        title_str = CommonFigureString.merge_reversible_reactions_with_order_prefix
        left_document_str = 'Reversible reactions\n(Suppose $v_F>v_R$)'
        right_document_str = 'Unidirectional reactions\n$v=v_F-v_R>0$'
    elif mode == DataName.combine_consecutive_reactions:
        total_width = 0.4
        # total_height = 0.33
        total_height = 0.35
        left_vert_axis = common_left_vert_axis
        right_vert_axis = common_right_vert_axis
        middle_vert_axis = common_middle_vert_axis
        main_horiz_axis = 0.11
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance / 2
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance / 2
        upper2_horiz_axis = main_horiz_axis + common_metabolite_distance
        bottom2_horiz_axis = main_horiz_axis - common_metabolite_distance
        left_upper_text_horiz_axis = upper2_horiz_axis + 0.045
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.035
        # title_axis = total_height - 0.02
        title_axis = total_height - 0.04
        # title_str = 'Combine consecutive reactions'
        title_str = CommonFigureString.combine_consecutive_reactions_with_order_prefix
        left_document_str = 'Consecutive reactions\n(Suppose $v_{F1}>v_{R1}$)'
        right_document_str = 'One reaction\n$v_{F1}-v_{R1}=v_F-v_R>0$'
    elif mode == DataName.prune_branches:
        total_width = 0.7
        total_height = 0.35
        branch_main_axis_distance = 0.12
        left_vert_axis = 0.1
        left_branch_vert_axis = left_vert_axis + branch_main_axis_distance
        middle_vert_axis = 0.3
        right1_vert_axis = 0.4
        right1_branch_vert_axis = right1_vert_axis + branch_main_axis_distance
        right2_vert_axis = 0.6
        right_vert_axis = 0.52
        main_horiz_axis = 0.12
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance
        left_upper_text_horiz_axis = upper_horiz_axis + 0.04
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.03
        title_axis = total_height - 0.04
        # title_str = 'Miss branch pathways'
        title_str = CommonFigureString.miss_branch_pathways_with_order_prefix
        left_document_str = 'With branch pathway'
        right1_document_str = 'Replace to biomass flux'
        right2_document_str = 'Completely remove'
    else:
        raise ValueError()

    reaction_text_common_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.width: 0.05,
        ParameterName.font_size: MetaboliteConfig.font_size + 3,
        # ParameterName.text_box: True
    }
    left_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.right,
    }
    right_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    document_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size,
        ParameterName.width: 0.15,
        ParameterName.height: 0.04,
        # ParameterName.text_box: True
    }
    document_title_text_config = {
        **document_text_config,
        ParameterName.width: 0.15,
        ParameterName.height: 0.02,
        ParameterName.font_weight: FontWeight.bold,
        # ParameterName.text_box: True
    }
    title_text_config = {
        **SensitivityConfig.title_text_config,
        ParameterName.width: total_width,
        ParameterName.height: 0.03,
    }
    chevron_len = 0.07
    normal_chevron_width = CommonElementConfig.normal_chevron_width
    chevron_middle_x_loc = middle_vert_axis + 0.01
    chevron_config_list.append({
        **CommonElementConfig.chevron_config,
        ParameterName.width: normal_chevron_width - 0.015,
        ParameterName.name: 'chevron',
        ParameterName.tail_end_center: Vector(chevron_middle_x_loc - chevron_len / 2, main_horiz_axis),
        ParameterName.head: Vector(chevron_middle_x_loc + chevron_len / 2, main_horiz_axis),
    })
    text_config_list.extend([
        {
            **title_text_config,
            ParameterName.name: 'title',
            ParameterName.string: title_str,
            ParameterName.center: Vector(total_width / 2, title_axis)
        },
        {
            **document_title_text_config,
            ParameterName.name: 'left_document_title',
            ParameterName.string: 'Raw network',
            ParameterName.center: Vector(left_vert_axis, document_title_axis)
        },
        {
            **document_title_text_config,
            ParameterName.name: 'right_document_title',
            ParameterName.string: 'Modified network',
            ParameterName.center: Vector(right_vert_axis, document_title_axis)
        },
        {
            **document_text_config,
            ParameterName.name: 'left_document',
            ParameterName.string: left_document_str,
            ParameterName.center: Vector(left_vert_axis, left_upper_text_horiz_axis)
        }

    ])
    if mode == DataName.merge_reversible_reaction or mode == DataName.combine_consecutive_reactions:
        text_config_list.append({
            **document_text_config,
            ParameterName.name: 'right_document',
            ParameterName.string: right_document_str,
            ParameterName.center: Vector(right_vert_axis, right_upper_text_horiz_axis)
        })
        if mode == DataName.merge_reversible_reaction:
            left_target_metabolite_list = [metabolite_list.obj_example_a1, metabolite_list.obj_example_b1]
            left_target_reaction_tuple_list = [(reaction_list.obj_example_abf1, reaction_list.obj_example_abr1)]
            left_reaction_string_tuple_list = [('$v_F$', '$v_R$')]
            left_upper_horiz_axis = upper_horiz_axis

            right_target_reaction_tuple_list = [(reaction_list.obj_example_abf2,)]
            right_reaction_string_tuple_list = [('$v$',)]
        elif mode == DataName.combine_consecutive_reactions:
            left_target_metabolite_list = [
                metabolite_list.obj_example_a1, metabolite_list.obj_example_b1, metabolite_list.obj_example_c1]
            left_target_reaction_tuple_list = [
                (reaction_list.obj_example_abf1, reaction_list.obj_example_abr1),
                (reaction_list.obj_example_bcf1, reaction_list.obj_example_bcr1),
            ]
            left_reaction_string_tuple_list = [('$v_{F1}$', '$v_{R1}$'), ('$v_{F2}$', '$v_{R2}$')]
            left_upper_horiz_axis = upper2_horiz_axis

            right_target_reaction_tuple_list = [(reaction_list.obj_example_abf2, reaction_list.obj_example_abr2)]
            right_reaction_string_tuple_list = [('$v_F$', '$v_R$')]
        else:
            raise ValueError()
        plot_metabolite_with_reversible_reaction(
            left_vert_axis, left_upper_horiz_axis, common_metabolite_distance,
            left_target_metabolite_list,
            left_target_reaction_tuple_list, left_reaction_string_tuple_list)
        plot_metabolite_with_reversible_reaction(
            right_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a2, metabolite_list.obj_example_b2],
            right_target_reaction_tuple_list, right_reaction_string_tuple_list)
    elif mode == DataName.prune_branches:
        text_config_list.extend([
            {
                **document_text_config,
                ParameterName.name: 'right_document1',
                ParameterName.string: right1_document_str,
                ParameterName.center: Vector(right1_vert_axis, right_upper_text_horiz_axis)
            },
            {
                **document_text_config,
                ParameterName.name: 'right_document2',
                ParameterName.string: right2_document_str,
                ParameterName.center: Vector(right2_vert_axis, right_upper_text_horiz_axis)
            },
        ])
        plot_metabolite_with_reversible_reaction(
            left_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a1, metabolite_list.obj_example_b1, metabolite_list.obj_example_c1],
            [
                (reaction_list.obj_example_abf1, reaction_list.obj_example_abr1),
                (reaction_list.obj_example_bcf1, reaction_list.obj_example_bcr1),
            ],
            [('$v_{F1}$', '$v_{R1}$'), ('$v_{F2}$', '$v_{R2}$')]
        )
        plot_metabolite_with_reversible_reaction(
            right1_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a2, metabolite_list.obj_example_b2, metabolite_list.obj_example_c2],
            [
                (reaction_list.obj_example_abf2, reaction_list.obj_example_abr2),
                (reaction_list.obj_example_bcf2, reaction_list.obj_example_bcr2),
            ],
            [('$v_{F3}$', '$v_{R3}$'), ('$v_{F4}$', '$v_{R4}$')]
        )
        plot_metabolite_with_reversible_reaction(
            right2_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a3, metabolite_list.obj_example_b3, metabolite_list.obj_example_c3],
            [
                (reaction_list.obj_example_abf3, reaction_list.obj_example_abr3),
                (reaction_list.obj_example_bcf3, reaction_list.obj_example_bcr3),
            ],
            [('$v_{F3}$', '$v_{R3}$'), ('$v_{F4}$', '$v_{R4}$')]
        )
        metabolite_list.obj_example_d1.set_center(Vector(left_branch_vert_axis, main_horiz_axis))
        left_branch_reaction_text_center_x_loc = (left_vert_axis + left_branch_vert_axis) / 2
        reaction_bd_to_metabolite_distance = 0.04
        reaction_bd_text_loc = main_horiz_axis + 0.02
        reaction_list.obj_example_bd1.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(left_vert_axis + reaction_bd_to_metabolite_distance, main_horiz_axis),
            Vector(left_branch_vert_axis - reaction_bd_to_metabolite_distance, main_horiz_axis), {})]
        ).set_display_text_config_dict({
            **reaction_text_common_config,
            ParameterName.string: '$v_b$',
            ParameterName.center: Vector(left_branch_reaction_text_center_x_loc, reaction_bd_text_loc)
        })
        biomass_reaction_y_loc = (main_horiz_axis + bottom_horiz_axis) / 2
        reaction_list.obj_example_bb.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(left_branch_vert_axis, biomass_reaction_y_loc + reversible_reaction_tail_offset),
            Vector(left_branch_vert_axis, biomass_reaction_y_loc - reversible_reaction_tail_offset), {})]
        ).set_display_text_config_dict({
            **document_text_config,
            **right_text_config,
            ParameterName.string: 'Biomass',
            ParameterName.center: Vector(left_branch_vert_axis + reaction_text_distance + 0.05, biomass_reaction_y_loc)
        })

        right1_branch_reaction_text_center_x_loc = (right1_vert_axis + right1_branch_vert_axis) / 2 + 0.01
        reaction_list.obj_example_bd2.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(right1_vert_axis + reaction_bd_to_metabolite_distance, main_horiz_axis),
            Vector(right1_branch_vert_axis - reaction_bd_to_metabolite_distance + 0.02, main_horiz_axis), {})]
        ).set_display_text_config_dict({
            **document_text_config,
            ParameterName.string: 'Biomass $v_b$',
            ParameterName.center: Vector(right1_branch_reaction_text_center_x_loc + 0.01, reaction_bd_text_loc - 0.002)
        })
        text_config_list.append({
            **title_text_config,
            ParameterName.name: 'or',
            ParameterName.string: 'or',
            ParameterName.center: Vector(right_vert_axis + 0.01, main_horiz_axis)
        })
    else:
        raise ValueError()

    total_size = Vector(total_width, total_height)
    chevron_obj_list = [ChevronArrow(**chevron_config) for chevron_config in chevron_config_list]
    return total_size, chevron_obj_list


def data_availability_sensitivity_layout_generator(mode, current_title, result_label_name_dict):
    if mode == DataName.smaller_data_size:
        total_width = 0.75
        total_height = 0.29
    elif mode == DataName.data_without_pathway:
        total_width = 0.3
        total_height = 0.44
    elif mode == DataName.compartmental_data:
        total_width = 0.51
        total_height = 0.44
    else:
        raise ValueError()

    title_height = 0.05
    body_height = total_height - title_height

    data_rectangle_text_margin = 0.025
    data_rectangle_overlap_area_margin = 0.01

    round_rectangle_config_list = []
    text_config_list = [
        {
            **SensitivityConfig.title_text_config,
            ParameterName.name: ParameterName.figure_title,
            ParameterName.string: current_title,
            ParameterName.font_size: MetaboliteConfig.font_size + 4,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, body_height + title_height / 2)
        }
    ]

    text_width = 0.1
    common_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size - 1,
        ParameterName.height: 0.05,
        ParameterName.width: text_width,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    }
    normal_text_config = {
        **common_text_config,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    title_config = {
        **common_text_config,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: MetaboliteConfig.font_size + 1,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    common_round_rectangle_config_dict = CommonElementConfig.simulated_background_config_dict
    distance_inside_each_group = 0.025

    if mode == DataName.smaller_data_size:
        title_x_location = 0.11
        text_item_left = 0.22
        text_item_right = total_width
        distance_inside_each_group = 0.025
        distance_between_group = 0.07
        raw_data_center_bottom_y = data_rectangle_overlap_area_margin + data_rectangle_text_margin
        text_left_offset = 0
        raw_data_center_y_value = [
            raw_data_center_bottom_y + distance_inside_each_group, raw_data_center_bottom_y]
        medium_data_center_bottom_y = raw_data_center_bottom_y + distance_between_group
        medium_data_center_y_value = [
            medium_data_center_bottom_y + distance_inside_each_group, medium_data_center_bottom_y]
        few_data_center_bottom_y = medium_data_center_bottom_y + distance_between_group
        few_data_center_y_value = [few_data_center_bottom_y + distance_inside_each_group, few_data_center_bottom_y]
        few_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.3,
        }
        medium_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.2,
        }
        raw_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.dark_light_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        text_top_location = few_data_center_y_value[0] + data_rectangle_text_margin
        # few_data_rectangle_pair = [
        #     Vector(title_x_location - 0.08, text_item_right - 0.025),
        #     Vector(few_data_center_y_value[1] - data_rectangle_text_margin, text_top_location),
        # ]  # [(left, right), (bottom, top)]
        expand_width_vector = Vector(-data_rectangle_overlap_area_margin, data_rectangle_overlap_area_margin)
        raw_data_rectangle_left_right_pair = Vector(
            data_rectangle_overlap_area_margin, total_width - data_rectangle_overlap_area_margin)
        medium_data_rectangle_left_right_pair = raw_data_rectangle_left_right_pair - expand_width_vector
        few_data_rectangle_left_right_pair = medium_data_rectangle_left_right_pair - expand_width_vector
        few_data_rectangle_pair = [
            # Vector(title_x_location - 0.08, text_item_right - 0.025),
            few_data_rectangle_left_right_pair,
            Vector(few_data_center_y_value[1] - data_rectangle_text_margin, text_top_location),
        ]  # [(left, right), (bottom, top)]
        few_data_string_list = DataSensitivityMetabolicNetworkConfig.few_data_list
        few_data_title_center = Vector(title_x_location, float(np.mean(few_data_center_y_value)))
        medium_data_rectangle_pair = [
            # few_data_rectangle_pair[0] + expand_width_vector,
            medium_data_rectangle_left_right_pair,
            Vector(
                medium_data_center_y_value[1] - data_rectangle_text_margin,
                text_top_location + data_rectangle_overlap_area_margin),
        ]
        medium_data_string_list = DataSensitivityMetabolicNetworkConfig.medium_data_list
        medium_data_title_center = Vector(title_x_location, float(np.mean(medium_data_center_y_value)))
        raw_data_rectangle_pair = [
            # medium_data_rectangle_pair[0] + expand_width_vector,
            raw_data_rectangle_left_right_pair,
            Vector(
                raw_data_center_y_value[1] - data_rectangle_text_margin,
                text_top_location + 2 * data_rectangle_overlap_area_margin),
        ]
        raw_data_string_list = DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list
        raw_data_title_center = Vector(title_x_location, float(np.mean(raw_data_center_y_value)))
        left_right_x_range = Vector(text_item_left, text_item_right)

        flux_range_string_dict = {
            DataName.few_data: (
                result_label_name_dict[DataName.few_data],
                left_right_x_range,
                few_data_title_center,
                few_data_center_y_value,
                few_data_string_list,
                few_data_rectangle_pair,
                few_data_rectangle_config,
            ),
            DataName.medium_data: (
                result_label_name_dict[DataName.medium_data],
                left_right_x_range,
                medium_data_title_center,
                medium_data_center_y_value,
                medium_data_string_list,
                medium_data_rectangle_pair,
                medium_data_rectangle_config,
            ),
            DataName.raw_data_result_label: (
                CommonFigureString.experimental_available_mid_data_wrap,
                left_right_x_range,
                raw_data_title_center,
                raw_data_center_y_value,
                raw_data_string_list,
                raw_data_rectangle_pair,
                raw_data_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.data_without_pathway:
        distance_between_group = 0.06
        # bottom_panel_bottom_y = 0.05
        bottom_panel_bottom_y = 0.03
        ppp_removed_str_list = DataSensitivityMetabolicNetworkConfig.ppp_removed_list
        aa_removed_str_list = DataSensitivityMetabolicNetworkConfig.aa_removed_list
        tca_removed_str_list = DataSensitivityMetabolicNetworkConfig.tca_removed_list
        other_metabolite_str_list = DataSensitivityMetabolicNetworkConfig.other_metabolite_list
        data_without_aa_center_y_value = numbered_even_sequence(
            bottom_panel_bottom_y, distance_inside_each_group, len(aa_removed_str_list) + 1)[::-1]
        data_without_tca_center_y_value = numbered_even_sequence(
            bottom_panel_bottom_y, distance_inside_each_group, len(tca_removed_str_list) + 1)[::-1]
        # data_without_ppp_center_y_value = [0.4, 0.35, 0.3]
        data_without_ppp_center_y_value = numbered_even_sequence(
            data_without_aa_center_y_value[0] + distance_between_group, distance_inside_each_group,
            len(ppp_removed_str_list) + 1)[::-1]
        other_metabolite_data_center_y_value = numbered_even_sequence(
            data_without_tca_center_y_value[0] + distance_between_group, distance_inside_each_group,
            len(other_metabolite_str_list) + 1)[::-1]
        left_panel_width = 0.14
        right_panel_width = 0.13
        left_panel_left_right_x_value = Vector(
            data_rectangle_overlap_area_margin, data_rectangle_overlap_area_margin + left_panel_width)
        right_panel_left_right_x_value = Vector(
            total_width - data_rectangle_overlap_area_margin - right_panel_width,
            total_width - data_rectangle_overlap_area_margin)
        text_left_offset = 0.02
        medium_data_without_combination_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        compartmental_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        all_data_result_label_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        bottom_rectangle_common_bottom = data_rectangle_overlap_area_margin

        data_without_ppp_rectangle_pair = [
            right_panel_left_right_x_value,
            Vector(
                data_without_ppp_center_y_value[-1] - data_rectangle_text_margin,
                data_without_ppp_center_y_value[0] + data_rectangle_text_margin),
        ]  # [(left, right), (bottom, top)]
        data_without_aa_rectangle_pair = [
            right_panel_left_right_x_value,
            Vector(
                bottom_rectangle_common_bottom,
                data_without_aa_center_y_value[0] + data_rectangle_text_margin),
        ]
        data_without_tca_rectangle_pair = [
            left_panel_left_right_x_value,
            Vector(
                bottom_rectangle_common_bottom,
                data_without_tca_center_y_value[0] + data_rectangle_text_margin),
        ]
        left_panel_center_x = float(np.mean(left_panel_left_right_x_value))
        right_panel_center_x = float(np.mean(right_panel_left_right_x_value))

        flux_range_string_dict = {
            DataName.data_without_ppp: (
                result_label_name_dict[DataName.data_without_ppp],
                right_panel_left_right_x_value,
                Vector(right_panel_center_x, data_without_ppp_center_y_value[0]),
                data_without_ppp_center_y_value[1:],
                DataSensitivityMetabolicNetworkConfig.ppp_removed_list,
                data_without_ppp_rectangle_pair,
                medium_data_without_combination_rectangle_config,
            ),
            DataName.data_without_aa: (
                result_label_name_dict[DataName.data_without_aa],
                right_panel_left_right_x_value,
                Vector(right_panel_center_x, data_without_aa_center_y_value[0]),
                data_without_aa_center_y_value[1:],
                aa_removed_str_list,
                data_without_aa_rectangle_pair,
                compartmental_data_rectangle_config,
            ),
            'other_metabolite_list': (
                CommonFigureString.other_metabolite_list,
                left_panel_left_right_x_value,
                Vector(left_panel_center_x, other_metabolite_data_center_y_value[0]),
                other_metabolite_data_center_y_value[1:],
                other_metabolite_str_list,
                None,
                {},
            ),
            DataName.data_without_tca: (
                result_label_name_dict[DataName.data_without_tca],
                left_panel_left_right_x_value,
                Vector(left_panel_center_x, data_without_tca_center_y_value[0]),
                data_without_tca_center_y_value[1:],
                DataSensitivityMetabolicNetworkConfig.tca_removed_list,
                data_without_tca_rectangle_pair,
                all_data_result_label_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.compartmental_data:
        total_row_num = len(
            DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_without_compartments)
        all_available_row_num = len(
            DataSensitivityMetabolicNetworkConfig.all_available_data_list_with_compartments)
        title_distance = 0.045
        text_bottom = 0.03
        text_top = total_height - title_height - 0.02
        # common_y_array = np.linspace(text_top, text_bottom, total_row_num + 2)
        common_y_array = numbered_even_sequence(text_bottom, distance_inside_each_group, total_row_num)[::-1]
        # left_x_range = Vector(0.02, 0.12)
        left_panel_width = 0.14
        left_panel_left = data_rectangle_overlap_area_margin
        left_x_range = Vector(left_panel_left, left_panel_left + left_panel_width)
        mid_panel_left = left_x_range[1] + 0.02
        mid_panel_width = 0.15
        # mid_x_range = Vector(0.15, 0.25)
        mid_x_range = Vector(mid_panel_left, mid_panel_left + mid_panel_width)
        # right_x_range = Vector(0.25, 0.32)
        right_panel_left = mid_x_range[1] - 0.01
        right_x_range = Vector(right_panel_left, total_width - data_rectangle_overlap_area_margin)
        title_y_location = common_y_array[0] + title_distance
        all_data_y_array = common_y_array[1:all_available_row_num + 1]
        other_data_y_array = common_y_array
        text_left_offset = 0.02
        medium_data_without_combination_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        compartmental_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        all_data_result_label_rectangle_config = {
            ParameterName.face_color: ColorConfig.dark_light_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        rectangle_minimal_bottom = data_rectangle_overlap_area_margin
        inner_rectangle_bottom_top = Vector(
            rectangle_minimal_bottom + data_rectangle_overlap_area_margin,
            title_y_location + data_rectangle_text_margin + 0.005)
        outer_rectangle_bottom_top = inner_rectangle_bottom_top + Vector(-1, 1) * data_rectangle_overlap_area_margin
        # common_rectangle_bottom_top = Vector(
        #     text_bottom - data_rectangle_text_margin, text_top + data_rectangle_text_margin)
        medium_data_without_combination_rectangle_pair = [
            left_x_range, outer_rectangle_bottom_top, ]  # [(left, right), (bottom, top)]
        compartmental_data_rectangle_pair = [
            mid_x_range, inner_rectangle_bottom_top, ]
        all_data_result_rectangle_pair = [
            Vector(mid_panel_left - data_rectangle_overlap_area_margin, right_x_range[1]),
            outer_rectangle_bottom_top, ]

        flux_range_string_dict = {
            DataName.medium_data_without_combination: (
                CommonFigureString.experimental_available_mid_data_double_wrap,
                left_x_range,
                Vector(float(np.mean(left_x_range)), title_y_location),
                other_data_y_array,
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_without_compartments,
                medium_data_without_combination_rectangle_pair,
                medium_data_without_combination_rectangle_config,
            ),
            DataName.compartmental_data: (
                CommonFigureString.compartmental_data_wrap,
                mid_x_range,
                Vector(float(np.mean(mid_x_range)), title_y_location),
                other_data_y_array,
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_with_compartments,
                compartmental_data_rectangle_pair,
                compartmental_data_rectangle_config,
            ),
            DataName.all_data_result_label: (
                CommonFigureString.all_available_compartmental_data_double_wrap,
                right_x_range,
                Vector(float(np.mean(right_x_range)), title_y_location),
                all_data_y_array,
                DataSensitivityMetabolicNetworkConfig.all_available_data_list_with_compartments,
                all_data_result_rectangle_pair,
                all_data_result_label_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)
    else:
        raise ValueError()
    round_rectangle_obj_list = [
        RoundRectangle(**round_rectangle_config) for round_rectangle_config in round_rectangle_config_list
    ]
    return text_config_list, round_rectangle_obj_list, total_width, total_height


def config_sensitivity_layout_generator(mode, current_title, result_label_name_dict):
    if mode == DataName.different_constant_flux:
        total_width = 0.35
        total_height = 0.2
    elif mode == DataName.different_flux_range:
        total_width = 0.35
        total_height = 0.2
    else:
        raise ValueError()

    title_height = 0.05
    body_height = total_height - title_height

    data_rectangle_text_margin = 0.025
    data_rectangle_overlap_area_margin = 0.01

    round_rectangle_config_list = []
    text_config_list = [
        {
            **SensitivityConfig.title_text_config,
            ParameterName.name: ParameterName.figure_title,
            ParameterName.string: current_title,
            ParameterName.font_size: MetaboliteConfig.font_size + 4,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, body_height + title_height / 2)
        }
    ]

    text_width = 0.1
    common_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size - 1,
        ParameterName.height: 0.05,
        ParameterName.width: text_width,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    }
    normal_text_config = {
        **common_text_config,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    title_config = {
        **common_text_config,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: MetaboliteConfig.font_size + 1,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    common_round_rectangle_config_dict = CommonElementConfig.simulated_background_config_dict
    distance_inside_each_group = 0.025

    if mode == DataName.different_constant_flux:
        distance_between_group = 0.06
        bottom_y = 0.03
        distance_inside_each_group = 0.025
        text_left_offset = 0.05

        constant_flux_string_list = DataSensitivityMetabolicNetworkConfig.different_constant_flux_string_list
        constant_flux_center_y_value = numbered_even_sequence(
            bottom_y, distance_inside_each_group, len(constant_flux_string_list))[::-1]
        panel_x_range = Vector(
            data_rectangle_overlap_area_margin, total_width - data_rectangle_overlap_area_margin)

        flux_range_string_dict = {
            DataName.different_constant_flux: (
                None,
                panel_x_range,
                None,
                constant_flux_center_y_value,
                constant_flux_string_list,
                None,
                {},
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.different_flux_range:
        distance_between_group = 0.06
        bottom_panel_bottom_y = 0.03
        flux_lower_bound_string_list = DataSensitivityMetabolicNetworkConfig.flux_lower_bound_string_list
        flux_upper_bound_string_list = DataSensitivityMetabolicNetworkConfig.flux_upper_bound_string_list
        lower_upper_bound_center_y_value = numbered_even_sequence(
            bottom_panel_bottom_y, distance_inside_each_group, len(flux_lower_bound_string_list) + 1)[::-1]
        panel_width = (total_width - 3 * data_rectangle_overlap_area_margin) / 2
        left_panel_start = data_rectangle_overlap_area_margin
        right_panel_end = total_width - data_rectangle_overlap_area_margin
        left_panel_left_right_x_value = Vector(left_panel_start, left_panel_start + panel_width)
        right_panel_left_right_x_value = Vector(right_panel_end - panel_width, right_panel_end)
        text_left_offset = 0.02
        lower_upper_bound_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        rectangle_common_bottom = data_rectangle_overlap_area_margin

        rectangle_bottom_top_pair = Vector(
            rectangle_common_bottom, lower_upper_bound_center_y_value[0] + data_rectangle_text_margin)
        left_panel_rectangle_pair = [
            left_panel_left_right_x_value, rectangle_bottom_top_pair,
        ]  # [(left, right), (bottom, top)]
        right_panel_rectangle_pair = [
            right_panel_left_right_x_value, rectangle_bottom_top_pair]
        left_panel_center_x = float(np.mean(left_panel_left_right_x_value))
        right_panel_center_x = float(np.mean(right_panel_left_right_x_value))

        flux_range_string_dict = {
            'lower_bound': (
                CommonFigureString.lower_bound,
                left_panel_left_right_x_value,
                Vector(left_panel_center_x, lower_upper_bound_center_y_value[0]),
                lower_upper_bound_center_y_value[1:],
                flux_lower_bound_string_list,
                left_panel_rectangle_pair,
                lower_upper_bound_rectangle_config,
            ),
            'upper_bound': (
                CommonFigureString.upper_bound,
                right_panel_left_right_x_value,
                Vector(right_panel_center_x, lower_upper_bound_center_y_value[0]),
                lower_upper_bound_center_y_value[1:],
                flux_upper_bound_string_list,
                right_panel_rectangle_pair,
                lower_upper_bound_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)
    else:
        raise ValueError()
    round_rectangle_obj_list = [
        RoundRectangle(**round_rectangle_config) for round_rectangle_config in round_rectangle_config_list
    ]
    return text_config_list, round_rectangle_obj_list, total_width, total_height