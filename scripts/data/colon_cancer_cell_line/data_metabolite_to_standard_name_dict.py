from scripts.src.core.common.classes import TransformDict

data_metabolite_to_standard_name_dict = TransformDict({
    '(r,s)-lactate': 'lactate',
    '(s)-malate': 'malate',
    '2-oxoglutarate': 'a-ketoglutarate',

    'd-glucose': 'glucose',
    'g6p': 'glucose 6-phosphate',
    'f6p': 'fructose 6-phosphate',
    'fructose-1,6-bisphosphate': 'fructose 1,6-bisphosphate',
    'fructose-16-bisphosphate': 'fructose 1,6-bisphosphate',
    'dihydroxy-acetone-phosphate': 'dihydroxyacetone phosphate',
    'd-glyceraldehdye-3-phosphate': 'glyceraldehyde 3-phosphate',
    '3pg': '3-phosphoglycerate',
    '2pg': '2-phosphoglycerate',

    'd-ribose-5-phosphate': 'ribose 5-phosphate',
    'd-sedoheptulose-7-phosphate': 'sedoheptulose 7-phosphate',
    'd-erythrose-4-phosphate': 'erythrose 4-phosphate',
    'd-erythrose 4-phosphate': 'erythrose 4-phosphate',

    'l-lysine': 'lysine',
    'l-tryptophan': 'tryptophan',
    'l-isoleucine': 'isoleucine',
    'l-leucine': 'leucine',
    'l-glutamate': 'glutamate',
    'd-aspartate': 'aspartate',
})
