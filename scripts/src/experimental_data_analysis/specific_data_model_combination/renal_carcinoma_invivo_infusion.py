from scripts.src.common.config import Color, Keywords, Direct, DataType
from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from scripts.src.common.plotting_functions import multi_row_col_bar_plot

from scripts.data.common_functions import common_data_loader

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

from ...common.result_processing_functions import common_flux_comparison_func

data_wrap_obj, keyword = common_data_loader(DataType.renal_carcinoma, test_mode=False, natural_anti_correction=True)
# user_defined_model = model_loader(ModelList.invivo_infusion_model)
user_defined_model = model_loader(ModelList.base_model_with_glc_tca_buffer)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'renal_carcinoma_invivo_infusion'
# output_folder = '{}/{}'.format(Direct.output_direct, name)
# raw_data_folder = '{}/{}'.format(output_folder, Direct.raw_flux_analysis_direct)


class SpecificParameter(object):
    test_dynamic_constant_flux_list = []
    test_preset_constant_flux_value_dict = {
        # 'GLC_total_input': 100,
        'GLC_supplement_net': 0,
        'CIT_supplement_net': 0,
        # 'GLN_input': 80,
        'ASP_input': 50,
        # 'SER_input': 8,
        # 'ALA_input': 20,
        # 'OAC_supplement_net': 0,
    }
    specific_flux_range_dict = {
        'Salvage_c': (1, 10),
    }


test_data_param_raw_list = [
    {
        keyword.tissue: keyword.kidney,
        '': [
            {
                keyword.patient: 1,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                ]
            }]
    }
]

complete_data_param_raw_list = [
    {
        keyword.tissue: keyword.kidney,
        '': [
            {
                keyword.patient: 1,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 2,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 3,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 4,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 5,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
        ]
    },
    {
        keyword.tissue: keyword.carcinoma,
        '': [
            {
                keyword.patient: 1,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 2,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 3,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 4,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 5,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
        ]
    },
    {
        keyword.tissue: keyword.brain,
        '': [
            {
                keyword.patient: 1,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 2,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 3,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 4,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
            {
                keyword.patient: 5,
                '': [
                    # {
                    #     keyword.index: 1,
                    # },
                    # {
                    #     keyword.index: 2,
                    # },
                    # {
                    #     keyword.index: 3,
                    # },
                    {
                        keyword.index: Keywords.average,
                    },
                ]
            },
        ]},
]

important_flux_list = [
    # 'GLC_unlabelled_input',
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
    ('AKGMAL_m__R', 'AKGMAL_m')
]


mid_name_list = [
    ['3PG_c', 'SER_c', 'PYR_c+PYR_m', 'LAC_c'],
    ['ALA_c', 'CIT_c+CIT_m', 'SUC_m', 'FUM_m'],
    ['MAL_c+MAL_m', 'GLU_c+GLU_m', 'GLN_c+GLN_m', 'ASP_c+ASP_m']
]


def data_param_list_generator(param_raw_list):
    current_param_list = []
    for labeling_param_dict in param_raw_list:
        labeling_key = labeling_param_dict[keyword.tissue]
        labeling_content_list = labeling_param_dict['']
        for type_param_dict in labeling_content_list:
            type_key = type_param_dict[keyword.patient]
            type_content_list = type_param_dict['']
            for index_param_dict in type_content_list:
                index_key = index_param_dict[keyword.index]
                current_param_list.append({
                    keyword.tissue: labeling_key,
                    keyword.patient: type_key,
                    keyword.index: index_key,
                    Keywords.obj_threshold_key: None
                })
    return current_param_list


data_param_raw_list = complete_data_param_raw_list
total_param_list = data_param_list_generator(data_param_raw_list)


def collect_results(final_data_obj):
    final_mapping_dict = {}
    for param_dict in total_param_list:
        tissue_key = param_dict[keyword.tissue]
        patient_key = param_dict[keyword.patient]
        index_key = param_dict[keyword.index]
        project_name = data_wrap_obj.project_name_generator(tissue_key, patient_key, index_key)
        final_mapping_dict[project_name] = (tissue_key, patient_key, index_key)
        final_data_obj.load_current_result_label(project_name)
        if Keywords.obj_threshold_key in final_data_obj.final_information_dict[project_name]:
            del final_data_obj.final_information_dict[project_name][Keywords.obj_threshold_key]
    return final_mapping_dict


def experimental_results_comparison_parameter_generator(target_metabolite_data_dict):
    final_color_dict = {}
    final_data_dict_for_plotting = {}
    for labeling_key, each_labeling_data_dict in target_metabolite_data_dict.items():
        data_dict_for_plotting = {}
        color_dict = {}
        for type_key, each_type_data_dict in each_labeling_data_dict.items():
            for index_key, each_index_data_dict in each_type_data_dict.items():
                current_type_index_name = '{}_{}'.format(type_key, index_key)
                if current_type_index_name not in color_dict:
                    if type_key == 1:
                        current_color = Color.blue
                    elif type_key == 2:
                        current_color = Color.orange
                    else:
                        raise ValueError()
                    color_dict[current_type_index_name] = current_color
                for metabolite_name, each_metabolite_data_obj in each_index_data_dict.items():
                    if metabolite_name not in data_dict_for_plotting:
                        data_dict_for_plotting[metabolite_name] = {}
                    data_dict_for_plotting[metabolite_name][current_type_index_name] = \
                        each_metabolite_data_obj.data_vector
        final_data_dict_for_plotting[labeling_key] = data_dict_for_plotting
        final_color_dict[labeling_key] = color_dict
    return keyword.output_folder, final_data_dict_for_plotting, final_color_dict


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


def experimental_data_plotting(
        complete_experimental_mid_data_obj_dict, complete_result_information_dict, output_direct):
    mid_data_dict_for_plotting = {}
    raw_data_dict_for_plotting = {}
    color_dict = {}
    patient_color_dict = {}
    complete_color_list = [Color.blue, Color.orange, Color.purple]
    for result_label, experimental_mid_data_obj_dict in complete_experimental_mid_data_obj_dict.items():
        result_information_dict = complete_result_information_dict[result_label]
        tissue = result_information_dict[keyword.tissue]
        patient = result_information_dict[keyword.patient]
        index = result_information_dict[keyword.index]
        if index == Keywords.average:
            continue
        if tissue not in mid_data_dict_for_plotting:
            mid_data_dict_for_plotting[tissue] = {}
            raw_data_dict_for_plotting[tissue] = {}
        for metabolite_name, mid_data_obj in experimental_mid_data_obj_dict.items():
            current_mid_label_tissue_dict = mid_data_dict_for_plotting[tissue]
            current_raw_label_tissue_dict = raw_data_dict_for_plotting[tissue]
            if metabolite_name not in current_mid_label_tissue_dict:
                current_mid_label_tissue_dict[metabolite_name] = {}
                current_raw_label_tissue_dict[metabolite_name] = {}
            patient_index_str = f'{patient}_{index}'
            current_mid_label_tissue_dict[metabolite_name][patient_index_str] = mid_data_obj.data_vector
            current_raw_label_tissue_dict[metabolite_name][patient_index_str] = mid_data_obj.raw_data_vector
            if patient_index_str not in color_dict:
                if patient not in patient_color_dict:
                    current_color = complete_color_list[len(patient_color_dict) % 3]
                    patient_color_dict[patient] = current_color
                color_dict[patient_index_str] = patient_color_dict[patient]
    target_emu_name_nested_list = [
        ['glucose', '3-phosphoglycerate', 'pyruvate', 'lactate'],
        ['alanine', 'citrate', 'succinate', 'fumarate'],
        ['malate', 'aspartate', 'glutamate', 'glutamine'],
    ]
    target_row_num = len(target_emu_name_nested_list)
    target_col_num = len(target_emu_name_nested_list[0])
    for tissue, each_tissue_mid_data_dict_for_plotting in mid_data_dict_for_plotting.items():
        each_tissue_raw_data_dict_for_plotting = raw_data_dict_for_plotting[tissue]
        for raw_data in (False, True):
            if raw_data:
                parent_direct = 'raw_data'
                complete_data_dict = each_tissue_raw_data_dict_for_plotting
                ylim = (0, None)
            else:
                parent_direct = 'mid_data'
                complete_data_dict = each_tissue_mid_data_dict_for_plotting
                ylim = (0, 1)
            current_title = f'{tissue}'
            current_output_direct = '{}/{}'.format(output_direct, parent_direct)
            check_and_mkdir_of_direct(current_output_direct)
            multi_row_col_bar_plot(
                complete_data_dict, target_emu_name_nested_list, target_row_num, target_col_num,
                error_bar_data_dict=None, color_dict=color_dict, title_dict=None,
                output_direct=current_output_direct, current_title=current_title, ylim=ylim,
                xlabel_list=None, figsize=None, legend=False)


def result_output_dataframe_dict_generator(complete_result_dict):
    pass
    # return {'Sheet1': pd.DataFrame()}


def metabolic_network_parameter_generator():
    experimental_mid_metabolite_set = {
        'PYR_c', 'PYR_m',
        'LAC_c',
        'ALA_c',
        'SUC_m',
        'FUM_m',
        'SER_c',
        'MAL_c', 'MAL_m',
        'ASP_c', 'ASP_m',
        'GLU_c', 'GLU_m',
        'GLN_c', 'GLN_m',
        'CIT_c', 'CIT_m',
        '3PG_c',
    }
    experimental_mixed_mid_metabolite_set = {
        'PYR_c', 'PYR_m',
        'MAL_c', 'MAL_m',
        'ASP_c', 'ASP_m',
        'GLU_c', 'GLU_m',
        'GLN_c', 'GLN_m',
        'CIT_c', 'CIT_m',
    }
    biomass_metabolite_set = {
        'ALA_c', 'RIB5P_c', 'GLY_c', 'SER_c', 'ASP_c',
        'ACCOA_c', 'GLU_c', 'GLN_c',
    }
    input_metabolite_set = {
        'GLC_e', 'GLC_unlabelled_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e',
    }
    c13_labeling_metabolite_set = {
        'GLC_e',
    }
    boundary_flux_set = {
        'GLC_input', 'GLC_unlabelled_input'
    }
    infusion = False
    return experimental_mid_metabolite_set, experimental_mixed_mid_metabolite_set, biomass_metabolite_set, \
        input_metabolite_set, c13_labeling_metabolite_set, boundary_flux_set, infusion
