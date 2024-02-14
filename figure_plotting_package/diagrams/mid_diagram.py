from ..common.common_functions import construct_full_name, basic_shape_parameter_set, \
    load_required_parameter, text_parameter_set

from .config import warnings, np, Vector, ParameterName, ZOrderConfig, ColorConfig, JoinStyle, VerticalAlignment, \
    common_text_config_dict
from .config import CompositeFigure, Rectangle, TextBox


class MIDDiagramConfig(object):
    total_height = 1.05
    each_bar_total_width = 0.3
    box_height = 0.9
    text_box_margin = 0.05
    text_height = total_height - box_height - text_box_margin
    bar_width_ratio = 0.55

    bound_box_z_order = ZOrderConfig.default_axis_z_order + ZOrderConfig.z_order_increment
    bar_order = ZOrderConfig.default_patch_z_order
    bound_box_background_order = ZOrderConfig.default_image_z_order
    bound_box_common_config = {
        ParameterName.edge_width: 17,
        ParameterName.face_color: None,
        ParameterName.z_order: bound_box_z_order,
        ParameterName.join_style: JoinStyle.miter
    }
    bound_box_background_config = {
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.white_color,
        ParameterName.z_order: bound_box_background_order,
    }

    blue_box_config = {
        **bound_box_common_config,
        ParameterName.edge_color: ColorConfig.normal_blue
    }
    orange_box_config = {
        **bound_box_common_config,
        ParameterName.edge_color: ColorConfig.orange
    }
    box_config_dict = {
        ParameterName.blue: blue_box_config,
        ParameterName.orange: orange_box_config,
    }

    bar_common_config = {
        ParameterName.edge_width: None,
        ParameterName.z_order: bar_order
    }

    blue_bar_config = {
        **bar_common_config,
        ParameterName.face_color: ColorConfig.medium_blue
    }
    orange_bar_config = {
        **bar_common_config,
        ParameterName.face_color: ColorConfig.light_orange
    }
    gray_bar_config = {
        **bar_common_config,
        ParameterName.face_color: ColorConfig.medium_light_gray
    }
    bar_config_dict = {
        ParameterName.blue: blue_bar_config,
        ParameterName.orange: orange_bar_config,
        ParameterName.gray: gray_bar_config,
    }

    text_config = {
        **common_text_config_dict,
        ParameterName.font_size: 85,
        ParameterName.width: each_bar_total_width,
        ParameterName.height: text_height,
        ParameterName.vertical_alignment: VerticalAlignment.top,
    }


class MIDDiagram(CompositeFigure):
    each_bar_total_width = MIDDiagramConfig.each_bar_total_width
    total_height = MIDDiagramConfig.total_height
    box_height = MIDDiagramConfig.box_height

    def __init__(
            self, data_vector: np.ndarray, color_name=ParameterName.blue,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):

        each_bar_total_width = self.each_bar_total_width
        total_height = self.total_height
        box_height = self.box_height
        box_bottom_y = total_height - box_height
        if not isinstance(data_vector, np.ndarray):
            data_vector = np.array(data_vector)
        self.data_vector = data_vector
        data_vector_len = data_vector.shape[-1]
        dim = len(data_vector.shape)
        width = each_bar_total_width * data_vector_len
        # center = Vector(width / 2, total_height / 2)
        self.data_vector_len = data_vector_len
        self.name = construct_full_name(ParameterName.mid_diagram_suffix, self.count)
        assert np.all(data_vector < 1) and np.all(data_vector > 0)
        if dim == 1:
            assert isinstance(color_name, str)
            bound_box_config = MIDDiagramConfig.box_config_dict[color_name]
            bar_config_list = [MIDDiagramConfig.bar_config_dict[color_name]]
            data_vector = data_vector.reshape([1, -1])
        else:
            assert isinstance(color_name, (tuple, list))
            bound_box_config = MIDDiagramConfig.box_config_dict[color_name[0]]
            bar_config_list = [MIDDiagramConfig.bar_config_dict[each_color_name] for each_color_name in color_name]
        # if color_name == ParameterName.blue:
        #     bound_box_config = MIDDiagramConfig.blue_box_config
        #     bar_config = MIDDiagramConfig.blue_bar_config
        # elif color_name == ParameterName.orange:
        #     bound_box_config = MIDDiagramConfig.orange_box_config
        #     bar_config = MIDDiagramConfig.orange_bar_config
        # else:
        #     raise ValueError()

        box_parameter_set = {
            ParameterName.width,
            ParameterName.height,
        } | basic_shape_parameter_set
        box_param_dict = {
            ParameterName.center: Vector(width / 2, total_height - box_height / 2),
            ParameterName.width: width,
            ParameterName.height: box_height,
        }
        load_required_parameter(box_param_dict, bound_box_config, box_parameter_set)
        kwargs_unused_set1 = load_required_parameter(box_param_dict, kwargs, box_parameter_set)
        # move_and_scale_parameter_dict(box_param_dict, scale, bottom_left_offset)
        bound_box = Rectangle(**box_param_dict)
        bound_box_background = Rectangle(**{**box_param_dict, **MIDDiagramConfig.bound_box_background_config})

        bar_parameter_set = box_parameter_set
        bar_width_ratio = MIDDiagramConfig.bar_width_ratio
        each_bar_width = each_bar_total_width * bar_width_ratio
        base_y_value = box_bottom_y * np.ones(data_vector_len)
        bar_center_x_loc_list = [each_bar_total_width * (i + 0.5) for i in range(data_vector_len)]
        bar_center_y_loc_list = data_vector / 2 + box_bottom_y
        common_bar_param_dict = {
            ParameterName.width: each_bar_width,
        }
        kwargs_unused_set2 = set()
        bar_param_dict_list = []
        for bar_config, each_row_data_vector in zip(bar_config_list, data_vector):
            bar_param_dict = dict(common_bar_param_dict)
            load_required_parameter(bar_param_dict, bar_config, bar_parameter_set)
            bar_center_y_array = each_row_data_vector / 2 + base_y_value
            for bar_center_x, bar_center_y, bar_data in zip(
                    bar_center_x_loc_list, bar_center_y_array, each_row_data_vector):
                bar_param_dict_list.append({
                    **bar_param_dict,
                    ParameterName.center: Vector(bar_center_x, bar_center_y),
                    ParameterName.height: bar_data,
                })
            base_y_value += each_row_data_vector

        # load_required_parameter(common_bar_param_dict, bar_config_list, bar_parameter_set)
        # kwargs_unused_set2 = load_required_parameter(common_bar_param_dict, kwargs, bar_parameter_set)
        # bar_param_dict_list = []
        # for bar_center_x, bar_center_y, bar_data in zip(bar_center_x_loc_list, bar_center_y_loc_list, data_vector):
        #     bar_param_dict = dict(common_bar_param_dict)
        #     bar_param_dict.update({
        #             ParameterName.center: Vector(bar_center_x, bar_center_y),
        #             ParameterName.height: bar_data,
        #         })
        #     bar_param_dict_list.append(bar_param_dict)
        # for bar_param_dict in bar_param_dict_list:
        #     move_and_scale_parameter_dict(bar_param_dict, scale, bottom_left_offset)
        bar_list = [Rectangle(**bar_param_dict) for bar_param_dict in bar_param_dict_list]

        # text_center_y = center.y - size.y / 2 - MIDDiagramConfig.text_y_distance - MIDDiagramConfig.text_height / 2
        text_height = MIDDiagramConfig.text_height
        # text_center_y = box_bottom_y - text_height / 2 - MIDDiagramConfig.text_box_margin
        text_center_y = text_height / 2
        common_text_param_dict = {
            # ParameterName.text_box: True
        }
        load_required_parameter(common_text_param_dict, MIDDiagramConfig.text_config, text_parameter_set)
        kwargs_unused_set3 = load_required_parameter(common_text_param_dict, kwargs, text_parameter_set)
        kwargs_unused_set = kwargs_unused_set1 & kwargs_unused_set2 & kwargs_unused_set3
        if len(kwargs_unused_set) > 0:
            warnings.warn('Unused kwargs exist!: {}'.format(kwargs_unused_set))
        text_param_dict_list = []
        for index, (text_center_x) in enumerate(bar_center_x_loc_list):
            text_param_dict = dict(common_text_param_dict)
            text_param_dict.update({
                    ParameterName.center: Vector(text_center_x, text_center_y),
                    ParameterName.string: f'm+{index}'
                })
            text_param_dict_list.append(text_param_dict)
        # for text_param_dict in text_param_dict_list:
        #     move_and_scale_parameter_dict(text_param_dict, scale, bottom_left_offset)
        text_list = [TextBox(**text_param_dict) for text_param_dict in text_param_dict_list]
        mid_diagram_dict = {
            ParameterName.bound_box: {'bound_box': bound_box, 'bound_box_background': bound_box_background},
            ParameterName.bar: {bar_obj.name: bar_obj for bar_obj in bar_list},
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_list},
        }
        super().__init__(
            mid_diagram_dict, bottom_left=bound_box.bottom_left, size=bound_box.size, name=self.name,
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)

    @staticmethod
    def calculate_center(self, scale, *args):
        bar_num = args[0]
        return Vector(self.each_bar_total_width * bar_num, self.height_to_width_ratio) / 2 * scale
