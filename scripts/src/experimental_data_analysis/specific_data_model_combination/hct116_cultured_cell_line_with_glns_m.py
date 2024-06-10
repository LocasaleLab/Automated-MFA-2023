from .hct116_cultured_cell_line import (
    data_wrap_obj, SpecificParameter, total_param_list, experimental_data_plotting, keyword_list,
    collect_results, project_name_generator,
)

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

user_defined_model = model_loader(ModelList.base_model_with_glns_m)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'hct116_cultured_cell_line_with_glns_m'


important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    ('PGM_c', 'PGM_c__R'),
    'Salvage_c',
    'PC_m',
    'G6PDH2R_PGL_GND_c',
    'PDH_m',
    'CS_m',
    'AKGD_m',
    'ICDH_m',
    'PYK_c',
    'ACITL_c',
    ('SUCD_m', 'SUCD_m__R'),
    ('FUMH_m', 'FUMH_m__R'),
    ('MDH_m', 'MDH_m__R'),
    ('GPT_c', 'GPT_c__R'),
    'PHGDH_PSAT_PSP_c',
    ('LDH_c', 'LDH_c__R'),
    'GLN_input',
    'GLNS_m',
    'GLNS_c',
]


