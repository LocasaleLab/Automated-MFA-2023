from ..config import Vector, ElementName, Arrow, Region, TextBox, Capsule, Circle, ParameterName, \
    MetaboliteConfig, MixedMIDCircle, BiomassFluxArrow, basic_shape_parameter_set, construct_full_name, \
    load_required_parameter, text_parameter_set, ColorConfig
from .common_functions import modify_size_of_long_text, complete_arrow_parameter_set_dict


class MetaboliteElement(Region):
    def __init__(
            self, center: Vector, metabolite_name: str, display_metabolite_name: str,
            as_input_metabolite=False, as_c13_labeling_metabolite=False,
            with_mid_data=False, with_mixed_mid_data=False, with_biomass_flux=False,
            invalid_state=False, other_color_state=None,
            scale=1, bottom_left_offset=None, **kwargs):
        self.metabolite_name = metabolite_name
        self.display_metabolite_name = display_metabolite_name
        capsule_parameter_set = {
            ParameterName.width,
            ParameterName.height,
        } | basic_shape_parameter_set
        # if data_sensitivity_state is not None:
        #     capsule_face_color = MetaboliteConfig.data_sensitivity_color_dict[data_sensitivity_state]
        if other_color_state is not None:
            assert ColorConfig.check_if_color(other_color_state)
            capsule_face_color = other_color_state
        elif as_input_metabolite:
            if with_mid_data:
                raise ValueError()
            if as_c13_labeling_metabolite:
                capsule_face_color = MetaboliteConfig.c13_metabolite_face_color
            else:
                capsule_face_color = MetaboliteConfig.input_metabolite_face_color
        elif with_mid_data:
            capsule_face_color = MetaboliteConfig.mid_face_color
        elif invalid_state:
            capsule_face_color = MetaboliteConfig.invalid_face_color
        else:
            capsule_face_color = MetaboliteConfig.normal_face_color
        capsule_param_dict = {
            ParameterName.center: center,
            ParameterName.name: construct_full_name(metabolite_name, ParameterName.capsule_suffix),
            ParameterName.face_color: capsule_face_color,
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: bottom_left_offset
        }
        load_required_parameter(
            capsule_param_dict, MetaboliteConfig.__dict__, capsule_parameter_set)
        kwargs_unused_set1 = load_required_parameter(capsule_param_dict, kwargs, capsule_parameter_set)
        self.capsule = Capsule(**capsule_param_dict)
        super().__init__(self.capsule.bottom_left, self.capsule.size, name=metabolite_name)

        text_param_dict = {
            ParameterName.name: construct_full_name(metabolite_name, ParameterName.text_suffix),
            ParameterName.center: center,
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: bottom_left_offset
        }
        load_required_parameter(text_param_dict, MetaboliteConfig.__dict__, text_parameter_set)
        modify_size_of_long_text(text_param_dict, display_metabolite_name)
        kwargs_unused_set2 = load_required_parameter(text_param_dict, kwargs, text_parameter_set)
        kwargs_unused_set = kwargs_unused_set1 & kwargs_unused_set2
        text_param_dict[ParameterName.z_order] = MetaboliteConfig.text_z_order
        if len(kwargs_unused_set) > 0:
            print('Unused kwargs exist!: {}'.format(kwargs_unused_set))
        self.text_box = TextBox(
            self.display_metabolite_name, **text_param_dict)
        self.mixed_mid_data_marker = None
        self.biomass_flux_marker = None
        if with_mixed_mid_data:
            circle_param_dict = {
                ParameterName.name: construct_full_name(metabolite_name, ParameterName.mixed_mid_circle_suffix),
                ParameterName.center: MixedMIDCircle.center_offset + center,
                ParameterName.scale: scale,
                ParameterName.bottom_left_offset: bottom_left_offset
            }
            circle_param_set = {ParameterName.radius} | basic_shape_parameter_set
            load_required_parameter(circle_param_dict, MixedMIDCircle.__dict__, circle_param_set)
            self.mixed_mid_data_marker = Circle(**circle_param_dict)
        if with_biomass_flux:
            arrow_param_dict = {
                ParameterName.name: construct_full_name(metabolite_name, ParameterName.biomass_flux_suffix),
                ParameterName.tail: BiomassFluxArrow.tail_offset + center,
                ParameterName.head: BiomassFluxArrow.head_offset + center,
                ParameterName.scale: scale,
                ParameterName.bottom_left_offset: bottom_left_offset
            }
            arrow_param_set = complete_arrow_parameter_set_dict[ParameterName.common] | \
                complete_arrow_parameter_set_dict[ElementName.Arrow] | basic_shape_parameter_set
            load_required_parameter(arrow_param_dict, BiomassFluxArrow.__dict__, arrow_param_set)
            self.biomass_flux_marker = Arrow(**arrow_param_dict)

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        for element_obj in [self.capsule, self.text_box, self.mixed_mid_data_marker, self.biomass_flux_marker]:
            if element_obj is not None:
                element_obj.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        shape_obj = self.capsule.add_to_mpl_axes(parent_ax, parent_transformation)
        text_obj = self.text_box.add_to_mpl_axes(parent_ax, parent_transformation)
        if self.mixed_mid_data_marker is not None:
            mixed_mid_data_marker = self.mixed_mid_data_marker.add_to_mpl_axes(parent_ax, parent_transformation)
        else:
            mixed_mid_data_marker = None
        if self.biomass_flux_marker is not None:
            biomass_flux_marker = self.biomass_flux_marker.add_to_mpl_axes(parent_ax, parent_transformation)
        else:
            biomass_flux_marker = None
        return shape_obj, text_obj, mixed_mid_data_marker, biomass_flux_marker
