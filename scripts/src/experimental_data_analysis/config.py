from scripts.src.core.common.classes import OptionDict
from scripts.src.common.config import Direct as CommonDirect, Keywords
from scripts.src.core.common.config import ParamName
from .inventory import DataModelType, RunningMode


class Direct(object):
    # root_direct = 'scripts'
    # data_direct = '{}/data'.format(root_direct)
    # output_direct = '{}/output'.format(root_direct)
    name = 'experimental_data_analysis'
    output_direct = f'{CommonDirect.output_direct}/{name}'
    common_data_direct = f'{CommonDirect.common_submitted_raw_data_direct}/{name}'


# test_mode = True
# data_model_name = DataModelType.renal_carcinoma_invivo_infusion
# data_model_name = DataModelType.lung_tumor_invivo_infusion
data_model_name = DataModelType.colon_cancer_cell_line
# data_model_name = DataModelType.hct116_cultured_cell_line
load_previous_results = True


# running_mode = RunningMode.flux_analysis
running_mode = RunningMode.result_process
# running_mode = RunningMode.raw_experimental_data_plotting

# solver_type = ParamName.slsqp_numba_solver
solver_type = ParamName.slsqp_numba_python_solver
# solver_type = ParamName.slsqp_solver

experimental_results_comparison = False
fluxes_comparison = True
output_flux_results = False
verify_result = False

loss_percentile = 0.005
# loss_percentile = 0.002
report_interval = 50
thread_num_constraint = 4


def running_settings(test_mode=False):
    if test_mode:
        each_case_optimization_num = 10
        parallel_parameter_dict = None
        # parallel_parameter_dict = {
        #     'max_optimization_each_generation': 20,
        #     'each_process_optimization_num': 10,
        #     'processes_num': 1
        # }
    elif data_model_name == DataModelType.hct116_cultured_cell_line:
        each_case_optimization_num = 400
        parallel_parameter_dict = {
            'max_optimization_each_generation': 5000,
            'each_process_optimization_num': 10,
            # 'processes_num': 4
            'processes_num': 6
        }
    else:
        each_case_optimization_num = 20000
        parallel_parameter_dict = {
            'max_optimization_each_generation': 5000,
            'each_process_optimization_num': 50,
            # 'processes_num': 4
            'processes_num': 6
        }
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

