from ..common.config import ModelKeyword
from ..common.functions import tissue_specific_name_constructor
from ..common.classes import TransformDict

from .model_class import EMUMIDDimDict, MFAModel, UserDefinedModel
from .common_model_process_functions import model_preprocess, compart_all_metabolites, \
    flux_balance_equation_generator, metabolite_carbon_number_verification
from .emu_analyzer_functions import emu_equation_analyzer, emu_matrix_equation_generator


def common_model_constructor(user_defined_model: UserDefinedModel):
    (
        metabolite_reaction_dict, product_reaction_dict_for_emu, composite_reaction_dict,
        flux_name_index_dict, input_metabolite_name_set, complete_metabolite_dim_dict,
        target_emu_list) = model_preprocess(
        user_defined_model.reaction_list, user_defined_model.symmetrical_metabolite_set,
        user_defined_model.added_input_metabolite_set, user_defined_model.emu_excluded_metabolite_set,
        user_defined_model.balance_excluded_metabolite_set, user_defined_model.target_metabolite_list,
        user_defined_model.composite_reaction_list)
    # print(input_metabolite_name_set - complete_metabolite_dim_dict.keys())

    all_target_metabolite_name_set = list(complete_metabolite_dim_dict.keys() - input_metabolite_name_set)
    # all_target_metabolite_name_set = {
    #     key: value for key, value in complete_metabolite_dim_dict.items() if key not in input_metabolite_name_set}
    complete_tissue_metabolite_compartment_dict, metabolite_bare_metabolite_name_dict = compart_all_metabolites(
        complete_metabolite_dim_dict.keys(), user_defined_model.model_compartment_set)
    bare_metabolite_dim_dict = metabolite_carbon_number_verification(
        complete_metabolite_dim_dict, metabolite_bare_metabolite_name_dict)
    flux_balance_matrix, flux_balance_right_side_vector = flux_balance_equation_generator(
        metabolite_reaction_dict, composite_reaction_dict, flux_name_index_dict)
    emu_mid_equation_dict, input_emu_dict = emu_equation_analyzer(
        product_reaction_dict_for_emu, target_emu_list, input_metabolite_name_set)
    output_emu_mid_equation_dict = emu_matrix_equation_generator(emu_mid_equation_dict, input_emu_dict)
    complete_emu_dim_dict = EMUMIDDimDict()
    mfa_model = MFAModel(
        input_emu_dict, target_emu_list, output_emu_mid_equation_dict, composite_reaction_dict,
        complete_emu_dim_dict, flux_name_index_dict, flux_balance_matrix, flux_balance_right_side_vector,
        bare_metabolite_dim_dict, metabolite_bare_metabolite_name_dict, complete_tissue_metabolite_compartment_dict,
        all_target_metabolite_name_set, user_defined_model.model_metabolite_to_standard_name_dict,
        user_defined_model)
    return mfa_model


def multiple_tissue_model_converter(tissue_specific_user_defined_model_dict):
    def modified_tissue_name_generator(raw_reactant_name, current_tissue_name, other_compartment_metabolite_dict):
        if raw_reactant_name in other_compartment_metabolite_dict:
            target_tissue_name = other_compartment_metabolite_dict[raw_reactant_name]
            if target_tissue_name == ModelKeyword.general:
                modified_tissue_name = None
            else:
                modified_tissue_name = target_tissue_name
        else:
            modified_tissue_name = current_tissue_name
        return modified_tissue_name

    def rename_reaction_list(raw_reaction_list, current_tissue_name, other_compartment_metabolite_dict):
        new_reaction_list = []
        for raw_reaction in raw_reaction_list:
            raw_reactant_name = raw_reaction[0]
            modified_tissue_name = modified_tissue_name_generator(
                raw_reactant_name, current_tissue_name, other_compartment_metabolite_dict)
            if modified_tissue_name is None:
                new_reaction_list.append(raw_reaction)
                continue
            new_reaction = list(raw_reaction)
            new_reaction[0] = tissue_specific_name_constructor(raw_reactant_name, modified_tissue_name)
            new_reaction_list.append(tuple(new_reaction))
        return new_reaction_list

    def rename_and_add_to_complete_set(
            raw_single_set, complete_set, current_tissue_name, other_compartment_metabolite_dict):
        for raw_name in raw_single_set:
            modified_tissue_name = modified_tissue_name_generator(
                raw_name, current_tissue_name, other_compartment_metabolite_dict)
            new_name = tissue_specific_name_constructor(raw_name, modified_tissue_name)
            complete_set.add(new_name)

    complete_reaction_list = []
    complete_emu_excluded_metabolite_set = set()
    complete_balance_excluded_metabolite_set = set()
    complete_symmetrical_metabolite_set = set()
    complete_added_input_metabolite_set = set()
    complete_model_compartment_set = set()
    complete_model_metabolite_to_standard_name_dict = TransformDict()
    complete_model_tissue_set = set(tissue_specific_user_defined_model_dict.keys())
    for tissue_name, each_tissue_user_defined_model in tissue_specific_user_defined_model_dict.items():
        current_other_compartment_metabolite_dict = {}
        for other_tissue_name, other_metabolite_set in \
                each_tissue_user_defined_model.other_pool_metabolite_dict.items():
            for other_metabolite_name in other_metabolite_set:
                current_other_compartment_metabolite_dict[other_metabolite_name] = other_tissue_name
        for raw_reaction_dict in each_tissue_user_defined_model.reaction_list:
            new_reaction_dict = dict(raw_reaction_dict)
            raw_id = new_reaction_dict[ModelKeyword.id]
            raw_sub_reaction_list = new_reaction_dict[ModelKeyword.sub]
            raw_pro_reaction_list = new_reaction_dict[ModelKeyword.pro]
            new_id = tissue_specific_name_constructor(raw_id, tissue_name)
            new_sub_reaction_list = rename_reaction_list(
                raw_sub_reaction_list, tissue_name, current_other_compartment_metabolite_dict)
            new_pro_reaction_list = rename_reaction_list(
                raw_pro_reaction_list, tissue_name, current_other_compartment_metabolite_dict)
            new_reaction_dict.update({
                ModelKeyword.id: new_id,
                ModelKeyword.sub: new_sub_reaction_list,
                ModelKeyword.pro: new_pro_reaction_list})
            complete_reaction_list.append(new_reaction_dict)

        raw_emu_excluded_metabolite_set = each_tissue_user_defined_model.emu_excluded_metabolite_set
        rename_and_add_to_complete_set(
            raw_emu_excluded_metabolite_set, complete_emu_excluded_metabolite_set, tissue_name,
            current_other_compartment_metabolite_dict)
        raw_balance_excluded_metabolite_set = each_tissue_user_defined_model.balance_excluded_metabolite_set
        rename_and_add_to_complete_set(
            raw_balance_excluded_metabolite_set, complete_balance_excluded_metabolite_set, tissue_name,
            current_other_compartment_metabolite_dict)
        raw_symmetrical_metabolite_set = each_tissue_user_defined_model.symmetrical_metabolite_set
        rename_and_add_to_complete_set(
            raw_symmetrical_metabolite_set, complete_symmetrical_metabolite_set, tissue_name,
            current_other_compartment_metabolite_dict)
        raw_added_input_metabolite_set = each_tissue_user_defined_model.added_input_metabolite_set
        rename_and_add_to_complete_set(
            raw_added_input_metabolite_set, complete_added_input_metabolite_set, tissue_name,
            current_other_compartment_metabolite_dict)
        raw_model_compartment_set = each_tissue_user_defined_model.model_compartment_set
        complete_model_compartment_set |= raw_model_compartment_set
        model_metabolite_to_standard_name_dict = each_tissue_user_defined_model.model_metabolite_to_standard_name_dict
        complete_model_metabolite_to_standard_name_dict.update(model_metabolite_to_standard_name_dict)

    complete_user_defined_model = UserDefinedModel(
        reaction_list=complete_reaction_list,
        symmetrical_metabolite_set=complete_symmetrical_metabolite_set,
        added_input_metabolite_set=complete_added_input_metabolite_set,
        emu_excluded_metabolite_set=complete_emu_excluded_metabolite_set,
        balance_excluded_metabolite_set=complete_balance_excluded_metabolite_set,
        target_metabolite_list=None,
        model_compartment_set=complete_model_compartment_set,
        model_tissue_set=complete_model_tissue_set,
        model_metabolite_to_standard_name_dict=complete_model_metabolite_to_standard_name_dict,
    )
    return complete_user_defined_model
