from .config import Vector, ParameterName, ZOrderConfig, ColorConfig, JoinStyle
from ..common.common_figure_materials import CommonElementConfig
from .config import CompositeFigure, Rectangle, TextBox, Line, Arrow


def bidirectional_arrow_config_constructor(tail_location, head_location, dots_radius):
    vector1 = head_location - tail_location
    offset_vector = dots_radius / vector1.length * vector1
    updated_tail_location = tail_location + offset_vector
    updated_head_location = head_location - offset_vector
    return updated_tail_location, updated_head_location


class AxisDiagramConfig(object):
    bound_box_z_order = ZOrderConfig.default_axis_z_order + ZOrderConfig.z_order_increment
    content_z_order = ZOrderConfig.default_patch_z_order
    dash_line_z_order = content_z_order - ZOrderConfig.z_order_increment
    label_order = content_z_order + ZOrderConfig.z_order_increment
    order_increment = ZOrderConfig.z_order_increment
    bound_box_background_order = ZOrderConfig.default_image_z_order
    text_order = ZOrderConfig.default_text_z_order

    bound_box_background_config = {
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.white_color,
        ParameterName.z_order: bound_box_background_order,
    }
    tick_len = 0.01
    text_config = CommonElementConfig.common_text_config
    edge_config = {
        ParameterName.join_style: JoinStyle.miter,
        ParameterName.face_color: None,
    }

    cross_axis_arrow_config = {
        **edge_config,
        ParameterName.z_order: content_z_order,
        ParameterName.head_len_width_ratio: 1.2,
        ParameterName.tail_arrow: False,
        ParameterName.head_arrow: True,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.normal_blue,
        ParameterName.stem_width: 0.007,
        ParameterName.head_width: 0.021,
    }


class AxisDiagram(CompositeFigure):
    box_size = Vector(0.8, 0.6)
    box_bottom_left = Vector(1, 1) - box_size
    height_to_width_ratio = box_size.y / box_size.x

    def __init__(
            self, config_class, axis_content_obj_list, x_tick_list=(), y_tick_list=(), line_config_list=(),
            text_config_list=(), **kwargs):
        box_bottom_left = self.box_bottom_left
        box_size = self.box_size
        box_param_dict = {
            ParameterName.center: box_bottom_left + box_size / 2,
            ParameterName.width: box_size.x,
            ParameterName.height: box_size.y,
        }
        bound_box = Rectangle(**{**box_param_dict, **config_class.bound_box_config})
        bound_box_background = Rectangle(**{**box_param_dict, **config_class.bound_box_background_config})

        line_list = []
        tick_len = config_class.tick_len
        for x_tick_x_loc in x_tick_list:
            line_list.append(Line(**{
                **config_class.bound_box_config,
                ParameterName.start: Vector(x_tick_x_loc, box_bottom_left.y),
                ParameterName.end: Vector(x_tick_x_loc, box_bottom_left.y - tick_len)
            }))
        for y_tick_y_loc in y_tick_list:
            line_list.append(Line(**{
                **config_class.bound_box_config,
                ParameterName.start: Vector(box_bottom_left.x, y_tick_y_loc),
                ParameterName.end: Vector(box_bottom_left.x - tick_len, y_tick_y_loc)
            }))
        for line_config in line_config_list:
            line_list.append(Line(**line_config))

        text_list = []
        for text_config in text_config_list:
            complete_text_config = {
                **AxisDiagramConfig.text_config,
                **text_config
            }
            text_list.append(TextBox(**complete_text_config))
        axis_obj_dict = {
            ParameterName.bound_box: {'bound_box': bound_box, 'bound_box_background': bound_box_background},
            ParameterName.axis_content: {
                axis_content_obj.name: axis_content_obj for axis_content_obj in axis_content_obj_list},
            ParameterName.dash: {dash_obj.name: dash_obj for dash_obj in line_list},
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_list},
        }
        super().__init__(
            axis_obj_dict, bottom_left=bound_box.bottom_left, size=bound_box.size, **kwargs)

    def box_transform(self, raw_vector=None, raw_x=None, raw_y=None, inplace=True):
        """
        raw_vector, raw_x, raw_y: 0: bottom/left, 1: top/right
        """
        if raw_vector is not None:
            if inplace:
                raw_vector *= self.box_size.x
                raw_vector += self.box_bottom_left
                new_vector = raw_vector
            else:
                new_vector = raw_vector * self.box_size.x
                new_vector += self.box_bottom_left
            return new_vector
        elif raw_x is not None:
            return raw_x * self.box_size.x + self.box_bottom_left.x
        elif raw_y is not None:
            return raw_y * self.box_size.x + self.box_bottom_left.y
        else:
            raise ValueError()

    def transform_single_point(self, single_point, vertex_scale_vector, minimum_value):
        new_point = self.box_transform(
            single_point * vertex_scale_vector + Vector(0, minimum_value))
        return new_point

    def transform_path_list(self, function_path_list, vertex_scale_vector, minimum_value):
        new_path_step_list = []
        for path_step in function_path_list:
            copied_path_step = path_step.copy()
            for vertex_index, path_vertex in enumerate(copied_path_step.vertex_list):
                copied_path_step.vertex_list[vertex_index] = self.box_transform(
                    path_vertex * vertex_scale_vector + Vector(0, minimum_value), inplace=False)
            new_path_step_list.append(copied_path_step)
        return new_path_step_list


class CrossAxisDiagram(CompositeFigure):
    box_size = Vector(0.8, 0.6)
    box_bottom_left = Vector(1, 1) - box_size
    height_to_width_ratio = box_size.y / box_size.x
    center = box_bottom_left + box_size / 2

    def __init__(
            self, config_class, axis_content_obj_list, x_tick_list=(), y_tick_list=(), line_config_list=(),
            text_config_list=(), **kwargs):
        box_bottom_left = self.box_bottom_left
        box_size = self.box_size
        width, height = box_size
        self.total_width = width
        self.total_height = height
        self.height_to_width_ratio = height / width

        axis_param_dict = {
            **config_class.cross_axis_arrow_config
        }
        y_tail = box_bottom_left + Vector(width / 2, 0)
        y_head = box_bottom_left + Vector(width / 2, height)
        x_tail = box_bottom_left + Vector(0, height / 2)
        x_head = box_bottom_left + Vector(width, height / 2)
        x_axis_arrow_param_dict = {
            **axis_param_dict,
            ParameterName.tail: x_tail,
            ParameterName.head: x_head,
        }
        y_axis_arrow_param_dict = {
            **axis_param_dict,
            ParameterName.tail: y_tail,
            ParameterName.head: y_head,
        }
        cross_axis_dict = {'x': Arrow(**x_axis_arrow_param_dict), 'y': Arrow(**y_axis_arrow_param_dict)}
        # bound_box_background = Rectangle(**{**box_param_dict, **config_class.bound_box_background_config})

        line_list = []
        tick_len = config_class.tick_len
        for x_tick_x_loc in x_tick_list:
            line_list.append(Line(**{
                **config_class.bound_box_config,
                ParameterName.start: Vector(x_tick_x_loc, box_bottom_left.y),
                ParameterName.end: Vector(x_tick_x_loc, box_bottom_left.y - tick_len)
            }))
        for y_tick_y_loc in y_tick_list:
            line_list.append(Line(**{
                **config_class.bound_box_config,
                ParameterName.start: Vector(box_bottom_left.x, y_tick_y_loc),
                ParameterName.end: Vector(box_bottom_left.x - tick_len, y_tick_y_loc)
            }))
        for line_config in line_config_list:
            line_list.append(Line(**line_config))

        text_list = []
        for text_config in text_config_list:
            complete_text_config = {
                **AxisDiagramConfig.text_config,
                **text_config
            }
            text_list.append(TextBox(**complete_text_config))
        axis_obj_dict = {
            ParameterName.cross_axis: cross_axis_dict,
            ParameterName.axis_content: {
                axis_content_obj.name: axis_content_obj for axis_content_obj in axis_content_obj_list},
            ParameterName.dash: {dash_obj.name: dash_obj for dash_obj in line_list},
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_list},
        }

        total_size = Vector(self.total_width, self.height_to_width_ratio * self.total_width)
        super().__init__(
            axis_obj_dict, bottom_left=self.box_bottom_left, size=self.box_size, **kwargs)

    def box_transform(self, raw_vector=None, raw_x=None, raw_y=None, inplace=True):
        """
        raw_vector, raw_x, raw_y: -0.5: bottom/left, 0.5: top/right
        """
        if raw_vector is not None:
            if inplace:
                raw_vector *= self.box_size.x
                raw_vector += self.center
                new_vector = raw_vector
            else:
                new_vector = raw_vector * self.box_size.x
                new_vector += self.center
            return new_vector
        elif raw_x is not None:
            return raw_x * self.box_size.x + self.center.x
        elif raw_y is not None:
            return raw_y * self.box_size.x + self.center.y
        else:
            raise ValueError()
