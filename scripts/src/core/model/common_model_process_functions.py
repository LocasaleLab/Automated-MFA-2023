import warnings

from ..common.packages import it, np
from ..common.classes import DefaultDict
from ..common.config import CoreConstants

from .model_class import Reaction, CompositeReaction


# metabolite_reaction_dict = {
#     'AKG': [Reaction(id='R2', sub=('CIT'), pro=('AKG', 'CO2'))]
# }
def model_preprocess(
        reaction_list, symmetrical_metabolite_set, added_input_metabolite_set,
        emu_excluded_metabolite_set=None, balance_excluded_metabolite_set=None, target_metabolite_name_list=None,
        composite_reaction_list=None):
    """
    balance_excluded_metabolite_set will be added to final input metabolite dict.
    :param composite_reaction_list:
    :param emu_excluded_metabolite_set:
    :param reaction_list:
    :param symmetrical_metabolite_set:
    :param added_input_metabolite_set:
    :param balance_excluded_metabolite_set:
    :param target_metabolite_list:
    :return:
    """
    def extend_symmetric_metabolite_in_product_list(reaction_obj):
        new_product_list = []
        for product_node in reaction_obj.product_list:
            if product_node.name in symmetrical_metabolite_set:
                new_product_list.extend(product_node.split_symmetry())
            else:
                new_product_list.append(product_node)
        new_reaction_obj = reaction_obj.copy()
        new_reaction_obj.product_list = new_product_list
        return new_reaction_obj

    def process_one_reaction(reaction_obj):
        # Check repeat.
        if reaction_obj.reaction_id in reaction_set:
            raise KeyError("Reaction ID repeat! {}".format(reaction_obj.reaction_id))
        reaction_set.add(reaction_obj.reaction_id)
        flux_name_list.append(reaction_obj.reaction_id)

        # Process flux balance constraints.
        for substrate_node in reaction_obj.substrate_list:
            if substrate_node.name not in balance_excluded_metabolite_set:
                metabolite_reaction_dict[substrate_node.name][0][reaction_obj.reaction_id] += substrate_node.coefficient
        for product_node in reaction_obj.product_list:
            if product_node.name not in balance_excluded_metabolite_set:
                metabolite_reaction_dict[product_node.name][1][reaction_obj.reaction_id] += product_node.coefficient

        # Process EMU constraints
        reaction_obj = extend_symmetric_metabolite_in_product_list(reaction_obj)
        unique_metabolite_name_set = set()
        # Only append the reaction once for symmetrical metabolites
        for product_node in reaction_obj.product_list:
            metabolite_name = product_node.name
            if metabolite_name in emu_excluded_metabolite_set or metabolite_name in unique_metabolite_name_set:
                continue
            unique_metabolite_name_set.add(metabolite_name)
            product_reaction_dict_for_emu[metabolite_name].append(reaction_obj)

    def record_and_check_metabolite_carbon_num(reaction_obj):
        for metabolite_node in it.chain(reaction_obj.substrate_list, reaction_obj.product_list):
            metabolite_name = metabolite_node.name
            if metabolite_name not in complete_metabolite_dim_dict:
                current_metabolite_carbon_num = len(metabolite_node.carbon_composition_list)
                if metabolite_name not in complete_metabolite_dim_dict:
                    complete_metabolite_dim_dict[metabolite_name] = current_metabolite_carbon_num
                else:
                    if current_metabolite_carbon_num != 0 and \
                            complete_metabolite_dim_dict[metabolite_name] != current_metabolite_carbon_num:
                        raise ValueError('Metabolite carbon not consistent! {} in reaction {}'.format(
                            metabolite_name, reaction_obj.reaction_id))
                    elif current_metabolite_carbon_num == 0:
                        warnings.warn('Metabolite {} shows empty carbon str in reaction {}'.format(
                            metabolite_name, reaction_obj.reaction_id))

    # product_reaction_dict_for_emu = defaultdict(lambda: [])
    # metabolite_reaction_dict = defaultdict(lambda: (defaultdict(lambda: 0), defaultdict(lambda: 0)))
    product_reaction_dict_for_emu = DefaultDict([])
    metabolite_reaction_dict = DefaultDict((DefaultDict(0), DefaultDict(0)))
    if emu_excluded_metabolite_set is None:
        emu_excluded_metabolite_set = set()
    if balance_excluded_metabolite_set is None:
        balance_excluded_metabolite_set = set()
    if composite_reaction_list is None:
        composite_reaction_list = []
    flux_name_list = []
    reaction_set = set()
    complete_metabolite_dim_dict = {}
    composite_reaction_dict = {}

    # Parse reactions
    for current_reaction_dict in reaction_list:
        current_reaction = Reaction(**current_reaction_dict)
        record_and_check_metabolite_carbon_num(current_reaction)
        process_one_reaction(current_reaction)
        if current_reaction.reversible:
            reversed_reaction = current_reaction.reverse_reaction()
            process_one_reaction(reversed_reaction)

    # Generate common index for each flux to ensure the same order all over the code
    flux_name_index_dict = {flux_name: flux_index for flux_index, flux_name in enumerate(flux_name_list)}

    # Add composite reaction to flux dict
    for composite_reaction_parameter_dict in composite_reaction_list:
        composite_reaction_obj = CompositeReaction(**composite_reaction_parameter_dict)
        for composite_node_obj in composite_reaction_obj.compose_list:
            if composite_node_obj.reaction_id not in flux_name_index_dict:
                raise ValueError(
                    'Element {} of composite reaction {} has not be declared before!'.format(
                        composite_node_obj.reaction_id, composite_reaction_obj.reaction_id))
        composite_reaction_dict[composite_reaction_obj.reaction_id] = composite_reaction_obj
        flux_name_index_dict[composite_reaction_obj.reaction_id] = len(flux_name_index_dict)

    # Check flux balance relationship
    for balanced_metabolite_name, (reaction_dict_as_substrate, reaction_dict_as_product) in \
            metabolite_reaction_dict.items():
        if len(reaction_dict_as_substrate) == 0 or len(reaction_dict_as_product) == 0:
            raise ValueError('Flux to {} is unbalanced!'.format(balanced_metabolite_name))

    # Parse input metabolites
    input_metabolite_name_set = set()
    for input_metabolite_name in added_input_metabolite_set:
        if input_metabolite_name not in balance_excluded_metabolite_set:
            raise ValueError(
                'Input metabolite is not excluded from flux balance equations! {}'.format(input_metabolite_name))
        input_metabolite_name_set.add(input_metabolite_name)

    # Set all excluded EMU metabolites to unlabeled state.
    for emu_excluded_metabolite in emu_excluded_metabolite_set:
        if emu_excluded_metabolite not in added_input_metabolite_set:
            input_metabolite_name_set.add(emu_excluded_metabolite)

    # If target metabolite is not set, all non-excluded metabolites will be considered as target metabolites.
    if target_metabolite_name_list is None:
        target_metabolite_name_list = list(product_reaction_dict_for_emu.keys())

    # # Parse target EMU
    # target_emu_list = []
    # for target_metabolite in target_metabolite_list:
    #     carbon_num = complete_metabolite_dim_dict[target_metabolite]
    #     target_emu_list.append(EMUElement(target_metabolite, [1] * carbon_num))

    return metabolite_reaction_dict, product_reaction_dict_for_emu, composite_reaction_dict, flux_name_index_dict, \
        input_metabolite_name_set, complete_metabolite_dim_dict, target_metabolite_name_list


def compart_all_metabolites(all_metabolite_name_list, model_compartment_set):
    compartment_suffix_dict = {
        compartment_label: '_{}'.format(compartment_label) for compartment_label in model_compartment_set}
    # complete_compartment_metabolite_dict = defaultdict(lambda: set())
    complete_tissue_compartment_metabolite_dict = {}
    metabolite_bare_metabolite_name_dict = {}
    for current_metabolite_name in all_metabolite_name_list:
        target_model_compartment = None
        bare_metabolite_name_with_tissue = None
        for model_compartment, compartment_suffix in compartment_suffix_dict.items():
            if current_metabolite_name.endswith(compartment_suffix):
                target_model_compartment = model_compartment
                bare_metabolite_name_with_tissue = current_metabolite_name[:-len(compartment_suffix)]
                break
        if target_model_compartment is None:
            bare_metabolite_name_with_tissue = current_metabolite_name
        if bare_metabolite_name_with_tissue is None:
            raise ValueError()
        *tissue_prefix_list, bare_metabolite_name = bare_metabolite_name_with_tissue.split(
            CoreConstants.specific_tissue_sep)
        if len(tissue_prefix_list) == 0:
            tissue_prefix = None
        else:
            tissue_prefix = tissue_prefix_list[0]
        if tissue_prefix not in complete_tissue_compartment_metabolite_dict:
            complete_tissue_compartment_metabolite_dict[tissue_prefix] = {}
        if target_model_compartment not in complete_tissue_compartment_metabolite_dict[tissue_prefix]:
            complete_tissue_compartment_metabolite_dict[tissue_prefix][target_model_compartment] = set()
        complete_tissue_compartment_metabolite_dict[tissue_prefix][target_model_compartment].add(
            current_metabolite_name)
        metabolite_bare_metabolite_name_dict[current_metabolite_name] = bare_metabolite_name
    return complete_tissue_compartment_metabolite_dict, metabolite_bare_metabolite_name_dict


def metabolite_carbon_number_verification(complete_metabolite_dim_dict, metabolite_bare_metabolite_name_dict):
    bare_metabolite_dim_dict = {}
    for complete_metabolite_name, metabolite_dim in complete_metabolite_dim_dict.items():
        bare_metabolite_name = metabolite_bare_metabolite_name_dict[complete_metabolite_name]
        if bare_metabolite_name in bare_metabolite_dim_dict:
            current_metabolite_dim = bare_metabolite_dim_dict[bare_metabolite_name]
            if metabolite_dim != current_metabolite_dim:
                raise ValueError(
                    'Dim of new metabolite {} is {}, while the previous dim of metabolite {} is {}'.format(
                        complete_metabolite_name, metabolite_dim, bare_metabolite_name, current_metabolite_dim))
        else:
            bare_metabolite_dim_dict[bare_metabolite_name] = metabolite_dim
    return bare_metabolite_dim_dict


def flux_balance_equation_generator(metabolite_reaction_dict, composite_reaction_dict, flux_name_index_dict):
    flux_size = len(flux_name_index_dict)
    metabolite_size = len(metabolite_reaction_dict)
    composite_reaction_size = len(composite_reaction_dict)
    complete_size = metabolite_size + composite_reaction_size
    flux_balance_matrix = np.zeros((complete_size, flux_size))
    for metabolite_index, (metabolite, (flux_dict_as_substrate, flux_dict_as_product)) in enumerate(
            metabolite_reaction_dict.items()):
        for reaction_id, reaction_coefficient in flux_dict_as_substrate.items():
            flux_index = flux_name_index_dict[reaction_id]
            flux_balance_matrix[metabolite_index, flux_index] -= reaction_coefficient
        for reaction_id, reaction_coefficient in flux_dict_as_product.items():
            flux_index = flux_name_index_dict[reaction_id]
            flux_balance_matrix[metabolite_index, flux_index] += reaction_coefficient
    for composite_reaction_row_index, (composite_reaction_id, composite_reaction_obj) in enumerate(
            composite_reaction_dict.items()):
        current_row_index = metabolite_size + composite_reaction_row_index
        composite_flux_index = flux_name_index_dict[composite_reaction_id]
        flux_balance_matrix[current_row_index, composite_flux_index] -= 1
        for composite_node_obj in composite_reaction_obj.compose_list:
            raw_flux_index = flux_name_index_dict[composite_node_obj.reaction_id]
            flux_balance_matrix[current_row_index, raw_flux_index] += composite_node_obj.coefficient
    flux_balance_right_side = np.zeros(complete_size)
    return flux_balance_matrix, flux_balance_right_side
