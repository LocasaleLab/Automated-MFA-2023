from . import colon_cancer_cell_line
from .colon_cancer_cell_line import *
from .colon_cancer_cell_line import total_param_list as raw_total_param_list, \
    project_name_generator as raw_project_name_generator, special_result_label_converter, \
    keyword_list as raw_keyword_list

name = 'colon_cancer_cell_line_traditional_method'

total_param_list = [
    {
        **raw_param_dict,
        Keywords.traditional_method: True
    }
    for raw_param_dict in raw_total_param_list
]

keyword_list = [*raw_keyword_list, Keywords.traditional_method]


def project_name_generator(
        cell_line, glucose_level, repeat_index, traditional_method=True):
    base_name = raw_project_name_generator(cell_line, glucose_level, repeat_index)
    return base_name


parent_data_model_obj = colon_cancer_cell_line
parent_result_name = colon_cancer_cell_line.name
parent_final_data_obj = CurrentFinalResult(
    result_name=parent_result_name, data_model_object=parent_data_model_obj)

collect_results = collect_results_func_template(
    project_name_generator, total_param_list, keyword_list, different_final_data_obj=parent_final_data_obj)

