from .config import Vector, ParameterName, NetworkGeneralConfig, LegendConfig
from .config import CompositeFigure, TextBox, flux_value_mapper_dict, TextCommentConfig

from .layout_generator_functions import network_layout_generator, exchange_partial_network_layout_generator, \
    legend_layout_generator, text_comment_layout_generator, multi_tissue_network_layout_generator
from .metabolic_network_contents.content_list import MetaboliteList, ReactionList, SubnetworkList, assign_value_to_network, \
    assign_flux_name_to_network

network_height_to_width_ratio = NetworkGeneralConfig.network_height_to_width_ratio
display_value_format_string = NetworkGeneralConfig.display_value_format_string


def set_and_convert_network_elements(
        metabolite_list, reaction_list, subnetwork_list=None, other_text_list=(), other_obj_list=(),
        input_metabolite_set=None, c13_labeling_metabolite_set=None, mid_data_metabolite_set=None,
        mixed_mid_data_metabolite_set=None, biomass_metabolite_set=None, invalid_metabolite_set=None,
        boundary_flux_set=None, hidden_metabolite_set=None, hidden_reaction_set=None,
        metabolite_data_sensitivity_state_dict=None, reaction_data_sensitivity_state_dict=None,
        display_flux_name=False, reaction_text_dict=None, reaction_text_config_dict=None,
        reaction_raw_value_dict=None, flux_value_mapper=None, extra_parameter_dict=None):
    """
    Priority:
    display_flux_name > reaction_text_dict > reaction_raw_value_dict
    """
    all_data_mode = False
    all_mixed_data_mode = False
    if input_metabolite_set is None:
        input_metabolite_set = set()
    if c13_labeling_metabolite_set is None:
        c13_labeling_metabolite_set = set()
    if isinstance(mid_data_metabolite_set, str):
        if mid_data_metabolite_set == ParameterName.all_data_mode:
            all_data_mode = True
        if mid_data_metabolite_set == ParameterName.all_mixed_data_mode:
            all_mixed_data_mode = True
    elif mid_data_metabolite_set is None:
        mid_data_metabolite_set = set()
    if mixed_mid_data_metabolite_set is None:
        mixed_mid_data_metabolite_set = set()
    if biomass_metabolite_set is None:
        biomass_metabolite_set = set()
    if invalid_metabolite_set is None:
        invalid_metabolite_set = set()
    if boundary_flux_set is None:
        boundary_flux_set = set()
    if hidden_metabolite_set is None:
        hidden_metabolite_set = set()
    if hidden_reaction_set is None:
        hidden_reaction_set = set()
    if extra_parameter_dict is None:
        extra_parameter_dict = {}
    display_flux_value = False
    if display_flux_name:
        assign_flux_name_to_network(reaction_list)
    else:
        if reaction_text_dict is None:
            if reaction_raw_value_dict is not None:
                display_flux_value = True
            reaction_text_dict = {}
    if metabolite_data_sensitivity_state_dict is None:
        metabolite_data_sensitivity_state_dict = {}
    if reaction_data_sensitivity_state_dict is None:
        reaction_data_sensitivity_state_dict = {}

    metabolite_element_list = []
    for _, metabolite_obj in metabolite_list.content_list_pair:
        if metabolite_obj.center is None or metabolite_obj.metabolite_name in hidden_metabolite_set:
            continue
        if metabolite_obj.metabolite_name in extra_parameter_dict:
            metabolite_obj.update_extra_parameter_dict(extra_parameter_dict[metabolite_obj.metabolite_name])
        if metabolite_obj.metabolite_name in input_metabolite_set:
            metabolite_obj.set_input_state(True)
            if metabolite_obj.metabolite_name in c13_labeling_metabolite_set:
                metabolite_obj.set_c13_labeling_state(True)
        elif all_data_mode or all_mixed_data_mode:
            # Under all data mode, all metabolites that are not input metabolite have known MID data
            metabolite_obj.set_mid_data_state(True)
        if metabolite_obj.metabolite_name in mid_data_metabolite_set:
            metabolite_obj.set_mid_data_state(True)
        if not all_data_mode:
            # No metabolite is mixed under all data. All metabolites are mixed under all mixed data mode
            if all_mixed_data_mode or metabolite_obj.metabolite_name in mixed_mid_data_metabolite_set:
                metabolite_obj.set_mixed_mid_data_state(True)
        if metabolite_obj.metabolite_name in biomass_metabolite_set:
            metabolite_obj.set_biomass_flux_state(True)
        if metabolite_obj.metabolite_name in invalid_metabolite_set:
            metabolite_obj.set_invalid_state(True)
        if metabolite_obj.metabolite_name in metabolite_data_sensitivity_state_dict:
            metabolite_obj.set_data_sensitivity_state(
                metabolite_data_sensitivity_state_dict[metabolite_obj.metabolite_name])
        # metabolite_element_list.append(metabolite_obj.to_element(scale, bottom_left_offset))
        metabolite_element_list.append(metabolite_obj.to_element())
    reaction_element_list = []
    for _, reaction_obj in reaction_list.content_list_pair:
        if reaction_obj.reaction_start_end_list is None or reaction_obj.reaction_name in hidden_reaction_set:
            continue
        if reaction_obj.reaction_name in extra_parameter_dict:
            reaction_obj.update_extra_parameter_dict(extra_parameter_dict[reaction_obj.reaction_name])
        if reaction_obj.reaction_name in boundary_flux_set:
            reaction_obj.set_boundary_flux(True)
        if display_flux_name:
            pass
        elif display_flux_value:
            if reaction_obj.net_value is not None:
                flux_value = reaction_obj.net_value
            elif reaction_raw_value_dict is not None and reaction_obj.reaction_name in reaction_raw_value_dict:
                flux_value = reaction_raw_value_dict[reaction_obj.reaction_name]
            else:
                flux_value = None
            if flux_value is not None:
                reaction_obj.set_display_text(display_value_format_string.format(flux_value))
                if flux_value_mapper is not None:
                    reaction_obj.update_extra_parameter_dict(flux_value_mapper(flux_value))
        elif reaction_obj.reaction_name in reaction_text_dict:
            reaction_obj.set_display_text(reaction_text_dict[reaction_obj.reaction_name])
            reaction_obj.update_display_text_config_item(reaction_text_config_dict)
        if reaction_obj.reaction_name in reaction_data_sensitivity_state_dict:
            reaction_obj.set_data_sensitivity_state(
                reaction_data_sensitivity_state_dict[reaction_obj.reaction_name])
        # reaction_element_list.append(reaction_obj.to_element(scale, bottom_left_offset))
        reaction_element_list.append(reaction_obj.to_element())
    subnetwork_element_list = []
    if subnetwork_list is not None:
        for _, subnetwork_obj in subnetwork_list.content_list_pair:
            if subnetwork_obj.left_right_location is None:
                continue
            # subnetwork_element_list.append(subnetwork_obj.to_element(scale, bottom_left_offset))
            subnetwork_element_list.append(subnetwork_obj.to_element())
    other_text_obj_list = []
    for other_text_config_dict in other_text_list:
        other_text_obj_list.append(TextBox(**other_text_config_dict))
    metabolic_element_dict = {
        ParameterName.metabolite: {metabolite_obj.name: metabolite_obj for metabolite_obj in metabolite_element_list},
        ParameterName.reaction: {reaction_obj.name: reaction_obj for reaction_obj in reaction_element_list},
        ParameterName.subnetwork: {subnetwork_obj.name: subnetwork_obj for subnetwork_obj in subnetwork_element_list},
        ParameterName.other_text: {other_text_obj.name: other_text_obj for other_text_obj in other_text_obj_list},
        ParameterName.other_obj: {other_obj.name: other_obj for other_obj in other_obj_list},
    }
    return metabolic_element_dict


class MetabolicNetwork(CompositeFigure):
    height_to_width_ratio = network_height_to_width_ratio

    def __init__(
            self, input_metabolite_set=None, c13_labeling_metabolite_set=None, mid_data_metabolite_set=None,
            mixed_mid_data_metabolite_set=None, biomass_metabolite_set=None, boundary_flux_set=None,
            hidden_metabolite_set=None, hidden_reaction_set=None,
            metabolite_data_sensitivity_state_dict=None, reaction_data_sensitivity_state_dict=None,
            display_flux_name=False, reaction_text_dict=None, reaction_text_config_dict=None,
            reaction_raw_value_dict=None, visualize_flux_value=None, visualize_flux_param_dict=None,
            infusion=False, with_glns_m=False, absolute_value_output_value_dict=None, extra_parameter_dict=None,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        metabolite_list = MetaboliteList(infusion)
        reaction_list = ReactionList(infusion, with_glns_m)
        subnetwork_list = SubnetworkList(infusion)
        other_text_list = []
        flux_value_mapper = None
        if reaction_raw_value_dict is not None:
            assign_value_to_network(reaction_raw_value_dict, reaction_list, infusion)
            if visualize_flux_value is not None:
                if visualize_flux_param_dict is None:
                    visualize_flux_param_dict = {}
                flux_value_mapper = flux_value_mapper_dict[visualize_flux_value](
                    reaction_list, absolute_value_output_value_dict=absolute_value_output_value_dict)
        network_layout_generator(metabolite_list, reaction_list, subnetwork_list, other_text_list, infusion)
        metabolic_element_dict = set_and_convert_network_elements(
            metabolite_list, reaction_list, subnetwork_list, other_text_list,
            input_metabolite_set=input_metabolite_set, c13_labeling_metabolite_set=c13_labeling_metabolite_set,
            mid_data_metabolite_set=mid_data_metabolite_set,
            mixed_mid_data_metabolite_set=mixed_mid_data_metabolite_set,
            biomass_metabolite_set=biomass_metabolite_set, boundary_flux_set=boundary_flux_set,
            hidden_metabolite_set=hidden_metabolite_set, hidden_reaction_set=hidden_reaction_set,
            metabolite_data_sensitivity_state_dict=metabolite_data_sensitivity_state_dict,
            reaction_data_sensitivity_state_dict=reaction_data_sensitivity_state_dict,
            display_flux_name=display_flux_name, reaction_text_dict=reaction_text_dict,
            reaction_text_config_dict=reaction_text_config_dict,
            reaction_raw_value_dict=reaction_raw_value_dict, flux_value_mapper=flux_value_mapper,
            extra_parameter_dict=extra_parameter_dict)

        if bottom_left_offset is None:
            bottom_left_offset = Vector(0, 0)
        super().__init__(
            metabolic_element_dict, bottom_left_offset, Vector(scale, scale * self.height_to_width_ratio),
            scale=scale, bottom_left_offset=bottom_left_offset,
            base_z_order=base_z_order, z_order_increment=z_order_increment, **kwargs)


class MetabolicNetworkLegend(CompositeFigure):
    total_width = LegendConfig.legend_width

    def __init__(
            self, mode=ParameterName.normal, legend_config_dict=None, extra_parameter_dict=None, **kwargs):
        patch_raw_obj_dict, text_param_dict, total_width, total_height = legend_layout_generator(
            mode, legend_config_dict)
        self.height_to_width_ratio = total_height / total_width
        common_text_param_dict = LegendConfig.common_text_param_dict
        patch_obj_list = [
            patch_raw_obj.to_element()
            for name, patch_raw_obj in patch_raw_obj_dict.items()
        ]
        if extra_parameter_dict is None:
            extra_parameter_dict = {}
        text_box_list = [
            TextBox(**{
                **text_basic_param_dict,
                **common_text_param_dict,
                **extra_parameter_dict,
            })
            for text_basic_param_dict in text_param_dict.values()
        ]

        metabolic_legend_element_dict = {
            ParameterName.patch: {patch_obj.name: patch_obj for patch_obj in patch_obj_list},
            ParameterName.text_box: {text_box.name: text_box for text_box in text_box_list}
        }
        super().__init__(
            metabolic_legend_element_dict,
            # bottom_left_offset, Vector(scale, scale * self.height_to_width_ratio),
            Vector(0, 0), Vector(total_width, total_height), **kwargs)


class MetabolicNetworkTextComment(CompositeFigure):
    total_width = LegendConfig.legend_width

    def __init__(self, metabolic_network_text_comment_config_dict, mode=ParameterName.normal, **kwargs):
        specific_text_param_dict, total_width, total_height = text_comment_layout_generator(
            mode, metabolic_network_text_comment_config_dict)
        self.height_to_width_ratio = total_height / total_width
        common_text_param_dict = TextCommentConfig.comment_text_common_param_dict
        text_box_list = [
            TextBox(**{
                **text_basic_param_dict,
                **common_text_param_dict
            })
            for text_basic_param_dict in specific_text_param_dict.values()
        ]

        metabolic_network_comment_element_dict = {
            ParameterName.text_box: {text_box.name: text_box for text_box in text_box_list}
        }
        super().__init__(
            metabolic_network_comment_element_dict, Vector(0, 0), Vector(total_width, total_height), **kwargs)


class ExchangeMetabolicNetwork(CompositeFigure):
    height_to_width_ratio = network_height_to_width_ratio

    def __init__(
            self, display_flux_name=False, reaction_raw_value_dict=None, visualize_flux_value=None,
            absolute_value_output_value_dict=None, small_network=False,
            input_metabolite_set=None, c13_labeling_metabolite_set=None, mid_data_metabolite_set=None,
            mixed_mid_data_metabolite_set=None, biomass_metabolite_set=None, boundary_flux_set=None,
            hidden_metabolite_set=None, hidden_reaction_set=None,
            metabolite_data_sensitivity_state_dict=None, reaction_data_sensitivity_state_dict=None,
            reaction_text_dict=None, reaction_text_config_dict=None, extra_parameter_dict=None,

            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        metabolite_list = MetaboliteList(infusion=False)
        reaction_list = ReactionList(infusion=False)
        subnetwork_list = SubnetworkList(infusion=False)
        other_text_list = []
        flux_value_mapper = None
        if reaction_raw_value_dict is not None:
            assign_value_to_network(reaction_raw_value_dict, reaction_list)
            if visualize_flux_value is not None:
                flux_value_mapper = flux_value_mapper_dict[visualize_flux_value](
                    reaction_list, absolute_value_output_value_dict=absolute_value_output_value_dict)
        total_width, total_height = exchange_partial_network_layout_generator(
            metabolite_list, reaction_list, subnetwork_list, other_text_list, smaller_network=small_network)
        metabolic_element_dict = set_and_convert_network_elements(
            metabolite_list, reaction_list, subnetwork_list, other_text_list,
            input_metabolite_set=input_metabolite_set, c13_labeling_metabolite_set=c13_labeling_metabolite_set,
            mid_data_metabolite_set=mid_data_metabolite_set,
            mixed_mid_data_metabolite_set=mixed_mid_data_metabolite_set,
            biomass_metabolite_set=biomass_metabolite_set, boundary_flux_set=boundary_flux_set,
            hidden_metabolite_set=hidden_metabolite_set, hidden_reaction_set=hidden_reaction_set,
            metabolite_data_sensitivity_state_dict=metabolite_data_sensitivity_state_dict,
            reaction_data_sensitivity_state_dict=reaction_data_sensitivity_state_dict,
            display_flux_name=display_flux_name, reaction_text_dict=reaction_text_dict,
            reaction_text_config_dict=reaction_text_config_dict,
            reaction_raw_value_dict=reaction_raw_value_dict, flux_value_mapper=flux_value_mapper,
            extra_parameter_dict=extra_parameter_dict)

        if bottom_left_offset is None:
            bottom_left_offset = Vector(0, 0)
        super().__init__(
            metabolic_element_dict, bottom_left_offset, Vector(total_width, total_height) * scale,
            scale=scale, bottom_left_offset=bottom_left_offset,
            base_z_order=base_z_order, z_order_increment=z_order_increment, background=False, **kwargs)


class MultiTissueMetabolicNetwork(CompositeFigure):
    height_to_width_ratio = network_height_to_width_ratio

    def __init__(
            self, input_metabolite_set=None, c13_labeling_metabolite_set=None, mid_data_metabolite_set=None,
            mixed_mid_data_metabolite_set=None, biomass_metabolite_set=None, boundary_flux_set=None,
            hidden_metabolite_set=None, hidden_reaction_set=None,
            metabolite_data_sensitivity_state_dict=None, reaction_data_sensitivity_state_dict=None,
            display_flux_name=False, reaction_text_dict=None, reaction_text_config_dict=None,
            reaction_raw_value_dict=None, visualize_flux_value=None, visualize_flux_param_dict=None,
            infusion=False, absolute_value_output_value_dict=None, extra_parameter_dict=None,
            tissue_name=None, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        metabolite_list = MetaboliteList(infusion)
        reaction_list = ReactionList(infusion)
        subnetwork_list = SubnetworkList(infusion)
        other_text_list = []
        flux_value_mapper = None
        if reaction_raw_value_dict is not None:
            assign_value_to_network(reaction_raw_value_dict, reaction_list, infusion)
            if visualize_flux_value is not None:
                if visualize_flux_param_dict is None:
                    visualize_flux_param_dict = {}
                flux_value_mapper = flux_value_mapper_dict[visualize_flux_value](
                    reaction_list, absolute_value_output_value_dict=absolute_value_output_value_dict)
        multi_tissue_network_layout_generator(
            metabolite_list, reaction_list, subnetwork_list, other_text_list, tissue_name)
        metabolic_element_dict = set_and_convert_network_elements(
            metabolite_list, reaction_list, subnetwork_list, other_text_list,
            input_metabolite_set=input_metabolite_set, c13_labeling_metabolite_set=c13_labeling_metabolite_set,
            mid_data_metabolite_set=mid_data_metabolite_set,
            mixed_mid_data_metabolite_set=mixed_mid_data_metabolite_set,
            biomass_metabolite_set=biomass_metabolite_set, boundary_flux_set=boundary_flux_set,
            hidden_metabolite_set=hidden_metabolite_set, hidden_reaction_set=hidden_reaction_set,
            metabolite_data_sensitivity_state_dict=metabolite_data_sensitivity_state_dict,
            reaction_data_sensitivity_state_dict=reaction_data_sensitivity_state_dict,
            display_flux_name=display_flux_name, reaction_text_dict=reaction_text_dict,
            reaction_text_config_dict=reaction_text_config_dict,
            reaction_raw_value_dict=reaction_raw_value_dict, flux_value_mapper=flux_value_mapper,
            extra_parameter_dict=extra_parameter_dict)

        if bottom_left_offset is None:
            bottom_left_offset = Vector(0, 0)
        super().__init__(
            metabolic_element_dict, bottom_left_offset, Vector(scale, scale * self.height_to_width_ratio),
            scale=scale, bottom_left_offset=bottom_left_offset,
            base_z_order=base_z_order, z_order_increment=z_order_increment, **kwargs)
