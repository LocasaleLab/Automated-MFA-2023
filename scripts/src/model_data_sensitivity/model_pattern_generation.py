import scripts.src.model_data_sensitivity.sensitivity_config
from scripts.src.core.model.model_class import UserDefinedModel
from scripts.src.core.common.functions import reverse_reaction_name
from scripts.src.common.built_in_packages import copy
from scripts.model.base_model.pathway_adjust_function import pathway_adjust_function
from scripts.model.model_loader import model_loader

from .config import raw_model, raw_model_with_glns_m
from .sensitivity_config import raw_config_first, ModelSetting, Keywords, consecutive_important_flux_replace_dict, \
    consecutive_important_flux_list, prune_branch_important_flux_replace_dict, prune_branch_important_flux_list, \
    normal_important_flux_list


def merge_reversible_reaction(
        raw_user_defined_model: UserDefinedModel, simulated_flux_value_dict, merged_reaction_dict):
    reaction_dict = raw_user_defined_model.reaction_dict
    final_modified_defined_model_dict = {}
    information_dict = {}
    for experiment_name, merged_reaction_name in merged_reaction_dict.items():
        new_reaction_dict = copy.deepcopy(reaction_dict)
        merged_reaction = new_reaction_dict[merged_reaction_name]
        reversed_merged_reaction_name = reverse_reaction_name(merged_reaction_name)
        forward_flux_value = simulated_flux_value_dict[merged_reaction_name]
        reverse_flux_value = simulated_flux_value_dict[reversed_merged_reaction_name]
        if forward_flux_value < reverse_flux_value:
            new_merged_reaction_name = reversed_merged_reaction_name
            new_merged_reaction = {
                'id': new_merged_reaction_name,
                'sub': merged_reaction['pro'],
                'pro': merged_reaction['sub']}
        else:
            new_merged_reaction_name = merged_reaction_name
            new_merged_reaction = merged_reaction
            del new_merged_reaction['reverse']
        del new_reaction_dict[merged_reaction_name]
        new_reaction_dict[new_merged_reaction_name] = new_merged_reaction

        modified_user_defined_model = UserDefinedModel(
            reaction_dict=new_reaction_dict,
            symmetrical_metabolite_set=raw_user_defined_model.symmetrical_metabolite_set,
            added_input_metabolite_set=raw_user_defined_model.added_input_metabolite_set,
            emu_excluded_metabolite_set=raw_user_defined_model.emu_excluded_metabolite_set,
            balance_excluded_metabolite_set=raw_user_defined_model.balance_excluded_metabolite_set,
            target_metabolite_list=None,
            model_compartment_set=raw_user_defined_model.model_compartment_set,
            model_metabolite_to_standard_name_dict=raw_user_defined_model.model_metabolite_to_standard_name_dict,
        )
        final_modified_defined_model_dict[experiment_name] = modified_user_defined_model
        information_dict[experiment_name] = merged_reaction_name
    return final_modified_defined_model_dict, information_dict


def combine_consecutive_reactions(
        raw_user_defined_model: UserDefinedModel, consecutive_reaction_dict):
    reaction_dict = raw_user_defined_model.reaction_dict
    final_modified_defined_model_dict = {}
    information_dict = {}
    for raw_consecutive_reaction_tuple, combined_reaction_dict in consecutive_reaction_dict.items():
        experiment_name = combined_reaction_dict['id']
        new_reaction_dict = copy.deepcopy(reaction_dict)
        for raw_consecutive_reaction_id in raw_consecutive_reaction_tuple:
            del new_reaction_dict[raw_consecutive_reaction_id]
        new_reaction_dict[experiment_name] = combined_reaction_dict

        modified_user_defined_model = UserDefinedModel(
            reaction_dict=new_reaction_dict,
            symmetrical_metabolite_set=raw_user_defined_model.symmetrical_metabolite_set,
            added_input_metabolite_set=raw_user_defined_model.added_input_metabolite_set,
            emu_excluded_metabolite_set=raw_user_defined_model.emu_excluded_metabolite_set,
            balance_excluded_metabolite_set=raw_user_defined_model.balance_excluded_metabolite_set,
            target_metabolite_list=None,
            model_compartment_set=raw_user_defined_model.model_compartment_set,
            model_metabolite_to_standard_name_dict=raw_user_defined_model.model_metabolite_to_standard_name_dict,
        )
        final_modified_defined_model_dict[experiment_name] = modified_user_defined_model
        information_dict[experiment_name] = experiment_name
    return final_modified_defined_model_dict, information_dict


def prune_branches(
        raw_user_defined_model: UserDefinedModel, branch_pathway_information_dict):
    final_modified_defined_model_dict = {}
    information_dict = {}
    for pathway_name, pathway_information in branch_pathway_information_dict.items():
        modified_defined_model = pathway_adjust_function(
            pathway_name, raw_user_defined_model.model_metabolite_to_standard_name_dict)
        final_modified_defined_model_dict[pathway_name] = modified_defined_model
        information_dict[pathway_name] = pathway_information
    return final_modified_defined_model_dict, information_dict


def model_processor(process_type, simulated_flux_value_dict):
    if process_type == ModelSetting.raw_model_with_glns_m:
        raw_user_defined_model = model_loader(raw_model_with_glns_m)
        raw_information_dict = {ModelSetting.raw_model: Keywords.raw_type_with_glns_m}
    else:
        raw_user_defined_model = model_loader(raw_model)
        raw_information_dict = {ModelSetting.raw_model: Keywords.raw_type}
    raw_modified_defined_model_dict = {ModelSetting.raw_model: raw_user_defined_model}
    if process_type == ModelSetting.merge_reversible_reaction:
        modified_defined_model_dict, information_dict = merge_reversible_reaction(
            raw_user_defined_model, simulated_flux_value_dict,
            scripts.src.model_data_sensitivity.sensitivity_config.merged_reaction_dict)
        important_flux_replace_dict = consecutive_important_flux_replace_dict
        important_flux_list = normal_important_flux_list
    elif process_type == ModelSetting.combine_consecutive_reactions:
        modified_defined_model_dict, information_dict = combine_consecutive_reactions(
            raw_user_defined_model, scripts.src.model_data_sensitivity.sensitivity_config.consecutive_reaction_dict)
        important_flux_replace_dict = consecutive_important_flux_replace_dict
        important_flux_list = consecutive_important_flux_list
    elif process_type == ModelSetting.prune_branches:
        modified_defined_model_dict, information_dict = prune_branches(
            raw_user_defined_model,
            scripts.src.model_data_sensitivity.sensitivity_config.prune_branch_pathway_information_dict)
        important_flux_replace_dict = prune_branch_important_flux_replace_dict
        important_flux_list = prune_branch_important_flux_list
    elif process_type in {ModelSetting.raw_model, ModelSetting.raw_model_with_glns_m}:
        modified_defined_model_dict = {}
        information_dict = {}
        important_flux_replace_dict = consecutive_important_flux_replace_dict
        important_flux_list = normal_important_flux_list
    else:
        raise ValueError()
    if raw_config_first:
        raw_modified_defined_model_dict.update(modified_defined_model_dict)
        raw_information_dict.update(information_dict)
        modified_defined_model_dict = raw_modified_defined_model_dict
        information_dict = raw_information_dict
    else:
        modified_defined_model_dict.update(raw_modified_defined_model_dict)
        information_dict.update(raw_information_dict)
    return modified_defined_model_dict, information_dict, important_flux_list, important_flux_replace_dict
