# Model without TCA cycle
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
        'id': 'PDH_c',
        'sub': [('PYR_c', 'abc')],
        'pro': [('ACCOA_c', 'bc'), ('CO2', 'a')],
    },
    {
        'id': 'CS_c',
        'sub': [('OAC_c', 'abcd'), ('ACCOA_c', 'ef')],
        'pro': [('CIT_c', 'dcbafe')],
    },
    {
        'id': 'ACONT_c',
        'sub': [('CIT_c', 'abcdef')],
        'pro': [('ICIT_c', 'abcdef')],
        'reverse': True
    },
    {
        'id': 'ICDH_c',
        'sub': [('ICIT_c', 'abcdef')],
        'pro': [('AKG_c', 'abcef'), ('CO2', 'd')],
    },
    {
        'id': 'AKGD_c',
        'sub': [('AKG_c', 'abcde')],
        'pro': [('SUCCOA_c', 'bcde'), ('CO2', 'a')],
    },
    {
        'id': 'SUCOAS_c',
        'sub': [('SUCCOA_c', 'abcd')],
        'pro': [('SUC_c', 'abcd')],
    },
    {
        'id': 'SUCD_c',
        'sub': [('SUC_c', 'abcd')],
        'pro': [('FUM_c', 'abcd')],
        'reverse': True
    },
    {
        'id': 'FUMH_c',
        'sub': [('FUM_c', 'abcd')],
        'pro': [('MAL_c', 'abcd')],
        'reverse': True
    },
    {
        'id': 'MDH_c',
        'sub': [('MAL_c', 'abcd')],
        'pro': [('OAC_c', 'abcd')],
        'reverse': True
    },
    {
        'id': 'PC_c',
        'sub': [('PYR_c', 'abc'), ('CO2', 'd')],
        'pro': [('OAC_c', 'abcd')],
    },
]

glu_reaction_list = [
    {
        'id': 'GLUD_c',
        'sub': [('AKG_c', 'abcde')],
        'pro': [('GLU_c', 'abcde')],
        'reverse': True
    },
    {
        'id': 'GLND_c',
        'sub': [('GLN_c', 'abcde')],
        'pro': [('GLU_c', 'abcde')],
    },
    {
        'id': 'GLNS_c',
        'sub': [('GLU_c', 'abcde')],
        'pro': [('GLN_c', 'abcde')],
    },
    {
        'id': 'ASPTA_c',
        'sub': [('ASP_c', 'abcd'), ('AKG_c', 'efghi')],
        'pro': [('OAC_c', 'abcd'), ('GLU_c', 'efghi')],
        'reverse': True
    },
    {
        'id': 'AS_c',
        'sub': [('ASP_c', 'abcd'), ('GLN_c', 'efghi')],
        'pro': [('ASN_c', 'abcd'), ('GLU_c', 'efghi')],
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


intake_secret_reaction_list = [
    {
        'id': 'GLC_input',
        'sub': [('GLC_e', 'abcdef')],
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
    'intake_secret_reaction': intake_secret_reaction_list,
    'ala_reaction': ala_reaction_list,
    'biomass_reaction': biomass_reaction_list,
}

emu_excluded_metabolite_set = {
    'CO2', 'BIOMASS', 'GLC_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e', 'ACCOA_lipid',
    '1CTHF_c', 'RIB5P_stock'}

symmetrical_metabolite_set = {'SUC_c', 'FUM_c'}

balance_excluded_metabolite_set = emu_excluded_metabolite_set

added_input_metabolite_set = {'GLC_e'}

model_compartment_set = {'c', 'e'}

