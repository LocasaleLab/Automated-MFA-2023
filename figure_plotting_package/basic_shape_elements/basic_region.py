from .config import ParameterName, Vector, initialize_vector_input


common_multiplied_parameter_set = {
    ParameterName.square_bottom_left_point,
    ParameterName.center,
    ParameterName.edge_width,
    ParameterName.width,
    ParameterName.height,
    ParameterName.font_size,
    ParameterName.head_width,
    ParameterName.stem_width,
    ParameterName.tail,
    ParameterName.head,
    ParameterName.radius,
    ParameterName.tail_end_center,
    ParameterName.bottom_left,
    ParameterName.size,
    ParameterName.start,
    ParameterName.end,
    ParameterName.marker_size
}

common_shift_parameter_set = {
    ParameterName.square_bottom_left_point,
    ParameterName.center,
    ParameterName.tail,
    ParameterName.head,
    ParameterName.bottom_left,
    ParameterName.start,
    ParameterName.end,
}


def move_and_scale_for_dict(
        target_dict, scale=1, multiplied_parameter_set=None,
        bottom_left_offset=None, shift_parameter_set=None):
    for key, value in target_dict.items():
        if scale != 1:
            if multiplied_parameter_set is None:
                multiplied_parameter_set = common_multiplied_parameter_set
            if key in multiplied_parameter_set and value is not None:
                target_dict[key] = scale * target_dict[key]
        if bottom_left_offset is not None:
            if shift_parameter_set is None:
                shift_parameter_set = common_shift_parameter_set
            if key in shift_parameter_set and value is not None:
                if not isinstance(value, Vector):
                    raise ValueError()
                target_dict[key] = bottom_left_offset + target_dict[key]


def iterative_move_and_scale_for_dict(
        target_obj, key=None, scale=1, multiplied_parameter_set=None,
        bottom_left_offset=None, shift_parameter_set=None):
    if isinstance(target_obj, dict):
        for key, value in target_obj.items():
            modified, new_value = iterative_move_and_scale_for_dict(
                value, key=key, scale=scale, multiplied_parameter_set=multiplied_parameter_set,
                bottom_left_offset=bottom_left_offset, shift_parameter_set=shift_parameter_set)
            if modified:
                target_obj[key] = new_value
    elif isinstance(target_obj, (tuple, list)):
        for new_target_value in target_obj:
            iterative_move_and_scale_for_dict(
                new_target_value, scale=scale, multiplied_parameter_set=multiplied_parameter_set,
                bottom_left_offset=bottom_left_offset, shift_parameter_set=shift_parameter_set)
    elif key is not None and isinstance(target_obj, (int, float, Vector)):
        modified = False
        new_value = None
        if scale != 1 and key in multiplied_parameter_set and target_obj is not None:
            modified = True
            new_value = target_obj * scale
        if bottom_left_offset is not None and key in shift_parameter_set and target_obj is not None:
            modified = True
            if not isinstance(target_obj, Vector):
                raise ValueError()
            new_value = target_obj + bottom_left_offset
        return modified, new_value
    return False, None


class Region(object):
    count = 0

    def __init__(self, bottom_left: Vector, size: Vector, name=None, **kwargs):
        Region.count += 1
        if name is None:
            name = self.__class__.__name__
        self.name = f'{name}_{self.count}'
        self.bottom_left = initialize_vector_input(bottom_left)
        self.size = initialize_vector_input(size)
        self.top_right = self.bottom_left + self.size

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        # for attr_name, attr_value in self.__dict__.items():
        #     if scale != 1 and attr_name in multiplied_parameter_set and attr_value is not None:
        #         self.__setattr__(attr_name, scale * self.__getattribute__(attr_name))
        #     if bottom_left_offset is not None and attr_name in shift_parameter_set and attr_value is not None:
        #         if not isinstance(attr_value, Vector):
        #             raise ValueError()
        #         self.__setattr__(attr_name, bottom_left_offset + self.__getattribute__(attr_name))
        move_and_scale_for_dict(
            self.__dict__,
            scale=scale, multiplied_parameter_set=common_multiplied_parameter_set,
            bottom_left_offset=bottom_left_offset, shift_parameter_set=common_shift_parameter_set)
        if base_z_order != 0 or z_order_increment != 1:
            z_order_name = ParameterName.z_order
            if z_order_name in self.__dict__:
                current_z_order = self.__getattribute__(z_order_name)
                self.__setattr__(z_order_name, z_order_increment * current_z_order + base_z_order)

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        pass
