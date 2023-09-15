from ..config import np, Vector, NetworkGeneralConfig, MetaboliteConfig, ReactionConfig, ParameterName, \
    HorizontalAlignment, VerticalAlignment

from .common_functions import add_straight_reaction_between_metabolites, cycle_layout, \
    calculate_reaction_between_adjacent_metabolites


metabolite_height = MetaboliteConfig.height
metabolite_width = MetaboliteConfig.width

reaction_stem_width = ReactionConfig.stem_width

display_text_vertical_distance = ReactionConfig.display_text_vertical_distance
display_text_horizontal_distance = ReactionConfig.display_text_horizontal_distance
display_text_half_height = ReactionConfig.display_text_height / 2
display_text_half_width = ReactionConfig.display_text_width / 2


def network_layout_generator(metabolite_list, reaction_list, subnetwork_list, other_text_list, infusion=False):
    main_vertical_axis_x_value = 0.36  # Glycolysis
    right_most_vertical_axis_x_value = 0.95  # Input metabolites
    right_1_vertical_axis_x_value = 0.5
    right_2_vertical_axis_x_value = 0.59
    right_3_vertical_axis_x_value = 0.73
    right_4_vertical_axis_x_value = 0.85
    left_1_vertical_axis_x_value = 0.22
    left_2_vertical_axis_x_value = 0.175
    left_most_vertical_axis_x_value = 0.05
    mitochondria_subnetwork_left = left_2_vertical_axis_x_value - 0.05
    cell_subnetwork_left = mitochondria_subnetwork_left - 0.02

    mitochondria_subnetwork_right = (right_2_vertical_axis_x_value + right_3_vertical_axis_x_value) / 2
    cell_subnetwork_right = (right_most_vertical_axis_x_value + right_4_vertical_axis_x_value) / 2
    gap_width = ReactionConfig.reaction_gap
    right_3_vertical_gap_line_pair_list = [(
        np.array([1, 0, -right_3_vertical_axis_x_value + gap_width / 2]),
        np.array([1, 0, -right_3_vertical_axis_x_value - gap_width / 2])
    )]

    cell_subnetwork_top = 0.88
    main_horizontal_axis_y_value = 0.405  # Pyruvate-lactate-alanine
    top_most_horizontal_axis_y_value = 0.8536  # Glucose
    bottom_1_horizontal_axis_y_value = 0.035  # Succinate
    bottom_most_horizontal_axis_y_value = 0.03  # GLN
    mitochondria_subnetwork_bottom = bottom_most_horizontal_axis_y_value - 0.022

    glycolysis_interval = (top_most_horizontal_axis_y_value - main_horizontal_axis_y_value) / 6
    mitochondria_subnetwork_top = main_horizontal_axis_y_value - glycolysis_interval / 2
    cell_subnetwork_bottom = 0
    tca_top_y_value = main_horizontal_axis_y_value - 2.5 * glycolysis_interval
    tca_radius = (tca_top_y_value - bottom_1_horizontal_axis_y_value) / 2
    tca_center_y_value = bottom_1_horizontal_axis_y_value + tca_radius
    tca_theta_list = [135, 45, -17, -90, -163]
    tca_reaction_theta_list = [
        ((115, None), (None, 63)),
        ((30.5, None), (None, -7)),
        ((-28.5, None), (None, -67)),
        ((-114, -113), (-151, -152)),
        ((-174.5, -173.5), (-210.5, -212)),
    ]
    display_text_theta_list = [90, 15, -55, -125, -195]
    display_text_radius_ratio_list = [0.85, 0.7, 0.75, 0.75, 0.7]

    glycolysis_metabolite_main_axis_list = [
        metabolite_list.obj_glc_c,
        metabolite_list.obj_g6p_c,
        metabolite_list.obj_fbp_c,
        metabolite_list.obj_gap_c,
        metabolite_list.obj_3pg_c,
        metabolite_list.obj_pep_c,
        metabolite_list.obj_pyr_c,
        metabolite_list.obj_pyr_m,
        metabolite_list.obj_accoa_m,
    ]

    glycolysis_reaction_main_axis_list = [
        reaction_list.obj_hex_c,
        reaction_list.obj_pgi_pfk_c,
        reaction_list.obj_fba_c,
        reaction_list.obj_gapd_pgk_c,
        reaction_list.obj_pgm_eno_c,
        reaction_list.obj_pyk_c,
        reaction_list.obj_pyr_trans,
        reaction_list.obj_pdh_m,
    ]

    last_y_location = 0
    for metabolite_index, metabolite_obj in enumerate(glycolysis_metabolite_main_axis_list):
        current_y_location = top_most_horizontal_axis_y_value - metabolite_index * glycolysis_interval
        metabolite_obj.set_center(Vector(main_vertical_axis_x_value, current_y_location))
        if metabolite_index != 0:
            reaction_obj = glycolysis_reaction_main_axis_list[metabolite_index - 1]
            add_straight_reaction_between_metabolites(
                last_y_location, current_y_location, ParameterName.vertical, main_vertical_axis_x_value, reaction_obj)
            display_text_x_value = main_vertical_axis_x_value - display_text_horizontal_distance - \
                display_text_half_width
            display_text_y_value = (last_y_location + current_y_location) / 2
            horizontal_alignment = HorizontalAlignment.right
            if reaction_obj is reaction_list.obj_fba_c:
                display_text_x_value -= 0.03
                display_text_y_value += 0.01
            elif reaction_obj is reaction_list.obj_pdh_m:
                display_text_x_value = main_vertical_axis_x_value + display_text_horizontal_distance + \
                    display_text_half_width
                horizontal_alignment = HorizontalAlignment.left
            reaction_obj.set_display_text_config_dict({
                ParameterName.center: Vector(display_text_x_value, display_text_y_value),
                ParameterName.horizontal_alignment: horizontal_alignment
            })
        last_y_location = current_y_location

    gap_c_y_value = metabolite_list.obj_gap_c.center.y
    metabolite_list.obj_dhap_c.set_center(Vector(left_1_vertical_axis_x_value, gap_c_y_value))
    tpi_c_obj = reaction_list.obj_tpi_c
    main_left_display_text_x_value = (left_1_vertical_axis_x_value + main_vertical_axis_x_value) / 2
    add_straight_reaction_between_metabolites(
        left_1_vertical_axis_x_value, main_vertical_axis_x_value, ParameterName.horizontal, gap_c_y_value,
        reaction_list.obj_tpi_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                main_left_display_text_x_value,
                gap_c_y_value - display_text_vertical_distance - display_text_half_height
            ),
            ParameterName.vertical_alignment: VerticalAlignment.top
        })
    pyr_c_y_value = metabolite_list.obj_pyr_c.center.y
    metabolite_list.obj_lac_c.set_center(Vector(left_1_vertical_axis_x_value, pyr_c_y_value))
    above_pyr_display_text_y_value = (
            pyr_c_y_value + display_text_vertical_distance + display_text_half_height)
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, left_1_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_ldh_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                main_left_display_text_x_value,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    metabolite_list.obj_lac_e.set_center(Vector(left_most_vertical_axis_x_value, pyr_c_y_value))
    left_exchange_flux_display_text_x_value = mitochondria_subnetwork_left + 0.01
    add_straight_reaction_between_metabolites(
        left_1_vertical_axis_x_value, left_most_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_lac_output).set_display_text_config_dict({
            ParameterName.center: Vector(
                left_exchange_flux_display_text_x_value,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    metabolite_list.obj_ala_c.set_center(Vector(right_1_vertical_axis_x_value, pyr_c_y_value))
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, right_1_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_gpt_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                (main_vertical_axis_x_value + right_1_vertical_axis_x_value) / 2,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    obj_fba_c = reaction_list.obj_fba_c
    if obj_fba_c.judge_if_reverse():
        fba_c_start_ratio = 0.55
        fba_c_branch_end_coordinate = Vector(
            metabolite_list.obj_dhap_c.center.x + 0.48 * metabolite_width,
            metabolite_list.obj_dhap_c.center.y + 0.49 * metabolite_height
        )
    else:
        if obj_fba_c.tail_arrow:
            fba_c_start_ratio = 0.45
        else:
            fba_c_start_ratio = 0.35
        fba_c_branch_end_coordinate = Vector(
            metabolite_list.obj_dhap_c.center.x + 0.5 * metabolite_width,
            metabolite_list.obj_dhap_c.center.y + 0.55 * metabolite_height
        )
    obj_fba_c.extend_reaction_start_end_list([
        (
            ParameterName.branch,
            fba_c_start_ratio,
            fba_c_branch_end_coordinate,
            {
                ParameterName.arrow: not obj_fba_c.judge_if_reverse()
            }
        )
    ])

    glc_c_y_value = metabolite_list.obj_glc_c.center.y
    metabolite_list.obj_glc_e.set_center(
        Vector(right_most_vertical_axis_x_value, glc_c_y_value)
    )
    right_exchange_flux_display_text_x_value = right_4_vertical_axis_x_value
    below_glc_display_text_y_value = (
            glc_c_y_value - display_text_vertical_distance - display_text_half_height)
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, main_vertical_axis_x_value, ParameterName.horizontal, glc_c_y_value,
        reaction_list.obj_glc_input).set_display_text_config_dict({
            ParameterName.center: Vector(
                right_exchange_flux_display_text_x_value,
                below_glc_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.top
        })

    if infusion:
        metabolite_list.obj_glc_unlabelled_e.set_center(
            Vector(left_most_vertical_axis_x_value, glc_c_y_value)
        )
        add_straight_reaction_between_metabolites(
            left_most_vertical_axis_x_value, main_vertical_axis_x_value, ParameterName.horizontal, glc_c_y_value,
            reaction_list.obj_glc_unlabelled_input).set_display_text_config_dict({
                ParameterName.center: Vector(
                    left_exchange_flux_display_text_x_value,
                    below_glc_display_text_y_value
                ),
                ParameterName.vertical_alignment: VerticalAlignment.top
            })

    metabolite_list.obj_ala_e.set_center(Vector(right_most_vertical_axis_x_value, pyr_c_y_value))
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, right_1_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_ala_input, {ParameterName.gap_line_pair_list: right_3_vertical_gap_line_pair_list}
    ).set_display_text_config_dict({
            ParameterName.center: Vector(
                right_2_vertical_axis_x_value + 0.01,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    # TCA
    tca_metabolite_cycle_list = [
        metabolite_list.obj_oac_m,
        metabolite_list.obj_cit_m,
        metabolite_list.obj_akg_m,
        metabolite_list.obj_suc_m,
        metabolite_list.obj_mal_m
    ]
    tca_reaction_cycle_list = [
        reaction_list.obj_cs_m,
        reaction_list.obj_acont_icdh_m,
        reaction_list.obj_akgd_sucoas_m,
        reaction_list.obj_sucd_fumh_m,
        reaction_list.obj_mdh_m
    ]
    tca_cycle_center = Vector(main_vertical_axis_x_value, tca_center_y_value)

    cycle_layout(
        tca_cycle_center, tca_radius, tca_metabolite_cycle_list, tca_theta_list,
        tca_reaction_cycle_list, tca_reaction_theta_list, display_text_theta_list, display_text_radius_ratio_list)
    accoa_m_y_value = metabolite_list.obj_accoa_m.center.y
    cs_m_branch_start_ratio = 90
    cs_m_branch_end_coordinate = Vector(
        main_vertical_axis_x_value,
        accoa_m_y_value - metabolite_height / 2 -
        MetaboliteConfig.interval_to_metabolite_ratio[ParameterName.blunt][ParameterName.vertical]
    )
    reaction_list.obj_cs_m.extend_reaction_start_end_list([
        (
            ParameterName.branch,
            cs_m_branch_start_ratio,
            cs_m_branch_end_coordinate,
            {
                ParameterName.arrow: reaction_list.obj_cs_m.judge_if_reverse()
            }
        )
    ])

    # AA

    oac_m_y_value = metabolite_list.obj_oac_m.center.y
    oac_m_x_value = metabolite_list.obj_oac_m.center.x
    pep_c_y_value = metabolite_list.obj_pep_c.center.y
    pyr_m_y_value = metabolite_list.obj_pyr_m.center.y
    metabolite_list.obj_asp_m.set_center(Vector(left_2_vertical_axis_x_value, oac_m_y_value))
    metabolite_list.obj_asp_c.set_center(Vector(right_3_vertical_axis_x_value, gap_c_y_value))
    metabolite_list.obj_oac_c.set_center(Vector(right_3_vertical_axis_x_value, pep_c_y_value))
    metabolite_list.obj_cit_c.set_center(Vector(right_3_vertical_axis_x_value, pyr_m_y_value))
    accoa_c_x_value = 0.3 * right_3_vertical_axis_x_value + 0.7 * right_4_vertical_axis_x_value
    accoa_c_y_value = 0.4 * pep_c_y_value + 0.6 * pyr_c_y_value
    metabolite_list.obj_accoa_c.set_center(Vector(accoa_c_x_value, accoa_c_y_value))
    metabolite_list.obj_mal_c.set_center(Vector(right_4_vertical_axis_x_value, pep_c_y_value))
    metabolite_list.obj_asp_e.set_center(Vector(right_most_vertical_axis_x_value, gap_c_y_value))

    add_straight_reaction_between_metabolites(
        left_2_vertical_axis_x_value, oac_m_x_value, ParameterName.horizontal, oac_m_y_value,
        reaction_list.obj_aspta_m).set_display_text_config_dict({
            ParameterName.center: Vector(
                (left_2_vertical_axis_x_value + oac_m_x_value) / 2,
                oac_m_y_value + display_text_vertical_distance + display_text_half_height,
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    pc_m_radius = (pyr_m_y_value - oac_m_y_value) * 1.3
    pc_m_center = Vector(oac_m_x_value + pc_m_radius - 0.01, oac_m_y_value)
    reaction_list.obj_pc_m.extend_reaction_start_end_list([
        (
            ParameterName.cycle,
            138,
            174,
            pc_m_center,
            pc_m_radius,
            {}
        )
    ]).set_display_text_config_dict({
        ParameterName.center: Vector(
            main_vertical_axis_x_value - 0.11,
            accoa_m_y_value + 0.01,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.right
    })
    above_pep_display_text_y_value = pep_c_y_value + display_text_vertical_distance + display_text_half_height
    add_straight_reaction_between_metabolites(
        right_3_vertical_axis_x_value, main_vertical_axis_x_value, ParameterName.horizontal, pep_c_y_value,
        reaction_list.obj_pepck_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                right_1_vertical_axis_x_value + 0.01,
                above_pep_display_text_y_value,
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })
    add_straight_reaction_between_metabolites(
        right_4_vertical_axis_x_value, right_3_vertical_axis_x_value, ParameterName.horizontal, pep_c_y_value,
        reaction_list.obj_mdh_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                (right_4_vertical_axis_x_value + right_3_vertical_axis_x_value) / 2,
                above_pep_display_text_y_value,
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })
    oac_c_left_display_text_x_value = right_3_vertical_axis_x_value - \
        display_text_horizontal_distance - display_text_half_width
    add_straight_reaction_between_metabolites(
        gap_c_y_value, pep_c_y_value, ParameterName.vertical, right_3_vertical_axis_x_value,
        reaction_list.obj_aspta_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                oac_c_left_display_text_x_value,
                0.35 * gap_c_y_value + 0.65 * pep_c_y_value,
            ),
            ParameterName.horizontal_alignment: HorizontalAlignment.right
        }, config_key='top')
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, right_3_vertical_axis_x_value, ParameterName.horizontal, gap_c_y_value,
        reaction_list.obj_asp_input).set_display_text_config_dict({
            ParameterName.center: Vector(
                right_exchange_flux_display_text_x_value,
                gap_c_y_value + display_text_vertical_distance + display_text_half_height,
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })
    obj_acitl_c = reaction_list.obj_acitl_c
    acitl_c_start_x_location, acitl_c_end_x_location = calculate_reaction_between_adjacent_metabolites(
        pyr_m_y_value, pep_c_y_value, ParameterName.vertical, *obj_acitl_c.judge_bidirectional_flag())
    _, acitl_c_branch_end_x_location = calculate_reaction_between_adjacent_metabolites(
        right_3_vertical_axis_x_value, accoa_c_x_value, ParameterName.horizontal,
        start_arrow=False, end_arrow=not obj_acitl_c.judge_if_reverse())
    obj_acitl_c.extend_reaction_start_end_list([
        (
            ParameterName.normal,
            Vector(right_3_vertical_axis_x_value, acitl_c_start_x_location),
            Vector(right_3_vertical_axis_x_value, acitl_c_end_x_location),
            {}
        ),
        (
            ParameterName.normal,
            Vector(right_3_vertical_axis_x_value + reaction_stem_width / 2, accoa_c_y_value),
            Vector(acitl_c_branch_end_x_location, accoa_c_y_value),
            {}
        )
    ]).set_display_text_config_dict({
        ParameterName.center: Vector(
            oac_c_left_display_text_x_value,
            0.65 * pyr_m_y_value + 0.35 * pep_c_y_value,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.right
    })

    # PPP
    ppp_metabolite_list = [
        metabolite_list.obj_rul5p_c,
        metabolite_list.obj_rib5p_c
    ]
    ppp_reaction_list = [
        reaction_list.obj_g6pdh2r_pgl_gnd_reaction,
        reaction_list.obj_rpi_c]
    g6p_c_y_value = metabolite_list.obj_g6p_c.center.y
    ppp_x_interval = right_1_vertical_axis_x_value - main_vertical_axis_x_value
    ery4p_y_value = (metabolite_list.obj_fbp_c.center.y + gap_c_y_value) / 2
    metabolite_list.obj_ery4p_c.set_center(
        Vector(right_1_vertical_axis_x_value, ery4p_y_value)
    )
    above_g6p_display_text_y_value = g6p_c_y_value + display_text_vertical_distance + display_text_half_height
    last_x_location = main_vertical_axis_x_value
    for metabolite_index, metabolite_obj in enumerate(ppp_metabolite_list):
        current_x_location = right_1_vertical_axis_x_value + ppp_x_interval * metabolite_index
        metabolite_obj.set_center(Vector(current_x_location, g6p_c_y_value))
        reaction_obj = ppp_reaction_list[metabolite_index]
        add_straight_reaction_between_metabolites(
            last_x_location, current_x_location, ParameterName.horizontal, g6p_c_y_value,
            reaction_obj).set_display_text_config_dict({
                ParameterName.center: Vector(
                    (last_x_location + current_x_location) / 2,
                    above_g6p_display_text_y_value,
                ),
                ParameterName.vertical_alignment: VerticalAlignment.baseline
            })
        last_x_location = current_x_location
    rpe_reaction_start_location = Vector(
        right_1_vertical_axis_x_value - 0.4 * metabolite_width,
        metabolite_list.obj_rul5p_c.center.y - 0.6 * metabolite_height
    )
    rpe_reaction_end_location = Vector(
        main_vertical_axis_x_value + 0.5 * metabolite_width,
        metabolite_list.obj_gap_c.center.y + 0.5 * metabolite_height
    )
    rpe_reaction_branch1_end_location = Vector(
        right_1_vertical_axis_x_value - 0.4 * metabolite_width,
        metabolite_list.obj_ery4p_c.center.y + 0.6 * metabolite_height
    )
    rpe_reaction_branch2_end_location = Vector(
        metabolite_list.obj_fbp_c.center.x + 0.5 * metabolite_width + MetaboliteConfig.interval_to_metabolite_ratio[
            ParameterName.arrow][ParameterName.horizontal],
        metabolite_list.obj_fbp_c.center.y
    )
    branch_ratio = 0.5
    reaction_list.obj_rpe_tkt_tala_c.extend_reaction_start_end_list([
        (
            ParameterName.normal,
            rpe_reaction_start_location,
            rpe_reaction_end_location,
            {
                ParameterName.dash_solid_empty_width: ReactionConfig.dash_reaction_solid_gap_ratio
            }
        ),
        (
            ParameterName.branch,
            branch_ratio,
            rpe_reaction_branch1_end_location,
            {
                ParameterName.arrow: True,
                ParameterName.dash: True
            }
        ),
        (
            ParameterName.branch,
            branch_ratio,
            rpe_reaction_branch2_end_location,
            {
                ParameterName.arrow: True,
                ParameterName.dash: True
            }
        )
    ]).set_display_text_config_dict({
        ParameterName.center: Vector(
            metabolite_list.obj_ery4p_c.center.x - 0.01,
            metabolite_list.obj_fbp_c.center.y,
        )
    })

    # Ser-Gly
    obj_3pg_c_y_value = metabolite_list.obj_3pg_c.center.y
    obj_fbp_c_y_value = metabolite_list.obj_fbp_c.center.y
    metabolite_list.obj_ser_c.set_center(Vector(right_2_vertical_axis_x_value, obj_3pg_c_y_value))
    metabolite_list.obj_gly_c.set_center(Vector(right_2_vertical_axis_x_value, obj_fbp_c_y_value))
    metabolite_list.obj_ser_e.set_center(Vector(right_most_vertical_axis_x_value, obj_3pg_c_y_value))
    metabolite_list.obj_gly_e.set_center(Vector(right_most_vertical_axis_x_value, obj_fbp_c_y_value))
    above_3pg_display_text_y_value = obj_3pg_c_y_value + display_text_vertical_distance + display_text_half_height
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal, obj_3pg_c_y_value,
        reaction_list.obj_phgdh_psat_psp_c
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            (main_vertical_axis_x_value + right_2_vertical_axis_x_value) / 2,
            above_3pg_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal, obj_3pg_c_y_value,
        reaction_list.obj_ser_input, {ParameterName.gap_line_pair_list: right_3_vertical_gap_line_pair_list}
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            right_exchange_flux_display_text_x_value,
            above_3pg_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    ser_left_display_text_x_value = right_2_vertical_axis_x_value - \
        display_text_horizontal_distance - display_text_half_width
    add_straight_reaction_between_metabolites(
        obj_3pg_c_y_value, obj_fbp_c_y_value, ParameterName.vertical, right_2_vertical_axis_x_value,
        reaction_list.obj_shmt_c
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            ser_left_display_text_x_value,
            (obj_3pg_c_y_value + obj_fbp_c_y_value) / 2,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.right
    })
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal, obj_fbp_c_y_value,
        reaction_list.obj_gly_input
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            right_exchange_flux_display_text_x_value,
            obj_fbp_c_y_value + display_text_vertical_distance + display_text_half_height,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })

    # GLU
    obj_akg_m_x_value = metabolite_list.obj_akg_m.center.x
    obj_akg_m_y_value = metabolite_list.obj_akg_m.center.y
    obj_akg_c_y_value = 2 * obj_akg_m_y_value - bottom_most_horizontal_axis_y_value
    metabolite_list.obj_glu_m.set_center(Vector(right_2_vertical_axis_x_value, obj_akg_m_y_value))
    metabolite_list.obj_gln_m.set_center(Vector(right_2_vertical_axis_x_value, bottom_most_horizontal_axis_y_value))
    metabolite_list.obj_glu_c.set_center(Vector(right_3_vertical_axis_x_value, obj_akg_m_y_value))
    metabolite_list.obj_gln_c.set_center(Vector(right_3_vertical_axis_x_value, bottom_most_horizontal_axis_y_value))
    metabolite_list.obj_akg_c.set_center(Vector(right_3_vertical_axis_x_value, obj_akg_c_y_value))
    metabolite_list.obj_gln_e.set_center(Vector(right_most_vertical_axis_x_value, bottom_most_horizontal_axis_y_value))
    above_glu_display_text_y_value = obj_akg_m_y_value + display_text_vertical_distance + display_text_half_height
    above_gln_display_text_y_value = bottom_most_horizontal_axis_y_value + \
        display_text_vertical_distance + display_text_half_height
    add_straight_reaction_between_metabolites(
        obj_akg_m_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal, obj_akg_m_y_value,
        reaction_list.obj_glud_m
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            (obj_akg_m_x_value + right_2_vertical_axis_x_value) / 2,
            above_glu_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    glu_gln_trans_display_text_x_value = (right_3_vertical_axis_x_value + right_2_vertical_axis_x_value) / 2
    add_straight_reaction_between_metabolites(
        right_3_vertical_axis_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal, obj_akg_m_y_value,
        reaction_list.obj_glu_trans
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            glu_gln_trans_display_text_x_value,
            above_glu_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    add_straight_reaction_between_metabolites(
        right_3_vertical_axis_x_value, right_2_vertical_axis_x_value, ParameterName.horizontal,
        bottom_most_horizontal_axis_y_value, reaction_list.obj_gln_trans
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            glu_gln_trans_display_text_x_value,
            above_gln_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    add_straight_reaction_between_metabolites(
        right_most_vertical_axis_x_value, right_3_vertical_axis_x_value, ParameterName.horizontal,
        bottom_most_horizontal_axis_y_value, reaction_list.obj_gln_input
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            right_exchange_flux_display_text_x_value,
            above_gln_display_text_y_value,
        ),
        ParameterName.vertical_alignment: VerticalAlignment.baseline
    })
    glu_gln_conversion_display_text_y_value = (bottom_most_horizontal_axis_y_value + obj_akg_m_y_value) / 2
    add_straight_reaction_between_metabolites(
        bottom_most_horizontal_axis_y_value, obj_akg_m_y_value, ParameterName.vertical,
        right_2_vertical_axis_x_value, reaction_list.obj_glnd_m
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            ser_left_display_text_x_value,
            glu_gln_conversion_display_text_y_value,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.right
    })
    glu_c_right_display_text_x_value = right_3_vertical_axis_x_value + \
        display_text_horizontal_distance + display_text_half_width
    add_straight_reaction_between_metabolites(
        bottom_most_horizontal_axis_y_value, obj_akg_m_y_value, ParameterName.vertical,
        right_3_vertical_axis_x_value, reaction_list.obj_as_c
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            glu_c_right_display_text_x_value,
            glu_gln_conversion_display_text_y_value,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.left
    })
    add_straight_reaction_between_metabolites(
        obj_akg_c_y_value, obj_akg_m_y_value, ParameterName.vertical, right_3_vertical_axis_x_value,
        reaction_list.obj_akg_to_glu_c
    ).set_display_text_config_dict({
        ParameterName.center: Vector(
            glu_c_right_display_text_x_value,
            (obj_akg_m_y_value + obj_akg_c_y_value) / 2,
        ),
        ParameterName.horizontal_alignment: HorizontalAlignment.left
    })

    reaction_list.obj_biomass.set_display_text_config_dict({
        ParameterName.center: Vector(
            (right_1_vertical_axis_x_value + right_2_vertical_axis_x_value) / 2,
            (pyr_m_y_value + accoa_m_y_value) / 2,
        )
    })

    # Subnetwork

    subnetwork_list.obj_cell.set_location(
        Vector(cell_subnetwork_left, cell_subnetwork_right),
        Vector(cell_subnetwork_bottom, cell_subnetwork_top)
    )

    subnetwork_list.obj_mitochondria.set_location(
        Vector(mitochondria_subnetwork_left, mitochondria_subnetwork_right),
        Vector(mitochondria_subnetwork_bottom, mitochondria_subnetwork_top)
    )
