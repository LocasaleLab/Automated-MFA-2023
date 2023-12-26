from .config import ParameterName, Vector, FontWeight, CompositeFigure, DataName, \
    CommonElementConfig, CommonFigureString, default_parameter_extract, TextBox, calculate_center_bottom_offset
from ..diagram_elements.axis_diagrams.flux_sloppiness_diagram import BasicFluxSloppinessDiagram


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
        total_subfigure_num = 3
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

        for index in range(3):
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

