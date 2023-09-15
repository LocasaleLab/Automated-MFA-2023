import numpy as np

from .classes import Vector, VerticalAlignment, HorizontalAlignment, FontWeight
from .config import Keywords, ParameterName, DataName
from .color import ColorConfig, ZOrderConfig, TextConfig
# from ..figure_elements.metabolic_network.config import network_height_to_width_ratio


class FigureConfig(object):
    flux_comparison_scale = 1
    top_margin_ratio = 0.05
    side_margin_ratio = 0.02

    common_data_figure_scale = 0.7


class CommonElementConfig(object):
    icon_text_size = 25
    normal_document_size = 15
    smaller_document_size = normal_document_size - 2
    larger_document_size = normal_document_size + 2
    bottom_document_size = normal_document_size + 1
    text_z_order = ZOrderConfig.default_text_z_order
    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01

    normal_chevron_width = 0.05
    arc_chevron_width = normal_chevron_width + 0.01
    chevron_config = {
        ParameterName.head_len_width_ratio: 0.4,
        ParameterName.width: normal_chevron_width,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.light_bright_sky,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order,
    }
    normal_chevron_head_len = normal_chevron_width * chevron_config[ParameterName.head_len_width_ratio]

    background_rectangle_config_dict = {
        ParameterName.width: 1,
        ParameterName.face_color: ColorConfig.light_gray,
        ParameterName.edge_width: None,
        ParameterName.z_order: ZOrderConfig.default_image_z_order,
    }

    simulated_background_config_dict = {
        # ParameterName.text: TextConfig.main_text_font,
        ParameterName.radius: 0.02,
        # ParameterName.face_color: ColorConfig.medium_light_blue,
        ParameterName.face_color: ColorConfig.medium_light_bright_blue,
        ParameterName.edge_width: None,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order - 0.5,
    }

    common_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }


class CommonFigureString(object):
    loss_function_str = 'Loss value'
    left_parenthesis = r'\mathrm{(}'
    right_parenthesis = r'\mathrm{)}'
    left_bold_parenthesis = r'\mathsf{(}'
    right_bold_parenthesis = r'\mathsf{)}'
    initial_flux = r'\mathbf{v}_0'
    known_flux = r'$\mathbf{v^\prime}$'
    flux_vector = r'\mathbf{v}'
    # loss_function = r'\mathit{L}\mathbf{\left(v\right)}'
    loss_function = r'\mathit{L}' + left_parenthesis + '\mathbf{v}' + right_parenthesis
    optimal_flux_vector = r'\mathbf{v}\mathit{^*}'
    final_loss = r'\mathit{L^*}'
    math_n = r'\mathit{n}'
    math_m = r'\mathit{m}'
    bold_math_n = r'\mathbf{n}'
    bold_math_m = r'\mathbf{m}'
    m_over_n = f'{math_m}/{math_n}'
    bold_m_over_n = f'{bold_math_m}/{bold_math_n}'

    # Figure label or title
    # average_running_time = 'Average running time (s)'
    average_running_time = 'Running time (s)'
    final_loss_with_equation = f'Final loss ${final_loss}$'
    final_loss_with_equation_bold = 'Final loss $\mathbf{L^*}$'
    selection_size_m = f'Selection size ${math_m}$'
    optimization_size_n = f'Optimization size ${math_n}$'
    selection_ratio_m_over_n = f'Selection ratio ${m_over_n}$'
    bold_selection_size_m = f'Selection size ${bold_math_m}$'
    bold_optimization_size_n = f'Optimization size ${bold_math_n}$'
    bold_selection_ratio_m_over_n = f'Selection ratio ${bold_m_over_n}$'
    mean = 'Mean'
    std = 'STD'

    initial_points = f'${math_n}$ initial points'
    n_optimized_solutions = f'${math_n}$ optimized solutions'
    m_selected_solutions = f'${math_m}$ selected solutions'
    best_solution = r'Best solution'

    experimental_available_mid_data = 'Experimentally-available MID data'
    experimental_available_mid_data_wrap = 'Experimentally\navailable MID data'
    experimental_available_mid_data_double_wrap = 'Experimentally\navailable\nMID data'
    all_available_mid_data = 'All-available MID data'
    all_available_compartmental_data = 'All available compartmental MID data'
    all_available_compartmental_data_wrap = 'All available\ncompartmental MID data'
    all_available_compartmental_data_double_wrap = 'All available\ncompartmental\nMID data'
    precise_mid_data = 'Precise MID data'
    noised_mid_data = 'Noised MID data'
    loss = 'Loss'
    euclidean_distance = 'Euclidean distance'
    relative_error = 'Relative error'
    patient_id = 'Patient ID'
    cell_line = 'Cell line'
    comparison_between_kidney_and_carcinoma = 'Comparison between normal kidney\ntissue and kidney carcinoma'
    comparison_between_different_tumor = 'Comparison of different kinds of tumor in mice'
    comparison_between_normal_flank_tumor = 'Comparison of normal lung tissue,\ntumor-flank tissue and lung tumor'
    comparison_between_normal_lung_tumor_patients = 'Comparison between normal lung tissue\nand lung cancer in patients'

    merge_reversible_reactions = 'Replace reversible reactions'
    merge_reversible_reactions_wrap = 'Replace\nreversible\nreactions'
    combine_consecutive_reactions = 'Combine consecutive reactions'
    combine_consecutive_reactions_wrap = 'Combine\nconsecutive\nreactions'
    miss_branch_pathways = 'Omit branch pathways'
    miss_branch_pathways_wrap = 'Omit branch\npathways'
    smaller_data_size = 'Limited available MID'
    smaller_data_size_wrap = 'Limited\navailable MID'
    data_without_pathway = 'Pathway enrichment'
    data_without_pathway_wrap = 'Pathway\nenrichment'
    compartmental_data = 'Compartmental MID measurement'
    compartmental_data_wrap = 'Compartmental\nMID measurement'

    different_constant_flux = 'Different boundary fluxes'
    different_constant_flux_wrap = 'Different\nboundary fluxes'
    different_flux_range = 'Allowable flux range'
    different_flux_range_wrap = 'Allowable\nflux range'
    model_sensitivity = 'Model sensitivity'
    data_sensitivity = 'Data sensitivity'
    config_sensitivity = 'Configuration sensitivity'

    experimental_data = 'Experimental data'
    all_data = 'All data'
    raw_model = 'Raw model'
    raw_config_bound = 'Raw config (Medium LB + Medium UB)'
    raw_config_input_flux = 'Raw config (GLC only)'
    raw_config_bound_input_flux = 'Raw config (Medium LB + Medium UB, GLC only)'
    lower_bound = 'Lower bound (LB)'
    upper_bound = 'Upper bound (UB)'
    other_metabolite_list = 'Other metabolites'

    a_string = 'A.'
    b_string = 'B.'
    c_string = 'C.'
    no_1_string = '①'
    no_2_string = '②'
    no_3_string = '③'

    model_sensitivity_with_order_prefix = f'{no_1_string} {model_sensitivity}'
    data_sensitivity_with_order_prefix = f'{no_2_string} {data_sensitivity}'
    data_sensitivity_with_noise_with_order_prefix = f'{no_2_string} {data_sensitivity} ({noised_mid_data})'
    config_sensitivity_with_order_prefix = f'{no_3_string} {config_sensitivity}'
    config_sensitivity_with_noise_with_order_prefix = f'{no_3_string} {config_sensitivity} ({noised_mid_data})'

    merge_reversible_reactions_with_order_prefix = f'{a_string} {merge_reversible_reactions}'
    combine_consecutive_reactions_with_order_prefix = f'{b_string} {combine_consecutive_reactions}'
    miss_branch_pathways_with_order_prefix = f'{c_string} {miss_branch_pathways}'
    merge_reversible_reactions_wrap_with_order_prefix = f'{a_string} {merge_reversible_reactions_wrap}'
    combine_consecutive_reactions_wrap_with_order_prefix = f'{b_string} {combine_consecutive_reactions_wrap}'
    miss_branch_pathways_wrap_with_order_prefix = f'{c_string} {miss_branch_pathways_wrap}'

    smaller_data_size_with_order_prefix = f'{a_string} {smaller_data_size}'
    data_without_pathway_with_order_prefix = f'{b_string} {data_without_pathway}'
    compartmental_data_with_order_prefix = f'{c_string} {compartmental_data}'
    smaller_data_size_wrap_with_order_prefix = f'{a_string} {smaller_data_size_wrap}'
    data_without_pathway_wrap_with_order_prefix = f'{b_string} {data_without_pathway_wrap}'
    compartmental_data_wrap_with_order_prefix = f'{c_string} {compartmental_data_wrap}'

    different_constant_flux_with_order_prefix = f'{a_string} {different_constant_flux}'
    different_constant_flux_with_noise_with_order_prefix = f'{a_string} {different_constant_flux} ({noised_mid_data})'
    different_constant_flux_wrap_with_order_prefix = f'{a_string} {different_constant_flux_wrap}'
    different_flux_range_with_order_prefix = f'{b_string} {different_flux_range}'
    different_flux_range_wrap_with_order_prefix = f'{b_string} {different_flux_range_wrap}'

    major_pathway = 'Major pathways'
    major_pathway_wrap = 'Major\npathways'
    exchange_flux = 'Exchange fluxes'
    exchange_flux_wrap = 'Exchange\nfluxes'

    glc_input = 'GLC input'
    gln_input = 'GLN input'
    cma = 'CIT-MAL Antiport (CMA)'
    cma_wrap = 'CIT-MAL Antiport\n(CMA)'
    ama = 'AKG-MAL Antiport (AMA)'
    ama_wrap = 'AKG-MAL Antiport\n(AMA)'
    tca_flux = 'TCA flux (CS_m)'
    glycolysis = 'Glycolysis (GAPD_c)'
    lactate_production = 'LAC production (LDH_c)'
    lactate_ratio = f'{lactate_production} / {glycolysis}'
    tca_ratio = f'{tca_flux} / {glycolysis}'
    cma_tca_ratio = f'CMA / {tca_flux}'
    cma_ama_ratio = 'CMA / AMA'

    @staticmethod
    def fixed_flux_string_generator(fixed_value):
        return 'Fixed value: {:.1f}'.format(fixed_value)


class MetabolicNetworkConfig(object):
    common_experimental_mid_metabolite_set = {
        'GLC_c', 'FBP_c', 'DHAP_c', 'GAP_c', '3PG_c', 'PEP_c',
        'PYR_c', 'PYR_m', 'LAC_c', 'ALA_c', 'ERY4P_c',
        'CIT_m', 'MAL_m', 'AKG_m', 'SUC_m', 'ASP_m',
        'SER_c', 'GLY_c', 'ASP_c', 'CIT_c', 'MAL_c',
        'GLU_m', 'GLN_m', 'GLU_c', 'GLN_c', 'AKG_c', 'RIB5P_c'
    }
    common_experimental_mixed_mid_metabolite_set = {
        'PYR_c', 'PYR_m', 'CIT_m', 'CIT_c', 'MAL_m', 'MAL_c',
        'GLU_m', 'GLU_c', 'GLN_m', 'GLN_c', 'ASP_m', 'ASP_c',
        'AKG_m', 'AKG_c',
    }
    common_biomass_metabolite_set = {
        'ALA_c', 'RIB5P_c', 'GLY_c', 'SER_c', 'ASP_c',
        'ACCOA_c', 'GLU_c', 'GLN_c',
    }
    common_input_metabolite_set = {
        'GLC_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e',
    }
    infusion_input_metabolite_set = {
        'GLC_e', 'GLC_unlabelled_e', 'GLN_e', 'ASP_e', 'SER_e', 'GLY_e', 'ALA_e', 'LAC_e',
    }
    common_c13_labeling_metabolite_set = {
        'GLC_e',
    }
    common_boundary_flux_set = {
        'GLC_input'
    }
    infusion_boundary_flux_set = {
        'GLC_input', 'GLC_unlabelled_input'
    }
    common_diagram_network_setting_dict = {
        ParameterName.input_metabolite_set: common_input_metabolite_set,
        ParameterName.c13_labeling_metabolite_set: common_c13_labeling_metabolite_set,
        ParameterName.mid_data_metabolite_set: common_experimental_mid_metabolite_set,
        ParameterName.mixed_mid_data_metabolite_set:
            common_experimental_mixed_mid_metabolite_set,
        ParameterName.biomass_metabolite_set: common_biomass_metabolite_set,
        ParameterName.boundary_flux_set: common_boundary_flux_set,
        # ParameterName.reaction_raw_value_dict: {'GLC_input': 200},
        ParameterName.reaction_text_dict: {'GLC_input': CommonFigureString.fixed_flux_string_generator(200)},
        ParameterName.reaction_text_config_dict: {ParameterName.font_weight: FontWeight.bold},
    }
    common_data_flux_network_setting_dict = {}
    common_scale = 0.35
    # scale_with_legend = 1
    # total_width_with_legend = 1.35
    # height_to_width_ratio = 0.66
    # height_to_width_ratio = network_height_to_width_ratio / total_width_with_legend
    # legend_offset = Vector(1, 0)

    exchange_flux_alpha_dict = {
        ParameterName.alpha: 0.7
    }
    exchange_diagram_network_config = {
        ParameterName.extra_parameter_dict: {
            'CIT_trans': dict(exchange_flux_alpha_dict),
            'AKGMAL_m': dict(exchange_flux_alpha_dict),
            'ASPTA_m': dict(exchange_flux_alpha_dict),
            'ASPTA_c': dict(exchange_flux_alpha_dict),
        }
    }
    normal_network_display_text_dict = {
        'GLC_input': CommonFigureString.glc_input,
        'GLN_input': CommonFigureString.gln_input,
        'LDH_c': 'LDH_c',
        'CS_m': 'CS_m',
        'GAPD_PGK_c': 'GAPD_c',
    }
    exchange_network_display_text_dict = {
        'CIT_trans': CommonFigureString.cma_wrap,
        'AKGMAL_m': CommonFigureString.ama_wrap,
    }


class ProtocolSearchingMaterials(object):
    all_data_target_optimization_size = 5000
    all_data_target_selection_size = 100
    all_data_target_selection_ratio = all_data_target_selection_size / all_data_target_optimization_size

    experimental_data_target_optimization_size = 20000
    experimental_data_target_selection_size = 100
    experimental_data_target_selection_ratio = experimental_data_target_selection_size / \
        experimental_data_target_optimization_size

    all_data_text_comment_config_dict = {
        ParameterName.reaction_flux_num: 85,
        ParameterName.total_flux_num: 85,
        ParameterName.total_mid_num: 42,
        ParameterName.mid_metabolite_num: 42,
    }
    experimental_data_text_comment_config_dict = {
        ParameterName.reaction_flux_num: 85,
        ParameterName.total_flux_num: 105,
        ParameterName.total_mid_num: 22,
        ParameterName.mid_metabolite_num: 42,
    }


class ModelDataSensitivityDataFigureConfig(object):
    raw_data_str = 'raw_data'
    all_data_str = 'all_data'
    noise_str = '_noise'

    @staticmethod
    def modify_all_data_to_raw_data(raw_label: str):
        return raw_label.replace(
            ModelDataSensitivityDataFigureConfig.all_data_str, ModelDataSensitivityDataFigureConfig.raw_data_str)

    @staticmethod
    def modify_noise_data_to_raw_data(raw_label: str):
        return raw_label.replace(ModelDataSensitivityDataFigureConfig.noise_str, '')

    model_sensitivity_dict = {
        DataName.merge_reversible_reaction: None,
        DataName.combine_consecutive_reactions: None,
        DataName.prune_branches: None,
    }

    model_sensitivity_all_data_dict = {
        DataName.merge_reversible_reaction_all_data: None,
        DataName.combine_consecutive_reactions_all_data: None,
        DataName.prune_branches_all_data: None,
    }

    data_sensitivity_label_dict = {
        DataName.data_sensitivity: None,
        DataName.data_sensitivity_with_noise: None,
    }

    data_sensitivity_dict = {
        DataName.smaller_data_size: None,
        DataName.data_without_pathway: None,
        DataName.compartmental_data: None,
    }

    config_sensitivity_dict = {
        DataName.different_constant_flux: None,
        # DataName.different_flux_range: None,
    }
    config_sensitivity_constant_flux_with_noise_only_dict = {
        DataName.different_constant_flux_with_noise: None,
    }

    title_dict = {
        DataName.smaller_data_size: CommonFigureString.smaller_data_size,
        DataName.data_without_pathway: CommonFigureString.data_without_pathway,
        DataName.different_constant_flux: CommonFigureString.different_constant_flux,
        DataName.model_sensitivity: CommonFigureString.model_sensitivity,
        DataName.data_sensitivity: CommonFigureString.data_sensitivity,
        DataName.config_sensitivity: CommonFigureString.config_sensitivity,
    }
    title_with_order_prefix = {
        DataName.smaller_data_size: CommonFigureString.smaller_data_size_with_order_prefix,
        DataName.data_without_pathway: CommonFigureString.data_without_pathway_with_order_prefix,
        DataName.compartmental_data: CommonFigureString.compartmental_data_with_order_prefix,
        # DataName.different_constant_flux: CommonFigureString.different_constant_flux_with_order_prefix,
        DataName.model_sensitivity: CommonFigureString.model_sensitivity_with_order_prefix,
        DataName.data_sensitivity: CommonFigureString.data_sensitivity_with_order_prefix,
        DataName.config_sensitivity: CommonFigureString.config_sensitivity_with_order_prefix,
        DataName.different_flux_range: CommonFigureString.different_flux_range_with_order_prefix,
        DataName.different_constant_flux: CommonFigureString.different_constant_flux_with_order_prefix,
    }

    # raw_data_result_label = 'raw_model__raw_data'
    # all_data_result_label = 'raw_model__all_data'
    # raw_data_noise_result_label = 'raw_model__raw_data_noise'
    # all_data_noise_result_label = 'raw_model__all_data_noise'
    raw_data_result_label = DataName.raw_data_result_label
    all_data_result_label = DataName.all_data_result_label
    raw_data_noise_result_label = DataName.raw_data_noise_result_label
    all_data_noise_result_label = DataName.all_data_noise_result_label
    raw_model_data_label_dict = {
        raw_data_result_label: None,
        all_data_result_label: None,
        raw_data_noise_result_label: None,
        all_data_noise_result_label: None,
    }

    group_id_name_dict = {
        DataName.merge_reversible_reaction: CommonFigureString.merge_reversible_reactions_wrap_with_order_prefix,
        DataName.combine_consecutive_reactions: CommonFigureString.combine_consecutive_reactions_wrap_with_order_prefix,
        DataName.prune_branches: CommonFigureString.miss_branch_pathways_wrap_with_order_prefix,
        'glycolysis': 'Glycolysis',
        'ser_gly': 'Ser-Gly',
        'tca': 'TCA cycle',
        'aa': 'AA',
        'ppp': 'PPP',
        'exchange': 'Transfer and\nexchange fluxes',
        # 'even': 'Evenly\ndistributed',
        # 'pathway': 'Pathway\nspecific',

        DataName.smaller_data_size: CommonFigureString.smaller_data_size_wrap_with_order_prefix,
        DataName.data_without_pathway: CommonFigureString.data_without_pathway_wrap_with_order_prefix,
        DataName.compartmental_data: CommonFigureString.compartmental_data_wrap_with_order_prefix,
        DataName.few_data: 'Few data',
        DataName.medium_data: 'Medium data',
        # DataName.data_without_ppp: 'Without PPP',
        # DataName.data_without_aa: 'Without AA',
        # DataName.data_without_tca: 'Without TCA',
        DataName.data_without_ppp: 'Remove PPP',
        DataName.data_without_aa: 'Remove AA',
        DataName.data_without_tca: 'Remove TCA',
        DataName.medium_data_without_combination: 'Experimental compartmental data',
        DataName.different_constant_flux: CommonFigureString.different_constant_flux_wrap_with_order_prefix,
        DataName.different_constant_flux_with_noise: CommonFigureString.different_constant_flux_wrap_with_order_prefix,
        DataName.different_flux_range: CommonFigureString.different_flux_range_wrap_with_order_prefix,
        raw_data_result_label: {
            DataName.model_sensitivity: CommonFigureString.raw_model,
            DataName.data_sensitivity: CommonFigureString.experimental_available_mid_data,
            DataName.config_sensitivity: CommonFigureString.raw_config_bound_input_flux,
        },
        all_data_result_label: {
            DataName.model_sensitivity: CommonFigureString.raw_model,
            DataName.data_sensitivity: 'All compartmental data',
            DataName.config_sensitivity: CommonFigureString.raw_config_bound_input_flux,
        },
    }

    label_dict = {
        DataName.model_sensitivity: {
            DataName.merge_reversible_reaction: {
                'glycolysis': {
                    'PGI__raw_data': 'PGI',
                    'FBA__raw_data': 'FBA',
                    'TPI__raw_data': 'TPI',
                    'GAPD__raw_data': 'GAPD',
                    'PGK__raw_data': 'PGK',
                    'PGM__raw_data': 'PGM',
                    'ENO__raw_data': 'ENO',
                    'LDH__raw_data': 'LDH',
                },
                'tca': {
                    'MDH_c__raw_data': 'MDH_c',
                    'ACONT__raw_data': 'ACONT',
                    'SUCD__raw_data': 'SUCD',
                    'FUMH__raw_data': 'FUMH',
                    'MDH_m__raw_data': 'MDH_m',
                },
                'aa': {
                    'GLUD_m__raw_data': 'GLUD_m',
                    'ASPTA_m__raw_data': 'ASPTA_m',
                    'ASPTA_c__raw_data': 'ASPTA_c',
                    'GPT__raw_data': 'GPT',
                },
                'ppp': {
                    'RPI__raw_data': 'RPI',
                    'RPE__raw_data': 'RPE',
                    'TKT1__raw_data': 'TKT1',
                    'TKT2__raw_data': 'TKT2',
                    'TALA__raw_data': 'TALA'
                },

            },
            DataName.combine_consecutive_reactions: {
                'glycolysis': {
                    'PGI_PFK_c__raw_data': 'PGI + PFK',
                    'GAPD_PGK_c__raw_data': 'GAPD + PGK',
                    'PGM_ENO_c__raw_data': 'PGM + ENO',
                },
                'tca': {
                    'ACONT_ICDH_m__raw_data': 'ACONT + ICDH',
                    'AKGD_SUCOAS_m__raw_data': 'AKGD + SUCOAS',
                    'SUCD_FUMH_m__raw_data': 'SUCD + FUMH',
                    'SUCD_FUMH_MDH_m__raw_data': 'SUCD + FUMH + MDH_m',
                },
            },
            DataName.prune_branches: {
                'ppp': {
                    'PPP_with_biomass__raw_data': 'With_biomass',
                    'PPP_without_biomass__raw_data': 'Without_biomass',
                },
                'ser_gly': {
                    'SG_with_biomass__raw_data': 'With_biomass',
                    'SG_without_biomass__raw_data': 'Without_biomass',
                },
                None: {
                    'no_compartment__raw_data': 'No compartment',
                }
            },
        },
        DataName.data_sensitivity: {
            DataName.smaller_data_size: {
                raw_data_result_label: group_id_name_dict[raw_data_result_label][DataName.data_sensitivity],
                f'raw_model__{DataName.medium_data}': group_id_name_dict[DataName.medium_data],
                f'raw_model__{DataName.few_data}': group_id_name_dict[DataName.few_data],
            },
            DataName.data_without_pathway: {
                f'raw_model__{DataName.data_without_ppp}': group_id_name_dict[DataName.data_without_ppp],
                f'raw_model__{DataName.data_without_aa}': group_id_name_dict[DataName.data_without_aa],
                f'raw_model__{DataName.data_without_tca}': group_id_name_dict[DataName.data_without_tca],
            },
            DataName.compartmental_data: {
                raw_data_result_label: group_id_name_dict[raw_data_result_label][DataName.data_sensitivity],
                f'raw_model__{DataName.medium_data_without_combination}':
                    group_id_name_dict[DataName.medium_data_without_combination],
                all_data_result_label: group_id_name_dict[all_data_result_label][DataName.data_sensitivity],
            }
        },
        DataName.config_sensitivity: {
            DataName.different_constant_flux: {
                1: {
                    'raw_model__raw_data__gln_only': 'GLN only',
                    'raw_model__raw_data__asp_only': 'ASP only',
                },
                2: {
                    'raw_model__raw_data__with_gln': 'GLC + GLN',
                    'raw_model__raw_data__with_asp': 'GLC + ASP',
                    'raw_model__raw_data__with_aa': 'GLC + AA',
                    'raw_model__raw_data__with_lac': 'GLC + LAC',
                },
                3: {
                    'raw_model__raw_data__with_gln_asp': 'GLC + GLN + ASP',
                    'raw_model__raw_data__with_gln_aa': 'GLC + GLN_input + AA',
                    'raw_model__raw_data__with_gln_lac': 'GLC + GLN + LAC',
                    'raw_model__raw_data__with_asp_lac': 'GLC + ASP + LAC',
                },
                4: {
                    'raw_model__raw_data__with_gln_asp_lac': 'GLC + GLN + ASP + LAC',
                    'raw_model__raw_data__with_all_exchange': 'GLC + GLN + ASP + AA + LAC',
                },
            },
            DataName.different_flux_range: {
                1: {
                    'raw_model__raw_data__low_lower_low_upper': 'Low LB + Low UB',
                    'raw_model__raw_data__low_lower_medium_upper': 'Low LB + Medium UB',
                    'raw_model__raw_data__low_lower_high_upper': 'Low LB + High UB',
                    'raw_model__raw_data__low_lower_ex_high_upper': 'Low LB + EX High UB',
                },
                2: {
                    'raw_model__raw_data__medium_lower_low_upper': 'Medium LB + Low UB',
                    'raw_model__raw_data__medium_lower_high_upper': 'Medium LB + High UB',
                    'raw_model__raw_data__medium_lower_ex_high_upper': 'Medium LB + EX High UB',
                },
                3: {
                    'raw_model__raw_data__high_lower_low_upper': 'High LB + Low UB',
                    'raw_model__raw_data__high_lower_medium_upper': 'High LB + Medium UB',
                    'raw_model__raw_data__high_lower_high_upper': 'High LB + High UB',
                    'raw_model__raw_data__high_lower_ex_high_upper': 'High LB + EX High UB',
                },
                4: {
                    'raw_model__raw_data__ex_high_lower_low_upper': 'EX High LB + Low UB',
                    'raw_model__raw_data__ex_high_lower_medium_upper': 'EX High LB + Medium UB',
                    'raw_model__raw_data__ex_high_lower_high_upper': 'EX High LB + High UB',
                    'raw_model__raw_data__ex_high_lower_ex_high_upper': 'EX High LB + EX High UB',
                },
            },
        },
    }
    # label_dict[DataName.config_sensitivity][DataName.different_constant_flux_with_noise] = {
    #     key: {
    #         raw_result_label.replace('raw_data', 'raw_data_noise'): tick_label
    #         for raw_result_label, tick_label in value_dict.items()
    #     }
    #     for key, value_dict in label_dict[DataName.config_sensitivity][DataName.different_constant_flux].items()
    # }
    x_tick_label_dict = {
        'glycolysis': {
            'HEX_c': 'HEX_c',
            'PGI_c__R_PGI_c': 'PGI_c Rnet',
            'PFK_c': 'PFK_c',
            'FBA_c_FBA_c__R': 'FBA_c net',
            'TPI_c_TPI_c__R': 'TPI_c net',
            'GAPD_c_GAPD_c__R': 'GAPD_c net',
            'PGK_c_PGK_c__R': 'PGK_c net',
            'PGM_c_PGM_c__R': 'PGM_c net',
            'ENO_c_ENO_c__R': 'ENO_c net',
            'PYK_c': 'PYK_c',
            'LDH_c_LDH_c__R': 'LDH_c net',
            'PEPCK_c': 'PEPCK_c',
            'ACITL_c': 'ACITL_c',
            'MDH_c__R_MDH_c': 'MDH_c Rnet',
            'ME2_c': 'ME2_c',
            'LIPID_c': 'LIPID_c',
        },
        'ser_gly': {
            'PHGDH_PSAT_PSP_c': 'PHGDH_c',
            'SHMT_c_SHMT_c__R': 'SHMT_c net',
            'SER_input': 'SER_input',
            'GLY_input': 'GLY_input',
        },
        'tca': {
            'PDH_m': 'PDH_m',
            'CS_m': 'CS_m',
            'ACONT_m_ACONT_m__R': 'ACONT_m net',
            'ICDH_m': 'ICDH_m',
            'AKGD_m': 'AKGD_m',
            'SUCOAS_m': 'SUCOAS_m',
            'SUCD_m_SUCD_m__R': 'SUCD_m net',
            'FUMH_m_FUMH_m__R': 'FUMH_m net',
            'MDH_m_MDH_m__R': 'MDH_m net',
            'PC_m': 'PC_m',
        },
        'aa': {
            'GLUD_m_GLUD_m__R': 'GLUD_m net',
            'GLND_m': 'GLND_m',
            'GLNS_c': 'GLNS_c',
            'ASPTA_m_ASPTA_m__R': 'ASPTA_m net',
            'AS_c': 'AS_c',
            'ASPTA_c_ASPTA_c__R': 'ASPTA_c net',
        },
        'ppp': {
            'G6PDH2R_PGL_GND_c': 'G6PDH2R_c',
            'RPI_c_RPI_c__R': 'RPI_c net',
            'RPE_c_RPE_c__R': 'RPE_c net',
            'TKT1_c_TKT1_c__R': 'TKT1_c net',
            'TKT2_c_TKT2_c__R': 'TKT2_c net',
            'TALA_c_TALA_c__R': 'TALA_c net',
            'Salvage_c': 'Salvage',
        },
        'exchange': {
            'PYR_trans_PYR_trans__R': 'PYR_trans net',
            'ASPGLU_m__R_ASPGLU_m': 'ASPGLU_m Rnet',
            'AKGMAL_m__R_AKGMAL_m': 'AKGMAL_m Rnet',
            'CIT_trans__R_CIT_trans': 'CIT_trans Rnet',
            'GLN_trans_GLN_trans__R': 'GLN_trans net',
            'GLU_trans__R_GLU_trans': 'GLU_trans Rnet',
            'GLC_input': 'GLC_input',
            'GLN_input': 'GLN_input',
            'ASP_input': 'ASP_input',
            'LAC_output': 'LAC_output',
            'ALA_input': 'ALA_input',
            'GPT_c_GPT_c__R': 'GPT_c net',
            'BIOMASS_REACTION': 'Biomass',
        },
    }


class DataSensitivityMetabolicNetworkConfig(object):
    smaller_size_data_sensitivity_dict = {
        'GLC_c': DataName.few_data,
        'FBP_c': DataName.raw_model_raw_data,
        'DHAP_c': DataName.raw_model_raw_data,
        '3PG_c': DataName.medium_data,
        'PEP_c': DataName.raw_model_raw_data,
        'PYR_c': DataName.few_data,
        'PYR_m': DataName.few_data,
        'LAC_c': DataName.few_data,
        'ALA_c': DataName.medium_data,
        'ERY4P_c': DataName.raw_model_raw_data,
        'CIT_m': DataName.medium_data,
        'CIT_c': DataName.medium_data,
        'MAL_m': DataName.raw_model_raw_data,
        'AKG_m': DataName.raw_model_raw_data,
        'SUC_m': DataName.few_data,
        'ASP_c': DataName.few_data,
        'ASP_m': DataName.few_data,
        'SER_c': DataName.few_data,
        'GLY_c': DataName.few_data,
        'MAL_c': DataName.raw_model_raw_data,
        'GLU_c': DataName.few_data,
        'GLU_m': DataName.few_data,
        'GLN_c': DataName.raw_model_raw_data,
        'GLN_m': DataName.raw_model_raw_data,
        'AKG_c': DataName.medium_data,
        'RIB5P_c': DataName.medium_data,
    }

    remove_pathway_data_sensitivity_dict = {
        'FBP_c': DataName.data_without_ppp,
        'ALA_c': DataName.data_without_aa,
        'ERY4P_c': DataName.data_without_ppp,
        'CIT_c': DataName.data_without_tca,
        'CIT_m': DataName.data_without_tca,
        'MAL_c': DataName.data_without_tca,
        'MAL_m': DataName.data_without_tca,
        'AKG_c': DataName.data_without_tca,
        'AKG_m': DataName.data_without_tca,
        'SUC_m': DataName.data_without_tca,
        'ASP_c': DataName.data_without_aa,
        'ASP_m': DataName.data_without_aa,
        'SER_c': DataName.data_without_aa,
        'GLY_c': DataName.data_without_aa,
        'GLU_c': DataName.data_without_aa,
        'GLU_m': DataName.data_without_aa,
        'GLN_c': DataName.data_without_aa,
        'GLN_m': DataName.data_without_aa,
        'RIB5P_c': DataName.data_without_ppp,
    }

    different_constant_flux_name_dict = {
        'GLC_input': 'GLC input',
        'GLN_input': 'GLN input',
        'ASP_input': 'ASP input',
        'SER_input': 'AA: SER input',
        'GLY_input': 'AA: GLY input',
        'LAC_output': 'LAC output',
    }

    few_data_list = [
        ['GLC_c', 'PYR_c/m', 'LAC_c', 'SUC_m', ],
        ['ASP_c/m', 'SER_c', 'GLY_c', 'GLU_c/m', ]
    ]
    medium_data_list = [
        ['2PG_c/3PG_c', 'CIT_c/m/ICIT_m', ],
        ['ALA_c', 'AKG_c', 'RIB5P_c', 'ASN_c', ],
    ]
    experimentally_available_data_list = [
        ['G6P_c/F6P_c', 'FBP_c', 'ERY4P_c', 'DHAP_c', ],
        ['PEP_c', 'MAL_c/m', 'AKG_m', 'GLN_c/m', ],
    ]
    other_data_example_list = [
        ['OAC_c/m', 'ACCOA_c/m']
    ]

    # ppp_removed_list = [
    #     ['G6P_c/F6P_c', 'FBP_c'],
    #     ['ERY4P_c', 'RIB5P_c'],
    # ]
    # tca_removed_list = [
    #     ['CIT_c/m/ICIT_m', '', 'FUM_m'],
    #     ['MAL_c/m', 'AKG_c/m', 'SUC_m'],
    # ]
    # aa_removed_list = [
    #     ['ALA_c', 'ASP_c/m'],
    #     ['ASN_c', 'SER_c', 'GLY_c'],
    #     ['GLU_c/m', 'GLN_c/m'],
    # ]

    other_metabolite_list = [
        ['GAP_c'],
        ['DHAP_c'],
        ['3PG_c'],
        ['PEP_c'],
        ['PYR_c/m'],
        ['LAC_c'],
    ]

    ppp_removed_list = [
        ['G6P_c/F6P_c'],
        ['FBP_c'],
        ['ERY4P_c'],
        ['RIB5P_c'],
    ]
    tca_removed_list = [
        ['CIT_c/m/ICIT_m'],
        ['FUM_m'],
        ['MAL_c/m'],
        ['AKG_c/m'],
        ['SUC_m'],
    ]
    aa_removed_list = [
        ['ALA_c'],
        ['ASP_c/m'],
        ['ASN_c'],
        ['SER_c'],
        ['GLY_c'],
        ['GLU_c/m'],
        ['GLN_c/m'],
    ]

    experimentally_available_data_list_without_compartments = [
        [''],
        ['PYR_c/m'],
        ['ASP_c/m'],
        ['GLU_c/m'],
        ['2PG_c/3PG_c'],
        [''],
        ['CIT_c/m/ICIT_m'],
        [''],
        ['G6P_c/F6P_c'],
        ['MAL_c/m'],
        ['GLN_c/m'],
        [''],
    ]
    # experimentally_available_data_list_with_compartments = [
    #     ['PYR_c', 'PYR_m'],
    #     ['ASP_c', 'ASP_m'],
    #     ['GLU_c', 'GLU_m'],
    #     ['2PG_c', '3PG_c'],
    #     ['CIT_c', 'CIT_m', 'ICIT_m'],
    #     ['G6P_c', 'F6P_c'],
    #     ['MAL_c', 'MAL_m'],
    #     ['GLN_c', 'GLN_m'],
    # ]
    experimentally_available_data_list_with_compartments = [
        [''],
        ['PYR_c + PYR_m'],
        ['ASP_c + ASP_m'],
        ['GLU_c + GLU_m'],
        ['2PG_c + 3PG_c'],
        [''],
        ['CIT_c + CIT_m\n+ ICIT_m'],
        [''],
        ['G6P_c + F6P_c'],
        ['MAL_c + MAL_m'],
        ['GLN_c + GLN_m'],
        [''],
    ]
    all_available_data_list_with_compartments = [
        ['Other compartmentally\nmeasured metabolites\nsuch as:'],
        [''],
        ['OAC_c + OAC_m'],
        ['ACCOA_c + ACCOA_m'],
    ]

    different_constant_flux_string_list = [
        ['Glucose input (GLC)'],
        ['Glutamine input (GLN)'],
        ['Aspartate input (ASP)'],
        ['Serine input and glycine input (S/G)'],
        ['Lactate output (LAC)'],
    ]

    flux_lower_bound_string_list = [
        ['Low: 0.5'],
        ['Medium: 1'],
        ['High: 2'],
        ['EX high: 5'],
    ]
    flux_upper_bound_string_list = [
        ['Low: 500'],
        ['Medium: 1000'],
        ['High: 2000'],
        ['EX high: 5000'],
    ]


common_index_lim = (-0.1, 1.1)
common_index_ticks = (0, 0.5, 1)
larger_index_lim = (-2.05, 2.05)
larger_index_ticks = (-2, -1, 0, 1, 2)


def attach_feature_to_flux_name_list(flux_name_list, target_feature_dict):
    target_feature_list = []
    for row_list in flux_name_list:
        current_row_target_feature_list = []
        for flux_name in row_list:
            current_row_target_feature_list.append(target_feature_dict[flux_name])
        target_feature_list.append(current_row_target_feature_list)
    return target_feature_list


class CommonFigureMaterials(object):
    common_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color,
        ParameterName.optimized: ColorConfig.optimized_flux_color,
        ParameterName.experimental: ColorConfig.experimental_flux_color,
    }

    mid_comparison_color_dict = common_color_dict

    random_fluxes_str = 'Random solution'
    optimized_solution_str = 'Optimized solution'
    best_optimized_solution_str = 'Best optimized solution'
    global_optimum_str = 'Global optimal point'
    local_optimum_str = 'Local optimal point'
    random_point_str = 'Random point'

    mid_comparison_name_dict = {
        ParameterName.optimized: 'Optimized MID',
        ParameterName.experimental: 'Target experimental MID',
        ParameterName.unoptimized: 'MID from random flux',
    }
    # histogram_color_dict = {
    #     key: common_color_dict[key] for key in (ParameterName.unoptimized, Keywords.optimized)
    # }
    histogram_color_dict = {
        ParameterName.unoptimized: common_color_dict[ParameterName.unoptimized],
        ParameterName.optimized: common_color_dict[ParameterName.optimized]
    }

    optimum_color_dict = {
        ParameterName.local_optimum: ColorConfig.optimized_flux_color_with_alpha,
        ParameterName.global_optimum: ColorConfig.global_optimum_color_with_alpha,
    }
    optimum_with_random_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color_with_alpha,
        **optimum_color_dict,
    }
    optimum_with_random_text_color_dict = {
        ParameterName.unoptimized: ColorConfig.random_flux_color,
        ParameterName.local_optimum: ColorConfig.optimized_flux_color,
        ParameterName.global_optimum: ColorConfig.global_optimum_color,
    }
    optimum_name_dict = {
        ParameterName.unoptimized: random_point_str,
        ParameterName.local_optimum: local_optimum_str,
        ParameterName.global_optimum: global_optimum_str,
    }
    best_and_other_optimized_solution_name_dict = {
        ParameterName.unoptimized: random_fluxes_str,
        ParameterName.local_optimum: optimized_solution_str,
        ParameterName.global_optimum: best_optimized_solution_str,
    }

    time_loss_name_dict = {
        ParameterName.optimized: optimized_solution_str,
        ParameterName.unoptimized: random_fluxes_str
    }

    distance_and_loss_color_dict = {
        ParameterName.loss: ColorConfig.loss_color,
        # ParameterName.distance: ColorConfig.to_optimal_distance_arrow_color,
        ParameterName.distance: ColorConfig.experimental_flux_color,
    }
    distance_and_loss_name_dict = {
        ParameterName.loss: 'Loss of solution',
        ParameterName.distance: 'Euclidean distance to\nthe best optimized solution'
    }

    default_mid_name_list = [
        ['GLC_c', 'FRU6P_c+GLC6P_c', 'E4P_c'],
        ['2PG_c+3PG_c', 'PEP_c', 'PYR_c+PYR_m', 'LAC_c'],
        ['CIT_c+CIT_m+ICIT_m', 'AKG_c+AKG_m', 'GLU_c+GLU_m'],
        ['SUC_m', 'FUM_m', 'MAL_c+MAL_m', 'ASP_c+ASP_m']
    ]

    # common_flux_location_nested_list = [
    #     ['FBA_c - FBA_c__R', 'G6PDH2R_PGL_GND_c', 'LDH_c - LDH_c__R'],
    #     ['PDH_m', 'CS_m', 'ICDH_m'],
    #     ['AKGD_m', 'FUMH_m - FUMH_m__R', 'MDH_m - MDH_m__R'],
    # ]

    protocol_sensitivity_display_flux_list = [
        ['FBA_c_FBA_c__R', 'G6PDH2R_PGL_GND_c', 'LDH_c_LDH_c__R', 'PHGDH_PSAT_PSP_c'],
        ['CS_m', 'ICDH_m', 'SUCD_m_SUCD_m__R', 'MDH_m_MDH_m__R'],
    ]


common_display_flux_dict = {
    'GLC_input': CommonFigureString.glc_input,
    'GLN_input': CommonFigureString.gln_input,
    'CS_m': CommonFigureString.tca_flux,
    # 'LDH_c - LDH_c__R': 'LAC production (LDH_c)',
    'LDH_c - LDH_c__R': CommonFigureString.lactate_production,
    'CIT_trans - CIT_trans__R': 'CIT_m to CIT_c',
    'CIT_trans__R - CIT_trans': CommonFigureString.cma,
    'AKGMAL_m__R - AKGMAL_m': CommonFigureString.ama,
    'MDH_c - MDH_c__R': 'MAL_c to OAC_c',
    # 'ACITL_c': 'CIT_c to OAC_c',
    'ACITL_c': 'ACITL',
    'PEPCK_c': 'OAC_c to PEP',
    'cancer_index': CommonFigureString.lactate_ratio,
    'tca_index': CommonFigureString.tca_ratio,
    # 'non_canonical_tca_index': 'Non-canonical / total TCA flux',
    'non_canonical_tca_index': CommonFigureString.cma_tca_ratio,
    'mas_index': CommonFigureString.cma_ama_ratio,
    'HEX_c': 'GLC_input'
}


class PHGDHRawMaterials(object):
    diagram_network_config_dict = {
        **MetabolicNetworkConfig.common_diagram_network_setting_dict,
    }
    data_flux_network_setting_dict = {
        **MetabolicNetworkConfig.common_data_flux_network_setting_dict,
        ParameterName.absolute_value_output_value_dict: {
            0: 0.05,
            50: 0.55,
            200: 0.8,
            350: 1,
        }
    }


class ColonCancerRawMaterials(object):
    target_mid_name_list = [
        ['GLC_c', 'E4P_c', 'PEP_c', 'PYR_c+PYR_m', ],
        ['LAC_c', 'CIT_c+CIT_m+ICIT_m', 'AKG_c+AKG_m', 'GLU_c+GLU_m'],
        ['SUC_m', 'FUM_m', 'MAL_c+MAL_m', 'ASP_c+ASP_m']
    ]
    flux_name_location_list = [
        ['GLC_input', 'GLN_input'],
        ['LDH_c - LDH_c__R', 'CS_m'],
        # , 'ACITL_c'
        ['cancer_index', 'tca_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_dict = {
        'GLC_input': (0, 250),
        'GLN_input': (0, 250),
        'HEX_c': (0, 500),
        'LDH_c - LDH_c__R': (-20, 400),
        'CS_m': (-10, 300),
        'CIT_trans__R - CIT_trans': (-40, 200),
        'AKGMAL_m__R - AKGMAL_m': (-10, 150),
        'MDH_c - MDH_c__R': (-300, 100),
        'ACITL_c': (-40, 250),
        'PEPCK_c': (-2, 60),
        'cancer_index': common_index_lim,
        'non_canonical_tca_index': common_index_lim,
        'tca_index': common_index_lim,
        # 'mas_index': (-20, 150),
        'mas_index': (-10, 30),
    }
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, y_lim_dict)
    y_ticks_dict = {
        'GLC_input': (0, 50, 100, 150, 200, 250),
        'GLN_input': (0, 50, 100, 150, 200, 250),
        'HEX_c': (0, 100, 200, 300, 400, 500),
        'LDH_c - LDH_c__R': (0, 100, 200, 300, 400),
        'CS_m': (0, 100, 200, 300),
        'CIT_trans__R - CIT_trans': (0, 50, 100, 150, 200),
        'AKGMAL_m__R - AKGMAL_m': (0, 50, 100, 150),
        'MDH_c - MDH_c__R': (-300, -200, -100, 0, 100),
        'ACITL_c': (0, 100, 200),
        'PEPCK_c': (0, 20, 40, 60),
        'cancer_index': common_index_ticks,
        'non_canonical_tca_index': common_index_ticks,
        'tca_index': common_index_ticks,
        # 'mas_index': (0, 50, 100, 150),
        'mas_index': [-10, 0, 10, 20, 30],
    }
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, y_ticks_dict)
    cell_line_name_list = [
        'SW48-P2',
        'SW948-P3',
        'HCT116-P3',
        'NCI-H5087',
        'SW620-P3',
        'HT29',
        'HCT8-P5',
        'SW480',
    ]
    cell_line_display_name_dict = {
        'SW48-P2': 'SW48',
        'SW948-P3': 'SW948',
        'HCT116-P3': 'HCT116',
        'NCI-H5087': 'NCI',
        'SW620-P3': 'SW620',
        'HT29': 'HT29',
        'HCT8-P5': 'HCT8',
        'SW480': 'SW480',
    }
    hct116_high_str = 'HCT116 normal glucose'
    mid_name_dict = {
        ParameterName.optimized: f'{hct116_high_str}\nOptimized MID',
        ParameterName.experimental: f'{hct116_high_str}\nExperimental MID',
    }
    mid_color_dict = {
        ParameterName.optimized: CommonFigureMaterials.mid_comparison_color_dict[ParameterName.optimized],
        ParameterName.experimental: CommonFigureMaterials.mid_comparison_color_dict[ParameterName.experimental],
    }
    color_dict = {
        Keywords.high_glucose: ColorConfig.normal_blue,
        Keywords.low_glucose: ColorConfig.orange,
    }
    name_dict = {
        Keywords.high_glucose: 'Normal glucose',
        Keywords.low_glucose: 'Low glucose',
    }
    loss_y_lim = [0, 6.50001]
    loss_y_ticks = np.arange(*loss_y_lim, 0.5)
    loss_y_tick_labels = ['{:.1f}'.format(y_tick) for y_tick in loss_y_ticks]
    metabolic_network_config_dict = {
        **MetabolicNetworkConfig.common_diagram_network_setting_dict,
        ParameterName.boundary_flux_set: 'ASP_input',
        # ParameterName.reaction_raw_value_dict: {'ASP_input': 100},
        ParameterName.reaction_text_dict: {'ASP_input': CommonFigureString.fixed_flux_string_generator(100)},
        ParameterName.absolute_value_output_value_dict: {
            0: 0.03,
            20: 0.4,
            50: 0.65,
            100: 0.7,
            200: 0.9,
            500: 1,
        }
    }
    normal_network_fixed_flux_string_dict = {'ASP_input': CommonFigureString.fixed_flux_string_generator(100)}
    common_diagram_network_config_dict = {
        **MetabolicNetworkConfig.common_diagram_network_setting_dict,
        ParameterName.boundary_flux_set: 'ASP_input',
        # ParameterName.reaction_raw_value_dict: {'ASP_input': 100},
        # ParameterName.reaction_text_dict: {'ASP_input': CommonFigureString.fixed_flux_string_generator(100)},
    }
    diagram_network_config_dict = {
        ParameterName.normal_network: {
            **common_diagram_network_config_dict,
            ParameterName.reaction_text_dict: {
                **normal_network_fixed_flux_string_dict,
                **MetabolicNetworkConfig.normal_network_display_text_dict,
            },
        },
        ParameterName.exchange_network: {
            **common_diagram_network_config_dict,
            **MetabolicNetworkConfig.exchange_diagram_network_config,
            ParameterName.reaction_text_dict: MetabolicNetworkConfig.exchange_network_display_text_dict,
        }
    }
    data_flux_network_config_dict = {
        **MetabolicNetworkConfig.common_data_flux_network_setting_dict,
        ParameterName.absolute_value_output_value_dict: {
            0: 0.05,
            50: 0.55,
            200: 0.8,
            350: 1,
        }
    }


class ColonCancerRatioMaterials(ColonCancerRawMaterials):
    flux_name_location_list = [
        ['CIT_trans__R - CIT_trans', 'AKGMAL_m__R - AKGMAL_m'],
        ['non_canonical_tca_index', 'mas_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, ColonCancerRawMaterials.y_lim_dict)
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, ColonCancerRawMaterials.y_ticks_dict)


class KidneyCarcinomaRawMaterials(object):
    # flux_name_location_list = [
    #     ['GLC_input', 'LDH_c - LDH_c__R', 'CIT_trans - CIT_trans__R', 'MDH_c - MDH_c__R', ],
    #     ['ACITL_c', 'PEPCK_c', 'cancer_index', 'non_canonical_tca_index', ],
    # ]
    target_mid_name_list = [
        ['3PG_c', 'PYR_c+PYR_m', 'LAC_c', 'ALA_c'],
        ['SER_c', 'GLU_c+GLU_m', 'GLN_c+GLN_m'],
        ['SUC_m', 'FUM_m', 'MAL_c+MAL_m', 'ASP_c+ASP_m']
    ]
    normal_tissue_str = 'Normal tissue'
    carcinoma_str = 'Carcinoma'
    p1_normal_tissue_str = f'Patient 1: {normal_tissue_str}'
    p1_carcinoma_str = f'Patient 1: {carcinoma_str}'
    mid_name_dict = {
        ParameterName.optimized: f'{p1_normal_tissue_str}\nOptimized MID',
        ParameterName.experimental: f'{p1_normal_tissue_str}\nExperimental MID',
    }
    mid_color_dict = {
        ParameterName.optimized: CommonFigureMaterials.mid_comparison_color_dict[ParameterName.optimized],
        ParameterName.experimental: CommonFigureMaterials.mid_comparison_color_dict[ParameterName.experimental],
    }
    flux_name_location_list = [
        ['GLC_input', 'GLN_input'],
        ['LDH_c - LDH_c__R', 'CS_m'],
        ['cancer_index', 'tca_index'],
    ]
    loss_y_lim = [0, 0.250001]
    loss_y_ticks = np.arange(*loss_y_lim, 0.05)
    loss_y_tick_labels = ['{:.2f}'.format(y_tick) for y_tick in loss_y_ticks]
    display_flux_name_dict = common_display_flux_dict
    y_lim_dict = {
        'GLC_input': (0, 400),
        'GLN_input': (0, 160),
        'LDH_c - LDH_c__R': (-100, 300),
        'CS_m': (0, 310),
        'CIT_trans__R - CIT_trans': (-15, 100),
        'MDH_c - MDH_c__R': (-200, 200),
        'ACITL_c': (-10, 100),
        'PEPCK_c': (-2, 40),
        'cancer_index': common_index_lim,
        'tca_index': common_index_lim,
        'non_canonical_tca_index': common_index_lim,
        # 'mas_index': (-210, 210),
        'mas_index': (-1, 1),
        'AKGMAL_m__R - AKGMAL_m': (-210, 210)
    }
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, y_lim_dict)
    y_ticks_dict = {
        'GLC_input': (0, 100, 200, 300, 400),
        'GLN_input': (0, 50, 100, 150),
        'LDH_c - LDH_c__R': (-100, 0, 100, 200, 300),
        'CS_m': (0, 100, 200, 300),
        'CIT_trans__R - CIT_trans': (0, 20, 40, 60, 80, 100),
        'MDH_c - MDH_c__R': (-200, -100, 0, 100, 200),
        'ACITL_c': (0, 20, 40, 60, 80, 100),
        'PEPCK_c': (0, 10, 20, 30, 40),
        'cancer_index': common_index_ticks,
        'tca_index': common_index_ticks,
        'non_canonical_tca_index': common_index_ticks,
        # 'mas_index': (-200, -100, 0, 100, 200),
        'mas_index': [-1, -0.5, 0, 0.5, 1],
        'AKGMAL_m__R - AKGMAL_m': (-200, -100, 0, 100, 200)
    }
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, y_ticks_dict)
    # class_display_name_dict = {
    #     Keywords.kidney: 'Normal tissue',
    #     Keywords.carcinoma: 'Carcinoma',
    # }
    class_display_name_dict = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
    }
    color_dict = {
        Keywords.kidney: ColorConfig.normal_blue,
        Keywords.carcinoma: ColorConfig.orange,
    }
    name_dict = {
        Keywords.kidney: normal_tissue_str,
        Keywords.carcinoma: carcinoma_str,
    }
    flux_value_mapper_dict = {
            0: 0.03,
            20: 0.3,
            100: 0.75,
            200: 0.9,
            500: 1,
        }
    normal_network_fixed_flux_string_dict = {'ASP_input': CommonFigureString.fixed_flux_string_generator(50)}
    common_diagram_network_config_dict = {
        **MetabolicNetworkConfig.common_diagram_network_setting_dict,
        ParameterName.c13_labeling_metabolite_set: MetabolicNetworkConfig.common_c13_labeling_metabolite_set,
        ParameterName.mid_data_metabolite_set: {
            'PYR_c', 'PYR_m', 'LAC_c', 'ALA_c', 'SUC_m', 'FUM_m', 'SER_c',
            'MAL_m', 'MAL_c', 'ASP_c', 'ASP_m', 'GLU_m', 'GLN_m', 'GLU_c',
            'GLN_c', 'CIT_c', 'CIT_m', '3PG_c',
        },
        ParameterName.mixed_mid_data_metabolite_set: {
            'PYR_c', 'PYR_m', 'CIT_m', 'CIT_c', 'MAL_m', 'MAL_c',
            'GLU_m', 'GLU_c', 'GLN_m', 'GLN_c', 'ASP_m', 'ASP_c',
        },
        ParameterName.biomass_metabolite_set: MetabolicNetworkConfig.common_biomass_metabolite_set,
        ParameterName.input_metabolite_set: MetabolicNetworkConfig.infusion_input_metabolite_set,
        ParameterName.boundary_flux_set: 'ASP_input',
        # ParameterName.reaction_raw_value_dict: {'ASP_input': 50},
        ParameterName.absolute_value_output_value_dict: flux_value_mapper_dict
    }

    diagram_network_config_dict = {
        ParameterName.normal_network: {
            **common_diagram_network_config_dict,
            ParameterName.reaction_text_dict: {
                **normal_network_fixed_flux_string_dict,
                **MetabolicNetworkConfig.normal_network_display_text_dict,
            },
        },
        ParameterName.exchange_network: {
            **common_diagram_network_config_dict,
            **MetabolicNetworkConfig.exchange_diagram_network_config,
            ParameterName.reaction_text_dict: MetabolicNetworkConfig.exchange_network_display_text_dict,
        }
    }
    data_flux_network_config_dict = {
        **MetabolicNetworkConfig.common_data_flux_network_setting_dict,
        ParameterName.absolute_value_output_value_dict: flux_value_mapper_dict
    }


class KidneyCarcinomaRatioMaterials(KidneyCarcinomaRawMaterials):
    # flux_name_location_list = [
    #     ['GLC_input', 'LDH_c - LDH_c__R', 'CIT_trans - CIT_trans__R', 'MDH_c - MDH_c__R', ],
    #     ['ACITL_c', 'PEPCK_c', 'cancer_index', 'non_canonical_tca_index', ],
    # ]
    flux_name_location_list = [
        ['CIT_trans__R - CIT_trans', 'AKGMAL_m__R - AKGMAL_m'],
        ['non_canonical_tca_index', 'mas_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, KidneyCarcinomaRawMaterials.y_lim_dict)
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, KidneyCarcinomaRawMaterials.y_ticks_dict)


class MultipleTumorRawMaterials(object):
    # flux_name_location_list = [
    #     ['GLC_input', 'LDH_c - LDH_c__R', 'CIT_trans - CIT_trans__R', 'MDH_c - MDH_c__R', ],
    #     ['ACITL_c', 'PEPCK_c', 'cancer_index', 'non_canonical_tca_index', ],
    # ]
    # flux_name_location_list = [
    #     ['cancer_index', 'tca_index'],
    #     ['non_canonical_tca_index', 'mas_index'],
    # ]
    flux_name_location_list = [
        ['GLC_input', 'GLN_input'],
        ['LDH_c - LDH_c__R', 'CS_m'],
        ['cancer_index', 'tca_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    # y_lim_list = [
    #     [(0, 350), (-50, 450), (-100, 10), (-200, 200)],
    #     [(-10, 100), (-2, 40), (-0.05, 1.05), (-0.05, 1.05)],
    # ]
    y_lim_dict = {
        'GLC_input': (-20, 450),
        'GLN_input': (0, 150),
        'LDH_c - LDH_c__R': (-110, 310),
        'CS_m': (0, 530),
        'CIT_trans__R - CIT_trans': (-30, 100),
        'MDH_c - MDH_c__R': (-200, 200),
        'ACITL_c': (-10, 100),
        'PEPCK_c': (-2, 40),
        'cancer_index': common_index_lim,
        'tca_index': common_index_lim,
        'non_canonical_tca_index': common_index_lim,
        # 'mas_index': (-220, 220),
        'mas_index': (-2, 2),
        'AKGMAL_m__R - AKGMAL_m': (-220, 220),
    }
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, y_lim_dict)
    # y_ticks_list = [
    #     [(0, 100, 200, 300), (0, 100, 200, 300, 400), (-100, -80, -60, -40, -20, 0), (-200, -100, 0, 100, 200)],
    #     [(0, 20, 40, 60, 80, 100), (0, 10, 20, 30, 40), (0, 0.5, 1.0), (0, 0.5, 1.0)],
    # ]
    y_ticks_dict = {
        'GLC_input': (0, 100, 200, 300, 400),
        'GLN_input': (0, 50, 100, 150),
        'LDH_c - LDH_c__R': (-100, 0, 100, 200, 300),
        'CS_m': (0, 100, 200, 300, 400, 500),
        'CIT_trans__R - CIT_trans': (-20, 0, 20, 40, 60, 80, 100),
        'MDH_c - MDH_c__R': (-200, -100, 0, 100, 200),
        'ACITL_c': (0, 20, 40, 60, 80, 100),
        'PEPCK_c': (0, 10, 20, 30, 40),
        'cancer_index': common_index_ticks,
        'tca_index': common_index_ticks,
        'non_canonical_tca_index': common_index_ticks,
        # 'mas_index': (-200, -100, 0, 100, 200),
        'mas_index': (-2, 0, 2),
        'AKGMAL_m__R - AKGMAL_m': (-200, -100, 0, 100, 200),
    }
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, y_ticks_dict)
    class_display_name_dict = {
        Keywords.kidney: 'Kidney',
        Keywords.lung: 'Lung',
        Keywords.brain: 'Brain',
    }
    color_dict = {
        Keywords.kidney: ColorConfig.normal_blue,
        Keywords.lung: ColorConfig.orange,
        Keywords.brain: ColorConfig.purple,
    }


class MultipleTumorRatioMaterials(MultipleTumorRawMaterials):
    flux_name_location_list = [
        ['CIT_trans__R - CIT_trans', 'AKGMAL_m__R - AKGMAL_m'],
        ['non_canonical_tca_index', 'mas_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, MultipleTumorRawMaterials.y_lim_dict)
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, MultipleTumorRawMaterials.y_ticks_dict)


class MouseComparisonMaterials(object):
    flux_name_location_list = [
        ['cancer_index', 'tca_index'],
        ['non_canonical_tca_index', 'mas_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_dict = {
        'GLC_input': (0, 350),
        'LDH_c - LDH_c__R': (-50, 450),
        'CIT_trans - CIT_trans__R': (-100, 10),
        'MDH_c - MDH_c__R': (-200, 200),
        'ACITL_c': (-10, 100),
        'PEPCK_c': (-2, 40),
        'cancer_index': common_index_lim,
        'tca_index': common_index_lim,
        'non_canonical_tca_index': common_index_lim,
        'mas_index': (-10, 210),
    }
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, y_lim_dict)
    y_ticks_dict = {
        'GLC_input': (0, 100, 200, 300),
        'LDH_c - LDH_c__R': (0, 100, 200, 300, 400),
        'CIT_trans - CIT_trans__R': (-100, -80, -60, -40, -20, 0),
        'MDH_c - MDH_c__R': (-200, -100, 0, 100, 200),
        'ACITL_c': (0, 20, 40, 60, 80, 100),
        'PEPCK_c': (0, 10, 20, 30, 40),
        'cancer_index': common_index_ticks,
        'tca_index': common_index_ticks,
        'non_canonical_tca_index': common_index_ticks,
        'mas_index': (0, 100, 200),
    }
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, y_ticks_dict)
    class_display_name_dict = {
        Keywords.lung: 'Normal lung',
        Keywords.flank: 'Normal flank',
        Keywords.tumor: 'Tumor',
    }
    color_dict = {
        Keywords.lung: ColorConfig.normal_blue,
        Keywords.flank: ColorConfig.orange,
        Keywords.tumor: ColorConfig.purple,
    }


class LungCancerComparisonMaterials(object):
    flux_name_location_list = [
        ['cancer_index', 'tca_index'],
        ['non_canonical_tca_index', 'mas_index'],
    ]
    display_flux_name_dict = common_display_flux_dict
    y_lim_dict = {
        'GLC_input': (0, 350),
        'LDH_c - LDH_c__R': (-50, 450),
        'CIT_trans - CIT_trans__R': (-100, 10),
        'MDH_c - MDH_c__R': (-200, 200),
        'ACITL_c': (-10, 100),
        'PEPCK_c': (-2, 40),
        'cancer_index': common_index_lim,
        'tca_index': common_index_lim,
        'non_canonical_tca_index': common_index_lim,
        'mas_index': (-10, 210),
    }
    y_lim_list = attach_feature_to_flux_name_list(flux_name_location_list, y_lim_dict)
    y_ticks_dict = {
        'GLC_input': (0, 100, 200, 300),
        'LDH_c - LDH_c__R': (0, 100, 200, 300, 400),
        'CIT_trans - CIT_trans__R': (-100, -80, -60, -40, -20, 0),
        'MDH_c - MDH_c__R': (-200, -100, 0, 100, 200),
        'ACITL_c': (0, 20, 40, 60, 80, 100),
        'PEPCK_c': (0, 10, 20, 30, 40),
        'cancer_index': common_index_ticks,
        'tca_index': common_index_ticks,
        'non_canonical_tca_index': common_index_ticks,
        'mas_index': (0, 100, 200),
    }
    y_ticks_list = attach_feature_to_flux_name_list(flux_name_location_list, y_ticks_dict)
    class_display_name_dict = {
        Keywords.lung: 'Normal tissue',
        Keywords.tumor: 'Tumor',
    }
    color_dict = {
        Keywords.lung: ColorConfig.normal_blue,
        Keywords.tumor: ColorConfig.orange,
    }

