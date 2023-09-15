from scripts.src.core.model.model_class import UserDefinedModel

from . import base_model, model_without_compartment

biomass_reaction_key = 'biomass_reaction'

base_biomass_reaction_list = [
    ('ALA_c', '', 0.5360230145753),
    ('ASN_c', '', 0.0544398374178039),
    ('ASP_c', '', 3.12819681162304),
    ('GLN_c', '', 0.862662039082123),
    ('GLU_c', '', 0.757970044047885),
    ('ACCOA_lipid', '', 1.0)
]

biomass_reaction_list_remove_ppp_with_biomass = base_biomass_reaction_list + [
    ('SER_c', '', 0.167507192054781),
    ('GLY_c', '', 0.62815197020543),
    ('GLC6P_c', '', 0.12),
]

biomass_reaction_list_remove_ppp_without_biomass = base_biomass_reaction_list + [
    ('SER_c', '', 0.167507192054781),
    ('GLY_c', '', 0.62815197020543),
]

biomass_reaction_list_remove_sg_with_biomass = base_biomass_reaction_list + [
    ('3PG_c', '', 0.167507192054781 + 0.62815197020543),
    ('RIB5P_c', '', 0.12),
]

biomass_reaction_list_remove_sg_without_biomass = base_biomass_reaction_list + [
    ('RIB5P_c', '', 0.12),
]


def pathway_adjust_function(pathway_name, model_metabolite_to_standard_name_dict):
    new_group_reaction_dict = dict(base_model.reaction_dict)
    if pathway_name.startswith('PPP') or pathway_name.startswith('SG'):
        if pathway_name.startswith('PPP'):
            del new_group_reaction_dict['ppp_reaction']
            if pathway_name == 'PPP_with_biomass':
                biomass_reaction_list = biomass_reaction_list_remove_ppp_with_biomass
            elif pathway_name == 'PPP_without_biomass':
                biomass_reaction_list = biomass_reaction_list_remove_ppp_without_biomass
            else:
                raise ValueError()
        elif pathway_name.startswith('SG'):
            del new_group_reaction_dict['ser_gly_reaction']
            if pathway_name == 'SG_with_biomass':
                biomass_reaction_list = biomass_reaction_list_remove_sg_with_biomass
            elif pathway_name == 'SG_without_biomass':
                biomass_reaction_list = biomass_reaction_list_remove_sg_without_biomass
            else:
                raise ValueError()
        else:
            raise ValueError()
        biomass_reaction_obj = [
            {
                'id': 'BIOMASS_REACTION',
                'sub': biomass_reaction_list,
                'pro': [('BIOMASS', '')],
            },
        ]
        new_group_reaction_dict['biomass_reaction'] = biomass_reaction_obj
        flat_reaction_list = []
        for _, pathway_reaction_list in new_group_reaction_dict.items():
            flat_reaction_list.extend(pathway_reaction_list)
        modified_user_defined_model = UserDefinedModel(
            reaction_list=flat_reaction_list,
            symmetrical_metabolite_set=base_model.symmetrical_metabolite_set,
            added_input_metabolite_set=base_model.added_input_metabolite_set,
            emu_excluded_metabolite_set=base_model.emu_excluded_metabolite_set,
            balance_excluded_metabolite_set=base_model.balance_excluded_metabolite_set,
            target_metabolite_list=None,
            model_compartment_set=base_model.model_compartment_set,
            model_metabolite_to_standard_name_dict=model_metabolite_to_standard_name_dict)
    elif pathway_name == 'no_compartment':
        flat_reaction_list = []
        for _, pathway_reaction_list in model_without_compartment.reaction_dict.items():
            flat_reaction_list.extend(pathway_reaction_list)
        modified_user_defined_model = UserDefinedModel(
            reaction_list=flat_reaction_list,
            symmetrical_metabolite_set=model_without_compartment.symmetrical_metabolite_set,
            added_input_metabolite_set=model_without_compartment.added_input_metabolite_set,
            emu_excluded_metabolite_set=model_without_compartment.emu_excluded_metabolite_set,
            balance_excluded_metabolite_set=model_without_compartment.balance_excluded_metabolite_set,
            target_metabolite_list=None,
            model_compartment_set=model_without_compartment.model_compartment_set,
            model_metabolite_to_standard_name_dict=model_metabolite_to_standard_name_dict)
    else:
        raise ValueError()
    return modified_user_defined_model
