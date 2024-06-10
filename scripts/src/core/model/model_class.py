from ..common.classes import default_transform_dict
from ..common.config import CoreConstants, ModelKeyword
from ..common.functions import reverse_reaction_name


class EMUMIDDimDict(object):
    def __init__(self):
        self.metabolite_dim_dict = {}
        pass

    def __getitem__(self, item):
        if item in self.metabolite_dim_dict:
            return self.metabolite_dim_dict[item]
        else:
            metabolite_name, emu_equation_string, *param_list = item.split(CoreConstants.emu_carbon_list_str_sep)
            carbon_num = emu_equation_string.count("1")
            self.metabolite_dim_dict[item] = carbon_num + 1
            return carbon_num + 1

    def __copy__(self):
        new_item = EMUMIDDimDict()
        new_item.metabolite_dim_dict = dict(self.metabolite_dim_dict)
        return new_item

    def copy(self):
        return self.__copy__()


# node = ('OAC', 'abcd', 2)
class Node(object):
    def __init__(self, name, carbon_composition_string, coefficient: float = 1):
        self.name = name
        self.coefficient = coefficient
        if isinstance(carbon_composition_string, str):
            # if '-' in carbon_composition_string:
            #     carbon_composition_list = carbon_composition_string.split(CoreConstants.carbon_list_unofficial_sep)
            # else:
            carbon_composition_list = list(carbon_composition_string)
        elif isinstance(carbon_composition_string, (list, tuple)):
            carbon_composition_list = list(carbon_composition_string)
        else:
            raise ValueError('Carbon composition format not allowed!')
        self.carbon_composition_list = carbon_composition_list

    def split_symmetry(self):
        return (Node(self.name, self.carbon_composition_list, self.coefficient / 2),
                Node(self.name, list(reversed(self.carbon_composition_list)), self.coefficient / 2))

    def __repr__(self):
        return "Node({:.1f}__{}__{})".format(self.coefficient, self.name, "-".join(self.carbon_composition_list))

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.carbon_composition_list == other.carbon_constitution_list,
            self.coefficient == other.coefficient])


# reaction_list = [
#     {
#         'id': 'R1',
#         'sub': [('OAC', 'abcd'), ('ACCOA', 'ef')],
#         'pro': [('CIT', 'dcbfea')],
#     },...]
class Reaction(object):
    def __init__(self, id: str, sub, pro, reverse=False, num_id=0):
        self.reaction_id = id
        substrate_list = []
        product_list = []
        for param_tuple in sub:
            if isinstance(param_tuple, Node):
                substrate_list.append(param_tuple)
            else:
                substrate_list.append(Node(*param_tuple))
        for param_tuple in pro:
            if isinstance(param_tuple, Node):
                product_list.append(param_tuple)
            else:
                product_list.append(Node(*param_tuple))
        self.substrate_list = substrate_list
        self.product_list = product_list
        self.reversible = reverse
        self.num_id = num_id

    def copy(self):
        return Reaction(self.reaction_id, self.substrate_list, self.product_list, self.reversible, self.num_id)

    def __repr__(self):
        return "Reaction({}, {}, {})".format(
            self.reaction_id, " ".join([node.name for node in self.substrate_list]),
            " ".join([node.name for node in self.product_list]))

    def __hash__(self):
        return self.reaction_id.__hash__()

    def reverse_reaction(self, num_id=0):
        new_reaction_id = reverse_reaction_name(self.reaction_id)
        new_product_list = self.substrate_list
        new_substrate_list = self.product_list
        if num_id == 0:
            num_id = self.num_id + 1
        return Reaction(new_reaction_id, new_substrate_list, new_product_list, False, num_id)


class CompositeNode(object):
    def __init__(self, reaction_id, coefficient: float = 1):
        self.reaction_id = reaction_id
        self.coefficient = float(coefficient)

    def __repr__(self):
        return "CompositeNode({}, {})".format(
            self.coefficient, self.reaction_id)


class CompositeReaction(object):
    def __init__(self, id: str, comp, flux_range=ModelKeyword.normal_range_type):
        self.reaction_id = id
        compose_list = []
        for param_tuple in comp:
            if isinstance(param_tuple, CompositeNode):
                compose_list.append(param_tuple)
            else:
                compose_list.append(CompositeNode(*param_tuple))
        self.compose_list = compose_list
        if isinstance(flux_range, str):
            self.flux_range = flux_range
            self.specific_range = None
        elif isinstance(flux_range, tuple) or isinstance(flux_range, list):
            if len(flux_range) != 2:
                raise ValueError('Range of flux {} not recognized!: {}'.format(id, flux_range))
            self.flux_range = ModelKeyword.specific_range_type
            self.specific_range = flux_range
        else:
            raise ValueError('Range of flux {} not recognized!: {}'.format(id, flux_range))

    def copy(self):
        return CompositeReaction(self.reaction_id, self.compose_list)

    def __repr__(self):
        return "CompositeReaction({}, {})".format(
            self.reaction_id, " ".join([node.reaction_id for node in self.compose_list]))


class EMUElement(object):
    """
        EMU name format: NAME__CODE. eg: PYR__011
        select_carbon_list: [1, 0, 1]
        metabolite_name="", selected_carbon_list=(), emu_name=""
    """
    def __init__(
            self, metabolite_name, selected_carbon_list, repeat_num=1, previous_visited_emu_name_set=None,
            convoluted_emu_list=None, append_carbon_to_name=True):
        def analyze_name(_metabolite_name):
            compartment = ""
            tissue = ""
            property_list = _metabolite_name.split('_')
            if len(property_list) > 1:
                compartment = property_list[1]
            if len(property_list) > 2:
                tissue = property_list[2]
            return compartment, tissue

        self.metabolite_name = metabolite_name
        self.compartment, self.tissue = analyze_name(metabolite_name)
        self.total_carbon_num = len(selected_carbon_list)
        self.emu_carbon_num = sum(selected_carbon_list)
        self.selected_carbon_list = list(selected_carbon_list)
        carbon_string_list = [str(num) for num in selected_carbon_list]

        if convoluted_emu_list is not None:
            if append_carbon_to_name:
                self_emu_name = '{}__{}'.format(metabolite_name, "".join(carbon_string_list))
            else:
                self_emu_name = metabolite_name
            convoluted_emu_full_name_list = ', '.join([emu_obj.full_name for emu_obj in convoluted_emu_list])
            emu_name = f'{CoreConstants.convolution_id}_{self_emu_name}({convoluted_emu_full_name_list})'
            convoluted_emu = True
        else:
            if append_carbon_to_name:
                emu_name = '{}__{}'.format(metabolite_name, "".join(carbon_string_list))
            else:
                emu_name = metabolite_name
            convoluted_emu = False

        if repeat_num > 1:
            full_name = "{}__{}".format(emu_name, repeat_num)
        else:
            full_name = emu_name
        self.emu_name = emu_name
        self.full_name = full_name
        if previous_visited_emu_name_set is None:
            previous_visited_emu_name_set = set()
        self.visited_emu_name_set = previous_visited_emu_name_set | {self.emu_name}
        self.repeat_num = repeat_num
        self.equivalent_emu_list = []
        self.convoluted_emu = convoluted_emu
        self.convoluted_emu_list = convoluted_emu_list

    def more_repeat_num_emu(self):
        return EMUElement(self.metabolite_name, self.selected_carbon_list, self.repeat_num + 1)

    def __eq__(self, other):
        return all([
            self.full_name == other.full_name,
            self.metabolite_name == other.metabolite_name,
            self.total_carbon_num == other.total_carbon_num,
            self.selected_carbon_list == other.selected_carbon_list,
            self.emu_carbon_num == other.emu_carbon_num])

    def __hash__(self):
        return self.full_name.__hash__()

    def __repr__(self):
        return "EMU({})".format(self.full_name)

    def __lt__(self, other):
        return self.full_name < other.full_name

    def copy_to_convolution(self, convoluted_emu_list):
        return EMUElement(
            self.metabolite_name, self.selected_carbon_list, self.repeat_num,
            convoluted_emu_list=convoluted_emu_list)


class UserDefinedModel(object):
    def __init__(
            self, reaction_list=None, reaction_dict=None, symmetrical_metabolite_set=None,
            added_input_metabolite_set=None, emu_excluded_metabolite_set=None, balance_excluded_metabolite_set=None,
            target_metabolite_list=None, model_compartment_set=None, composite_reaction_list=None,
            other_pool_metabolite_dict=None, model_tissue_set=None, model_metabolite_to_standard_name_dict=None):
        if reaction_list is not None and reaction_dict is not None:
            raise ValueError('Reaction list and reaction dict cannot be provided simultaneously!')
        if reaction_list is not None:
            reaction_dict = {}
            for reaction_item in reaction_list:
                current_id = reaction_item['id']
                if current_id in reaction_dict:
                    raise ValueError('Repeat reaction ID! {}'.format(current_id))
                reaction_dict[current_id] = reaction_item
        elif reaction_dict is not None:
            reaction_list = list(reaction_dict.values())
        else:
            raise ValueError('Either reaction_list or reaction_dict should not be None')
        self.reaction_list = reaction_list
        self.reaction_dict = reaction_dict
        if symmetrical_metabolite_set is None:
            symmetrical_metabolite_set = set()
        self.symmetrical_metabolite_set = symmetrical_metabolite_set
        if added_input_metabolite_set is None:
            added_input_metabolite_set = set()
        self.added_input_metabolite_set = added_input_metabolite_set
        if emu_excluded_metabolite_set is None:
            emu_excluded_metabolite_set = set()
        self.emu_excluded_metabolite_set = emu_excluded_metabolite_set
        if balance_excluded_metabolite_set is None:
            balance_excluded_metabolite_set = set()
        self.balance_excluded_metabolite_set = balance_excluded_metabolite_set
        self.target_metabolite_list = target_metabolite_list
        if model_compartment_set is None:
            model_compartment_set = set()
        self.model_compartment_set = model_compartment_set
        if composite_reaction_list is None:
            composite_reaction_list = []
        self.composite_reaction_list = composite_reaction_list
        if model_metabolite_to_standard_name_dict is None:
            model_metabolite_to_standard_name_dict = default_transform_dict
        self.model_metabolite_to_standard_name_dict = model_metabolite_to_standard_name_dict
        if other_pool_metabolite_dict is None:
            other_pool_metabolite_dict = {
                ModelKeyword.general: emu_excluded_metabolite_set}
        self.other_pool_metabolite_dict = other_pool_metabolite_dict
        if model_tissue_set is None:
            model_tissue_set = set()
        self.model_tissue_set = model_tissue_set


class MFAModel(object):
    def __init__(
            self, input_emu_dict, target_emu_list, emu_mid_equation_dict, emu_name_dependency_dict,
            composite_reaction_dict, complete_emu_dim_dict, complete_emu_obj_index_dict,
            flux_name_index_dict, flux_balance_matrix,
            flux_balance_right_side_vector, bare_metabolite_dim_dict, metabolite_bare_metabolite_name_dict,
            complete_tissue_compartment_metabolite_dict, input_metabolite_name_set, all_target_metabolite_name_set,
            model_metabolite_to_standard_name_dict, user_defined_model):
        self.input_emu_dict = input_emu_dict
        self.target_emu_list = target_emu_list
        self.emu_name_dependency_dict = emu_name_dependency_dict
        self.emu_mid_equation_dict = emu_mid_equation_dict
        self.composite_reaction_dict = composite_reaction_dict
        self.complete_emu_dim_dict = complete_emu_dim_dict
        self.complete_emu_obj_index_dict = complete_emu_obj_index_dict
        self.flux_name_index_dict = flux_name_index_dict
        self.flux_balance_matrix = flux_balance_matrix
        self.flux_balance_right_side_vector = flux_balance_right_side_vector
        self.bare_metabolite_dim_dict = bare_metabolite_dim_dict
        self.metabolite_bare_metabolite_name_dict = metabolite_bare_metabolite_name_dict
        self.complete_tissue_compartment_metabolite_dict = complete_tissue_compartment_metabolite_dict
        self.input_metabolite_name_set = input_metabolite_name_set
        self.all_target_metabolite_name_set = all_target_metabolite_name_set
        self.model_metabolite_to_standard_name_dict = model_metabolite_to_standard_name_dict
        self.user_defined_model = user_defined_model

