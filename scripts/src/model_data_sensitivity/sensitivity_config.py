from ..common.built_in_packages import ValueEnum
from ..common.config import Keywords as GeneralKeywords, FigureDataKeywords, BasicFigureData


raw_config_first = True


class RunningMode(ValueEnum):
    flux_analysis = 'flux_analysis'
    result_process = 'result_process'
    solver_output = 'solver_output'


class ExperimentName(ValueEnum):
    raw_model_raw_data = 'raw_model_raw_data'
    raw_model_all_data = 'raw_model_all_data'
    merge_reversible_reaction = 'merge_reversible_reaction'
    merge_reversible_reaction_all_data = 'merge_reversible_reaction_all_data'
    combine_consecutive_reactions = 'combine_consecutive_reactions'
    combine_consecutive_reactions_all_data = 'combine_consecutive_reactions_all_data'
    prune_branches = 'prune_branches'
    prune_branches_all_data = 'prune_branches_all_data'

    data_sensitivity = 'data_sensitivity'
    data_sensitivity_with_noise = 'data_sensitivity_with_noise'

    different_flux_range = 'different_flux_range'
    different_flux_range_all_data = 'different_flux_range_all_data'
    different_constant_flux = 'different_constant_flux'
    different_constant_flux_all_data = 'different_constant_flux_all_data'
    different_constant_flux_with_noise = 'different_constant_flux_with_noise'
    different_constant_flux_with_noise_all_data = 'different_constant_flux_with_noise_all_data'

    optimization_from_raw_data_average_solutions = 'optimization_from_raw_data_average_solutions'
    optimization_from_all_data_average_solutions = 'optimization_from_all_data_average_solutions'
    optimization_from_raw_data_average_solutions_with_squared_loss = 'optimization_from_raw_data_average_solutions_with_squared_loss'
    optimization_from_all_data_average_solutions_with_squared_loss = 'optimization_from_all_data_average_solutions_with_squared_loss'

    optimization_from_batched_simulated_raw_data = 'optimization_from_batched_simulated_raw_data'
    optimization_from_batched_simulated_all_data = 'optimization_from_batched_simulated_all_data'
    optimization_from_batched_simulated_raw_data_average_solutions = 'optimization_from_batched_simulated_raw_data_average_solutions'
    optimization_from_batched_simulated_all_data_average_solutions = 'optimization_from_batched_simulated_all_data_average_solutions'

    raw_model_raw_data_with_squared_loss = 'raw_model_raw_data_with_squared_loss'
    raw_model_all_data_with_squared_loss = 'raw_model_all_data_with_squared_loss'

    optimization_from_batched_simulated_raw_data_with_squared_loss = 'optimization_from_batched_simulated_raw_data_with_squared_loss'
    optimization_from_batched_simulated_all_data_with_squared_loss = 'optimization_from_batched_simulated_all_data_with_squared_loss'


class ModelSetting(ValueEnum):
    raw_model = 'raw_model'
    merge_reversible_reaction = 'merge_reversible_reaction'
    combine_consecutive_reactions = 'combine_consecutive_reactions'
    prune_branches = 'prune_branches'


class DataSetting(ValueEnum):
    raw_data = 'raw_data'
    all_data = 'all_data'
    raw_data_squared_loss = 'raw_data_squared_loss'
    all_data_squared_loss = 'all_data_squared_loss'
    medium_data_plus = 'medium_data_plus'
    medium_data = 'medium_data'
    few_data = 'few_data'
    data_without_ppp = 'data_without_ppp'
    data_without_aa = 'data_without_aa'
    data_without_tca = 'data_without_tca'
    medium_data_without_combination = 'data_without_combination'
    raw_data_batch = 'raw_data_batch'
    all_data_batch = 'all_data_batch'
    raw_data_batch_squared_loss = 'raw_data_batch_squared_loss'
    all_data_batch_squared_loss = 'all_data_batch_squared_loss'


squared_loss_data_dict = {
    DataSetting.raw_data: DataSetting.raw_data_squared_loss,
    DataSetting.all_data: DataSetting.all_data_squared_loss,
    DataSetting.raw_data_batch: DataSetting.raw_data_batch_squared_loss,
    DataSetting.all_data_batch: DataSetting.all_data_batch_squared_loss,
    ExperimentName.optimization_from_batched_simulated_raw_data: ExperimentName.optimization_from_batched_simulated_raw_data_with_squared_loss,
    ExperimentName.optimization_from_batched_simulated_all_data: ExperimentName.optimization_from_batched_simulated_all_data_with_squared_loss,
}


class ConfigSetting(ValueEnum):
    different_flux_range = 'different_flux_range'
    different_constant_flux = 'different_constant_flux'
    different_constant_flux_with_noise = 'different_constant_flux_with_noise'
    optimization_from_average_solutions = 'optimization_from_average_solutions'
    mean_squared_loss = 'mean_squared_loss'
    optimization_from_average_solutions_with_mean_squared_loss = f'{optimization_from_average_solutions}_{mean_squared_loss}'


class Keywords(GeneralKeywords):
    raw_type = 'raw'

    normal_result_process = 'normal_result_process'
    raw_model_result_process = 'raw_model_result_process'
    raw_model_averaged_optimization_result_process = 'raw_model_averaged_optimization_result_process'
    raw_model_batched_simulated_data_result_process = 'raw_model_different_simulated_data_result_process'
    raw_model_batched_simulated_data_averaged_optimization_result_process = 'raw_model_different_simulated_data_averaged_optimization_result_process'
    simulated_flux_value_dict = 'simulated_flux_value_dict'

    absolute_distance = 'absolute_distance'
    relative_distance = 'relative_distance'
    euclidean_distance = 'euclidean_distance'
    median = 'median'
    mean = 'mean'

    selection_size = 'selection_size'
    optimized_size = 'optimized_size'


model_data_config_dict = {
    ExperimentName.raw_model_raw_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.comment: 'Raw model, raw experimentally available MID data and normal config',
        },
    ExperimentName.raw_model_all_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.comment: 'Raw model, all available MID data and normal config',
        },
    ExperimentName.merge_reversible_reaction:
        {
            Keywords.model: ModelSetting.merge_reversible_reaction,
            Keywords.data: DataSetting.raw_data,
            Keywords.comment: 'Model with some reversible reactions are merged. '
                              'Raw experimentally available MID data and normal config',
        },
    ExperimentName.merge_reversible_reaction_all_data:
        {
            Keywords.model: ModelSetting.merge_reversible_reaction,
            Keywords.data: DataSetting.all_data,
            Keywords.comment: 'Model with some reversible reactions are merged. '
                              'All available MID data and normal config',
        },
    ExperimentName.combine_consecutive_reactions:
        {
            Keywords.model: ModelSetting.combine_consecutive_reactions,
            Keywords.data: DataSetting.raw_data,
            Keywords.comment: 'Model with some consecutive reactions are combined together. '
                              'Raw experimentally available MID data and normal config',
        },
    ExperimentName.combine_consecutive_reactions_all_data:
        {
            Keywords.model: ModelSetting.combine_consecutive_reactions,
            Keywords.data: DataSetting.all_data,
            Keywords.comment: 'Model with some consecutive reactions are combined together. '
                              'All available MID data and normal config',
        },
    ExperimentName.prune_branches:
        {
            Keywords.model: ModelSetting.prune_branches,
            Keywords.data: DataSetting.raw_data,
            Keywords.comment: 'Model with some reactions are removed. '
                              'Raw experimentally available MID data and normal config',
        },
    ExperimentName.prune_branches_all_data:
        {
            Keywords.model: ModelSetting.prune_branches,
            Keywords.data: DataSetting.all_data,
            Keywords.comment: 'Model with some reactions are removed. '
                              'All available MID data and normal config',
        },
    ExperimentName.data_sensitivity:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: [
                DataSetting.all_data,
                DataSetting.raw_data,
                # DataSetting.medium_data_plus,
                DataSetting.medium_data,
                DataSetting.few_data,
                DataSetting.data_without_ppp,
                DataSetting.data_without_aa,
                DataSetting.data_without_tca,
                DataSetting.medium_data_without_combination,
            ],
            Keywords.comment: 'Raw model, different availability of MID data and normal config',
        },
    ExperimentName.data_sensitivity_with_noise:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: [
                (DataSetting.all_data, True),
                (DataSetting.raw_data, True),
                # (DataSetting.medium_data_plus, True),
                (DataSetting.medium_data, True),
                (DataSetting.few_data, True),
                (DataSetting.data_without_ppp, True),
                (DataSetting.data_without_aa, True),
                (DataSetting.data_without_tca, True),
                (DataSetting.medium_data_without_combination, True),
            ],
            Keywords.comment: 'Raw model, different availability of MID data with noise and normal config',
        },
    ExperimentName.different_flux_range:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.config: ConfigSetting.different_flux_range,
            Keywords.comment: 'Raw model, raw experimentally available MID data, '
                              'and constraints of flux range is varied',
        },
    ExperimentName.different_flux_range_all_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.config: ConfigSetting.different_flux_range,
            Keywords.comment: 'Raw model, All available MID data, '
                              'and constraints of flux range is varied',
        },
    ExperimentName.different_constant_flux:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.config: ConfigSetting.different_constant_flux,
            Keywords.comment: 'Raw model, raw experimentally available MID data, '
                              'and constant flux is varied',
        },
    ExperimentName.different_constant_flux_all_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.config: ConfigSetting.different_constant_flux,
            Keywords.comment: 'Raw model, all available MID data, '
                              'and constant flux is varied',
        },
    ExperimentName.different_constant_flux_with_noise:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: (DataSetting.raw_data, True),
            Keywords.config: ConfigSetting.different_constant_flux,
            Keywords.comment: 'Raw model, raw experimentally available MID data with noise, '
                              'and constant flux is varied',
        },
    ExperimentName.different_constant_flux_with_noise_all_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: (DataSetting.all_data, True),
            Keywords.config: ConfigSetting.different_constant_flux,
            Keywords.comment: 'Raw model, all available MID data with noise, '
                              'and constant flux is varied',
        },
    ExperimentName.optimization_from_all_data_average_solutions:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.config: ConfigSetting.optimization_from_average_solutions,
            Keywords.comment: 'Raw model, all available MID data, optimization from averaged solutions',
        },
    ExperimentName.optimization_from_raw_data_average_solutions:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.config: ConfigSetting.optimization_from_average_solutions,
            Keywords.comment: 'Raw model, raw experimentally available MID data, optimization from averaged solutions',
        },
    ExperimentName.optimization_from_all_data_average_solutions_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.config: ConfigSetting.optimization_from_average_solutions_with_mean_squared_loss,
            Keywords.comment: 'Raw model, all available MID data, optimization from averaged solutions with Mean Square Loss',
        },
    ExperimentName.optimization_from_raw_data_average_solutions_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.config: ConfigSetting.optimization_from_average_solutions_with_mean_squared_loss,
            Keywords.comment: 'Raw model, raw experimentally available MID data, optimization from averaged solutions with Mean Square Loss',
        },
    ExperimentName.optimization_from_batched_simulated_all_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data_batch,
            Keywords.comment: 'Raw model, all available MID data, multiple simulated data',
        },
    ExperimentName.optimization_from_batched_simulated_raw_data:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data_batch,
            Keywords.comment: 'Raw model, raw experimentally available MID data, multiple simulated data',
        },
    ExperimentName.optimization_from_batched_simulated_all_data_average_solutions:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data_batch,
            Keywords.config: ConfigSetting.optimization_from_average_solutions,
            Keywords.comment: 'Raw model, all available MID data, multiple simulated data, optimization from averaged solutions',
        },
    ExperimentName.optimization_from_batched_simulated_raw_data_average_solutions:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data_batch,
            Keywords.config: ConfigSetting.optimization_from_average_solutions,
            Keywords.comment: 'Raw model, raw experimentally available MID data, multiple simulated data, optimization from averaged solutions',
        },
    ExperimentName.raw_model_raw_data_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data,
            Keywords.config: ConfigSetting.mean_squared_loss,
            Keywords.comment: 'Raw model, raw experimentally available MID data and optimization with Mean Square Loss',
        },
    ExperimentName.raw_model_all_data_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data,
            Keywords.config: ConfigSetting.mean_squared_loss,
            Keywords.comment: 'Raw model, all available MID data and optimization with Mean Square Loss',
        },
    ExperimentName.optimization_from_batched_simulated_raw_data_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.raw_data_batch,
            Keywords.config: ConfigSetting.mean_squared_loss,
            Keywords.comment: 'Raw model, all available MID data, multiple simulated data with Mean Square Loss',
        },
    ExperimentName.optimization_from_batched_simulated_all_data_with_squared_loss:
        {
            Keywords.model: ModelSetting.raw_model,
            Keywords.data: DataSetting.all_data_batch,
            Keywords.config: ConfigSetting.mean_squared_loss,
            Keywords.comment: 'Raw model, all available MID data, multiple simulated data with Mean Square Loss',
        },
}


merged_reaction_dict = {
    'PGI': 'PGI_c',
    'FBA': 'FBA_c',
    'TPI': 'TPI_c',
    'GAPD': 'GAPD_c',
    'PGK': 'PGK_c',
    'PGM': 'PGM_c',
    'ENO': 'ENO_c',
    'LDH': 'LDH_c',
    'MDH_c': 'MDH_c',
    'ACONT': 'ACONT_m',
    'SUCD': 'SUCD_m',
    'FUMH': 'FUMH_m',
    'MDH_m': 'MDH_m',
    'GLUD_m': 'GLUD_m',
    'ASPTA_m': 'ASPTA_m',
    'ASPTA_c': 'ASPTA_c',
    'GPT': 'GPT_c',
    'RPI': 'RPI_c',
    'RPE': 'RPE_c',
    'TKT1': 'TKT1_c',
    'TKT2': 'TKT2_c',
    'TALA': 'TALA_c'
}

consecutive_reaction_dict = {
    ('PGI_c', 'PFK_c'):
        {
            'id': 'PGI_PFK_c',
            'sub': [('GLC6P_c', 'abcdef')],
            'pro': [('FRU16BP_c', 'abcdef')],
        },
    ('GAPD_c', 'PGK_c'):
        {
            'id': 'GAPD_PGK_c',
            'sub': [('GAP_c', 'abc')],
            'pro': [('3PG_c', 'abc')],
            'reverse': True
        },
    ('PGM_c', 'ENO_c'):
        {
            'id': 'PGM_ENO_c',
            'sub': [('3PG_c', 'abc')],
            'pro': [('PEP_c', 'abc')],
            'reverse': True
        },
    ('ACONT_m', 'ICDH_m'):
        {
            'id': 'ACONT_ICDH_m',
            'sub': [('CIT_m', 'abcdef')],
            'pro': [('AKG_m', 'abcef'), ('CO2', 'd')],
        },
    ('AKGD_m', 'SUCOAS_m'):
        {
            'id': 'AKGD_SUCOAS_m',
            'sub': [('AKG_m', 'abcde')],
            'pro': [('SUC_m', 'bcde'), ('CO2', 'a')],
        },
    ('SUCD_m', 'FUMH_m'):
        {
            'id': 'SUCD_FUMH_m',
            'sub': [('SUC_m', 'abcd')],
            'pro': [('MAL_m', 'abcd')],
            'reverse': True
        },
    ('SUCD_m', 'FUMH_m', 'MDH_m'):
        {
            'id': 'SUCD_FUMH_MDH_m',
            'sub': [('SUC_m', 'abcd')],
            'pro': [('OAC_m', 'abcd')],
            'reverse': True
        },
}

consecutive_important_flux_replace_dict = {
    'ICDH_m': 'ACONT_ICDH_m',
    'AKGD_m': 'AKGD_SUCOAS_m',
    'SUCD_FUMH_m': 'SUCD_FUMH_MDH_m',
    'SUCD_FUMH_m__R': 'SUCD_FUMH_MDH_m__R',
    'SUCD_m': 'SUCD_FUMH_m',
    'SUCD_m__R': 'SUCD_FUMH_m__R',
}

consecutive_important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    'PDH_m',
    'CS_m',
    'AKGD_m',
    ('ACONT_m', 'ACONT_m__R'),
    'PYK_c',
    ('SUCD_m', 'SUCD_m__R'),
    ('GPT_c', 'GPT_c__R'),
    'PHGDH_PSAT_PSP_c',
    'G6PDH2R_PGL_GND_c',
    ('LDH_c', 'LDH_c__R'),
]

prune_branch_pathway_information_dict = {
    'PPP_with_biomass': 'PPP_with_biomass',
    'PPP_without_biomass': 'PPP_without_biomass',
    'SG_with_biomass': 'SG_with_biomass',
    'SG_without_biomass': 'SG_without_biomass',
    'no_compartment': 'no_compartment'
}

prune_branch_important_flux_replace_dict = {
    'PDH_m': 'PDH_c',
    'CS_m': 'CS_c',
    'ACONT_m': 'ACONT_c',
    'ACONT_m__R': 'ACONT_c__R',
    'AKGD_m': 'AKGD_c',
    'SUCOAS_m': 'SUCOAS_c',
    'ICDH_m': 'ICDH_c',
    'SUCD_m': 'SUCD_c',
    'SUCD_m__R': 'SUCD_c__R',
    'FUMH_m': 'FUMH_c',
    'FUMH_m__R': 'FUMH_c__R',
    'MDH_m': 'MDH_c',
    'MDH_m__R': 'MDH_c__R',
    'PC_m': 'PC_c',
    'GLUD_m': 'GLUD_c',
    'GLUD_m__R': 'GLUD_c__R',
    'GLND_m': 'GLND_c',
    'ASPTA_m': 'ASPTA_c',
    'ASPTA_m__R': 'ASPTA_c__R',
}

prune_branch_important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    'PDH_m',
    'CS_m',
    'AKGD_m',
    'ICDH_m',
    'PYK_c',
    ('SUCD_m', 'SUCD_m__R'),
    ('FUMH_m', 'FUMH_m__R'),
    ('MDH_m', 'MDH_m__R'),
    ('GPT_c', 'GPT_c__R'),
    'PHGDH_PSAT_PSP_c',
    'G6PDH2R_PGL_GND_c',
    ('LDH_c', 'LDH_c__R'),
]

normal_important_flux_list = [
    ('FBA_c', 'FBA_c__R'),
    'PDH_m',
    'CS_m',
    'AKGD_m',
    ('ACONT_m', 'ACONT_m__R'),
    'PYK_c',
    ('SUCD_m', 'SUCD_m__R'),
    ('FUMH_m', 'FUMH_m__R'),
    ('MDH_m', 'MDH_m__R'),
    ('GPT_c', 'GPT_c__R'),
    'PHGDH_PSAT_PSP_c',
    'G6PDH2R_PGL_GND_c',
    ('LDH_c', 'LDH_c__R'),
]

data_keep_dict = {
    DataSetting.raw_data: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'lactate',
        'phosphoenolpyruvate',
        'serine',
        'glycine',
        'asparagine',
        'citrate/isocitrate',
        'aspartate',
        'succinate',
        'alanine',
        'fumarate',
        'fructose 6-phosphate/glucose 6-phosphate',
        'malate',
        'ribose 5-phosphate',
        'glucose',
        'erythrose 4-phosphate',
        'glutamate',
        'a-ketoglutarate',
        'glutamine',
        'dihydroxyacetone phosphate',
        'fructose 1,6-bisphosphate'
    ],
    DataSetting.medium_data_plus: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'lactate',
        # 'phosphoenolpyruvate',
        'serine',
        'glycine',
        'asparagine',
        'citrate/isocitrate',
        'aspartate',
        'succinate',
        # 'alanine',
        'fumarate',  # New
        # 'fructose 6-phosphate/glucose 6-phosphate',
        'malate',  # New
        'ribose 5-phosphate',
        'glucose',
        'erythrose 4-phosphate',  # New
        'glutamate',
        'a-ketoglutarate',
        # 'glutamine',
        # 'dihydroxyacetone phosphate',
        # 'fructose 1,6-bisphosphate'
    ],
    DataSetting.medium_data: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'lactate',
        'serine',
        'glycine',
        'asparagine',
        'citrate/isocitrate',
        'aspartate',
        'succinate',
        'a-ketoglutarate',
        'glutamate',
        'alanine',
        'ribose 5-phosphate',
        'glucose',
    ],
    DataSetting.few_data: [
        'pyruvate',
        'lactate',
        'serine',
        'glycine',
        'aspartate',
        'succinate',
        'glucose',
        'glutamate',
    ],
    DataSetting.data_without_ppp: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'serine',
        'lactate',
        'phosphoenolpyruvate',
        'glycine',
        'asparagine',
        'citrate/isocitrate',
        'aspartate',
        'succinate',
        'alanine',
        'fumarate',
        'malate',
        'glucose',
        'glutamate',
        'a-ketoglutarate',
        'glutamine',
        'dihydroxyacetone phosphate',
    ],
    DataSetting.data_without_tca: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'serine',
        'lactate',
        'phosphoenolpyruvate',
        'glycine',
        'asparagine',
        'aspartate',
        'alanine',
        'fructose 6-phosphate/glucose 6-phosphate',
        'ribose 5-phosphate',
        'glucose',
        'erythrose 4-phosphate',
        'glutamate',
        'glutamine',
        'dihydroxyacetone phosphate',
        'fructose 1,6-bisphosphate'
    ],
    DataSetting.data_without_aa: [
        '2-phosphoglycerate/3-phosphoglycerate',
        'pyruvate',
        'lactate',
        'phosphoenolpyruvate',
        'citrate/isocitrate',
        'succinate',
        'fumarate',
        'fructose 6-phosphate/glucose 6-phosphate',
        'malate',
        'ribose 5-phosphate',
        'glucose',
        'erythrose 4-phosphate',
        'a-ketoglutarate',
        'dihydroxyacetone phosphate',
        'fructose 1,6-bisphosphate'
    ],
    DataSetting.medium_data_without_combination: [
        '2-phosphoglycerate~c',
        '3-phosphoglycerate~c',
        'pyruvate~c',
        'pyruvate~m',
        'serine~c',
        'lactate~c',
        'phosphoenolpyruvate~c',
        'glycine~c',
        'asparagine~c',
        'citrate~c',
        'citrate~m',
        'isocitrate~m',
        'aspartate~c',
        'aspartate~m',
        'succinate~m',
        'alanine~c',
        'fumarate~m',
        'fructose 6-phosphate~c',
        'glucose 6-phosphate~c',
        'malate~m',
        'malate~c',
        'ribose 5-phosphate~c',
        'glucose~c',
        'erythrose 4-phosphate~c',
        'glutamate~m',
        'glutamate~c',
        'a-ketoglutarate~m',
        'a-ketoglutarate~c',
        'glutamine~m',
        'glutamine~c',
        'dihydroxyacetone phosphate~c',
        'fructose 1,6-bisphosphate~c'
    ],
}

flux_range_dict = {
    'low_lower_low_upper': (0.5, 500),
    'low_lower_medium_upper': (0.5, 1000),
    'low_lower_high_upper': (0.5, 2000),
    'low_lower_ex_high_upper': (0.5, 5000),
    'medium_lower_low_upper': (1, 500),
    'medium_lower_high_upper': (1, 2000),
    'medium_lower_ex_high_upper': (1, 5000),
    'high_lower_low_upper': (2, 500),
    'high_lower_medium_upper': (2, 1000),
    'high_lower_high_upper': (2, 2000),
    'high_lower_ex_high_upper': (2, 5000),
    'ex_high_lower_low_upper': (5, 500),
    'ex_high_lower_medium_upper': (5, 1000),
    'ex_high_lower_high_upper': (5, 2000),
    'ex_high_lower_ex_high_upper': (5, 5000),
}


constant_flux_value_nested_dict = {
    'gln_only': {'GLN_input'},
    'asp_only': {'ASP_input'},
    'with_gln': {'GLC_input', 'GLN_input'},
    'with_asp': {'GLC_input', 'ASP_input'},
    'with_aa': {'GLC_input', 'SER_input', 'GLY_input', 'ALA_input'},
    'with_lac': {'GLC_input', 'LAC_output'},
    'with_gln_asp': {'GLC_input', 'GLN_input', 'ASP_input'},
    'with_gln_aa': {'GLC_input', 'GLN_input', 'SER_input', 'GLY_input', 'ALA_input'},
    'with_gln_lac': {'GLC_input', 'GLN_input', 'LAC_output'},
    'with_asp_lac': {'GLC_input', 'ASP_input', 'LAC_output'},
    'with_gln_asp_lac': {'GLC_input', 'GLN_input', 'ASP_input', 'LAC_output'},
    'with_all_exchange': {'GLC_input', 'GLN_input', 'ASP_input', 'LAC_output', 'SER_input', 'GLY_input', 'ALA_input'},
}

noise_rate = 0.2

constant_flux_value_nested_dict_with_noise = {
    'glc_only_low': {'GLC_input': 1 - noise_rate},
    'glc_only_high': {'GLC_input': 1 + noise_rate},
    'gln_only_low': {'GLN_input': 1 - noise_rate},
    'gln_only_high': {'GLN_input': 1 + noise_rate},
    'asp_only_low': {'ASP_input': 1 - noise_rate},
    'asp_only_high': {'ASP_input': 1 + noise_rate},
    'with_gln_low_high': {'GLC_input': 1 - noise_rate, 'GLN_input': 1 + noise_rate},
    'with_gln_high_low': {'GLC_input': 1 + noise_rate, 'GLN_input': 1 - noise_rate},
    'with_asp_low_high': {'GLC_input': 1 - noise_rate, 'ASP_input': 1 + noise_rate},
    'with_asp_high_low': {'GLC_input': 1 + noise_rate, 'ASP_input': 1 - noise_rate},
    'with_lac_low_high': {'GLC_input': 1 - noise_rate, 'LAC_output': 1 + noise_rate},
    'with_lac_high_low': {'GLC_input': 1 + noise_rate, 'LAC_output': 1 - noise_rate},
}

complete_analyzed_set_size_list = (
    100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000
)
complete_selected_min_loss_size_list = (1, 2, 5, 10, 20, 50, 100, 200, 500)


def return_analyzed_set_and_selected_min_loss_set(test_raw_model_analysis=False, current_experiment_name=None):
    if test_raw_model_analysis:
        if current_experiment_name in {ExperimentName.raw_model_all_data}:
            analyzed_set_size_list = (5000,)
            selected_min_loss_size_list = (100,)
        else:
            analyzed_set_size_list = (20000,)
            selected_min_loss_size_list = (100,)
    else:
        analyzed_set_size_list = complete_analyzed_set_size_list
        selected_min_loss_size_list = complete_selected_min_loss_size_list
    return analyzed_set_size_list, selected_min_loss_size_list


def complete_optimization_selection_parameters_dict_generator(analyzed_set_size_list, selected_min_loss_size_list):
    parameters_dict = {}
    for analyzed_set_size in analyzed_set_size_list:
        for selected_min_loss_size in selected_min_loss_size_list:
            if selected_min_loss_size > analyzed_set_size:
                continue
            analyzed_set_size_str = str(analyzed_set_size)
            if analyzed_set_size > 1000:
                analyzed_set_size_str = f'{int(analyzed_set_size / 1000 + .5)}k'
            current_name = f'{analyzed_set_size_str}_{selected_min_loss_size}'
            parameters_dict[current_name] = {
                Keywords.optimized_size: analyzed_set_size, Keywords.selection_size: selected_min_loss_size}
    return parameters_dict


class AverageSolution(BasicFigureData):
    data_prefix = FigureDataKeywords.raw_model_distance

    def __init__(self):
        super().__init__()
        self.complete_data_name_dict = {
            DataSetting.all_data: ExperimentName.raw_model_all_data,
            DataSetting.raw_data: ExperimentName.raw_model_raw_data,
            DataSetting.all_data_squared_loss: ExperimentName.raw_model_all_data_with_squared_loss,
            DataSetting.raw_data_squared_loss: ExperimentName.raw_model_raw_data_with_squared_loss,
            DataSetting.all_data_batch: ExperimentName.optimization_from_batched_simulated_all_data,
            DataSetting.raw_data_batch: ExperimentName.optimization_from_batched_simulated_raw_data,
            DataSetting.all_data_batch_squared_loss: ExperimentName.optimization_from_batched_simulated_all_data_with_squared_loss,
            DataSetting.raw_data_batch_squared_loss: ExperimentName.optimization_from_batched_simulated_raw_data_with_squared_loss,
        }

    def return_averaged_flux_solutions(
            self, storage_data_name, optimized_size, selection_size, batched_result_data_label=None):
        complete_data_name = self.complete_data_name_dict[storage_data_name]
        averaged_data_obj = self._return_figure_data(complete_data_name)
        if batched_result_data_label is not None:
            separate_selected_averaged_flux_value_dict = averaged_data_obj.separate_selected_averaged_flux_value_dict
            target_averaged_flux_value = separate_selected_averaged_flux_value_dict[optimized_size][selection_size][
                batched_result_data_label]
        else:
            selected_averaged_flux_value_dict = averaged_data_obj.selected_averaged_flux_value_dict
            target_averaged_flux_value = selected_averaged_flux_value_dict[optimized_size][selection_size]
        return target_averaged_flux_value

    def return_averaged_data(self, data_name):
        complete_data_name = self.complete_data_name_dict[data_name]
        averaged_data_obj = self._return_figure_data(complete_data_name)
        raw_selected_flux_value_dict = averaged_data_obj.raw_selected_flux_value_dict
        selected_averaged_flux_value_dict = averaged_data_obj.selected_averaged_flux_value_dict
        initial_raw_selected_diff_vector_dict = averaged_data_obj.raw_selected_diff_vector_dict
        initial_averaged_diff_vector_dict = averaged_data_obj.selected_averaged_diff_vector_dict
        raw_selected_loss_dict = averaged_data_obj.raw_loss_value_dict
        loss_of_mean_solution_dict = averaged_data_obj.loss_of_mean_solution_dict
        raw_all_select_euclidian_distance_dict = averaged_data_obj.final_raw_all_select_euclidian_distance_dict
        net_all_select_euclidian_distance_dict = averaged_data_obj.final_net_all_select_euclidian_distance_dict
        try:
            raw_mean_euclidian_distance_dict = averaged_data_obj.final_raw_euclidian_distance_dict
        except AttributeError:
            raw_mean_euclidian_distance_dict = None
        net_mean_euclidian_distance_dict = averaged_data_obj.final_net_euclidian_distance_dict
        net_all_selected_relative_error_dict = averaged_data_obj.net_all_selected_relative_error_dict
        net_selected_averaged_relative_error_dict = averaged_data_obj.net_selected_averaged_relative_error_dict
        final_flux_relative_distance_dict = averaged_data_obj.final_flux_relative_distance_dict
        try:
            net_distance_between_different_simulated_flux_dict = averaged_data_obj.net_distance_between_different_simulated_flux_dict
        except AttributeError:
            net_distance_between_different_simulated_flux_dict = None
        return (
            raw_selected_flux_value_dict, selected_averaged_flux_value_dict,
            initial_raw_selected_diff_vector_dict, initial_averaged_diff_vector_dict,
            raw_selected_loss_dict, loss_of_mean_solution_dict,
            raw_all_select_euclidian_distance_dict, net_all_select_euclidian_distance_dict,
            raw_mean_euclidian_distance_dict, net_mean_euclidian_distance_dict,
            net_all_selected_relative_error_dict,
            net_selected_averaged_relative_error_dict,
            final_flux_relative_distance_dict, net_distance_between_different_simulated_flux_dict)


averaged_solution_data_obj = AverageSolution()


