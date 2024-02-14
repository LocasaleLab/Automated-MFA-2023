from ..config import np, Vector, NetworkGeneralConfig, MetaboliteConfig, ReactionConfig, ParameterName, \
    HorizontalAlignment, VerticalAlignment

from .common_functions import add_straight_reaction_between_metabolites, cycle_layout, \
    add_bent_reaction_between_metabolites


metabolite_height = MetaboliteConfig.height
metabolite_width = MetaboliteConfig.width

reaction_stem_width = ReactionConfig.stem_width

display_text_vertical_distance = ReactionConfig.display_text_vertical_distance
display_text_horizontal_distance = ReactionConfig.display_text_horizontal_distance
display_text_half_height = ReactionConfig.display_text_height / 2
display_text_half_width = ReactionConfig.display_text_width / 2


def exchange_partial_network_layout_generator(
        metabolite_list, reaction_list, subnetwork_list, other_text_list, smaller_network=False):
    if smaller_network:
        main_vertical_axis_x_value = 0.2
        total_width = NetworkGeneralConfig.exchange_network_smaller_width
        total_height = NetworkGeneralConfig.exchange_network_smaller_height
    else:
        main_vertical_axis_x_value = 0.31  # Glycolysis
        total_width = NetworkGeneralConfig.exchange_network_normal_width
        total_height = NetworkGeneralConfig.exchange_network_normal_height
    # right_most_vertical_axis_x_value = main_vertical_axis_x_value + 0.57  # Input metabolites
    right_most_vertical_axis_x_value = main_vertical_axis_x_value + 0.61  # Input metabolites
    right_1_vertical_axis_x_value = main_vertical_axis_x_value + 0.11
    right_2_vertical_axis_x_value = main_vertical_axis_x_value + 0.28
    right_3_vertical_axis_x_value = main_vertical_axis_x_value + 0.46
    right_4_vertical_axis_x_value = main_vertical_axis_x_value + 0.52
    left_1_vertical_axis_x_value = main_vertical_axis_x_value - 0.12
    left_most_vertical_axis_x_value = 0.05
    mitochondria_subnetwork_left = left_1_vertical_axis_x_value - 0.065
    cell_subnetwork_left = mitochondria_subnetwork_left - 0.012
    mitochondria_subnetwork_right = (right_1_vertical_axis_x_value + right_2_vertical_axis_x_value) / 2
    if smaller_network:
        # cell_subnetwork_right = (right_most_vertical_axis_x_value + right_3_vertical_axis_x_value) / 2
        cell_subnetwork_right = right_3_vertical_axis_x_value + 0.055
    else:
        cell_subnetwork_right = (right_most_vertical_axis_x_value + right_4_vertical_axis_x_value) / 2

    # main_horizontal_axis_y_value = 0.405  # Pyruvate-lactate-alanine
    # top_most_horizontal_axis_y_value = main_horizontal_axis_y_value + 0.4486  # Glucose
    # bottom_1_horizontal_axis_y_value = 0.035  # Succinate
    # bottom_most_horizontal_axis_y_value = 0.03  # GLN
    if smaller_network:
        cell_subnetwork_bottom = 0
        bottom_most_horizontal_axis_y_value = 0  # GLN
    else:
        cell_subnetwork_bottom = 0.05
        bottom_most_horizontal_axis_y_value = 0.02  # GLN
    bottom_1_horizontal_axis_y_value = cell_subnetwork_bottom + 0.025  # Succinate
    main_horizontal_axis_y_value = cell_subnetwork_bottom + 0.395  # Pyruvate-lactate-alanine
    # mitochondria_subnetwork_bottom = bottom_most_horizontal_axis_y_value - 0.022
    mitochondria_subnetwork_bottom = cell_subnetwork_bottom + 0.008
    # glycolysis_interval = (top_most_horizontal_axis_y_value - main_horizontal_axis_y_value) / 6
    glycolysis_interval = 0.07476666666666666
    mitochondria_subnetwork_top = main_horizontal_axis_y_value - glycolysis_interval / 2
    # glycolysis_base_location = top_most_horizontal_axis_y_value - glycolysis_interval * 2
    # cell_subnetwork_top = top_most_horizontal_axis_y_value - glycolysis_interval * 2.5

    tca_top_y_value = main_horizontal_axis_y_value - 2.5 * glycolysis_interval
    tca_radius = (tca_top_y_value - bottom_1_horizontal_axis_y_value) / 2
    tca_center_y_value = bottom_1_horizontal_axis_y_value + tca_radius
    tca_theta_list = [150, 55, 0, -60]
    tca_reaction_theta_list = [
        ((135, None), (None, 75)),
        ((38, None), (None, 10)),
        ((-11, None), (None, -44)),
        ((-83, -82), (-198, -199)),
    ]
    display_text_theta_list = [105, 25, -27, -130]
    display_text_radius_ratio_list = [0.8, 0.75, 0.75, 0.75]

    gap_width = ReactionConfig.reaction_gap
    tca_left = main_vertical_axis_x_value - tca_radius
    tca_left_vertical_gap_line_pair_list = [(
        np.array([1, 0, -tca_left + gap_width / 2]),
        np.array([1, 0, -tca_left - gap_width / 2])
    )]

    # Glycolysis
    if smaller_network:
        glycolysis_metabolite_main_axis_list = []
        glycolysis_reaction_main_axis_list = []
    else:
        glycolysis_metabolite_main_axis_list = [
            metabolite_list.obj_glc_e,
            metabolite_list.obj_glc_c,
            metabolite_list.obj_3pg_c,
        ]
        glycolysis_reaction_main_axis_list = [
            reaction_list.obj_hex_c,
            reaction_list.obj_gapd_pgk_c,
            reaction_list.obj_pgm_eno_c,
        ]
    glycolysis_metabolite_main_axis_list.extend([
        # metabolite_list.obj_glc_e,
        # metabolite_list.obj_glc_c,
        # metabolite_list.obj_g6p_c,
        # metabolite_list.obj_fbp_c,
        # metabolite_list.obj_gap_c,
        # metabolite_list.obj_3pg_c,
        metabolite_list.obj_pep_c,
        metabolite_list.obj_pyr_c,
        metabolite_list.obj_pyr_m,
        metabolite_list.obj_accoa_m,
    ])
    pyr_c_index = glycolysis_metabolite_main_axis_list.index(metabolite_list.obj_pyr_c)
    # glycolysis_metabolite_y_location_list = [
    #     main_horizontal_axis_y_value + (pyr_c_index - metabolite_index) * glycolysis_interval
    #     for metabolite_index, _ in enumerate(glycolysis_metabolite_main_axis_list)
    # ]
    try:
        glc_c_index = glycolysis_metabolite_main_axis_list.index(metabolite_list.obj_glc_c)
        cell_subnetwork_top = main_horizontal_axis_y_value + (pyr_c_index - glc_c_index + 0.5) * glycolysis_interval
    except ValueError:
        pep_c_index = glycolysis_metabolite_main_axis_list.index(metabolite_list.obj_pep_c)
        cell_subnetwork_top = main_horizontal_axis_y_value + (pyr_c_index - pep_c_index + 0.5) * glycolysis_interval
    # last_y_location = main_horizontal_axis_y_value + (pyr_c_index + 1) * glycolysis_interval
    last_y_location = None

    glycolysis_reaction_main_axis_list.extend([
        # reaction_list.obj_hex_c,
        # reaction_list.obj_pgi_pfk_c,
        # reaction_list.obj_fba_c,
        # reaction_list.obj_gapd_pgk_c,
        # reaction_list.obj_pgm_eno_c,
        reaction_list.obj_pyk_c,
        reaction_list.obj_pyr_trans,
        reaction_list.obj_pdh_m,
    ])

    # glycolysis_text_config = {
    #     **other_display_text_config,
    #     ParameterName.string: 'Glycolysis or\nGluconeogenesis',
    #     ParameterName.center: Vector(main_vertical_axis_x_value, glycolysis_base_location + 0.005),
    # }
    # other_text_list.append(glycolysis_text_config)
    # last_y_location = glycolysis_base_location
    for metabolite_index, metabolite_obj in enumerate(glycolysis_metabolite_main_axis_list):
        # current_y_location = glycolysis_base_location - metabolite_index * glycolysis_interval
        current_y_location = main_horizontal_axis_y_value + (pyr_c_index - metabolite_index) * glycolysis_interval
        metabolite_obj.set_center(Vector(main_vertical_axis_x_value, current_y_location))
        if metabolite_index != 0:
            reaction_obj = glycolysis_reaction_main_axis_list[metabolite_index - 1]
            add_straight_reaction_between_metabolites(
                last_y_location, current_y_location, ParameterName.vertical, main_vertical_axis_x_value, reaction_obj)
            display_text_x_value = main_vertical_axis_x_value - display_text_horizontal_distance - \
                display_text_half_width
            display_text_y_value = (last_y_location + current_y_location) / 2
            horizontal_alignment = HorizontalAlignment.right
            if reaction_obj is reaction_list.obj_pdh_m:
                display_text_x_value = main_vertical_axis_x_value + display_text_horizontal_distance + \
                    display_text_half_width
                horizontal_alignment = HorizontalAlignment.left
            reaction_obj.set_display_text_config_dict({
                ParameterName.center: Vector(display_text_x_value, display_text_y_value),
                ParameterName.horizontal_alignment: horizontal_alignment
            })
        last_y_location = current_y_location

    # LAC and ALA
    main_left_display_text_x_value = (left_1_vertical_axis_x_value + main_vertical_axis_x_value) / 2
    left_most_display_text_x_value = (left_most_vertical_axis_x_value + left_1_vertical_axis_x_value) / 2
    pyr_c_y_value = metabolite_list.obj_pyr_c.center.y
    metabolite_list.obj_lac_c.set_center(Vector(left_1_vertical_axis_x_value, pyr_c_y_value))
    above_pyr_display_text_y_value = (
            pyr_c_y_value + display_text_vertical_distance + display_text_half_height)
    if not smaller_network:
        metabolite_list.obj_lac_e.set_center(Vector(left_most_vertical_axis_x_value, pyr_c_y_value))
        add_straight_reaction_between_metabolites(
            left_1_vertical_axis_x_value, left_most_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
            reaction_list.obj_lac_output).set_display_text_config_dict({
                ParameterName.center: Vector(
                    left_most_display_text_x_value,
                    above_pyr_display_text_y_value
                ),
                ParameterName.vertical_alignment: VerticalAlignment.baseline
            })
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, left_1_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_ldh_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                main_left_display_text_x_value,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    pep_c_x_value, pep_c_y_value = metabolite_list.obj_pep_c.center
    ala_c_x_value = right_1_vertical_axis_x_value + 0.08
    metabolite_list.obj_ala_c.set_center(Vector(ala_c_x_value, pyr_c_y_value))
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, ala_c_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_gpt_c)
    glu_akg_c_2_y_value = (pyr_c_y_value + pep_c_y_value) / 2
    glu_c_2_x_value = main_vertical_axis_x_value + 0.05
    akg_c_2_x_value = right_2_vertical_axis_x_value - 0.115
    metabolite_list.obj_glu_c_2.set_center(Vector(glu_c_2_x_value, glu_akg_c_2_y_value))
    metabolite_list.obj_akg_c_2.set_center(Vector(akg_c_2_x_value, glu_akg_c_2_y_value))
    glu_akg_c_2_mid_x_value = (glu_c_2_x_value + akg_c_2_x_value) / 2
    gpt_c_tail = metabolite_list.obj_glu_c_2.center + Vector(0.03, -0.015)
    gpt_c_mid = Vector(glu_akg_c_2_mid_x_value, pyr_c_y_value + reaction_stem_width)
    gpt_c_head = metabolite_list.obj_akg_c_2.center + Vector(-0.03, -0.015)
    reaction_list.obj_gpt_c.extend_reaction_start_end_list([
        (
            ParameterName.path_cycle, gpt_c_tail, gpt_c_mid, gpt_c_head, {}),
    ]).set_display_text_config_dict({
            ParameterName.center: Vector(
                glu_akg_c_2_mid_x_value,
                pyr_c_y_value - 0.02
            ),
            ParameterName.vertical_alignment: VerticalAlignment.top
        })

    # TCA
    tca_metabolite_cycle_list = [
        metabolite_list.obj_oac_m,
        metabolite_list.obj_cit_m,
        metabolite_list.obj_akg_m,
        metabolite_list.obj_mal_m
    ]
    tca_reaction_cycle_list = [
        reaction_list.obj_cs_m,
        reaction_list.obj_acont_icdh_m,
        reaction_list.obj_akgd_sucoas_m,
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

    oac_m_y_value = metabolite_list.obj_oac_m.center.y
    oac_m_x_value = metabolite_list.obj_oac_m.center.x
    pyr_m_y_value = metabolite_list.obj_pyr_m.center.y
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

    # Exchange
    akg_m_x_value, akg_m_y_value = metabolite_list.obj_akg_m.center
    # metabolite_list.obj_glu_m.set_center(Vector(left_2_vertical_axis_x_value, akg_m_y_value))
    # metabolite_list.obj_asp_m.set_center(Vector(left_2_vertical_axis_x_value, oac_m_y_value))
    # add_straight_reaction_between_metabolites(
    #     akg_m_x_value, left_2_vertical_axis_x_value, ParameterName.horizontal, akg_m_y_value,
    #     reaction_list.obj_aspta_circle_m, {ParameterName.gap_line_pair_list: tca_left_vertical_gap_line_pair_list}
    # ).set_display_text_config_dict({
    #         ParameterName.center: Vector(
    #             main_vertical_axis_x_value - 0.01,
    #             akg_m_y_value + 0.023
    #         ),
    #         ParameterName.vertical_alignment: VerticalAlignment.baseline
    #     })
    # aspta_circle_m_tail = metabolite_list.obj_asp_m.center + Vector(0.03, -0.015)
    # aspta_circle_m_mid = Vector(
    #     (metabolite_list.obj_oac_m.center.x + metabolite_list.obj_asp_m.center.x) / 2,
    #     akg_m_y_value + reaction_stem_width)
    # aspta_circle_m_head = metabolite_list.obj_oac_m.center - Vector(0.03, 0.015)
    # reaction_list.obj_aspta_circle_m.extend_reaction_start_end_list([
    #     (ParameterName.path_cycle, aspta_circle_m_tail, aspta_circle_m_mid, aspta_circle_m_head, {})])

    mal_m_x_value, mal_m_y_value = metabolite_list.obj_mal_m.center
    cit_m_x_value, cit_m_y_value = metabolite_list.obj_cit_m.center
    glu_c_y_value = akg_m_y_value - 0.04
    glu_c_x_value = right_3_vertical_axis_x_value - 0.06
    asp_c_y_value = akg_m_y_value + 0.01
    metabolite_list.obj_mal_c.set_center(Vector(right_2_vertical_axis_x_value + 0.03, mal_m_y_value))
    metabolite_list.obj_akg_c.set_center(Vector(right_2_vertical_axis_x_value, akg_m_y_value))
    metabolite_list.obj_cit_c.set_center(Vector(right_2_vertical_axis_x_value + 0.03, cit_m_y_value + 0.04))
    metabolite_list.obj_oac_c.set_center(Vector(right_2_vertical_axis_x_value + 0.08, akg_m_y_value + 0.05))
    metabolite_list.obj_glu_c.set_center(Vector(glu_c_x_value, glu_c_y_value))
    metabolite_list.obj_asp_c.set_center(Vector(right_3_vertical_axis_x_value, asp_c_y_value))
    akg_c_x_value, akg_c_y_value = metabolite_list.obj_akg_c.center
    oac_c_x_value, oac_c_y_value = metabolite_list.obj_oac_c.center

    if not smaller_network:
        metabolite_list.obj_gln_c.set_center(Vector(right_4_vertical_axis_x_value, glu_c_y_value))
        metabolite_list.obj_gln_e.set_center(
            Vector(right_4_vertical_axis_x_value, bottom_most_horizontal_axis_y_value))
        below_as_c_display_text_y_value = glu_c_y_value - display_text_vertical_distance - display_text_half_height
        as_c_display_text_x_value = (glu_c_x_value + right_4_vertical_axis_x_value) / 2
        add_straight_reaction_between_metabolites(
            glu_c_x_value, right_4_vertical_axis_x_value, ParameterName.horizontal,
            glu_c_y_value, reaction_list.obj_as_c
        ).set_display_text_config_dict({
            ParameterName.center: Vector(
                as_c_display_text_x_value,
                below_as_c_display_text_y_value,
            ),
            ParameterName.vertical_alignment: VerticalAlignment.top,
        })
        gln_input_display_text_x_value = right_4_vertical_axis_x_value - display_text_horizontal_distance \
            - display_text_half_width
        gln_input_display_text_y_value = (bottom_most_horizontal_axis_y_value + glu_c_y_value) / 2
        add_straight_reaction_between_metabolites(
            bottom_most_horizontal_axis_y_value, glu_c_y_value, ParameterName.vertical,
            right_4_vertical_axis_x_value, reaction_list.obj_gln_input
        ).set_display_text_config_dict({
            ParameterName.center: Vector(
                gln_input_display_text_x_value,
                gln_input_display_text_y_value,
            ),
            ParameterName.horizontal_alignment: HorizontalAlignment.right,
        })
        metabolite_list.obj_asp_e.set_center(Vector(right_most_vertical_axis_x_value, asp_c_y_value))
        asp_input_display_text_x_value = (right_most_vertical_axis_x_value + right_3_vertical_axis_x_value) / 2
        asp_input_display_text_y_value = asp_c_y_value + display_text_vertical_distance + display_text_half_height
        add_straight_reaction_between_metabolites(
            right_most_vertical_axis_x_value, right_3_vertical_axis_x_value, ParameterName.horizontal, asp_c_y_value,
            reaction_list.obj_asp_input).set_display_text_config_dict({
                ParameterName.center: Vector(
                    asp_input_display_text_x_value,
                    asp_input_display_text_y_value,
                ),
                ParameterName.vertical_alignment: VerticalAlignment.baseline
            })

    akg_c_trans_x_value = akg_c_x_value - 0.02
    add_bent_reaction_between_metabolites(
        akg_c_2_x_value, glu_akg_c_2_y_value, ParameterName.horizontal,
        akg_c_y_value, akg_c_trans_x_value,
        reaction_list.obj_akg_c_trans).set_display_text_config_dict({
            ParameterName.center: Vector(akg_c_trans_x_value - 0.04, (oac_c_y_value + pep_c_y_value) / 2),
            ParameterName.horizontal_alignment: HorizontalAlignment.right,
        })

    akgmal_circle_m_common_mid = Vector((akg_m_x_value + akg_c_x_value) / 2, (akg_m_y_value + mal_m_y_value) / 2)
    akgmal_circle_m_edge1_tail = metabolite_list.obj_akg_m.center + Vector(0.03, -0.015)
    akgmal_circle_m_edge1_mid = akgmal_circle_m_common_mid + Vector(0, reaction_stem_width / 2)
    akgmal_circle_m_edge1_head = metabolite_list.obj_akg_c.center + Vector(-0.03, -0.015)
    akgmal_circle_m_edge2_tail = metabolite_list.obj_mal_c.center + Vector(-0.037, 0.008)
    akgmal_circle_m_edge2_mid = akgmal_circle_m_common_mid - Vector(0, reaction_stem_width / 2)
    akgmal_circle_m_edge2_head = metabolite_list.obj_mal_m.center + Vector(0.04, 0.005)
    reaction_list.obj_akgmal_circle_m.extend_reaction_start_end_list([
        (
            ParameterName.path_cycle, akgmal_circle_m_edge1_tail, akgmal_circle_m_edge1_mid,
            akgmal_circle_m_edge1_head, {}),
        (
            ParameterName.path_cycle, akgmal_circle_m_edge2_tail, akgmal_circle_m_edge2_mid,
            akgmal_circle_m_edge2_head, {})
    ]).set_display_text_config_dict({
            ParameterName.center: akgmal_circle_m_common_mid + Vector(0, -0.02),
            ParameterName.vertical_alignment: VerticalAlignment.top
        })

    mal_c_x_value, mal_c_y_value = metabolite_list.obj_mal_c.center
    cit_trans_circle_common_mid = Vector((mal_m_x_value + mal_c_x_value) / 2, (cit_m_y_value + mal_m_y_value) / 2)
    cit_trans_circle_edge1_tail = metabolite_list.obj_cit_c.center + Vector(-0.02, -0.018)
    cit_trans_circle_edge1_mid = cit_trans_circle_common_mid + Vector(0, reaction_stem_width / 2)
    cit_trans_circle_edge1_head = metabolite_list.obj_cit_m.center + Vector(0.04, -0.015)
    cit_trans_circle_edge2_tail = metabolite_list.obj_mal_m.center + Vector(0.038, 0.012)
    cit_trans_circle_edge2_mid = cit_trans_circle_common_mid - Vector(0, reaction_stem_width / 2)
    cit_trans_circle_edge2_head = metabolite_list.obj_mal_c.center + Vector(-0.025, 0.018)
    reaction_list.obj_cit_trans_circle.extend_reaction_start_end_list([
        (
            ParameterName.path_cycle, cit_trans_circle_edge1_tail, cit_trans_circle_edge1_mid,
            cit_trans_circle_edge1_head, {}),
        (
            ParameterName.path_cycle, cit_trans_circle_edge2_tail, cit_trans_circle_edge2_mid,
            cit_trans_circle_edge2_head, {})
    ]).set_display_text_config_dict({
            ParameterName.center: cit_trans_circle_common_mid + Vector(0, 0.02),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    mdh_c_reaction_x_value = (mal_c_x_value + oac_c_x_value) / 2
    mdh_c_reaction_text_y_value = mal_c_y_value * 0.65 + oac_c_y_value * 0.35
    add_straight_reaction_between_metabolites(
        mal_c_y_value, oac_c_y_value, ParameterName.vertical, mdh_c_reaction_x_value,
        reaction_list.obj_mdh_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                mdh_c_reaction_x_value - 0.04,
                mdh_c_reaction_text_y_value,
            ),
            ParameterName.horizontal_alignment: HorizontalAlignment.right
        })

    aspta_circle_c_common_mid = (metabolite_list.obj_oac_c.center + metabolite_list.obj_glu_c.center) / 2
    aspta_circle_c_edge1_tail = metabolite_list.obj_asp_c.center + Vector(-0.038, 0)
    aspta_circle_c_edge1_mid = aspta_circle_c_common_mid + Vector(0, reaction_stem_width / 2)
    aspta_circle_c_edge1_head = metabolite_list.obj_oac_c.center + Vector(0, -0.018)
    aspta_circle_c_edge2_tail = metabolite_list.obj_akg_c.center + Vector(0.038, 0)
    aspta_circle_c_edge2_mid = aspta_circle_c_common_mid - Vector(0, reaction_stem_width / 2)
    aspta_circle_c_edge2_head = metabolite_list.obj_glu_c.center + Vector(0, 0.018)
    reaction_list.obj_aspta_circle_c.extend_reaction_start_end_list([
        (
            ParameterName.path_cycle, aspta_circle_c_edge1_tail, aspta_circle_c_edge1_mid,
            aspta_circle_c_edge1_head, {}),
        (
            ParameterName.path_cycle, aspta_circle_c_edge2_tail, aspta_circle_c_edge2_mid,
            aspta_circle_c_edge2_head, {})
    ]).set_display_text_config_dict({
            ParameterName.center: aspta_circle_c_common_mid + Vector(0, 0),
            # ParameterName.vertical_alignment: VerticalAlignment.baseline
        })

    cit_c_x_value, cit_c_y_value = metabolite_list.obj_cit_c.center
    obj_acitl_c_reaction_x_value = (cit_c_x_value + oac_c_x_value) / 2
    obj_acitl_c_reaction_text_y_value = oac_c_y_value * 0.5 + cit_c_y_value * 0.5
    add_straight_reaction_between_metabolites(
        cit_c_y_value, oac_c_y_value, ParameterName.vertical, obj_acitl_c_reaction_x_value,
        reaction_list.obj_acitl_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                obj_acitl_c_reaction_x_value,
                obj_acitl_c_reaction_text_y_value,
            ),
            # ParameterName.horizontal_alignment: HorizontalAlignment.right
        })

    add_bent_reaction_between_metabolites(
        oac_c_y_value, oac_c_x_value + 0.01, ParameterName.vertical,
        pep_c_x_value, pep_c_y_value,
        reaction_list.obj_pepck_circle_c
    ).set_display_text_config_dict({
            ParameterName.center: Vector(oac_c_x_value + 0.055, (oac_c_y_value + pep_c_y_value) / 2),
            ParameterName.horizontal_alignment: HorizontalAlignment.left,
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

    return total_width, total_height
