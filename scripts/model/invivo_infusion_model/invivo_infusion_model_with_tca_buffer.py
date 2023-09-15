from .invivo_infusion_model import reaction_dict, \
    emu_excluded_metabolite_set as basic_emu_excluded_metabolite_set, symmetrical_metabolite_set, \
    added_input_metabolite_set, model_compartment_set, composite_reaction_list, \
    ModelKeyword

reaction_dict['tca_reaction'].append(
    {
        'id': 'CIT_supplement',
        'sub': [('CIT_stock', 'abcdef')],
        'pro': [('CIT_m', 'abcdef')],
        'reverse': True
    }
)

emu_excluded_metabolite_set = basic_emu_excluded_metabolite_set | {'CIT_stock'}

balance_excluded_metabolite_set = emu_excluded_metabolite_set

composite_reaction_list.append(
    {
        'id': 'CIT_supplement_net',
        'comp': [('CIT_supplement', ), ('CIT_supplement__R', -1)],
        ModelKeyword.flux_range: ModelKeyword.add_range_type
    }
)

