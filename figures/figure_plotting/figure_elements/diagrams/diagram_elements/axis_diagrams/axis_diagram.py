from ..config import Vector, ParameterName, ZOrderConfig, ColorConfig, TextConfig, \
    JoinStyle, VerticalAlignment, HorizontalAlignment, CommonElementConfig
from ..config import CompositeFigure, Rectangle, TextBox, Line


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
    # tick_config = {
    #     **common_edge_config,
    #     ParameterName.z_order: bound_box_z_order,
    #     ParameterName.edge_color: ColorConfig.normal_blue
    # }
    # text_config = {
    #     ParameterName.font: TextConfig.main_text_font,
    #     ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    #     ParameterName.horizontal_alignment: HorizontalAlignment.center,
    #     ParameterName.z_order: text_order,
    # }
    text_config = CommonElementConfig.common_text_config
    edge_config = {
        ParameterName.join_style: JoinStyle.miter,
        ParameterName.face_color: None,
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
        mid_diagram_dict = {
            ParameterName.bound_box: {'bound_box': bound_box, 'bound_box_background': bound_box_background},
            ParameterName.axis_content: {
                axis_content_obj.name: axis_content_obj for axis_content_obj in axis_content_obj_list},
            ParameterName.dash: {dash_obj.name: dash_obj for dash_obj in line_list},
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_list},
        }
        super().__init__(
            mid_diagram_dict, bottom_left=bound_box.bottom_left, size=bound_box.size, **kwargs)

    def box_transform(self, raw_vector=None, raw_x=None, raw_y=None, inplace=True):
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
