from .normal_network_layout_generator import network_layout_generator
from .common_functions import add_straight_reaction_between_metabolites
from ..config import ParameterName, Vector, ReactionConfig

display_text_vertical_distance = ReactionConfig.display_text_vertical_distance
display_text_horizontal_distance = ReactionConfig.display_text_horizontal_distance
display_text_half_height = ReactionConfig.display_text_height / 2
display_text_half_width = ReactionConfig.display_text_width / 2


def single_normal_tissue_layout_generator(
        metabolite_list, reaction_list, subnetwork_list, other_text_list, tissue_name):
    network_layout_generator(metabolite_list, reaction_list, subnetwork_list, other_text_list, infusion=False)
    pep_c_y_value = metabolite_list.obj_pep_c.center.y
    lac_e_x_value = metabolite_list.obj_lac_e.center.x
    pyr_e_obj = metabolite_list.obj_pyr_e

    pyr_e_obj.set_center(Vector(lac_e_x_value, pep_c_y_value))
    above_pyr_display_text_y_value = (
            pep_c_y_value + display_text_vertical_distance + display_text_half_height)
    add_straight_reaction_between_metabolites(
        main_vertical_axis_x_value, left_1_vertical_axis_x_value, ParameterName.horizontal, pyr_c_y_value,
        reaction_list.obj_ldh_c).set_display_text_config_dict({
            ParameterName.center: Vector(
                main_left_display_text_x_value,
                above_pyr_display_text_y_value
            ),
            ParameterName.vertical_alignment: VerticalAlignment.baseline
        })



def serum_layout_generator(metabolite_list, reaction_list, subnetwork_list, other_text_list):
    pass


def multi_tissue_network_layout_generator(
        metabolite_list, reaction_list, subnetwork_list, other_text_list, tissue_name):
    if tissue_name == Keywords.all_tissue:
        pass
    elif tissue_name == Keywords.serum:
        serum_layout_generator(
            metabolite_list, reaction_list, subnetwork_list, other_text_list)
    else:
        single_normal_tissue_layout_generator(
            metabolite_list, reaction_list, subnetwork_list, other_text_list, tissue_name)

