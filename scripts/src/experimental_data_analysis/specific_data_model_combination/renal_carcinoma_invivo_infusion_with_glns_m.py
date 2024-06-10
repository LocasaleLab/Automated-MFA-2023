from .renal_carcinoma_invivo_infusion import *
from .renal_carcinoma_invivo_infusion import total_param_list as raw_total_param_list, \
    project_name_generator as raw_project_name_generator, \
    keyword_list as raw_keyword_list
import os

user_defined_model = model_loader(ModelList.base_model_with_glc_tca_buffer_glns_m)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'renal_carcinoma_invivo_infusion_with_glns_m'

if 'PART' in os.environ:
    if os.environ['PART'] == '0':
        total_param_list = raw_total_param_list[:7]
    else:
        total_param_list = raw_total_param_list[7:]
else:
    total_param_list = raw_total_param_list


def project_name_generator(
        tissue_name, tissue_index, repeat_index, loss_key=None):
    base_name = raw_project_name_generator(tissue_name, tissue_index, repeat_index)
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
    final_dict_for_flux_comparison_plotting = {}
    final_key_name_parameter_dict = {}
    final_color_dict = {}
    comparison_name_tissue_dict = {
        'kidney_tumor_vs_brain': [keyword.carcinoma, keyword.brain],
        'tumor_vs_kidney': [keyword.kidney, keyword.carcinoma]}
    current_important_flux_list = list(important_flux_list)
    if current_index_name_func_dict is not None:
        current_important_flux_list.extend(current_index_name_func_dict.items())
    patient_key_set = set()
    for comparison_name, current_tissue_name_list in comparison_name_tissue_dict.items():
        data_dict_for_plotting = {}
        key_name_parameter_dict = {}
        color_dict = {}
        data_dict_order_list = []
        if comparison_name == 'kidney_tumor_vs_brain':
            for tissue_index, tissue_name in enumerate(current_tissue_name_list):
                for patient_key, current_patient_dict in final_solution_data_dict[tissue_name].items():
                    if patient_key not in patient_key_set:
                        patient_key_set.add(patient_key)
                    current_flux_name_index_dict = final_flux_name_index_dict[tissue_name][patient_key]
                    data_dict_order_list.append(
                        (tissue_index, tissue_name, patient_key, current_patient_dict, current_flux_name_index_dict))
        elif comparison_name == 'tumor_vs_kidney':
            for patient_key in patient_key_set:
                for tissue_index, tissue_name in enumerate(current_tissue_name_list):
                    current_patient_dict = final_solution_data_dict[tissue_name][patient_key]
                    current_flux_name_index_dict = final_flux_name_index_dict[tissue_name][patient_key]
                    data_dict_order_list.append(
                        (tissue_index, tissue_name, patient_key, current_patient_dict, current_flux_name_index_dict))
        else:
            raise ValueError()
        for tissue_index, tissue_name, patient_key, current_patient_dict, current_flux_name_index_dict in data_dict_order_list:
            for index_num, current_data_array in current_patient_dict.items():
                key_name = '{}_{}_{}'.format(tissue_name, patient_key, index_num)
                key_name_parameter_dict[key_name] = (tissue_name, patient_key, index_num)
                if tissue_index == 0:
                    color_dict[key_name] = Color.blue
                else:
                    color_dict[key_name] = Color.orange
                common_flux_comparison_func(
                    current_important_flux_list, current_flux_name_index_dict[index_num], current_data_array,
                    data_dict_for_plotting, key_name)
        final_dict_for_flux_comparison_plotting[comparison_name] = data_dict_for_plotting
        final_key_name_parameter_dict[comparison_name] = key_name_parameter_dict
        final_color_dict[comparison_name] = color_dict
    return final_dict_for_flux_comparison_plotting, final_key_name_parameter_dict, final_color_dict

