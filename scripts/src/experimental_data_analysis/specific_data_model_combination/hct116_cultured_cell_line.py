from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from scripts.src.common.config import Color, Keywords, Direct, DataType
from scripts.src.common.plotting_functions import group_bar_plot, multi_row_col_bar_plot

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
unoptimized = Keywords.unoptimized


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
                        # obj_threshold_key: 999999
                    },
                    {
                        keyword.index: 1,
                        obj_threshold_key: unoptimized
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


def data_param_list_generator(param_raw_list):
    current_param_list = []
    for raw_param_dict in param_raw_list:
        experiments_key = raw_param_dict[keyword.experiments]
        each_cell_line_content_list = raw_param_dict['']
        for cell_line_content_dict in each_cell_line_content_list:
            condition_key = cell_line_content_dict[keyword.condition]
            each_glucose_level_content_list = cell_line_content_dict['']
            for glucose_level_dict in each_glucose_level_content_list:
                index_key = glucose_level_dict[keyword.index]
                try:
                    obj_threshold = glucose_level_dict[obj_threshold_key]
                except KeyError:
                    obj_threshold = None
                new_param_dict = {
                    keyword.experiments: experiments_key,
                    keyword.condition: condition_key,
                    keyword.index: index_key,
                    obj_threshold_key: obj_threshold
                }
                current_param_list.append(new_param_dict)
    return current_param_list


data_param_raw_list = complete_data_param_raw_list
total_param_list = data_param_list_generator(data_param_raw_list)
empty_patient_key = ''


def collect_results(final_data_obj):
    final_mapping_dict = {}
    for param_dict in total_param_list:
        experiments_key = param_dict[keyword.experiments]
        condition_key = param_dict[keyword.condition]
        repeat_index = param_dict[keyword.index]

        project_name = data_wrap_obj.project_name_generator(
            experiments_key, condition_key, repeat_index)
        if obj_threshold_key not in param_dict:
            param_dict[obj_threshold_key] = None
        if param_dict[obj_threshold_key] == unoptimized:
            unoptimized_project_name = f'{project_name}__{unoptimized}'
            project_parameter = (experiments_key, condition_key, repeat_index, unoptimized_project_name)
            final_mapping_dict[project_name] = project_parameter
            project_name = unoptimized_project_name
        else:
            project_parameter = (experiments_key, condition_key, repeat_index, None)
            if project_name not in final_mapping_dict:
                final_mapping_dict[project_name] = project_parameter
        # (
        #     final_data_obj.final_loss_data_dict[project_name], final_data_obj.final_solution_data_dict[project_name],
        #     final_data_obj.final_flux_name_index_dict[project_name],
        #     final_data_obj.final_information_dict[project_name],
        #     final_data_obj.final_predicted_data_dict[project_name],
        #     final_data_obj.final_target_experimental_mid_data_dict[project_name],
        #     final_data_obj.final_time_data_dict[project_name]
        # ) = final_data_obj.iteration(project_name)
        final_data_obj.load_current_result_label(project_name)
        final_data_obj.final_information_dict[project_name][obj_threshold_key] = param_dict[obj_threshold_key]
    return final_mapping_dict


def result_output_dataframe_dict_generator(complete_result_dict):
    pass
    # return {'Sheet1': pd.DataFrame()}


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
