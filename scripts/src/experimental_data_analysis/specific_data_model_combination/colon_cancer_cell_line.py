from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from scripts.src.common.config import Color, Keywords, Direct, DataType
from scripts.src.common.plotting_functions import group_bar_plot, multi_row_col_bar_plot
from scripts.src.common.functions import data_param_list_generator_func_template, collect_results_func_template, \
    special_result_label_converter
from scripts.src.common.result_processing_functions import experimental_data_plotting_func_template

from scripts.data.common_functions import common_data_loader

from scripts.model.model_loader import model_loader, ModelList
from scripts.src.core.model.model_constructor import common_model_constructor

from ...common.result_processing_functions import common_flux_comparison_func
from ..result_processing_functions import CurrentFinalResult

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


separate_data_param_raw_list = [
    {
        keyword.cell_line: 'SW620-P3',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
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
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
                    {
                        keyword.index: 1,
                    },
                    {
                        keyword.index: 2,
                    },
                    {
                        keyword.index: 3,
                    },
                    ]
            },
        ]
    },
]

average_data_param_raw_list = [
    {
        keyword.cell_line: 'SW620-P3',
        '': [
            {
                keyword.glucose_level: keyword.high_glucose_level,
                '': [
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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
                    {
                        keyword.index: Keywords.average,
                    },
                    ]
            },
            {
                keyword.glucose_level: keyword.low_glucose_level,
                '': [
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


# data_param_raw_list = separate_data_param_raw_list
data_param_raw_list = average_data_param_raw_list
# total_param_list = data_param_list_generator(data_param_raw_list)
keyword_list = [keyword.cell_line, keyword.glucose_level, keyword.index]
total_param_list = data_param_list_generator_func_template(keyword_list)(data_param_raw_list)

project_name_generator = data_wrap_obj.project_name_generator
collect_results = collect_results_func_template(
    project_name_generator, total_param_list, keyword_list)


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


target_emu_name_nested_list = [
    ['glucose', 'fructose 1,6-bisphosphate', 'glyceraldehyde 3-phosphate', 'dihydroxyacetone phosphate'],
    ['3-phosphoglycerate', 'phosphoenolpyruvate', 'pyruvate', 'lactate'],
    ['a-ketoglutarate', 'glutamate', 'glutamine', 'aspartate']
]


def major_minor_key_analysis_func(result_information_dict):
    tissue = result_information_dict[keyword.cell_line]
    glucose_level = result_information_dict[keyword.glucose_level]
    index = result_information_dict[keyword.index]
    glucose_level_index_str = f'{glucose_level}_{index}'
    major_key = tissue
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
    major_key_file_name_func=lambda major_key: f'target_metabolites_{major_key}_cell_line')


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
