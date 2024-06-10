from .base_model import reaction_dict as basic_reaction_dict, \
    emu_excluded_metabolite_set, balance_excluded_metabolite_set, symmetrical_metabolite_set, \
    added_input_metabolite_set, model_compartment_set, \
    composite_reaction_list, ModelKeyword

reaction_dict = dict(basic_reaction_dict)
reaction_dict['glu_reaction'] = list(basic_reaction_dict['glu_reaction'])

reaction_dict['glu_reaction'].append(
    {
        'id': 'GLNS_m',
        'sub': [('GLU_m', 'abcde')],
        'pro': [('GLN_m', 'abcde')],
    }
)


