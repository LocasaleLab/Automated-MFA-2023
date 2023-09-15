from ..common.config import ParameterName, Constant, DataName
from ..common.classes import Vector
from ..figure_elements.element_dict import ElementName, element_dict
from .common_functions import calculate_center_bottom_offset, calculate_subfigure_layout
from ..common.common_figure_materials import FigureConfig, MetabolicNetworkConfig, \
    ModelDataSensitivityDataFigureConfig

Subfigure = element_dict[ElementName.Subfigure]
CompositeFigure = element_dict[ElementName.CompositeFigure]
OptimizationDiagram = element_dict[ElementName.OptimizationDiagram]
ProtocolDiagram = element_dict[ElementName.ProtocolDiagram]
SensitivityAllFluxHeatmap = element_dict[ElementName.SensitivityAllFluxHeatmap]
SensitivityDiagram = element_dict[ElementName.SensitivityDiagram]

common_sensitivity_diagram_scale = 0.35
common_data_sensitivity_diagram_scale = 0.2
common_heatmap_scale = 0.45
heatmap_common_offset = Vector(0.05, -0.03)
common_left_right_column_ratio = (0.32, 0.68)
subfigure_c_d_offset = Vector(0, -0.01)
subfigure_e_f_offset = Vector(0, -0.01)


class SubfigureA(Subfigure):
    subfigure_label = 'a'
    subfigure_title = 'sensitivity_analysis_optimization_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.28
        center = OptimizationDiagram.calculate_center(OptimizationDiagram, scale, ParameterName.sensitivity)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = OptimizationDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.03, -0.015),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.sensitivity,
            ParameterName.background: False,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureB(Subfigure):
    subfigure_label = 'b'
    subfigure_title = 'protocol_diagram_sensitivity'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        scale = 0.5
        center = ProtocolDiagram.calculate_center(ProtocolDiagram, scale, ParameterName.sensitivity)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        data_acquisition_diagram = ProtocolDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + Vector(0.01, -0.005),
            ParameterName.scale: scale,
            ParameterName.mode: ParameterName.sensitivity,
        })

        subfigure_element_dict = {
            data_acquisition_diagram.name: data_acquisition_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'model_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.model_sensitivity
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, 0) + subfigure_c_d_offset)

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'heatmap_for_merge_reversible_reactions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.model_sensitivity
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset:
                subfigure_bottom_left + center_bottom_offset + heatmap_common_offset + subfigure_c_d_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: ModelDataSensitivityDataFigureConfig.title_with_order_prefix[data_name],
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'data_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.data_sensitivity
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(
            bottom_left_offset=center_bottom_offset + Vector(0.01, 0) + subfigure_e_f_offset)

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'heatmap_for_data_sensitivity'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.data_sensitivity
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset:
                subfigure_bottom_left + center_bottom_offset + heatmap_common_offset + subfigure_e_f_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: ModelDataSensitivityDataFigureConfig.title_with_order_prefix[data_name],
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'config_sensitivity_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.config_sensitivity
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.01, 0))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class SubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'heatmap_for_config_sensitivity'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.config_sensitivity
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
                ParameterName.figure_title: ModelDataSensitivityDataFigureConfig.title_with_order_prefix[data_name],
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureC(Subfigure):
    subfigure_label = 'c'
    subfigure_title = 'sensitivity_merge_reversible_reactions_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.merge_reversible_reaction
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.01, 0))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureD(Subfigure):
    subfigure_label = 'd'
    subfigure_title = 'heatmap_for_merge_reversible_reactions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = False
        scale = common_heatmap_scale
        data_name = DataName.merge_reversible_reaction
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureE(Subfigure):
    subfigure_label = 'e'
    subfigure_title = 'sensitivity_combine_consecutive_reactions_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.combine_consecutive_reactions
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.01, -0.))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        # subfigure_element_dict = {}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureF(Subfigure):
    subfigure_label = 'f'
    subfigure_title = 'heatmap_for_combine_consecutive_reactions'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = False
        scale = common_heatmap_scale
        data_name = DataName.combine_consecutive_reactions
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureG(Subfigure):
    subfigure_label = 'g'
    subfigure_title = 'sensitivity_prune_branches_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.prune_branches
        scale = common_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.02, 0.005))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        # subfigure_element_dict = {}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureH(Subfigure):
    subfigure_label = 'h'
    subfigure_title = 'heatmap_for_prune_branches'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = True
        scale = common_heatmap_scale
        data_name = DataName.prune_branches
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset:
                subfigure_bottom_left + center_bottom_offset + heatmap_common_offset + Vector(0, 0.005),
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureI(Subfigure):
    subfigure_label = 'i'
    subfigure_title = 'sensitivity_data_sensitivity_smaller_data_size_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.smaller_data_size
        scale = common_data_sensitivity_diagram_scale

        sensitivity_diagram = SensitivityDiagram(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left,
            ParameterName.scale: scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.mode: mode,
            }
        })

        center = sensitivity_diagram.calculate_center(scale)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)
        sensitivity_diagram.move_and_scale(bottom_left_offset=center_bottom_offset + Vector(0.02, -0.0))

        subfigure_element_dict = {sensitivity_diagram.name: sensitivity_diagram}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureJ(Subfigure):
    subfigure_label = 'j'
    subfigure_title = 'heatmap_for_data_sensitivity'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        cbar = False
        scale = common_heatmap_scale
        data_name = DataName.data_sensitivity
        center = SensitivityAllFluxHeatmap.calculate_center(
            SensitivityAllFluxHeatmap, scale, data_name, cbar)
        center_bottom_offset = calculate_center_bottom_offset(center, subfigure_size)

        sensitivity_all_flux_heatmap = SensitivityAllFluxHeatmap(**{
            ParameterName.bottom_left_offset: subfigure_bottom_left + center_bottom_offset + heatmap_common_offset,
            ParameterName.scale: scale,
            ParameterName.cbar: cbar,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: data_name,
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class OldSubfigureK(Subfigure):
    subfigure_label = 'k'
    subfigure_title = 'sensitivity_data_sensitivity_without_specific_pathway_diagram'

    def __init__(self, subfigure_bottom_left=None, subfigure_size=None):
        mode = DataName.data_without_pathway
        scale = common_data_sensitivity_diagram_scale

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


class OldSubfigureL(Subfigure):
    subfigure_label = 'l'
    subfigure_title = 'heatmap_for_data_sensitivity_with_noise'

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
            },
        })

        subfigure_element_dict = {
            sensitivity_all_flux_heatmap.name: sensitivity_all_flux_heatmap}
        super().__init__(
            subfigure_element_dict, subfigure_bottom_left, subfigure_size,
            subfigure_label=self.subfigure_label, subfigure_title=self.subfigure_title, background=False)


class Figure3(element_dict[ElementName.Figure]):
    figure_label = 'figure_3'
    figure_title = 'Figure 3'

    def __init__(self):
        subfigure_class_list = [
            SubfigureA,
            SubfigureB,
            SubfigureC,
            SubfigureD,
            SubfigureE,
            SubfigureF,
            SubfigureG,
            SubfigureH,
            # SubfigureI,
            # SubfigureJ,
            # SubfigureK,
            # SubfigureL,
        ]

        figure_size = Constant.default_figure_size
        height_to_width_ratio = figure_size[1] / figure_size[0]
        top_margin_ratio = FigureConfig.top_margin_ratio
        side_margin_ratio = FigureConfig.side_margin_ratio

        figure_layout_list = [
            (0.19, [
                (common_left_right_column_ratio[0], 'a'),
                (common_left_right_column_ratio[1], 'b')
            ]),
            (0.29, [
                (common_left_right_column_ratio[0], 'c'),
                (common_left_right_column_ratio[1], 'd')
            ]),
            (0.22, [
                (common_left_right_column_ratio[0], 'e'),
                (common_left_right_column_ratio[1], 'f')
            ]),
            (0.26, [
                (common_left_right_column_ratio[0], 'g'),
                (common_left_right_column_ratio[1], 'h')
            ]),
            # (0.155, [
            #     (common_left_right_column_ratio[0], 'g'),
            #     (common_left_right_column_ratio[1], 'h')
            # ]),
            # (0.125, [
            #     (common_left_right_column_ratio[0], 'i'),
            #     (common_left_right_column_ratio[1], 'j')
            # ]),
            # (0.16, [
            #     (common_left_right_column_ratio[0], 'k'),
            #     (common_left_right_column_ratio[1], 'l')
            # ]),
        ]

        subfigure_obj_list = calculate_subfigure_layout(
            figure_layout_list, subfigure_class_list, height_to_width_ratio, top_margin_ratio, side_margin_ratio)
        subfigure_dict = {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list}
        super().__init__(self.figure_label, subfigure_dict, figure_size=figure_size, figure_title=self.figure_title)

