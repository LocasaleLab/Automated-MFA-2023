from ..common.packages import Counter, PriorityQueue
from ..common.classes import DefaultDict
from ..common.config import CoreConstants

from .model_class import EMUElement
from ..common.classes import DictList


def decode_emu_name(emu_name):
    metabolite_name, carbon_list_str, *param_list = emu_name.split(CoreConstants.emu_carbon_list_str_sep)
    carbon_list = [int(char) for char in list(carbon_list_str)]
    return EMUElement(metabolite_name, carbon_list)


# Return a list of emu / emu combination and their coefficient to form the current_emu
# [ { "composition": [emu_source1, emu_source2, ...], "coefficient": 0.5 } , ...]
def find_overlapped_emu(current_emu, reaction_obj):
    """
    This function will find all combinations of overlapped EMU for current_emu in a reaction reaction_obj. For
    those symmetrical metabolites, they have been extended to two 0.5 symmetrical items in the reaction_obj.
    It is assumed that coefficients of all substrates in reaction_obj equal to 1.

    :param current_emu:
    :param reaction_obj:
    :return:
    """
    def dfs_find_all_combination(
            rest_carbon_atom_key_set, substrate_node_search_list, current_combination, result_combination_list):
        """
        This function uses iterative DFS to search all EMU combinations that can generate a certain EMU
        of produce metabolite in a reaction_obj. Coefficients of all possible substrate must be 1, while
        the coefficients of product may not be 1.

        :param rest_carbon_atom_key_set: Rest of carbon atom that has not been mapped, such as {'a', 'b', 'c'}
        :param substrate_node_search_list: List of reaction node that need to be search, such as [Node('AKG', 'abcde')]
        :param current_combination: Current EMU combination that can generate mapped carbon atoms.
        :param result_combination_list: Final list of all combinations.
        :return: None. The output is result_combination_list.
        """
        if not rest_carbon_atom_key_set:
            result_combination_list.append(current_combination)
            return
        elif not substrate_node_search_list:
            return
        else:
            for substrate_index, substrate_node in enumerate(substrate_node_search_list):
                substrate_name = substrate_node.name
                carbon_composition_list = substrate_node.carbon_composition_list
                selected_carbon_list = [0] * len(carbon_composition_list)
                new_rest_carbon_set = set(rest_carbon_atom_key_set)
                for carbon_atom_key in rest_carbon_atom_key_set:
                    try:
                        loc = carbon_composition_list.index(carbon_atom_key)
                    except ValueError:
                        continue
                    else:
                        selected_carbon_list[loc] = 1
                        new_rest_carbon_set -= {carbon_atom_key}
                if sum(selected_carbon_list) > 0:
                    new_emu_dict = {
                        'metabolite_name': substrate_name,
                        'selected_carbon_list': selected_carbon_list,
                    }
                    new_search_space_list = substrate_node_search_list[substrate_index + 1:]
                    new_combination = current_combination + [new_emu_dict]
                    dfs_find_all_combination(
                        new_rest_carbon_set, new_search_space_list, new_combination, result_combination_list)

    final_overlapped_emu_list = []
    for product_node in reaction_obj.product_list:
        if product_node.name == current_emu.metabolite_name:
            query_carbon_atom_key_set = {
                carbon_atom_key for index, carbon_atom_key in enumerate(product_node.carbon_composition_list)
                if current_emu.selected_carbon_list[index]}
            different_combination_list = []
            dfs_find_all_combination(
                query_carbon_atom_key_set, reaction_obj.substrate_list, [], different_combination_list)
            for combination in different_combination_list:
                final_overlapped_emu_list.append((product_node.coefficient, combination))
    return final_overlapped_emu_list


def emu_equation_analyzer(
        metabolite_reaction_dict, target_emu_list, input_metabolite_name_set):
    def add_new_emu_to_queue(current_emu: EMUElement):
        # Num that a EMU has been added to queue in this path.
        insert_count['count'] += 1
        emu_need_to_add.put(((-1 * current_emu.emu_carbon_num, insert_count['count']), current_emu))

    def sort_emu_equations_dict_by_carbon_num(raw_emu_equations_dict):
        sorted_key_list = sorted(list(raw_emu_equations_dict.keys()))
        sorted_mid_equations_dict = {}
        for sorted_key in sorted_key_list:
            sorted_mid_equations_dict[sorted_key] = raw_emu_equations_dict[sorted_key]
        return sorted_mid_equations_dict

    # emu_mid_equations_dict_carbon_num_list = defaultdict(
    #     lambda: defaultdict(lambda: []))
    emu_mid_equations_dict_carbon_num_list = DefaultDict(DefaultDict([]))
    # Total num that a EMU has been added to queue or input set.
    complete_emu_visiting_num_dict = Counter()

    input_emu_dict = {}
    insert_count = {'count': 0}
    emu_need_to_add = PriorityQueue()
    for target_emu in target_emu_list:
        complete_emu_visiting_num_dict[target_emu.emu_name] += 1
        if target_emu.metabolite_name in input_metabolite_name_set:
            input_emu_dict[target_emu.emu_name] = target_emu
        else:
            add_new_emu_to_queue(target_emu)

    while not emu_need_to_add.empty():
        _, analyzing_emu = emu_need_to_add.get()
        for reaction in metabolite_reaction_dict[analyzing_emu.metabolite_name]:
            reaction_id = reaction.reaction_id
            if reaction_id == CoreConstants.biomass_flux_id:
                continue
            overlapped_emu_dict_combination_list = find_overlapped_emu(analyzing_emu, reaction)
            for coefficient, emu_dict_combination in overlapped_emu_dict_combination_list:
                emu_combination_list = []
                for overlapped_emu_dict in emu_dict_combination:
                    metabolite_name = overlapped_emu_dict['metabolite_name']
                    selected_carbon_list = overlapped_emu_dict['selected_carbon_list']
                    overlapped_emu_name = "{}{}{}".format(
                        metabolite_name, CoreConstants.emu_carbon_list_str_sep, "".join(
                            [str(num) for num in selected_carbon_list]))
                    # If the overlapped EMU is in input metabolite, just add it to input EMU list.
                    if metabolite_name in input_metabolite_name_set:
                        new_emu_element = EMUElement(metabolite_name, selected_carbon_list)
                        if overlapped_emu_name not in input_emu_dict:
                            input_emu_dict[overlapped_emu_name] = new_emu_element
                    # If the overlapped EMU is not input metabolite, check if it is visited in the path of current
                    # layer.
                    else:
                        new_emu_element = EMUElement(metabolite_name, selected_carbon_list)
                        if overlapped_emu_name not in complete_emu_visiting_num_dict:
                            complete_emu_visiting_num_dict[overlapped_emu_name] += 1
                            add_new_emu_to_queue(new_emu_element)
                    emu_combination_list.append(new_emu_element)
                if coefficient != 1:
                    emu_tuple = (reaction_id, emu_combination_list, coefficient)
                else:
                    emu_tuple = (reaction_id, emu_combination_list)
                emu_mid_equations_dict_carbon_num_list[analyzing_emu.emu_carbon_num][analyzing_emu.full_name].append(
                    emu_tuple)

    sorted_emu_equations_dict_carbon_num_list = sort_emu_equations_dict_by_carbon_num(
        emu_mid_equations_dict_carbon_num_list)
    return sorted_emu_equations_dict_carbon_num_list, input_emu_dict


def emu_matrix_equation_generator(
        emu_mid_equations_dict_carbon_num_list,
        input_emu_dict):
    # complete_emu_object_dict = {emu_name: decode_emu_name(emu_name) for emu_name in input_emu_name_set}
    complete_emu_object_dict = dict(input_emu_dict)
    # complete_emu_name_set = set(input_emu_name_set)
    emu_matrix_equation_dict = {}
    for carbon_num, emu_mid_equations_dict in emu_mid_equations_dict_carbon_num_list.items():
        this_layer_emu_dict_list = DictList()
        for emu_name in emu_mid_equations_dict.keys():
            if emu_name not in complete_emu_object_dict:
                complete_emu_object_dict[emu_name] = decode_emu_name(emu_name)
            this_layer_emu_dict_list[emu_name] = complete_emu_object_dict[emu_name]
            # this_layer_emu_dict_list.add(emu_name)
        # A * x = b * y
        input_and_lower_layer_emu_dict_list = DictList()
        # matrix_a_flux_location_dict = defaultdict(lambda: defaultdict(lambda: 0))
        # matrix_b_flux_location_dict = defaultdict(lambda: defaultdict(lambda: 0))
        matrix_a_flux_location_dict = DefaultDict(DefaultDict(0))
        matrix_b_flux_location_dict = DefaultDict(DefaultDict(0))
        for analyzed_emu_name, mid_equations_list in emu_mid_equations_dict.items():
            analyzed_emu_index = this_layer_emu_dict_list.index(analyzed_emu_name)
            for reaction_id, emu_combination_list, *param_list in mid_equations_list:
                # flux_value_tensor = flux_tensor[flux_name_index_dict[reaction_id]] * param_list[0]
                if len(param_list) == 1:
                    coefficient = param_list[0]
                else:
                    coefficient = 1.0
                if len(emu_combination_list) == 1:
                    emu_object = emu_combination_list[0]
                    dependent_emu_name = emu_object.emu_name
                    if dependent_emu_name in this_layer_emu_dict_list:
                        current_layer_emu_col_index = this_layer_emu_dict_list.index(dependent_emu_name)
                        matrix_a_flux_location_dict[
                            (analyzed_emu_index, current_layer_emu_col_index)][reaction_id] += coefficient
                    elif dependent_emu_name in complete_emu_object_dict:
                        input_and_lower_layer_emu_dict_list[dependent_emu_name] = emu_object
                        current_layer_input_col_index = input_and_lower_layer_emu_dict_list.index(dependent_emu_name)
                        matrix_b_flux_location_dict[
                            (analyzed_emu_index, current_layer_input_col_index)][reaction_id] -= coefficient
                    else:
                        raise ValueError()
                else:
                    for emu_object in emu_combination_list:
                        dependent_emu_name = emu_object.emu_name
                        if dependent_emu_name not in complete_emu_object_dict:
                            raise ValueError()
                    sorted_emu_combination_list = sorted(emu_combination_list)
                    dependent_emu_complete_name = CoreConstants.convolution_emu_sep.join(
                        [emu.full_name for emu in sorted_emu_combination_list])
                    if dependent_emu_complete_name not in input_and_lower_layer_emu_dict_list:
                        input_and_lower_layer_emu_dict_list[dependent_emu_complete_name] = sorted_emu_combination_list
                    current_layer_input_col_index = input_and_lower_layer_emu_dict_list.index(
                        dependent_emu_complete_name)
                    matrix_b_flux_location_dict[
                        (analyzed_emu_index, current_layer_input_col_index)][reaction_id] -= coefficient
                matrix_a_flux_location_dict[
                    (analyzed_emu_index, analyzed_emu_index)][reaction_id] -= coefficient
            # complete_emu_name_set.add(emu_name)
        matrix_a_dim = len(emu_mid_equations_dict)
        matrix_b_col = len(input_and_lower_layer_emu_dict_list)
        emu_matrix_equation_dict[carbon_num] = (
            this_layer_emu_dict_list, input_and_lower_layer_emu_dict_list,
            matrix_a_flux_location_dict, matrix_b_flux_location_dict, matrix_a_dim, matrix_b_col)
    return emu_matrix_equation_dict

