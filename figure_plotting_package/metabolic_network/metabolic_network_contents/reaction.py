from ..config import ElementName as BasicElementName, extract_display_name, ReactionConfig, \
    NetworkGeneralConfig, ParameterName
from ..metabolic_network_elements.reaction_element import ReactionElement


class Reaction(object):
    def __init__(
            self, reaction_name, reversible=False, reaction_start_end_list=None, change_arrow_by_value=True,
            extra_parameter_dict=None, **kwargs):
        self.reaction_name = reaction_name
        self.kwargs = kwargs
        self.display_reaction_name = extract_display_name(reaction_name)
        self.reaction_start_end_list = reaction_start_end_list
        if extra_parameter_dict is None:
            extra_parameter_dict = {}
        self.extra_parameter_dict = extra_parameter_dict

        self.reversible = False
        self.boundary_flux = False
        self.display_config_nested_dict = {}
        self.default_display_text_config = {}
        self.change_arrow_by_value = True
        self.forward_value = None
        self.backward_value = None
        self.net_value = None
        self.tail_arrow = None
        self.head_arrow = None
        self._initialize_tags(reversible, change_arrow_by_value)

    def _initialize_tags(self, reversible=False, change_arrow_by_value=True):
        self.reversible = reversible
        self.boundary_flux = False
        self.display_config_nested_dict = {}
        self.default_display_text_config = ReactionConfig.default_display_text_config
        self.change_arrow_by_value = change_arrow_by_value
        self.forward_value = None
        self.backward_value = None
        self.net_value = None
        self.tail_arrow = None
        self.head_arrow = None

    def reset(self):
        self.reaction_start_end_list = None
        self._initialize_tags()

    def set_reversible(self, reversible):
        self.reversible = reversible

    def set_reaction_start_end_list(self, new_start_end_list):
        self.reaction_start_end_list = new_start_end_list
        return self

    def extend_reaction_start_end_list(self, new_added_start_end_list):
        if self.reaction_start_end_list is None:
            self.reaction_start_end_list = []
        self.reaction_start_end_list.extend(new_added_start_end_list)
        return self

    def set_boundary_flux(self, boundary_flux: bool):
        self.boundary_flux = boundary_flux
        return self

    def set_display_text_config_dict(self, display_config_dict: dict, config_key=None):
        new_text_config_dict = dict(self.default_display_text_config)
        new_text_config_dict.update(display_config_dict)
        self.display_config_nested_dict[config_key] = new_text_config_dict
        return self

    def update_display_text_config_item(self, updated_display_config_dict: dict = None, config_key=None):
        if updated_display_config_dict is not None:
            if config_key is not None:
                self.display_config_nested_dict[config_key].update(updated_display_config_dict)
            else:
                for display_config_dict in self.display_config_nested_dict.values():
                    display_config_dict.update(updated_display_config_dict)
        return self

    def set_display_text(self, display_text: str, config_key=None):
        if self.reaction_name == NetworkGeneralConfig.biomass_str:
            display_text = f'Biomass reaction:\n{display_text}'
        self.update_display_text_config_item({ParameterName.string: display_text}, config_key)
        return self

    def set_value(self, flux_value):
        if isinstance(flux_value, (tuple, list)) and len(flux_value) == 2:
            forward, backward = flux_value
            self.net_value = abs(forward - backward)
        elif isinstance(flux_value, (float, int)):
            forward = flux_value
            backward = 0
            self.net_value = forward
        else:
            raise ValueError()
        self.forward_value = forward
        self.backward_value = backward

    def judge_bidirectional_flag(self):
        if not self.change_arrow_by_value:
            net_value = None
        else:
            net_value = self.net_value
        if self.tail_arrow is None:
            if self.reversible and net_value is None:
                head_arrow = tail_arrow = True
            else:
                if self.reversible and net_value is not None and \
                        self.backward_value > self.forward_value:
                    head_arrow = False
                    tail_arrow = True
                else:
                    head_arrow = True
                    tail_arrow = False
            self.tail_arrow = tail_arrow
            self.head_arrow = head_arrow
        return self.tail_arrow, self.head_arrow

    def judge_if_reverse(self):
        tail, head = self.judge_bidirectional_flag()
        return tail and not head

    def update_extra_parameter_dict(self, new_extra_parameter_dict):
        self.extra_parameter_dict.update(new_extra_parameter_dict)
        return self

    def to_element(self, scale=1, bottom_left_offset=None):
        gap_line_pair_list_label = ParameterName.gap_line_pair_list
        dash_solid_empty_width_label = ParameterName.dash_solid_empty_width
        branch_list_label = ParameterName.branch_list
        reaction_edge_parameter_list = []
        current_reaction_edge_dict = None
        for reaction_edge_property, *reaction_edge_parameter_tuple in self.reaction_start_end_list:
            if reaction_edge_property != ParameterName.branch:
                if current_reaction_edge_dict is not None:
                    reaction_edge_parameter_list.append(current_reaction_edge_dict)
                tail_arrow, head_arrow = self.judge_bidirectional_flag()
                if reaction_edge_property == ParameterName.normal:
                    tail, head, parameter_dict = reaction_edge_parameter_tuple
                    current_reaction_edge_dict = {
                        ParameterName.class_name: BasicElementName.Arrow,
                        ParameterName.tail: tail,
                        ParameterName.head: head,
                        ParameterName.tail_arrow: tail_arrow,
                        ParameterName.head_arrow: head_arrow,
                        ParameterName.boundary_flux: self.boundary_flux,
                        **self.extra_parameter_dict,
                    }
                elif reaction_edge_property == ParameterName.cycle:
                    theta_tail, theta_head, center, radius, parameter_dict = reaction_edge_parameter_tuple
                    current_reaction_edge_dict = {
                        ParameterName.class_name: BasicElementName.ArcArrow,
                        ParameterName.theta_tail: theta_tail,
                        ParameterName.theta_head: theta_head,
                        ParameterName.center: center,
                        ParameterName.radius: radius,
                        ParameterName.tail_arrow: tail_arrow,
                        ParameterName.head_arrow: head_arrow,
                        ParameterName.boundary_flux: self.boundary_flux,
                        **self.extra_parameter_dict,
                    }
                elif reaction_edge_property == ParameterName.path_cycle:
                    tail, mid, head, parameter_dict = reaction_edge_parameter_tuple
                    current_reaction_edge_dict = {
                        ParameterName.class_name: BasicElementName.ArcPathArrow,
                        ParameterName.tail: tail,
                        ParameterName.mid: mid,
                        ParameterName.head: head,
                        ParameterName.tail_arrow: tail_arrow,
                        ParameterName.head_arrow: head_arrow,
                        ParameterName.boundary_flux: self.boundary_flux,
                        **self.extra_parameter_dict,
                    }
                elif reaction_edge_property == ParameterName.bent:
                    tail, head, arrow_head_direction, parameter_dict = reaction_edge_parameter_tuple
                    current_reaction_edge_dict = {
                        ParameterName.class_name: BasicElementName.BentArrow,
                        ParameterName.tail: tail,
                        ParameterName.head: head,
                        ParameterName.radius: ReactionConfig.bent_reaction_radius,
                        ParameterName.arrow_head_direction: arrow_head_direction,
                        ParameterName.tail_arrow: tail_arrow,
                        ParameterName.head_arrow: head_arrow,
                        ParameterName.boundary_flux: self.boundary_flux,
                        **self.extra_parameter_dict,
                    }
                elif reaction_edge_property == ParameterName.broken:
                    tail, head, transition_point_list, parameter_dict = reaction_edge_parameter_tuple
                    current_reaction_edge_dict = {
                        ParameterName.class_name: BasicElementName.BrokenArrow,
                        ParameterName.tail: tail,
                        ParameterName.head: head,
                        ParameterName.tail_arrow: tail_arrow,
                        ParameterName.head_arrow: head_arrow,
                        ParameterName.boundary_flux: self.boundary_flux,
                        ParameterName.transition_point_list: transition_point_list,
                        **self.extra_parameter_dict,
                    }
                else:
                    raise ValueError()
                if gap_line_pair_list_label in parameter_dict:
                    current_reaction_edge_dict[gap_line_pair_list_label] = parameter_dict[gap_line_pair_list_label]
                if dash_solid_empty_width_label in parameter_dict:
                    current_reaction_edge_dict[dash_solid_empty_width_label] = parameter_dict[
                        dash_solid_empty_width_label]
            else:
                if current_reaction_edge_dict is None:
                    raise ValueError('Cannot put branch to first of reaction list')
                else:
                    stem_location, terminal_location, parameter_dict = reaction_edge_parameter_tuple
                    branch_parameter_dict = {
                        ParameterName.stem_location: stem_location,
                        ParameterName.terminal_location: terminal_location,
                    }
                    if ParameterName.arrow in parameter_dict:
                        branch_parameter_dict[ParameterName.arrow] = parameter_dict[ParameterName.arrow]
                    if ParameterName.dash in parameter_dict:
                        branch_parameter_dict[ParameterName.dash] = parameter_dict[ParameterName.dash]
                    if branch_list_label not in current_reaction_edge_dict:
                        current_reaction_edge_dict[branch_list_label] = []
                    current_reaction_edge_dict[branch_list_label].append(branch_parameter_dict)
        if current_reaction_edge_dict is not None:
            reaction_edge_parameter_list.append(current_reaction_edge_dict)
        display_text_param_nested_dict = {
            key: config_dict for key, config_dict in self.display_config_nested_dict.items()
            if ParameterName.string in config_dict
        }
        return ReactionElement(
            self.reaction_name, self.display_reaction_name, reaction_edge_parameter_list,
            display_text_param_nested_dict=display_text_param_nested_dict,
            scale=scale, bottom_left_offset=bottom_left_offset, **self.kwargs)
