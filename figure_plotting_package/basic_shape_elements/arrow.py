from .config import np, Vector, Constants, ParameterName
from .config import initialize_vector_input, \
    calculate_line_intersect_to_ratio, union_of_segment_on_line, cos_sin, convert_theta_to_coordinate, \
    calculate_degree_of_vector, calculate_center_radius_angle_of_three_points_on_circle, \
    solve_intersect_by_slope_point_line

from .shapes import PathShape, PathStep, PathOperation, ellipse_arc_obj


class Branch(object):
    def __init__(self, stem_location: float, terminal_location, arrow=True, dash=False):
        """
        stem_ratio_location is tail and terminal_location is head
        :param stem_location: In straight arrow, the location is represented by ratio from tail, while
            in arc it is represented by angle.
        :param terminal_location:
        :param arrow:
        :param dash:
        """
        self.stem_location = stem_location
        self.terminal_location = initialize_vector_input(terminal_location)
        self.arrow = arrow
        self.dash = dash


def transform_arrow_gap_line_and_pair(self, scale, bottom_left_offset):
    def transform_line_triple(raw_line_triple, _scale, _bottom_left_offset):
        new_raw_line_triple = raw_line_triple.copy()
        new_raw_line_triple[2] = new_raw_line_triple[2] * _scale - new_raw_line_triple[:2] @ _bottom_left_offset
        return new_raw_line_triple

    try:
        gap_line_pair_list = self.__getattribute__(ParameterName.gap_line_pair_list)
    except AttributeError:
        pass
    else:
        if gap_line_pair_list is not None:
            new_gap_line_pair_list = []
            for gap_line1, gap_line2 in gap_line_pair_list:
                assert isinstance(gap_line1, np.ndarray) and len(gap_line1) == 3 \
                       and isinstance(gap_line2, np.ndarray) and len(gap_line2) == 3
                new_gap_line1 = transform_line_triple(gap_line1, scale, bottom_left_offset)
                new_gap_line2 = transform_line_triple(gap_line2, scale, bottom_left_offset)
                new_gap_line_pair_list.append((new_gap_line1, new_gap_line2))
            self.__setattr__(ParameterName.gap_line_pair_list, new_gap_line_pair_list)

    try:
        dash_solid_empty_width = self.__getattribute__(ParameterName.dash_solid_empty_width)
    except AttributeError:
        pass
    else:
        if dash_solid_empty_width is not None:
            new_dash_solid_empty_width = (
                dash_solid_empty_width[0] * scale, dash_solid_empty_width[1] * scale
            )
            self.__setattr__(ParameterName.dash_solid_empty_width, new_dash_solid_empty_width)

    try:
        branch_list = self.__getattribute__(ParameterName.branch_list)
    except AttributeError:
        pass
    else:
        if branch_list is not None:
            for branch_obj in branch_list:
                branch_obj.terminal_location = (
                        branch_obj.terminal_location * scale + bottom_left_offset)


class ArrowBase(PathShape):
    def __init__(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment, reset_vertex_array=False)
        path_step_list = self.path_step_generator()
        super().__init__(path_step_list, **kwargs)

    def move_and_scale(
            self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, reset_vertex_array=True):
        if bottom_left_offset is None:
            bottom_left_offset = Vector(0, 0)
        else:
            bottom_left_offset = initialize_vector_input(bottom_left_offset)
        transform_arrow_gap_line_and_pair(self, scale, bottom_left_offset)
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment, reset_vertex_array)


def side_coordinate_pair_generator(mid_point_coordinate, arrow_side_unit_vector, stem_width):
    side_coordinate_1 = mid_point_coordinate + arrow_side_unit_vector * (stem_width / 2)
    side_coordinate_2 = mid_point_coordinate - arrow_side_unit_vector * (stem_width / 2)
    return side_coordinate_1, side_coordinate_2


def arrow_coordinate_generator(stem_end_center_coordinate, arrow_side_unit_vector, head_width, stem_width):
    head_side_outer_coordinate_1, head_side_outer_coordinate_2 = side_coordinate_pair_generator(
        stem_end_center_coordinate, arrow_side_unit_vector, head_width)
    head_side_inner_coordinate_1, head_side_inner_coordinate_2 = side_coordinate_pair_generator(
        stem_end_center_coordinate, arrow_side_unit_vector, stem_width)
    return head_side_outer_coordinate_1, head_side_inner_coordinate_1, \
        head_side_outer_coordinate_2, head_side_inner_coordinate_2


def create_start_end_step(start_point):
    start_step_list = [PathStep(PathOperation.moveto, start_point)]
    end_step_list = [PathStep(PathOperation.lineto, start_point), PathStep(PathOperation.closepoly)]
    return start_step_list, end_step_list


def draw_an_arrow(
        tail_coordinate, head_coordinate, stem_width, head_width, head_len, tail_arrow, head_arrow,
        gap_line_pair_list, dash_solid_empty_width, transition_point_list=None):
    def single_combine_transition_point_with_gap_bound_location(
            _final_bound_coordinate_list, _current_head, _current_tail):
        *_, _current_arrow_side_unit_vector = calculate_necessary_vector(_current_head, _current_tail)
        _current_gap_bound_location_list = analyze_gap_and_dash(
            _current_head, _current_tail,
            gap_line_pair_list, dash_solid_empty_width, stem_width, _current_arrow_side_unit_vector,
            False, False)
        _final_bound_coordinate_list.extend(_current_gap_bound_location_list)

    (
        head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, head_end_center_coordinate,
        tail_end_center_coordinate, arrow_side_unit_vector) = draw_head_and_tail(
        head_width, stem_width, head_len, tail_coordinate, head_coordinate, tail_arrow, head_arrow)
    if transition_point_list is not None:
        # This intersect_coordinate is from head to tail
        intersect_coordinate_list = broken_arrow_transition_coordinate_generator(
            transition_point_list, tail_end_center_coordinate, head_end_center_coordinate, stem_width)
        current_head = head_coordinate
        final_bound_coordinate_list = []
        for current_transition_point, current_intersect_coordinate in zip(
                reversed(transition_point_list), intersect_coordinate_list):
            single_combine_transition_point_with_gap_bound_location(
                final_bound_coordinate_list, current_head, current_transition_point)
            final_bound_coordinate_list.append(current_intersect_coordinate)
            current_head = current_transition_point
        single_combine_transition_point_with_gap_bound_location(
            final_bound_coordinate_list, current_head, tail_coordinate)
        bound_coordinate_list = intersect_coordinate_list
    else:
        gap_bound_location_list = analyze_gap_and_dash(
            head_end_center_coordinate, tail_end_center_coordinate,
            gap_line_pair_list, dash_solid_empty_width, stem_width, arrow_side_unit_vector,
            tail_arrow, head_arrow)
        bound_coordinate_list = gap_bound_location_list

    complete_path_step_list = construct_arrow_path_list(
        head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, bound_coordinate_list)
    return complete_path_step_list


def calculate_necessary_vector(head_coordinate, tail_coordinate):
    arrow_direction_vector = head_coordinate - tail_coordinate
    arrow_direction_len = arrow_direction_vector.length
    arrow_direction_unit_vector = arrow_direction_vector / arrow_direction_len
    arrow_side_unit_vector = arrow_direction_unit_vector.vertical_vector()
    return arrow_direction_vector, arrow_direction_len, arrow_direction_unit_vector, arrow_side_unit_vector


def draw_chevron_head_and_tail(tail_end_center, head, head_len, width, tail_arrow, head_arrow):
    def draw_chevron_path_step_list(arrow_bool, arrow_coordinate, reverse, head_marker):
        if arrow_bool:
            if head_marker:
                arrow_center_coordinate = arrow_coordinate - head_vector
                arrow_peak_coordinate = arrow_coordinate
            else:
                arrow_center_coordinate = arrow_coordinate
                arrow_peak_coordinate = arrow_coordinate + head_vector
        else:
            arrow_center_coordinate = arrow_peak_coordinate = arrow_coordinate
        arrow_side_coordinate_1, arrow_side_coordinate_2 = side_coordinate_pair_generator(
            arrow_center_coordinate, arrow_side_unit_vector, width)
        if arrow_bool:
            arrow_vertex_list = [
                arrow_side_coordinate_2,
                arrow_peak_coordinate,
                arrow_side_coordinate_1,
            ]
        else:
            arrow_vertex_list = [
                arrow_side_coordinate_2,
                arrow_side_coordinate_1,
            ]
        if reverse:
            arrow_vertex_list.reverse()
        arrow_start_point = arrow_vertex_list[0]
        arrow_path_step_list = [PathStep(PathOperation.lineto, vertex) for vertex in arrow_vertex_list[1:]]
        return arrow_start_point, arrow_path_step_list

    (
        arrow_direction_vector, arrow_direction_len, arrow_direction_unit_vector,
        arrow_side_unit_vector) = calculate_necessary_vector(head, tail_end_center)
    head_vector = head_len * arrow_direction_unit_vector

    tail_start_point, tail_path_step_list = draw_chevron_path_step_list(tail_arrow, tail_end_center, True, False)
    head_start_point, head_path_step_list = draw_chevron_path_step_list(head_arrow, head, False, True)
    return head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, arrow_side_unit_vector


def draw_chevron_head_and_tail_old(tail_end_center, head, head_len, width):
    (
        arrow_direction_vector, arrow_direction_len, arrow_direction_unit_vector,
        arrow_side_unit_vector) = calculate_necessary_vector(head, tail_end_center)
    assert head_len < arrow_direction_len
    head_end_center_coordinate = head - head_len * arrow_direction_unit_vector
    tail_inner_coordinate = tail_end_center + head_len * arrow_direction_unit_vector

    head_side_coordinate_1, head_side_coordinate_2 = side_coordinate_pair_generator(
        head_end_center_coordinate, arrow_side_unit_vector, width)
    tail_side_coordinate_1, tail_side_coordinate_2 = side_coordinate_pair_generator(
        tail_end_center, arrow_side_unit_vector, width)

    head_vertex_list = [
        head_side_coordinate_2,
        head,
        head_side_coordinate_1,
    ]
    tail_vertex_list = [
        tail_side_coordinate_1,
        tail_inner_coordinate,
        tail_side_coordinate_2,
    ]
    head_path_step_list = [PathStep(PathOperation.lineto, vertex) for vertex in head_vertex_list[1:]]
    tail_path_step_list = [PathStep(PathOperation.lineto, vertex) for vertex in tail_vertex_list]
    head_start_point = head_side_coordinate_2
    tail_start_point = tail_side_coordinate_1
    return tail_path_step_list, head_path_step_list, head_start_point, tail_start_point


def draw_head_and_tail(
        head_width, stem_width, head_len, tail_coordinate, head_coordinate, tail_arrow, head_arrow):
    def draw_path_step_list(arrow_bool, arrow_coordinate, arrow_end_direction_sign, reverse):
        if arrow_bool:
            arrow_end_center_coordinate = arrow_coordinate - \
                                          arrow_end_direction_sign * arrow_direction_unit_vector * head_len
            (
                arrow_side_outer_coordinate_1, arrow_side_inner_coordinate_1,
                arrow_side_outer_coordinate_2, arrow_side_inner_coordinate_2) = arrow_coordinate_generator(
                arrow_end_center_coordinate, arrow_side_unit_vector, head_width, stem_width)
            arrow_vertex_list = [
                arrow_side_inner_coordinate_2,
                arrow_side_outer_coordinate_2,
                arrow_coordinate,
                arrow_side_outer_coordinate_1,
                arrow_side_inner_coordinate_1,
            ]
        else:
            arrow_end_center_coordinate = arrow_coordinate
            arrow_side_coordinate_1, arrow_side_coordinate_2 = side_coordinate_pair_generator(
                arrow_coordinate, arrow_side_unit_vector, stem_width)
            arrow_vertex_list = [
                arrow_side_coordinate_2,
                arrow_side_coordinate_1,
            ]
        if reverse:
            arrow_vertex_list.reverse()
        arrow_start_point = arrow_vertex_list[0]
        arrow_path_step_list = []
        for vertex in arrow_vertex_list[1:]:
            arrow_path_step_list.append(PathStep(PathOperation.lineto, vertex))
        return arrow_end_center_coordinate, arrow_start_point, arrow_path_step_list

    (
        arrow_direction_vector, arrow_direction_len, arrow_direction_unit_vector,
        arrow_side_unit_vector) = calculate_necessary_vector(head_coordinate, tail_coordinate)
    assert arrow_direction_len > Constants.computation_eps
    if tail_arrow and head_arrow:
        if 2 * head_len > arrow_direction_len:
            head_len = arrow_direction_len / 2
    elif tail_arrow or head_arrow:
        if head_len > arrow_direction_len:
            head_len = arrow_direction_len

    head_end_center_coordinate, head_start_point, head_path_step_list = draw_path_step_list(
        head_arrow, head_coordinate, 1, False)
    tail_end_center_coordinate, tail_start_point, tail_path_step_list = draw_path_step_list(
        tail_arrow, tail_coordinate, -1, True)

    return head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, \
        head_end_center_coordinate, tail_end_center_coordinate, arrow_side_unit_vector


def analyze_gap_and_dash(
        head_end_center_coordinate: Vector, tail_end_center_coordinate: Vector,
        gap_line_pair_list, dash_solid_empty_width, stem_width, arrow_side_unit_vector,
        tail_arrow, head_arrow):
    # Start from tail to head by ratio of total length
    raw_gap_ratio_range_list = []
    distinct = True
    if gap_line_pair_list is not None:
        for gap_line_pair in gap_line_pair_list:
            gap_start_ratio, gap_end_ratio = calculate_line_intersect_to_ratio(
                tail_end_center_coordinate, head_end_center_coordinate, gap_line_pair)
            if gap_start_ratio > gap_end_ratio:
                gap_start_ratio, gap_end_ratio = gap_end_ratio, gap_start_ratio
            if gap_start_ratio is np.nan or gap_end_ratio is np.nan:
                continue
            if gap_start_ratio < 0:
                if gap_end_ratio < 0:
                    continue
                gap_start_ratio = 0
            if gap_end_ratio > 1:
                if gap_start_ratio > 1:
                    continue
                gap_end_ratio = 1
            raw_gap_ratio_range_list.append((gap_start_ratio, gap_end_ratio))
            distinct = False
    if dash_solid_empty_width is not None:
        each_cycle_len = dash_solid_empty_width[0] + dash_solid_empty_width[1]
        solid_len, gap_len = dash_solid_empty_width
        stem_length = (head_end_center_coordinate - tail_end_center_coordinate).length
        cycle_num = int(stem_length / each_cycle_len)
        solid_len_ratio = solid_len / stem_length
        each_cycle_ratio = each_cycle_len / stem_length
        rest_len = stem_length - cycle_num * each_cycle_len
        if rest_len <= solid_len:
            start_loc = (rest_len - solid_len) / 2
        elif rest_len + solid_len > each_cycle_len:
            start_loc = (rest_len - each_cycle_len - solid_len) / 2
        else:
            start_loc = 0
        start_loc_ratio = start_loc / stem_length
        # To cover all situation in rest cycle
        for i in range(cycle_num + 1):
            start = i * each_cycle_ratio + solid_len_ratio + start_loc_ratio
            end = (i + 1) * each_cycle_ratio + start_loc_ratio
            raw_gap_ratio_range_list.append((start, end))
    # This list is from tail to head
    gap_ratio_range_list = union_of_segment_on_line(raw_gap_ratio_range_list, distinct)

    # This list is from head to tail
    gap_bound_location_list = []
    arrow_vector = head_end_center_coordinate - tail_end_center_coordinate
    for gap_end_ratio, gap_start_ratio in reversed(gap_ratio_range_list):
        if gap_end_ratio >= 1 or gap_start_ratio <= 0:
            continue
        else:
            if gap_end_ratio <= 0:
                gap_end_side_coordinate_pair = (None, None)
            else:
                gap_end_mid_location = arrow_vector * gap_end_ratio + tail_end_center_coordinate
                gap_end_side_coordinate_pair = side_coordinate_pair_generator(
                    gap_end_mid_location, arrow_side_unit_vector, stem_width)
            # If start ratio exceed 1, don't draw this path
            if gap_start_ratio >= 1:
                gap_start_side_coordinate_pair = (None, None)
            else:
                gap_start_mid_location = arrow_vector * gap_start_ratio + tail_end_center_coordinate
                gap_start_side_coordinate_pair = side_coordinate_pair_generator(
                    gap_start_mid_location, arrow_side_unit_vector, stem_width)
        gap_bound_location_list.append((gap_start_side_coordinate_pair, gap_end_side_coordinate_pair))
    return gap_bound_location_list


def construct_arrow_path_list(
        head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, bound_coordinate_list):
    head_start_step_list, head_end_step_list = create_start_end_step(head_start_point)
    complete_path_step_list = [
        *head_start_step_list,
        *head_path_step_list,
    ]
    transition_end_point_list = []
    transition_stop = False
    finished = False
    end_step_list = head_end_step_list
    for (
            (gap_start_side_coordinate_1, gap_start_side_coordinate_2),
            (gap_end_side_coordinate_1, gap_end_side_coordinate_2)) in bound_coordinate_list:
        ###############
        if gap_start_side_coordinate_1 is None and gap_start_side_coordinate_2 is None \
                and gap_end_side_coordinate_1 is not None and gap_end_side_coordinate_2 is not None:
            # This is a transition point
            complete_path_step_list.append(PathStep(PathOperation.lineto, gap_start_side_coordinate_1))
            transition_end_point_list.append(gap_end_side_coordinate_1)
        else:
            if len(transition_end_point_list) > 0:
                transition_stop = True
            if gap_start_side_coordinate_1 is None and gap_start_side_coordinate_2 is None:
                complete_path_step_list.extend(end_step_list)
            else:
                complete_path_step_list.extend([
                    PathStep(PathOperation.lineto, gap_start_side_coordinate_1),
                    PathStep(PathOperation.lineto, gap_start_side_coordinate_2),
                    *end_step_list
                ])
        if transition_stop:
            while len(transition_end_point_list) > 0:
                current_end_point = transition_end_point_list.pop()
                complete_path_step_list.append(PathStep(PathOperation.lineto, current_end_point))
            transition_stop = False
            transition_end_point_list = []
        ###############
        if gap_end_side_coordinate_1 is None and gap_end_side_coordinate_2 is None:
            finished = True
        else:
            start_step_list, end_step_list = create_start_end_step(gap_end_side_coordinate_2)
            complete_path_step_list.extend([
                *start_step_list,
                PathStep(PathOperation.lineto, gap_end_side_coordinate_1),
            ])
    if not finished:
        complete_path_step_list.extend([
            PathStep(PathOperation.lineto, tail_start_point),
            *tail_path_step_list,
            *end_step_list
        ])
    return complete_path_step_list


def calculate_branch_tail_coordinate(
        branch_head_coordinate, branch_extend_tail_coordinate, main_arrow_unit_direction_vector,
        dash_solid_empty_width, branch_obj, stem_width):
    if branch_obj.dash:
        branch_dash_solid_empty_width = dash_solid_empty_width
    else:
        branch_dash_solid_empty_width = None
    branch_arrow_direction_vector = branch_head_coordinate - branch_extend_tail_coordinate
    branch_arrow_direction_unit_vector = branch_arrow_direction_vector.unit_vector()
    mapped_branch_arrow_direction = np.abs(branch_arrow_direction_vector @ main_arrow_unit_direction_vector)
    similarity_ratio = stem_width / 2 / np.sqrt(
        branch_arrow_direction_vector.square_sum - mapped_branch_arrow_direction ** 2)
    mid_coordinate = branch_extend_tail_coordinate + similarity_ratio * branch_arrow_direction_vector
    mid_to_edge_difference_vector = branch_arrow_direction_unit_vector \
                                    * mapped_branch_arrow_direction * similarity_ratio
    if dash_solid_empty_width is None:
        # Main arrow is solid, therefore the branch is not dash
        branch_tail_coordinate = mid_coordinate - mid_to_edge_difference_vector
    elif branch_dash_solid_empty_width is None:
        # Main arrow is dash, but the branch is solid
        branch_tail_coordinate = mid_coordinate
    else:
        # Both main arrow and the branch is dash
        branch_tail_coordinate = mid_coordinate + mid_to_edge_difference_vector
    return branch_tail_coordinate, branch_dash_solid_empty_width


def analyze_branch(
        branch_list, gap_line_pair_list, dash_solid_empty_width,
        main_arrow_tail_coordinate, main_arrow_head_coordinate, stem_width, head_width, head_len):
    branch_arrow_path_step_list = []
    if branch_list is not None:
        main_arrow_direction_vector = main_arrow_head_coordinate - main_arrow_tail_coordinate
        main_arrow_unit_direction_vector = main_arrow_direction_vector.unit_vector()
        for branch_obj in branch_list:
            branch_head_coordinate = branch_obj.terminal_location
            branch_extend_tail_coordinate = branch_obj.stem_location * main_arrow_direction_vector \
                                            + main_arrow_tail_coordinate
            branch_tail_coordinate, branch_dash_solid_empty_width = calculate_branch_tail_coordinate(
                branch_head_coordinate, branch_extend_tail_coordinate, main_arrow_unit_direction_vector,
                dash_solid_empty_width, branch_obj, stem_width)
            current_branch_arrow_path_step_list = draw_an_arrow(
                branch_tail_coordinate, branch_head_coordinate, stem_width, head_width, head_len, False,
                branch_obj.arrow, gap_line_pair_list, branch_dash_solid_empty_width)
            branch_arrow_path_step_list.extend(current_branch_arrow_path_step_list)
    return branch_arrow_path_step_list


class ChevronArrow(ArrowBase):
    def __init__(
            self, tail_end_center: Vector, head: Vector, head_len_width_ratio: float,
            width: float, scale=1, bottom_left_offset=None, tail_arrow=True, head_arrow=True, **kwargs):
        assert head_len_width_ratio > 0
        assert width > 0
        self.tail_end_center = initialize_vector_input(tail_end_center)
        self.head = initialize_vector_input(head)
        self.head_len_width_ratio = head_len_width_ratio
        self.width = width
        self.tail_arrow = tail_arrow
        self.head_arrow = head_arrow
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        head = self.head
        tail_end_center = self.tail_end_center
        width = self.width
        head_len = width * self.head_len_width_ratio
        tail_arrow = self.tail_arrow
        head_arrow = self.head_arrow

        (
            head_path_step_list, tail_path_step_list, head_start_point, tail_start_point,
            arrow_side_unit_vector) = draw_chevron_head_and_tail(
            tail_end_center, head, head_len, width, tail_arrow, head_arrow)

        # tail_path_step_list, head_path_step_list, head_start_point, tail_start_point = draw_chevron_head_and_tail(
        #     tail_end_center, head, head_len, width)

        path_step_list = construct_arrow_path_list(
            head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, [])
        return path_step_list


class Arrow(ArrowBase):
    def __init__(
            self, tail: Vector, head: Vector, stem_width: float, head_width: float, head_len_width_ratio: float,
            tail_arrow: bool = False, head_arrow: bool = True, gap_line_pair_list: list = None,
            dash_solid_empty_width: (float, float) = None, branch_list: list = None,
            scale=1, bottom_left_offset=None, **kwargs):
        self.tail = initialize_vector_input(tail)
        self.head = initialize_vector_input(head)
        self.tail_arrow = tail_arrow
        self.head_arrow = head_arrow
        assert stem_width > 0
        self.stem_width = stem_width
        assert head_width > 0
        self.head_width = head_width
        assert head_len_width_ratio > 0
        self.head_len_width_ratio = head_len_width_ratio
        if gap_line_pair_list is not None:
            for gap_line1, gap_line2 in gap_line_pair_list:
                assert isinstance(gap_line1, np.ndarray) and len(gap_line1) == 3 \
                       and isinstance(gap_line2, np.ndarray) and len(gap_line2) == 3
            self.gap_line_pair_list = gap_line_pair_list
        else:
            self.gap_line_pair_list = None
        if dash_solid_empty_width is not None:
            self.dash_solid_empty_width = dash_solid_empty_width
        else:
            self.dash_solid_empty_width = None
        if branch_list is not None:
            self.branch_list = [Branch(**branch_dict) for branch_dict in branch_list]
        else:
            self.branch_list = None
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        tail = self.tail
        head = self.head
        stem_width = self.stem_width
        head_width = self.head_width
        head_len_width_ratio = self.head_len_width_ratio
        gap_line_pair_list = self.gap_line_pair_list
        dash_solid_empty_width = self.dash_solid_empty_width
        branch_list = self.branch_list

        main_arrow_head = self.head_arrow
        main_arrow_tail = self.tail_arrow
        head_len = head_width * head_len_width_ratio

        main_arrow_path_step_list = draw_an_arrow(
            tail, head, stem_width, head_width, head_len,
            main_arrow_tail, main_arrow_head, gap_line_pair_list, dash_solid_empty_width)

        branch_arrow_path_step_list = analyze_branch(
            branch_list, gap_line_pair_list, dash_solid_empty_width, tail, head,
            stem_width, head_width, head_len)

        main_arrow_path_step_list.extend(branch_arrow_path_step_list)
        return main_arrow_path_step_list


def side_coordinate_pair_generator_arc(center, radius, width, theta):
    side_coordinate_1 = convert_theta_to_coordinate(theta, center, radius + (width / 2))
    side_coordinate_2 = convert_theta_to_coordinate(theta, center, radius - (width / 2))
    return side_coordinate_1, side_coordinate_2


def arrow_coordinate_generator_arc(center, radius, stem_width, head_width, theta):
    arrow_stem_width_coordinate_1, arrow_stem_width_coordinate_2 = side_coordinate_pair_generator_arc(
        center, radius, stem_width, theta)
    arrow_head_width_coordinate_1, arrow_head_width_coordinate_2 = side_coordinate_pair_generator_arc(
        center, radius, head_width, theta)
    return arrow_stem_width_coordinate_1, arrow_head_width_coordinate_1, arrow_stem_width_coordinate_2, \
           arrow_head_width_coordinate_2


def draw_an_arrow_arc(
        center, radius, theta_head, theta_tail, stem_width, head_width, head_len_theta, tail_arrow, head_arrow,
        gap_line_pair_list, dash_solid_empty_width):
    (
        head_path_step_list, tail_path_step_list, head_start_point,
        tail_start_point, head_end_theta, tail_end_theta) = draw_head_and_tail_arc(
        head_width, stem_width, head_len_theta, center, radius,
        theta_head, theta_tail, tail_arrow, head_arrow)
    gap_bound_location_list = analyze_gap_and_dash_arc(
        theta_head, theta_tail, center, radius, gap_line_pair_list, dash_solid_empty_width, stem_width,
        tail_arrow, head_arrow)
    complete_path_step_list = construct_arrow_path_list_arc(
        head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, gap_bound_location_list,
        head_end_theta, tail_end_theta, center, radius, stem_width)
    return complete_path_step_list


def draw_head_and_tail_arc(
        head_width, stem_width, head_len_theta, center, radius,
        theta_head, theta_tail, tail_arrow: bool, head_arrow: bool):
    def draw_path_step_list(arrow_bool, arrow_theta, arrow_end_direction_sign, reverse):
        arrow_coordinate = convert_theta_to_coordinate(arrow_theta, center, radius)
        if arrow_bool:
            arrow_end_theta = arrow_theta - arrow_end_direction_sign * arrow_direction_sign * head_len_theta
            (
                arrow_stem_width_coordinate_1, arrow_head_width_coordinate_1,
                arrow_stem_width_coordinate_2,
                arrow_head_width_coordinate_2) = arrow_coordinate_generator_arc(
                center, radius, stem_width, head_width, arrow_end_theta)
            arrow_vertex_list = [
                arrow_stem_width_coordinate_2,
                arrow_head_width_coordinate_2,
                arrow_coordinate,
                arrow_head_width_coordinate_1,
                arrow_stem_width_coordinate_1,
            ]
        else:
            arrow_end_theta = arrow_theta
            arrow_side_coordinate_1, arrow_side_coordinate_2 = side_coordinate_pair_generator_arc(
                center, radius, stem_width, arrow_end_theta)
            arrow_vertex_list = [
                arrow_side_coordinate_2,
                arrow_side_coordinate_1,
            ]
        if reverse:
            arrow_vertex_list.reverse()
        arrow_start_point = arrow_vertex_list[0]
        arrow_path_step_list = []
        for vertex in arrow_vertex_list[1:]:
            arrow_path_step_list.append(PathStep(PathOperation.lineto, vertex))
        return arrow_end_theta, arrow_start_point, arrow_path_step_list

    arrow_direction_sign = np.sign(theta_head - theta_tail)

    head_end_theta, head_start_point, head_path_step_list = draw_path_step_list(head_arrow, theta_head, 1, False)
    tail_end_theta, tail_start_point, tail_path_step_list = draw_path_step_list(tail_arrow, theta_tail, -1, True)
    return head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, \
        head_end_theta, tail_end_theta


def analyze_gap_and_dash_arc(
        theta_head, theta_tail, center, radius, gap_line_pair_list, dash_solid_empty_width, stem_width,
        tail_arrow, head_arrow):
    gap_bound_location_list = []

    return gap_bound_location_list


def generate_bidirectional_arc(center, radius, width, theta1, theta2):
    outer_path_list = ellipse_arc_obj.generator(center, theta1, theta2, radius + (width / 2))
    if radius <= width / 2:
        inner_path_list = []
    else:
        inner_path_list = ellipse_arc_obj.generator(center, theta2, theta1, radius - (width / 2))
    return outer_path_list, inner_path_list


def construct_arrow_path_list_arc(
        head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, gap_bound_location_list,
        head_end_theta, tail_end_theta, center, radius, stem_width):
    head_start_step_list, head_end_step_list = create_start_end_step(head_start_point)
    complete_path_step_list = [
        *head_start_step_list,
        *head_path_step_list,
    ]
    finished = False
    arc_start_theta = head_end_theta
    end_step_list = head_end_step_list
    for (
            (gap_start_side_coordinate_1, gap_start_side_coordinate_2),
            (gap_end_side_coordinate_1, gap_end_side_coordinate_2),
            (gap_start_theta, gap_end_theta)) in gap_bound_location_list:
        if gap_start_side_coordinate_1 is None and gap_start_side_coordinate_2 is None:
            complete_path_step_list.extend(end_step_list)
        else:
            outer_path_list, inner_path_list = generate_bidirectional_arc(
                center, radius, stem_width, arc_start_theta, gap_start_theta)
            complete_path_step_list.extend([
                *outer_path_list,
                PathStep(PathOperation.lineto, gap_start_side_coordinate_2),
                *inner_path_list,
                *end_step_list
            ])
        if gap_end_side_coordinate_1 is None and gap_end_side_coordinate_2 is None:
            finished = True
        else:
            arc_start_theta = gap_end_theta
            start_step_list, end_step_list = create_start_end_step(gap_end_side_coordinate_2)
            complete_path_step_list.extend([
                *start_step_list,
                PathStep(PathOperation.lineto, gap_end_side_coordinate_1),
            ])
    if not finished:
        outer_path_list, inner_path_list = generate_bidirectional_arc(
            center, radius, stem_width, arc_start_theta, tail_end_theta)
        complete_path_step_list.extend([
            *outer_path_list,
            *tail_path_step_list,
            *inner_path_list,
            *end_step_list
        ])
    return complete_path_step_list


def analyze_branch_arc(
        arc_branch_list, gap_line_pair_list, dash_solid_empty_width,
        main_arrow_center_coordinate, main_arrow_radius, main_arrow_stem_width, main_arrow_head_width, head_len,
        theta_head, theta_tail):
    branch_arrow_path_step_list = []
    if arc_branch_list is not None:
        for arc_branch_obj in arc_branch_list:
            branch_head_coordinate = arc_branch_obj.terminal_location
            branch_tail_theta_location = arc_branch_obj.stem_location
            assert (branch_tail_theta_location - theta_head) * (branch_tail_theta_location - theta_tail) < 0
            branch_extend_tail_coordinate = convert_theta_to_coordinate(
                branch_tail_theta_location, main_arrow_center_coordinate, main_arrow_radius)
            main_arrow_unit_direction_vector = cos_sin(branch_tail_theta_location).vertical_vector_cw()
            branch_tail_coordinate, branch_dash_solid_empty_width = calculate_branch_tail_coordinate(
                branch_head_coordinate, branch_extend_tail_coordinate, main_arrow_unit_direction_vector,
                dash_solid_empty_width, arc_branch_obj, main_arrow_stem_width)
            current_branch_arrow_path_step_list = draw_an_arrow(
                branch_tail_coordinate, branch_head_coordinate, main_arrow_stem_width, main_arrow_head_width, head_len,
                False, arc_branch_obj.arrow, gap_line_pair_list, branch_dash_solid_empty_width)
            branch_arrow_path_step_list.extend(current_branch_arrow_path_step_list)
    return branch_arrow_path_step_list


class ArcChevronArrow(ArrowBase):
    def __init__(
            self, center: Vector, radius: float, theta_head: float, theta_tail_end_center: float, width: float,
            head_len_width_ratio: float, scale=1, bottom_left_offset=None, **kwargs):
        """head -> outer_arc -> tail -> inner_arc (CCW if head > tail, CW if head < tail)"""
        self.center = initialize_vector_input(center)
        assert radius > 0
        self.radius = radius
        self.theta_head = theta_head
        self.theta_tail_end_center = theta_tail_end_center
        assert width > 0
        self.width = width
        assert head_len_width_ratio > 0
        self.head_len_width_ratio = head_len_width_ratio
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        center = self.center
        radius = self.radius
        theta_head = self.theta_head
        theta_tail_end_center = self.theta_tail_end_center
        width = self.width

        head_len = width * self.head_len_width_ratio
        head_len_theta = head_len / radius * 360 / (2 * np.pi)
        total_delta_theta = np.abs(theta_head - theta_tail_end_center)
        assert head_len_theta < total_delta_theta
        direction = np.sign(theta_head - theta_tail_end_center)
        theta_tail = theta_tail_end_center + direction * head_len_theta
        theta_head_end = theta_head - direction * head_len_theta

        head_side_coordinate_1, head_side_coordinate_2 = side_coordinate_pair_generator_arc(
            center, radius, width, theta_head_end)
        head_coordinate = convert_theta_to_coordinate(theta_head, center, radius)
        tail_side_coordinate_1, tail_side_coordinate_2 = side_coordinate_pair_generator_arc(
            center, radius, width, theta_tail_end_center)
        tail_coordinate = convert_theta_to_coordinate(theta_tail, center, radius)

        head_vertex_list = [
            head_side_coordinate_2,
            head_coordinate,
            head_side_coordinate_1,
        ]
        tail_vertex_list = [
            tail_side_coordinate_1,
            tail_coordinate,
            tail_side_coordinate_2,
        ]
        head_path_step_list = [PathStep(PathOperation.lineto, vertex) for vertex in head_vertex_list[1:]]
        tail_path_step_list = [PathStep(PathOperation.lineto, vertex) for vertex in tail_vertex_list]

        complete_path_step_list = construct_arrow_path_list_arc(
            head_path_step_list, tail_path_step_list, head_side_coordinate_2, tail_side_coordinate_1, [],
            theta_head_end, theta_tail_end_center, center, radius, width)
        return complete_path_step_list


class ArcArrow(ArrowBase):
    def __init__(
            self, center: Vector, radius: float, theta_head: float, theta_tail: float,
            head_width: float, stem_width: float, head_len_width_ratio: float, tail_arrow=False, head_arrow=True,
            gap_line_pair_list: list = None, dash_solid_empty_width: (float, float) = None,
            branch_list: list = None, scale=1, bottom_left_offset=None, **kwargs):
        # head -> outer_arc -> tail -> inner_arc (CCW if head > tail, CW if head < tail)
        self.center = initialize_vector_input(center)
        assert radius > 0
        self.radius = radius
        self.theta_head = theta_head
        self.theta_tail = theta_tail
        assert head_width > 0
        self.head_width = head_width
        assert stem_width > 0
        self.stem_width = stem_width
        assert head_len_width_ratio > 0
        self.head_len_width_ratio = head_len_width_ratio
        self.tail_arrow = tail_arrow
        self.head_arrow = head_arrow
        if gap_line_pair_list is not None:
            for gap_line1, gap_line2 in gap_line_pair_list:
                assert isinstance(gap_line1, np.ndarray) and len(gap_line1) == 3 \
                       and isinstance(gap_line2, np.ndarray) and len(gap_line2) == 3
            self.gap_line_pair_list = gap_line_pair_list
        else:
            self.gap_line_pair_list = None
        if dash_solid_empty_width is not None:
            self.dash_solid_empty_width = dash_solid_empty_width
        else:
            self.dash_solid_empty_width = None
        if branch_list is not None:
            self.branch_list = [Branch(**branch_dict) for branch_dict in branch_list]
        else:
            self.branch_list = None
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        center = self.center
        radius = self.radius
        theta_tail = self.theta_tail
        theta_head = self.theta_head
        stem_width = self.stem_width
        head_width = self.head_width
        head_len_width_ratio = self.head_len_width_ratio
        gap_line_pair_list = self.gap_line_pair_list
        dash_solid_empty_width = self.dash_solid_empty_width
        branch_list = self.branch_list

        head_len = head_width * head_len_width_ratio
        head_len_theta = head_len / radius * 360 / (2 * np.pi)
        delta_theta = np.abs(theta_head - theta_tail)
        direction = np.sign(theta_head - theta_tail)
        main_arrow_head = self.head_arrow
        main_arrow_tail = self.tail_arrow
        if main_arrow_tail:
            assert 2 * head_len_theta < delta_theta
        else:
            assert head_len_theta < delta_theta

        main_arrow_path_step_list = draw_an_arrow_arc(
            center, radius, theta_head, theta_tail, stem_width, head_width, head_len_theta,
            main_arrow_tail, main_arrow_head, gap_line_pair_list, dash_solid_empty_width)

        branch_arrow_path_step_list = analyze_branch_arc(
            branch_list, gap_line_pair_list, dash_solid_empty_width, self.center, radius,
            stem_width, head_width, head_len, theta_head, theta_tail)

        main_arrow_path_step_list.extend(branch_arrow_path_step_list)
        return main_arrow_path_step_list


class ArcPathArrow(ArcArrow):
    def __init__(
            self, tail: Vector, mid: Vector, head: Vector, stem_width: float, head_width: float,
            head_len_width_ratio: float, tail_arrow: bool = False, head_arrow: bool = True,
            gap_line_pair_list: list = None, dash_solid_empty_width: (float, float) = None, branch_list: list = None,
            scale=1, bottom_left_offset=None, **kwargs):
        center, radius, (theta_tail, theta_mid, theta_head) = calculate_center_radius_angle_of_three_points_on_circle(
            tail, mid, head)
        if center is None:
            raise ValueError('Three points are on the line!')
        super().__init__(
            center, radius, theta_head, theta_tail,
            head_width=head_width, stem_width=stem_width, head_len_width_ratio=head_len_width_ratio,
            tail_arrow=tail_arrow, head_arrow=head_arrow,
            gap_line_pair_list=gap_line_pair_list, dash_solid_empty_width=dash_solid_empty_width,
            branch_list=branch_list, scale=scale, bottom_left_offset=bottom_left_offset, **kwargs)


def calculate_transition_points_in_bent_arrow(tail, head, radius, arrow_head_direction):
    mid_location1 = Vector(head.x, tail.y)
    mid_location2 = Vector(tail.x, head.y)
    ccw_turn90_matrix = np.array([[0, -1], [1, 0]])
    mid1_head_vector = head - mid_location1
    ccw_rotated_tail_mid1_vector = ccw_turn90_matrix @ (mid_location1 - tail).T
    test_product = mid1_head_vector @ ccw_rotated_tail_mid1_vector
    if arrow_head_direction == ParameterName.ccw:
        if test_product > 0:
            mid_location = mid_location1
        else:
            mid_location = mid_location2
    elif arrow_head_direction == ParameterName.cw:
        if test_product > 0:
            mid_location = mid_location2
        else:
            mid_location = mid_location1
    else:
        raise ValueError()

    mid_to_head_unit_vector = Vector(array=np.sign(head - mid_location))
    mid_to_tail_unit_vector = Vector(array=np.sign(tail - mid_location))
    head_transition_point = mid_location + mid_to_head_unit_vector * radius
    tail_transition_point = mid_location + mid_to_tail_unit_vector * radius
    bent_center = mid_location + (mid_to_head_unit_vector + mid_to_tail_unit_vector) * radius
    return mid_location, bent_center, tail_transition_point, head_transition_point


def generate_arc_path_list_in_bent_arrow(
        bent_center, tail_transition_point, head_transition_point, width, radius, arrow_head_direction):
    tail_theta_test_vector = tail_transition_point - bent_center
    tail_theta = calculate_degree_of_vector(tail_theta_test_vector)
    if arrow_head_direction == ParameterName.ccw:
        head_theta = tail_theta + 90
        theta1 = tail_theta
        theta2 = head_theta
        outer_path_list, inner_path_list = generate_bidirectional_arc(
            bent_center, radius, width, theta1, theta2)
        first_arc_path_list, second_arc_path_list = inner_path_list, outer_path_list
    elif arrow_head_direction == ParameterName.cw:
        head_theta = tail_theta - 90
        theta1 = head_theta
        theta2 = tail_theta
        outer_path_list, inner_path_list = generate_bidirectional_arc(
            bent_center, radius, width, theta1, theta2)
        first_arc_path_list, second_arc_path_list = outer_path_list, inner_path_list
    else:
        raise ValueError()
    return first_arc_path_list, second_arc_path_list


# Upstream and downstream path should be lineto
def arc_adjacent_path_check(
        arc_path_list, upstream_lineto_point, normal_downstream_lineto_point,
        downstream_backup_point, mid_location):
    """
        If the arc is normal, use the normal_downstream_lineto_point
        If the arc is empty, use downstream_backup_point as transition point
    """
    if len(arc_path_list) == 0:
        """Correct point will be always further to mid_location"""
        combined_point_1 = Vector(upstream_lineto_point.x, downstream_backup_point.y)
        combined_point_2 = Vector(downstream_backup_point.x, upstream_lineto_point.y)
        if abs(combined_point_1.x - mid_location.x) > abs(combined_point_2.x - mid_location.x):
            combined_point = combined_point_1
        else:
            combined_point = combined_point_2
        path_list = [
            PathStep(PathOperation.lineto, combined_point),
            PathStep(PathOperation.lineto, normal_downstream_lineto_point)
        ]
    else:
        path_list = [
            PathStep(PathOperation.lineto, upstream_lineto_point),
            *arc_path_list,
            PathStep(PathOperation.lineto, normal_downstream_lineto_point)
        ]
    return path_list


class BentChevronArrow(ArrowBase):
    def __init__(
            self, tail_end_center: Vector, head: Vector, head_len_width_ratio: float,
            width: float, radius: float, arrow_head_direction=ParameterName.ccw, head_arrow=True, tail_arrow=True,
            scale=1, bottom_left_offset=None, **kwargs):
        assert head_len_width_ratio > 0
        assert width > 0
        self.tail_end_center = initialize_vector_input(tail_end_center)
        self.head = initialize_vector_input(head)
        self.head_len_width_ratio = head_len_width_ratio
        self.width = width
        assert radius > 0
        self.radius = radius
        self.arrow_head_direction = arrow_head_direction
        self.head_arrow = head_arrow
        self.tail_arrow = tail_arrow
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        tail_end_center = self.tail_end_center
        head = self.head
        width = self.width
        head_len_width_ratio = self.head_len_width_ratio
        radius = self.radius
        arrow_head_direction = self.arrow_head_direction

        head_arrow = self.head_arrow
        tail_arrow = self.tail_arrow
        head_len = width * head_len_width_ratio

        (
            mid_location, bent_center, tail_transition_point,
            head_transition_point) = calculate_transition_points_in_bent_arrow(
            tail_end_center, head, radius, arrow_head_direction)

        first_arc_path_list, second_arc_path_list = generate_arc_path_list_in_bent_arrow(
            bent_center, tail_transition_point, head_transition_point, width, radius, arrow_head_direction)

        (
            tail_transition_path_step_list, tail_path_step_list, tail_transition_start_point, tail_start_point,
            _) = draw_chevron_head_and_tail(
            tail_end_center, tail_transition_point, head_len, width, tail_arrow, False)
        tail_transition_end_point = tail_transition_path_step_list[0].vertex_list[0]
        (
            head_path_step_list, head_transition_path_step_list, head_start_point, head_transition_start_point,
            _) = draw_chevron_head_and_tail(
            head_transition_point, head, head_len, width, False, head_arrow)
        head_transition_end_point = head_transition_path_step_list[0].vertex_list[0]
        head_start_path_list, head_end_path_list = create_start_end_step(head_start_point)

        first_arc_adjacent_path_list = arc_adjacent_path_check(
            first_arc_path_list, head_transition_start_point, tail_start_point, tail_transition_end_point,
            mid_location)
        second_arc_adjacent_path_list = arc_adjacent_path_check(
            second_arc_path_list, tail_transition_start_point, head_start_point, head_transition_end_point,
            mid_location)
        complete_path_step_list = [
            *head_start_path_list,
            *head_path_step_list,
            *first_arc_adjacent_path_list,
            *tail_path_step_list,
            *second_arc_adjacent_path_list,
            *head_end_path_list[1:],
        ]

        return complete_path_step_list


class BentArrow(ArrowBase):
    def __init__(
            self, tail: Vector, head: Vector, stem_width: float, head_width: float, head_len_width_ratio: float,
            radius: float, arrow_head_direction=ParameterName.ccw, head_arrow=True, tail_arrow=False,
            scale=1, bottom_left_offset=None, **kwargs):
        self.tail = initialize_vector_input(tail)
        self.head = initialize_vector_input(head)
        assert stem_width > 0
        self.stem_width = stem_width
        assert head_width > 0
        self.head_width = head_width
        assert head_len_width_ratio > 0
        self.head_len_width_ratio = head_len_width_ratio
        assert radius > 0
        self.radius = radius
        self.arrow_head_direction = arrow_head_direction
        self.head_arrow = head_arrow
        self.tail_arrow = tail_arrow
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        tail = self.tail
        head = self.head
        stem_width = self.stem_width
        head_width = self.head_width
        head_len_width_ratio = self.head_len_width_ratio
        radius = self.radius
        arrow_head_direction = self.arrow_head_direction

        head_arrow = self.head_arrow
        tail_arrow = self.tail_arrow
        head_len = head_width * head_len_width_ratio

        (
            mid_location, bent_center, tail_transition_point,
            head_transition_point) = calculate_transition_points_in_bent_arrow(
            tail, head, radius, arrow_head_direction)

        # First check if the transition arc could be drawn. If not, adjust adjacent paths.
        first_arc_path_list, second_arc_path_list = generate_arc_path_list_in_bent_arrow(
            bent_center, tail_transition_point, head_transition_point, stem_width, radius, arrow_head_direction)

        # tail part draw
        (
            tail_path_step_list, tail_transition_path_step_list, tail_start_point, tail_transition_start_point,
            *_) = draw_head_and_tail(
            head_width, stem_width, head_len, tail_transition_point, tail, False, tail_arrow)
        # tail_lineto_transition_path = PathStep(PathOperation.lineto, tail_transition_start_point)
        tail_transition_end_point = tail_transition_path_step_list[0].vertex_list[0]
        # head part draw
        (
            head_path_step_list, head_transition_path_step_list, head_start_point, head_transition_start_point,
            *_) = draw_head_and_tail(
            head_width, stem_width, head_len, head_transition_point, head, False, head_arrow)
        # head_lineto_transition_path = PathStep(PathOperation.lineto, head_transition_start_point)
        head_transition_end_point = head_transition_path_step_list[0].vertex_list[0]
        head_start_path_list, head_end_path_list = create_start_end_step(head_start_point)

        first_arc_adjacent_path_list = arc_adjacent_path_check(
            first_arc_path_list, head_transition_start_point, tail_start_point, tail_transition_end_point,
            mid_location)
        second_arc_adjacent_path_list = arc_adjacent_path_check(
            second_arc_path_list, tail_transition_start_point, head_start_point, head_transition_end_point,
            mid_location)

        complete_path_step_list = [
            *head_start_path_list,
            *head_path_step_list,
            # head_lineto_transition_path,
            # *first_arc_path_list,
            # PathStep(PathOperation.lineto, tail_start_point),
            *first_arc_adjacent_path_list,
            *tail_path_step_list,
            # tail_lineto_transition_path,
            # *second_arc_path_list,
            # *head_end_path_list,
            *tail_path_step_list,
            *second_arc_adjacent_path_list,
            *head_end_path_list[1:],
        ]

        return complete_path_step_list


def broken_transition_side_coordinate_pair_generator(start_point, middle_point, end_point, width):
    *_, start_arrow_direction_unit_vector, start_arrow_side_unit_vector = calculate_necessary_vector(
        middle_point, start_point)
    start_side_coordinate_1, start_side_coordinate_2 = side_coordinate_pair_generator(
        start_point, start_arrow_side_unit_vector, width)
    *_, end_arrow_direction_unit_vector, end_arrow_side_unit_vector = calculate_necessary_vector(
        end_point, middle_point)
    end_side_coordinate_1, end_side_coordinate_2 = side_coordinate_pair_generator(
        middle_point, end_arrow_side_unit_vector, width)
    intersect_coordinate_1 = solve_intersect_by_slope_point_line(
        start_side_coordinate_1, start_arrow_direction_unit_vector,
        end_side_coordinate_1, end_arrow_direction_unit_vector)
    intersect_coordinate_2 = solve_intersect_by_slope_point_line(
        start_side_coordinate_2, start_arrow_direction_unit_vector,
        end_side_coordinate_2, end_arrow_direction_unit_vector)
    return intersect_coordinate_1, intersect_coordinate_2


def broken_arrow_transition_coordinate_generator(transition_point_list, tail_end_center, head, width):
    """
    Transition points are ordered from tail to head, but the gap_bound_list is from head to tail. Therefore,
    the list needs to be reversed before output.
    """
    start_point = tail_end_center
    intersect_coordinate_list = []
    for transition_point_index, transition_point in enumerate(transition_point_list):
        middle_point = transition_point
        try:
            end_point = transition_point_list[transition_point_index + 1]
        except IndexError:
            end_point = head
        intersect_coordinate_1, intersect_coordinate_2 = broken_transition_side_coordinate_pair_generator(
            start_point, middle_point, end_point, width)
        intersect_coordinate_list.append((
            (None, None),
            (intersect_coordinate_1, intersect_coordinate_2)
        ))
    intersect_coordinate_list = list(reversed(intersect_coordinate_list))
    return intersect_coordinate_list


class BrokenChevronArrow(ArrowBase):
    def __init__(
            self, tail_end_center: Vector, head: Vector, head_len_width_ratio: float,
            width: float, transition_point_list=(),
            scale=1, bottom_left_offset=None, tail_arrow=True, head_arrow=True, **kwargs):
        assert head_len_width_ratio > 0
        assert width > 0
        self.tail_end_center = initialize_vector_input(tail_end_center)
        self.head = initialize_vector_input(head)
        self.head_len_width_ratio = head_len_width_ratio
        self.width = width
        self.tail_arrow = tail_arrow
        self.head_arrow = head_arrow
        self.transition_point_list = [
            initialize_vector_input(transition_point) for transition_point in transition_point_list]
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        head = self.head
        tail_end_center = self.tail_end_center
        width = self.width
        head_len = width * self.head_len_width_ratio
        tail_arrow = self.tail_arrow
        head_arrow = self.head_arrow
        transition_point_list = self.transition_point_list

        (
            head_path_step_list, tail_path_step_list, head_start_point, tail_start_point,
            arrow_side_unit_vector) = draw_chevron_head_and_tail(
            tail_end_center, head, head_len, width, tail_arrow, head_arrow)
        intersect_coordinate_list = broken_arrow_transition_coordinate_generator(
            transition_point_list, tail_end_center, head, width)
        path_step_list = construct_arrow_path_list(
            head_path_step_list, tail_path_step_list, head_start_point, tail_start_point, intersect_coordinate_list)
        return path_step_list


class BrokenArrow(ArrowBase):
    def __init__(
            self, tail: Vector, head: Vector, stem_width: float, head_width: float, head_len_width_ratio: float,
            tail_arrow: bool = False, head_arrow: bool = True, gap_line_pair_list: list = None,
            dash_solid_empty_width: (float, float) = None, branch_list: list = None,
            transition_point_list: list = (), scale=1, bottom_left_offset=None, **kwargs):
        self.tail = initialize_vector_input(tail)
        self.head = initialize_vector_input(head)
        self.tail_arrow = tail_arrow
        self.head_arrow = head_arrow
        assert stem_width > 0
        self.stem_width = stem_width
        assert head_width > 0
        self.head_width = head_width
        assert head_len_width_ratio > 0
        self.head_len_width_ratio = head_len_width_ratio
        if gap_line_pair_list is not None:
            for gap_line1, gap_line2 in gap_line_pair_list:
                assert isinstance(gap_line1, np.ndarray) and len(gap_line1) == 3 \
                       and isinstance(gap_line2, np.ndarray) and len(gap_line2) == 3
            self.gap_line_pair_list = gap_line_pair_list
        else:
            self.gap_line_pair_list = None
        if dash_solid_empty_width is not None:
            self.dash_solid_empty_width = dash_solid_empty_width
        else:
            self.dash_solid_empty_width = None
        if branch_list is not None:
            self.branch_list = [Branch(**branch_dict) for branch_dict in branch_list]
        else:
            self.branch_list = None
        self.transition_point_list = [
            initialize_vector_input(transition_point) for transition_point in transition_point_list]
        super().__init__(scale, bottom_left_offset, **kwargs)

    def path_step_generator(self):
        tail = self.tail
        head = self.head
        stem_width = self.stem_width
        head_width = self.head_width
        head_len_width_ratio = self.head_len_width_ratio
        gap_line_pair_list = self.gap_line_pair_list
        dash_solid_empty_width = self.dash_solid_empty_width
        branch_list = self.branch_list
        transition_point_list = self.transition_point_list

        main_arrow_head = self.head_arrow
        main_arrow_tail = self.tail_arrow
        head_len = head_width * head_len_width_ratio

        main_arrow_path_step_list = draw_an_arrow(
            tail, head, stem_width, head_width, head_len,
            main_arrow_tail, main_arrow_head, gap_line_pair_list, dash_solid_empty_width, transition_point_list)

        branch_arrow_path_step_list = analyze_branch(
            branch_list, gap_line_pair_list, dash_solid_empty_width, tail, head,
            stem_width, head_width, head_len)

        main_arrow_path_step_list.extend(branch_arrow_path_step_list)
        return main_arrow_path_step_list


