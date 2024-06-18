from ..config import ColorConfig
from .metabolite import Metabolite
from .reaction import Reaction
from .subnetwork import Subnetwork


class MetaboliteList(object):
    def __init__(self, infusion=False):
        # Glycolysis
        self.obj_glc_c = Metabolite('GLC_c')
        self.obj_g6p_c = Metabolite('G6P_c')
        self.obj_fbp_c = Metabolite('FBP_c')
        self.obj_gap_c = Metabolite('GAP_c')
        self.obj_dhap_c = Metabolite('DHAP_c')
        self.obj_3pg_c = Metabolite('3PG_c')
        self.obj_pep_c = Metabolite('PEP_c')
        self.obj_pyr_c = Metabolite('PYR_c')
        self.obj_lac_c = Metabolite('LAC_c')

        self.obj_cit_c = Metabolite('CIT_c')
        self.obj_akg_c = Metabolite('AKG_c')
        self.obj_akg_c_2 = Metabolite('AKG_c')
        self.obj_oac_c = Metabolite('OAC_c')
        self.obj_mal_c = Metabolite('MAL_c')
        self.obj_accoa_c = Metabolite('ACCOA_c')

        # TCA_cycle
        self.obj_pyr_m = Metabolite('PYR_m')
        self.obj_accoa_m = Metabolite('ACCOA_m')
        self.obj_cit_m = Metabolite('CIT_m')
        self.obj_akg_m = Metabolite('AKG_m')
        self.obj_suc_m = Metabolite('SUC_m')
        self.obj_mal_m = Metabolite('MAL_m')
        self.obj_oac_m = Metabolite('OAC_m')

        # PPP
        self.obj_rul5p_c = Metabolite('RUL5P_c')
        self.obj_rib5p_c = Metabolite('RIB5P_c')
        self.obj_ery4p_c = Metabolite('ERY4P_c')

        # AA
        self.obj_asp_m = Metabolite('ASP_m')
        self.obj_glu_m = Metabolite('GLU_m')
        self.obj_gln_m = Metabolite('GLN_m')
        self.obj_ala_c = Metabolite('ALA_c')
        self.obj_ser_c = Metabolite('SER_c')
        self.obj_gly_c = Metabolite('GLY_c')
        self.obj_asp_c = Metabolite('ASP_c')
        self.obj_glu_c = Metabolite('GLU_c')
        self.obj_glu_c_2 = Metabolite('GLU_c')
        self.obj_gln_c = Metabolite('GLN_c')

        # Input
        self.obj_glc_unlabelled_e = Metabolite('GLC_unlabelled_e', display_metabolite_name='GLC')
        self.obj_glc_e = Metabolite('GLC_e')
        self.obj_lac_e = Metabolite('LAC_e')
        self.obj_gly_e = Metabolite('GLY_e')
        self.obj_asp_e = Metabolite('ASP_e')
        self.obj_ser_e = Metabolite('SER_e')
        self.obj_ala_e = Metabolite('ALA_e')
        self.obj_gln_e = Metabolite('GLN_e')
        self.obj_glu_e = Metabolite('GLU_e')
        self.obj_pyr_e = Metabolite('PYR_e')

        self.content_list_pair = [
            (value.metabolite_name, value) for value in self.__dict__.values() if isinstance(value, Metabolite)
        ]


class ReactionList(object):
    reaction_name_mapping_dict = {
        'PGI_PFK_c': (
            'PGI_c\nPFK_c',
            ['PGI_c', 'PFK_c'],
            lambda pgi_c_value_obj, pfk_c_value_obj: pgi_c_value_obj),
        'GAPD_PGK_c': (
            'GAPD_c\nPGK_c',
            ['GAPD_c', 'PGK_c'],
            lambda gapd_c_value_obj, pgk_c_value_obj: pgk_c_value_obj),
        'PGM_ENO_c': (
            'PGM_c\nENO_c',
            ['PGM_c', 'ENO_c'],
            lambda pgm_c_value_obj, eno_c_value_obj: eno_c_value_obj),
        'ACONT_ICDH_m': (
            'ACONT_m\nICDH_m',
            ['ACONT_m', 'ICDH_m'],
            lambda acont_m_value_obj, icdh_m_value_obj: icdh_m_value_obj),
        'AKGD_SUCOAS_m': (
            'AKGD_m\nSUCOAS_m',
            ['AKGD_m', 'SUCOAS_m'],
            lambda akgd_m_value_obj, sucoas_m_value_obj: sucoas_m_value_obj),
        'SUCD_FUMH_m': (
            'SUCD_m\nFUMH_m',
            ['SUCD_m', 'FUMH_m'],
            lambda sucd_m_value_obj, fumh_m_value_obj: fumh_m_value_obj),
        'RPE_TKT1_TKT2_TALA_c': (
            'RPE_c TKT1_c\nTKT2_c TALA_c',
            ['RPE_c', 'TKT1_c', 'TKT2_c', 'TALA_c'],
            lambda rpe_c_value_obj, tkt1_c_value_obj, tkt2_c_value_obj, tala_c_value_obj: tala_c_value_obj),
        'GLN_to_GLU_c': (
            'AS_c - GLNS_c',
            ['AS_c', 'GLNS_c'],
            lambda as_c_value_obj, glns_c_value_obj: (as_c_value_obj, glns_c_value_obj)),
        'AKG_to_GLU_c': (
            'ASPTA_c + GPT_c',
            ['ASPTA_c', 'GPT_c'],
            lambda aspta_c_value_obj, gpt_c_value_obj: (
                aspta_c_value_obj[0] + gpt_c_value_obj[1],
                aspta_c_value_obj[1] + gpt_c_value_obj[0]
            )),
        'GLN_to_GLU_m': (
            'GLND_m - GLNS_m',
            ['GLND_m', 'GLNS_m'],
            lambda glnd_m_value_obj, glns_m_value_obj: (glnd_m_value_obj, glns_m_value_obj)),
    }
    normal_gln_to_glu_m = (
        'GLND_m',
        ['GLND_m', ],
        lambda glnd_m_value_obj: glnd_m_value_obj
    )

    def __init__(self, infusion=False, with_glns_m=False):
        # Glycolysis
        self.obj_hex_c = Reaction('HEX_c')
        # self.obj_pgi_c = Reaction('PGI_c', True)
        # self.obj_pfk_c = Reaction('PFK_c')
        self.obj_pgi_pfk_c = Reaction('PGI_PFK_c', True)
        self.obj_fba_c = Reaction('FBA_c', True)
        self.obj_tpi_c = Reaction('TPI_c', True)
        # self.obj_gapd_c = Reaction('GAPD_c', True)
        # self.obj_pgk_c = Reaction('PGK_c', True)
        self.obj_gapd_pgk_c = Reaction('GAPD_PGK_c', True)
        # self.obj_pgm_c = Reaction('PGM_c', True)
        # self.obj_eno_c = Reaction('ENO_c', True)
        self.obj_pgm_eno_c = Reaction('PGM_ENO_c', True)
        self.obj_pyk_c = Reaction('PYK_c')
        self.obj_ldh_c = Reaction('LDH_c', True)

        self.obj_pepck_c = Reaction('PEPCK_c')
        self.obj_pepck_circle_c = Reaction('PEPCK_c')
        self.obj_acitl_c = Reaction('ACITL_c')
        self.obj_mdh_c = Reaction('MDH_c', True)
        # self.obj_me2_c = Reaction('ME2_c')
        # self.obj_lipid_c = Reaction('LIPID_c')

        # TCA cycle
        self.obj_pdh_m = Reaction('PDH_m')
        self.obj_cs_m = Reaction('CS_m')
        # self.obj_acont_m = Reaction('ACONT_m', True)
        # self.obj_icdh_m = Reaction('ICDH_m')
        self.obj_acont_icdh_m = Reaction('ACONT_ICDH_m')
        # self.obj_akgd_m = Reaction('AKGD_m')
        # self.obj_sucoas_m = Reaction('SUCOAS_m')
        self.obj_akgd_sucoas_m = Reaction('AKGD_SUCOAS_m')
        # self.obj_sucd_m = Reaction('SUCD_m', True)
        # self.obj_fumh_m = Reaction('FUMH_m', True)
        self.obj_sucd_fumh_m = Reaction('SUCD_FUMH_m', True)
        self.obj_mdh_m = Reaction('MDH_m', True)

        self.obj_pc_m = Reaction('PC_m')

        # Ser-Gly
        self.obj_phgdh_psat_psp_c = Reaction('PHGDH_PSAT_PSP_c')
        self.obj_shmt_c = Reaction('SHMT_c', True)
        self.obj_ser_input = Reaction('SER_input')
        self.obj_gly_input = Reaction('GLY_input')

        # PPP
        self.obj_g6pdh2r_pgl_gnd_reaction = Reaction('G6PDH2R_PGL_GND_c')
        self.obj_rpi_c = Reaction('RPI_c', True)
        self.obj_rpe_tkt_tala_c = Reaction('RPE_TKT1_TKT2_TALA_c', True, change_arrow_by_value=False)

        # GLU
        self.obj_glud_m = Reaction('GLUD_m', True)
        if with_glns_m:
            glnd_m_reversible = True
        else:
            glnd_m_reversible = False
            self.reaction_name_mapping_dict['GLN_to_GLU_m'] = self.normal_gln_to_glu_m
        # self.obj_glnd_m = Reaction('GLND_m', glnd_m_reversible)
        self.obj_glnd_m = Reaction('GLN_to_GLU_m', glnd_m_reversible)
        self.obj_as_c = Reaction('GLN_to_GLU_c', True)
        self.obj_aspta_m = Reaction('ASPTA_m', True)
        self.obj_aspta_circle_m = Reaction('ASPTA_m', True)
        self.obj_aspta_c = Reaction('ASPTA_c', True)
        self.obj_aspta_circle_c = Reaction('ASPTA_c', True)
        self.obj_akg_to_glu_c = Reaction('AKG_to_GLU_c', True)

        # ALA
        self.obj_ala_input = Reaction('ALA_input')
        self.obj_gpt_c = Reaction('GPT_c', True)
        self.obj_akg_c_trans = Reaction('GPT_c', True)

        # Exchange
        self.obj_pyr_trans = Reaction('PYR_trans', True)
        self.obj_aspglu_m = Reaction('ASPGLU_m', True)
        self.obj_akgmal_m = Reaction('AKGMAL_m', True)
        self.obj_akgmal_circle_m = Reaction('AKGMAL_m', True)
        self.obj_cit_trans = Reaction('CIT_trans', True)
        self.obj_cit_trans_circle = Reaction('CIT_trans', True)
        self.obj_gln_trans = Reaction('GLN_trans', True)
        self.obj_glu_trans = Reaction('GLU_trans', True)

        # Intake
        # self.obj_glc_input = Reaction('GLC_input')
        # self.obj_glc_unlabelled_input = Reaction('GLC_unlabelled_input')
        # self.obj_gln_input = Reaction('GLN_input')
        # self.obj_asp_input = Reaction('ASP_input')
        # self.obj_lac_output = Reaction('LAC_output')
        # self.obj_pyr_input = Reaction('PYR_input')
        self.obj_glc_input = Reaction('GLC_input')
        self.obj_glc_unlabelled_input = Reaction('GLC_unlabelled_input', True)
        self.obj_gln_input = Reaction('GLN_input')
        self.obj_asp_input = Reaction('ASP_input')
        self.obj_lac_output = Reaction('LAC_output')
        self.obj_pyr_input = Reaction('PYR_input')
        self.obj_biomass = Reaction('BIOMASS_REACTION')

        self.content_list_pair = [
            (value.reaction_name, value) for value in self.__dict__.values() if isinstance(value, Reaction)
        ]


class SubnetworkList(object):
    def __init__(self, infusion=False):
        self.obj_cell = Subnetwork('cell', color=ColorConfig.cell_network_color, more_top_margin=infusion)
        self.obj_mitochondria = Subnetwork('mitochondria', color=ColorConfig.mitochondria_network_color)

        self.content_list_pair = [
            (value.subnetwork_name, value) for value in self.__dict__.values() if isinstance(value, Subnetwork)
        ]


def reaction_raw_value_processing(reaction_raw_value_dict):
    analyzed_reaction_name_set = set()
    final_reaction_value_dict = {}
    reverse_reaction_suffix = '__R'
    for reaction_raw_name, reaction_raw_value in reaction_raw_value_dict.items():
        if reaction_raw_name in analyzed_reaction_name_set or reaction_raw_name.startswith('MIX'):
            continue
        if reaction_raw_name.endswith(reverse_reaction_suffix):
            forward_reaction_name = reaction_raw_name[:-len(reverse_reaction_suffix)]
            forward_reaction_value = reaction_raw_value_dict[forward_reaction_name]
            reaction_value_obj = (forward_reaction_value, reaction_raw_value)
            analyzed_reaction_name_set.add(reaction_raw_name)
        else:
            forward_reaction_name = reaction_raw_name
            reverse_reaction_name = f'{reaction_raw_name}{reverse_reaction_suffix}'
            if reverse_reaction_name in reaction_raw_value_dict:
                reverse_reaction_value = reaction_raw_value_dict[reverse_reaction_name]
                reaction_value_obj = (reaction_raw_value, reverse_reaction_value)
                analyzed_reaction_name_set.add(reverse_reaction_name)
            else:
                reaction_value_obj = reaction_raw_value
        final_reaction_value_dict[forward_reaction_name] = reaction_value_obj
        analyzed_reaction_name_set.add(forward_reaction_name)
    return final_reaction_value_dict


def assign_value_to_network(
        reaction_raw_value_dict, reaction_list: ReactionList, infusion=False):
    reaction_name_mapping_dict = reaction_list.reaction_name_mapping_dict
    processed_reaction_value_dict = reaction_raw_value_processing(reaction_raw_value_dict)
    for reaction_name, reaction_obj in reaction_list.content_list_pair:
        if reaction_name in processed_reaction_value_dict:
            reaction_obj.set_value(processed_reaction_value_dict[reaction_name])
        elif reaction_name in reaction_name_mapping_dict:
            _, required_reaction_name_list, reaction_process_func = reaction_name_mapping_dict[reaction_name]
            required_reaction_obj_list = []
            success = True
            for required_reaction_name in required_reaction_name_list:
                if required_reaction_name in processed_reaction_value_dict:
                    required_reaction_obj_list.append(processed_reaction_value_dict[required_reaction_name])
                else:
                    success = False
                    break
            if success:
                reaction_obj.set_value(reaction_process_func(*required_reaction_obj_list))


def assign_flux_name_to_network(reaction_list: ReactionList):
    reaction_name_mapping_dict = reaction_list.reaction_name_mapping_dict
    for reaction_name, reaction_obj in reaction_list.content_list_pair:
        if reaction_name in reaction_name_mapping_dict:
            display_flux_name, *_ = reaction_name_mapping_dict[reaction_name]
            reaction_obj.set_display_text(display_flux_name)
        else:
            reaction_obj.set_display_text(reaction_name)
