from ..common.third_party_packages import np
from ..common.classes import Vector, VerticalAlignment, HorizontalAlignment, FontWeight, SegmentedLinearMappers
from ..common.color import ColorConfig, TextConfig, ZOrderConfig
from ..common.config import ParameterName as GeneralParameterName
from ..common.common_figure_materials import CommonElementConfig
from ..basic_shape_elements import Region, TextBox, Capsule, Circle, Arrow, ArcArrow, ArcPathArrow, \
    BentArrow, BrokenArrow, Rectangle, RoundRectangle, ElementName, CompositeFigure, ChevronArrow, Line
from ..common.common_functions import convert_theta_to_coordinate, basic_shape_parameter_set, construct_full_name, \
    load_required_parameter, text_parameter_set, calculate_bottom_left_point, calculate_top_right_point, \
    numbered_even_sequence, default_parameter_extract


class ParameterName(GeneralParameterName):
    blunt = 'blunt'
    # arrow = 'arrow' # Defined in parent parameter name
    common = 'common'

    branch = 'branch'
    cycle = 'cycle'
    path_cycle = 'path_cycle'
    bent = 'bent'
    broken = 'broken'

    metabolite = 'metabolite'
    reaction = 'reaction'
    subnetwork = 'subnetwork'
    other_text = 'other_text'

    # Suffix
    capsule_suffix = 'capsule'
    mixed_mid_circle_suffix = 'mixed_mid_circle'
    biomass_flux_suffix = 'biomass_flux'
    text_suffix = 'text'
    arrow_suffix_dict = {
        'Arrow': 'arrow',
        'ArcArrow': 'arc_arrow',
        'ArcPathArrow': 'arc_path_arrow',
        'BentArrow': 'bent_arrow'
    }


p = 0.01
t = 0.0001
z_order_increment = ZOrderConfig.z_order_increment


class ModeName(object):
    merge_reversible_reaction = 'merge_reversible_reaction'
    combine_consecutive_reactions = 'combine_consecutive_reactions'
    prune_branches = 'prune_branches'
    compartmental_data = 'compartmental_data'

    smaller_data_size = 'smaller_data_size'
    raw_model_raw_data = 'raw_model_raw_data'
    raw_model_all_data = 'raw_model_all_data'
    medium_data = 'medium_data'
    few_data = 'few_data'

    data_without_pathway = 'data_without_pathway'
    data_without_ppp = 'data_without_ppp'
    data_without_tca = 'data_without_tca'
    data_without_aa = 'data_without_aa'
    medium_data_without_combination = 'medium_data_without_combination'

    different_constant_flux = 'different_constant_flux'
    different_flux_range = 'different_flux_range'


class LegendConfig(object):
    legend_width = 0.35
    legend_horizontal_width = 1.5
    legend_each_row_height = 0.05
    background_color = ColorConfig.gray

    common_text_param_dict = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: 10,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        # ParameterName.text_box: True
    }


class NetworkGeneralConfig(object):
    network_normal_width = 1
    horizontal_legend_width = 1
    network_total_width_with_legend = network_normal_width + LegendConfig.legend_width
    methionine_network_total_width = 1.5
    network_height_to_width_ratio = 0.88
    network_normal_height = 0.88
    title_height = 0.08
    network_total_height_with_title = network_normal_height + title_height
    # exchange_network_normal_width = 0.85
    exchange_network_normal_width = 0.97
    exchange_network_normal_height = 0.77
    exchange_network_height_to_width_ratio = exchange_network_normal_height / exchange_network_normal_width
    exchange_network_total_height_with_title = exchange_network_normal_height + title_height
    exchange_network_smaller_width = 0.72
    exchange_network_smaller_height = 0.51
    exchange_network_smaller_height_to_width_ratio = exchange_network_smaller_height / exchange_network_smaller_width
    biomass_str = 'BIOMASS_REACTION'
    display_value_format_string = '{:.1f}'

    common_title_config_dict = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: 25,
        # ParameterName.text_box: True,
    }


class MetaboliteConfig(object):
    # width = 9 * p
    # height = 4 * p
    width = 7.3 * p
    height = 3 * p
    edge_width = None

    font = TextConfig.main_text_font
    font_color = ColorConfig.metabolite_text_color
    font_size = 11
    smaller_font_size = font_size - 0.6
    smallest_font_size = font_size - 1.2
    vertical_alignment = VerticalAlignment.center_baseline
    z_order = ZOrderConfig.default_axis_z_order
    text_z_order = z_order + z_order_increment

    normal_face_color = ColorConfig.normal_metabolite_color
    input_metabolite_face_color = ColorConfig.input_metabolite_color
    c13_metabolite_face_color = ColorConfig.c13_metabolite_color
    mid_face_color = ColorConfig.mid_metabolite_color
    invalid_face_color = ColorConfig.gray
    raw_model_raw_data_color = ColorConfig.mid_metabolite_color
    medium_data_color = ColorConfig.c13_metabolite_color
    few_data_color = ColorConfig.metabolite_few_data_set
    data_without_ppp_color = ColorConfig.metabolite_darker_blue
    data_without_tca_color = ColorConfig.c13_metabolite_color
    data_without_aa_color = ColorConfig.metabolite_few_data_set

    interval_to_metabolite_ratio = {
        ParameterName.blunt: {
            ParameterName.horizontal: 0.31 * p,
            ParameterName.vertical: 0.32 * p,
        },
        ParameterName.arrow: {
            ParameterName.horizontal: 0.21 * p,
            ParameterName.vertical: 0.22 * p,
        }
    }


class MixedMIDCircle(object):
    radius = 0.65 * p
    center_offset = Vector(
        MetaboliteConfig.width * 0.4, MetaboliteConfig.height * 0.43)
    face_color = ColorConfig.mixed_mid_metabolite_circle_color
    edge_width = None
    z_order = MetaboliteConfig.z_order + 2 * z_order_increment


class BiomassFluxArrow(object):
    tail_offset = Vector(
        MetaboliteConfig.width * 0.38, -MetaboliteConfig.height * 0.25)
    head_offset = Vector(
        MetaboliteConfig.width * 0.58, -MetaboliteConfig.height * 0.53)
    head_width = 1.2 * p
    stem_width = 0.6 * p
    head_len_width_ratio = 0.75
    edge_width = None
    face_color = ColorConfig.biomass_metabolite_arrow_color
    z_order = MetaboliteConfig.z_order + z_order_increment


other_display_text_config = {
    ParameterName.font: TextConfig.main_text_font,
    ParameterName.font_size: MetaboliteConfig.font_size,
    ParameterName.width: 0.15,
    ParameterName.height: 0.05,
    ParameterName.horizontal_alignment: HorizontalAlignment.center,
    ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    ParameterName.font_weight: FontWeight.bold,
    ParameterName.z_order: MetaboliteConfig.text_z_order + z_order_increment,
    # ParameterName.text_box: True
}


class ReactionConfig(object):
    # head_width = 3 * p
    # stem_width = 1.5 * p
    # head_width = 1.6 * p
    head_width = 1.6 * p
    # stem_width = 0.7 * p
    stem_width = head_width / 2
    head_len_width_ratio = 0.85
    edge_width = None
    z_order = ZOrderConfig.default_axis_z_order - 2 * z_order_increment
    bent_reaction_radius = 4 * p

    reaction_gap = 2 * stem_width
    dash_reaction_solid_gap_ratio = (0.9 * p, 0.35 * p)
    normal_face_color = ColorConfig.normal_reaction_color
    boundary_face_color = ColorConfig.boundary_reaction_color

    display_text_width = MetaboliteConfig.width
    display_text_height = MetaboliteConfig.height
    display_text_horizontal_distance = 1 * p
    display_text_vertical_distance = 1.2 * p

    default_display_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: MetaboliteConfig.font_size - 1,
        ParameterName.width: display_text_width,
        ParameterName.height: display_text_height,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.z_order: MetaboliteConfig.text_z_order + z_order_increment
    }


class SubnetworkConfig(object):
    class Rectangle(object):
        face_color = ColorConfig.normal_reaction_color
        edge_width = None
        z_order = ZOrderConfig.default_patch_z_order
        radius = 2 * p

    class Text(object):
        width = 10 * p
        height = 5 * p

        # text_top_margin = 1.25 * p
        text_top_margin = 2 * p
        lower_text_top_margin = 7 * p
        # text_left_margin = 1.25 * p
        text_left_margin = 2 * p

        font = TextConfig.main_text_font
        font_color = ColorConfig.subnetwork_text_color
        font_size = 13
        font_weight = 'bold'
        vertical_alignment = VerticalAlignment.top
        horizontal_alignment = HorizontalAlignment.left
        z_order = ZOrderConfig.default_patch_z_order + z_order_increment


class TextCommentConfig(object):
    comment_text_common_param_dict = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_size: 15,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.font_weight: FontWeight.bold,
    }


class ZoomBoxConfig(object):
    common_zoom_box_config = {
        ParameterName.radius: SubnetworkConfig.Rectangle.radius,
        ParameterName.z_order: ZOrderConfig.default_legend_z_order,
        ParameterName.face_color: None,
        ParameterName.edge_width: 1.2,
        ParameterName.edge_color: ColorConfig.normal_blue,
    }


def collect_and_find_flux_value_range(reaction_list_with_flux):
    complete_net_flux_value_list = []
    for reaction_name, reaction_obj in reaction_list_with_flux.content_list_pair:
        if reaction_obj.net_value is not None:
            complete_net_flux_value_list.append(reaction_obj.net_value)
    if len(complete_net_flux_value_list) == 0:
        return 0, 1000
    else:
        complete_net_flux_value_array = np.array(complete_net_flux_value_list)
        min_net_flux_value = np.min(complete_net_flux_value_array)
        max_net_flux_value = np.max(complete_net_flux_value_array)
        return min_net_flux_value, max_net_flux_value


class BaseFluxValueMapper(object):
    def __init__(self, input_ratio_output_value_dict, reaction_list_with_flux):
        self.min_net_flux_value, self.max_net_flux_value = collect_and_find_flux_value_range(
            reaction_list_with_flux)
        self.net_flux_diff = self.max_net_flux_value - self.min_net_flux_value
        output_conversion_func_dict = {}
        assert 0 in input_ratio_output_value_dict and 1 in input_ratio_output_value_dict
        last_input_value = None
        last_output_value = None
        for input_ratio, output_value in input_ratio_output_value_dict.items():
            if input_ratio == 0:
                last_input_value = self.min_net_flux_value
                last_output_value = output_value
                continue
            elif input_ratio == 1:
                current_input_value = self.max_net_flux_value
            else:
                current_input_value = input_ratio * self.net_flux_diff + self.min_net_flux_value
            current_output_diff = output_value - last_output_value
            # output_conversion_func_dict[current_input_value] = lambda x: \
            #     last_output_value + \
            #     (x - last_input_value) / (current_input_value - last_input_value) * current_output_diff
            output_conversion_func_dict[current_input_value] = self.conversion_func_generator(
                current_input_value, last_input_value, last_output_value, current_output_diff)
            last_input_value = current_input_value
            last_output_value = output_value
        self.output_conversion_func_dict = output_conversion_func_dict

    @staticmethod
    def conversion_func_generator(current_input_value, last_input_value, last_output_value, current_output_diff):
        def conversion_func(input_value):
            return last_output_value + \
                (input_value - last_input_value) / (current_input_value - last_input_value) * current_output_diff
        return conversion_func

    def segment_linear_mapper_func(self, raw_net_flux_value):
        for input_value_upper_bound, output_conversion_func in self.output_conversion_func_dict.items():
            if raw_net_flux_value <= input_value_upper_bound:
                return output_conversion_func(raw_net_flux_value)
        raise ValueError(f'Cannot find appropriate conversion func: {raw_net_flux_value}')


class TransparencyGenerator(SegmentedLinearMappers):
    min_transparency = 0.1
    max_transparency = 1
    input_ratio_output_value_dict = {
        0: 0.05,
        0.1: 0.55,
        0.5: 0.8,
        1: 1
    }

    def __init__(
            self, reaction_list_with_flux, min_max_net_flux_value_pair=None,
            absolute_value_output_value_dict=None, input_ratio_output_value_dict=None,
            min_max_output_value_pair=(0, 1)):
        if absolute_value_output_value_dict is not None:
            input_ratio_output_value_dict = None
        elif input_ratio_output_value_dict is None:
            input_ratio_output_value_dict = self.input_ratio_output_value_dict
        if min_max_net_flux_value_pair is None:
            min_max_net_flux_value_pair = collect_and_find_flux_value_range(reaction_list_with_flux)
        super().__init__(
            min_max_input_value_pair=min_max_net_flux_value_pair,
            absolute_value_output_dict=absolute_value_output_value_dict,
            relative_ratio_output_value_dict=input_ratio_output_value_dict,
            min_max_output_value_pair=min_max_output_value_pair
        )
        # super().__init__(input_ratio_output_value_dict, reaction_list_with_flux)

    def __call__(self, net_flux_value):
        output_transparency = self.segment_linear_mapper_func(net_flux_value)
        return {ParameterName.alpha: output_transparency}


flux_value_mapper_dict = {
    ParameterName.transparency: TransparencyGenerator
}


def extract_display_name(raw_name):
    try:
        last_underline_loc = raw_name.rindex('_')
    except ValueError:
        return raw_name
    else:
        return raw_name[:last_underline_loc]
