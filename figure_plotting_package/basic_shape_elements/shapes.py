from .config import enum, np, mpath, mpatches, transforms, mlines, Color, Vector, black_color, LineStyle, JoinStyle
from .config import rotate_corner_offset_around_center, calculate_top_right_point, \
    calculate_bottom_left_point, cos_sin, initialize_vector_input, check_enum_obj, \
    calculate_pedal_of_one_point_to_segment_defined_by_two_points

from .basic_region import Region


class BasicShape(Region):
    def __init__(
            self, bottom_left: Vector, size: Vector, edge_width: float = 1, edge_style: LineStyle = LineStyle.normal,
            edge_color: Color = black_color, face_color: Color = None, alpha: float = None, z_order: float = 0,
            join_style: JoinStyle = JoinStyle.miter,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        super(BasicShape, self).__init__(bottom_left, size, **kwargs)
        self.edge_width = 0 if edge_width is None else edge_width
        self.edge_color = edge_color
        self.face_color = face_color
        if alpha is not None:
            if face_color is None:
                raise ValueError('Must set face_color first before set alpha')
            self.face_color = face_color.add_transparency(alpha)
        self.fill = face_color is not None
        self.edge_style = check_enum_obj(edge_style, LineStyle)
        self.z_order = z_order
        self.join_style = check_enum_obj(join_style, JoinStyle)

        # If transformed in children class, the scale and bottom_left_offset argument will be intercepted in
        # derived class. In this step scale and bottom_left_offset will be default value.
        # Therefore, there will be no transformation.
        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

        self.mpl_patch = None

    def convert_to_mpl_patch(self):
        pass

    def add_to_mpl_axes(self, ax, transformation):
        if self.mpl_patch is None:
            self.convert_to_mpl_patch()
        assert self.mpl_patch is not None
        current_patch = ax.add_patch(self.mpl_patch)
        current_patch.set_transform(transformation)
        return current_patch

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        shape_obj = self.add_to_mpl_axes(parent_ax, parent_transformation)
        return shape_obj


class Line(BasicShape):
    def __init__(
            self, start: Vector, end: float, edge_width: float = 1, edge_style: LineStyle = LineStyle.normal,
            edge_color: Color = black_color, join_style: JoinStyle = JoinStyle.miter,
            alpha: float = None, z_order: float = 0, **kwargs):
        start = initialize_vector_input(start)
        end = initialize_vector_input(end)
        self.start = start
        self.end = end
        start_end_array = np.vstack([start, end])
        bottom_left = Vector(array=np.min(start_end_array, axis=0))
        top_right = np.max(start_end_array, axis=1)
        size = top_right - bottom_left
        super().__init__(
            bottom_left, size, edge_width=edge_width, edge_style=edge_style,
            edge_color=edge_color, alpha=alpha, z_order=z_order,
            join_style=join_style, **kwargs)

    def convert_to_mpl_patch(self):
        x_data = Vector(self.start[0], self.end[0])
        y_data = Vector(self.start[1], self.end[1])
        self.mpl_patch = mlines.Line2D(
            x_data, y_data, linestyle=self.edge_style, linewidth=self.edge_width,
            color=self.edge_color, zorder=self.z_order,
            solid_joinstyle=self.join_style, dash_joinstyle=self.join_style)


class Circle(BasicShape):
    def __init__(self, center: Vector, radius: float, **kwargs):
        assert radius > 0
        self.center = initialize_vector_input(center)
        self.radius = radius
        bottom_left = self.center - radius
        size = Vector(2 * radius, 2 * radius)
        super(Circle, self).__init__(bottom_left, size, **kwargs)

    def convert_to_mpl_patch(self):
        self.mpl_patch = mpatches.Circle(
            self.center.to_tuple(), self.radius, fill=self.fill, linestyle=self.edge_style, linewidth=self.edge_width,
            edgecolor=self.edge_color, facecolor=self.face_color, zorder=self.z_order, joinstyle=self.join_style)


class Rectangle(BasicShape):
    def __init__(self, center: Vector, width: float, height: float, angle=0, **kwargs):
        assert -45 <= angle <= 45
        assert width > 0
        assert height > 0
        self.center = initialize_vector_input(center)
        self.width = width
        self.height = height
        self.angle = angle
        self.corner_offset_matrix = np.array([
            [- width / 2, - height / 2],
            [width / 2, - height / 2],
            [width / 2, height / 2],
            [- width / 2, height / 2]])

        point_location_matrix = rotate_corner_offset_around_center(
            self.center, self.corner_offset_matrix, angle)
        self.square_bottom_left_point = point_location_matrix[0, :]
        if angle == 0:
            super(Rectangle, self).__init__(
                Vector(array=point_location_matrix[0, :]), Vector(width, height), **kwargs)
        else:
            bottom_left_corner = calculate_bottom_left_point(point_location_matrix)
            top_right_corner = calculate_top_right_point(point_location_matrix)
            super(Rectangle, self).__init__(
                bottom_left_corner, top_right_corner - bottom_left_corner, **kwargs)

    def convert_to_mpl_patch(self):
        self.mpl_patch = mpatches.Rectangle(
            # self.bottom_left.to_tuple(),
            self.square_bottom_left_point,
            self.width, self.height, self.angle,
            fill=self.fill, linestyle=self.edge_style, linewidth=self.edge_width,
            edgecolor=self.edge_color, facecolor=self.face_color, zorder=self.z_order, joinstyle=self.join_style)


class Ellipse(BasicShape):
    def __init__(self, center: Vector, width: float, height: float, angle=0, **kwargs):
        assert -45 <= angle <= 45
        assert width > 0
        assert height > 0
        self.center = initialize_vector_input(center)
        self.width = width
        self.height = height
        self.angle = angle
        self.corner_offset_matrix = np.array([
            [- width / 2, - height / 2],
            [width / 2, - height / 2],
            [width / 2, height / 2],
            [- width / 2, height / 2]])

        self.point_location_matrix = rotate_corner_offset_around_center(
            self.center, self.corner_offset_matrix, angle)
        if angle == 0:
            bottom_left_corner = Vector(array=self.point_location_matrix[0, :])
            size_vector = Vector(width, height)
        else:
            bottom_left_corner = calculate_bottom_left_point(self.point_location_matrix)
            top_right_corner = calculate_top_right_point(self.point_location_matrix)
            size_vector = top_right_corner - bottom_left_corner
        super(Ellipse, self).__init__(bottom_left_corner, size_vector, **kwargs)

    def convert_to_mpl_patch(self):
        self.mpl_patch = mpatches.Ellipse(
            self.center.to_tuple(), self.width, self.height, self.angle,
            fill=self.fill, linestyle=self.edge_style, linewidth=self.edge_width,
            edgecolor=self.edge_color, facecolor=self.face_color, zorder=self.z_order, joinstyle=self.join_style)


class Polygon(BasicShape):
    def __init__(self, vertex_list, **kwargs):
        assert np.all(vertex_list[0] == vertex_list[-1])
        self.vertex_num = len(vertex_list) - 1
        self.vertex_list = vertex_list
        bottom_left_point = calculate_bottom_left_point(vertex_list)
        top_right_point = calculate_top_right_point(vertex_list)
        super(Polygon, self).__init__(bottom_left_point, top_right_point - bottom_left_point, **kwargs)

    def convert_to_mpl_patch(self):
        self.mpl_patch = mpatches.Polygon(
            np.array(self.vertex_list), closed=True,
            fill=self.fill, linestyle=self.edge_style, linewidth=self.edge_width,
            edgecolor=self.edge_color, facecolor=self.face_color, zorder=self.z_order, joinstyle=self.join_style)


class PathOperation(enum.Enum):
    stop = mpath.Path.STOP
    moveto = mpath.Path.MOVETO
    lineto = mpath.Path.LINETO
    curve3 = mpath.Path.CURVE3
    curve4 = mpath.Path.CURVE4
    closepoly = mpath.Path.CLOSEPOLY


class PathStep(object):
    empty_step_set = {
        PathOperation.moveto,
        PathOperation.closepoly,
        PathOperation.stop
    }

    def __init__(
            self, path_operation: PathOperation, point1: Vector = None, point2: Vector = None, point3: Vector = None):
        self.path_operation = path_operation
        self.vertex_list = []
        if path_operation in {PathOperation.moveto, PathOperation.lineto, PathOperation.curve3, PathOperation.curve4}:
            assert point1 is not None
            self.vertex_list.append(initialize_vector_input(point1))
        if path_operation in {PathOperation.curve3, PathOperation.curve4}:
            assert point2 is not None
            self.vertex_list.append(initialize_vector_input(point2))
        if path_operation == PathOperation.curve4:
            assert point3 is not None
            self.vertex_list.append(initialize_vector_input(point3))

    def is_empty_step(self):
        return self.path_operation in self.empty_step_set

    def to_vertex_code_list(self):
        vertex_list = []
        code_list = []
        for vertex in self.vertex_list:
            vertex_list.append(vertex.to_tuple())
            code_list.append(self.path_operation.value)
        return vertex_list, code_list

    def __repr__(self):
        return "{}: {}".format(self.path_operation.name, ",".join([vertex.__str__() for vertex in self.vertex_list]))

    def copy(self):
        return PathStep(self.path_operation, *self.vertex_list)


class EllipseArc(object):
    maximal_degree_each_segment = 30

    def __init__(self):
        self.unit_circle_point_dict = {}

    @staticmethod
    def length_of_bezier_arm(angle):
        return 4 * np.tan(np.deg2rad(angle / 4)) / 3

    @staticmethod
    def four_control_point(angle):
        # The first control point is on x-axis: (1, 0)
        # Draw counterclockwise
        cp1 = Vector(1, 0)
        arm_length = EllipseArc.length_of_bezier_arm(angle)
        cp2 = Vector(1, arm_length)
        cp4 = cos_sin(angle)
        cp4_arm_vector = arm_length * cp4.vertical_vector()
        cp3 = cp4 - cp4_arm_vector
        return np.array([cp1, cp2, cp3, cp4])

    def generator(self, center, theta1, theta2, half_width, half_height=None, angle=0):
        """
        Arc is draw from theta1 to theta2
        theta1 and theta2 are defined in degree by counterclockwise before rotate by angle
        :param center:
        :param half_width:
        :param half_height:
        :param theta1:
        :param theta2:
        :param angle:
        :return:
        """
        assert half_width > 0
        if half_height is not None:
            assert half_height > 0
        delta_theta = np.abs(theta2 - theta1)
        if delta_theta in self.unit_circle_point_dict:
            unit_circle_point_list = self.unit_circle_point_dict[delta_theta]
        else:
            segment_num = int(np.ceil(delta_theta / self.maximal_degree_each_segment))
            each_segment_delta_theta = delta_theta / segment_num
            if each_segment_delta_theta in self.unit_circle_point_dict:
                unit_circle_each_segment_point = self.unit_circle_point_dict[each_segment_delta_theta]
            else:
                unit_circle_each_segment_point = EllipseArc.four_control_point(each_segment_delta_theta)
                self.unit_circle_point_dict[each_segment_delta_theta] = unit_circle_each_segment_point
            unit_circle_point_list = [unit_circle_each_segment_point]
            segment_rotate_trans = transforms.Affine2D()
            for index in range(1, segment_num):
                segment_rotate_trans.rotate_deg(each_segment_delta_theta)
                updated_control_point = segment_rotate_trans.transform(unit_circle_each_segment_point)
                unit_circle_point_list.append(updated_control_point)
            self.unit_circle_point_dict[delta_theta] = unit_circle_point_list
        if theta2 < theta1:
            # unit_circle_point_list = [
            #     unit_circle_point[::-1] for unit_circle_point in reversed(unit_circle_point_list)]
            unit_circle_point_list = [
                unit_circle_point @ np.array([[1, 0], [0, -1]]) for unit_circle_point in unit_circle_point_list]
        theta1_rotate_trans = transforms.Affine2D().rotate_deg(theta1)
        unit_circle_point_list = [
            theta1_rotate_trans.transform(unit_circle_point) for unit_circle_point in unit_circle_point_list]
        final_point_trans = transforms.Affine2D().scale(half_width, half_height)
        if angle != 0:
            final_point_trans.rotate_deg(angle)
        final_point_trans.translate(*center)
        final_point_list = []
        for unit_circle_point in unit_circle_point_list:
            final_point_list.append(final_point_trans.transform(unit_circle_point))
        final_path_step_list = []
        for final_point_array in final_point_list:
            final_path_step_list.append(PathStep(PathOperation.curve4, *final_point_array[1:]))
        return final_path_step_list


ellipse_arc_obj = EllipseArc()


class PathShape(BasicShape):
    def __init__(self, path_step_list: list, closed=True, **kwargs):
        # self.path_step_list = path_step_list
        # self.path_num = len(path_step_list)
        self.closed = closed
        vertex_list = []
        code_list = []
        first_step_vertex_list = None
        first_step_code_list = None
        for path_operation_obj in path_step_list:
            current_vertex_list, current_code_list = path_operation_obj.to_vertex_code_list()
            if closed:
                if first_step_vertex_list is None and not path_operation_obj.is_empty_step():
                    first_step_vertex_list = current_vertex_list
                    first_step_code_list = current_code_list
                elif path_operation_obj.path_operation == PathOperation.closepoly:
                    vertex_list.extend(first_step_vertex_list)
                    code_list.extend(first_step_code_list)
                    first_step_vertex_list = None
                    first_step_code_list = None
            vertex_list.extend(current_vertex_list)
            code_list.extend(current_code_list)
        self.vertex_array = np.array(vertex_list)
        self.code_array = np.array(code_list)

        bottom_left_point = calculate_bottom_left_point(self.vertex_array)
        top_right_point = calculate_top_right_point(self.vertex_array)
        BasicShape.__init__(self, bottom_left_point, top_right_point - bottom_left_point, **kwargs)

    def move_and_scale(
            self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, reset_vertex_array=True):
        if scale == 1 and bottom_left_offset is None:
            return
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        if not reset_vertex_array:
            return
        if bottom_left_offset is None:
            bottom_left_offset = Vector(0, 0)
        else:
            bottom_left_offset = initialize_vector_input(bottom_left_offset)
        self.vertex_array = transforms.Affine2D().scale(scale).translate(*bottom_left_offset).transform(
            self.vertex_array)

    def path_step_generator(self):
        return []

    def convert_to_mpl_patch(self):
        path = mpath.Path(self.vertex_array, self.code_array)
        if not self.closed:
            fill = False
            facecolor = None
        else:
            fill = self.fill
            facecolor = self.face_color
        self.mpl_patch = mpatches.PathPatch(
            path, fill=fill, linestyle=self.edge_style, linewidth=self.edge_width,
            edgecolor=self.edge_color, facecolor=facecolor, zorder=self.z_order, joinstyle=self.join_style)


class PathRectangle(PathShape):
    def __init__(
            self, center: Vector, width: float, height: float, angle=0,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        assert -45 <= angle <= 45
        assert width > 0
        assert height > 0
        self.center = initialize_vector_input(center)
        self.width = width
        self.height = height
        self.angle = angle
        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment, reset_vertex_array=False)
        path_step_list = self.path_step_generator()
        PathShape.__init__(self, path_step_list, **kwargs)

    def path_step_generator(self):
        width = self.width
        height = self.height

        corner_offset_matrix = np.array([
            [- width / 2, - height / 2],
            [width / 2, - height / 2],
            [width / 2, height / 2],
            [- width / 2, height / 2]])

        point_location_matrix = rotate_corner_offset_around_center(
            self.center, corner_offset_matrix, self.angle)
        path_step_list = []
        for edge_index in range(4):
            if edge_index == 0:
                operation = PathOperation.moveto
            else:
                operation = PathOperation.lineto
            path_step_list.append(PathStep(operation, point_location_matrix[edge_index]))
            if edge_index == 3:
                path_step_list.append(PathStep(PathOperation.lineto, point_location_matrix[0]))
                path_step_list.append(PathStep(PathOperation.closepoly))
        return path_step_list


class RoundRectangle(PathRectangle):
    def __init__(self, center: Vector, width: float, height: float, radius: float, angle=0, **kwargs):
        assert radius > 0
        assert width >= 2 * radius or height >= 2 * radius
        self.radius = radius
        PathRectangle.__init__(self, center, width, height, angle, **kwargs)

    def path_step_generator(self):
        # TODO: Move joint of path into middle point of bottom edge.

        width = self.width
        height = self.height
        radius = self.radius
        angle = self.angle

        corner_offset_matrix = np.array([
            [- width / 2, - height / 2],
            [width / 2, - height / 2],
            [width / 2, height / 2],
            [- width / 2, height / 2]])

        corner_transition_offset_matrix = np.array([
            [0, radius, radius, 0],
            [-radius, 0, 0, radius],
            [0, -radius, -radius, 0],
            [radius, 0, 0, -radius]
        ])
        corner_transition_point_matrix = (
                corner_transition_offset_matrix +
                np.hstack([corner_offset_matrix, corner_offset_matrix])).reshape([-1, 2])
        control_vertex_matrix = rotate_corner_offset_around_center(
            self.center, corner_offset_matrix, angle)
        transition_vertex_matrix = rotate_corner_offset_around_center(
            self.center, corner_transition_point_matrix, angle)

        path_step_list = []
        for edge_index in range(4):
            if edge_index == 0:
                operation = PathOperation.moveto
            else:
                operation = PathOperation.lineto
            path_step_list.append(PathStep(operation, transition_vertex_matrix[edge_index * 2]))
            path_step_list.append(PathStep(
                PathOperation.curve3,
                control_vertex_matrix[edge_index],
                transition_vertex_matrix[edge_index * 2 + 1]))
            if edge_index == 3:
                path_step_list.append(PathStep(PathOperation.lineto, transition_vertex_matrix[0]))
                path_step_list.append(PathStep(PathOperation.closepoly))
        return path_step_list


class Capsule(PathRectangle):
    def __init__(
            self, center: Vector, width: float, height: float, angle=0, cap_on_width=True, **kwargs):
        assert -45 <= angle <= 45
        assert width > 0
        assert height > 0
        self.center = initialize_vector_input(center)
        if cap_on_width:
            assert width > height
        else:
            assert height > width
        self.cap_on_width = cap_on_width
        PathRectangle.__init__(self, center, width, height, angle, **kwargs)

    def path_step_generator(self):
        width = self.width
        height = self.height
        angle = self.angle

        # Plot order (ccw): line_2 -> circle_arc_1 -> line_1 -> circle_arc_2
        if self.cap_on_width:
            center_rectangle_width = width - height
            center_rectangle_height = height
            circle_radius = height / 2
            circle_center_offset1 = Vector(center_rectangle_width / 2, 0)
            circle_degree_1 = (-90, 90)
            circle_center_offset2 = Vector(-center_rectangle_width / 2, 0)
            circle_degree_2 = (90, 270)
            line_offset1 = [
                Vector(center_rectangle_width / 2, center_rectangle_height / 2),
                Vector(-center_rectangle_width / 2, center_rectangle_height / 2)]
            line_offset2 = [
                Vector(-center_rectangle_width / 2, -center_rectangle_height / 2),
                Vector(center_rectangle_width / 2, -center_rectangle_height / 2)]
        else:
            center_rectangle_width = width
            center_rectangle_height = height - width
            circle_radius = width / 2
            circle_center_offset1 = Vector(0, -center_rectangle_height / 2)
            circle_degree_1 = (180, 360)
            circle_center_offset2 = Vector(0, center_rectangle_height / 2)
            circle_degree_2 = (0, 180)
            line_offset1 = [
                Vector(center_rectangle_width / 2, -center_rectangle_height / 2),
                Vector(center_rectangle_width / 2, center_rectangle_height / 2)]
            line_offset2 = [
                Vector(-center_rectangle_width / 2, center_rectangle_height / 2),
                Vector(-center_rectangle_width / 2, -center_rectangle_height / 2)]
        rotate_trans = transforms.Affine2D().rotate_deg(angle)
        line_offset1 = rotate_trans.transform(line_offset1) + self.center
        line_offset2 = rotate_trans.transform(line_offset2) + self.center
        circle_center_offset1 = rotate_trans.transform(circle_center_offset1) + self.center
        circle_center_offset2 = rotate_trans.transform(circle_center_offset2) + self.center

        path_step_list = [
            PathStep(PathOperation.moveto, line_offset2[0]),
            PathStep(PathOperation.lineto, line_offset2[1]),
            *ellipse_arc_obj.generator(
                circle_center_offset1, *circle_degree_1, circle_radius, half_height=None, angle=angle),
            PathStep(PathOperation.lineto, line_offset1[1]),
            *ellipse_arc_obj.generator(
                circle_center_offset2, *circle_degree_2, circle_radius, half_height=None, angle=angle),
            PathStep(PathOperation.closepoly)
        ]
        return path_step_list


class Brace(PathShape):
    def __init__(
            self, head: Vector, left_tail: Vector, right_tail: Vector, radius: float,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        """
                direction  ->
        left_tail \        / right_tail
                   ---  --- main_axis
                      \/
                     head
        radius is the horizontal radius. Vertical radius is determined by distance between head and tail
        """
        assert radius > 0
        self.head = initialize_vector_input(head)
        self.left_tail = initialize_vector_input(left_tail)
        self.right_tail = initialize_vector_input(right_tail)
        self.radius = radius
        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment, reset_vertex_array=False)
        path_step_list = self.path_step_generator()
        PathShape.__init__(self, path_step_list, **kwargs)

    def path_step_generator(self):
        head = self.head
        left_tail = self.left_tail
        right_tail = self.right_tail
        horizontal_radius = self.radius

        vector_between_tails: Vector = right_tail - left_tail
        unit_vector_between_tails = vector_between_tails.unit_vector()
        unit_vector_perpendicular_tails = unit_vector_between_tails.vertical_vector()
        angle = np.rad2deg(np.arccos(unit_vector_between_tails[0]))
        if unit_vector_between_tails[1] < 0:
            angle = -angle

        head_to_tail_intersect_location = calculate_pedal_of_one_point_to_segment_defined_by_two_points(
            left_tail, right_tail, head)
        if (head_to_tail_intersect_location - left_tail) @ (head_to_tail_intersect_location - right_tail) > 0:
            raise ValueError('head should intersect line between two tails')
        vertical_radius = (head_to_tail_intersect_location - head).length / 2
        center = (head_to_tail_intersect_location + head) / 2
        tail_to_main_axis_vector = unit_vector_perpendicular_tails * vertical_radius
        left_tail_to_main_axis_intersect = left_tail - tail_to_main_axis_vector
        right_tail_to_main_axis_intersect = right_tail - tail_to_main_axis_vector
        center_to_left_main_axis_vector = left_tail_to_main_axis_intersect - center
        center_to_right_main_axis_vector = right_tail_to_main_axis_intersect - center
        assert center_to_left_main_axis_vector.length > 2 * horizontal_radius
        assert center_to_right_main_axis_vector.length > 2 * horizontal_radius

        horizontal_radius_vector_between_tails = horizontal_radius * unit_vector_between_tails
        left_tail_arc_center = left_tail + horizontal_radius_vector_between_tails
        left_tail_arc_end = left_tail_to_main_axis_intersect + horizontal_radius_vector_between_tails
        left_tail_arc_path_list = ellipse_arc_obj.generator(
            left_tail_arc_center, -180, -90, horizontal_radius, vertical_radius, angle=angle)
        head_left_arc_start = center - horizontal_radius_vector_between_tails
        left_to_head_straight_line = PathStep(PathOperation.lineto, head_left_arc_start)
        head_left_arc_center = head - horizontal_radius_vector_between_tails
        head_left_arc_path_list = ellipse_arc_obj.generator(
            head_left_arc_center, 90, 0, horizontal_radius, vertical_radius, angle=angle)
        head_right_arc_center = head + horizontal_radius_vector_between_tails
        head_right_arc_path_list = ellipse_arc_obj.generator(
            head_right_arc_center, 180, 90, horizontal_radius, vertical_radius, angle=angle)
        head_right_arc_end = center + horizontal_radius_vector_between_tails
        right_tail_arc_start = right_tail_to_main_axis_intersect - horizontal_radius_vector_between_tails
        head_to_right_straight_line = PathStep(PathOperation.lineto, right_tail_arc_start)
        right_tail_arc_center = right_tail - horizontal_radius_vector_between_tails
        right_tail_arc_path_list = ellipse_arc_obj.generator(
            right_tail_arc_center, -90, 0, horizontal_radius, vertical_radius, angle=angle)

        path_step_list = [
            PathStep(PathOperation.moveto, left_tail),
            *left_tail_arc_path_list,
            left_to_head_straight_line,
            *head_left_arc_path_list,
            *head_right_arc_path_list,
            head_to_right_straight_line,
            *right_tail_arc_path_list,
        ]
        return path_step_list
