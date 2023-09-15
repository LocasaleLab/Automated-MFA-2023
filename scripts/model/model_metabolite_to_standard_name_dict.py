from scripts.src.core.common.classes import TransformDict

model_metabolite_to_standard_name_dict = TransformDict({
    # Glycolysis
    'GLC': 'glucose',
    'GLC6P': 'glucose 6-phosphate',
    'FRU6P': 'fructose 6-phosphate',
    'FRU16BP': 'fructose 1,6-bisphosphate',
    'DHAP': 'dihydroxyacetone phosphate',
    'GAP': 'glyceraldehyde 3-phosphate',
    'BPG13': '1,3-bisphosphoglycerate',
    '3PG': '3-phosphoglycerate',
    '2PG': '2-phosphoglycerate',
    'PEP': 'phosphoenolpyruvate',
    'PYR': 'pyruvate',
    'LAC': 'lactate',

    # TCA
    'OAC': 'oxaloacetate',
    'ACCOA': 'acetyl-coa',
    'CIT': 'citrate',
    'ICIT': 'isocitrate',
    'SUCCOA': 'succinyl-coa',
    'SUC': 'succinate',
    'FUM': 'fumarate',
    'MAL': 'malate',
    'AKG': 'a-ketoglutarate',

    # PPP
    'RIB5P': 'ribose 5-phosphate',
    'XYL5P': 'xylose 5-phosphate',
    'SED7P': 'sedoheptulose 7-phosphate',
    'E4P': 'erythrose 4-phosphate',
    'RUL5P': 'ribulose 5-phosphate',

    # AAs
    'ALA': 'alanine',
    'ASN': 'asparagine',
    'ASP': 'aspartate',
    'GLN': 'glutamine',
    'GLU': 'glutamate',
    'GLY': 'glycine',
    'PRO': 'proline',
    'SER': 'serine',
})
