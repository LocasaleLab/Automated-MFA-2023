from .config import np, Vector, ParameterName, CompositeFigure, TextBox, ColorConfig, ZOrderConfig, \
    TextConfig, HorizontalAlignment, VerticalAlignment, FontWeight, CommonFigureMaterials, LineStyle
from .config import PathShape, PathStep, PathOperation, Circle, CommonElementConfig, common_legend_generator, \
    AxisDiagram, AxisDiagramConfig


class OptimumDistributionDiagramConfig(AxisDiagramConfig):
    bound_box_z_order = AxisDiagramConfig.bound_box_z_order
    dash_line_z_order = AxisDiagramConfig.dash_line_z_order
    content_z_order = AxisDiagramConfig.content_z_order
    label_order = AxisDiagramConfig.label_order
    global_optimum_order = label_order + AxisDiagramConfig.order_increment
    text_config = AxisDiagramConfig.text_config
    optimum_with_random_color_dict = CommonFigureMaterials.optimum_with_random_color_dict
    optimum_with_random_text_color_dict = CommonFigureMaterials.optimum_with_random_text_color_dict
    optimum_name_dict = CommonFigureMaterials.optimum_name_dict
    global_optimum_color = optimum_with_random_color_dict[ParameterName.global_optimum]
    global_optimum_text_color = optimum_with_random_text_color_dict[ParameterName.global_optimum]
    local_optimum_color = optimum_with_random_color_dict[ParameterName.local_optimum]
    local_optimum_text_color = optimum_with_random_text_color_dict[ParameterName.local_optimum]
    random_point_color = optimum_with_random_color_dict[ParameterName.unoptimized]
    random_text_color = optimum_with_random_text_color_dict[ParameterName.unoptimized]

    common_edge_width = 3
    guide_line_edge_width = 1
    common_edge_config = {
        **AxisDiagramConfig.edge_config,
        ParameterName.edge_width: common_edge_width,
    }
    bound_box_config = {
        **common_edge_config,
        ParameterName.z_order: bound_box_z_order,
        ParameterName.edge_color: ColorConfig.normal_blue
    }
    function_curve_config = {
        **common_edge_config,
        ParameterName.closed: False,
        ParameterName.z_order: content_z_order,
        ParameterName.edge_color: ColorConfig.orange
    }
    guide_line_config = {
        **common_edge_config,
        ParameterName.edge_width: guide_line_edge_width,
        ParameterName.z_order: content_z_order,
        ParameterName.edge_color: local_optimum_color,
    }
    dash_line_config = {
        **common_edge_config,
        ParameterName.z_order: dash_line_z_order,
        ParameterName.edge_style: LineStyle.thin_dash,
    }
    global_dash_line_config = {
        **dash_line_config,
        # ParameterName.edge_color: ColorConfig.medium_blue,
        ParameterName.edge_color: global_optimum_color,
    }
    local_dash_line_config = {
        **dash_line_config,
        ParameterName.edge_color: local_optimum_color,
    }
    random_dash_line_config = {
        **dash_line_config,
        ParameterName.edge_color: random_point_color,
    }
    # label_text_font_size = 27
    label_text_font_size = 20
    label_text_config = {
        **text_config,
        ParameterName.font_size: label_text_font_size,
    }
    supplementary_text_config = {
        # ParameterName.font_size: 18,
        ParameterName.font_size: 15,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.line_space: 1.5,
    }
    global_optimum_text_config = {
        **supplementary_text_config,
        # ParameterName.font_color: ColorConfig.normal_blue,
        ParameterName.font_color: global_optimum_text_color,
    }
    local_optimum_text_config = {
        **supplementary_text_config,
        ParameterName.font_color: local_optimum_text_color,
    }
    random_text_config = {
        **supplementary_text_config,
        ParameterName.font_color: random_text_color,
    }
    local_optimum_guide_text_config = {
        **local_optimum_text_config,
        ParameterName.width: 0.4,
        ParameterName.height: 0.3
    }
    optimum_point_config = {
        ParameterName.edge_color: None,
        ParameterName.radius: 0.007,
        ParameterName.z_order: label_order,
    }
    global_optimal_point_config = {
        **optimum_point_config,
        ParameterName.face_color: optimum_with_random_color_dict[ParameterName.global_optimum],
        ParameterName.z_order: global_optimum_order,
    }
    local_optimal_point_config = {
        **optimum_point_config,
        ParameterName.face_color: optimum_with_random_color_dict[ParameterName.local_optimum],
    }
    random_point_config = {
        **optimum_point_config,
        ParameterName.face_color: optimum_with_random_color_dict[ParameterName.unoptimized],
    }


class OptimumFunctionPath(object):
    class OneDominantGlobalOptimum(object):
        total_width = 1
        height_to_width_ratio = 0.28412874583795783
        path_step_list = [
            PathStep(PathOperation.moveto, Vector(0.0, 0.23006659267480573)),
            PathStep(PathOperation.curve4, Vector(0.05584128745837957, 0.25657047724750287),
                     Vector(0.10890788013318532, 0.28307436182019996), Vector(0.1568856825749168, 0.2721864594894559)),
            PathStep(PathOperation.curve4, Vector(0.20486348501664817, 0.26128745837957834),
                     Vector(0.24339178690344068, 0.17389567147613744), Vector(0.2906415094339623, 0.1646947835738067)),
            PathStep(PathOperation.curve4, Vector(0.33789234184239736, 0.15549389567147603),
                     Vector(0.3882941176470588, 0.24361820199778025), Vector(0.4403906770255272, 0.21699223085460623)),
            PathStep(PathOperation.curve4, Vector(0.49248834628190896, 0.19035516093229768),
                     Vector(0.5523418423973364, 0.018723640399555926), Vector(0.60322974472808, 0.00492785793562714)),
            PathStep(PathOperation.curve4, Vector(0.6541065482796892, -0.008879023307436182),
                     Vector(0.6987014428412874, 0.1191897891231963), Vector(0.7457047724750279, 0.13419533851276344)),
            PathStep(PathOperation.curve4, Vector(0.7927081021087681, 0.14920088790233058),
                     Vector(0.8433518312985571, 0.09304106548279681), Vector(0.8852719200887904, 0.09498335183129848)),
            PathStep(PathOperation.curve4, Vector(0.9271920088790234, 0.0969145394006661),
                     Vector(0.9622086570477248, 0.12136514983351822), Vector(1.0, 0.14581576026637083)),
        ]
        random_vector_list = [
            Vector(0.23, 0.21),
            Vector(0.503, 0.14),
            Vector(0.715, 0.11),
        ]
        global_optimal_vector = Vector(0.615, 0.0045)
        local_optimal_vector_list = [
            Vector(0.295, 0.165),
            Vector(0.605, 0.0055),
            Vector(0.885, 0.095),
        ]
        guide_line_config_list = [
            {
                ParameterName.start: Vector(0.608, 0.02),
                ParameterName.end: Vector(0.655, 0.22),
            },
            {
                ParameterName.start: Vector(0.293, 0.15),
                ParameterName.end: Vector(0.28, 0.075),
            },
        ]
        supplementary_text_config_list = [
            {
                ParameterName.center: Vector(0.67, 0.25),
                ParameterName.string: 'Near to global optimal point\nwith similar loss',
            },
            {
                ParameterName.center: Vector(0.27, 0.05),
                ParameterName.string: 'Far from global optimal point\nwith higher loss',
            },
        ]

    class MultipleSimilarLocalOptima(object):
        total_width = 1
        height_to_width_ratio = 0.28412874583795783
        path_step_list = [
            PathStep(PathOperation.moveto, Vector(0.0, 0.21697003329633716)),
            PathStep(PathOperation.curve4, Vector(0.05319311875693676, 0.2594117647058824),
                     Vector(0.10361154273029971, 0.30186459489456163), Vector(0.14384905660377353, 0.2679023307436183)),
            PathStep(PathOperation.curve4, Vector(0.18408657047724747, 0.23395116537180907),
                     Vector(0.2042064372918979, 0.02681465038845711), Vector(0.24420199778024412, 0.01322974472808)),
            PathStep(PathOperation.curve4, Vector(0.28419755826859044, -0.000355160932297629),
                     Vector(0.3377669256381798, 0.1878690344062153), Vector(0.3838224195338512, 0.18640399556048814)),
            PathStep(PathOperation.curve4, Vector(0.4298779134295228, 0.18495005549389554),
                     Vector(0.48199223085460596, -0.008357380688124529), Vector(0.52053274139845, 0.00449500554938977)),
            PathStep(PathOperation.curve4, Vector(0.5590788013318535, 0.017358490566037596),
                     Vector(0.5721642619311875, 0.26233074361820213), Vector(0.615072142064373, 0.26354051054384)),
            PathStep(PathOperation.curve4, Vector(0.657968923418424, 0.2647502774694783),
                     Vector(0.7314206437291898, 0.017591564927857836), Vector(0.77795782463929, 0.01177580466148738)),
            PathStep(PathOperation.curve4, Vector(0.8244950055493895, 0.005948945615982383),
                     Vector(0.8579467258601554, 0.20096559378468387), Vector(0.8943063263041066, 0.22861265260821312)),
            PathStep(PathOperation.curve4, Vector(0.9306659267480577, 0.25625971143174237),
                     Vector(0.9633962264150944, 0.21697003329633716), Vector(1.0, 0.17768035516093245)),
        ]
        random_vector_list = [
            Vector(0.19, 0.15),
            Vector(0.435, 0.13),
            Vector(0.68, 0.17),
        ]
        global_optimal_vector = Vector(0.518, 0.0045)
        local_optimal_vector_list = [
            Vector(0.248, 0.013),
            Vector(0.512, 0.0048),
            Vector(0.78, 0.0123),
        ]
        guide_line_config_list = [
            {
                ParameterName.start: Vector(0.251, 0.025),
                ParameterName.end: Vector(0.29, 0.22),
            },
        ]
        supplementary_text_config_list = [
            {
                ParameterName.center: Vector(0.36, 0.25),
                ParameterName.string: 'Far from global optimal point\nbut with similar loss',
            },
        ]


class OptimumDistributionDiagram(AxisDiagram):
    height_to_width_ratio = 0.5
    total_height = height_to_width_ratio * AxisDiagram.total_width
    box_size = Vector(0.8, 0.4)
    box_bottom_left = Vector(1, height_to_width_ratio) - box_size

    def __init__(
            self, distribution_type=ParameterName.one_dominant_global_optimum, **kwargs):
        minimum_value = 0.05
        vertical_scale_ratio = 0.4 / 0.3
        vertex_scale_vector = Vector(1, vertical_scale_ratio)
        box_width, box_height = self.box_size
        box_left, box_bottom = self.box_bottom_left

        if distribution_type == ParameterName.one_dominant_global_optimum:
            target_function_obj = OptimumFunctionPath.OneDominantGlobalOptimum
        elif distribution_type == ParameterName.multiple_similar_local_optima:
            target_function_obj = OptimumFunctionPath.MultipleSimilarLocalOptima
        else:
            raise ValueError()

        function_path_list = target_function_obj.path_step_list
        global_optimal_vector = target_function_obj.global_optimal_vector * vertex_scale_vector \
            + Vector(0, minimum_value)
        global_optimal_location, global_optimum = global_optimal_vector
        local_optimal_vector_list = target_function_obj.local_optimal_vector_list
        selected_local_optimal_location, selected_local_optimum = local_optimal_vector_list[0] * vertex_scale_vector \
            + Vector(0, minimum_value)
        random_vector_list = target_function_obj.random_vector_list
        selected_random_location, selected_random_loss = random_vector_list[0] * vertex_scale_vector \
            + Vector(0, minimum_value)
        guide_line_config_list = target_function_obj.guide_line_config_list
        supplementary_text_config_list = target_function_obj.supplementary_text_config_list
        for path_step in function_path_list:
            for vertex_index, path_vertex in enumerate(path_step.vertex_list):
                path_step.vertex_list[vertex_index] = self.box_transform(
                    path_vertex * vertex_scale_vector + Vector(0, minimum_value))
        function_path_config = {
            ParameterName.path_step_list: function_path_list,
            **OptimumDistributionDiagramConfig.function_curve_config
        }
        function_path_obj = PathShape(**function_path_config)

        content_obj_list = [
            function_path_obj,
            Circle(**{
                **OptimumDistributionDiagramConfig.global_optimal_point_config,
                ParameterName.center: global_optimal_vector
            })
        ]
        for local_optimal_vector in local_optimal_vector_list:
            content_obj_list.append(Circle(**{
                **OptimumDistributionDiagramConfig.local_optimal_point_config,
                ParameterName.center: self.box_transform(
                    local_optimal_vector * vertex_scale_vector + Vector(0, minimum_value))
            }))
        for random_vector in random_vector_list:
            content_obj_list.append(Circle(**{
                **OptimumDistributionDiagramConfig.random_point_config,
                ParameterName.center: self.box_transform(
                    random_vector * vertex_scale_vector + Vector(0, minimum_value))
            }))
        line_config_list = [
            {
                **OptimumDistributionDiagramConfig.global_dash_line_config,
                ParameterName.name: 'global_optimum_horizontal',
                ParameterName.start: self.box_transform(Vector(0, global_optimum)),
                ParameterName.end: self.box_transform(Vector(1, global_optimum))
            },
            {
                **OptimumDistributionDiagramConfig.global_dash_line_config,
                ParameterName.name: 'global_optimal_solution_vertical',
                ParameterName.start: self.box_transform(Vector(global_optimal_location, 0)),
                ParameterName.end: self.box_transform(global_optimal_vector)
            },
            {
                **OptimumDistributionDiagramConfig.local_dash_line_config,
                ParameterName.name: 'local_optimum_horizontal',
                ParameterName.start: self.box_transform(Vector(0, selected_local_optimum)),
                ParameterName.end: self.box_transform(Vector(selected_local_optimal_location, selected_local_optimum))
            },
            {
                **OptimumDistributionDiagramConfig.random_dash_line_config,
                ParameterName.name: 'random_loss_horizontal',
                ParameterName.start: self.box_transform(Vector(0, selected_random_loss)),
                ParameterName.end: self.box_transform(Vector(selected_random_location, selected_random_loss))
            },
        ]
        supplementary_text_height = 0.05
        # left_label_distance = 0.03
        left_label_distance = 0.01
        left_text_distance = 0.01
        bottom_label_distance = 0.05
        bottom_text_distance = 0.01
        if abs(selected_local_optimum - global_optimum) < 0.015:
            selected_local_optimum += np.sign(selected_local_optimum - global_optimum) * 0.015
        text_config_list = [
            {
                **OptimumDistributionDiagramConfig.label_text_config,
                ParameterName.string: 'Loss value',
                # ParameterName.vertical_alignment: VerticalAlignment.baseline,
                # ParameterName.horizontal_alignment: HorizontalAlignment.center,
                # ParameterName.center: Vector(
                #     (box_left - left_label_distance) / 2,
                #     self.box_transform(raw_y=0.55 * self.height_to_width_ratio)),
                # ParameterName.width: box_height,
                # ParameterName.height: box_left - left_label_distance,
                # ParameterName.angle: 90,
                ParameterName.horizontal_alignment: HorizontalAlignment.right,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.center: Vector(
                    (box_left - left_label_distance) / 2,
                    self.box_bottom_left.y + self.box_size.y - 0.02),
                ParameterName.width: box_left - left_label_distance,
                ParameterName.height: supplementary_text_height,
                ParameterName.text_box: False,
            },
            {
                **OptimumDistributionDiagramConfig.label_text_config,
                ParameterName.string: 'Solution space',
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=0.5),
                    (box_bottom - bottom_label_distance) / 2),
                ParameterName.width: box_width,
                ParameterName.height: box_bottom - bottom_label_distance,
            },
            {
                **OptimumDistributionDiagramConfig.global_optimum_text_config,
                ParameterName.string: 'Global optimum',
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.right,
                ParameterName.center: Vector(
                    (box_left - left_text_distance) / 2,
                    self.box_transform(raw_y=global_optimum)),
                ParameterName.width: box_left - left_text_distance,
                ParameterName.height: supplementary_text_height,
            },
            {
                **OptimumDistributionDiagramConfig.global_optimum_text_config,
                ParameterName.string: 'Global optimal solution',
                ParameterName.vertical_alignment: VerticalAlignment.top,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: Vector(
                    self.box_transform(raw_x=global_optimal_location),
                    box_bottom - bottom_text_distance - supplementary_text_height / 2),
                ParameterName.width: 0.2,
                ParameterName.height: supplementary_text_height,
            },
            {
                **OptimumDistributionDiagramConfig.local_optimum_text_config,
                ParameterName.string: 'Local optimum',
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.right,
                ParameterName.center: Vector(
                    (box_left - left_text_distance) / 2,
                    self.box_transform(raw_y=selected_local_optimum)),
                ParameterName.width: box_left - left_text_distance,
                ParameterName.height: supplementary_text_height,
            },
            {
                **OptimumDistributionDiagramConfig.random_text_config,
                ParameterName.string: 'Random point loss',
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.right,
                ParameterName.center: Vector(
                    (box_left - left_text_distance) / 2,
                    self.box_transform(raw_y=selected_random_loss)),
                ParameterName.width: box_left - left_text_distance,
                ParameterName.height: supplementary_text_height,
            },
        ]

        for guide_line_config_dict, supplementary_text_config in zip(
                guide_line_config_list, supplementary_text_config_list):
            real_guide_line_start, real_guide_line_end, real_text_center = [self.box_transform(
                raw_vector * vertex_scale_vector + Vector(0, minimum_value)) for raw_vector in [
                guide_line_config_dict[ParameterName.start],
                guide_line_config_dict[ParameterName.end],
                supplementary_text_config[ParameterName.center]]
            ]
            line_config_list.append({
                **OptimumDistributionDiagramConfig.guide_line_config,
                ParameterName.start: real_guide_line_start,
                ParameterName.end: real_guide_line_end,
            })
            text_config_list.append({
                **OptimumDistributionDiagramConfig.local_optimum_guide_text_config,
                ParameterName.center: real_text_center,
                ParameterName.string: supplementary_text_config[ParameterName.string]
            })

        super().__init__(
            OptimumDistributionDiagramConfig, content_obj_list, line_config_list=line_config_list,
            text_config_list=text_config_list, background=False, **kwargs)


def each_element_location_generation(
        bottom, subplot_height_to_width_ratio, title_gap, title_box_height, top_margin):
    subplot_top = bottom + subplot_height_to_width_ratio
    title_center_y = subplot_top + title_gap + title_box_height / 2
    title_top = subplot_top + title_gap + title_box_height + top_margin
    return subplot_top, title_center_y, title_top


class OptimumDistributionComparisonDiagramConfig(object):
    scale = 0.9
    left = 0
    # total_width = 1.6
    total_width = 0.95
    lower_bottom = 0
    title_box_height = 0.04
    explanation_text_box_height = 0.2
    title_box_y_distance = 0.03
    left_column_width = 0.7
    legend_gap = 0
    # legend_height = 0.04
    legend_height = 0.15
    legend_font_size = 20
    chevron_center_x = 0.88
    chevron_width = 0.09
    chevron_x_tail = chevron_center_x - chevron_width / 2
    chevron_x_head = chevron_center_x + chevron_width / 2
    right_explanation_center_x = 1.3
    right_text_width = 0.5

    subplot_total_height = OptimumDistributionDiagram.total_height * scale
    subplot_total_width = OptimumDistributionDiagram.total_width * scale
    (
        lower_box_top, lower_title_center_y, upper_bottom
    ) = each_element_location_generation(
        lower_bottom, subplot_total_height, title_box_y_distance, title_box_height,
        title_box_y_distance)
    lower_explanation_text_center_y = (lower_bottom + lower_box_top) / 2 + 0.03
    (
        upper_box_top, upper_title_center_y, upper_top
    ) = each_element_location_generation(
        upper_bottom, subplot_total_height, title_box_y_distance, title_box_height,
        title_box_y_distance)
    upper_explanation_text_center_y = (upper_bottom + upper_box_top) / 2 + 0.03

    legend_center_y = upper_top + legend_gap + legend_height / 2
    legend_center_x = total_width / 2 + 0.05
    legend_center = Vector(legend_center_x, legend_center_y)
    legend_size = Vector(2 * total_width - legend_center_x * 2, legend_height)
    total_height = upper_top + legend_gap + legend_height
    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01
    explanation_left_margin = 0.2

    upper_title_center = Vector(subplot_total_width / 2, upper_title_center_y)
    lower_title_center = Vector(subplot_total_width / 2, lower_title_center_y)
    upper_explanation_text_center = Vector(right_explanation_center_x, upper_explanation_text_center_y)
    lower_explanation_text_center = Vector(right_explanation_center_x, lower_explanation_text_center_y)
    common_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }
    title_text_config = {
        **common_text_config,
        ParameterName.font_size: 23,
        ParameterName.width: left_column_width,
        ParameterName.height: title_box_height,
        # ParameterName.font_weight: FontWeight.bold,
        ParameterName.text_box: False
    }
    explanation_text_config = {
        **common_text_config,
        ParameterName.font_size: 25,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.width: right_text_width,
        ParameterName.height: explanation_text_box_height,
        ParameterName.line_space: 2,
        ParameterName.text_box: False,
    }
    chevron_config = {
        **CommonElementConfig.chevron_config,
        ParameterName.width: CommonElementConfig.normal_chevron_width + 0.01
    }
    lower_chevron_config = {
        **chevron_config,
        ParameterName.tail_end_center: Vector(chevron_x_tail, lower_explanation_text_center_y),
        ParameterName.head: Vector(chevron_x_head, lower_explanation_text_center_y),
    }
    upper_chevron_config = {
        **chevron_config,
        ParameterName.tail_end_center: Vector(chevron_x_tail, upper_explanation_text_center_y),
        ParameterName.head: Vector(chevron_x_head, upper_explanation_text_center_y),
    }
    legend_config_dict = {
        ParameterName.legend_center: legend_center,
        ParameterName.legend_area_size: legend_size,
        ParameterName.name_dict: OptimumDistributionDiagramConfig.optimum_name_dict,
        # ParameterName.horiz_or_vertical: ParameterName.horizontal,
        ParameterName.horiz_or_vertical: ParameterName.vertical,
        ParameterName.shape: ParameterName.circle,
        ParameterName.alpha: None,
        ParameterName.location_config_dict: {
            # ParameterName.total_horiz_edge_ratio: 0.2,
            # ParameterName.col_horiz_edge_ratio: 0.2,
            ParameterName.total_verti_edge_ratio: 0.1,
            ParameterName.row_verti_edge_ratio: 0.8,
        },
        ParameterName.text_config_dict: {
            ParameterName.font_size: legend_font_size,
            ParameterName.font_weight: FontWeight.bold
        }
    }


class OptimumDistributionComparisonDiagram(CompositeFigure):
    total_width = OptimumDistributionComparisonDiagramConfig.total_width
    total_height = OptimumDistributionComparisonDiagramConfig.total_height
    height_to_width_ratio = total_height / total_width

    def __init__(self, **kwargs):
        common_left = OptimumDistributionComparisonDiagramConfig.left
        upper_bottom = OptimumDistributionComparisonDiagramConfig.upper_bottom
        lower_bottom = OptimumDistributionComparisonDiagramConfig.lower_bottom
        title_box_y_distance = OptimumDistributionComparisonDiagramConfig.title_box_y_distance
        common_optimum_distribution_diagram_config = {
            ParameterName.scale: OptimumDistributionComparisonDiagramConfig.scale,
            ParameterName.base_z_order: OptimumDistributionComparisonDiagramConfig.child_diagram_base_z_order,
            ParameterName.z_order_increment: OptimumDistributionComparisonDiagramConfig.child_diagram_z_order_increment
        }
        upper_optimum_distribution_diagram_config_dict = {
            **common_optimum_distribution_diagram_config,
            ParameterName.distribution_type: ParameterName.one_dominant_global_optimum,
            ParameterName.bottom_left_offset: Vector(common_left, upper_bottom),
        }
        lower_optimum_distribution_diagram_config_dict = {
            **common_optimum_distribution_diagram_config,
            ParameterName.distribution_type: ParameterName.multiple_similar_local_optima,
            ParameterName.bottom_left_offset: Vector(common_left, lower_bottom),
        }
        upper_optimum_distribution_diagram_obj = OptimumDistributionDiagram(
            **upper_optimum_distribution_diagram_config_dict)
        lower_optimum_distribution_diagram_obj = OptimumDistributionDiagram(
            **lower_optimum_distribution_diagram_config_dict)

        upper_title_text_config_dict = {
            **OptimumDistributionComparisonDiagramConfig.title_text_config,
            ParameterName.string: 'One dominant global optimum landscape',
            ParameterName.center: OptimumDistributionComparisonDiagramConfig.upper_title_center
        }
        lower_title_text_config_dict = {
            **OptimumDistributionComparisonDiagramConfig.title_text_config,
            ParameterName.string: 'Multiple similar local optima landscape',
            ParameterName.center: OptimumDistributionComparisonDiagramConfig.lower_title_center
        }
        # upper_explanation_text_config_dict = {
        #     **OptimumDistributionComparisonDiagramConfig.explanation_text_config,
        #     ParameterName.string: 'Local optimal point are either\nnear to global optimum with similar loss\n'
        #                           'or far from that with higher loss',
        #     ParameterName.center: OptimumDistributionComparisonDiagramConfig.upper_explanation_text_center
        # }
        # lower_explanation_text_config_dict = {
        #     **OptimumDistributionComparisonDiagramConfig.explanation_text_config,
        #     ParameterName.string: 'Local optimal point may be\nfar from global optimum with similar loss',
        #     ParameterName.center: OptimumDistributionComparisonDiagramConfig.lower_explanation_text_center
        # }
        text_obj_dict = {
            'upper_title': TextBox(**upper_title_text_config_dict),
            'lower_title': TextBox(**lower_title_text_config_dict),
            # 'upper_explanation': TextBox(**upper_explanation_text_config_dict),
            # 'lower_explanation': TextBox(**lower_explanation_text_config_dict),
        }
        # chevron_obj_dict = {
        #     'upper_arrow': ChevronArrow(**OptimumDistributionComparisonDiagramConfig.lower_chevron_config),
        #     'bottom_arrow': ChevronArrow(**OptimumDistributionComparisonDiagramConfig.upper_chevron_config),
        # }

        legend_obj = common_legend_generator(
            OptimumDistributionComparisonDiagramConfig.legend_config_dict,
            OptimumDistributionDiagramConfig.optimum_with_random_color_dict)
        size = Vector(self.total_width, self.total_height)
        optimum_distribution_comparison_diagram_dict = {
            ParameterName.text: text_obj_dict,
            ParameterName.optimum_distribution_diagram: {
                'upper_optimum_distribution': upper_optimum_distribution_diagram_obj,
                'lower_optimum_distribution': lower_optimum_distribution_diagram_obj},
            # ParameterName.chevron_arrow: chevron_obj_dict,
            ParameterName.legend: {ParameterName.legend: legend_obj},
        }
        super().__init__(
            optimum_distribution_comparison_diagram_dict, Vector(0, 0), size, background=False, **kwargs)


