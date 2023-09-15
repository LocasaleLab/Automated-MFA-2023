from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout, single_subfigure_layout
from ..common.common_figure_materials import MetabolicNetworkConfig, FigureConfig, CommonFigureString
from .figure_3 import common_heatmap_scale, heatmap_common_offset, common_left_right_column_ratio


Subfigure = element_dict[ElementName.Subfigure]
CompositeFigure = element_dict[ElementName.CompositeFigure]
NoisyDataDiagram = element_dict[ElementName.NoisyDataDiagram]
ProtocolDiagram = element_dict[ElementName.ProtocolDiagram]
SensitivityAllFluxHeatmap = element_dict[ElementName.SensitivityAllFluxHeatmap]
SensitivityDiagram = element_dict[ElementName.SensitivityDiagram]

common_data_sensitivity_diagram_scale = 0.2


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'sensitivity_analysis_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.5
        center = NoisyDataDiagram.calculate_center(NoisyDataDiagram, scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = NoisyDataDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.03, -0.015),
            ParameterName.scale: scale,
            ParameterName.background: False,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'heatmap_for_data_sensitivity_noise'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.data_sensitivity_with_noise
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: CommonFigureString.data_sensitivity_with_noise_with_order_prefix,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'heatmap_for_different_constant_flux_with_noise'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.different_constant_flux_with_noise
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: CommonFigureString.config_sensitivity_with_noise_with_order_prefix,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'sensitivity_boundary_sensitivity_different_constant_flux_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.different_constant_flux
        scale = common_data_sensitivity_diagram_scale + 0.07

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.02, -0.02))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'heatmap_for_different_constant_flux'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = False
        scale = common_heatmap_scale
        data_name = DataName.different_constant_flux
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: CommonFigureString.precise_mid_data,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'heatmap_for_different_constant_flux_with_noise'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = False
        scale = common_heatmap_scale
        data_name = DataName.different_constant_flux_with_noise
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: CommonFigureString.noised_mid_data,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'sensitivity_for_different_flux_range_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.different_flux_range
        scale = 0.45

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.01, 0.01))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'heatmap_for_different_flux_range'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.different_flux_range
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: CommonFigureString.precise_mid_data,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class FigureS3(element_dict[ElementName.Figure]):
    figure_label = 'figure_s3'
    figure_title = 'Figure S3'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            # SubfigureD,
            # SubfigureE,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        # b_c_height = 0.17
        # b_c_height = 0.15
        # a_height = 2 * b_c_height
        # d_e_height = 0.18
        a_height = 0.21
        b_c_height = 0.2
        d_e_height = 0.23

        figure_layout_list = [
            (a_height, [
                (1, 'a'),
            ]),
            (b_c_height, [
                (1, 'b'),
            ]),
            (b_c_height, [
                (1, 'c'),
            ]),
            # (d_e_height, [
            #     (common_left_right_column_ratio[0], 'd'),
            #     (common_left_right_column_ratio[1], 'e'),
            # ]),
        ]
        # figure_layout_list = [
        #     (a_height, [
        #         (common_left_right_column_ratio[0], 'a'),
        #     ]),
        #     (d_e_height, [
        #         (common_left_right_column_ratio[0], 'd'),
        #         (common_left_right_column_ratio[1], 'e'),
        #     ]),
        # ]
        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)

        # subfigure_b_c_size = Vector(common_left_right_column_ratio[1], b_c_height)
        # subfigure_b_center = subfigure_b_c_size / 2 + Vector(common_left_right_column_ratio[0], 0)
        # subfigure_c_center = subfigure_b_c_size / 2 + Vector(common_left_right_column_ratio[0], b_c_height)
        #
        # subfigure_obj_list.extend([
        #     single_subfigure_layout(
        #         subfigure_b_center, subfigure_b_c_size, SubfigureB, height_to_width_ratio, top_margin_ratio,
        #         side_margin_ratio),
        #     single_subfigure_layout(
        #         subfigure_c_center, subfigure_b_c_size, SubfigureC, height_to_width_ratio, top_margin_ratio,
        #         side_margin_ratio),
        # ])

        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

