from .config import ParameterName, Vector, FontWeight, CompositeFigure, ColorConfig, \
    HorizontalAlignment, VerticalAlignment, CommonElementConfig, CommonFigureString, \
    default_parameter_extract, TextBox, calculate_center_bottom_offset, \
    CrossAxisDiagram, AxisDiagramConfig, Circle, Line, Ellipse


class SingleFluxSloppinessDiagramConfig(AxisDiagramConfig):
    bound_box_z_order = AxisDiagramConfig.bound_box_z_order
    dash_line_z_order = AxisDiagramConfig.dash_line_z_order
    bound_box_background_order = AxisDiagramConfig.bound_box_background_order
    content_z_order = AxisDiagramConfig.content_z_order
    label_order = AxisDiagramConfig.label_order
    arrow_z_order = dash_line_z_order
    text_order = AxisDiagramConfig.text_order
    text_config = AxisDiagramConfig.text_config

    common_edge_width = 3
    thin_line_width = 1
    common_edge_config = {
        **AxisDiagramConfig.edge_config,
        ParameterName.edge_width: common_edge_width,
    }
    brace_height = 0.05
    label_text_font_size = 20
    label_text_config = {
        **text_config,
        ParameterName.font_size: label_text_font_size,
    }
    sub_title_text_config = {
        **text_config,
        ParameterName.font_size: 20,
    }

    selected_solution_color = ColorConfig.selected_solution_color
    selected_solution_text_color = ColorConfig.selected_solution_text_color
    averaged_solution_color = ColorConfig.averaged_solution_color
    averaged_solution_text_color = ColorConfig.averaged_solution_text_color
    reoptimized_solution_color = ColorConfig.reoptimized_solution_color
    reoptimized_solution_text_color = ColorConfig.reoptimized_solution_text_color
    predefined_flux_color = ColorConfig.known_flux_color
    predefined_flux_text_color = ColorConfig.known_flux_text_color

    normal_text_font_size = 20
    normal_text_height = 0.1
    common_solutions_text_config = {
        **text_config,
        ParameterName.font_size: normal_text_font_size - 2,
        ParameterName.width: 0.2,
        ParameterName.height: normal_text_height,
        ParameterName.font_weight: FontWeight.bold,
    }
    common_indicator_line_config = {
        **common_edge_config,
        ParameterName.edge_width: thin_line_width,
        ParameterName.z_order: text_order,
    }
    optimized_solutions_text_config = {
        **common_solutions_text_config,
        # ParameterName.font_color: ColorConfig.orange,
        ParameterName.font_color: selected_solution_color,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    optimized_indicator_line_config = {
        **common_indicator_line_config,
        # ParameterName.edge_color: ColorConfig.medium_orange,
        ParameterName.edge_color: selected_solution_color,
    }
    averaged_solutions_text_config = {
        **common_solutions_text_config,
        ParameterName.font_color: averaged_solution_color,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    averaged_indicator_line_config = {
        **common_indicator_line_config,
        ParameterName.edge_color: averaged_solution_color,
    }
    reoptimized_solutions_text_config = {
        **common_solutions_text_config,
        ParameterName.font_color: reoptimized_solution_color,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    reoptimized_indicator_line_config = {
        **common_indicator_line_config,
        ParameterName.edge_color: reoptimized_solution_color,
    }
    # known_flux_text_config = {
    #     **text_config,
    #     ParameterName.font_size: normal_text_font_size - 4,
    #     ParameterName.font_color: ColorConfig.dark_blue,
    #     ParameterName.width: 0.2,
    #     ParameterName.height: normal_text_height,
    #     ParameterName.font_weight: FontWeight.bold,
    # }
    known_flux_text_config = {
        **common_solutions_text_config,
        # ParameterName.font_size: normal_text_font_size - 4,
        ParameterName.font_color: predefined_flux_color,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    known_flux_indicator_line_config = {
        **common_indicator_line_config,
        ParameterName.edge_color: predefined_flux_color,
    }
    low_loss_text_config = {
        **common_solutions_text_config,
        ParameterName.font_color: ColorConfig.random_flux_color.transparency_mix(0.8),
    }

    dots_radius = 0.007
    solution_dots_config = {
        ParameterName.radius: dots_radius,
        # ParameterName.face_color: ColorConfig.medium_orange,
        ParameterName.edge_width: None,
        ParameterName.z_order: content_z_order,
    }
    known_flux_dots_config = {
        **solution_dots_config,
        ParameterName.radius: dots_radius * 1.5,
        ParameterName.face_color: predefined_flux_color,
    }
    selected_solutions_dots_config = {
        **solution_dots_config,
        ParameterName.face_color: selected_solution_color,
    }
    averaged_dots_config = {
        **solution_dots_config,
        ParameterName.face_color: averaged_solution_color,
    }
    reoptimized_dots_config = {
        **solution_dots_config,
        ParameterName.face_color: reoptimized_solution_color,
    }

    low_loss_ellipse_background_config = {
        **AxisDiagramConfig.edge_config,
        # ParameterName.face_color: ColorConfig.random_flux_color_with_alpha.transparency_mix(0.2),
        ParameterName.face_color: ColorConfig.random_flux_color_with_alpha.transparency_mix(0.2),
        ParameterName.z_order: dash_line_z_order,
    }
    low_loss_ellipse_config = {
        **AxisDiagramConfig.edge_config,
        ParameterName.edge_width: common_edge_width,
        # ParameterName.edge_color: ColorConfig.random_flux_color_with_alpha,
        ParameterName.edge_color: ColorConfig.random_flux_color_with_alpha,
        ParameterName.z_order: label_order,
    }

    known_flux_vertical_line_config = {
        **optimized_indicator_line_config,
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

    known_flux_coordinate = Vector(0, 0)
    selected_optimized_coordinate_list = [
        Vector(-0.07157, -0.28344),
        Vector(-0.07273, 0.28111),
        Vector(-0.06485, 0.13394),
        Vector(0.03634, -0.37886),
        Vector(0.01933, -0.29547),
        Vector(0.02891, 0.18733),
        Vector(0.01991, 0.36733),
        Vector(0.05744, 0.33542),
        Vector(-0.02323, 0.31164),
        Vector(0.07186, -0.30810),
        Vector(-0.03138, -0.25687),
        Vector(0.07440, 0.27329),
        Vector(0.06941, -0.17890),
        Vector(-0.07255, 0.24522),
        Vector(0.08991, -0.11803),
        Vector(0.04076, 0.10652),
        Vector(0.02128, 0.32104),
        Vector(0.09332, -0.14875),
        Vector(0.02945, -0.10263),
        Vector(-0.0300, -0.15916),
        Vector(0.04718, 0.07406),
        Vector(-0.05263, -0.30915),
    ]

    averaged_optimized_coordinate_list = [
        Vector(0.01513, 0.04812),
        Vector(-0.03114, 0.02473),
        Vector(0.03715, 0.03238),
        Vector(0.02877, -0.03989),
        Vector(0.03908, -0.01866),
        Vector(-0.05530, 0.01888),
        Vector(0.06186, 0.03866),
        Vector(0.04530, -0.07264),
        Vector(-0.04777, 0.04885),
        Vector(0.04197, 0.02909),
    ]

    re_optimized_coordinate_list = [
        Vector(0.01513, 0.03866),
        Vector(-0.03114, 0.01888),
        Vector(0.03715, 0.02909),
        Vector(0.02877, -0.01866),
        Vector(0.03908, -0.03989),
        Vector(-0.05530, 0.04885),
        Vector(0.06186, 0.04812),
        Vector(0.04530, -0.07264),
        Vector(-0.04777, 0.02473),
        Vector(0.04197, 0.03238),
    ]

    @staticmethod
    def calculate_center(self, scale, *args):
        size = args[0]
        assert isinstance(size, Vector)
        _, total_size = self.calculate_box_and_total_size(size)
        return total_size / 2 * scale


class SingleFluxSloppinessDiagram(CrossAxisDiagram):
    def __init__(self, *args, config_class=SingleFluxSloppinessDiagramConfig, **kwargs):
        super().__init__(config_class, *args, **kwargs)

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) / 2 * scale


class BasicFluxSloppinessDiagram(SingleFluxSloppinessDiagram):
    # total_width = 0.6
    # total_height = 0.7
    # height_to_width_ratio = total_height / total_width
    # box_size = Vector(total_width, total_height)
    # box_bottom_left = Vector(0, 0)
    # center = box_bottom_left + box_size / 2

    def __init__(self, figure_data_parameter_dict, bottom_left, size, **kwargs):
        mode = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.mode, ParameterName.selected)
        data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, ParameterName.all_data_mode)
        known_flux_coordinate = SingleFluxSloppinessDiagramConfig.known_flux_coordinate
        self.box_bottom_left = bottom_left
        self.box_size = size
        self.center = self.box_bottom_left + self.box_size / 2
        label_text_width = 0.3
        label_text_height = 0.05

        if mode == ParameterName.selected or mode == ParameterName.raw_optimized:
            coordinate_list = SingleFluxSloppinessDiagramConfig.selected_optimized_coordinate_list
            solution_dots_config = SingleFluxSloppinessDiagramConfig.selected_solutions_dots_config
        elif mode == ParameterName.averaged:
            coordinate_list = SingleFluxSloppinessDiagramConfig.averaged_optimized_coordinate_list
            solution_dots_config = SingleFluxSloppinessDiagramConfig.averaged_dots_config
        elif mode == ParameterName.optimized:
            coordinate_list = SingleFluxSloppinessDiagramConfig.re_optimized_coordinate_list
            solution_dots_config = SingleFluxSloppinessDiagramConfig.reoptimized_dots_config
        else:
            raise ValueError()
        if data_name == ParameterName.all_data_mode:
            ellipse_width_coeff = 0.29
            ellipse_height_coeff = 0.85
            low_loss_text_coeff = Vector(0.23, 0.2)
        elif data_name == ParameterName.experimental:
            ellipse_width_coeff = 0.45
            ellipse_height_coeff = 0.85
            low_loss_text_coeff = Vector(0.3, 0.25)
        else:
            raise ValueError()
        text_config_list = [
            {
                **SingleFluxSloppinessDiagramConfig.label_text_config,
                ParameterName.string: CommonFigureString.unconstrained_fluxes_wrap,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: self.box_transform(raw_vector=Vector(-0.1, 0.6)),
                ParameterName.width: label_text_width,
                ParameterName.height: label_text_height,
            },
            {
                **SingleFluxSloppinessDiagramConfig.label_text_config,
                ParameterName.string: CommonFigureString.constrained_fluxes_wrap,
                ParameterName.font_weight: FontWeight.bold,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.center: self.box_transform(Vector(0.45, -0.065)),
                ParameterName.width: label_text_width,
                ParameterName.height: label_text_height,
            },
        ]

        flux_dot_list = []
        line_config_list = []
        known_flux_real_location = self.box_transform(known_flux_coordinate, inplace=False)
        for sample_coordinate in coordinate_list:
            sample_real_location = self.box_transform(sample_coordinate, inplace=False)
            flux_dot_list.append(Circle(**{
                **solution_dots_config,
                ParameterName.center: sample_real_location,
            }))
        indicator_line_config_list = []
        if mode == ParameterName.selected or mode == ParameterName.raw_optimized:
            if mode == ParameterName.selected:
                text_str = CommonFigureString.selected_solution_wrap
            else:
                text_str = CommonFigureString.optimized_solution_wrap
            text_config_list.append({
                **SingleFluxSloppinessDiagramConfig.optimized_solutions_text_config,
                ParameterName.string: text_str,
                ParameterName.center: self.box_transform(Vector(-0.3, 0.2)),
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
            })
            indicator_line_config_list.extend([
                {
                    **SingleFluxSloppinessDiagramConfig.optimized_indicator_line_config,
                    ParameterName.start: self.box_transform(Vector(-0.18, 0.22)),
                    ParameterName.end: self.box_transform(Vector(-0.095, 0.275)),
                },
                {
                    **SingleFluxSloppinessDiagramConfig.optimized_indicator_line_config,
                    ParameterName.start: self.box_transform(Vector(-0.18, 0.18)),
                    ParameterName.end: self.box_transform(Vector(-0.085, 0.14)),
                },
            ])
        elif mode == ParameterName.averaged:
            text_config_list.append({
                **SingleFluxSloppinessDiagramConfig.averaged_solutions_text_config,
                ParameterName.string: CommonFigureString.averaged_solution_wrap,
                ParameterName.center: self.box_transform(Vector(-0.32, 0.1)),
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
            })
            indicator_line_config_list.extend([
                {
                    **SingleFluxSloppinessDiagramConfig.averaged_indicator_line_config,
                    ParameterName.start: self.box_transform(Vector(-0.2, 0.09)),
                    ParameterName.end: self.box_transform(Vector(-0.065, 0.055)),
                },
            ])
        elif mode == ParameterName.optimized:
            text_config_list.append({
                **SingleFluxSloppinessDiagramConfig.reoptimized_solutions_text_config,
                ParameterName.string: CommonFigureString.reoptimized_solution_wrap,
                ParameterName.center: self.box_transform(Vector(-0.32, 0.1)),
            })
            indicator_line_config_list.extend([
                {
                    **SingleFluxSloppinessDiagramConfig.reoptimized_indicator_line_config,
                    ParameterName.start: self.box_transform(Vector(-0.19, 0.09)),
                    ParameterName.end: self.box_transform(Vector(-0.072, 0.057)),
                },
            ])
        if mode != ParameterName.raw_optimized:
            text_config_list.append({
                **SingleFluxSloppinessDiagramConfig.known_flux_text_config,
                ParameterName.string: 'Known\nflux vector',
                # ParameterName.center: known_flux_real_location + Vector(-0.045, -0.03),
                ParameterName.center: self.box_transform(Vector(-0.32, -0.15)),
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
            })
            flux_dot_list.append(Circle(**{
                **SingleFluxSloppinessDiagramConfig.known_flux_dots_config,
                ParameterName.center: known_flux_real_location,
            }))
            indicator_line_config_list.extend([
                {
                    **SingleFluxSloppinessDiagramConfig.known_flux_indicator_line_config,
                    ParameterName.start: self.box_transform(Vector(-0.18, -0.12)),
                    ParameterName.end: self.box_transform(Vector(-0.02, -0.017)),
                },
            ])
        flux_dot_list.extend(
            [Line(**indicator_line_config) for indicator_line_config in indicator_line_config_list])
        low_loss_ellipse_center = self.box_transform(Vector(0, 0))
        low_loss_ellipse_width = ellipse_width_coeff * self.box_size.x
        low_loss_ellipse_height = ellipse_height_coeff * self.box_size.y
        low_loss_text_center = self.box_transform(low_loss_text_coeff)
        flux_dot_list.extend([
            Ellipse(**{
                **SingleFluxSloppinessDiagramConfig.low_loss_ellipse_config,
                ParameterName.center: low_loss_ellipse_center,
                ParameterName.width: low_loss_ellipse_width,
                ParameterName.height: low_loss_ellipse_height, }),
            Ellipse(**{
                **SingleFluxSloppinessDiagramConfig.low_loss_ellipse_background_config,
                ParameterName.center: low_loss_ellipse_center,
                ParameterName.width: low_loss_ellipse_width,
                ParameterName.height: low_loss_ellipse_height, }),
        ])
        text_config_list.extend([
            {
                **SingleFluxSloppinessDiagramConfig.low_loss_text_config,
                ParameterName.string: 'Low loss\nregion',
                ParameterName.center: low_loss_text_center,
                ParameterName.horizontal_alignment: HorizontalAlignment.center,
                ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            },
        ])

        super().__init__(
            flux_dot_list, line_config_list=line_config_list, text_config_list=text_config_list,
            background=False, **kwargs)


class FluxSloppinessDiagram(CompositeFigure):
    total_width = 0.7
    height_to_width_ratio = 0.8
    title_gap = 0.1
    title_height = 0.12
    figure_width = 0.6
    figure_height = 0.7
    font_size = 27
    box_bottom_left = Vector(0.05, 0)

    def calculate_height(self, figure_title=None, **kwargs):
        figure_height = self.figure_height
        total_height = self.box_bottom_left.y + figure_height
        if figure_title is not None:
            total_height += self.title_height + self.title_gap
        return total_height

    def __init__(self, figure_data_parameter_dict, **kwargs):
        figure_title = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_title, None, pop=True)
        total_width = self.total_width
        figure_left, figure_bottom = self.box_bottom_left
        figure_height = self.figure_height
        figure_width = self.figure_width
        total_height = self.calculate_height(figure_title)
        title_height = self.title_height
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        title_bottom = figure_bottom + figure_height + self.title_gap
        title_center_x = figure_left + figure_width / 2
        title_center_y = title_bottom + title_height / 2

        basic_flux_sloppiness_config_dict = {
            ParameterName.bottom_left: self.box_bottom_left,
            ParameterName.size: Vector(figure_width, figure_height),
            ParameterName.figure_data_parameter_dict: {
                **figure_data_parameter_dict,
            },
        }
        title_text_config = {
            **CommonElementConfig.common_text_config,
            ParameterName.font_size: self.font_size,
            ParameterName.string: figure_title,
            ParameterName.center: Vector(title_center_x, title_center_y),
            ParameterName.width: figure_width,
            ParameterName.height: title_height,
        }

        subfigure_element_dict = {
            'basic_flux_sloppiness_diagram': {
                'basic_flux_sloppiness_diagram': BasicFluxSloppinessDiagram(**basic_flux_sloppiness_config_dict)},
        }
        if figure_title is not None:
            subfigure_element_dict['basic_flux_sloppiness_diagram']['title'] = TextBox(**title_text_config)
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)


class SmallFluxSloppinessDiagram(FluxSloppinessDiagram):
    title_gap = 0.05
    title_height = 0.1
    font_size = 35
    box_bottom_left = Vector(0.05, 0)


class MultipleFluxSloppinessDiagram(CompositeFigure):
    def __init__(self, figure_data_parameter_dict, horiz_or_vertical=ParameterName.horizontal, **kwargs):
        figure_title_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.figure_title, None, pop=True)
        default_sloppiness_width = SmallFluxSloppinessDiagram.total_width
        # default_sloppiness_height = FluxSloppinessDiagram.figure_height + FluxSloppinessDiagram.title_height
        default_sloppiness_height = SmallFluxSloppinessDiagram.calculate_height(
            SmallFluxSloppinessDiagram, figure_title_list)
        subfigure_scale = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.scale, 1, pop=True)
        with_re_optimization = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.with_re_optimization, True, pop=True)
        if with_re_optimization:
            total_subfigure_num = 3
        else:
            total_subfigure_num = 2
        if horiz_or_vertical == ParameterName.vertical:
            diagram_y_interval = default_parameter_extract(
                figure_data_parameter_dict, ParameterName.ax_interval, 0, pop=True)
            total_height = 1
            each_diagram_height = (total_height - (total_subfigure_num - 1) * diagram_y_interval) / total_subfigure_num
            default_scale = each_diagram_height / default_sloppiness_height
            common_scale = default_scale * subfigure_scale
            current_cell_height = default_sloppiness_height * common_scale
            current_cell_width = default_sloppiness_width * common_scale
            cell_size = Vector(current_cell_width, current_cell_height)
            total_width = current_cell_width
            cell_bottom_left_list = [
                Vector(0, current_cell_height * i + diagram_y_interval * min(i - 1, 0))
                for i in range(total_subfigure_num)]
            cell_bottom_left_list.reverse()
        elif horiz_or_vertical == ParameterName.horizontal:
            diagram_x_interval = default_parameter_extract(
                figure_data_parameter_dict, ParameterName.ax_interval, 0, pop=True)
            total_width = 1
            each_diagram_width = (total_width - (total_subfigure_num - 1) * diagram_x_interval) / total_subfigure_num
            default_scale = each_diagram_width / default_sloppiness_width
            common_scale = default_scale * subfigure_scale
            current_cell_height = default_sloppiness_height * common_scale
            current_cell_width = default_sloppiness_width * common_scale
            cell_size = Vector(current_cell_width, current_cell_height)
            total_height = current_cell_height
            cell_bottom_left_list = [
                Vector(current_cell_width * i + diagram_x_interval * min(i - 1, 0), 0)
                for i in range(total_subfigure_num)]
        else:
            raise ValueError()

        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width

        common_data_name = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.data_name, ParameterName.all_data_mode)
        mode_list = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.mode,
            [ParameterName.selected, ParameterName.averaged, ParameterName.optimized], pop=True)

        figure_dict = {}

        for index in range(total_subfigure_num):
            cell_bottom_left = cell_bottom_left_list[index]
            current_mode = mode_list[index]
            if figure_title_list is not None:
                figure_title = figure_title_list[index]
            else:
                figure_title = None
            this_obj_figure_data_parameter_dict = {
                ParameterName.figure_title: figure_title,
                ParameterName.mode: current_mode,
                ParameterName.data_name: common_data_name
            }
            flux_sloppiness_figure = SmallFluxSloppinessDiagram(**{
                ParameterName.bottom_left_offset: cell_bottom_left,
                ParameterName.scale: common_scale,
                ParameterName.figure_data_parameter_dict: this_obj_figure_data_parameter_dict,
            })
            center = flux_sloppiness_figure.calculate_center(flux_sloppiness_figure, common_scale)
            center_bottom_offset = calculate_center_bottom_offset(center, cell_size)
            flux_sloppiness_figure.move_and_scale(bottom_left_offset=center_bottom_offset)
            figure_dict[f'sloppiness_figure_{index}'] = flux_sloppiness_figure

        subfigure_element_dict = {'basic_flux_sloppiness_diagram': figure_dict}
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)

