from scripts.src.core.common.classes import TransformDict

model_reaction_to_standard_name_dict = TransformDict({
    # Glycolysis
    'HEX_c': 'Hexokinase',
    'PGI_c': 'Glucose-6-phosphate isomerase',
    'PFK_c': 'Phosphofructokinase-1',
    'FBA_c': 'Fructose-bisphosphate aldolase',
    'TPI_c': 'Triosephosphate isomerase',
    'GAPD_c': 'Glyceraldehyde-3-phosphate dehydrogenase',
    'PGK_c': 'Phosphoglycerate kinase',
    'PGM_c': 'Phosphoglycerate mutase',
    'ENO_c': 'Phosphopyruvate hydratase (enolase)',
    'PYK_c': 'Pyruvate kinase',
    'LDH_c': 'Lactate dehydrogenase',
    'PEPCK_c': 'Phosphoenolpyruvate carboxykinase',
    'ACITL_c': 'ATP citrate lyase',
    'MDH_c': 'Malate dehydrogenase (cytosol)',
    'ME2_c': 'NADP-malic enzyme',
    'LIPID_c': 'Lipid synthesis',

    # TCA
    'PDH_m': 'Pyruvate dehydrogenase (mitochondria)',
    'CS_m': 'Citrate synthase',
    'ACONT_m': 'Aconitase',
    'ICDH_m': 'Isocitrate dehydrogenase',
    'AKGD_m': 'α-Ketoglutarate dehydrogenase',
    'SUCOAS_m': 'Succinyl-CoA synthetase',
    'SUCD_m': 'Succinate dehydrogenase',
    'FUMH_m': 'Fumarase',
    'MDH_m': 'Malate dehydrogenase',
    'PC_m': 'Pyruvate carboxylase',

    # PPP
    'G6PDH2R_PGL_GND_c': 'Glucose 6-phosphate dehydrogenase/6-phosphogluconolactonase/6-phosphogluconate dehydrogenase',
    'RPI_c': 'Ribose-5-phosphate isomerase',
    'RPE_c': 'Ribulose 5-phosphate 3-epimerase',
    'TKT1_c': 'Transketolase',
    'TKT2_c': 'Transketolase',
    'TALA_c': 'Transaldolase',
    'Salvage_c': 'Salvage pathway of ribose 5-phosphate',

    # Ser-Gly
    'PHGDH_PSAT_PSP_c': 'Phosphoglycerate dehydrogenase/phosphoserine aminotransferase/phosphoserine phosphatase',
    'SHMT_c': 'Serine hydroxymethyltransferase (cytosol)',
    'SER_input': 'Serine input flux',
    'GLY_input': 'Glycine input flux',

    # Glu
    'GLUD_m': 'Glutamate dehydrogenase (mitochondria)',
    'GLND_m': 'Glutaminase (mitochondria)',
    'GLNS_c': 'Glutamine synthetase',
    'ASPTA_m': 'Aspartate transaminase (mitochondria)',
    'AS_c': 'Asparagine synthetase (cytosol)',
    'ASPTA_c': 'Aspartate transaminase (cytosol)',

    # Ala
    'ALA_input': 'Alanine input',
    'GPT_c': 'Glutamate-pyruvate transaminase',

    # Exchange
    'PYR_trans': 'Pyruvate transport (cytosol and mitochondria)',
    'ASPGLU_m': 'Glutamate aspartate transporter',
    'AKGMAL_m': 'Mitochondrial a-ketoglutarate/malate carrier',
    'CIT_trans': 'Citrate/malate antiporter',
    'GLN_trans': 'Glutamine transport (cytosol and mitochondria)',
    'GLU_trans': 'Glutamate transport (cytosol and mitochondria)',

    'GLC_input': 'Glucose input',
    'GLN_input': 'Glutamine input',
    'ASP_input': 'Aspartate input',
    'LAC_output': 'Lactate output',

    # Biomass
    'BIOMASS_REACTION': 'Biomass reaction',

    # supplement
    'GLC_supplement': 'Glucose supplement',
    'CIT_supplement': 'Citrate supplement',
})
