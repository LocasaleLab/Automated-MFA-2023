from .config import np, DataName, Vector, CompositeFigure, ColorConfig, ZOrderConfig, CommonElementConfig, \
    ParameterName, default_parameter_extract, FontWeight, HorizontalAlignment, VerticalAlignment, \
    TextBox, GeneralElements, numbered_even_sequence, ReactionConfig, CommonFigureString, MetabolicNetworkLegend
from .config import ModelDataSensitivityDataFigureConfig, DataSensitivityMetabolicNetworkConfig, \
    SensitivityConfig, MetabolicNetworkConfig, MetabolicNetworkWithLegend

RoundRectangle = GeneralElements.RoundRectangle
MetaboliteConfig = GeneralElements.MetaboliteConfig
ChevronArrow = GeneralElements.ChevronArrow
Metabolite = GeneralElements.MetaboliteList
Reaction = GeneralElements.ReactionList
arrange_text_by_row = GeneralElements.arrange_text_by_row
set_and_convert_network_elements = GeneralElements.set_and_convert_network_elements


class DiagramConfig(object):
    metabolite_vertical_distance = 0.1
    metabolite_horiz_distance = 0.25
    total_width = 3.5 * metabolite_horiz_distance
    total_height = 0.45
    mid_vertical_offset = 0.03
    reaction_horiz_offset = 0.04
    reaction_vert_offset = 0.015
    legend_width = total_width + 0.05

    min_transparency = 0.2
    max_transparency = 1
    absolute_value_output_value_dict = {
        0: min_transparency,
        100: max_transparency,
    }
    min_max_output_value_pair = (min_transparency, max_transparency)


class LossOfAveragedSolutionsDiagram(CompositeFigure):
    legend_height = 0.1

    def calculate_total_width_height(self, legend, *args):
        total_width = DiagramConfig.total_width
        total_height = DiagramConfig.total_height
        if legend:
            total_height += self.legend_height
        return total_width, total_height

    def calculate_center(self, scale, *args):
        return self.total_size / 2 * scale

    def __init__(self, figure_data_parameter_dict, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, 0, pop=True)
        legend = default_parameter_extract(figure_data_parameter_dict, ParameterName.legend, False, pop=True)
        if legend:
            network_bottom = self.legend_height
        else:
            network_bottom = 0
        new_metabolic_network_config_dict = default_parameter_extract(
            figure_data_parameter_dict, ParameterName.metabolic_network_config_dict, {}, pop=True)
        metabolic_network_config_dict = {
            **ExampleLossDiagramConfig.common_diagram_network_setting_dict_generator(mode),
            **new_metabolic_network_config_dict,
        }
        effective_sensitivity_diagram_config_dict = {
            ParameterName.name: f'model_sensitivity_diagram_{mode}',
            ParameterName.mode: mode,
            ParameterName.bottom_left_offset: Vector(0, network_bottom),
            ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
            **figure_data_parameter_dict,
        }
        sensitivity_diagram_obj = ExampleLossDiagram(**effective_sensitivity_diagram_config_dict)
        subfigure_element_dict = {'diagram': {'diagram': sensitivity_diagram_obj, }, }

        total_width, total_height = self.calculate_total_width_height(legend)
        self.total_size = Vector(total_width, total_height)
        self.total_width, self.total_height = total_width, total_height
        self.height_to_width_ratio = total_height / total_width
        if legend:
            effective_metabolic_network_legend_config_dict = {
                ParameterName.bottom_left_offset: Vector(0, 0),
                ParameterName.legend_config_dict: ExampleLossDiagramLegendConfig,
                ParameterName.mode: ParameterName.horizontal,
            }
            metabolic_legend_obj = MetabolicNetworkLegend(**effective_metabolic_network_legend_config_dict)
            subfigure_element_dict['metabolic_network_legend'] = {'metabolic_network_legend': metabolic_legend_obj}
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


def mid_value_dict_generator(mode):
    mid_value_dict = {
        'D': '$[1, 0]$',
        'E': '$[0, 1]$',
        'F': '$[0, 1]$',
        'G': '$[1, 0]$',
    }
    if mode == 0:
        mid_value_dict.update({
            'A': '$[0, 1]$',
            'B': '$[0, 1]$',
            'C': '$[0, 1]$',
            'H': '$[0, 1]$',
            'I': '$[0, 1]$',
        })
    elif mode == 1:
        mid_value_dict.update({
            'A': '$[0, 1]$',
            'B': '$[0, 1]$',
            'C': '$[1, 0]$',
            'H': '$[1, 0]$',
            'I': '$[1, 0]$',
        })

    elif mode == 2:
        mid_value_dict.update({
            'A': '$[1, 0]$',
            'B': '$[0, 1]$',
            'C': '$[0, 1]$',
            'H': '$[1, 0]$',
            'I': '$[1, 0]$',
        })

    elif mode == 3:
        mid_value_dict.update({
            'A': '$[0.5, 0.5]$',
            'B': '$[0.5, 0.5]$',
            'C': '$[0.5, 0.5]$',
            'H': '$[0.5, 0.5]$',
            'I': '$[0.5, 0.5]$',
        })
    else:
        raise ValueError()
    return mid_value_dict


def flux_value_dict_generator(mode):
    if mode == 0:
        flux_value_dict = {
            'AB': 50,
            'BC': 50,
            'DA': 0,
            'EA': 100,
            'FC': 100,
            'GC': 0,
            'AH': 50,
            'CI': 50,
        }
    elif mode == 1:
        flux_value_dict = {
            'AB': 100,
            'BC': 0,
            'DA': 0,
            'EA': 100,
            'FC': 0,
            'GC': 100,
            'AH': 0,
            'CI': 100,
        }
    elif mode == 2:
        flux_value_dict = {
            'AB': 0,
            'BC': 100,
            'DA': 100,
            'EA': 0,
            'FC': 100,
            'GC': 0,
            'AH': 100,
            'CI': 0,
        }
    elif mode == 3:
        flux_value_dict = {
            'AB': 50,
            'BC': 50,
            'DA': 50,
            'EA': 50,
            'FC': 50,
            'GC': 50,
            'AH': 50,
            'CI': 50,
        }
    else:
        raise ValueError()
    return flux_value_dict


class ExampleLossDiagramConfig(object):
    common_input_metabolite_set = {'D', 'E', 'F', 'G', }
    common_c13_labeling_metabolite_set = {'E', 'F', }
    common_diagram_network_setting_dict = {
        ParameterName.input_metabolite_set: common_input_metabolite_set,
        ParameterName.c13_labeling_metabolite_set: common_c13_labeling_metabolite_set,
    }
    common_data_flux_network_setting_dict = {}

    @staticmethod
    def common_diagram_network_setting_dict_generator(mode):
        if mode == 0:
            mid_data_metabolite_set = {'A', 'B', 'H', 'C', 'I'}
            invalid_metabolite_set = set()
        elif mode == 1:
            mid_data_metabolite_set = {'A', 'B'}
            invalid_metabolite_set = set()
        elif mode == 2:
            mid_data_metabolite_set = {'B', 'C'}
            invalid_metabolite_set = set()
        elif mode == 3:
            mid_data_metabolite_set = set()
            invalid_metabolite_set = {'A', 'B', 'H', 'C', 'I'}
        else:
            raise ValueError()
        target_diagram_network_setting_dict = {
            **ExampleLossDiagramConfig.common_diagram_network_setting_dict,
            ParameterName.mid_data_metabolite_set: mid_data_metabolite_set,
            ParameterName.invalid_metabolite_set: invalid_metabolite_set,
        }
        return target_diagram_network_setting_dict


class ExampleLossDiagramLegendConfig(GeneralElements.LegendConfig):
    legend_horizontal_width = DiagramConfig.legend_width
    metabolite_content_dict = {
        'D': Metabolite('D').set_input_state(True),
        'E': Metabolite('E').set_input_state(True).set_c13_labeling_state(True),
        'A': Metabolite('A'),
        'B': Metabolite('B').set_mid_data_state(True),
        'C': Metabolite('C').set_invalid_state(True),
    }
    reaction_content_dict = {
        'fluxes': Reaction('unidirectional'),
    }
    text_content_dict = {
        'D': 'Input metabolites\nwith unlabelled MID',
        'E': 'Input metabolites with $\mathregular{^{13}}$C\nlabelled',
        'A': 'Metabolites\nwith unlabelled MID',
        'B': 'Metabolites\nwith fully labelled MID',
        'C': 'Metabolites\nwith partically labelled MID',
        'fluxes': 'Normal fluxes',
    }


class ExampleLossDiagramMetabolite(object):
    def __init__(self):
        self.obj_example_a = Metabolite('A')
        self.obj_example_b = Metabolite('B')
        self.obj_example_c = Metabolite('C')
        self.obj_example_d = Metabolite('D')
        self.obj_example_e = Metabolite('E')
        self.obj_example_f = Metabolite('F')
        self.obj_example_g = Metabolite('G')
        self.obj_example_h = Metabolite('H')
        self.obj_example_i = Metabolite('I')

        self.content_list_pair = [
            (value.metabolite_name, value) for value in self.__dict__.values() if isinstance(value, Metabolite)
        ]


class ExampleLossDiagramReaction(object):
    def __init__(self):
        self.obj_example_ab = Reaction('AB')
        self.obj_example_bc = Reaction('BC')
        self.obj_example_da = Reaction('DA')
        self.obj_example_ea = Reaction('EA')
        self.obj_example_fc = Reaction('FC')
        self.obj_example_gc = Reaction('GC')
        self.obj_example_ah = Reaction('AH')
        self.obj_example_ci = Reaction('CI')

        self.content_list_pair = [
            (value.reaction_name, value) for value in self.__dict__.values() if isinstance(value, Reaction)
        ]


class ExampleLossDiagram(CompositeFigure):
    total_width = DiagramConfig.total_width
    total_height = DiagramConfig.total_height
    height_to_width_ratio = total_height / total_width

    def __init__(self, metabolic_network_config_dict, mode=0, scale=1, **kwargs):
        metabolite_list = ExampleLossDiagramMetabolite()
        reaction_list = ExampleLossDiagramReaction()
        other_text_list = []
        other_obj_list = metabolic_sensitivity_network_layout_generator(
            metabolite_list, reaction_list, other_text_list, self.total_width, self.total_height, mode=mode)
        total_size = Vector(self.total_width, self.total_height)
        metabolic_element_dict = set_and_convert_network_elements(
            metabolite_list, reaction_list, other_text_list=other_text_list, other_obj_list=other_obj_list,
            reaction_raw_value_dict=flux_value_dict_generator(mode),
            flux_value_mapper=GeneralElements.TransparencyGenerator(
                None, min_max_net_flux_value_pair=(0, 100),
                absolute_value_output_value_dict=DiagramConfig.absolute_value_output_value_dict,
                min_max_output_value_pair=DiagramConfig.min_max_output_value_pair,
            ),
            **metabolic_network_config_dict)
        super().__init__(
            metabolic_element_dict, Vector(0, 0), total_size * scale, scale=scale, background=False, **kwargs)


def metabolic_sensitivity_network_layout_generator(
        metabolite_list, reaction_list, text_config_list, total_width, total_height, mode=0):
    other_obj_list = []
    bottom_horiz_axis = DiagramConfig.metabolite_vertical_distance
    middle_horiz_axis = 2 * DiagramConfig.metabolite_vertical_distance
    top_horiz_axis = 3 * DiagramConfig.metabolite_vertical_distance
    vert_axis_1 = 0.25 * DiagramConfig.metabolite_horiz_distance
    vert_axis_2 = 0.9 * DiagramConfig.metabolite_horiz_distance
    vert_axis_3 = 1.5 * DiagramConfig.metabolite_horiz_distance
    vert_axis_4 = 1.75 * DiagramConfig.metabolite_horiz_distance
    vert_axis_5 = 2 * DiagramConfig.metabolite_horiz_distance
    vert_axis_6 = 2.6 * DiagramConfig.metabolite_horiz_distance
    vert_axis_7 = 3.25 * DiagramConfig.metabolite_horiz_distance

    mid_vertical_offset = DiagramConfig.mid_vertical_offset

    metabolite_obj_loc_dict = {
        metabolite_list.obj_example_a: (
            Vector(vert_axis_2, middle_horiz_axis), Vector(vert_axis_2, middle_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_b: (
            Vector(vert_axis_4, bottom_horiz_axis), Vector(vert_axis_4, bottom_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_c: (
            Vector(vert_axis_6, middle_horiz_axis), Vector(vert_axis_6, middle_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_d: (
            Vector(vert_axis_1, top_horiz_axis), Vector(vert_axis_1, top_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_e: (
            Vector(vert_axis_3, top_horiz_axis), Vector(vert_axis_3, top_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_f: (
            Vector(vert_axis_5, top_horiz_axis), Vector(vert_axis_5, top_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_g: (
            Vector(vert_axis_7, top_horiz_axis), Vector(vert_axis_7, top_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_h: (
            Vector(vert_axis_1, bottom_horiz_axis), Vector(vert_axis_1, bottom_horiz_axis + mid_vertical_offset)),
        metabolite_list.obj_example_i: (
            Vector(vert_axis_7, bottom_horiz_axis), Vector(vert_axis_7, bottom_horiz_axis + mid_vertical_offset)),
    }

    basic_font_size = 13
    reaction_text_common_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: basic_font_size,
        ParameterName.width: 0.05,
    }
    document_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: basic_font_size + 1,
        ParameterName.width: 0.15,
        ParameterName.height: 0.04,
    }
    document_title_text_config = {
        **document_text_config,
        ParameterName.width: 0.15,
        ParameterName.height: 0.02,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: basic_font_size + 3,
    }
    left_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.right,
    }
    right_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }

    reaction_horiz_offset = DiagramConfig.reaction_horiz_offset
    reaction_vert_offset = DiagramConfig.reaction_vert_offset

    title_dict = {
        0: 'Real flux\n(B is fully labelled)',
        1: 'Selected solution 1\n(B is fully labelled)',
        2: 'Selected solution 2\n(B is fully labelled)',
        3: 'Averaged solution\n(B is partially labelled)',
    }

    reaction_obj_loc_dict = {
        reaction_list.obj_example_ab: (
            Vector(vert_axis_2 + reaction_horiz_offset, middle_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_4 - reaction_horiz_offset, bottom_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_bc: (
            Vector(vert_axis_6 - reaction_horiz_offset, middle_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_4 + reaction_horiz_offset, bottom_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_da: (
            Vector(vert_axis_1 + reaction_horiz_offset, top_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_2 - reaction_horiz_offset, middle_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_ea: (
            Vector(vert_axis_3 - reaction_horiz_offset, top_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_2 + reaction_horiz_offset, middle_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_fc: (
            Vector(vert_axis_5 + reaction_horiz_offset, top_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_6 - reaction_horiz_offset, middle_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_gc: (
            Vector(vert_axis_7 - reaction_horiz_offset, top_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_6 + reaction_horiz_offset, middle_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_ah: (
            Vector(vert_axis_2 - reaction_horiz_offset, middle_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_1 + reaction_horiz_offset, bottom_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
        reaction_list.obj_example_ci: (
            Vector(vert_axis_6 + reaction_horiz_offset, middle_horiz_axis - reaction_vert_offset),
            Vector(vert_axis_7 - reaction_horiz_offset, bottom_horiz_axis + reaction_vert_offset),
            Vector(0, 0)
        ),
    }

    metabolite_mid_value_dict = mid_value_dict_generator(mode)
    for target_metabolite_obj, (
            metabolite_obj_loc_vector, metabolite_text_loc_vector) in metabolite_obj_loc_dict.items():
        target_metabolite_obj.set_center(metabolite_obj_loc_vector)
        text_config_list.append({
            **document_text_config,
            ParameterName.name: f'{target_metabolite_obj.metabolite_name}_mid',
            ParameterName.string: metabolite_mid_value_dict[target_metabolite_obj.metabolite_name],
            ParameterName.center: metabolite_text_loc_vector
        })

    reaction_value_dict = flux_value_dict_generator(mode)
    for target_reaction_obj, (
            reaction_start_loc_vector, reaction_end_loc_vector, reaction_text_offset
    ) in reaction_obj_loc_dict.items():
        text_center = (reaction_start_loc_vector + reaction_end_loc_vector) / 2 + reaction_text_offset
        target_reaction_obj.extend_reaction_start_end_list([(
            ParameterName.normal,
            reaction_start_loc_vector,
            reaction_end_loc_vector, {})]
        ).set_display_text_config_dict({
            **reaction_text_common_config,
            **left_text_config,
            ParameterName.string: reaction_value_dict[target_reaction_obj.reaction_name],
            ParameterName.center: text_center,
        })

    text_config_list.append({
        **document_title_text_config,
        ParameterName.string: title_dict[mode],
        ParameterName.center: Vector(total_width / 2, total_height - 0.06)
    })

    return other_obj_list

