from common_and_plotting_functions.config import Direct as GeneralDirect
from common_and_plotting_functions.functions import default_parameter_extract
from common_and_plotting_functions.built_in_packages import it, warnings, enum
from common_and_plotting_functions.third_party_packages import np

from figure_plotting_package.common.config import ParameterName as GeneralParameterName
from figure_plotting_package.common.classes import Vector, VerticalAlignment, HorizontalAlignment, FontWeight, \
    LineStyle, FontStyle
from figure_plotting_package.common.color import ColorConfig, ZOrderConfig, TextConfig
from figure_plotting_package.common.common_functions import t_test_of_two_groups, \
    symmetrical_lim_tick_generator_with_zero, initialize_vector_input, calculate_center_bottom_offset, \
    numbered_even_sequence
from figure_plotting_package.common.common_figure_materials import CommonElementConfig
from figure_plotting_package.common.figure_data_format import BasicFigureData as RawBasicFigureData
from figure_plotting_package.common.core_plotting_functions import heatmap_and_box3d_parameter_preparation

from figure_plotting_package.elements import Elements as GeneralElements, common_legend_generator

from figure_plotting_package.data_figure.config import net_flux_x_axis_labels_generator, merge_axis_format_dict, \
    DataFigureConfig, ParameterName as DataFigureParameterName, generate_violin_config_dict
from figure_plotting_package.diagrams.config import ParameterName as DiagramParameterName

CompositeFigure = GeneralElements.CompositeFigure
TextBox = GeneralElements.TextBox
random_seed = np.random.default_rng(4536251)


class Keywords(object):
    name = 'name'
    type = 'type'
    parameters = 'parameters'
    default = 'default'

    kidney = 'kidney'
    carcinoma = 'carcinoma'
    brain = 'brain'
    lung = 'lung'
    flank = 'flank'
    tumor = 'tumor'
    all_tissue = 'all_tissue'

    high_glucose = 'H'
    low_glucose = 'L'

    general = 'general'
    serum = 'serum'
    liver = 'liver'
    heart = 'heart'
    vastus_muscle = 'vastus_muscle'
    soleus_muscle = 'soleus_muscle'
    gastroc_muscle = 'gastroc_muscle'
    brown_adipose = 'brown_adipose'
    po_adipose = 'periovarian_adipose'
    sq_adipose = 'sub_q_fat'


class Direct(GeneralDirect):
    figure_output_direct = 'figures/output_figure'


class Figure(GeneralElements.Figure):
    figure_output_direct = Direct.figure_output_direct
    top_margin_ratio = 0.05
    side_margin_ratio = 0.02


class DataName(object):
    raw_model_raw_data = 'raw_model_raw_data'
    raw_model_all_data = 'raw_model_all_data'
    raw_model_with_glns_m_raw_data = 'raw_model_with_glns_m_raw_data'
    raw_model_with_glns_m_all_data = 'raw_model_with_glns_m_all_data'
    raw_model_raw_data_with_squared_loss = 'raw_model_raw_data_with_squared_loss'
    raw_model_all_data_with_squared_loss = 'raw_model_all_data_with_squared_loss'
    optimization_from_solutions_raw_data = 'optimization_from_raw_data_average_solutions'
    optimization_from_solutions_all_data = 'optimization_from_all_data_average_solutions'
    optimization_from_solutions_raw_data_with_squared_loss = 'optimization_from_raw_data_average_solutions_with_squared_loss'
    optimization_from_solutions_all_data_with_squared_loss = 'optimization_from_all_data_average_solutions_with_squared_loss'
    optimization_from_batched_raw_data = 'optimization_from_batched_simulated_raw_data'
    optimization_from_batched_all_data = 'optimization_from_batched_simulated_all_data'
    optimization_from_solutions_batched_raw_data = 'optimization_from_batched_simulated_raw_data_average_solutions'
    optimization_from_solutions_batched_all_data = 'optimization_from_batched_simulated_all_data_average_solutions'
    optimization_from_batched_raw_data_with_squared_loss = 'optimization_from_batched_simulated_raw_data_with_squared_loss'
    optimization_from_batched_all_data_with_squared_loss = 'optimization_from_batched_simulated_all_data_with_squared_loss'

    raw_data_result_label = 'raw_model__raw_data'
    all_data_result_label = 'raw_model__all_data'
    raw_data_noise_result_label = 'raw_model__raw_data_noise'
    all_data_noise_result_label = 'raw_model__all_data_noise'

    model_sensitivity = 'model_sensitivity'
    model_sensitivity_all_data = 'model_sensitivity_all_data'
    merge_reversible_reaction = 'merge_reversible_reaction'
    merge_reversible_reaction_all_data = 'merge_reversible_reaction_all_data'
    combine_consecutive_reactions = 'combine_consecutive_reactions'
    combine_consecutive_reactions_all_data = 'combine_consecutive_reactions_all_data'
    prune_branches = 'prune_branches'
    prune_branches_all_data = 'prune_branches_all_data'

    data_sensitivity = 'data_sensitivity'
    data_sensitivity_with_noise = 'data_sensitivity_with_noise'
    smaller_data_size = 'smaller_data_size'
    medium_data_plus = 'medium_data_plus'
    medium_data = 'medium_data'
    few_data = 'few_data'
    data_without_pathway = 'data_without_pathway'
    data_without_ppp = 'data_without_ppp'
    data_without_aa = 'data_without_aa'
    data_without_tca = 'data_without_tca'
    medium_data_without_combination = 'data_without_combination'
    compartmental_data = 'data_with_compartments'
    # experimental_non_compartmental_data = 'experimental_available_non-compartmental_data'

    config_sensitivity = 'config_sensitivity'
    config_sensitivity_all_data = 'config_sensitivity_all_data'
    different_flux_range = 'different_flux_range'
    different_flux_range_all_data = 'different_flux_range_all_data'
    different_constant_flux = 'different_constant_flux'
    different_constant_flux_all_data = 'different_constant_flux_all_data'
    different_constant_flux_with_noise = 'different_constant_flux_with_noise'
    different_constant_flux_with_noise_all_data = 'different_constant_flux_with_noise_all_data'

    colon_cancer_cell_line = 'colon_cancer_cell_line'
    colon_cancer_cell_line_with_glns_m = 'colon_cancer_cell_line_with_glns_m'
    colon_cancer_cell_line_squared_loss = 'colon_cancer_cell_line_squared_loss'
    colon_cancer_cell_line_traditional_method = 'colon_cancer_cell_line_traditional_method'
    colon_cancer_cell_line_with_glns_m_traditional_method = 'colon_cancer_cell_line_with_glns_m_traditional_method'
    renal_carcinoma_invivo_infusion = 'renal_carcinoma_invivo_infusion'
    renal_carcinoma_invivo_infusion_with_glns_m = 'renal_carcinoma_invivo_infusion_with_glns_m'
    renal_carcinoma_invivo_infusion_squared_loss = 'renal_carcinoma_invivo_infusion_squared_loss'
    renal_carcinoma_invivo_infusion_traditional_method = 'renal_carcinoma_invivo_infusion_traditional_method'
    renal_carcinoma_invivo_infusion_with_glns_m_traditional_method = \
        'renal_carcinoma_invivo_infusion_with_glns_m_traditional_method'
    lung_tumor_invivo_infusion = 'lung_tumor_invivo_infusion'
    hct116_cultured_cell_line = 'hct116_cultured_cell_line'
    hct116_cultured_cell_line_with_glns_m = 'hct116_cultured_cell_line_with_glns_m'
    hct116_cultured_cell_line_squared_loss = 'hct116_cultured_cell_line_squared_loss'
    multiple_tumor = 'multiple_tumor'


class ParameterName(GeneralParameterName):
    # Published data parameters
    multiple_tumor = DataName.multiple_tumor


class BasicFigureData(RawBasicFigureData):
    data_direct = Direct.figure_raw_data_direct
