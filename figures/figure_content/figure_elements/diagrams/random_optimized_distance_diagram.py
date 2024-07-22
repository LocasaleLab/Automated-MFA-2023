from .config import Vector, ParameterName, VerticalAlignment, HorizontalAlignment, LineStyle, FontWeight, \
    CommonFigureMaterials, ColorConfig, CommonFigureString
from .config import Circle, Arrow, bidirectional_arrow_config_constructor
from .single_protocol_diagram import ProtocolDiagram, ProtocolDiagramConfig


class RandomOptimizedDistanceDiagramConfig(ProtocolDiagramConfig):
    loss_dots_config = ProtocolDiagramConfig.loss_dots_config
    arrow_line_config = ProtocolDiagramConfig.arrow_line_config
    text_config = ProtocolDiagramConfig.text_config
    unoptimized_content_color = CommonFigureMaterials.optimum_with_random_color_dict[ParameterName.unoptimized]
    unoptimized_text_color = CommonFigureMaterials.optimum_with_random_text_color_dict[ParameterName.unoptimized]
    global_optimum_color = CommonFigureMaterials.optimum_with_random_color_dict[ParameterName.global_optimum]
    global_optimum_text_color = CommonFigureMaterials.optimum_with_random_text_color_dict[ParameterName.global_optimum]
    local_optimum_color = CommonFigureMaterials.optimum_with_random_color_dict[ParameterName.local_optimum]
    to_optimal_distance_content_color = ColorConfig.raw_distance_color_with_alpha
    to_optimal_distance_text_color = ColorConfig.distance_text_color

    dots_radius = 0.015
    bound_box_config = {
        **ProtocolDiagramConfig.bound_box_config,
        ParameterName.edge_width: 5,
    }
    normal_arrow_line_config = {
        **arrow_line_config,
        ParameterName.face_color: ColorConfig.to_known_flux_distance_arrow_color,
    }
    global_optimum_distance_arrow_line_config = {
        **arrow_line_config,
        ParameterName.face_color: to_optimal_distance_content_color,
    }
    common_dots_config = {
        **loss_dots_config,
        ParameterName.radius: dots_radius,
    }
    global_optimum_dot_config = {
        **common_dots_config,
        ParameterName.face_color: global_optimum_color
    }
    local_optimum_dot_config = {
        **common_dots_config,
        ParameterName.face_color: local_optimum_color
    }
    random_dot_config = {
        **common_dots_config,
        ParameterName.face_color: unoptimized_content_color
    }

    selected_text_config = {
        **ProtocolDiagramConfig.selected_text_config,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.font_size: 30
    }
    distance_text_config = {
        **selected_text_config,
        ParameterName.font_color: to_optimal_distance_text_color,
    }
    global_optimum_text_config = {
        **selected_text_config,
        ParameterName.font_color: global_optimum_text_color,
    }
    random_dot_text_config = {
        **selected_text_config,
        ParameterName.font_color: unoptimized_text_color
    }
    random_optimized_comparison_label_text_config = {
        **text_config,
        ParameterName.font_size: 40,
    }


class RandomOptimizedDistanceDiagram(ProtocolDiagram):
    total_width = 1
    total_height = 1
    height_to_width_ratio = total_height / total_width
    box_size = Vector(0.95, 0.95)
    box_bottom_left = Vector(0.05, 0.05)

    def __init__(self, **kwargs):
        optimized_coordinate_list = [
            Vector(0.7, 0.75),
            Vector(0.2, 0.15),
            Vector(0.23, 0.57),
            Vector(0.8, 0.35),
        ]
        global_optimum_coordinate = Vector(0.5, 0.4)
        random_coordinate_list = [
            Vector(0.65, 0.1),
            Vector(0.12, 0.84),
            Vector(0.4, 0.22),
            Vector(0.91, 0.88),
        ]
        dots_radius = RandomOptimizedDistanceDiagramConfig.dots_radius
        box_width = self.box_size.x
        box_height = self.box_size.y
        total_width = self.total_width

        title_height = 0.1
        boundary_width = 0.05
        axis_label_distance = 0.02
        text_config_list = [
            {
                **RandomOptimizedDistanceDiagramConfig.random_optimized_comparison_label_text_config,
                ParameterName.string: 'Flux 1',
                # ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (boundary_width - axis_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: boundary_width - axis_label_distance,
            },
            {
                **RandomOptimizedDistanceDiagramConfig.random_optimized_comparison_label_text_config,
                ParameterName.string: 'Flux 2',
                # ParameterName.font_weight: FontWeight.bold,
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
        global_optimum_location = self.box_transform(global_optimum_coordinate, inplace=False)
        for local_optimum_index, local_optimum_coordinate in enumerate(optimized_coordinate_list):
            local_optimum_real_location = self.box_transform(local_optimum_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **RandomOptimizedDistanceDiagramConfig.local_optimum_dot_config,
                ParameterName.center: local_optimum_real_location,
            }))
            line_config_list.append({
                **RandomOptimizedDistanceDiagramConfig.global_optimum_distance_arrow_line_config,
                ParameterName.start: global_optimum_location,
                ParameterName.end: local_optimum_real_location
            })
            if local_optimum_index == 0:
                updated_tail_location, updated_head_location = bidirectional_arrow_config_constructor(
                    global_optimum_location, local_optimum_real_location, dots_radius)
                flux_dot_list.append(Arrow(**{
                    **RandomOptimizedDistanceDiagramConfig.global_optimum_distance_arrow_line_config,
                    ParameterName.tail: updated_tail_location,
                    ParameterName.head: updated_head_location,
                }))
                mid_location = (global_optimum_location + local_optimum_real_location) / 2
                text_config_list.append(
                    {
                        **RandomOptimizedDistanceDiagramConfig.distance_text_config,
                        ParameterName.string: f'Euclidean\ndistance',
                        ParameterName.center: mid_location + Vector(-0.12, 0),
                    }
                )
                text_config_list.append(
                    {
                        **RandomOptimizedDistanceDiagramConfig.selected_text_config,
                        ParameterName.string: f'No.{local_optimum_index + 2} optimized\nsolution',
                        ParameterName.center: local_optimum_real_location + Vector(-0.12, 0.03),
                    }
                )
            else:
                text_config_list.append(
                    {
                        **RandomOptimizedDistanceDiagramConfig.selected_text_config,
                        ParameterName.string: f'No.{local_optimum_index + 2}',
                        ParameterName.center: local_optimum_real_location + Vector(-0.08, 0),
                    }
                )
        for random_index, random_coordinate in enumerate(random_coordinate_list):
            random_real_location = self.box_transform(random_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **RandomOptimizedDistanceDiagramConfig.random_dot_config,
                ParameterName.center: random_real_location,
            }))
            if random_index == 0:
                updated_tail_location, updated_head_location = bidirectional_arrow_config_constructor(
                    global_optimum_location, random_real_location, dots_radius)
                flux_dot_list.append(Arrow(**{
                    **RandomOptimizedDistanceDiagramConfig.global_optimum_distance_arrow_line_config,
                    ParameterName.tail: updated_tail_location,
                    ParameterName.head: updated_head_location,
                }))
                text_config_list.append({
                    **RandomOptimizedDistanceDiagramConfig.random_dot_text_config,
                    ParameterName.string: CommonFigureString.random_fluxes_wrap,
                    ParameterName.center: random_real_location + Vector(0.11, -0.015),
                })
                # mid_location = (global_optimum_location + random_real_location) / 2
                # text_config_list.append({
                #     **RandomOptimizedDistanceDiagramConfig.distance_text_config,
                #     ParameterName.string: f'Distance to\nrandom solution',
                #     ParameterName.center: mid_location + Vector(-0.05, 0),
                # })
        flux_dot_list.append(Circle(**{
            **RandomOptimizedDistanceDiagramConfig.global_optimum_dot_config,
            ParameterName.center: global_optimum_location,
        }))
        text_config_list.append({
            **RandomOptimizedDistanceDiagramConfig.global_optimum_text_config,
            ParameterName.string: CommonFigureString.best_optimized_solution_wrap,
            ParameterName.center: global_optimum_location + Vector(-0.13, 0.01),
            ParameterName.horizontal_alignment: HorizontalAlignment.right,
        })

        super().__init__(
            flux_dot_list, config_class=RandomOptimizedDistanceDiagramConfig, line_config_list=line_config_list,
            text_config_list=text_config_list, **kwargs)
