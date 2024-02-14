from ..config import LineStyle, FontWeight, ColorConfig, ParameterName, VerticalAlignment, HorizontalAlignment, np, \
    CommonFigureString
from ..config import Vector, Circle, Arrow, Brace, Line

from .axis_diagram import AxisDiagram, Rectangle, AxisDiagramConfig


def generate_arrow_tails_with_shrink_ratio(tail_dot_center, head_dot_center, dots_radius):
    vector1 = head_dot_center - tail_dot_center
    shrink_ratio = (vector1.length - dots_radius) / vector1.length
    updated_head_dot_center = tail_dot_center + vector1 * shrink_ratio
    updated_tail_dot_center = head_dot_center + (tail_dot_center - head_dot_center) * shrink_ratio
    return updated_tail_dot_center, updated_head_dot_center


class ProtocolDiagramConfig(AxisDiagramConfig):
    bound_box_z_order = AxisDiagramConfig.bound_box_z_order
    dash_line_z_order = AxisDiagramConfig.dash_line_z_order
    bound_box_background_order = AxisDiagramConfig.bound_box_background_order
    content_z_order = AxisDiagramConfig.content_z_order
    arrow_z_order = dash_line_z_order
    text_order = AxisDiagramConfig.text_order
    text_config = AxisDiagramConfig.text_config

    initial_solution_color = ColorConfig.random_flux_color_with_alpha
    selected_solution_color = ColorConfig.selected_solution_color
    selected_solution_text_color = ColorConfig.selected_solution_text_color
    averaged_solution_color = ColorConfig.averaged_solution_color
    averaged_solution_text_color = ColorConfig.averaged_solution_text_color
    reoptimized_solution_color = ColorConfig.reoptimized_solution_color
    reoptimized_solution_text_color = ColorConfig.reoptimized_solution_text_color

    common_edge_width = 7
    common_edge_config = {
        **AxisDiagramConfig.edge_config,
        ParameterName.edge_width: common_edge_width,
    }
    bound_box_config = {
        **common_edge_config,
        ParameterName.z_order: bound_box_z_order,
        ParameterName.edge_color: ColorConfig.normal_blue
    }
    dash_line_config = {
        **common_edge_config,
        ParameterName.z_order: dash_line_z_order,
        # ParameterName.edge_color: ColorConfig.medium_blue,
        ParameterName.edge_style: LineStyle.thin_dash,
    }
    selected_dashed_line_config = {
        **dash_line_config,
        ParameterName.edge_color: selected_solution_color,
    }
    arrow_line_config = {
        ParameterName.stem_width: 0.008,
        ParameterName.head_width: 0.032,
        ParameterName.head_len_width_ratio: 1,
        ParameterName.tail_arrow: True,
        ParameterName.head_arrow: True,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.medium_orange,
        ParameterName.z_order: content_z_order
    }
    brace_config = {
        **common_edge_config,
        # ParameterName.edge_color: ColorConfig.normal_blue,
        ParameterName.z_order: content_z_order,
        ParameterName.radius: 0.05,
        ParameterName.edge_width: 5
    }
    initial_brace_config = {
        **brace_config,
        ParameterName.edge_color: initial_solution_color
    }
    selected_brace_config = {
        **brace_config,
        ParameterName.edge_color: selected_solution_color
    }
    brace_height = 0.05
    label_text_font_size = 45
    label_text_config = {
        **text_config,
        ParameterName.font_size: label_text_font_size,
    }
    sub_title_text_config = {
        **text_config,
        ParameterName.font_size: 40,
    }
    brace_text_config = {
        **text_config,
        ParameterName.font_size: 35,
    }

    dots_text_font_size = 40
    dots_text_height = 0.1
    dots_text_config = {
        **text_config,
        ParameterName.font_size: dots_text_font_size,
        ParameterName.width: 0.2,
        ParameterName.height: dots_text_height,
        ParameterName.font_weight: FontWeight.bold,
    }
    selected_text_config = {
        **dots_text_config,
        # ParameterName.font_color: ColorConfig.normal_blue,
        ParameterName.font_color: selected_solution_text_color,
    }
    averaged_text_config = {
        **dots_text_config,
        ParameterName.font_color: averaged_solution_text_color
    }
    known_flux_text_config = {
        **dots_text_config,
        ParameterName.font_color: ColorConfig.normal_blue,
    }
    reoptimized_text_color = {
        **dots_text_config,
        ParameterName.font_color: reoptimized_solution_text_color,
    }

    dots_radius = 0.02
    loss_dots_config = {
        ParameterName.radius: dots_radius,
        # ParameterName.face_color: ColorConfig.normal_blue,
        ParameterName.edge_width: None,
        ParameterName.z_order: content_z_order,
    }
    initial_loss_dots_config = {
        **loss_dots_config,
        # ParameterName.face_color: ColorConfig.normal_blue
        ParameterName.face_color: ColorConfig.random_flux_color_with_alpha
    }
    selected_loss_dots_config = {
        **loss_dots_config,
        ParameterName.face_color: selected_solution_color
    }
    unselected_loss_docts_config = {
        **loss_dots_config,
        ParameterName.face_color: ColorConfig.gray,
    }
    average_dots_config = {
        **loss_dots_config,
        # ParameterName.face_color: ColorConfig.dark_blue,
        ParameterName.face_color: averaged_solution_color
    }

    known_flux_vertical_line_config = {
        **dash_line_config,
        ParameterName.edge_color: ColorConfig.medium_orange,
    }
    average_vertical_line_config = {
        **common_edge_config,
        ParameterName.z_order: dash_line_z_order,
        ParameterName.edge_color: ColorConfig.medium_blue,
        ParameterName.edge_width: common_edge_width - 2
    }
    error_bar_cap_len = 0.2
    error_bar_line_config = {
        **common_edge_config,
        ParameterName.edge_width: common_edge_width * 0.1,
        ParameterName.edge_color: ColorConfig.normal_blue,
        ParameterName.z_order: dash_line_z_order,
    }

    heatmap_square_color_list = [
        ColorConfig.light_bright_orange,
        # ColorConfig.slightly_light_orange,
        ColorConfig.medium_bright_orange,
        ColorConfig.light_bright_blue,
        ColorConfig.light_medium_bright_blue,
        ColorConfig.medium_bright_blue,
        # ColorConfig.normal_blue,
    ]
    heatmap_square_config = {
        ParameterName.edge_width: None,
        ParameterName.z_order: content_z_order,
    }
    mean_heatmap_square_color_index_list = [
        [3, 1, 3, 0],
        [0, 4, 2, 1],
        [1, 0, 4, 0],
        [2, 4, 3, 1],
    ]
    std_heatmap_square_color_index_list = [
        [0, 3, 0, 1],
        [2, 1, 4, 2],
        [0, 4, 0, 1],
        [3, 1, 3, 0],
    ]
    sensitivity_heatmap_square_color_index_list = [
        [0, 4, 2, 4, 3, 0, 2, 1],
        [1, 3, 0, 1, 0, 1, 0, 2],
        [3, 0, 2, 4, 1, 3, 1, 4],
        [2, 4, 1, 2, 0, 4, 2, 3],
        # [1, 3, 2, 0, 4, 2, 1, 4],
    ]

    @staticmethod
    def calculate_center(self, scale, *args):
        size = args[0]
        assert isinstance(size, Vector)
        _, total_size = self.calculate_box_and_total_size(size)
        return total_size / 2 * scale


class ProtocolDiagram(AxisDiagram):
    def __init__(self, *args, config_class=ProtocolDiagramConfig, **kwargs):
        super().__init__(config_class, *args, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) / 2 * scale


class InitialDistributionDiagram(ProtocolDiagram):
    class Config(ProtocolDiagramConfig):
        bound_box_config = {
            **ProtocolDiagramConfig.bound_box_config,
            ParameterName.edge_width: None
        }

    total_width = 0.4
    total_height = 0.6
    height_to_width_ratio = total_height / total_width
    box_size = Vector(total_width, 0.4)
    box_bottom_left = Vector(0, 0)

    def __init__(self, **kwargs):
        sample_coordinate_list = [
            Vector(0.25952305, 0.68329664),
            Vector(0.16167916, 0.27399579),
            Vector(0.50768284, 0.51133309),
            Vector(0.73458929, 0.75),
            Vector(0.83299338, 0.88164381),
            Vector(0.93613044, 0.39480171),
            Vector(0.33271919, 0.17907892),
        ]
        box_width = self.box_size.x
        box_height = self.box_size.y

        flux_dot_list = []
        initial_dots_config = ProtocolDiagramConfig.initial_loss_dots_config
        for sample_coordinate in sample_coordinate_list:
            sample_real_location = self.box_transform(sample_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **initial_dots_config,
                ParameterName.center: sample_real_location,
            }))
        box_center_x = self.box_transform(raw_x=0.5)
        brace_tail_y = box_height + -0.01
        brace_head_y = box_height + ProtocolDiagramConfig.brace_height
        brace_left = self.box_transform(raw_x=0)
        brace_right = self.box_transform(raw_x=1)
        text_bottom = brace_head_y + 0
        flux_dot_list.append(Brace(**{
            **ProtocolDiagramConfig.initial_brace_config,
            ParameterName.head: Vector(box_center_x, brace_head_y),
            ParameterName.right_tail: Vector(brace_left, brace_tail_y),
            ParameterName.left_tail: Vector(brace_right, brace_tail_y),
        }))
        selected_text_height = ProtocolDiagramConfig.dots_text_height
        text_config_list = [
            {
                **ProtocolDiagramConfig.brace_text_config,
                ParameterName.string: CommonFigureString.initial_points,
                ParameterName.center: Vector(
                    box_center_x,
                    text_bottom + selected_text_height / 2),
                ParameterName.width: box_width,
                ParameterName.height: selected_text_height,
            },
        ]
        super().__init__(
            flux_dot_list, config_class=self.Config,
            text_config_list=text_config_list, **kwargs)


class LossDistributionDiagramConfig(object):
    # total_loss_dot_loc_list = [0.2, 0.45, 0.6, 0.73, 0.8, 0.85, 0.92]
    total_loss_dot_loc_list = [0.13, 0.23, 0.41, 0.58, 0.71, 0.85, 0.92]
    total_text_list = ['A', 'B', None, None, None, 'C', None]
    total_num = len(total_loss_dot_loc_list)
    normal_select_num = 3
    best_select_num = 1
    selected_loss_dot_loc_list = [0.2, 0.45, 0.6]
    selected_text_list = ['A', 'B', None]
    unselected_loss_dot_loc_list = [0.73, 0.8, 0.85, 0.92]
    unselected_text_list = [None, None, 'C', None]
    euclidean_distance_y_loc_list = [
        0.42464251, 0.68927921, 0.84231319, 0.13923709,
        0.20687409, 0.9212252]
    relative_error_y_loc_list = [
        0.54071287, 0.09208063, 0.66914014, 0.12797837,
        0.28899508, 0.38628004]
    # selected_color = ColorConfig.normal_blue
    selected_color = ProtocolDiagramConfig.selected_solution_color
    selected_text_color = ProtocolDiagramConfig.selected_solution_text_color
    unselected_color = ColorConfig.gray

    @staticmethod
    def add_loss_dot_and_text(
            loss_dot_loc_list, text_str_list, box_size, common_loss_dot_loc, common_text_loc,
            color, text_color, loss_dot_list, loss_dots_config, text_config_list, common_text_config,
            horizontal_or_vertical):
        for dot_loc, text_string in zip(loss_dot_loc_list, text_str_list):
            if horizontal_or_vertical == ParameterName.vertical:
                real_loc = dot_loc * box_size.y
                loss_dot_center = Vector(common_loss_dot_loc, real_loc)
                text_center = Vector(common_text_loc, real_loc)
            elif horizontal_or_vertical == ParameterName.horizontal:
                real_loc = dot_loc * box_size.x
                loss_dot_center = Vector(real_loc, common_loss_dot_loc)
                text_center = Vector(real_loc, common_text_loc)
            else:
                raise ValueError()
            loss_dot_list.append(Circle(**{
                **loss_dots_config,
                ParameterName.face_color: color,
                ParameterName.center: loss_dot_center,
            }))
            if text_string is not None:
                text_config_list.append({
                    **common_text_config,
                    ParameterName.string: text_string,
                    ParameterName.font_color: text_color,
                    ParameterName.center: text_center,
                })

    @staticmethod
    def draw_selected_or_unselected_loss_diagram(
            total_loss_dot_loc_list, total_text_list, select_num,
            box_size, common_loss_dot_loc, common_text_loc, loss_dot_list, loss_dots_config,
            text_config_list, selected_text_config, horizontal_or_vertical):
        selected_loss_dot_loc_list = total_loss_dot_loc_list[:select_num]
        unselected_loss_dot_loc_list = total_loss_dot_loc_list[select_num:]
        min_selected_loss_loc = min(selected_loss_dot_loc_list)
        max_selected_loss_loc = max(selected_loss_dot_loc_list)
        selected_text_list = total_text_list[:select_num]
        unselected_text_list = total_text_list[select_num:]
        LossDistributionDiagramConfig.add_loss_dot_and_text(
            selected_loss_dot_loc_list, selected_text_list, box_size,
            common_loss_dot_loc, common_text_loc,
            LossDistributionDiagramConfig.selected_color, LossDistributionDiagramConfig.selected_text_color,
            loss_dot_list, loss_dots_config,
            text_config_list, selected_text_config, horizontal_or_vertical)
        unselected_dot_color = LossDistributionDiagramConfig.unselected_color
        LossDistributionDiagramConfig.add_loss_dot_and_text(
            unselected_loss_dot_loc_list, unselected_text_list, box_size,
            common_loss_dot_loc, common_text_loc,
            unselected_dot_color, unselected_dot_color, loss_dot_list, loss_dots_config,
            text_config_list, selected_text_config, horizontal_or_vertical)
        if len(selected_loss_dot_loc_list) == 1:
            return selected_loss_dot_loc_list[0], None
        else:
            return min_selected_loss_loc, max_selected_loss_loc


class LossDistributionDiagram(ProtocolDiagram):
    total_width = 0.33
    total_height = 1.2
    height_to_width_ratio = total_height / total_width
    box_size = Vector(total_width - 0.1, total_height)
    box_bottom_left = Vector(0.1, 0)

    @staticmethod
    def _total_width_height(mode, height):
        if mode == ParameterName.loss_data:
            total_width = 0.4
        elif mode == ParameterName.net_euclidean_distance or mode == ParameterName.flux_relative_distance:
            total_width = 0.3
        else:
            raise ValueError()
        if height == ParameterName.normal:
            total_height = 1.2
        elif height == ParameterName.low_height:
            total_height = 1
        else:
            raise ValueError()
        return total_width, total_height

    @staticmethod
    def calculate_center(self, scale, mode=ParameterName.loss_data, height=ParameterName.normal, *args):
        total_width, total_height = self._total_width_height(mode, height)
        return Vector(total_width, total_height) / 2 * scale

    def __init__(self, selected=False, mode=ParameterName.loss_data, height=ParameterName.normal, **kwargs):
        total_loss_dot_y_loc_list = LossDistributionDiagramConfig.total_loss_dot_loc_list
        total_text_list = LossDistributionDiagramConfig.total_text_list
        euclidean_distance_y_loc_list = LossDistributionDiagramConfig.euclidean_distance_y_loc_list
        relative_error_y_loc_list = LossDistributionDiagramConfig.relative_error_y_loc_list
        total_width, total_height = self._total_width_height(mode, height)
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = self.total_height / total_width
        self.box_size = Vector(total_width - 0.1, self.total_height)

        common_loss_dot_x_loc = self.box_transform(raw_x=0.4)
        common_text_x_loc = self.box_transform(raw_x=0.2)
        common_central_dot_x_loc = self.box_transform(raw_x=0.5)
        box_width = self.box_size.x
        box_height = self.box_size.y
        box_left = self.box_bottom_left.x
        left_label_distance = 0.05
        brace_width = ProtocolDiagramConfig.brace_height
        brace_tail_x = self.box_transform(raw_x=0.52)
        # brace_head_x = self.box_transform(raw_x=0.7)
        brace_head_x = brace_tail_x + brace_width
        brace_text_center_x = self.box_transform(raw_x=0.9)

        if mode == ParameterName.loss_data:
            # y_label = r'Final loss $\mathbf{L^*}$'
            y_label = CommonFigureString.final_loss_with_equation_bold
        elif mode == ParameterName.net_euclidean_distance:
            # y_label = 'Euclidean distance'
            y_label = CommonFigureString.euclidean_distance
        elif mode == ParameterName.flux_relative_distance:
            # y_label = 'Relative error'
            y_label = CommonFigureString.relative_error
        else:
            raise ValueError()
        text_config_list = [{
            **ProtocolDiagramConfig.label_text_config,
            ParameterName.string: y_label,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.vertical_alignment: VerticalAlignment.baseline,
            ParameterName.horizontal_alignment: HorizontalAlignment.center,
            ParameterName.center: Vector(
                (box_left - left_label_distance) / 2,
                self.box_transform(raw_y=0.5 * box_height / box_width)),
            ParameterName.width: box_height,
            ParameterName.height: box_left - left_label_distance,
            ParameterName.angle: 90,
        }, ]

        dots_text_config = {
            **ProtocolDiagramConfig.dots_text_config,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            ParameterName.horizontal_alignment: HorizontalAlignment.center,
            # ParameterName.font_color: ColorConfig.normal_blue,
            ParameterName.width: 0.2,
            ParameterName.height: 0.1,
        }
        loss_dot_list = []
        initial_loss_dots_config = ProtocolDiagramConfig.initial_loss_dots_config
        if mode == ParameterName.loss_data:
            if selected:
                select_num = LossDistributionDiagramConfig.normal_select_num
                brace_text_string = CommonFigureString.m_selected_solutions
            else:
                select_num = LossDistributionDiagramConfig.total_num
                brace_text_string = CommonFigureString.n_optimized_solutions
            raw_min_selected_y_loc, raw_max_selected_y_loc = \
                LossDistributionDiagramConfig.draw_selected_or_unselected_loss_diagram(
                    total_loss_dot_y_loc_list, total_text_list, select_num,
                    self.box_size, common_loss_dot_x_loc, common_text_x_loc, loss_dot_list, initial_loss_dots_config,
                    text_config_list, dots_text_config, ParameterName.vertical)
            min_selected_y_loc = self.box_transform(raw_y=raw_min_selected_y_loc * box_height / box_width)
            max_selected_y_loc = self.box_transform(raw_y=raw_max_selected_y_loc * box_height / box_width)
            head_y = (min_selected_y_loc + max_selected_y_loc) / 2
            brace_config = {
                **ProtocolDiagramConfig.selected_brace_config,
                ParameterName.head: Vector(brace_head_x, head_y),
                ParameterName.right_tail: Vector(brace_tail_x, max_selected_y_loc),
                ParameterName.left_tail: Vector(brace_tail_x, min_selected_y_loc),
            }
            text_center = Vector(brace_text_center_x, head_y)
            loss_dot_list.append(Brace(**brace_config))
            text_config_list.append(
                {
                    **ProtocolDiagramConfig.brace_text_config,
                    ParameterName.string: brace_text_string,
                    ParameterName.center: text_center,
                    ParameterName.width: box_height,
                    ParameterName.vertical_alignment: VerticalAlignment.top,
                    ParameterName.height: ProtocolDiagramConfig.dots_text_height,
                    ParameterName.angle: 90,
                    ParameterName.text_box: False,
                }
            )
        elif mode == ParameterName.net_euclidean_distance or mode == ParameterName.flux_relative_distance:
            if mode == ParameterName.net_euclidean_distance:
                loss_dot_y_loc_list = euclidean_distance_y_loc_list
            elif mode == ParameterName.flux_relative_distance:
                loss_dot_y_loc_list = relative_error_y_loc_list
            else:
                raise ValueError()
            for dot_y_loc in loss_dot_y_loc_list:
                real_y_loc = dot_y_loc * self.box_size.y
                loss_dot_list.append(Circle(**{
                    **initial_loss_dots_config,
                    ParameterName.center: Vector(common_central_dot_x_loc, real_y_loc),
                }))
        # y_tick_loc_list = np.linspace(0.03, 0.97, 6) * self.box_size.y
        y_tick_loc_list = []

        super().__init__(
            loss_dot_list, y_tick_list=y_tick_loc_list, text_config_list=text_config_list, **kwargs)


class HorizontalLossDistributionDiagram(ProtocolDiagram):
    total_width = 1.2
    total_height = 0.4
    bottom_boundary = 0.1
    height_to_width_ratio = total_height / total_width
    box_size = Vector(total_width, total_height - bottom_boundary)
    box_bottom_left = Vector(0, bottom_boundary)

    def __init__(self, selected=False, **kwargs):
        box_width, box_height = self.box_size
        box_bottom = self.box_bottom_left.y
        total_loss_dot_x_loc_list = LossDistributionDiagramConfig.total_loss_dot_loc_list
        total_text_list = LossDistributionDiagramConfig.total_text_list
        common_loss_dot_y_loc = self.box_transform(raw_y=0.4 * box_height / box_width)
        common_text_y_loc = self.box_transform(raw_y=0.2 * box_height / box_width)
        brace_tail_y = self.box_transform(raw_y=0.52 * box_height / box_width)
        # brace_head_y = self.box_transform(raw_y=0.7 * box_height / box_width)
        brace_head_y = brace_tail_y + ProtocolDiagramConfig.brace_height
        text_center_y = self.box_transform(raw_y=0.82 * box_height / box_width)
        brace_left = self.box_transform(raw_x=min(total_loss_dot_x_loc_list))
        brace_right = self.box_transform(raw_x=max(total_loss_dot_x_loc_list))
        best_solution_x_loc = brace_left
        head_x = (brace_left + brace_right) / 2
        axis_label_distance = 0.03

        final_loss_str = CommonFigureString.final_loss_with_equation_bold
        loss_dot_list = []
        text_config_list = [
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: final_loss_str,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (box_bottom - axis_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: box_bottom - axis_label_distance,
            },
        ]
        dots_text_config = {
            **ProtocolDiagramConfig.dots_text_config,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            ParameterName.horizontal_alignment: HorizontalAlignment.center,
            ParameterName.font_color: ColorConfig.normal_blue,
            ParameterName.width: 0.2,
            ParameterName.height: 0.1,
        }
        initial_loss_dots_config = ProtocolDiagramConfig.initial_loss_dots_config

        if selected:
            select_num = LossDistributionDiagramConfig.best_select_num
            brace_text_string = CommonFigureString.best_solution
            text_center = Vector(best_solution_x_loc + 0.05, text_center_y)
            loss_dot_list.append(Line(**{
                **ProtocolDiagramConfig.selected_brace_config,
                ParameterName.start: Vector(best_solution_x_loc, brace_head_y),
                ParameterName.end: Vector(best_solution_x_loc, brace_tail_y),
            }))
        else:
            select_num = LossDistributionDiagramConfig.total_num
            loss_dot_list.append(Brace(**{
                **ProtocolDiagramConfig.selected_brace_config,
                ParameterName.head: Vector(head_x, brace_head_y),
                ParameterName.right_tail: Vector(brace_left, brace_tail_y),
                ParameterName.left_tail: Vector(brace_right, brace_tail_y),
            }))
            brace_text_string = CommonFigureString.n_optimized_solutions
            text_center = Vector(head_x, text_center_y)

        LossDistributionDiagramConfig.draw_selected_or_unselected_loss_diagram(
            total_loss_dot_x_loc_list, total_text_list, select_num,
            self.box_size, common_loss_dot_y_loc, common_text_y_loc, loss_dot_list, initial_loss_dots_config,
            text_config_list, dots_text_config, ParameterName.horizontal)

        text_config_list.append(
            {
                **ProtocolDiagramConfig.brace_text_config,
                ParameterName.string: brace_text_string,
                ParameterName.center: text_center,
                ParameterName.width: box_width,
                ParameterName.height: ProtocolDiagramConfig.dots_text_height,
            }
        )

        super().__init__(
            loss_dot_list, text_config_list=text_config_list, **kwargs)


class AverageDiagram(ProtocolDiagram):
    total_width = 0.9
    total_height = 0.9
    height_to_width_ratio = total_height / total_width
    box_size = Vector(0.8, 0.7)
    box_bottom_left = Vector(0.1, 0.1)

    def __init__(self, mode=ParameterName.simulated, **kwargs):
        sample_coordinate_list = [
            Vector(0.2, 0.15),
            Vector(0.65, 0.1),
            Vector(0.7, 0.75),
            Vector(0.8, 0.35),
        ]
        average_coordinate = np.mean(sample_coordinate_list, axis=0)
        known_flux_coordinate = Vector(0.4, 0.55)
        reoptimized_solution_coordinate = Vector(0.45, 0.59)
        dots_radius = ProtocolDiagramConfig.dots_radius
        box_width = self.box_size.x
        box_height = self.box_size.y
        box_left = self.box_bottom_left.x
        total_width = self.total_width
        left_label_distance = 0.05

        if mode == ParameterName.simulated:
            title_string = 'Euclidean distance'
        elif (
                mode == ParameterName.sensitivity or mode == ParameterName.experimental
                or mode == ParameterName.simulated_reoptimization):
            title_string = 'Average of selected solutions'
        elif mode == ParameterName.optimization_from_average_solutions:
            title_string = 'Optimization'
        else:
            raise ValueError()
        title_height = 0.1
        boundary_width = 0.1
        axis_label_distance = 0.02
        text_config_list = [
            {
                **ProtocolDiagramConfig.sub_title_text_config,
                ParameterName.string: title_string,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.left,
                ParameterName.center: Vector(total_width / 2, boundary_width + box_height + title_height / 2),
                ParameterName.width: total_width,
                ParameterName.height: title_height,
            },
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: 'Flux 1',
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (boundary_width - axis_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: boundary_width - axis_label_distance,
            },
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: 'Flux 2',
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    (boundary_width - axis_label_distance) / 2,
                    self.box_transform(raw_y=0.5 * box_height / box_width)),
                ParameterName.width: box_height,
                ParameterName.height: boundary_width - axis_label_distance,
                ParameterName.angle: 90,
            },
        ]

        flux_dot_list = []
        line_config_list = []
        average_real_location = self.box_transform(average_coordinate, inplace=False)
        selected_text_config = ProtocolDiagramConfig.selected_text_config
        if mode != ParameterName.optimization_from_average_solutions:
            for sample_coordinate in sample_coordinate_list:
                sample_real_location = self.box_transform(sample_coordinate, inplace=False)
                flux_dot_list.append(Circle(**{
                    **ProtocolDiagramConfig.selected_loss_dots_config,
                    ParameterName.center: sample_real_location,
                }))
                line_config_list.append({
                    **ProtocolDiagramConfig.selected_dashed_line_config,
                    ParameterName.start: average_real_location,
                    ParameterName.end: sample_real_location
                })
            text_config_list.extend([
                {
                    **selected_text_config,
                    ParameterName.string: 'A',
                    ParameterName.center: self.box_transform(sample_coordinate_list[0], inplace=False) + Vector(-0.05, 0),
                },
                {
                    **selected_text_config,
                    ParameterName.string: 'B',
                    ParameterName.center: self.box_transform(sample_coordinate_list[2], inplace=False) + Vector(0.05, 0),
                }
            ])
        flux_dot_list.append(Circle(**{
            **ProtocolDiagramConfig.average_dots_config,
            ParameterName.center: average_real_location,
        }))
        text_config_list.append(
            {
                **ProtocolDiagramConfig.averaged_text_config,
                ParameterName.string: 'Average',
                ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size - 5,
                ParameterName.center: average_real_location + Vector(-0.13, 0.01),
                ParameterName.horizontal_alignment: HorizontalAlignment.right,
            }
        )
        if mode == ParameterName.simulated or mode == ParameterName.sensitivity:
            known_real_location = self.box_transform(known_flux_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **ProtocolDiagramConfig.initial_loss_dots_config,
                ParameterName.face_color: ColorConfig.slightly_light_orange,
                ParameterName.center: known_real_location,
            }))
            text_config_list.append(
                {
                    **ProtocolDiagramConfig.known_flux_text_config,
                    ParameterName.string: CommonFigureString.known_flux,
                    ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size + 10,
                    ParameterName.center: known_real_location + Vector(-0.05, 0),
                }
            )
            if mode == ParameterName.simulated:
                # vector1 = known_real_location - average_real_location
                # shrink_ratio = (vector1.length - dots_radius) / vector1.length
                # updated_known_real_location = average_real_location + vector1 * shrink_ratio
                # updated_average_real_location = known_real_location + \
                #                                 (average_real_location - known_real_location) * shrink_ratio
                updated_known_real_location, updated_average_real_location = generate_arrow_tails_with_shrink_ratio(
                    known_real_location, average_real_location, dots_radius)
                flux_dot_list.append(
                    Arrow(**{
                        **ProtocolDiagramConfig.arrow_line_config,
                        ParameterName.tail: updated_known_real_location,
                        ParameterName.head: updated_average_real_location,
                    }))
        elif mode == ParameterName.optimization_from_average_solutions:
            reoptimized_solution_real_location = self.box_transform(reoptimized_solution_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **ProtocolDiagramConfig.loss_dots_config,
                ParameterName.face_color: ColorConfig.reoptimized_solution_color,
                ParameterName.center: reoptimized_solution_real_location,
            }))
            text_config_list.append(
                {
                    **ProtocolDiagramConfig.reoptimized_text_color,
                    ParameterName.string: CommonFigureString.reoptimized_solution_wrap,
                    ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size - 5,
                    ParameterName.center: reoptimized_solution_real_location + Vector(-0.03, 0.09),
                }
            )
            updated_average_real_location, updated_reoptimized_solution_real_location = generate_arrow_tails_with_shrink_ratio(
                average_real_location, reoptimized_solution_real_location, dots_radius)
            flux_dot_list.append(
                Arrow(**{
                    **ProtocolDiagramConfig.arrow_line_config,
                    ParameterName.tail_arrow: False,
                    ParameterName.face_color: ColorConfig.reoptimized_solution_color,
                    ParameterName.tail: updated_average_real_location,
                    ParameterName.head: updated_reoptimized_solution_real_location,
                }))
        super().__init__(
            flux_dot_list, line_config_list=line_config_list, text_config_list=text_config_list, **kwargs)


class HorizontalComparisonDiagram(ProtocolDiagram):
    total_width = 0.9
    total_height = 0.4
    height_to_width_ratio = total_height / total_width
    box_size = Vector(0.8, 0.15)
    box_bottom_left = Vector(0.1, 0.1)

    @staticmethod
    def calculate_box_and_total_size(title_string=None):
        box_size = HorizontalComparisonDiagram.box_size
        if title_string is not None:
            total_size = box_size + Vector(0.1, 0.2)
        else:
            total_size = box_size + Vector(0.1, 0.1)
        return total_size

    def __init__(
            self, average_flux_value, title_string=None, flux_index=1,
            standard_deviation=None, known_flux_value=None, mode=ParameterName.simulated, **kwargs):
        box_width = self.box_size.x
        box_height = self.box_size.y
        total_size = self.calculate_box_and_total_size(title_string)
        box_left = self.box_bottom_left.x
        total_width, total_height = total_size
        self.total_width, self.total_height = total_size
        selected_text_height = ProtocolDiagramConfig.dots_text_height

        # if mode == ParameterName.simulated or mode == ParameterName.sensitivity:
        #     title_string = 'Relative error'
        # elif mode == ParameterName.experimental:
        #     title_string = 'Mean and standard deviation of each flux'
        # else:
        #     raise ValueError()
        title_height = 0.1
        boundary_width = 0.1
        axis_label_distance = 0.02
        text_config_list = [
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: f'Flux {flux_index}',
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (boundary_width - axis_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: boundary_width - axis_label_distance,
            },
        ]
        if title_string is not None:
            text_config_list.append({
                **ProtocolDiagramConfig.sub_title_text_config,
                ParameterName.string: title_string,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.left,
                ParameterName.center: Vector(total_width / 2, boundary_width + box_height + title_height / 2),
                ParameterName.width: total_width,
                ParameterName.height: title_height,
            })

        figure_content_list = []
        line_config_list = []
        if mode == ParameterName.simulated or mode == ParameterName.sensitivity:
            assert known_flux_value is not None
            known_flux_end_location = self.box_transform(Vector(known_flux_value, box_height / box_width))
            known_flux_line_config = {
                **ProtocolDiagramConfig.known_flux_vertical_line_config,
                ParameterName.start: self.box_transform(Vector(known_flux_value, 0)),
                ParameterName.end: known_flux_end_location
            }
            known_flux_text_config = {
                **ProtocolDiagramConfig.known_flux_text_config,
                ParameterName.string: CommonFigureString.known_flux,
                ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size + 5,
                ParameterName.center: known_flux_end_location + Vector(0, selected_text_height / 2 + 0.01),
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
            }
            average_end_location = self.box_transform(Vector(average_flux_value, box_height / box_width))
            average_line_config = {
                **ProtocolDiagramConfig.average_vertical_line_config,
                ParameterName.start: self.box_transform(Vector(average_flux_value, 0)),
                ParameterName.end: average_end_location
            }
            average_text_config = {
                **ProtocolDiagramConfig.averaged_text_config,
                ParameterName.string: 'Average',
                ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size - 5,
                ParameterName.center: average_end_location + Vector(0, selected_text_height / 2 + 0.02),
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
            }
            arrow_relative_location = 0.3
            distance_arrow_config = {
                **ProtocolDiagramConfig.arrow_line_config,
                ParameterName.tail: self.box_transform(
                    Vector(known_flux_value, arrow_relative_location * box_height / box_width)),
                ParameterName.head: self.box_transform(
                    Vector(average_flux_value, arrow_relative_location * box_height / box_width)),
            }
            distance_text_relative_location = 0.45
            distance_text_loc = self.box_transform(Vector(
                (known_flux_value + average_flux_value) / 2,
                distance_text_relative_location * box_height / box_width)) + \
                Vector(0, selected_text_height / 2 + 0.01)
            distance_ratio = 100 * (average_flux_value - known_flux_value) / known_flux_value
            distance_text_config = {
                **ProtocolDiagramConfig.selected_text_config,
                ParameterName.string: 'e.g. {}{:.0f}%'.format(
                    '+' if distance_ratio > 0 else '', distance_ratio),
                ParameterName.font_size: ProtocolDiagramConfig.dots_text_font_size - 15,
                ParameterName.center: distance_text_loc,
                ParameterName.font_color: ColorConfig.orange,
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
            }
            line_config_list.extend([known_flux_line_config, average_line_config])
            figure_content_list.append(Arrow(**distance_arrow_config))
            text_config_list.extend([known_flux_text_config, average_text_config, distance_text_config])
        elif mode == ParameterName.experimental:
            figure_content_list.append(Circle(**{
                **ProtocolDiagramConfig.average_dots_config,
                ParameterName.center: self.box_transform(Vector(average_flux_value, 0.5 * box_height / box_width)),
            }))
            if standard_deviation is not None:
                error_bar_cap_half_len = ProtocolDiagramConfig.error_bar_cap_len / 2
                error_bar_horizontal_start_x_loc = self.box_transform(raw_x=average_flux_value - standard_deviation)
                error_bar_horizontal_end_x_loc = self.box_transform(raw_x=average_flux_value + standard_deviation)
                error_bar_middle_y_loc = self.box_transform(
                    raw_y=0.5 * box_height / box_width)
                error_bar_bottom_y_loc = self.box_transform(
                    raw_y=(0.5 - error_bar_cap_half_len) * box_height / box_width)
                error_bar_top_y_loc = self.box_transform(
                    raw_y=(0.5 + error_bar_cap_half_len) * box_height / box_width)
                line_config_list.extend([
                    {
                        **ProtocolDiagramConfig.error_bar_line_config,
                        ParameterName.start: Vector(error_bar_horizontal_start_x_loc, error_bar_middle_y_loc),
                        ParameterName.end: Vector(error_bar_horizontal_end_x_loc, error_bar_middle_y_loc),
                    },
                    {
                        **ProtocolDiagramConfig.error_bar_line_config,
                        ParameterName.start: Vector(error_bar_horizontal_start_x_loc, error_bar_bottom_y_loc),
                        ParameterName.end: Vector(error_bar_horizontal_start_x_loc, error_bar_top_y_loc),
                    },
                    {
                        **ProtocolDiagramConfig.error_bar_line_config,
                        ParameterName.start: Vector(error_bar_horizontal_end_x_loc, error_bar_bottom_y_loc),
                        ParameterName.end: Vector(error_bar_horizontal_end_x_loc, error_bar_top_y_loc),
                    },
                ])
        else:
            raise ValueError()
        super().__init__(
            figure_content_list, line_config_list=line_config_list, text_config_list=text_config_list, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        title_string = args[0]
        return self.calculate_box_and_total_size(title_string) / 2 * scale


class HeatmapDiagram(ProtocolDiagram):
    square_edge = 0.1
    square_unit_size = Vector(square_edge, square_edge)
    box_bottom_left = Vector(0.1, 0.1)

    @staticmethod
    def calculate_box_and_total_size(size: Vector):
        box_size = np.flip(size * HeatmapDiagram.square_unit_size)
        total_size = box_size + HeatmapDiagram.box_bottom_left + Vector(0, 0.1)
        return box_size, total_size

    @staticmethod
    def calculate_center(self, scale, *args):
        title_string = args[0]
        _, total_size = self.calculate_box_and_total_size(title_string)
        return total_size / 2 * scale

    def __init__(self, size, mean_or_std=ParameterName.mean, mode=ParameterName.simulated, **kwargs):
        box_size, total_size = self.calculate_box_and_total_size(size)
        total_width, total_height = total_size
        self.total_width, self.total_height = total_size
        box_width, box_height = box_size
        self.box_size = box_size

        title_height = 0.1
        boundary_width = self.box_bottom_left.x
        axis_label_distance = 0.03
        square_edge = self.square_edge
        if mode == ParameterName.simulated:
            # x_label = f'${CommonFigureString.math_m}$'
            # y_label = f'${CommonFigureString.math_n}$'
            x_label = CommonFigureString.bold_optimization_size_n
            y_label = CommonFigureString.bold_selection_size_m
            if mean_or_std == ParameterName.mean:
                title_string = CommonFigureString.mean
            elif mean_or_std == ParameterName.std:
                title_string = CommonFigureString.std
            else:
                raise ValueError()
            special_config = {}
            center_y_loc = boundary_width + box_height + title_height / 2
        elif mode == ParameterName.sensitivity:
            title_string = 'Relative error of fluxes\nunder perturbations'
            x_label = 'Flux'
            y_label = 'Perturbations'
            special_config = {ParameterName.font_size: ProtocolDiagramConfig.label_text_font_size - 10}
            center_y_loc = boundary_width + box_height + title_height / 2 + 0.05
        else:
            raise ValueError()
        current_ax_label_font_size = ProtocolDiagramConfig.label_text_font_size - 15
        text_config_list = [
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: title_string,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.left,
                ParameterName.center: Vector(total_width / 2, center_y_loc),
                ParameterName.width: total_width,
                ParameterName.height: title_height,
            },
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: x_label,
                ParameterName.font_size: current_ax_label_font_size,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (boundary_width - axis_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: boundary_width - axis_label_distance,
            },
            {
                **ProtocolDiagramConfig.label_text_config,
                ParameterName.string: y_label,
                ParameterName.font_size: current_ax_label_font_size,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    (boundary_width - axis_label_distance) / 2,
                    self.box_transform(raw_y=0.5 * box_height / box_width)),
                ParameterName.width: box_height,
                ParameterName.height: boundary_width - axis_label_distance,
                ParameterName.angle: 90,
                **special_config,
            },
        ]

        color_list = ProtocolDiagramConfig.heatmap_square_color_list
        if mode == ParameterName.simulated:
            if mean_or_std == ParameterName.mean:
                heatmap_square_color_index_list = ProtocolDiagramConfig.mean_heatmap_square_color_index_list
            elif mean_or_std == ParameterName.std:
                heatmap_square_color_index_list = ProtocolDiagramConfig.std_heatmap_square_color_index_list
            else:
                raise ValueError()
        elif mode == ParameterName.sensitivity:
            heatmap_square_color_index_list = ProtocolDiagramConfig.sensitivity_heatmap_square_color_index_list
        else:
            raise ValueError()
        figure_square_list = []
        for row_index in np.arange(size.x):
            for col_index in np.arange(size.y):
                figure_square_list.append(Rectangle(**{
                    **ProtocolDiagramConfig.heatmap_square_config,
                    ParameterName.center:
                        (Vector(col_index, row_index) + 0.5) * self.square_edge + self.box_bottom_left,
                    ParameterName.width: square_edge,
                    ParameterName.height: square_edge,
                    ParameterName.face_color: color_list[
                        heatmap_square_color_index_list[int(row_index)][int(col_index)]]
                }))
        super().__init__(
            figure_square_list, text_config_list=text_config_list, **kwargs)

