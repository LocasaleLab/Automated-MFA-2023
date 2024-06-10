from .colon_cancer_cell_line import *
from .colon_cancer_cell_line import total_param_list as raw_total_param_list, \
    project_name_generator as raw_project_name_generator, special_result_label_converter, \
    keyword_list as raw_keyword_list
import os

user_defined_model = model_loader(ModelList.base_model_with_glns_m)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'colon_cancer_cell_line_with_glns_m'

if 'PART' in os.environ:
    part_value = os.environ['PART']
    if part_value == '0':
        total_param_list = raw_total_param_list[:5]
    elif part_value == '1':
        total_param_list = raw_total_param_list[5:8]
    elif part_value == '2':
        total_param_list = raw_total_param_list[8:11]
    else:
        total_param_list = raw_total_param_list[11:]
else:
    total_param_list = raw_total_param_list


def project_name_generator(
        cell_line, glucose_level, repeat_index, loss_key=None):
    base_name = raw_project_name_generator(cell_line, glucose_level, repeat_index)
    if loss_key is not None and loss_key == Keywords.squared_loss:
        base_name = special_result_label_converter(base_name, Keywords.squared_loss)
    return base_name


# Generate tissue to result_label mapping dict
collect_results = collect_results_func_template(project_name_generator, total_param_list, keyword_list)


important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    'PC_m',
    'G6PDH2R_PGL_GND_c',
    'PDH_m',
    'CS_m',
    'AKGD_m',
    'ICDH_m',
    'PYK_c',
    ('SUCD_m', 'SUCD_m__R'),
    ('FUMH_m', 'FUMH_m__R'),
    ('CIT_trans__R', 'CIT_trans'),
    ('MDH_c', 'MDH_c__R'),
    ('MDH_m', 'MDH_m__R'),
    ('GPT_c', 'GPT_c__R'),
    'PHGDH_PSAT_PSP_c',
    ('LDH_c', 'LDH_c__R'),
    'Salvage_c',
    'ACITL_c',
    'PEPCK_c',
    ('GAPD_c', 'GAPD_c__R'),
    'GLC_input',
    'GLN_input',
    ('SHMT_c', 'SHMT_c__R'),
    ('AKGMAL_m__R', 'AKGMAL_m'),
    'GLNS_m',
    'GLNS_c',
]


def flux_comparison_parameter_generator(final_solution_data_dict, final_flux_name_index_dict):
    from ...common.config import index_calculation_func_dict
    current_index_name_func_dict = index_calculation_func_dict
    current_important_flux_list = list(important_flux_list)
    if current_index_name_func_dict is not None:
        current_important_flux_list.extend(current_index_name_func_dict.items())

    final_dict_for_comparison = {}
    final_key_name_parameter_dict = {}
    final_color_dict = {}
    comparison_dict = {
        keyword.high_low_glucose: [keyword.high_glucose_level, keyword.low_glucose_level]
    }
    for comparison_name, current_glucose_level_list in comparison_dict.items():
        key_name_parameter_dict = {}
        data_dict_for_plotting = {}
        color_dict = {}
        for cell_line_key, current_cell_line_dict in final_solution_data_dict.items():
            for glucose_level_index, glucose_level in enumerate(current_glucose_level_list):
                for index_num, current_data_array in current_cell_line_dict[glucose_level].items():
                    key_name = '{}_{}_{}'.format(cell_line_key, glucose_level, index_num)
                    key_name_parameter_dict[key_name] = (cell_line_key, glucose_level, index_num)
                    if glucose_level_index == 0:
                        current_color = Color.blue
                    else:
                        current_color = Color.orange
                    if key_name not in color_dict:
                        color_dict[key_name] = current_color
                    common_flux_comparison_func(
                        current_important_flux_list,
                        final_flux_name_index_dict[cell_line_key][glucose_level][index_num], current_data_array,
                        data_dict_for_plotting, key_name)
        final_dict_for_comparison[comparison_name] = data_dict_for_plotting
        final_color_dict[comparison_name] = color_dict
        final_key_name_parameter_dict[comparison_name] = key_name_parameter_dict
    return final_dict_for_comparison, final_key_name_parameter_dict, final_color_dict
