from .config import ParameterName, TextBox, NetworkGeneralConfig, ZoomBoxConfig, \
    SensitivityConfig, MetaboliteConfig, CommonFigureString, CommonElementConfig, RoundRectangle, Rectangle, Line
from .metabolic_network import MetabolicNetwork, MetabolicNetworkLegend, ExchangeMetabolicNetwork, \
    ModelSensitivityDiagram, FluxRangeTableDiagram, MetabolicNetworkTextComment, DataAvailabilityDiagram, \
    ConfigSensitivityDiagram
from .metabolic_network_elements import MetaboliteElement, ReactionElement, SubnetworkElement
from ..basic_shape_elements.composite_figure_and_axes import CompositeFigure
from ...common.classes import Vector
from ...common.config import DataName
from ..common_functions import default_parameter_extract
from ...common.common_figure_materials import DataSensitivityMetabolicNetworkConfig, MetabolicNetworkConfig, \
    ModelDataSensitivityDataFigureConfig

common_title_config_dict = NetworkGeneralConfig.common_title_config_dict
network_normal_width = NetworkGeneralConfig.network_normal_width
network_normal_height = NetworkGeneralConfig.network_normal_height
network_height_to_width_ratio = NetworkGeneralConfig.network_height_to_width_ratio
title_height = NetworkGeneralConfig.title_height
network_total_height_with_title = NetworkGeneralConfig.network_total_height_with_title
exchange_network_normal_height = NetworkGeneralConfig.exchange_network_normal_height
exchange_network_normal_width = NetworkGeneralConfig.exchange_network_normal_width
exchange_network_total_height_with_title = NetworkGeneralConfig.exchange_network_total_height_with_title


class MetabolicNetworkWithLegend(CompositeFigure):
    @staticmethod
    def calculate_width_and_height(figure_title=None, legend=False, text_comment_config_dict=None):
        if legend or text_comment_config_dict is not None:
            total_width = NetworkGeneralConfig.network_total_width_with_legend
        else:
            total_width = network_normal_width
        if figure_title:
            total_height = network_total_height_with_title
        else:
            total_height = network_height_to_width_ratio
        return total_width, total_height

    @staticmethod
    def calculate_center(self, scale, *args, figure_title=None, legend=False, text_comment_config_dict=None):
        total_width, total_height = self.calculate_width_and_height(figure_title, legend, text_comment_config_dict)
        return Vector(total_width, total_height) * scale / 2

    def __init__(
            self, metabolic_network_config_dict=None, figure_title=None, figure_title_config_dict=None,
            legend=False, metabolic_network_legend_config_dict=None, metabolic_network_text_comment_config_dict=None,
            **kwargs):
        total_width, total_height = self.calculate_width_and_height(
            figure_title, legend, metabolic_network_text_comment_config_dict)
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        subfigure_element_dict = {}
        scale_with_legend = 1
        if metabolic_network_config_dict is None:
            metabolic_network_config_dict = {}
        effective_metabolic_network_config_dict = {
            ParameterName.scale: scale_with_legend,
            **metabolic_network_config_dict,
        }
        metabolic_network_obj = MetabolicNetwork(**effective_metabolic_network_config_dict)
        subfigure_element_dict['metabolic_network'] = {'metabolic_network': metabolic_network_obj}

        if figure_title is not None:
            if figure_title_config_dict is None:
                figure_title_config_dict = {}
            figure_title_obj = TextBox(**{
                **common_title_config_dict,
                ParameterName.string: figure_title,
                ParameterName.width: network_normal_width,
                ParameterName.height: title_height,
                ParameterName.center: Vector(
                    network_normal_width / 2, title_height / 2 + network_height_to_width_ratio),
                **figure_title_config_dict,
            })
            subfigure_element_dict['title'] = {'title': figure_title_obj}

        if legend:
            if metabolic_network_legend_config_dict is None:
                metabolic_network_legend_config_dict = {}
            extra_offset = default_parameter_extract(
                metabolic_network_legend_config_dict, ParameterName.extra_offset, Vector(0, 0), pop=True)
            effective_metabolic_network_legend_config_dict = {
                ParameterName.bottom_left_offset: Vector(network_normal_width, 0) + extra_offset,
                ParameterName.scale: scale_with_legend,
                **metabolic_network_legend_config_dict,
            }
            metabolic_legend_obj = MetabolicNetworkLegend(**effective_metabolic_network_legend_config_dict)
            subfigure_element_dict['metabolic_network_legend'] = {'metabolic_network_legend': metabolic_legend_obj}
        if metabolic_network_text_comment_config_dict is not None:
            extra_offset = default_parameter_extract(
                metabolic_network_text_comment_config_dict, ParameterName.extra_offset, Vector(0, 0), pop=True)
            effective_metabolic_network_text_comment_config_dict = {
                ParameterName.bottom_left_offset: Vector(network_normal_width, 0) + extra_offset,
                ParameterName.scale: scale_with_legend,
                ParameterName.metabolic_network_text_comment_config_dict: metabolic_network_text_comment_config_dict,
            }
            metabolic_text_comment_obj = MetabolicNetworkTextComment(
                **effective_metabolic_network_text_comment_config_dict)
            subfigure_element_dict['metabolic_network_text_comment'] = {
                'metabolic_network_text_comment': metabolic_text_comment_obj}
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)


class ExchangeMetabolicNetworkWithTitle(CompositeFigure):
    @staticmethod
    def calculate_width_and_height(figure_title=None, small_network=False):
        if small_network:
            total_width = NetworkGeneralConfig.exchange_network_smaller_width
        else:
            total_width = exchange_network_normal_width
        if small_network:
            total_height = NetworkGeneralConfig.exchange_network_smaller_height
        elif figure_title:
            total_height = exchange_network_total_height_with_title
        else:
            total_height = exchange_network_normal_height
        return total_width, total_height

    @staticmethod
    def calculate_center(self, scale, *args, figure_title=None, small_network=False):
        total_width, total_height = self.calculate_width_and_height(figure_title, small_network)
        return Vector(total_width, total_height) * scale / 2

    def __init__(
            self, metabolic_network_config_dict=None, small_network=False,
            figure_title=None, figure_title_config_dict=None, **kwargs):
        total_width, total_height = self.calculate_width_and_height(figure_title, small_network)
        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        subfigure_element_dict = {}
        scale_with_legend = 1
        if metabolic_network_config_dict is None:
            metabolic_network_config_dict = {}
        effective_exchange_metabolic_network_config_dict = {
            ParameterName.scale: scale_with_legend,
            ParameterName.small_network: small_network,
            **metabolic_network_config_dict,
        }
        exchange_metabolic_network_obj = ExchangeMetabolicNetwork(**effective_exchange_metabolic_network_config_dict)
        subfigure_element_dict[ParameterName.exchange_network] = {
            ParameterName.exchange_network: exchange_metabolic_network_obj
        }

        if figure_title is not None:
            if figure_title_config_dict is None:
                figure_title_config_dict = {}
            figure_title_obj = TextBox(**{
                **common_title_config_dict,
                ParameterName.string: figure_title,
                ParameterName.width: network_normal_width,
                ParameterName.height: title_height,
                ParameterName.center: Vector(
                    network_normal_width / 2, title_height / 2 + network_height_to_width_ratio),
                **figure_title_config_dict,
            })
            subfigure_element_dict['title'] = {'title': figure_title_obj}

        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(total_width, total_height), background=False, **kwargs)


class NormalAndExchangeTwinNetwork(CompositeFigure):
    metabolic_network_common_scale = 0.5
    total_width = 1
    normal_network_center_x = 0.27
    exchange_network_center_x = 0.77
    top_edge_width = 0.01
    bottom_edge_width = 0.01
    legend_height = 0.08
    legend_offset = Vector(0.14, 0.01)
    total_height = 1
    height_to_width_ratio = total_height / total_width

    @staticmethod
    def calculate_height(self, scale, legend=False, figure_title=True, *args):
        if legend:
            bottom_edge_height = self.legend_height + self.bottom_edge_width
        else:
            bottom_edge_height = self.bottom_edge_width
        network_top = bottom_edge_height + network_normal_height * self.metabolic_network_common_scale
        if figure_title:
            total_height = network_top + title_height
        else:
            total_height = network_top
        return bottom_edge_height, network_top, total_height * scale

    @staticmethod
    def calculate_center(self, scale, legend=False, figure_title=True, *args):
        *_, scaled_total_height = self.calculate_height(self, scale, legend, figure_title)
        return Vector(self.total_width * scale, scaled_total_height) / 2

    @staticmethod
    def calculate_title_center_x(self, scale):
        return Vector(self.normal_network_center_x, self.exchange_network_center_x) * scale

    def __init__(
            self, metabolic_network_config_dict, figure_title=True, legend=False, zoom_in_box=True,
            metabolic_network_legend_config_dict=None, **kwargs):
        normal_network_scale = self.metabolic_network_common_scale
        exchange_network_scale = normal_network_scale + 0.05
        exchange_network_width = NetworkGeneralConfig.exchange_network_smaller_width * exchange_network_scale
        exchange_network_height = NetworkGeneralConfig.exchange_network_smaller_height * exchange_network_scale
        normal_network_height = network_normal_height * normal_network_scale
        normal_network_width = network_normal_width * normal_network_scale
        # normal_network_center_x = self.normal_network_center_x
        # exchange_network_center_x = self.exchange_network_center_x
        normal_network_center_x, exchange_network_center_x = self.calculate_title_center_x(self, 1)
        bottom_edge_height, network_top, total_height = self.calculate_height(self, 1, legend, figure_title)

        self.total_height = total_height
        self.height_to_width_ratio = total_height / self.total_width
        normal_network_left_loc = normal_network_center_x - normal_network_width / 2
        exchange_network_left_loc = exchange_network_center_x - exchange_network_width / 2

        normal_network_bottom_left = Vector(normal_network_left_loc, bottom_edge_height)
        exchange_network_bottom_left = Vector(
            exchange_network_left_loc, bottom_edge_height + (normal_network_height - exchange_network_height) / 2)

        if metabolic_network_config_dict is None:
            metabolic_network_config_dict = {}
        if ParameterName.normal_network in metabolic_network_config_dict:
            assert ParameterName.exchange_network in metabolic_network_config_dict
            normal_network_config_dict = metabolic_network_config_dict[ParameterName.normal_network]
            exchange_network_config_dict = metabolic_network_config_dict[ParameterName.exchange_network]
        else:
            normal_network_config_dict = metabolic_network_config_dict
            exchange_network_config_dict = dict(metabolic_network_config_dict)
        network_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.height: 0.05,
            ParameterName.text_box: False,
        }

        normal_network_obj = MetabolicNetworkWithLegend(**{
            ParameterName.bottom_left_offset: normal_network_bottom_left,
            ParameterName.scale: normal_network_scale,
            ParameterName.metabolic_network_config_dict: normal_network_config_dict,
        })
        exchange_network_obj = ExchangeMetabolicNetworkWithTitle(**{
            ParameterName.bottom_left_offset: exchange_network_bottom_left,
            ParameterName.scale: exchange_network_scale,
            ParameterName.small_network: True,
            ParameterName.metabolic_network_config_dict: exchange_network_config_dict,
        })

        subfigure_element_dict = {
            'network': {
                ParameterName.normal_network: normal_network_obj,
                ParameterName.exchange_network: exchange_network_obj,
            },
        }

        if figure_title:
            title_center_y = network_top + title_height / 2
            normal_network_text_loc = Vector(normal_network_center_x, title_center_y)
            exchange_network_text_loc = Vector(exchange_network_center_x, title_center_y)
            normal_network_title_obj = TextBox(**{
                **network_title_config_dict,
                ParameterName.string: CommonFigureString.major_pathway,
                ParameterName.width: normal_network_width,
                ParameterName.center: normal_network_text_loc,
            })
            exchange_network_title_obj = TextBox(**{
                **network_title_config_dict,
                ParameterName.string: CommonFigureString.exchange_flux,
                ParameterName.width: exchange_network_width,
                ParameterName.center: exchange_network_text_loc,
            })
            subfigure_element_dict[ParameterName.figure_title] = {
                ParameterName.normal_network: normal_network_title_obj,
                ParameterName.exchange_network: exchange_network_title_obj,
            }
        if zoom_in_box:
            zoom_in_obj_dict = self._zoom_box_obj_generator(normal_network_obj, exchange_network_obj)
            subfigure_element_dict[ParameterName.zoom_in_box] = zoom_in_obj_dict

        if legend:
            if metabolic_network_legend_config_dict is None:
                metabolic_network_legend_config_dict = {}
            effective_metabolic_network_legend_config_dict = {
                ParameterName.bottom_left_offset: self.legend_offset,
                ParameterName.scale: normal_network_scale,
                ParameterName.mode: ParameterName.horizontal,
                **metabolic_network_legend_config_dict,
            }
            metabolic_legend_obj = MetabolicNetworkLegend(**effective_metabolic_network_legend_config_dict)
            subfigure_element_dict['metabolic_network_legend'] = {'metabolic_network_legend': metabolic_legend_obj}
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)

    @staticmethod
    def _zoom_box_obj_generator(normal_network_obj, exchange_network_obj):
        common_zoom_box_config = {
            **ZoomBoxConfig.common_zoom_box_config,
        }
        normal_network_box_relative_bottom_left_corner = Vector(0.11, 0)
        normal_network_box_relative_size = Vector(0.78, 0.59)
        normal_network_box_relative_center = normal_network_box_relative_bottom_left_corner \
                                             + normal_network_box_relative_size / 2
        normal_network_box_absolute_center = normal_network_box_relative_center * normal_network_obj.size \
                                             + normal_network_obj.bottom_left
        normal_network_box_absolute_size = normal_network_box_relative_size * normal_network_obj.size
        normal_network_box_top_right_corner = normal_network_box_absolute_center + normal_network_box_absolute_size / 2
        normal_network_box_bottom_right_corner = normal_network_box_absolute_center \
                                                 + Vector(1, -1) * normal_network_box_absolute_size / 2
        normal_top_right_corner_offset = Vector(0.001, -0.02)
        normal_bottom_right_corner_offset = Vector(0.001, 0.02)

        exchange_network_subnetwork_dict = exchange_network_obj.element_dict_by_type_name[
            ParameterName.exchange_network][ParameterName.exchange_network].element_dict_by_type_name[
            ParameterName.subnetwork]
        cell_subnetwork_obj = None
        for key, value in exchange_network_subnetwork_dict.items():
            if key.startswith('cell'):
                cell_subnetwork_obj = value
                break
        current_radius = cell_subnetwork_obj.rectangle.radius
        exchange_network_box_bottom_left_corner = cell_subnetwork_obj.bottom_left
        exchange_network_box_size = cell_subnetwork_obj.size
        exchange_network_box_center = exchange_network_box_bottom_left_corner + exchange_network_box_size / 2
        exchange_network_box_top_left_corner = exchange_network_box_center \
                                               + Vector(-1, 1) * exchange_network_box_size / 2
        exchange_top_left_corner_offset = Vector(-0.001, -0.02)
        exchange_bottom_left_corner_offset = Vector(-0.001, 0.02)

        normal_network_box_obj = RoundRectangle(**{
            **common_zoom_box_config,
            ParameterName.radius: current_radius,
            ParameterName.center: normal_network_box_absolute_center,
            ParameterName.width: normal_network_box_absolute_size.x,
            ParameterName.height: normal_network_box_absolute_size.y,
        })

        exchange_network_box_obj = RoundRectangle(**{
            **common_zoom_box_config,
            ParameterName.radius: current_radius,
            ParameterName.name: 'exchange_network_box',
            ParameterName.center: exchange_network_box_center,
            ParameterName.width: exchange_network_box_size.x,
            ParameterName.height: exchange_network_box_size.y,
        })

        connection_line_obj_list = [
            Line(**{
                **common_zoom_box_config,
                ParameterName.start: normal_network_box_top_right_corner + normal_top_right_corner_offset,
                ParameterName.end: exchange_network_box_top_left_corner + exchange_top_left_corner_offset,
            }),
            Line(**{
                **common_zoom_box_config,
                ParameterName.start: normal_network_box_bottom_right_corner + normal_bottom_right_corner_offset,
                ParameterName.end: exchange_network_box_bottom_left_corner + exchange_bottom_left_corner_offset,
            }),
        ]

        obj_dict = {
            'normal_network_box': normal_network_box_obj,
            'exchange_network_box': exchange_network_box_obj,
            'line1': connection_line_obj_list[0],
            'line2': connection_line_obj_list[1]
        }
        return obj_dict


class NetworkMFAResultComparison(CompositeFigure):
    network_common_scale = 0.5
    total_width = 1
    left_edge_width = 0.01
    bottom_edge_width = 0.02
    inner_x_interval = 0.01
    total_height = 1
    title_height = 0.06
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        network_scale = self.network_common_scale
        left_edge_width = self.left_edge_width
        bottom_edge_width = self.bottom_edge_width
        network_type = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.network_type, ParameterName.normal_network)
        if network_type == ParameterName.normal_network:
            target_class = MetabolicNetworkWithLegend
            network_center = MetabolicNetworkWithLegend.calculate_center(
                MetabolicNetworkWithLegend, network_scale, figure_title=None, legend=False)
        elif network_type == ParameterName.exchange_network:
            target_class = ExchangeMetabolicNetworkWithTitle
            network_center = ExchangeMetabolicNetworkWithTitle.calculate_center(
                ExchangeMetabolicNetworkWithTitle, network_scale, figure_title=False, small_network=False)
        else:
            raise ValueError()
        network_width, network_height = network_center * 2

        inner_x_interval = self.inner_x_interval
        bottom_network_bottom_loc = bottom_edge_width
        network_total_height = bottom_network_bottom_loc + network_height
        left_network_left_loc = left_edge_width
        right_network_left_loc = left_network_left_loc + inner_x_interval + network_width
        top_text_center_y_loc = network_total_height + self.title_height / 2
        top_left_text_x_loc = left_network_left_loc + network_width / 2
        top_right_text_x_loc = right_network_left_loc + network_width / 2
        total_height = network_total_height + self.title_height
        self.total_height = total_height
        self.height_to_width_ratio = total_height / self.total_width

        condition_list = figure_data_parameter_dict[ParameterName.condition]
        condition_name_title_string_dict = figure_data_parameter_dict[ParameterName.name_dict]
        condition_title_list = [condition_name_title_string_dict[condition_name] for condition_name in condition_list]
        metabolic_network_config_for_each_condition_dict = figure_data_parameter_dict[
            ParameterName.metabolic_network_config_dict]
        metabolic_network_config_dict_list = [
            metabolic_network_config_for_each_condition_dict[condition_name] for condition_name in condition_list]

        exchange_diagram_network_obj_list = [
            target_class(**{
                ParameterName.bottom_left_offset: Vector(exchange_network_left_loc, bottom_network_bottom_loc),
                ParameterName.scale: network_scale,
                ParameterName.small_network: False,
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
            }) for exchange_network_left_loc, metabolic_network_config_dict
            in zip([left_network_left_loc, right_network_left_loc], metabolic_network_config_dict_list)
        ]

        condition_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.width: 0.5,
            ParameterName.height: self.title_height,
        }
        condition_title_obj_list = [
            TextBox(**{
                **condition_title_config_dict,
                ParameterName.string: condition_title,
                ParameterName.center: Vector(condition_text_x_loc, top_text_center_y_loc),
            }) for condition_title, condition_text_x_loc
            in zip(condition_title_list, [top_left_text_x_loc, top_right_text_x_loc])
        ]
        subfigure_element_dict = {
            'top_title': {
                key: condition_title_obj
                for key, condition_title_obj in zip(['left', 'right'], condition_title_obj_list)
            },
            'twin_diagram': {
                key: bottom_exchange_network_obj
                for key, bottom_exchange_network_obj in zip(['bottom', 'top'], exchange_diagram_network_obj_list)
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class NormalAndExchangeNetworkMFAResultComparison(CompositeFigure):
    twin_network_common_scale = 0.9
    total_width = 1
    left_edge_width = 0.05
    top_edge_width = 0.01
    bottom_edge_width = 0.02
    inner_y_interval = 0.05
    total_height = 1
    title_height = 0.06
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        twin_network_common_scale = self.twin_network_common_scale
        left_edge_width = self.left_edge_width
        bottom_edge_width = self.bottom_edge_width
        twin_network_common_left_loc = left_edge_width
        bottom_network_bottom_loc = bottom_edge_width
        twin_network_center = NormalAndExchangeTwinNetwork.calculate_center(
            NormalAndExchangeTwinNetwork, twin_network_common_scale, figure_title=False, legend=False)
        twin_network_width, twin_network_height = twin_network_center * 2
        top_network_bottom_loc = bottom_network_bottom_loc + twin_network_height + self.inner_y_interval
        top_network_top = top_network_bottom_loc + twin_network_height
        network_type_title_center_y = top_network_top + 0.5 * self.title_height
        total_height = top_network_top + self.title_height
        self.total_height = total_height
        normal_network_center_x, exchange_network_center_x = NormalAndExchangeTwinNetwork.calculate_title_center_x(
            NormalAndExchangeTwinNetwork, twin_network_common_scale) + left_edge_width

        left_condition_text_center_x = left_edge_width / 2 + 0.01
        bottom_network_center_y = bottom_network_bottom_loc + twin_network_center.y
        top_network_center_y = top_network_bottom_loc + twin_network_center.y

        condition_list = figure_data_parameter_dict[ParameterName.condition]
        condition_name_title_string_dict = figure_data_parameter_dict[ParameterName.name_dict]
        condition_title_list = [condition_name_title_string_dict[condition_name] for condition_name in condition_list]
        metabolic_network_config_for_each_condition_dict = figure_data_parameter_dict[
            ParameterName.metabolic_network_config_dict]
        diagram_class_title_string_list = [CommonFigureString.major_pathway, CommonFigureString.exchange_flux]
        metabolic_network_config_dict_list = [
            metabolic_network_config_for_each_condition_dict[condition_name] for condition_name in condition_list]
        twin_diagram_network_obj_list = [
            NormalAndExchangeTwinNetwork(**{
                ParameterName.bottom_left_offset: Vector(twin_network_common_left_loc, network_bottom_loc),
                ParameterName.scale: twin_network_common_scale,
                ParameterName.figure_title: False,
                ParameterName.zoom_in_box: False,
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
            }) for network_bottom_loc, metabolic_network_config_dict
            in zip([top_network_bottom_loc, bottom_network_bottom_loc], metabolic_network_config_dict_list)
        ]

        condition_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.width: left_edge_width,
            ParameterName.angle: 90,
            ParameterName.height: 0.05,
        }
        network_type_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.width: 0.5,
            ParameterName.height: self.title_height,
        }
        condition_title_obj_list = [
            TextBox(**{
                **condition_title_config_dict,
                ParameterName.string: condition_title,
                ParameterName.center: Vector(left_condition_text_center_x, condition_text_y_loc),
            }) for condition_title, condition_text_y_loc
            in zip(condition_title_list, [top_network_center_y, bottom_network_center_y])
        ]
        network_type_title_obj_list = [
            TextBox(**{
                **network_type_title_config_dict,
                ParameterName.string: diagram_class_title,
                ParameterName.center: Vector(network_text_x_loc, network_type_title_center_y),
            }) for diagram_class_title, network_text_x_loc
            in zip(diagram_class_title_string_list, [normal_network_center_x, exchange_network_center_x])
        ]
        subfigure_element_dict = {
            'top_title': {
                key: diagram_class_title_obj
                for key, diagram_class_title_obj in zip(['bottom', 'top'], network_type_title_obj_list)
            },
            'left_title': {
                key: condition_title_obj
                for key, condition_title_obj in zip(['left', 'right'], condition_title_obj_list)
            },
            'twin_diagram': {
                key: bottom_exchange_network_obj
                for key, bottom_exchange_network_obj in zip(['bottom', 'top'], twin_diagram_network_obj_list)
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class QuadMetabolicNetworkComparison(CompositeFigure):
    quad_metabolic_network_common_scale = 0.45
    total_width = 1
    top_edge_width = 0.05
    bottom_edge_width = 0.02
    inner_x_interval = 0
    # inner_y_interval = -0.01
    inner_y_interval = 0.02
    left_edge_width = total_width - inner_x_interval - 2 * network_normal_width * quad_metabolic_network_common_scale
    total_height = (
                           network_normal_height + exchange_network_normal_height
                   ) * quad_metabolic_network_common_scale + inner_y_interval + top_edge_width + bottom_edge_width
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        network_scale = self.quad_metabolic_network_common_scale
        exchange_network_height = exchange_network_normal_height * network_scale
        normal_network_height = network_normal_height * network_scale
        normal_network_width = network_normal_width * network_scale
        bottom_edge_width = self.bottom_edge_width
        left_edge_width = self.left_edge_width
        top_edge_width = self.top_edge_width
        inner_x_interval = self.inner_x_interval
        inner_y_interval = self.inner_y_interval
        bottom_network_bottom_loc = bottom_edge_width
        top_network_bottom_loc = bottom_network_bottom_loc + inner_y_interval + exchange_network_height
        network_total_height = top_network_bottom_loc + normal_network_height
        left_network_left_loc = left_edge_width
        right_network_left_loc = left_network_left_loc + inner_x_interval + normal_network_width
        left_text_x_loc = left_edge_width / 2 + 0.02
        left_bottom_text_y_loc = bottom_network_bottom_loc + exchange_network_height / 2 - 0.03
        left_top_text_y_loc = top_network_bottom_loc + normal_network_height / 2 + 0.03
        top_text_y_loc = network_total_height + top_edge_width / 2
        top_left_text_x_loc = left_network_left_loc + normal_network_width / 2
        top_right_text_x_loc = right_network_left_loc + normal_network_width / 2
        scale = self.quad_metabolic_network_common_scale

        condition_list = figure_data_parameter_dict[ParameterName.condition]
        condition_name_title_string_dict = figure_data_parameter_dict[ParameterName.name_dict]
        condition_title_list = [condition_name_title_string_dict[condition_name] for condition_name in condition_list]
        metabolic_network_config_for_each_condition_dict = figure_data_parameter_dict[
            ParameterName.metabolic_network_config_dict]
        diagram_class_title_string_list = [CommonFigureString.exchange_flux_wrap, CommonFigureString.major_pathway_wrap]
        condition_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.width: normal_network_width,
            ParameterName.height: top_edge_width,
        }
        diagram_class_title_config_dict = {
            **common_title_config_dict,
            ParameterName.font_size: 12,
            ParameterName.width: left_edge_width,
            ParameterName.height: 0.05,
        }
        condition_title_obj_list = [
            TextBox(**{
                **condition_title_config_dict,
                ParameterName.string: condition_title,
                ParameterName.center: Vector(top_text_x_loc, top_text_y_loc),
            }) for condition_title, top_text_x_loc
            in zip(condition_title_list, [top_left_text_x_loc, top_right_text_x_loc])
        ]
        diagram_class_title_obj_list = [
            TextBox(**{
                **diagram_class_title_config_dict,
                ParameterName.string: diagram_class_title,
                ParameterName.center: Vector(left_text_x_loc, left_text_y_loc),
            }) for diagram_class_title, left_text_y_loc
            in zip(diagram_class_title_string_list, [left_bottom_text_y_loc, left_top_text_y_loc])
        ]
        metabolic_network_config_dict_list = [
            metabolic_network_config_for_each_condition_dict[condition_name] for condition_name in condition_list]
        bottom_exchange_network_obj_list = [
            ExchangeMetabolicNetworkWithTitle(**{
                ParameterName.bottom_left_offset: Vector(network_left_loc + 0.022, bottom_network_bottom_loc),
                ParameterName.scale: scale,
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
            }) for network_left_loc, metabolic_network_config_dict
            in zip([left_network_left_loc, right_network_left_loc], metabolic_network_config_dict_list)
        ]
        top_normal_network_obj_list = [
            MetabolicNetworkWithLegend(**{
                ParameterName.bottom_left_offset: Vector(network_left_loc, top_network_bottom_loc),
                ParameterName.scale: scale,
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
            }) for network_left_loc, metabolic_network_config_dict
            in zip([left_network_left_loc, right_network_left_loc], metabolic_network_config_dict_list)
        ]

        subfigure_element_dict = {
            'top_title': {
                key: condition_title_obj
                for key, condition_title_obj in zip(['left', 'right'], condition_title_obj_list)
            },
            'left_title': {
                key: diagram_class_title_obj
                for key, diagram_class_title_obj in zip(['bottom', 'top'], diagram_class_title_obj_list)
            },
            'bottom_exchange_network': {
                key: bottom_exchange_network_obj
                for key, bottom_exchange_network_obj in zip(['left', 'right'], bottom_exchange_network_obj_list)
            },
            'top_normal_network': {
                key: top_normal_network_obj
                for key, top_normal_network_obj in zip(['left', 'right'], top_normal_network_obj_list)
            }
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class SingleSensitivityDiagram(CompositeFigure):
    def calculate_center(self, scale, *args):
        return self.total_size / 2 * scale

    def __init__(self, figure_data_parameter_dict, separate=False, **kwargs):
        # mode = figure_data_parameter_dict.pop(ParameterName.mode)
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, None, pop=True)
        background = default_parameter_extract(figure_data_parameter_dict, ParameterName.background, True, pop=True)
        # model_sensitivity_set = {
        #     DataName.merge_reversible_reaction, DataName.combine_consecutive_reactions, DataName.prune_branches}
        # data_and_boundary_sensitivity_set = {
        #     DataName.smaller_data_size, DataName.data_without_pathway, DataName.different_constant_flux}
        model_sensitivity_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
        data_sensitivity_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_dict
        config_sensitivity_dict = ModelDataSensitivityDataFigureConfig.config_sensitivity_dict
        data_and_boundary_sensitivity_dict = {**data_sensitivity_dict, DataName.different_constant_flux: None}
        if mode in model_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'model_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                **figure_data_parameter_dict,
            }
            diagram_class = ModelSensitivityDiagram
        elif mode in data_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'data_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                ParameterName.separate: separate,
                **figure_data_parameter_dict,
            }
            diagram_class = DataAvailabilityDiagram
        elif mode in config_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'config_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                **figure_data_parameter_dict,
            }
            diagram_class = ConfigSensitivityDiagram
        elif mode in data_and_boundary_sensitivity_dict:
            if mode == DataName.smaller_data_size:
                metabolic_network_config_dict = {
                    ParameterName.metabolite_data_sensitivity_state_dict:
                        DataSensitivityMetabolicNetworkConfig.smaller_size_data_sensitivity_dict,
                    ParameterName.input_metabolite_set: MetabolicNetworkConfig.common_input_metabolite_set,
                }
            elif mode == DataName.data_without_pathway:
                metabolic_network_config_dict = {
                    ParameterName.metabolite_data_sensitivity_state_dict:
                        DataSensitivityMetabolicNetworkConfig.remove_pathway_data_sensitivity_dict,
                    ParameterName.mid_data_metabolite_set:
                        MetabolicNetworkConfig.common_experimental_mid_metabolite_set,
                }
            elif mode == DataName.different_constant_flux:
                metabolic_network_config_dict = {
                    ParameterName.reaction_text_dict:
                        DataSensitivityMetabolicNetworkConfig.different_constant_flux_name_dict,
                    ParameterName.boundary_flux_set: set(
                        DataSensitivityMetabolicNetworkConfig.different_constant_flux_name_dict),
                }
            else:
                raise ValueError()
            effective_sensitivity_diagram_config_dict = {
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
                ParameterName.legend: True,
                ParameterName.metabolic_network_legend_config_dict: {ParameterName.mode: mode},
            }
            diagram_class = MetabolicNetworkWithLegend
        # elif mode == DataName.different_flux_range:
        #     effective_sensitivity_diagram_config_dict = {}
        #     diagram_class = FluxRangeTableDiagram
        else:
            raise ValueError()
        sensitivity_diagram_obj = diagram_class(**effective_sensitivity_diagram_config_dict)
        total_size = sensitivity_diagram_obj.size
        subfigure_element_dict = {'diagram': {'diagram': sensitivity_diagram_obj, }, }
        # if mode in data_and_boundary_sensitivity_dict:
        #     raw_total_height = total_size.y
        #     total_width = total_size.x
        #     title_text_height = 0.08
        #     total_height = raw_total_height + title_text_height
        #     figure_title_str = ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode]
        #     figure_title_config_dict = {
        #         **SensitivityConfig.title_text_config,
        #         ParameterName.font_size: MetaboliteConfig.font_size + 25,
        #         ParameterName.string: figure_title_str,
        #         ParameterName.width: total_width,
        #         ParameterName.height: title_text_height,
        #         ParameterName.center: Vector(total_width / 2 - 0.02, raw_total_height + title_text_height / 2)
        #     }
        #     title_text_obj = TextBox(**figure_title_config_dict)
        #     subfigure_element_dict['title'] = {'title': title_text_obj}
        #     total_size = Vector(total_width, total_height)
        if background:
            background_config_dict = {
                **CommonElementConfig.simulated_background_config_dict,
                ParameterName.center: total_size / 2,
                ParameterName.width: total_size.x,
                ParameterName.height: total_size.y,
            }
            subfigure_element_dict[ParameterName.background] = {
                ParameterName.background: RoundRectangle(**background_config_dict)
            }
        self.total_size = total_size
        self.total_width, self.total_height = self.total_size
        self.height_to_width_ratio = total_size[1] / total_size[0]
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class ComplexSensitivityDiagram(CompositeFigure):
    def calculate_center(self, scale, *args):
        return self.total_size / 2 * scale

    class Config(object):
        # model_sensitivity config:
        common_model_sensitivity_diagram_scale = 0.9
        model_sensitivity_size = Vector(0.8, 0.7)
        merge_reversible_reactions_center_x = 0.2
        combine_consecutive_reactions_center_x = 0.6
        upper_center_y = 0.53
        prune_branches_center_x = 0.4
        bottom_center_y = 0.17
        merge_reversible_reactions_target_center = Vector(merge_reversible_reactions_center_x, upper_center_y)
        combine_consecutive_reactions_target_center = Vector(combine_consecutive_reactions_center_x, upper_center_y)
        prune_branches_target_center = Vector(prune_branches_center_x, bottom_center_y)
        model_sensitivity_target_center_dict = {
            DataName.merge_reversible_reaction: merge_reversible_reactions_target_center,
            DataName.combine_consecutive_reactions: combine_consecutive_reactions_target_center,
            DataName.prune_branches: prune_branches_target_center,
        }

        # data_sensitivity config:
        common_data_sensitivity_diagram_scale = 0.8
        data_sensitivity_size = Vector(0.8, 0.67)
        top_panel_center_x = data_sensitivity_size.x / 2
        left_panel_center_x = 0.17
        smaller_data_size_center_y = 0.54
        data_without_pathway_center_y = 0.21
        right_panel_center_x = 0.55
        # right_center_y = 0.35
        smaller_data_size_target_center = Vector(top_panel_center_x, smaller_data_size_center_y)
        data_without_pathway_target_center = Vector(left_panel_center_x, data_without_pathway_center_y)
        compartmental_data_target_center = Vector(right_panel_center_x, data_without_pathway_center_y)
        data_sensitivity_target_center_dict = {
            DataName.smaller_data_size: smaller_data_size_target_center,
            DataName.data_without_pathway: data_without_pathway_target_center,
            DataName.compartmental_data: compartmental_data_target_center,
        }

        # config_sensitivity config:
        #################### Config with different flux range data #################
        # common_config_sensitivity_diagram_scale = 0.9
        # config_sensitivity_size = Vector(0.7, 0.4)
        # left_panel_center_x = 0.2
        # right_panel_center_x = 0.53
        # common_center_y = 0.3
        # different_constant_flux_target_center = Vector(left_panel_center_x, common_center_y)
        # different_flux_range_target_center = Vector(right_panel_center_x, common_center_y)
        #############################################################################
        common_config_sensitivity_diagram_scale = 1
        config_sensitivity_size = Vector(0.6, 0.4)
        center_x = config_sensitivity_size[0] / 2
        common_center_y = 0.3
        different_constant_flux_target_center = Vector(center_x, common_center_y)
        config_sensitivity_target_center_dict = {
            DataName.different_constant_flux: different_constant_flux_target_center,
        }

    @staticmethod
    def _arrange_subfigure_layout(content_dict, target_center_dict, common_scale, subfigure_obj_dict):
        for each_subfigure_mode in content_dict.keys():
            common_figure_parameter_dict = {
                ParameterName.bottom_left_offset: target_center_dict[each_subfigure_mode],
                ParameterName.scale: common_scale,
                ParameterName.separate: False,
                ParameterName.figure_data_parameter_dict: {
                    ParameterName.mode: each_subfigure_mode,
                    ParameterName.background: True,
                }
            }
            current_subfigure_diagram_obj = SingleSensitivityDiagram(**common_figure_parameter_dict)
            raw_center = current_subfigure_diagram_obj.calculate_center(common_scale)
            current_subfigure_diagram_obj.move_and_scale(bottom_left_offset=-raw_center)
            subfigure_obj_dict[each_subfigure_mode] = current_subfigure_diagram_obj

    def __init__(self, figure_data_parameter_dict, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, pop=True)
        subfigure_obj_dict = {}
        if mode == DataName.model_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
            target_center_dict = self.Config.model_sensitivity_target_center_dict
            scale = self.Config.common_model_sensitivity_diagram_scale
            total_size = self.Config.model_sensitivity_size
        elif mode == DataName.data_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_dict
            target_center_dict = self.Config.data_sensitivity_target_center_dict
            scale = self.Config.common_data_sensitivity_diagram_scale
            total_size = self.Config.data_sensitivity_size
        elif mode == DataName.config_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.config_sensitivity_dict
            target_center_dict = self.Config.config_sensitivity_target_center_dict
            scale = self.Config.common_config_sensitivity_diagram_scale
            total_size = self.Config.config_sensitivity_size
        else:
            raise ValueError()
        self._arrange_subfigure_layout(content_dict, target_center_dict, scale, subfigure_obj_dict)
        total_width, raw_total_height = total_size
        title_text_height = 0.08
        total_height = raw_total_height + title_text_height
        figure_title_str = ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode]
        title_config_dict = {
            **SensitivityConfig.title_text_config,
            ParameterName.font_size: MetaboliteConfig.font_size + 10,
            ParameterName.string: figure_title_str,
            ParameterName.width: total_width,
            ParameterName.height: title_text_height,
            ParameterName.center: Vector(total_width / 2 - 0.02, raw_total_height + title_text_height / 2)
        }
        subfigure_element_dict = {
            'diagram': subfigure_obj_dict,
            ParameterName.figure_title: {ParameterName.figure_title: TextBox(**title_config_dict)}
        }
        total_size = Vector(total_width, total_height)
        self.total_size = total_size
        self.total_width, self.total_height = total_size
        self.height_to_width_ratio = total_size[1] / total_size[0]
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class SensitivityDiagram(CompositeFigure):
    def __new__(cls, figure_data_parameter_dict, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode)
        complex_data_name_set = {
            DataName.model_sensitivity, DataName.data_sensitivity, DataName.config_sensitivity}
        if mode in complex_data_name_set:
            target_obj = ComplexSensitivityDiagram(figure_data_parameter_dict, **kwargs)
        else:
            target_obj = SingleSensitivityDiagram(figure_data_parameter_dict, separate=True, **kwargs)
        return target_obj


class ElementName(object):
    MetaboliteNode = 'MetaboliteNode'
    Reaction = 'Reaction'
    Subnetwork = 'Subnetwork'
    MetabolicNetwork = 'MetabolicNetwork'
    MetabolicNetworkLegend = 'MetabolicNetworkLegend'
    MetabolicNetworkWithLegend = 'MetabolicNetworkWithLegend'
    ExchangeMetabolicNetworkWithTitle = 'ExchangeMetabolicNetworkWithTitle'
    QuadMetabolicNetworkComparison = 'QuadMetabolicNetworkComparison'
    NormalAndExchangeTwinNetwork = 'NormalAndExchangeTwinNetwork'
    NetworkMFAResultComparison = 'ExchangeNetworkMFAResultComparison'
    NormalAndExchangeNetworkMFAResultComparison = 'NormalAndExchangeNetworkMFAResultComparison'
    SensitivityDiagram = 'SensitivityDiagram'


class Elements(object):
    MetaboliteNode = MetaboliteElement
    Reaction = ReactionElement
    Subnetwork = SubnetworkElement
    MetabolicNetwork = MetabolicNetwork
    MetabolicNetworkLegend = MetabolicNetworkLegend
    MetabolicNetworkWithLegend = MetabolicNetworkWithLegend
    ExchangeMetabolicNetworkWithTitle = ExchangeMetabolicNetworkWithTitle
    QuadMetabolicNetworkComparison = QuadMetabolicNetworkComparison
    NormalAndExchangeTwinNetwork = NormalAndExchangeTwinNetwork
    NetworkMFAResultComparison = NetworkMFAResultComparison
    NormalAndExchangeNetworkMFAResultComparison = NormalAndExchangeNetworkMFAResultComparison
    SensitivityDiagram = SensitivityDiagram


element_dict = {
    ElementName.MetaboliteNode: MetaboliteElement,
    ElementName.Reaction: ReactionElement,
    ElementName.Subnetwork: SubnetworkElement,
    ElementName.MetabolicNetwork: MetabolicNetwork,
    ElementName.MetabolicNetworkLegend: MetabolicNetworkLegend,
    ElementName.MetabolicNetworkWithLegend: MetabolicNetworkWithLegend,
    ElementName.ExchangeMetabolicNetworkWithTitle: ExchangeMetabolicNetworkWithTitle,
    ElementName.QuadMetabolicNetworkComparison: QuadMetabolicNetworkComparison,
    ElementName.NormalAndExchangeTwinNetwork: NormalAndExchangeTwinNetwork,
    ElementName.NormalAndExchangeNetworkMFAResultComparison: NormalAndExchangeNetworkMFAResultComparison,
    ElementName.NetworkMFAResultComparison: NetworkMFAResultComparison,
    ElementName.SensitivityDiagram: SensitivityDiagram,
}
