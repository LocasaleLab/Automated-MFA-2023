from ..common.config import DataName, ParameterName, Figure as RawFigure, Vector, calculate_center_bottom_offset
from ..common.common_figure_materials import MetabolicNetworkConfig, PHGDHRawMaterials, \
    CommonFigureString
from ..common.elements import Elements

Subfigure = Elements.Subfigure
common_scale = 0.7
LossOfAveragedSolutionsDiagram = Elements.LossOfAveragedSolutionsDiagram


def common_example_network_generator(subfigure_bottom_left, subfigure_size, scale, mode, legend):
    metabolic_network_config_dict = {
        ParameterName.bottom_left_offset: subfigure_bottom_left,
        ParameterName.scale: scale,
        ParameterName.figure_data_parameter_dict: {
            ParameterName.mode: mode,
            ParameterName.legend: legend,
        }
    }
    loss_of_averaged_solutions_example_network = LossOfAveragedSolutionsDiagram(**metabolic_network_config_dict)

    center = loss_of_averaged_solutions_example_network.calculate_center(scale)
    bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
    loss_of_averaged_solutions_example_network.move_and_scale(
        bottom_left_offset=bottom_offset + Vector(0, 0))
    return loss_of_averaged_solutions_example_network


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'loss_of_averaged_solutions_example_network_real_flux'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_scale
        loss_of_averaged_solutions_example_network = common_example_network_generator(
            subfigure_bottom_left, subfigure_size, scale, 0, False)

        subfigure_element_dict = {
            loss_of_averaged_solutions_example_network.name: loss_of_averaged_solutions_example_network}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'loss_of_averaged_solutions_example_network_optimized_solution_1'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_scale
        loss_of_averaged_solutions_example_network = common_example_network_generator(
            subfigure_bottom_left, subfigure_size, scale, 1, False)

        subfigure_element_dict = {
            loss_of_averaged_solutions_example_network.name: loss_of_averaged_solutions_example_network}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'loss_of_averaged_solutions_example_network_optimized_solution_2'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_scale
        loss_of_averaged_solutions_example_network = common_example_network_generator(
            subfigure_bottom_left, subfigure_size, scale, 2, False)

        subfigure_element_dict = {
            loss_of_averaged_solutions_example_network.name: loss_of_averaged_solutions_example_network}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'loss_of_averaged_solutions_example_network_averaged_solution'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = common_scale
        loss_of_averaged_solutions_example_network = common_example_network_generator(
            subfigure_bottom_left, subfigure_size, scale, 3, True)

        subfigure_element_dict = {
            loss_of_averaged_solutions_example_network.name: loss_of_averaged_solutions_example_network}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size, subfigure_label=self.subfigure_label,
            subfigure_title=self.subfigure_title, background=False)


class Figure(RawFigure):
    figure_label = 'figure_loss_of_averaged_solutions'
    figure_size = Vector(8, 12)

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
        ]

        figure_layout_list = [
            (0.2, [(0.8, 'a')]),
            (0.2, [(0.8, 'b')]),
            (0.2, [(0.8, 'c')]),
            (0.24, [(0.8, 'd')]),
        ]
        super().__init__(
            self.figure_label, subfigure_class_list, figure_layout_list, {})
