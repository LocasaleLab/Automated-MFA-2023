from .third_party_packages import np
from common_and_plotting_functions.config import Direct as GeneralDirect, Keywords as ParentKeywords, \
    FigureDataKeywords
from figure_plotting_package.common.figure_data_format import BasicFigureData as RawBasicFigureData, \
    FigureData as RawFigureData

random_seed = np.random.default_rng(4536251)


class Keywords(object):
    model = 'model'
    data = 'data'
    config = 'config'
    label = 'label'
    index_label = 'index_label'
    comment = 'comment'

    # Parallel keywords:
    each_process_optimization_num = 'each_process_optimization_num'
    max_optimization_each_generation = 'max_optimization_each_generation'
    thread_num_constraint = 'thread_num_constraint'
    processes_num = 'processes_num'
    parallel_test = 'parallel_test'

    predefined_initial_solution_matrix = 'predefined_initial_solution_matrix'
    unoptimized = 'unoptimized'
    squared_loss = 'squared_loss'
    traditional_method = 'traditional_method'
    loss = 'loss'
    test = 'test'
    optimized = 'optimized'
    experimental = 'experimental'
    obj_threshold_key = 'obj_threshold'
    metabolite_name_col = 'Name'
    average = 'average'

    tca_index = 'tca_index'
    cancer_index = 'cancer_index'
    non_canonical_tca_index = 'non_canonical_tca_index'
    net_r5p_production = 'net_r5p_production'
    mas_index = 'mas_index'

    sheet_name = 'sheet_name'
    sheet_information_str = 'sheet_information'
    complete_result_name_str = 'complete_result_name'
    index_name = 'Index'
    experiments = 'experiments'

    normal_simulated_base_name = 'simulated_flux_vector_and_mid_data'
    batched_simulated_base_name = 'simulated_batched_flux_vector_and_mid_data'
    simulated_noise_str = '_with_noise'
    simulated_flux_name_index_dict = 'flux_name_index_dict'
    simulated_final_flux_vector_list = 'final_flux_vector_list'
    simulated_output_mid_data_dict_list = 'output_mid_data_dict_list'
    simulated_output_all_mid_data_dict_list = 'output_all_mid_data_dict_list'


class Direct(GeneralDirect):
    common_submitted_raw_data_direct = GeneralDirect.common_submitted_raw_data_direct
    tmp_data_direct = GeneralDirect.figure_raw_data_direct
    flux_result_xlsx_filename = f'{ParentKeywords.flux_raw_data}.xlsx'
    mid_result_xlsx_filename = f'{ParentKeywords.mid_raw_data}.xlsx'
    solver_description_xlsx_filename = f'{ParentKeywords.solver_descriptions}.xlsx'
    data_direct = 'scripts/data'
    output_direct = 'scripts/output'
    raw_flux_analysis = 'raw_flux_analysis'
    flux_comparison = 'flux_comparison'
    predicted_experimental_mid_comparison_direct = 'predicted_experimental_mid_comparison'
    raw_and_mid_experimental_data_display_direct = 'raw_and_mid_experimental_data_display'
    metabolic_network_visualization_direct = 'metabolic_network_visualization'

    solution_array = 'solution_array'
    time_array = 'time_array'
    loss_array = 'loss_array'
    result_information = 'result_information'
    predicted_dict = 'predicted_dict'
    flux_name_index_dict = 'flux_name_index_dict'
    experimental_data = 'experimental_data'

    simulated_input_file_name = 'simulated_flux_vector_and_mid_data.py'
    simulated_input_file_path = f'scripts/src/simulated_data/{simulated_input_file_name}'
    simulated_output_py_file_direct = 'scripts/data/simulated_data'
    simulated_data_direct_name = 'simulated_data'
    simulated_output_xlsx_file_direct = f'{common_submitted_raw_data_direct}/{simulated_data_direct_name}'
    simulated_output_pickle_direct = simulated_output_py_file_direct


class FigureData(RawFigureData):
    def __init__(self, data_prefix, data_name):
        super().__init__(GeneralDirect.figure_raw_data_direct, data_prefix, data_name)


class BasicFigureData(RawBasicFigureData):
    data_direct = GeneralDirect.figure_raw_data_direct


class DataType(object):
    test = 'test'
    hct116_cultured_cell_line = 'hct116_cultured_cell_line'
    renal_carcinoma = 'renal_carcinoma'
    lung_tumor = 'lung_tumor'
    colon_cancer = 'colon_cancer'


def rgba_to_rgb(raw_rgb, alpha, background=None):
    """
    Convert color in RGBA to RGB.
    :param raw_rgb: RGB components in RGBA form.
    :param alpha: Transparency of RGBA color.
    :param background: Background color.
    :return: Transformed RGB color.
    """
    if background is None:
        background = np.array([1, 1, 1])
    return raw_rgb * alpha + background * (1 - alpha)


class Color(object):
    white = np.array([1, 1, 1])
    blue = np.array([21, 113, 177]) / 255
    orange = np.array([251, 138, 68]) / 255
    purple = np.array([112, 48, 160]) / 255
    light_blue = np.array([221, 241, 255]) / 255

    alpha_value = 0.3
    alpha_for_bar_plot = alpha_value + 0.1
    alpha_for_heatmap = alpha_value + 0.2

    color_list = [
        rgba_to_rgb(blue, alpha_for_heatmap, white), white,
        rgba_to_rgb(orange, alpha_for_heatmap, white)]


def net_r5p_production(flux_name_value_dict):
    r5p_product_net = flux_name_value_dict['RPI_c'] - flux_name_value_dict['RPI_c__R']
    r5p_back_net = flux_name_value_dict['TKT1_c'] - flux_name_value_dict['TKT1_c__R']
    return r5p_product_net - r5p_back_net


def tca_index_calculation(flux_name_value_dict):
    gapd_net = flux_name_value_dict['GAPD_c'] - flux_name_value_dict['GAPD_c__R']
    tca_net = flux_name_value_dict['CS_m']
    return tca_net / gapd_net


def cancer_index_calculation(flux_name_value_dict):
    gapd_net = flux_name_value_dict['GAPD_c'] - flux_name_value_dict['GAPD_c__R']
    ldh_net = flux_name_value_dict['LDH_c'] - flux_name_value_dict['LDH_c__R']
    return ldh_net / gapd_net


def non_canonical_tca_index_calculation(flux_name_value_dict):
    tca_total = flux_name_value_dict['CS_m']
    main_tca_flux = flux_name_value_dict['AKGD_m']
    non_canonical_tca_flux = flux_name_value_dict['ACITL_c']
    tca_exchange_net = flux_name_value_dict['CIT_trans__R'] - flux_name_value_dict['CIT_trans']
    # return non_canonical_tca_flux / tca_total
    return tca_exchange_net / tca_total


def mas_index(flux_name_value_dict):
    akgd_total = flux_name_value_dict['AKGD_m']
    mas_flux = flux_name_value_dict['AKGMAL_m__R'] - flux_name_value_dict['AKGMAL_m']
    cit_trans_net = flux_name_value_dict['CIT_trans__R'] - flux_name_value_dict['CIT_trans']
    # return mas_flux / cit_trans_net
    return cit_trans_net / mas_flux


index_calculation_func_dict = {
    Keywords.tca_index: tca_index_calculation,
    Keywords.cancer_index: cancer_index_calculation,
    Keywords.non_canonical_tca_index: non_canonical_tca_index_calculation,
    Keywords.net_r5p_production: net_r5p_production,
    Keywords.mas_index: mas_index,
}


net_flux_list = [
    ('PGI_c', 'PGI_c__R'),
    ('FBA_c', 'FBA_c__R'),
    ('TPI_c', 'TPI_c__R'),
    ('GAPD_c', 'GAPD_c__R'),
    ('PGK_c', 'PGK_c__R'),
    ('PGM_c', 'PGM_c__R'),
    ('ENO_c', 'ENO_c__R'),
    ('LDH_c', 'LDH_c__R'),
    ('MDH_c', 'MDH_c__R'),
    ('SHMT_c', 'SHMT_c__R'),
    ('ACONT_m', 'ACONT_m__R'),
    ('SUCD_m', 'SUCD_m__R'),
    ('FUMH_m', 'FUMH_m__R'),
    ('MDH_m', 'MDH_m__R'),
    ('GLUD_m', 'GLUD_m__R'),
    ('ASPTA_m', 'ASPTA_m__R'),
    ('ASPTA_c', 'ASPTA_c__R'),
    ('RPI_c', 'RPI_c__R'),
    ('RPE_c', 'RPE_c__R'),
    ('TKT1_c', 'TKT1_c__R'),
    ('TKT2_c', 'TKT2_c__R'),
    ('TALA_c', 'TALA_c__R'),
    ('PYR_trans', 'PYR_trans__R'),
    ('ASPGLU_m', 'ASPGLU_m__R'),
    ('AKGMAL_m', 'AKGMAL_m__R'),
    ('CIT_trans', 'CIT_trans__R'),
    ('GLN_trans', 'GLN_trans__R'),
    ('GLU_trans', 'GLU_trans__R'),
    ('GPT_c', 'GPT_c__R'),
]


