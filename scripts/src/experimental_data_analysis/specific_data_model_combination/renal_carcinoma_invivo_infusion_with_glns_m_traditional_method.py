from . import renal_carcinoma_invivo_infusion_with_glns_m
from .renal_carcinoma_invivo_infusion_with_glns_m import *
from .renal_carcinoma_invivo_infusion_with_glns_m import total_param_list as raw_total_param_list, \
    project_name_generator as raw_project_name_generator, keyword_list as raw_keyword_list

name = 'renal_carcinoma_invivo_infusion_with_glns_m_traditional_method'

total_param_list = [
    {
        **raw_param_dict,
        Keywords.loss: Keywords.squared_loss
    }
    for raw_param_dict in raw_total_param_list
]

keyword_list = [*raw_keyword_list, Keywords.loss]


def project_name_generator(
        tissue_name, tissue_index, repeat_index, traditional_method=True):
    base_name = raw_project_name_generator(tissue_name, tissue_index, repeat_index)
    return base_name


parent_data_model_obj = renal_carcinoma_invivo_infusion_with_glns_m
parent_result_name = renal_carcinoma_invivo_infusion_with_glns_m.name
parent_final_data_obj = CurrentFinalResult(
    result_name=parent_result_name, data_model_object=parent_data_model_obj)

collect_results = collect_results_func_template(
    project_name_generator, total_param_list, keyword_list, different_final_data_obj=parent_final_data_obj)

