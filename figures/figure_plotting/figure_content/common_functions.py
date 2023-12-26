from ..common.classes import Vector


def calculate_subfigure_layout(
        figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio):
    subfigure_label_class_dict = {
        subfigure_class.subfigure_label: subfigure_class
        for subfigure_class in subfigure_class_list
    }
    subfigure_obj_list = []
    total_height = height_to_width_ratio - top_margin_ratio
    total_width = 1 - 2 * side_margin_ratio
    current_top = total_height
    for row_height, row_layout in figure_layout_list:
        current_height = row_height * total_height
        current_bottom = current_top - current_height
        current_left = side_margin_ratio
        for col_width, subfigure_label in row_layout:
            current_width = total_width * col_width
            subfigure_class = subfigure_label_class_dict[subfigure_label]
            subfigure_obj_list.append(subfigure_class(
                subfigure_bottom_left=Vector(current_left, current_bottom),
                subfigure_size=Vector(current_width, current_height)))
            current_left += current_width
        current_top = current_bottom
    return subfigure_obj_list


def single_subfigure_layout(
        center_location, size, subfigure_class, height_to_width_ratio, top_margin_ratio, side_margin_ratio):
    total_height = height_to_width_ratio - top_margin_ratio
    total_width = 1 - 2 * side_margin_ratio
    real_size = size * Vector(total_width, total_height)
    real_bottom_left = center_location * Vector(total_width, - total_height) + \
        Vector(side_margin_ratio, height_to_width_ratio - top_margin_ratio) - real_size / 2
    return subfigure_class(
        subfigure_bottom_left=real_bottom_left, subfigure_size=real_size)

