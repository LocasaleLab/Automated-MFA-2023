from scripts.src.common.config import Color, Keywords, Direct, DataType
from scripts.src.common.functions import data_param_list_generator_func_template, collect_results_func_template, \
    special_result_label_converter
from scripts.src.common.result_processing_functions import experimental_data_plotting_func_template

from scripts.data.common_functions import common_data_loader

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

data_wrap_obj, keyword = common_data_loader(
    DataType.hct116_cultured_cell_line, test_mode=False, natural_anti_correction=False)
user_defined_model = model_loader(ModelList.base_model)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'hct116_cultured_cell_line'
output_folder = '{}/{}'.format(Direct.output_direct, name)
raw_data_folder = '{}/{}'.format(output_folder, Direct.raw_flux_analysis)
obj_threshold_key = Keywords.obj_threshold_key


class SpecificParameter(object):
    test_dynamic_constant_flux_list = []
    test_preset_constant_flux_value_dict = {
        'GLC_input': 200,
    }
    specific_flux_range_dict = {
        # 'ASP_input': (1, 150),
        # 'GLN_input': (1, 100)
    }


complete_data_param_raw_list = [
    {
        keyword.experiments: 'HCT116_WQ2101',
        '': [
            {
                keyword.condition: keyword.ctrl,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 1,
                        obj_threshold_key: Keywords.unoptimized
                    },
                    {
                        keyword.index: 1,
                        Keywords.loss: Keywords.squared_loss
                    },
                ]
            },
        ]
    }
]

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
]


data_param_raw_list = complete_data_param_raw_list
# total_param_list_old = data_param_list_generator(data_param_raw_list)
short_keyword_list = [keyword.experiments, keyword.condition, keyword.index]
total_param_list = data_param_list_generator_func_template(
    short_keyword_list, extra_key_default_value_dict={
        obj_threshold_key: None, Keywords.loss: None})(data_param_raw_list)


def project_name_generator(
        tissue_name, tissue_index, repeat_index, unoptimized_key=None, loss_key=None):
    base_name = data_wrap_obj.project_name_generator(tissue_name, tissue_index, repeat_index)
    if unoptimized_key is not None and unoptimized_key == Keywords.unoptimized:
        base_name = special_result_label_converter(base_name, Keywords.unoptimized)
    if loss_key is not None and loss_key == Keywords.squared_loss:
        base_name = special_result_label_converter(base_name, Keywords.squared_loss)
    return base_name


keyword_list = [*short_keyword_list, obj_threshold_key, Keywords.loss]


collect_results = collect_results_func_template(
    project_name_generator, total_param_list, keyword_list)


target_emu_name_nested_list = [
    ['glucose', 'fructose 1,6-bisphosphate', 'glyceraldehyde 3-phosphate', 'dihydroxyacetone phosphate'],
    ['3-phosphoglycerate', 'phosphoenolpyruvate', 'pyruvate', 'lactate'],
    ['a-ketoglutarate', 'glutamate', 'glutamine', 'aspartate']
]


def major_minor_key_analysis_func(result_information_dict):
    cell_line = result_information_dict[keyword.cell_line]
    glucose_level = result_information_dict[keyword.glucose_level]
    index = result_information_dict[keyword.index]
    glucose_level_index_str = f'{glucose_level}_{index}'
    major_key = cell_line
    minor_key_list = [glucose_level, index]
    minor_key_str = glucose_level_index_str
    if glucose_level == keyword.high_glucose_level:
        current_color = Color.blue
    elif glucose_level == keyword.low_glucose_level:
        current_color = Color.orange
    else:
        raise ValueError()
    return major_key, minor_key_list, minor_key_str, current_color, 0


experimental_data_plotting = experimental_data_plotting_func_template(
    target_emu_name_nested_list, major_minor_key_analysis_func,
    major_key_file_name_func=lambda cell_line: f'target_metabolites_{cell_line}')

