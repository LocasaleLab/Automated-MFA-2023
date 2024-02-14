from .third_party_packages import np, transforms, stats
from .config import Constants
from .classes import Vector
from .config import ParameterName
from .light_weight_functions import default_parameter_extract, round_to_str_with_fixed_point


def construct_full_name(raw_name, suffix):
    return f'{raw_name}_{suffix}'


def cos_sin(angle):
    rad = np.deg2rad(angle)
    return Vector(np.cos(rad), np.sin(rad))


def rotate_matrix_generator(angle):
    rad = np.deg2rad(angle)
    sin = np.sin(rad)
    cos = np.cos(rad)
    return np.array([[cos, -sin], [sin, cos]])


def transform_inplace(raw_vector, multiply=1, add=0):
    raw_vector *= multiply
    raw_vector += add


def calculate_degree_of_vector(target_vector: Vector):
    """
    Return theta between (-180, 180]
    """
    x, y = target_vector
    if x == 0 and y == 0:
        raise ValueError()
    elif x == 0:
        return 90 if y > 0 else -90
    elif y == 0:
        return 0 if x > 0 else 180
    else:
        abs_value = np.rad2deg(np.arctan(y / x))
        if x * y > 0:
            if x < 0:
                abs_value -= 180
        else:
            if x < 0:
                abs_value += 180
        return abs_value


def rotate_corner_offset_around_center(center, corner_offset_matrix, angle):
    if angle == 0:
        return corner_offset_matrix + center
    else:
        rotation_matrix = rotate_matrix_generator(angle)
        new_corner_offset_matrix = (rotation_matrix @ corner_offset_matrix.T).T
        new_point_location_matrix = new_corner_offset_matrix + center
        return new_point_location_matrix


def convert_theta_to_coordinate(theta, center, radius):
    theta_cos_sin = cos_sin(theta)
    return center + radius * theta_cos_sin


def calculate_bottom_left_point(point_list):
    return Vector(array=np.min(point_list, axis=0))


def calculate_top_right_point(point_list):
    return Vector(array=np.max(point_list, axis=0))


def load_required_parameter(target_dict, source_dict, parameter_set):
    unused_key_set = set()
    for key, value in source_dict.items():
        if key in parameter_set:
            target_dict[key] = value
        else:
            unused_key_set.add(key)
    return unused_key_set


def initialize_vector_input(input_obj):
    if isinstance(input_obj, (tuple, list)):
        assert len(input_obj) == 2
        return Vector(*input_obj)
    elif isinstance(input_obj, np.ndarray):
        return Vector(array=input_obj)
    elif isinstance(input_obj, Vector):
        return input_obj
    else:
        raise ValueError()


def clip_angle_to_normal_range(width, height, angle):
    if angle is None:
        angle = 0
    elif angle > 90 or angle < -90:
        angle = np.sign(angle) * abs(angle) - 90
    elif angle > 45 or angle < -45:
        height, width = width, height
        angle = np.sign(angle) * (90 - abs(angle))
    return width, height, angle


def check_enum_obj(input_value, enum_class):
    if isinstance(input_value, enum_class):
        return input_value.value
    elif input_value in enum_class.__dict__:
        return enum_class.__dict__[input_value].value
    else:
        raise ValueError('Not recognized input value: {} in Enum class {}'.format(input_value, enum_class))


def solve_intersect_by_slope_point_line(u1: Vector, p1: Vector, u2: Vector, p2: Vector):
    """
    u1, u2: Vector, unit vector for the line
    p1, p2: Vector, one point on the line
    """
    tmp_u1 = Vector(u1.y, -u1.x)
    tmp_u2 = Vector(u2.y, -u2.x)
    matrix_a = np.array([tmp_u1, tmp_u2])
    vector_b = np.array([tmp_u1 @ p1, tmp_u2 @ p2])
    result_arr = np.linalg.solve(matrix_a, vector_b)
    return Vector(array=result_arr)


def calculate_line_intersect_to_ratio(
        main_vector_start_point: Vector, main_vector_end_point: Vector, intersect_line_vector_list: list):
    """
    Intersect line is defined by (A, B, C), represents A * x + B * y + C = 0
    :return:
    """
    diff = (main_vector_end_point - main_vector_start_point) @ np.array([[0, -1], [1, 0]])
    main_vector_b = np.linalg.det(np.array([main_vector_end_point, main_vector_start_point]))
    coeff_matrix = np.array([diff, [0, 0]])
    c_column = np.array([[main_vector_b], [0]])
    result_list = []
    for intersect_line_vector in intersect_line_vector_list:
        intersect_ab = intersect_line_vector[:2]
        intersect_c = intersect_line_vector[2]
        # start_value = main_vector_start_point @ intersect_ab + intersect_c
        # end_value = main_vector_end_point @ intersect_ab + intersect_c
        # if start_value * end_value > 0:
        #     result = None
        # else:
        coeff_matrix[1, :] = intersect_ab
        coeff_matrix_det = np.linalg.det(coeff_matrix)
        if abs(coeff_matrix_det) < Constants.computation_eps:
            result_list.append(np.nan)
            continue
        c_column[1, 0] = intersect_c
        x_matrix_det = np.linalg.det(np.hstack([-c_column, coeff_matrix[:, 1].reshape([-1, 1])]))
        y_matrix_det = np.linalg.det(np.hstack([coeff_matrix[:, 0].reshape([-1, 1]), -c_column]))
        intersect_location = Vector(x_matrix_det / coeff_matrix_det, y_matrix_det / coeff_matrix_det)
        main_vector_diff = main_vector_end_point - main_vector_start_point
        intersect_diff = intersect_location - main_vector_start_point
        if main_vector_diff[0] != 0:
            result = intersect_diff[0] / main_vector_diff[0]
        else:
            result = intersect_diff[1] / main_vector_diff[1]
        result_list.append(result)
    return result_list


def union_of_segment_on_line(segment_list, distinct=False):
    # start_label: True
    # end_label: False
    # start and end is included, which means (3, 4) union (4, 5) will merge to 3, 5
    if len(segment_list) == 0:
        return []
    if len(segment_list) == 1:
        return segment_list
    if distinct:
        return segment_list
    computation_eps = Constants.computation_eps
    coordinate_state_list = []
    for start_loc, end_loc in segment_list:
        # This is to cover the two vertex
        coordinate_state_list.extend([
            (start_loc - computation_eps, True), (end_loc + computation_eps, False)])
    sorted_coordinate_state_list = sorted(coordinate_state_list)
    union_segment_list = []
    current_start_loc = 0
    current_status_count = 0
    for loc, status in sorted_coordinate_state_list:
        if status:
            if current_status_count == 0:
                current_start_loc = loc
            current_status_count += 1
        else:
            current_status_count -= 1
            if current_status_count == 0:
                union_segment_list.append((current_start_loc + computation_eps, loc - computation_eps))
    return union_segment_list


def calculate_pedal_of_one_point_to_segment_defined_by_two_points(
        segment_vector_1, segment_vector_2, outside_vector):
    segment_x_difference, segment_y_difference = segment_vector_2 - segment_vector_1
    tmp_y_minus_x_array = np.array([segment_y_difference, -segment_x_difference])
    tmp_x_y_array = np.array([segment_x_difference, segment_y_difference])
    a_matrix = np.zeros([2, 2])
    b_vector = np.zeros(2)
    a_matrix[0, :] = tmp_y_minus_x_array
    b_vector[0] = segment_vector_1 @ tmp_y_minus_x_array
    a_matrix[1, :] = tmp_x_y_array
    b_vector[1] = outside_vector @ tmp_x_y_array
    # intersect_point = np.linalg.solve(a_matrix, b_vector)
    intersect_point = Vector(array=np.linalg.solve(a_matrix, b_vector))
    return intersect_point


def calculate_center_radius_angle_of_three_points_on_circle(tail: Vector, mid: Vector, head: Vector):
    mid_tail_diff = mid - tail
    head_tail_diff = head - tail
    mid_tail_right_side = np.sum(mid ** 2 - tail ** 2)
    head_tail_right_side = np.sum(head ** 2 - tail ** 2)
    left_matrix = np.vstack([mid_tail_diff, head_tail_diff]) * 2
    right_vector = [mid_tail_right_side, head_tail_right_side]
    try:
        center = np.linalg.solve(left_matrix, right_vector)
    except np.linalg.LinAlgError:
        center = None
        radius = None
        angle_triple = None
    else:
        center = Vector(array=center)
        radius = np.linalg.norm(tail - center)
        theta_tail = calculate_degree_of_vector(tail - center)
        theta_mid = calculate_degree_of_vector(mid - center)
        theta_head = calculate_degree_of_vector(head - center)
        mid_tail_deg_diff = theta_mid - theta_tail
        head_mid_deg_diff = theta_head - theta_mid
        if mid_tail_deg_diff * head_mid_deg_diff < 0:
            if abs(mid_tail_deg_diff) > 360:
                if theta_tail > 0:
                    theta_tail -= 360
                else:
                    theta_tail += 360
            else:
                if theta_head > 0:
                    theta_head -= 360
                else:
                    theta_head += 360
        angle_triple = (theta_tail, theta_mid, theta_head)
    return center, radius, angle_triple


basic_shape_parameter_set = {
    ParameterName.name,
    ParameterName.edge_width,
    ParameterName.edge_style,
    ParameterName.edge_color,
    ParameterName.face_color,
    ParameterName.alpha,
    ParameterName.z_order,
    ParameterName.join_style,
}

text_parameter_set = {
    ParameterName.name,
    ParameterName.width,
    ParameterName.height,
    ParameterName.font,
    ParameterName.font_size,
    ParameterName.font_color,
    ParameterName.font_weight,
    ParameterName.horizontal_alignment,
    ParameterName.vertical_alignment,
    ParameterName.z_order,
}


def numbered_even_sequence(start, step, num):
    return np.arange(num) * step + start


def symmetrical_lim_tick_generator_with_zero(pos_lim, neg_lim=None, tick_interval=None):
    half_tick = np.arange(0, pos_lim, tick_interval)
    if neg_lim is None:
        neg_lim = pos_lim
        negative_half_tick = -half_tick[:0:-1]
    else:
        negative_half_tick = -np.arange(0, neg_lim, tick_interval)[:0:-1]
    lim = [-neg_lim, pos_lim]
    full_tick = np.concatenate([negative_half_tick, half_tick])
    return lim, full_tick


def t_test_of_two_groups(sample_1, sample_2):
    res = stats.ttest_ind(sample_1, sample_2, equal_var=False)
    return res.pvalue


def calculate_center_bottom_offset(insider_center: Vector, outsider_size: Vector):
    return outsider_size / 2 - insider_center


def unit_decorator(func):
    return func
