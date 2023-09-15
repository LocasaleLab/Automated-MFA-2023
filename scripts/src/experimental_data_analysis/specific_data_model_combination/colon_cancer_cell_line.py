from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from scripts.src.common.config import Color, Keywords, Direct, DataType
from scripts.src.common.plotting_functions import group_bar_plot, multi_row_col_bar_plot

from scripts.data.common_functions import common_data_loader

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

from ...common.result_processing_functions import common_flux_comparison_func

data_wrap_obj, keyword = common_data_loader(DataType.colon_cancer, test_mode=False, natural_anti_correction=False)
user_defined_model = model_loader(ModelList.base_model)
mfa_model_obj = common_model_constructor(user_defined_model)


name = 'colon_cancer_cell_line'
output_folder = '{}/{}'.format(Direct.output_direct, name)
raw_data_folder = '{}/{}'.format(output_folder, Direct.raw_flux_analysis)


class SpecificParameter(object):
    test_dynamic_constant_flux_list = []
    test_preset_constant_flux_value_dict = {
        # 'GLC_input': 100,
        'ASP_input': 100,

        # 'GLN_input': 80,
        # 'ASP_input': 10,
        # 'SER_input': 8,
        # 'ALA_input': 20,
    }
    specific_flux_range_dict = {
        'Salvage_c': (1, 10)
    }


complete_data_param_raw_list = [
    {
        keyword.cell_line: 'SW620-P3',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'SW480',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'HCT8-P5',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'HT29',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'HCT116-P3',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'NCI-H5087',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'SW48-P2',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'SW948-P3',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
        keyword.cell_line: 'NCI-H5087',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
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
                keyword.glucose_level: keyword.low_glucose_level,
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
]


important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    ('PGM_c', 'PGM_c__R'),
    'GLC_input',
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
    ('CIT_trans__R', 'CIT_trans'),
    'PEPCK_c',
    'MDH_c',
    'ASPTA_c',
    ('MDH_c', 'MDH_c__R'),
    ('ASPTA_c', 'ASPTA_c__R'),
    ('AKGMAL_m__R', 'AKGMAL_m'),
    'ME2_c',
    ('ASPGLU_m', 'ASPGLU_m__R'),
    'GLN_input',
    'ASP_input',
    ('GAPD_c', 'GAPD_c__R'),
    'HEX_c',
]


def data_param_list_generator(param_raw_list):
    current_param_list = []
    for raw_param_dict in param_raw_list:
        cell_line_key = raw_param_dict[keyword.cell_line]
        each_cell_line_content_list = raw_param_dict['']
        for cell_line_content_dict in each_cell_line_content_list:
            glucose_level_key = cell_line_content_dict[keyword.glucose_level]
            each_glucose_level_content_list = cell_line_content_dict['']
            for glucose_level_dict in each_glucose_level_content_list:
                index_key = glucose_level_dict[keyword.index]
                new_param_dict = {
                    keyword.cell_line: cell_line_key,
                    keyword.glucose_level: glucose_level_key,
                    keyword.index: index_key,
                    Keywords.obj_threshold_key: None
                }
                current_param_list.append(new_param_dict)
    return current_param_list


data_param_raw_list = complete_data_param_raw_list
total_param_list = data_param_list_generator(data_param_raw_list)
empty_patient_key = ''


def collect_results(final_data_obj):
    final_mapping_dict = {}
    for param_dict in total_param_list:
        cell_line_key = param_dict[keyword.cell_line]
        glucose_level_key = param_dict[keyword.glucose_level]
        repeat_index = param_dict[keyword.index]
        project_name = data_wrap_obj.project_name_generator(
            cell_line_key, glucose_level_key, repeat_index)
        final_mapping_dict[project_name] = (cell_line_key, glucose_level_key, repeat_index)
        final_data_obj.load_current_result_label(project_name)
        if Keywords.obj_threshold_key in final_data_obj.final_information_dict[project_name]:
            del final_data_obj.final_information_dict[project_name][Keywords.obj_threshold_key]
    return final_mapping_dict


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
                    # color_dict[flux_title][key_name] = current_color
                    if key_name not in color_dict:
                        color_dict[key_name] = current_color
                    common_flux_comparison_func(
                        current_important_flux_list,
                        final_flux_name_index_dict[cell_line_key][glucose_level][index_num], current_data_array,
                        data_dict_for_plotting, key_name)

                    # for flux_name in important_flux_list:
                    #     if isinstance(flux_name, str):
                    #         single_flux = True
                    #         flux_title = flux_name
                    #     elif isinstance(flux_name, tuple) or isinstance(flux_name, list):
                    #         single_flux = False
                    #         flux_title = '{} - {}'.format(flux_name[0], flux_name[1])
                    #     else:
                    #         raise ValueError()
                    #     if single_flux:
                    #         flux_index = common_flux_name_index_dict[flux_name]
                    #         calculated_flux_array = current_data_array[:, flux_index]
                    #     else:
                    #         flux_index1 = common_flux_name_index_dict[flux_name[0]]
                    #         flux_index2 = common_flux_name_index_dict[flux_name[1]]
                    #         calculated_flux_array = (
                    #                 current_data_array[:, flux_index1] - current_data_array[:, flux_index2])
                    #     if flux_title not in data_dict_for_plotting:
                    #         data_dict_for_plotting[flux_title] = {}
                    #         # color_dict[flux_title] = {}
                    #     data_dict_for_plotting[flux_title][key_name] = calculated_flux_array
        final_dict_for_comparison[comparison_name] = data_dict_for_plotting
        final_color_dict[comparison_name] = color_dict
        final_key_name_parameter_dict[comparison_name] = key_name_parameter_dict
    return final_dict_for_comparison, final_key_name_parameter_dict, final_color_dict


def experimental_data_plotting(
        complete_experimental_mid_data_obj_dict, complete_result_information_dict, output_direct):
    mid_data_dict_for_plotting = {}
    raw_data_dict_for_plotting = {}
    color_dict = {}
    for result_label, experimental_mid_data_obj_dict in complete_experimental_mid_data_obj_dict.items():
        result_information_dict = complete_result_information_dict[result_label]
        cell_line = result_information_dict[keyword.cell_line]
        glucose_level = result_information_dict[keyword.glucose_level]
        index = result_information_dict[keyword.index]
        if index == Keywords.average:
            continue
        if cell_line not in mid_data_dict_for_plotting:
            mid_data_dict_for_plotting[cell_line] = {}
            raw_data_dict_for_plotting[cell_line] = {}
        for metabolite_name, mid_data_obj in experimental_mid_data_obj_dict.items():
            current_mid_cell_line_dict = mid_data_dict_for_plotting[cell_line]
            current_raw_cell_line_dict = raw_data_dict_for_plotting[cell_line]
            if metabolite_name not in current_mid_cell_line_dict:
                current_mid_cell_line_dict[metabolite_name] = {}
                current_raw_cell_line_dict[metabolite_name] = {}
            glucose_level_index_str = '{}_{}'.format(glucose_level, index)
            current_mid_cell_line_dict[metabolite_name][glucose_level_index_str] = mid_data_obj.data_vector
            current_raw_cell_line_dict[metabolite_name][glucose_level_index_str] = mid_data_obj.raw_data_vector
            if glucose_level_index_str not in color_dict:
                if glucose_level == keyword.high_glucose_level:
                    color_dict[glucose_level_index_str] = Color.blue
                elif glucose_level == keyword.low_glucose_level:
                    color_dict[glucose_level_index_str] = Color.orange
                else:
                    raise ValueError()
    target_emu_name_nested_list = [
        ['glucose', 'fructose 1,6-bisphosphate', 'glyceraldehyde 3-phosphate', 'dihydroxyacetone phosphate'],
        ['3-phosphoglycerate', 'phosphoenolpyruvate', 'pyruvate', 'lactate'],
        ['a-ketoglutarate', 'glutamate', 'glutamine', 'aspartate']
    ]
    target_row_num = len(target_emu_name_nested_list)
    target_col_num = len(target_emu_name_nested_list[0])
    for cell_line, each_cell_line_mid_data_dict_for_plotting in mid_data_dict_for_plotting.items():
        each_cell_line_raw_data_dict_for_plotting = raw_data_dict_for_plotting[cell_line]
        for raw_data in (False, True):
            if raw_data:
                parent_direct = 'raw_data'
                complete_data_dict = each_cell_line_raw_data_dict_for_plotting
                ylim = (0, None)
            else:
                parent_direct = 'mid_data'
                complete_data_dict = each_cell_line_mid_data_dict_for_plotting
                ylim = (0, 1)
            current_cell_line_output_direct = '{}/{}/{}'.format(output_direct, parent_direct, cell_line)
            check_and_mkdir_of_direct(current_cell_line_output_direct)
            # group_bar_plot(
            #     complete_data_dict, error_bar_data_dict=None, color_dict=color_dict,
            #     title_dict=None, output_direct=current_cell_line_output_direct, ylim=ylim, xlabel_list=None)
            multi_row_col_bar_plot(
                complete_data_dict, target_emu_name_nested_list, target_row_num, target_col_num,
                error_bar_data_dict=None, color_dict=color_dict, title_dict=None,
                output_direct=current_cell_line_output_direct, current_title='target_metabolites', ylim=ylim,
                xlabel_list=None, figsize=None)


mid_name_list = [
    ['GLC_c', '3PG_c', 'PYR_c+PYR_m', 'LAC_c'],
    ['ALA_c', 'CIT_c+CIT_m+ICIT_m', 'MAL_c+MAL_m'],
    ['GLU_c+GLU_m', 'GLN_c+GLN_m', 'ASP_c+ASP_m']
]


def metabolic_network_parameter_generator():
    experimental_mid_metabolite_set = {
        'ALA_c',
        'ASN_c',
        'GLY_c',
        'GLC_c',
        'FBP_c',
        'DHAP_c',
        'GAP_c',
        '3PG_c',
        'PEP_c',
        'PYR_c', 'PYR_m',
        'LAC_c',
        'CIT_c', 'CIT_m',
        'AKG_c', 'AKG_m',
        'SUC_m',
        'FUM_m',
        'MAL_c', 'MAL_m',
        'SED7P_c',
        'ERY4P_c',
        'SER_c',
        'ASP_c', 'ASP_m',
        'GLN_c', 'GLN_m',
        'GLU_c', 'GLU_m',
    }
    experimental_mixed_mid_metabolite_set = {
        'PYR_c', 'PYR_m',
        'CIT_c', 'CIT_m',
        'AKG_c', 'AKG_m',
        'MAL_c', 'MAL_m',
        'ASP_c', 'ASP_m',
        'GLN_c', 'GLN_m',
        'GLU_c', 'GLU_m',
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
