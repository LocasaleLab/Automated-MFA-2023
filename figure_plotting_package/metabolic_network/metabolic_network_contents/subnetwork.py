from ..config import Vector
from ..metabolic_network_elements.subnetwork_element import SubnetworkElement


class Subnetwork(object):
    def __init__(
            self, subnetwork_name: str, left_right_location=None, bottom_top_location=None,
            color=None, more_top_margin=False, **kwargs):
        self.subnetwork_name = subnetwork_name
        self.display_subnetwork_name = subnetwork_name.capitalize()
        self.left_right_location = left_right_location
        self.bottom_top_location = bottom_top_location
        self.kwargs = kwargs
        self.color = color
        self.more_top_margin = more_top_margin
        self.element = None

    def set_kwargs(self, **kwargs):
        self.kwargs.update(kwargs)

    def set_location(self, left_right_location: Vector = None, bottom_top_location=None):
        if left_right_location is not None:
            self.left_right_location = left_right_location
        if bottom_top_location is not None:
            self.bottom_top_location = bottom_top_location

    def to_element(self, scale=1, bottom_left_offset=None):
        left_right_location = self.left_right_location
        bottom_top_location = self.bottom_top_location
        width = left_right_location[1] - left_right_location[0]
        assert width > 0
        height = bottom_top_location[1] - bottom_top_location[0]
        assert height > 0
        center = Vector(left_right_location.mean(), bottom_top_location.mean())
        return SubnetworkElement(
            self.subnetwork_name, self.display_subnetwork_name, center,
            scale=scale, bottom_left_offset=bottom_left_offset, width=width, height=height, face_color=self.color,
            more_top_margin=self.more_top_margin, **self.kwargs)
