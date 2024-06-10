from ..config import Vector, extract_display_name
from ..metabolic_network_elements.metabolite_element import MetaboliteElement


class Metabolite(object):
    def __init__(self, metabolite_name: str, center: Vector = None, display_metabolite_name=None, **kwargs):
        self.metabolite_name = metabolite_name
        self.center = center
        self.extra_parameter_dict = kwargs
        if display_metabolite_name is None:
            display_metabolite_name = extract_display_name(metabolite_name)
        self.display_metabolite_name = display_metabolite_name
        self.as_input_metabolite = False
        self.as_c13_labeling_metabolite = False
        self.with_mid_data = False
        self.with_mixed_mid_data = False
        self.with_biomass_flux = False
        self.invalid_state = False
        self.other_color_state = None
        self._initialize_tags()

    def _initialize_tags(self):
        self.as_input_metabolite = False
        self.as_c13_labeling_metabolite = False
        self.with_mid_data = False
        self.with_mixed_mid_data = False
        self.with_biomass_flux = False
        self.other_color_state = None

    def reset(self):
        self.center = None
        self._initialize_tags()

    def set_display_name(self, new_display_name: str):
        self.display_metabolite_name = new_display_name
        return self

    def set_center(self, new_center: Vector):
        self.center = new_center
        return self

    def set_input_state(self, as_input_metabolite: bool):
        self.as_input_metabolite = as_input_metabolite
        return self

    def set_c13_labeling_state(self, c13_labeling_state: bool):
        self.as_c13_labeling_metabolite = c13_labeling_state
        return self

    def set_mid_data_state(self, with_mid_data: bool):
        self.with_mid_data = with_mid_data
        return self

    def set_mixed_mid_data_state(self, with_mixed_mid_data: bool):
        self.with_mixed_mid_data = with_mixed_mid_data
        return self

    def set_biomass_flux_state(self, with_biomass_flux: bool):
        self.with_biomass_flux = with_biomass_flux
        return self

    def set_invalid_state(self, invalid_state: bool):
        self.invalid_state = invalid_state
        return self

    def set_data_sensitivity_state(self, other_color_state):
        self.other_color_state = other_color_state
        return self

    def set_other_color_state(self, other_color_state):
        self.other_color_state = other_color_state
        return self

    def update_extra_parameter_dict(self, new_extra_parameter_dict):
        self.extra_parameter_dict.update(new_extra_parameter_dict)
        return self

    def to_element(self, scale=1, bottom_left_offset=None):
        return MetaboliteElement(
            self.center, self.metabolite_name, self.display_metabolite_name,
            self.as_input_metabolite, self.as_c13_labeling_metabolite,
            self.with_mid_data, self.with_mixed_mid_data, self.with_biomass_flux,
            self.invalid_state, self.other_color_state,
            scale=scale, bottom_left_offset=bottom_left_offset, **self.extra_parameter_dict)
