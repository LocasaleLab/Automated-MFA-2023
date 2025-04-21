from ..common.config import DataName

renal_kidney_name = 'kidney'
renal_carcinoma_name = 'carcinoma'
renal_brain_name = 'brain'
renal_kidney_carcinoma_comparison_display_index = 1
renal_brain_display_index = 1
lung_patient_name = 'K1031'
common_display_cancer_cell_line = 'HCT116-P3'
common_data_width = 0.5
all_net_flux_comparison_scale = 0.4
common_data_figure_scale = 0.45

target_optimized_size = 20000
target_selected_size = 100
all_data_optimized_size = target_optimized_size
all_data_selection_size = target_selected_size
raw_data_optimized_size = target_optimized_size
raw_data_selection_size = target_selected_size
with_glns_m = True

raw_model_raw_data_with_glns_m = False
if raw_model_raw_data_with_glns_m:
    raw_model_raw_data_name = DataName.raw_model_with_glns_m_raw_data
    raw_data_traditional_optimized_size = 400
else:
    raw_model_raw_data_name = DataName.raw_model_raw_data
    # raw_data_traditional_optimized_size = 500
    raw_data_traditional_optimized_size = 400
# raw_model_raw_data_name = DataName.raw_model_raw_data_with_glns_m
raw_model_all_data_with_glns_m = False
if raw_model_all_data_with_glns_m:
    raw_model_all_data_name = DataName.raw_model_with_glns_m_all_data
    all_data_traditional_optimized_size = 400
else:
    raw_model_all_data_name = DataName.raw_model_all_data
    # all_data_traditional_optimized_size = 500
    all_data_traditional_optimized_size = 400
hct_116_data_name = DataName.hct116_cultured_cell_line
# hct_116_data_name = DataName.hct116_cultured_cell_line_with_glns_m
renal_carcinoma_data_set = DataName.renal_carcinoma_invivo_infusion
# renal_carcinoma_data_set = DataName.renal_carcinoma_invivo_infusion_with_glns_m
renal_carcinoma_traditional_data_set = DataName.renal_carcinoma_invivo_infusion_traditional_method
# renal_carcinoma_traditional_data_set = DataName.renal_carcinoma_invivo_infusion_with_glns_m_traditional_method
colon_cancer_data_set = DataName.colon_cancer_cell_line
# colon_cancer_data_set = DataName.colon_cancer_cell_line_with_glns_m
colon_cancer_traditional_data_set = DataName.colon_cancer_cell_line_traditional_method
# colon_cancer_traditional_data_set = DataName.colon_cancer_cell_line_with_glns_m_traditional_method


def common_result_label_constructor(condition, data_type):
    if condition == 'renal':
        if data_type == renal_brain_name:
            return f'brain__{renal_brain_display_index}_average'
        else:
            return f'{data_type}__{renal_kidney_carcinoma_comparison_display_index}_average'
    elif condition == 'lung':
        return f'human__{lung_patient_name}_tumor_average'
    elif condition == 'colon_cancer':
        if data_type == 'high':
            return f'{common_display_cancer_cell_line}__H_average'
        elif data_type == 'low':
            return f'{common_display_cancer_cell_line}__L_average'
        else:
            raise ValueError()
    else:
        raise ValueError()

