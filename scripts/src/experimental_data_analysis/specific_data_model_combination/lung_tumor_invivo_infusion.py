from scripts.src.common.config import Color, Keywords, Direct, DataType
from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from scripts.src.common.plotting_functions import multi_row_col_bar_plot
from scripts.src.common.functions import data_param_list_generator_func_template, collect_results_func_template, \
    special_result_label_converter

from scripts.data.common_functions import common_data_loader

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

from ...common.result_processing_functions import common_flux_comparison_func

data_wrap_obj, keyword = common_data_loader(DataType.lung_tumor, test_mode=False, natural_anti_correction=True)
# invivo_infusion_model = model_loader(ModelList.invivo_infusion_model)
user_defined_model = model_loader(ModelList.base_model_with_glc_tca_buffer)
mfa_model_obj = common_model_constructor(user_defined_model)

name = 'lung_tumor_invivo_infusion'
# output_folder = '{}/{}'.format(Direct.output_direct, name)
# raw_data_folder = '{}/{}'.format(output_folder, Direct.raw_flux_analysis)
multi_tumor_comparison = True


class SpecificParameter(object):
    test_dynamic_constant_flux_list = []
    test_preset_constant_flux_value_dict = {
        # 'GLC_total_input': 100,
        'GLC_supplement_net': 0,
        'CIT_supplement_net': 0,
        # 'GLC_input': 100,
        # 'GLN_input': 80,
        'ASP_input': 50,
        # 'SER_input': 8,
        # 'ALA_input': 20,
    }
    specific_flux_range_dict = {
        'Salvage_c': (1, 10)
    }


average_data_param_raw_list = [
    {
        keyword.experiments: keyword.human,
        '': [
            {
                keyword.patient: 'K1028',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1029',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1030',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1031',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1032',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1033',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1034',
                '': [
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1035',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1038',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1039',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1044',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1050',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1051',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1053',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1055',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1058',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1059',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
            {
                keyword.patient: 'K1060',
                '': [
                    {
                        keyword.tissue: keyword.lung,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                    {
                        keyword.tissue: keyword.tumor,
                        '': [
                            {
                                keyword.index: Keywords.average,
                            },
                        ]
                    },
                ],
            },
        ]
    },
]


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
    ('AKGMAL_m__R', 'AKGMAL_m')
]


mid_name_list = [
    ['GLC_c', '3PG_c', 'PYR_c+PYR_m', 'LAC_c'],
    ['ALA_c', 'CIT_c+CIT_m', 'MAL_c+MAL_m'],
    ['GLU_c+GLU_m', 'GLN_c+GLN_m', 'ASP_c+ASP_m']
]


def data_param_list_generator(param_raw_list):
    current_param_list = []
    for raw_param_dict in param_raw_list:
        experiments_key = raw_param_dict[keyword.experiments]
        experiment_content_list = raw_param_dict['']
        if experiments_key != keyword.human:
            experiment_content_list = [{keyword.patient: None, '': experiment_content_list}]
        for experiment_content_dict in experiment_content_list:
            patient_key = experiment_content_dict[keyword.patient]
            tissue_content_list = experiment_content_dict['']
            for type_param_dict in tissue_content_list:
                type_key = type_param_dict[keyword.tissue]
                type_content_list = type_param_dict['']
                for index_param_dict in type_content_list:
                    index_key = index_param_dict[keyword.index]
                    new_param_dict = {
                        keyword.experiments: experiments_key,
                        keyword.tissue: type_key,
                        keyword.index: index_key,
                        Keywords.obj_threshold_key: None
                    }
                    if patient_key is not None:
                        new_param_dict[keyword.patient] = patient_key
                    current_param_list.append(new_param_dict)
    return current_param_list


# data_param_raw_list = complete_data_param_raw_list
data_param_raw_list = average_data_param_raw_list
# total_param_list = data_param_list_generator(data_param_raw_list)
keyword_list = [keyword.experiments, keyword.patient, keyword.tissue, keyword.index]
total_param_list = data_param_list_generator_func_template(keyword_list)(average_data_param_raw_list)


def project_name_generator(experiment_name, patient_id, tissue_name, repeat_index):
    return data_wrap_obj.project_name_generator(experiment_name, tissue_name, repeat_index, patient_id)


collect_results = collect_results_func_template(project_name_generator, total_param_list, keyword_list)


def flux_comparison_parameter_generator(final_solution_data_dict, final_flux_name_index_dict):
    from ...common.config import index_calculation_func_dict
    current_index_name_func_dict = index_calculation_func_dict
    current_important_flux_list = list(important_flux_list)
    if current_index_name_func_dict is not None:
        current_important_flux_list.extend(current_index_name_func_dict.items())

    final_dict_for_flux_comparison_plotting = {}
    final_key_name_parameter_dict = {}
    final_color_dict = {}
    comparison_name_tissue_dict = {
        keyword.human: [keyword.lung, keyword.tumor],
        # keyword.mouse_lung_vs_tumor: [keyword.lung, keyword.flank, keyword.tumor],
        # keyword.mouse_tumor_ko: [keyword.hcc15, keyword.mct1ko, keyword.mct4ko]
    }
    for comparison_name, current_tissue_name_list in comparison_name_tissue_dict.items():
        data_dict_for_plotting = {}
        key_name_parameter_dict = {}
        color_dict = {}
        data_dict_order_list = []
        if comparison_name == keyword.human:
            for patient_key, current_patient_dict in final_solution_data_dict[comparison_name].items():
                for tissue_index, tissue_name in enumerate(current_tissue_name_list):
                    try:
                        current_tissue_dict = current_patient_dict[tissue_name]
                    except KeyError:
                        continue
                    current_flux_name_index_dict = final_flux_name_index_dict[comparison_name][patient_key][tissue_name]
                    data_dict_order_list.append(
                        (tissue_index, tissue_name, patient_key, current_tissue_dict, current_flux_name_index_dict))
        else:
            for tissue_index, tissue_name in enumerate(current_tissue_name_list):
                current_tissue_dict = final_solution_data_dict[comparison_name][keyword.empty_patient_key][tissue_name]
                current_flux_name_index_dict = final_flux_name_index_dict[comparison_name][keyword.empty_patient_key][
                    tissue_name]
                data_dict_order_list.append(
                    (tissue_index, tissue_name, '', current_tissue_dict, current_flux_name_index_dict))
        for tissue_index, tissue_name, patient_key, current_tissue_dict, current_flux_name_index_dict in data_dict_order_list:
            for index_num, current_data_array in current_tissue_dict.items():
                key_name = '{}_{}_{}'.format(tissue_name, patient_key, index_num)
                key_name_parameter_dict[key_name] = (tissue_name, patient_key, index_num)
                if tissue_index == 0:
                    color_dict[key_name] = Color.blue
                elif tissue_index == 1:
                    color_dict[key_name] = Color.orange
                else:
                    color_dict[key_name] = Color.purple
                common_flux_comparison_func(
                    current_important_flux_list, current_flux_name_index_dict[index_num],
                    current_data_array, data_dict_for_plotting, key_name)
        final_dict_for_flux_comparison_plotting[comparison_name] = data_dict_for_plotting
        final_color_dict[comparison_name] = color_dict
        final_key_name_parameter_dict[comparison_name] = key_name_parameter_dict
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
        experiments = result_information_dict[keyword.experiments]
        tissue = result_information_dict[keyword.tissue]
        try:
            patient = result_information_dict[keyword.patient]
        except KeyError:
            patient = ''
        index = result_information_dict[keyword.index]
        if index == Keywords.average:
            continue
        if experiments not in mid_data_dict_for_plotting:
            mid_data_dict_for_plotting[experiments] = {}
            raw_data_dict_for_plotting[experiments] = {}
        if tissue not in mid_data_dict_for_plotting[experiments]:
            mid_data_dict_for_plotting[experiments][tissue] = {}
            raw_data_dict_for_plotting[experiments][tissue] = {}
        for metabolite_name, mid_data_obj in experimental_mid_data_obj_dict.items():
            current_mid_label_tissue_dict = mid_data_dict_for_plotting[experiments][tissue]
            current_raw_label_tissue_dict = raw_data_dict_for_plotting[experiments][tissue]
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
    for experiments, each_experiment_mid_data_dict_for_plotting in mid_data_dict_for_plotting.items():
        for tissue, each_tissue_mid_data_dict_for_plotting in each_experiment_mid_data_dict_for_plotting.items():
            each_tissue_raw_data_dict_for_plotting = raw_data_dict_for_plotting[experiments][tissue]
            for raw_data in (False, True):
                if raw_data:
                    parent_direct = 'raw_data'
                    complete_data_dict = each_tissue_raw_data_dict_for_plotting
                    ylim = (0, None)
                else:
                    parent_direct = 'mid_data'
                    complete_data_dict = each_tissue_mid_data_dict_for_plotting
                    ylim = (0, 1)
                current_title = f'{experiments}_{tissue}'
                current_output_direct = '{}/{}'.format(output_direct, parent_direct)
                check_and_mkdir_of_direct(current_output_direct)
                multi_row_col_bar_plot(
                    complete_data_dict, target_emu_name_nested_list, target_row_num, target_col_num,
                    error_bar_data_dict=None, color_dict=color_dict, title_dict=None,
                    output_direct=current_output_direct, current_title=current_title, ylim=ylim,
                    xlabel_list=None, figsize=None, legend=False)


def metabolic_network_parameter_generator():
    experimental_mid_metabolite_set = {
        'GLC_c',
        '3PG_c',
        'PEP_c',
        'LAC_c',
        'CIT_c', 'CIT_m',
        'GLU_c', 'GLU_m',
        'MAL_c', 'MAL_m',
        'ALA_c',
        'ASP_c', 'ASP_m',
        'PYR_c', 'PYR_m',
        'GLN_c', 'GLN_m',
    }
    experimental_mixed_mid_metabolite_set = {
        'CIT_c', 'CIT_m',
        'GLU_c', 'GLU_m',
        'MAL_c', 'MAL_m',
        'ASP_c', 'ASP_m',
        'PYR_c', 'PYR_m',
        'GLN_c', 'GLN_m',
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
