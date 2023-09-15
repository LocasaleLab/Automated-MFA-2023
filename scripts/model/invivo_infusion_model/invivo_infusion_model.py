from scripts.src.core.common.config import ModelKeyword

normal_range = ModelKeyword.normal_range_type
add_range = ModelKeyword.add_range_type


# Renal carcinoma model
glycolysis_reaction_list = [
    {
        'id': 'HEX_c',
        'sub': [('GLC_c', 'abcdef')],
        'pro': [('GLC6P_c', 'abcdef')],
    },
    {
        'id': 'PGI_c',
        'sub': [('GLC6P_c', 'abcdef')],
        'pro': [('FRU6P_c', 'abcdef')],
        'reverse': True
    },
    {
        'id': 'PFK_c',
        'sub': [('FRU6P_c', 'abcdef')],
        'pro': [('FRU16BP_c', 'abcdef')],
    },
    {
        'id': 'FBA_c',
        'sub': [('FRU16BP_c', 'abcdef')],
        'pro': [('DHAP_c', 'cba'), ('GAP_c', 'def')],
        'reverse': True
    },
    {
        'id': 'TPI_c',
        'sub': [('DHAP_c', 'abc')],
        'pro': [('GAP_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'GAPD_c',
        'sub': [('GAP_c', 'abc')],
        'pro': [('13BPG_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'PGK_c',
        'sub': [('13BPG_c', 'abc')],
        'pro': [('3PG_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'PGM_c',
        'sub': [('3PG_c', 'abc')],
        'pro': [('2PG_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'ENO_c',
        'sub': [('2PG_c', 'abc')],
        'pro': [('PEP_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'PYK_c',
        'sub': [('PEP_c', 'abc')],
        'pro': [('PYR_c', 'abc')],
    },
    {
        'id': 'LDH_c',
        'sub': [('PYR_c', 'abc')],
        'pro': [('LAC_c', 'abc')],
        'reverse': True
    },
    {
        'id': 'PEPCK_c',
        'sub': [('OAC_c', 'abcd')],
        'pro': [('PEP_c', 'abc'), ('CO2', 'd')],
    },
    {
        'id': 'ACITL_c',
        'sub': [('CIT_c', 'abcdef')],
        'pro': [('OAC_c', 'dcba'), ('ACCOA_c', 'fe')],
    },
    {
        'id': 'MDH_c',
        'sub': [('MAL_c', 'abcd')],
        'pro': [('OAC_c', 'abcd')],
        'reverse': True
    },
    {
        'id': 'ME2_c',
        'sub': [('MAL_c', 'abcd')],
        'pro': [('PYR_c', 'abc'), ('CO2', 'd')],
    },
    {
        'id': 'LIPID_c',
        'sub': [('ACCOA_c', 'ab')],
        'pro': [('ACCOA_lipid', 'ab')],
    },
]

ser_gly_reaction_list = [
    {
        'id': 'PHGDH_PSAT_PSP_c',
        'sub': [('3PG_c', 'abc')],
        'pro': [('SER_c', 'abc')],
    },
    {
        'id': 'SHMT_c',
        'sub': [('SER_c', 'abc')],
        'pro': [('GLY_c', 'ab'), ('1CTHF_c', 'c')],
        'reverse': True
    },
    {
        'id': 'SER_input',
        'sub': [('SER_e', 'abc')],
        'pro': [('SER_c', 'abc')],
    },
    {
        'id': 'GLY_input',
        'sub': [('GLY_e', 'ab')],
        'pro': [('GLY_c', 'ab')],
    },
]

tca_reaction_list = [
    {
        'id': 'PDH_m',
        'sub': [('PYR_m', 'abc')],
        'pro': [('ACCOA_m', 'bc'), ('CO2', 'a')],
    },
    {
        'id': 'CS_m',
        'sub': [('OAC_m', 'abcd'), ('ACCOA_m', 'ef')],
        'pro': [('CIT_m', 'dcbafe')],
    },
    {
        'id': 'ACONT_m',
        'sub': [('CIT_m', 'abcdef')],
        'pro': [('ICIT_m', 'abcdef')],
        'reverse': True
    },
    {
        'id': 'ICDH_m',
        'sub': [('ICIT_m', 'abcdef')],
        'pro': [('AKG_m', 'abcef'), ('CO2', 'd')],
    },
    {
        'id': 'AKGD_m',
        'sub': [('AKG_m', 'abcde')],
        'pro': [('SUCCOA_m', 'bcde'), ('CO2', 'a')],
    },
    {
        'id': 'SUCOAS_m',
        'sub': [('SUCCOA_m', 'abcd')],
        'pro': [('SUC_m', 'abcd')],
    },
    {
        'id': 'SUCD_m',
        'sub': [('SUC_m', 'abcd')],
        'pro': [('FUM_m', 'abcd')],
        'reverse': True
    },
    {
        'id': 'FUMH_m',
        'sub': [('FUM_m', 'abcd')],
        'pro': [('MAL_m', 'abcd')],
        'reverse': True
    },
    {
        'id': 'MDH_m',
        'sub': [('MAL_m', 'abcd')],
        'pro': [('OAC_m', 'abcd')],
        'reverse': True
    },
    {
        'id': 'PC_m',
        'sub': [('PYR_m', 'abc'), ('CO2', 'd')],
        'pro': [('OAC_m', 'abcd')],
    },
]


glu_reaction_list = [
    {
        'id': 'GLUD_m',
        'sub': [('AKG_m', 'abcde')],
        'pro': [('GLU_m', 'abcde')],
        'reverse': True
    },
    {
        'id': 'GLND_m',
        'sub': [('GLN_m', 'abcde')],
        'pro': [('GLU_m', 'abcde')],
    },
    {
        'id': 'GLNS_c',
        'sub': [('GLU_c', 'abcde')],
        'pro': [('GLN_c', 'abcde')],
    },
    {
        'id': 'ASPTA_m',
        'sub': [('ASP_m', 'abcd'), ('AKG_m', 'efghi')],
        'pro': [('OAC_m', 'abcd'), ('GLU_m', 'efghi')],
        'reverse': True
    },
    {
        'id': 'AS_c',
        'sub': [('ASP_c', 'abcd'), ('GLN_c', 'efghi')],
        'pro': [('ASN_c', 'abcd'), ('GLU_c', 'efghi')],
    },
    {
        'id': 'ASPTA_c',
        'sub': [('ASP_c', 'abcd'), ('AKG_c', 'efghi')],
        'pro': [('OAC_c', 'abcd'), ('GLU_c', 'efghi')],
        'reverse': True
    },
]

ala_reaction_list = [
    {
        'id': 'ALA_input',
        'sub': [('ALA_e', 'abc')],
        'pro': [('ALA_c', 'abc')],
    },
    {
        'id': 'GPT_c',
        'sub': [('PYR_c', 'abc'), ('GLU_c', 'defgh')],
        'pro': [('ALA_c', 'abc'), ('AKG_c', 'defgh')],
        'reverse': True
    },
]

ppp_reaction_list = [
    {
        'id': 'G6PDH2R_PGL_GND_c',
        'sub': [('GLC6P_c', 'abcdef')],
        'pro': [('RUL5P_c', 'bcdef'), ('CO2', 'a')],
    },
    {
        'id': 'RPI_c',
        'sub': [('RUL5P_c', 'abcde')],
        'pro': [('RIB5P_c', 'abcde')],
        'reverse': True
    },
    {
        'id': 'RPE_c',
        'sub': [('RUL5P_c', 'abcde')],
        'pro': [('XYL5P_c', 'abcde')],
        'reverse': True
    },
    {
        'id': 'TKT1_c',
        'sub': [('XYL5P_c', 'abcde'), ('RIB5P_c', 'fghij')],
        'pro': [('GAP_c', 'cde'), ('SED7P_c', 'abfghij')],
        'reverse': True
    },
    {
        'id': 'TKT2_c',
        'sub': [('XYL5P_c', 'abcde'), ('E4P_c', 'fghi')],
        'pro': [('GAP_c', 'cde'), ('FRU6P_c', 'abfghi')],
        'reverse': True
    },
    {
        'id': 'TALA_c',
        'sub': [('SED7P_c', 'abcdefg'), ('GAP_c', 'hij')],
        'pro': [('FRU6P_c', 'abchij'), ('E4P_c', 'defg')],
        'reverse': True
    },
    {
        'id': 'Salvage_c',
        'sub': [('RIB5P_stock', 'abcde')],
        'pro': [('RIB5P_c', 'abcde')],
    },
]


# All exchange reaction related to mitochondria will be put here.
exchange_reaction_list = [
    {
        'id': 'PYR_trans',
        'sub': [('PYR_c', 'abc')],
        'pro': [('PYR_m', 'abc')],
        'reverse': True
    },
    {
        'id': 'ASPGLU_m',
        'sub': [('ASP_m', 'abcd'), ('GLU_c', 'efghi')],
        'pro': [('ASP_c', 'abcd'), ('GLU_m', 'efghi')],
        'reverse': True
    },
    {
        'id': 'AKGMAL_m',
        'sub': [('MAL_c', 'abcd'), ('AKG_m', 'efghi')],
        'pro': [('MAL_m', 'abcd'), ('AKG_c', 'efghi')],
        'reverse': True
    },
    {
        'id': 'CIT_trans',
        'sub': [('MAL_m', 'abcd'), ('CIT_c', 'efghij')],
        'pro': [('MAL_c', 'abcd'), ('CIT_m', 'efghij')],
        'reverse': True
    },
    {
        'id': 'GLN_trans',
        'sub': [('GLN_c', 'abcde')],
        'pro': [('GLN_m', 'abcde')],
        'reverse': True
    },

    # If this flux is missed, the total flux network will be unbalanced. Guess it is because other transport pathway
    # of glutamate is not sufficient to transport large amount of glutamate from mitochondria to cytosol.
    {
        'id': 'GLU_trans',
        'sub': [('GLU_c', 'abcde')],
        'pro': [('GLU_m', 'abcde')],
        'reverse': True
    },
]

intake_secret_reaction_list = [
    {
        'id': 'GLC_input',
        'sub': [('GLC_e', 'abcdef')],
        'pro': [('GLC_c', 'abcdef')],
    },
    # The only difference in this model
    {
        'id': 'GLC_unlabelled_input',
        'sub': [('GLC_unlabelled_e', 'abcdef')],
        'pro': [('GLC_c', 'abcdef')],
    },
    {
        'id': 'GLN_input',
        'sub': [('GLN_e', 'abcde')],
        'pro': [('GLN_c', 'abcde')],
    },
    {
        'id': 'ASP_input',
        'sub': [('ASP_e', 'abcd')],
        'pro': [('ASP_c', 'abcd')],
    },
    {
        'id': 'LAC_output',
        'sub': [('LAC_c', 'abc')],
        'pro': [('LAC_e', 'abc')],
    },
]

biomass_reaction_list = [
    {
        'id': 'BIOMASS_REACTION',
        'sub': [
            ('ALA_c', '', 0.5360230145753),
            ('ASN_c', '', 0.0544398374178039),
            ('ASP_c', '', 3.12819681162304),
            ('GLN_c', '', 0.862662039082123),
            ('GLU_c', '', 0.757970044047885),
            ('SER_c', '', 0.167507192054781),
            ('GLY_c', '', 0.62815197020543),
            ('RIB5P_c', '', 0.12),
            ('ACCOA_lipid', '', 1.0)
            ],
        'pro': [('BIOMASS', '')],
    },
]

reaction_dict = {
    'glycolysis_reaction': glycolysis_reaction_list,
    'ser_gly_reaction': ser_gly_reaction_list,
    'tca_reaction': tca_reaction_list,
    'glu_reaction': glu_reaction_list,
    'ppp_reaction': ppp_reaction_list,
    'exchange_reaction': exchange_reaction_list,
    'intake_secret_reaction': intake_secret_reaction_list,
    'ala_reaction': ala_reaction_list,
    'biomass_reaction': biomass_reaction_list,
}

emu_excluded_metabolite_set = {
    'CO2', 'BIOMASS', 'GLC_e', 'GLN_e', 'GLC_unlabelled_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e', 'ACCOA_lipid',
    '1CTHF_c', 'RIB5P_stock'}

symmetrical_metabolite_set = {'SUC_m', 'FUM_m'}

balance_excluded_metabolite_set = emu_excluded_metabolite_set

added_input_metabolite_set = {'GLC_e'}

model_compartment_set = {'m', 'c', 'e'}

composite_reaction_list = [
    {
        'id': 'GLC_total_input',
        'comp': [('GLC_input', ), ('GLC_unlabelled_input', )],
        ModelKeyword.flux_range: add_range
    }
]
