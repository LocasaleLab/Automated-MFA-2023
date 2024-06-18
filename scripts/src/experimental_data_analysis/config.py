from scripts.src.core.common.classes import OptionDict
from scripts.src.common.config import Direct as CommonDirect, Keywords
from scripts.src.core.common.config import ParamName
# from ...data.simulated_data import simulated_flux_vector_and_mid_data

from .inventory import DataModelType, RunningMode

# simulated_flux_value_dict = simulated_flux_vector_and_mid_data.simulated_flux_value_dict


class Direct(object):
    # root_direct = 'scripts'
    # data_direct = '{}/data'.format(root_direct)
    # output_direct = '{}/output'.format(root_direct)
    name = 'experimental_data_analysis'
    output_direct = f'{CommonDirect.output_direct}/{name}'
    common_data_direct = f'{CommonDirect.common_submitted_raw_data_direct}/{name}'


# test_mode = True
# data_model_name = DataModelType.renal_carcinoma_invivo_infusion
# data_model_name = DataModelType.renal_carcinoma_invivo_infusion_squared_loss
data_model_name = DataModelType.renal_carcinoma_invivo_infusion_traditional_method
# data_model_name = DataModelType.renal_carcinoma_invivo_infusion_with_glns_m
# data_model_name = DataModelType.renal_carcinoma_invivo_infusion_with_glns_m_traditional_method
# data_model_name = DataModelType.lung_tumor_invivo_infusion
# data_model_name = DataModelType.colon_cancer_cell_line
# data_model_name = DataModelType.colon_cancer_cell_line_squared_loss
# data_model_name = DataModelType.colon_cancer_cell_line_traditional_method
# data_model_name = DataModelType.colon_cancer_cell_line_with_glns_m
# data_model_name = DataModelType.colon_cancer_cell_line_with_glns_m_traditional_method
# data_model_name = DataModelType.hct116_cultured_cell_line
# data_model_name = DataModelType.hct116_cultured_cell_line_with_glns_m
load_previous_results = True


# running_mode = RunningMode.flux_analysis
running_mode = RunningMode.result_process
# running_mode = RunningMode.raw_experimental_data_plotting

# solver_type = ParamName.slsqp_numba_solver
solver_type = ParamName.slsqp_numba_python_solver
# solver_type = ParamName.slsqp_numba_nopython_solver
# solver_type = ParamName.slsqp_solver

experimental_results_comparison = False
fluxes_comparison = True
output_flux_results = False
verify_result = False
repeat_each_analyzed_set = True
traditional_repeat_each_analyzed_set = True

loss_percentile = 0.005
# loss_percentile = 0.002
report_interval = 50
repeat_time_each_analyzed_set = 5
traditional_method_total_num = 400
traditional_method_loss_percentile = 1 / 80
traditional_method_select_num = 5


def running_settings(test_mode=False):
    parallel_parameter_dict = {
        Keywords.max_optimization_each_generation: 10000,
        Keywords.each_process_optimization_num: 50,
        Keywords.processes_num: 6,
        Keywords.thread_num_constraint: None,
        # Keywords.thread_num_constraint: 4,
        # Keywords.parallel_test: True,
    }
    if test_mode:
        each_case_optimization_num = 10
        parallel_parameter_dict = None
    elif data_model_name in {
            DataModelType.hct116_cultured_cell_line, DataModelType.hct116_cultured_cell_line_with_glns_m}:
        each_case_optimization_num = 2000
        parallel_parameter_dict[Keywords.each_process_optimization_num] = 20
    elif data_model_name in {
            DataModelType.colon_cancer_cell_line_with_glns_m,
            DataModelType.renal_carcinoma_invivo_infusion_with_glns_m}:
        each_case_optimization_num = 100000
    else:
        each_case_optimization_num = 60000
    return each_case_optimization_num, parallel_parameter_dict


"""
Biomass coefficient dict from T. Shlomi, 2011 and Recon2 model.
For further analysis, coefficients are divided to amino acid and nucleotide part.
"""

aa_biomass_coefficient_dict_shlomi = {
    "glycine": 0.62815197,
    "serine": 0.167507192,
    "aspartate": 3.128196812,
    "asparagine": 0.054439837,
    "arginine": 0.054439837
}
nucleotide_biomass_coefficient_dict_shlomi = {
    "AMP": 0.023164655,
    "CMP": 0.038607758,
    "GMP": 0.043755459,
    "UMP": 0.023164655,
    "dAMP": 0.0094984,
    "dCMP": 0.006332267,
    "dGMP": 0.006332267,
    "dTMP": 0.0094984
}

aa_biomass_coefficient_dict_recon2 = {
    "glycine": 0.62815197,
    "serine": 0.167507192,
    "aspartate": 3.128196812,
    "asparagine": 0.054439837,
    "arginine": 0.054439837
}

nucleotide_biomass_coefficient_dict_recon2 = {
    "AMP": 0.023164655,
    "CMP": 0.038607758,
    "GMP": 0.043755459,
    "UMP": 0.023164655,
    "dAMP": 0.0094984,
    "dCMP": 0.006332267,
    "dGMP": 0.006332267,
    "dTMP": 0.0094984
}

biomass_constant_dict_shlomi = {
    "aminoacids": aa_biomass_coefficient_dict_shlomi,
    "nucleotide": nucleotide_biomass_coefficient_dict_shlomi
}

data_folder = 'data_and_models'
glc_6_labeling_key = 'glc_6'
glc_2_labeling_key = 'glc_2'
gln_5_labeling_key = 'gln_5'


class CommonParameters(object):
    common_flux_range = (1, 1000)
    specific_flux_range_dict = {}
    mix_ratio_multiplier = 100
    common_mix_ratio_range = (0.05, 0.95)
    mixed_compartment_list = ('m', 'c')
    model_compartment_set = {'m', 'c', 'e'}
    solver_config_dict = OptionDict()
    squared_loss_config_dict = OptionDict({
        ParamName.loss_type: ParamName.mean_squared_loss
    })

