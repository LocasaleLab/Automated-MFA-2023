
from ..config import Region, TextBox, ParameterName, ReactionConfig, basic_shape_parameter_set, \
    construct_full_name, load_required_parameter, calculate_bottom_left_point, calculate_top_right_point
from .common_functions import complete_arrow_parameter_set_dict, arrow_dict


class ReactionEdge(object):
    def __init__(
            self, class_name, reaction_name, index, tail_arrow=False, head_arrow=True, boundary_flux=False,
            scale=1, bottom_left_offset=None, **kwargs):
        arrow_param_dict = {
            ParameterName.name: construct_full_name(
                f'{reaction_name}_{index}', ParameterName.arrow_suffix_dict[class_name]),
            ParameterName.head_arrow: head_arrow,
            ParameterName.tail_arrow: tail_arrow,
            ParameterName.face_color:
                ReactionConfig.boundary_face_color if boundary_flux else ReactionConfig.normal_face_color,
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: bottom_left_offset
        }
        current_parameter_set = complete_arrow_parameter_set_dict[ParameterName.common] | \
            complete_arrow_parameter_set_dict[class_name] | basic_shape_parameter_set
        load_required_parameter(
            arrow_param_dict, ReactionConfig.__dict__, current_parameter_set)
        kwargs_unused_set = load_required_parameter(arrow_param_dict, kwargs, current_parameter_set)
        if len(kwargs_unused_set) > 0:
            print('Unused kwargs exist!: {}'.format(kwargs_unused_set))
        current_class = arrow_dict[class_name]
        self.arrow_obj = current_class(**arrow_param_dict)


class ReactionElement(Region):
    def __init__(
            self, reaction_name: str, display_reaction_name: str, reaction_edge_parameter_list: list,
            display_text_param_nested_dict, scale=1, bottom_left_offset=None, **kwargs):
        reaction_edge_obj_list = []
        bottom_left_corner_list = []
        top_right_corner_list = []
        for index, reaction_edge_parameter_dict in enumerate(reaction_edge_parameter_list):
            current_reaction_edge_obj = ReactionEdge(
                reaction_name=reaction_name, index=index,
                scale=scale, bottom_left_offset=bottom_left_offset, **reaction_edge_parameter_dict)
            reaction_edge_obj_list.append(current_reaction_edge_obj)
            bottom_left_corner_list.append(current_reaction_edge_obj.arrow_obj.bottom_left)
            top_right_corner_list.append(current_reaction_edge_obj.arrow_obj.top_right)
        bottom_left_corner = calculate_bottom_left_point(bottom_left_corner_list)
        top_right_corner = calculate_top_right_point(top_right_corner_list)
        self.reaction_edge_obj_list = reaction_edge_obj_list
        self.reaction_name = reaction_name
        self.display_reaction_name = display_reaction_name
        self.display_text_dict = {}
        for key, display_text_param_dict in display_text_param_nested_dict.items():
            self.display_text_dict[key] = TextBox(
                **display_text_param_dict, scale=scale, bottom_left_offset=bottom_left_offset)
        super().__init__(bottom_left_corner, top_right_corner - bottom_left_corner)

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        for reaction_edge in self.reaction_edge_obj_list:
            reaction_edge.arrow_obj.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        for key, display_text_obj in self.display_text_dict.items():
            display_text_obj.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        reaction_plot_obj_list = []
        display_text_obj_list = []
        for reaction_edge_obj in self.reaction_edge_obj_list:
            reaction_plot_obj_list.append(reaction_edge_obj.arrow_obj.add_to_mpl_axes(parent_ax, parent_transformation))
        for key, display_text_obj in self.display_text_dict.items():
            display_text_obj_list.append(display_text_obj.draw(fig, parent_ax, parent_transformation))
        return reaction_plot_obj_list, display_text_obj_list
