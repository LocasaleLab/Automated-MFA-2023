from .content_list import ReactionList


def reaction_raw_value_processing(reaction_raw_value_dict):
    analyzed_reaction_name_set = set()
    final_reaction_value_dict = {}
    reverse_reaction_suffix = '__R'
    for reaction_raw_name, reaction_raw_value in reaction_raw_value_dict.items():
        if reaction_raw_name in analyzed_reaction_name_set or reaction_raw_name.startswith('MIX'):
            continue
        if reaction_raw_name.endswith(reverse_reaction_suffix):
            forward_reaction_name = reaction_raw_name[:-len(reverse_reaction_suffix)]
            forward_reaction_value = reaction_raw_value_dict[forward_reaction_name]
            reaction_value_obj = (forward_reaction_value, reaction_raw_value)
            analyzed_reaction_name_set.add(reaction_raw_name)
        else:
            forward_reaction_name = reaction_raw_name
            reverse_reaction_name = f'{reaction_raw_name}{reverse_reaction_suffix}'
            if reverse_reaction_name in reaction_raw_value_dict:
                reverse_reaction_value = reaction_raw_value_dict[reverse_reaction_name]
                reaction_value_obj = (reaction_raw_value, reverse_reaction_value)
                analyzed_reaction_name_set.add(reverse_reaction_name)
            else:
                reaction_value_obj = reaction_raw_value
        final_reaction_value_dict[forward_reaction_name] = reaction_value_obj
        analyzed_reaction_name_set.add(forward_reaction_name)
    return final_reaction_value_dict


def assign_value_to_network(
        reaction_raw_value_dict, reaction_list: ReactionList, infusion=False):
    reaction_name_mapping_dict = ReactionList.reaction_name_mapping_dict
    processed_reaction_value_dict = reaction_raw_value_processing(reaction_raw_value_dict)
    for reaction_name, reaction_obj in reaction_list.content_list_pair:
        if reaction_name in processed_reaction_value_dict:
            reaction_obj.set_value(processed_reaction_value_dict[reaction_name])
        elif reaction_name in reaction_name_mapping_dict:
            _, required_reaction_name_list, reaction_process_func = reaction_name_mapping_dict[reaction_name]
            required_reaction_obj_list = []
            success = True
            for required_reaction_name in required_reaction_name_list:
                if required_reaction_name in processed_reaction_value_dict:
                    required_reaction_obj_list.append(processed_reaction_value_dict[required_reaction_name])
                else:
                    success = False
                    break
            if success:
                reaction_obj.set_value(reaction_process_func(*required_reaction_obj_list))


def assign_flux_name_to_network(reaction_list: ReactionList):
    reaction_name_mapping_dict = ReactionList.reaction_name_mapping_dict
    for reaction_name, reaction_obj in reaction_list.content_list_pair:
        if reaction_name in reaction_name_mapping_dict:
            display_flux_name, *_ = reaction_name_mapping_dict[reaction_name]
            reaction_obj.set_display_text(display_flux_name)
        else:
            reaction_obj.set_display_text(reaction_name)
