from .config import it, np, Vector, VerticalAlignment, HorizontalAlignment, ParameterName, \
    ColorConfig, ZOrderConfig, TextConfig, initialize_vector_input, default_parameter_extract

from .composite_figure_and_axes import CompositeFigure
from .modified_text import TextBox
from .shapes import Rectangle, Circle


class LegendConfig(object):
    basic_z_order = ZOrderConfig.default_legend_z_order
    patch_z_order = basic_z_order + ZOrderConfig.z_order_increment
    text_z_order = basic_z_order + 2 * ZOrderConfig.z_order_increment

    legend_horiz_edge_ratio = 0.6
    legend_col_horiz_edge_ratio = 0.2
    legend_verti_edge_ratio = 0.05
    # legend_verti_edge_ratio = 0.02
    legend_row_verti_edge_ratio = 0.3
    patch_height_to_width_ratio = 0.6
    # patch_height_shrink = 0.5
    patch_height_shrink = 0.7
    patch_text_distance_ratio = 0.1
    # text_font_size_ratio = 50
    text_font_size_ratio = 60

    patch_config_dict = {
        ParameterName.edge_width: None,
        ParameterName.z_order: patch_z_order,
    }

    text_config_dict = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.vertical_alignment: VerticalAlignment.center,
        ParameterName.z_order: text_z_order,
    }

    background_rectangle_config_dict = {
        ParameterName.edge_width: None,
        ParameterName.color: ColorConfig.white_color,
        ParameterName.z_order: basic_z_order,
    }


def shape_constructor(raw_shape, patch_width, patch_height, common_config_dict, color_dict):
    def single_shape_constructor(single_shape):
        if single_shape == ParameterName.rectangle:
            new_config_dict = {
                **common_config_dict,
                ParameterName.width: patch_width,
                ParameterName.height: patch_height,
            }
            obj_class = Rectangle
        elif single_shape == ParameterName.circle:
            new_config_dict = {
                **common_config_dict,
                ParameterName.radius: patch_height,
            }
            obj_class = Circle
        else:
            raise ValueError()
        return new_config_dict, obj_class

    if isinstance(raw_shape, (list, tuple, dict)):
        assert len(raw_shape) == len(color_dict)
        config_dict_list = []
        obj_list = []
        if isinstance(raw_shape, dict):
            raw_shape_iter = [raw_shape[key] for key in color_dict.keys()]
        else:
            raw_shape_iter = raw_shape
        for current_single_shape in raw_shape_iter:
            current_config_dict, current_obj_class = single_shape_constructor(current_single_shape)
            config_dict_list.append(current_config_dict)
            obj_list.append(current_obj_class)
        return config_dict_list, obj_list
    elif isinstance(raw_shape, str):
        current_config_dict, current_obj_class = single_shape_constructor(raw_shape)
        return it.repeat(current_config_dict), it.repeat(current_obj_class)
    else:
        raise ValueError()


class PatchLegend(CompositeFigure):
    def __init__(
            self, center: Vector, width: float, height: float, color_dict, name_dict,
            horiz_or_vertical=ParameterName.horizontal, shape=ParameterName.rectangle, config_dict=None,
            row_num=None, col_num=None, **kwargs):
        assert width > 0 and height > 0
        legend_num = len(color_dict)
        assert len(name_dict) == legend_num
        center = initialize_vector_input(center)
        size = Vector(width, height)
        bottom_left = center - size / 2
        if row_num is None and col_num is None:
            if horiz_or_vertical == ParameterName.horizontal:
                if legend_num <= 3:
                    row_num = 1
                    col_num = legend_num
                elif legend_num % 3 == 0:
                    col_num = 3
                    row_num = legend_num / col_num
                else:
                    col_num = 2
                    row_num = int(legend_num / col_num + 0.99999)
            else:
                col_num = 1
                row_num = legend_num
        elif row_num is not None:
            if col_num is None:
                col_num = int(legend_num / row_num + 0.99999)
            else:
                assert row_num * col_num == legend_num
        else:
            row_num = int(legend_num / col_num + 0.99999)
        location_config_dict = default_parameter_extract(config_dict, ParameterName.location_config_dict, {})
        total_horiz_edge_ratio = default_parameter_extract(
            location_config_dict, ParameterName.total_horiz_edge_ratio, LegendConfig.legend_horiz_edge_ratio)
        col_horiz_edge_ratio = default_parameter_extract(
            location_config_dict, ParameterName.col_horiz_edge_ratio, LegendConfig.legend_col_horiz_edge_ratio)
        total_verti_edge_ratio = default_parameter_extract(
            location_config_dict, ParameterName.total_verti_edge_ratio, LegendConfig.legend_verti_edge_ratio)
        row_verti_edge_ratio = default_parameter_extract(
            location_config_dict, ParameterName.row_verti_edge_ratio, LegendConfig.legend_row_verti_edge_ratio)
        real_col_size = width / (col_num * (1 + 2 * col_horiz_edge_ratio) + 2 * total_horiz_edge_ratio)
        col_size_with_margin = real_col_size * (1 + 2 * col_horiz_edge_ratio)
        left_right_margin = real_col_size * total_horiz_edge_ratio
        each_col_margin = real_col_size * col_horiz_edge_ratio
        real_row_size = height / (row_num * (1 + 2 * row_verti_edge_ratio) + 2 * total_verti_edge_ratio)
        row_size_with_margin = real_row_size * (1 + 2 * row_verti_edge_ratio)
        top_bottom_margin = real_row_size * total_verti_edge_ratio
        patch_height = real_row_size * LegendConfig.patch_height_shrink
        patch_width = patch_height / LegendConfig.patch_height_to_width_ratio
        patch_text_distance = real_col_size * LegendConfig.patch_text_distance_ratio
        text_font_size = real_col_size * LegendConfig.text_font_size_ratio
        text_width = real_col_size - patch_width - patch_text_distance

        if ParameterName.text_config_dict in config_dict:
            text_config_dict = config_dict[ParameterName.text_config_dict]
            if text_config_dict is None:
                text_config_dict = {}
        else:
            text_config_dict = {}
        if ParameterName.legend_patch_config_dict in config_dict:
            legend_patch_config_dict = config_dict[ParameterName.legend_patch_config_dict]
            if legend_patch_config_dict is None:
                legend_patch_config_dict = {}
        else:
            legend_patch_config_dict = {}
        if ParameterName.alpha in config_dict:
            alpha = config_dict[ParameterName.alpha]
        else:
            alpha = None
        common_patch_config_dict = {
            **LegendConfig.patch_config_dict,
            **legend_patch_config_dict,
        }
        # if shape == ParameterName.rectangle:
        #     common_patch_config_dict.update({
        #         ParameterName.width: patch_width,
        #         ParameterName.height: patch_height,
        #     })
        #     patch_obj_class = Rectangle
        # elif shape == ParameterName.circle:
        #     common_patch_config_dict.update({
        #         ParameterName.radius: patch_height,
        #     })
        #     patch_obj_class = Circle
        # else:
        #     raise ValueError()
        config_dict_list, obj_func_list = shape_constructor(
            shape, patch_width, patch_height, common_patch_config_dict, color_dict)
        patch_config_dict_list = []
        text_config_dict_list = []
        patch_obj_list = []
        for (total_index, (type_label, type_color)), current_config_dict, current_obj_func in zip(
                enumerate(color_dict.items()), config_dict_list, obj_func_list):
            type_name_text = name_dict[type_label]
            row_index = int(total_index / col_num)
            col_index = total_index % col_num
            this_item_center_y = center.y + height / 2 - top_bottom_margin - ((row_index + 0.5) * row_size_with_margin)
            if total_index == legend_num - 1 and col_index == 0:
                this_item_left_x = center.x - col_size_with_margin / 2
            else:
                this_item_left_x = bottom_left.x + left_right_margin + (col_index * col_size_with_margin)
            patch_left_x = this_item_left_x + each_col_margin
            patch_center_x = patch_left_x + patch_width / 2
            text_center_x = patch_left_x + patch_width + patch_text_distance + text_width / 2
            if alpha is not None and not type_color.alpha_set:
                current_type_color = type_color.add_transparency(alpha)
            else:
                current_type_color = type_color
            current_patch_config_dict = {
                **current_config_dict,
                ParameterName.center: Vector(patch_center_x, this_item_center_y),
                # ParameterName.width: patch_width,
                # ParameterName.height: patch_height,
                ParameterName.face_color: current_type_color,
                # **LegendConfig.patch_config_dict,
                # **legend_patch_config_dict
            }
            current_text_config_dict = {
                ParameterName.string: type_name_text,
                ParameterName.center: Vector(text_center_x, this_item_center_y),
                ParameterName.font_size: text_font_size,
                ParameterName.width: text_width,
                ParameterName.height: real_row_size,
                **LegendConfig.text_config_dict,
                **text_config_dict,
            }
            # patch_config_dict_list.append(current_patch_config_dict)
            text_config_dict_list.append(current_text_config_dict)
            patch_obj_list.append(current_obj_func(**current_patch_config_dict))

        # patch_obj_list = [patch_obj_class(**patch_config_dict) for patch_config_dict in patch_config_dict_list]
        text_obj_list = [TextBox(**text_config_dict) for text_config_dict in text_config_dict_list]

        # background_rectangle = Rectangle(
        #     **{
        #         **LegendConfig.background_rectangle_config_dict,
        #         ParameterName.center: center,
        #         ParameterName.width: width,
        #         ParameterName.height: height,
        #     }
        # )
        legend_dict = {
            ParameterName.patch: {patch_obj.name: patch_obj for patch_obj in patch_obj_list},
            ParameterName.text: {text_obj.name: text_obj for text_obj in text_obj_list},
            # ParameterName.background: {
            #     background_rectangle.name: background_rectangle
            # }
        }
        super().__init__(
            legend_dict, bottom_left, size,
            # scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            # z_order_increment=z_order_increment,
            **kwargs)

    def _rescale_to_maximize_and_recenter(self, parent_ax):
        figure_box = parent_ax.figure.bbox
        figure_height_to_width_ratio = figure_box.height / figure_box.width
        *_, width, height = parent_ax.get_position().bounds
        parent_axis_size = Vector(width, height * figure_height_to_width_ratio)
        rescale_ratio = np.min(parent_axis_size / self.size)
        target_center = 0.5 * parent_axis_size
        new_center = 0.5 * self.size * rescale_ratio
        self.move_and_scale(scale=rescale_ratio, bottom_left_offset=target_center - new_center)
        pass

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        # self._rescale_to_maximize_and_recenter(parent_ax)
        super().draw(fig, parent_ax, parent_transformation)


def common_legend_generator(legend_config_dict, color_dict):
    legend_type = default_parameter_extract(legend_config_dict, ParameterName.legend_type, ParameterName.patch_legend)
    horiz_or_vertical = default_parameter_extract(
        legend_config_dict, ParameterName.horiz_or_vertical, ParameterName.horizontal)
    shape = default_parameter_extract(
        legend_config_dict, ParameterName.shape, ParameterName.rectangle)
    alpha = default_parameter_extract(
        legend_config_dict, ParameterName.alpha, ColorConfig.alpha_for_bar_plot)
    row_num, col_num = default_parameter_extract(legend_config_dict, ParameterName.grid_shape, (None, None))
    (
        legend_area_center,
        legend_area_size,
        name_dict,
    ) = [
        legend_config_dict[key]
        for key in [
            ParameterName.legend_center,
            ParameterName.legend_area_size,
            ParameterName.name_dict,
        ]
    ]
    legend_color_dict = default_parameter_extract(legend_config_dict, ParameterName.legend_color_dict, color_dict)
    legend_width, legend_height = legend_area_size
    if legend_type == ParameterName.patch_legend:
        (
            text_config_dict,
            legend_patch_config_dict,
            location_config_dict,
        ) = [
            legend_config_dict[key]
            if key in legend_config_dict else None
            for key in [
                ParameterName.text_config_dict,
                ParameterName.legend_patch_config_dict,
                ParameterName.location_config_dict
            ]
        ]
        effective_legend_config_dict = {
            ParameterName.alpha: alpha,
        }
        if text_config_dict is not None:
            effective_legend_config_dict[ParameterName.text_config_dict] = text_config_dict
        if legend_patch_config_dict is not None:
            effective_legend_config_dict[ParameterName.legend_patch_config_dict] = legend_patch_config_dict
        if location_config_dict is not None:
            effective_legend_config_dict[ParameterName.location_config_dict] = location_config_dict
        legend_obj = PatchLegend(
            legend_area_center, legend_width, legend_height, legend_color_dict, name_dict, shape=shape,
            horiz_or_vertical=horiz_or_vertical, config_dict=effective_legend_config_dict,
            row_num=row_num, col_num=col_num)
    else:
        raise ValueError()
    return legend_obj
