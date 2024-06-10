from scripts.src.core.model.model_class import UserDefinedModel

from .model_metabolite_to_standard_name_dict import model_metabolite_to_standard_name_dict


class ModelList(object):
    base_model = 'base_model'
    base_model_with_glns_m = 'base_model_with_glns_m'
    base_model_with_glc_tca_buffer = 'base_model_with_glc_tca_buffer'
    base_model_with_glc_tca_buffer_glns_m = 'base_model_with_glc_tca_buffer_glns_m'
    invivo_infusion_model = 'invivo_infusion_model'
    invivo_infusion_model_with_oac_buffer = 'invivo_infusion_model_with_oac_buffer'


model_path_name_dict = {
    ModelList.base_model: 'base_model',
    ModelList.invivo_infusion_model: ModelList.invivo_infusion_model
}


def model_loader(model_type, model_parameter=None):
    if model_type == ModelList.base_model:
        from .base_model import base_model
        current_model = base_model
    elif model_type == ModelList.base_model_with_glc_tca_buffer:
        from .base_model import base_model_with_glc_tca_buffer
        current_model = base_model_with_glc_tca_buffer
    elif model_type == ModelList.base_model_with_glc_tca_buffer_glns_m:
        from .base_model import base_model_with_glc_tca_buffer_glns_m as current_model
    elif model_type == ModelList.base_model_with_glns_m:
        from .base_model import base_model_with_glns_m as current_model
    elif model_type == ModelList.invivo_infusion_model:
        from .invivo_infusion_model import invivo_infusion_model
        current_model = invivo_infusion_model
    elif model_type == ModelList.invivo_infusion_model_with_oac_buffer:
        from .invivo_infusion_model import invivo_infusion_model_with_tca_buffer
        current_model = invivo_infusion_model_with_tca_buffer
    else:
        raise ValueError()
    reaction_list = []
    for pathway_name, pathway_reaction_list in current_model.reaction_dict.items():
        reaction_list.extend(pathway_reaction_list)
    user_defined_model = UserDefinedModel(
        reaction_list=reaction_list,
        symmetrical_metabolite_set=current_model.symmetrical_metabolite_set,
        added_input_metabolite_set=current_model.added_input_metabolite_set,
        emu_excluded_metabolite_set=current_model.emu_excluded_metabolite_set,
        balance_excluded_metabolite_set=current_model.balance_excluded_metabolite_set,
        target_metabolite_list=None,
        model_compartment_set=current_model.model_compartment_set,
        composite_reaction_list=current_model.composite_reaction_list,
        model_metabolite_to_standard_name_dict=model_metabolite_to_standard_name_dict,
    )
    return user_defined_model

