from ..config import Vector, RoundRectangle, Region, TextBox, ParameterName, \
    SubnetworkConfig, basic_shape_parameter_set, construct_full_name, \
    load_required_parameter, text_parameter_set


class SubnetworkElement(Region):
    def __init__(
            self, subnetwork_name: str, display_subnetwork_name: str, center, width, height, more_top_margin=False,
            scale=1, bottom_left_offset=None, **kwargs):
        self.subnetwork_name = subnetwork_name
        self.display_subnetwork_name = display_subnetwork_name
        rectangle_parameter_set = basic_shape_parameter_set | {ParameterName.radius}
        rectangle_param_dict = {
            ParameterName.name: construct_full_name(subnetwork_name, ParameterName.capsule_suffix),
            ParameterName.center: center,
            ParameterName.width: width,
            ParameterName.height: height,
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: bottom_left_offset
        }
        load_required_parameter(
            rectangle_param_dict, SubnetworkConfig.Rectangle.__dict__, rectangle_parameter_set)
        kwargs_unused_set1 = load_required_parameter(rectangle_param_dict, kwargs, rectangle_parameter_set)

        text_param_dict = {
            ParameterName.name: construct_full_name(subnetwork_name, ParameterName.text_suffix),
            ParameterName.scale: scale,
            ParameterName.bottom_left_offset: bottom_left_offset
        }

        load_required_parameter(text_param_dict, SubnetworkConfig.Text.__dict__, text_parameter_set)
        kwargs_unused_set2 = load_required_parameter(text_param_dict, kwargs, text_parameter_set)
        if more_top_margin:
            text_top_margin = SubnetworkConfig.Text.lower_text_top_margin
        else:
            text_top_margin = SubnetworkConfig.Text.text_top_margin
        text_param_dict[ParameterName.center] = self.calculate_text_center_loc(
            center, width, height, text_param_dict[ParameterName.width], text_param_dict[ParameterName.height],
            text_top_margin=text_top_margin,
            text_left_margin=SubnetworkConfig.Text.text_left_margin)

        # self.rectangle = Rectangle(**rectangle_param_dict)
        self.rectangle = RoundRectangle(**rectangle_param_dict)

        kwargs_unused_set = kwargs_unused_set1 & kwargs_unused_set2
        if len(kwargs_unused_set) > 0:
            print('Unused kwargs exist!: {}'.format(kwargs_unused_set))
        self.text_box = TextBox(self.display_subnetwork_name, **text_param_dict)
        super().__init__(self.rectangle.bottom_left, self.rectangle.size, name=subnetwork_name)

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        for element_obj in [self.rectangle, self.text_box]:
            if element_obj is not None:
                element_obj.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

    @staticmethod
    def calculate_text_center_loc(
            rectangle_center, rectangle_width, rectangle_height, text_width, text_height,
            text_top_margin, text_left_margin):
        rectangle_bottom_left = rectangle_center - Vector(rectangle_width, rectangle_height) / 2
        return rectangle_bottom_left + Vector(0, rectangle_height) + Vector(text_left_margin, -text_top_margin) + \
            Vector(text_width / 2, -text_height / 2)

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        rectangle_obj = self.rectangle.add_to_mpl_axes(parent_ax, parent_transformation)
        text_obj = self.text_box.add_to_mpl_axes(parent_ax, parent_transformation)
        return rectangle_obj, text_obj
