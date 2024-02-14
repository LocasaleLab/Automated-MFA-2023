from .config import np, DataName, Vector, CompositeFigure, ColorConfig, ZOrderConfig, CommonFigureString, \
    CommonElementConfig, ParameterName, FontWeight, HorizontalAlignment, VerticalAlignment, \
    TextBox, GeneralElements, numbered_even_sequence
from .config import ModelDataSensitivityDataFigureConfig, DataSensitivityMetabolicNetworkConfig, \
    SensitivityConfig, MetaboliteConfig, ReactionConfig

ChevronArrow = GeneralElements.ChevronArrow
RoundRectangle = GeneralElements.RoundRectangle
Metabolite = GeneralElements.MetaboliteList
Reaction = GeneralElements.ReactionList
arrange_text_by_row = GeneralElements.arrange_text_by_row
set_and_convert_network_elements = GeneralElements.set_and_convert_network_elements


class NetworkSensitivityDiagramMetabolite(object):
    def __init__(self):
        self.obj_example_a1 = Metabolite('A')
        self.obj_example_b1 = Metabolite('B')
        self.obj_example_c1 = Metabolite('C')
        self.obj_example_a2 = Metabolite('A')
        self.obj_example_b2 = Metabolite('B')
        self.obj_example_c2 = Metabolite('C')
        self.obj_example_a3 = Metabolite('A')
        self.obj_example_b3 = Metabolite('B')
        self.obj_example_c3 = Metabolite('C')
        self.obj_example_d1 = Metabolite('D')

        self.content_list_pair = [
            (value.metabolite_name, value) for value in self.__dict__.values() if isinstance(value, Metabolite)
        ]


class NetworkSensitivityDiagramReaction(object):
    def __init__(self):
        self.obj_example_abf1 = Reaction('AB_F')
        self.obj_example_abr1 = Reaction('AB_R')
        self.obj_example_bcf1 = Reaction('BC_F')
        self.obj_example_bcr1 = Reaction('BC_R')
        self.obj_example_abf2 = Reaction('AB_F')
        self.obj_example_abr2 = Reaction('AB_R')
        self.obj_example_bcf2 = Reaction('BC_F')
        self.obj_example_bcr2 = Reaction('BC_R')
        self.obj_example_abf3 = Reaction('AB_F')
        self.obj_example_abr3 = Reaction('AB_R')
        self.obj_example_bcf3 = Reaction('BC_F')
        self.obj_example_bcr3 = Reaction('BC_R')
        self.obj_example_bd1 = Reaction('BD')
        self.obj_example_bd2 = Reaction('BD')
        self.obj_example_bb = Reaction('B_biomass')

        self.content_list_pair = [
            (value.reaction_name, value) for value in self.__dict__.values() if isinstance(value, Reaction)
        ]


class ModelSensitivityDiagram(CompositeFigure):
    def __init__(
            self, mode=DataName.merge_reversible_reaction, scale=1, **kwargs):
        metabolite_list = NetworkSensitivityDiagramMetabolite()
        reaction_list = NetworkSensitivityDiagramReaction()
        other_text_list = []
        total_size, other_obj_list = metabolic_sensitivity_network_layout_generator(
            metabolite_list, reaction_list, other_text_list, mode=mode)
        metabolic_element_dict = set_and_convert_network_elements(
            metabolite_list, reaction_list, other_text_list=other_text_list, other_obj_list=other_obj_list)
        super().__init__(
            metabolic_element_dict, Vector(0, 0), total_size * scale, scale=scale, background=False, **kwargs)


class DataAvailabilityDiagram(CompositeFigure):
    def __init__(self, mode=DataName.smaller_data_size, separate=False, **kwargs):
        (
            text_config_list, round_rectangle_obj_list, total_width, total_height
        ) = data_availability_sensitivity_layout_generator(
            mode, ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode],
            ModelDataSensitivityDataFigureConfig.group_id_name_dict, separate)

        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        total_size = Vector(total_width, total_height)

        element_dict = {
            'text': {},
            'rectangle': {
                round_rectangle_obj.name: round_rectangle_obj for round_rectangle_obj in round_rectangle_obj_list},
        }
        for text_config in text_config_list:
            text_box_obj = TextBox(**text_config)
            element_dict['text'][text_box_obj.name] = text_box_obj

        super().__init__(
            element_dict, Vector(0, 0), total_size, background=False, **kwargs)


class ConfigSensitivityDiagram(CompositeFigure):
    def __init__(self, mode=DataName.different_constant_flux, **kwargs):
        (
            text_config_list, round_rectangle_obj_list, total_width, total_height
        ) = config_sensitivity_layout_generator(
            mode, ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode],
            ModelDataSensitivityDataFigureConfig.group_id_name_dict)

        self.total_width = total_width
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        total_size = Vector(total_width, total_height)

        element_dict = {
            'text': {},
            'rectangle': {
                round_rectangle_obj.name: round_rectangle_obj for round_rectangle_obj in round_rectangle_obj_list},
        }
        for text_config in text_config_list:
            text_box_obj = TextBox(**text_config)
            element_dict['text'][text_box_obj.name] = text_box_obj

        super().__init__(
            element_dict, Vector(0, 0), total_size, background=False, **kwargs)


class FluxRangeTableDiagram(CompositeFigure):
    title_height = 0.1
    each_row_height = 0.06
    total_width = 0.6

    def __init__(self, **kwargs):
        flux_range_string_dict = {
            'low_lb': 'Low LB: 0.5',
            'medium_lb': 'Medium LB: 1',
            'high_lb': 'High LB: 2',
            'ex_high_lb': 'EX High LB: 5',
            'low_ub': 'Low UB: 500',
            'medium_ub': 'Medium UB: 1000',
            'high_ub': 'High UB: 2000',
            'ex_high_ub': 'Ex High UB: 5000',
        }
        flux_range_label_list = [
            ['low_lb', 'low_ub'],
            ['medium_lb', 'medium_ub'],
            ['high_lb', 'high_ub'],
            ['ex_high_lb', 'ex_high_ub'],
        ]
        emphasized_set = {'medium_lb', 'medium_ub'}
        total_row_num = len(flux_range_label_list)
        total_width = self.total_width
        each_row_height = self.each_row_height
        title_height = self.title_height
        table_height = total_row_num * each_row_height
        total_height = table_height + title_height
        total_size = Vector(total_width, total_height)
        common_text_config = {
            **ReactionConfig.default_display_text_config,
            ParameterName.font_size: MetaboliteConfig.font_size + 2,
            ParameterName.height: each_row_height,
        }

        text_config_list = []
        for row_index, row_label_list in enumerate(flux_range_label_list):
            current_col_num = len(row_label_list)
            each_col_width = total_width / current_col_num
            current_y_loc = table_height - (row_index + 0.5) * each_row_height
            for col_index, each_label in enumerate(row_label_list):
                if each_label is None:
                    continue
                current_x_loc = (col_index + 0.5) * each_col_width
                if each_label in emphasized_set:
                    text_box = True
                else:
                    text_box = False
                text_config_list.append({
                    **common_text_config,
                    ParameterName.string: flux_range_string_dict[each_label],
                    ParameterName.width: each_col_width,
                    ParameterName.center: Vector(current_x_loc, current_y_loc),
                    ParameterName.text_box: text_box,
                })
        title_config_dict = {
            **SensitivityConfig.title_text_config,
            ParameterName.string: CommonFigureString.different_flux_range,
            ParameterName.font_size: MetaboliteConfig.font_size + 10,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, table_height + title_height / 2)
        }

        element_dict = {
            'title': {'title': TextBox(**title_config_dict)},
            'table': {}
        }
        for text_config in text_config_list:
            text_box_obj = TextBox(**text_config)
            element_dict['table'][text_box_obj.name] = text_box_obj

        super().__init__(
            element_dict, Vector(0, 0), total_size, background=False, **kwargs)


def metabolic_sensitivity_network_layout_generator(
        metabolite_list, reaction_list, text_config_list, mode=DataName.merge_reversible_reaction):
    def plot_metabolite_with_reversible_reaction(
            x_loc, top_metabolite_y_loc, metabolite_distance, target_metabolite_list,
            target_reaction_tuple_list, reaction_string_tuple_list):
        y_loc_list = [top_metabolite_y_loc - metabolite_distance * i for i, _ in enumerate(target_metabolite_list)]
        for target_y_loc, target_metabolite_obj in zip(y_loc_list, target_metabolite_list):
            target_metabolite_obj.set_center(Vector(x_loc, target_y_loc))
        reaction_y_loc_list = [
            (y_loc + y_loc_list[y_loc_index + 1]) / 2 for y_loc_index, y_loc in enumerate(y_loc_list[:-1])]
        for reaction_y_loc, target_reaction_tuple, reaction_string_tuple in zip(
                reaction_y_loc_list, target_reaction_tuple_list, reaction_string_tuple_list):
            if len(target_reaction_tuple) == 1:
                target_reaction_obj = target_reaction_tuple[0]
                reaction_string = reaction_string_tuple[0]
                target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(x_loc, reaction_y_loc + reversible_reaction_tail_offset),
                    Vector(x_loc, reaction_y_loc - reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **left_text_config,
                    ParameterName.string: reaction_string,
                    ParameterName.center: Vector(x_loc - reaction_text_distance, reaction_y_loc)
                })
            elif len(target_reaction_tuple) == 2:
                forward_target_reaction_obj, backward_target_reaction_obj = target_reaction_tuple
                forward_reaction_string, backward_reaction_string = reaction_string_tuple
                forward_reaction_x_loc = x_loc - reversible_reaction_distance / 2
                backward_reaction_x_loc = x_loc + reversible_reaction_distance / 2
                forward_target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(forward_reaction_x_loc, reaction_y_loc + reversible_reaction_tail_offset),
                    Vector(forward_reaction_x_loc, reaction_y_loc - reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **left_text_config,
                    ParameterName.string: forward_reaction_string,
                    ParameterName.center: Vector(forward_reaction_x_loc - reaction_text_distance, reaction_y_loc)
                })
                backward_target_reaction_obj.extend_reaction_start_end_list([(
                    ParameterName.normal,
                    Vector(backward_reaction_x_loc, reaction_y_loc - reversible_reaction_tail_offset),
                    Vector(backward_reaction_x_loc, reaction_y_loc + reversible_reaction_head_offset), {})]
                ).set_display_text_config_dict({
                    **reaction_text_common_config,
                    **right_text_config,
                    ParameterName.string: backward_reaction_string,
                    ParameterName.center: Vector(backward_reaction_x_loc + reaction_text_distance, reaction_y_loc)
                })
            else:
                raise ValueError()

    chevron_config_list = []
    # common_left_vert_axis = 0.15
    # common_right_vert_axis = 0.35
    # common_middle_vert_axis = 0.25
    common_left_vert_axis = 0.1
    common_right_vert_axis = 0.3
    common_middle_vert_axis = 0.2
    reversible_reaction_distance = 0.013
    reversible_reaction_tail_offset = 0.022
    reversible_reaction_head_offset = 0.024
    reaction_text_distance = 0.035
    common_metabolite_distance = 0.08
    right_document_str = None
    right1_document_str = None
    right2_document_str = None
    right1_vert_axis = None
    right2_vert_axis = None
    upper2_horiz_axis = None
    left_branch_vert_axis = None
    right1_branch_vert_axis = None
    if mode == DataName.merge_reversible_reaction:
        total_width = 0.4
        total_height = 0.35
        left_vert_axis = common_left_vert_axis
        right_vert_axis = common_right_vert_axis
        middle_vert_axis = common_middle_vert_axis
        main_horiz_axis = 0.1
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance / 2
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance / 2
        left_upper_text_horiz_axis = upper_horiz_axis + 0.045
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.035
        title_axis = total_height - 0.04
        # title_str = 'Merge reversible reactions'
        title_str = CommonFigureString.merge_reversible_reactions_with_order_prefix
        left_document_str = 'Reversible reactions\n(Suppose $v_F>v_R$)'
        right_document_str = 'Unidirectional reactions\n$v=v_F-v_R>0$'
    elif mode == DataName.combine_consecutive_reactions:
        total_width = 0.4
        # total_height = 0.33
        total_height = 0.35
        left_vert_axis = common_left_vert_axis
        right_vert_axis = common_right_vert_axis
        middle_vert_axis = common_middle_vert_axis
        main_horiz_axis = 0.11
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance / 2
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance / 2
        upper2_horiz_axis = main_horiz_axis + common_metabolite_distance
        bottom2_horiz_axis = main_horiz_axis - common_metabolite_distance
        left_upper_text_horiz_axis = upper2_horiz_axis + 0.045
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.035
        # title_axis = total_height - 0.02
        title_axis = total_height - 0.04
        # title_str = 'Combine consecutive reactions'
        title_str = CommonFigureString.combine_consecutive_reactions_with_order_prefix
        left_document_str = 'Consecutive reactions\n(Suppose $v_{F1}>v_{R1}$)'
        right_document_str = 'One reaction\n$v_{F1}-v_{R1}=v_F-v_R>0$'
    elif mode == DataName.prune_branches:
        total_width = 0.7
        total_height = 0.35
        branch_main_axis_distance = 0.12
        left_vert_axis = 0.1
        left_branch_vert_axis = left_vert_axis + branch_main_axis_distance
        middle_vert_axis = 0.3
        right1_vert_axis = 0.4
        right1_branch_vert_axis = right1_vert_axis + branch_main_axis_distance
        right2_vert_axis = 0.6
        right_vert_axis = 0.52
        main_horiz_axis = 0.12
        upper_horiz_axis = main_horiz_axis + common_metabolite_distance
        bottom_horiz_axis = main_horiz_axis - common_metabolite_distance
        left_upper_text_horiz_axis = upper_horiz_axis + 0.04
        right_upper_text_horiz_axis = left_upper_text_horiz_axis
        document_title_axis = left_upper_text_horiz_axis + 0.03
        title_axis = total_height - 0.04
        # title_str = 'Miss branch pathways'
        title_str = CommonFigureString.miss_branch_pathways_with_order_prefix
        left_document_str = 'With branch pathway'
        right1_document_str = 'Replace to biomass flux'
        right2_document_str = 'Completely remove'
    else:
        raise ValueError()

    reaction_text_common_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.width: 0.05,
        ParameterName.font_size: MetaboliteConfig.font_size + 3,
        # ParameterName.text_box: True
    }
    left_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.right,
    }
    right_text_config = {
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    document_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size,
        ParameterName.width: 0.15,
        ParameterName.height: 0.04,
        # ParameterName.text_box: True
    }
    document_title_text_config = {
        **document_text_config,
        ParameterName.width: 0.15,
        ParameterName.height: 0.02,
        ParameterName.font_weight: FontWeight.bold,
        # ParameterName.text_box: True
    }
    title_text_config = {
        **SensitivityConfig.title_text_config,
        ParameterName.width: total_width,
        ParameterName.height: 0.03,
    }
    chevron_len = 0.07
    normal_chevron_width = CommonElementConfig.normal_chevron_width
    chevron_middle_x_loc = middle_vert_axis + 0.01
    chevron_config_list.append({
        **CommonElementConfig.chevron_config,
        ParameterName.width: normal_chevron_width - 0.015,
        ParameterName.name: 'chevron',
        ParameterName.tail_end_center: Vector(chevron_middle_x_loc - chevron_len / 2, main_horiz_axis),
        ParameterName.head: Vector(chevron_middle_x_loc + chevron_len / 2, main_horiz_axis),
    })
    text_config_list.extend([
        {
            **title_text_config,
            ParameterName.name: 'title',
            ParameterName.string: title_str,
            ParameterName.center: Vector(total_width / 2, title_axis)
        },
        {
            **document_title_text_config,
            ParameterName.name: 'left_document_title',
            ParameterName.string: 'Raw network',
            ParameterName.center: Vector(left_vert_axis, document_title_axis)
        },
        {
            **document_title_text_config,
            ParameterName.name: 'right_document_title',
            ParameterName.string: 'Modified network',
            ParameterName.center: Vector(right_vert_axis, document_title_axis)
        },
        {
            **document_text_config,
            ParameterName.name: 'left_document',
            ParameterName.string: left_document_str,
            ParameterName.center: Vector(left_vert_axis, left_upper_text_horiz_axis)
        }

    ])
    if mode == DataName.merge_reversible_reaction or mode == DataName.combine_consecutive_reactions:
        text_config_list.append({
            **document_text_config,
            ParameterName.name: 'right_document',
            ParameterName.string: right_document_str,
            ParameterName.center: Vector(right_vert_axis, right_upper_text_horiz_axis)
        })
        if mode == DataName.merge_reversible_reaction:
            left_target_metabolite_list = [metabolite_list.obj_example_a1, metabolite_list.obj_example_b1]
            left_target_reaction_tuple_list = [(reaction_list.obj_example_abf1, reaction_list.obj_example_abr1)]
            left_reaction_string_tuple_list = [('$v_F$', '$v_R$')]
            left_upper_horiz_axis = upper_horiz_axis

            right_target_reaction_tuple_list = [(reaction_list.obj_example_abf2,)]
            right_reaction_string_tuple_list = [('$v$',)]
        elif mode == DataName.combine_consecutive_reactions:
            left_target_metabolite_list = [
                metabolite_list.obj_example_a1, metabolite_list.obj_example_b1, metabolite_list.obj_example_c1]
            left_target_reaction_tuple_list = [
                (reaction_list.obj_example_abf1, reaction_list.obj_example_abr1),
                (reaction_list.obj_example_bcf1, reaction_list.obj_example_bcr1),
            ]
            left_reaction_string_tuple_list = [('$v_{F1}$', '$v_{R1}$'), ('$v_{F2}$', '$v_{R2}$')]
            left_upper_horiz_axis = upper2_horiz_axis

            right_target_reaction_tuple_list = [(reaction_list.obj_example_abf2, reaction_list.obj_example_abr2)]
            right_reaction_string_tuple_list = [('$v_F$', '$v_R$')]
        else:
            raise ValueError()
        plot_metabolite_with_reversible_reaction(
            left_vert_axis, left_upper_horiz_axis, common_metabolite_distance,
            left_target_metabolite_list,
            left_target_reaction_tuple_list, left_reaction_string_tuple_list)
        plot_metabolite_with_reversible_reaction(
            right_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a2, metabolite_list.obj_example_b2],
            right_target_reaction_tuple_list, right_reaction_string_tuple_list)
    elif mode == DataName.prune_branches:
        text_config_list.extend([
            {
                **document_text_config,
                ParameterName.name: 'right_document1',
                ParameterName.string: right1_document_str,
                ParameterName.center: Vector(right1_vert_axis, right_upper_text_horiz_axis)
            },
            {
                **document_text_config,
                ParameterName.name: 'right_document2',
                ParameterName.string: right2_document_str,
                ParameterName.center: Vector(right2_vert_axis, right_upper_text_horiz_axis)
            },
        ])
        plot_metabolite_with_reversible_reaction(
            left_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a1, metabolite_list.obj_example_b1, metabolite_list.obj_example_c1],
            [
                (reaction_list.obj_example_abf1, reaction_list.obj_example_abr1),
                (reaction_list.obj_example_bcf1, reaction_list.obj_example_bcr1),
            ],
            [('$v_{F1}$', '$v_{R1}$'), ('$v_{F2}$', '$v_{R2}$')]
        )
        plot_metabolite_with_reversible_reaction(
            right1_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a2, metabolite_list.obj_example_b2, metabolite_list.obj_example_c2],
            [
                (reaction_list.obj_example_abf2, reaction_list.obj_example_abr2),
                (reaction_list.obj_example_bcf2, reaction_list.obj_example_bcr2),
            ],
            [('$v_{F3}$', '$v_{R3}$'), ('$v_{F4}$', '$v_{R4}$')]
        )
        plot_metabolite_with_reversible_reaction(
            right2_vert_axis, upper_horiz_axis, common_metabolite_distance,
            [metabolite_list.obj_example_a3, metabolite_list.obj_example_b3, metabolite_list.obj_example_c3],
            [
                (reaction_list.obj_example_abf3, reaction_list.obj_example_abr3),
                (reaction_list.obj_example_bcf3, reaction_list.obj_example_bcr3),
            ],
            [('$v_{F3}$', '$v_{R3}$'), ('$v_{F4}$', '$v_{R4}$')]
        )
        metabolite_list.obj_example_d1.set_center(Vector(left_branch_vert_axis, main_horiz_axis))
        left_branch_reaction_text_center_x_loc = (left_vert_axis + left_branch_vert_axis) / 2
        reaction_bd_to_metabolite_distance = 0.04
        reaction_bd_text_loc = main_horiz_axis + 0.02
        reaction_list.obj_example_bd1.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(left_vert_axis + reaction_bd_to_metabolite_distance, main_horiz_axis),
            Vector(left_branch_vert_axis - reaction_bd_to_metabolite_distance, main_horiz_axis), {})]
        ).set_display_text_config_dict({
            **reaction_text_common_config,
            ParameterName.string: '$v_b$',
            ParameterName.center: Vector(left_branch_reaction_text_center_x_loc, reaction_bd_text_loc)
        })
        biomass_reaction_y_loc = (main_horiz_axis + bottom_horiz_axis) / 2
        reaction_list.obj_example_bb.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(left_branch_vert_axis, biomass_reaction_y_loc + reversible_reaction_tail_offset),
            Vector(left_branch_vert_axis, biomass_reaction_y_loc - reversible_reaction_tail_offset), {})]
        ).set_display_text_config_dict({
            **document_text_config,
            **right_text_config,
            ParameterName.string: 'Biomass',
            ParameterName.center: Vector(left_branch_vert_axis + reaction_text_distance + 0.05, biomass_reaction_y_loc)
        })

        right1_branch_reaction_text_center_x_loc = (right1_vert_axis + right1_branch_vert_axis) / 2 + 0.01
        reaction_list.obj_example_bd2.extend_reaction_start_end_list([(
            ParameterName.normal,
            Vector(right1_vert_axis + reaction_bd_to_metabolite_distance, main_horiz_axis),
            Vector(right1_branch_vert_axis - reaction_bd_to_metabolite_distance + 0.02, main_horiz_axis), {})]
        ).set_display_text_config_dict({
            **document_text_config,
            ParameterName.string: 'Biomass $v_b$',
            ParameterName.center: Vector(right1_branch_reaction_text_center_x_loc + 0.01, reaction_bd_text_loc - 0.002)
        })
        text_config_list.append({
            **title_text_config,
            ParameterName.name: 'or',
            ParameterName.string: 'or',
            ParameterName.center: Vector(right_vert_axis + 0.01, main_horiz_axis)
        })
    else:
        raise ValueError()

    total_size = Vector(total_width, total_height)
    chevron_obj_list = [ChevronArrow(**chevron_config) for chevron_config in chevron_config_list]
    return total_size, chevron_obj_list


def data_availability_sensitivity_layout_generator(mode, current_title, result_label_name_dict, separate=False):
    if mode == DataName.smaller_data_size:
        if separate:
            total_width = 0.9
            total_height = 0.3
        else:
            total_width = 0.75
            total_height = 0.29
    elif mode == DataName.data_without_pathway:
        if separate:
            total_width = 0.8
            total_height = 0.29
        else:
            total_width = 0.3
            total_height = 0.44
    elif mode == DataName.compartmental_data:
        if separate:
            total_width = 0.8
            total_height = 0.43
        else:
            total_width = 0.51
            total_height = 0.44
    else:
        raise ValueError()

    title_height = 0.05
    body_height = total_height - title_height

    data_rectangle_text_margin = 0.025
    data_rectangle_overlap_area_margin = 0.01

    round_rectangle_config_list = []
    text_config_list = [
        {
            **SensitivityConfig.title_text_config,
            ParameterName.name: ParameterName.figure_title,
            ParameterName.string: current_title,
            ParameterName.font_size: MetaboliteConfig.font_size + 4,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, body_height + title_height / 2)
        }
    ]

    text_width = 0.1
    common_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size - 1,
        ParameterName.height: 0.05,
        ParameterName.width: text_width,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    }
    normal_text_config = {
        **common_text_config,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    title_config = {
        **common_text_config,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: MetaboliteConfig.font_size + 1,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    common_round_rectangle_config_dict = CommonElementConfig.simulated_background_config_dict
    distance_inside_each_group = 0.025

    if mode == DataName.smaller_data_size:
        title_x_location = 0.11
        text_item_left = 0.22
        text_item_right = total_width
        distance_between_group = 0.07

        if separate:
            left_right_margin = 0.03
            few_data_string_list = DataSensitivityMetabolicNetworkConfig.few_data_vertical_list
            medium_data_string_list = DataSensitivityMetabolicNetworkConfig.medium_data_vertical_list
            raw_data_string_list = DataSensitivityMetabolicNetworkConfig.experimentally_available_data_vertical_list
            raw_data_title_str = CommonFigureString.experimental_available_mid_data
            current_title_height = 0.038

            raw_data_rectangle_top_y = total_height - title_height
            raw_data_title_y_value = (raw_data_rectangle_top_y - current_title_height / 2)
            medium_data_title_y_value = raw_data_title_y_value - current_title_height
            medium_data_rectangle_top_y = medium_data_title_y_value + current_title_height / 2
            few_data_title_y_value = medium_data_title_y_value - current_title_height
            few_data_rectangle_top_y = few_data_title_y_value + current_title_height / 2
            raw_data_rectangle_bottom_y = data_rectangle_overlap_area_margin
            medium_data_rectangle_bottom_y = raw_data_rectangle_bottom_y + data_rectangle_overlap_area_margin
            few_data_rectangle_bottom_y = medium_data_rectangle_bottom_y + data_rectangle_overlap_area_margin
            few_data_bottom_text_center_y = few_data_rectangle_bottom_y + data_rectangle_text_margin - 0.007
            all_metabolite_center_y_value = numbered_even_sequence(
                few_data_bottom_text_center_y, distance_inside_each_group, 4)[::-1]
            few_data_center_y_value = medium_data_center_y_value = raw_data_center_y_value = \
                all_metabolite_center_y_value
            few_data_rectangle_y_range_pair = Vector(few_data_rectangle_bottom_y, few_data_rectangle_top_y)
            medium_data_rectangle_y_range_pair = Vector(medium_data_rectangle_bottom_y, medium_data_rectangle_top_y)
            raw_data_rectangle_y_range_pair = Vector(raw_data_rectangle_bottom_y, raw_data_rectangle_top_y)

            raw_data_left_x_value = left_right_margin
            two_column_text_width = 0.27
            text_left_offset = 0.01
            medium_data_left_x_value = raw_data_left_x_value + data_rectangle_overlap_area_margin
            few_data_left_x_value = medium_data_left_x_value + data_rectangle_overlap_area_margin
            few_data_right_x_value = few_data_left_x_value + two_column_text_width
            medium_data_right_x_value = few_data_right_x_value + two_column_text_width
            raw_data_right_x_value = medium_data_right_x_value + two_column_text_width
            few_data_rectangle_x_range_pair = Vector(few_data_left_x_value, few_data_right_x_value)
            medium_data_rectangle_x_range_pair = Vector(medium_data_left_x_value, medium_data_right_x_value)
            raw_data_rectangle_x_range_pair = Vector(raw_data_left_x_value, raw_data_right_x_value)
            few_data_text_x_range_pair = Vector(
                few_data_left_x_value + data_rectangle_text_margin,
                few_data_right_x_value - data_rectangle_text_margin)
            medium_data_text_x_range_pair = Vector(
                few_data_right_x_value + data_rectangle_text_margin,
                medium_data_right_x_value - data_rectangle_text_margin)
            raw_data_text_x_range_pair = Vector(
                medium_data_right_x_value + data_rectangle_text_margin,
                raw_data_right_x_value - data_rectangle_text_margin)
            few_data_title_x_value = np.mean(few_data_rectangle_x_range_pair)
            medium_data_title_x_value = np.mean(medium_data_rectangle_x_range_pair)
            raw_data_title_x_value = np.mean(raw_data_rectangle_x_range_pair)
            few_data_rectangle_pair = [few_data_rectangle_x_range_pair, few_data_rectangle_y_range_pair]
            medium_data_rectangle_pair = [medium_data_rectangle_x_range_pair, medium_data_rectangle_y_range_pair]
            raw_data_rectangle_pair = [raw_data_rectangle_x_range_pair, raw_data_rectangle_y_range_pair]
            few_data_title_center = Vector(few_data_title_x_value, few_data_title_y_value)
            medium_data_title_center = Vector(medium_data_title_x_value, medium_data_title_y_value)
            raw_data_title_center = Vector(raw_data_title_x_value, raw_data_title_y_value)
        else:
            text_left_offset = 0
            raw_data_title_str = CommonFigureString.experimental_available_mid_data_wrap
            few_data_string_list = DataSensitivityMetabolicNetworkConfig.few_data_list
            medium_data_string_list = DataSensitivityMetabolicNetworkConfig.medium_data_list
            raw_data_string_list = DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list
            raw_data_center_bottom_y = data_rectangle_overlap_area_margin + data_rectangle_text_margin
            raw_data_center_y_value = [
                raw_data_center_bottom_y + distance_inside_each_group, raw_data_center_bottom_y]
            medium_data_center_bottom_y = raw_data_center_bottom_y + distance_between_group
            medium_data_center_y_value = [
                medium_data_center_bottom_y + distance_inside_each_group, medium_data_center_bottom_y]
            few_data_center_bottom_y = medium_data_center_bottom_y + distance_between_group
            few_data_center_y_value = [few_data_center_bottom_y + distance_inside_each_group, few_data_center_bottom_y]

            text_top_location = few_data_center_y_value[0] + data_rectangle_text_margin
            expand_width_vector = Vector(-data_rectangle_overlap_area_margin, data_rectangle_overlap_area_margin)
            raw_data_rectangle_left_right_pair = Vector(
                data_rectangle_overlap_area_margin, total_width - data_rectangle_overlap_area_margin)
            medium_data_rectangle_left_right_pair = raw_data_rectangle_left_right_pair - expand_width_vector
            few_data_rectangle_left_right_pair = medium_data_rectangle_left_right_pair - expand_width_vector
            few_data_rectangle_pair = [
                few_data_rectangle_left_right_pair,
                Vector(few_data_center_y_value[1] - data_rectangle_text_margin, text_top_location),
            ]  # [(left, right), (bottom, top)]
            few_data_title_center = Vector(title_x_location, float(np.mean(few_data_center_y_value)))
            medium_data_rectangle_pair = [
                medium_data_rectangle_left_right_pair,
                Vector(
                    medium_data_center_y_value[1] - data_rectangle_text_margin,
                    text_top_location + data_rectangle_overlap_area_margin),
            ]
            medium_data_title_center = Vector(title_x_location, float(np.mean(medium_data_center_y_value)))
            raw_data_rectangle_pair = [
                raw_data_rectangle_left_right_pair,
                Vector(
                    raw_data_center_y_value[1] - data_rectangle_text_margin,
                    text_top_location + 2 * data_rectangle_overlap_area_margin),
            ]
            raw_data_title_center = Vector(title_x_location, float(np.mean(raw_data_center_y_value)))
            left_right_x_range = Vector(text_item_left, text_item_right)
            raw_data_text_x_range_pair = medium_data_text_x_range_pair = few_data_text_x_range_pair = \
                left_right_x_range

        few_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.3,
        }
        medium_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.2,
        }
        raw_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.dark_light_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        flux_range_string_dict = {
            DataName.few_data: (
                result_label_name_dict[DataName.few_data],
                few_data_text_x_range_pair,
                few_data_title_center,
                few_data_center_y_value,
                few_data_string_list,
                few_data_rectangle_pair,
                few_data_rectangle_config,
            ),
            DataName.medium_data: (
                result_label_name_dict[DataName.medium_data],
                medium_data_text_x_range_pair,
                medium_data_title_center,
                medium_data_center_y_value,
                medium_data_string_list,
                medium_data_rectangle_pair,
                medium_data_rectangle_config,
            ),
            DataName.raw_model_raw_data: (
                raw_data_title_str,
                raw_data_text_x_range_pair,
                raw_data_title_center,
                raw_data_center_y_value,
                raw_data_string_list,
                raw_data_rectangle_pair,
                raw_data_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.data_without_pathway:
        distance_between_group = 0.06
        # bottom_panel_bottom_y = 0.05
        bottom_panel_bottom_y = 0.03
        ppp_removed_str_list = DataSensitivityMetabolicNetworkConfig.ppp_removed_list
        aa_removed_str_list = DataSensitivityMetabolicNetworkConfig.aa_removed_list
        tca_removed_str_list = DataSensitivityMetabolicNetworkConfig.tca_removed_list
        other_metabolite_str_list = DataSensitivityMetabolicNetworkConfig.other_metabolite_list
        current_title_height = 0.038

        if separate:
            text_left_offset = 0.03
            common_rectangle_top = total_height - 0.06
            common_title_height = common_rectangle_top - current_title_height / 2
            common_center_y_value = numbered_even_sequence(
                common_title_height, -distance_inside_each_group, len(aa_removed_str_list) + 1)
            other_metabolite_data_center_y_value = common_center_y_value[:len(other_metabolite_str_list) + 1]
            data_without_ppp_center_y_value = common_center_y_value[:len(ppp_removed_str_list) + 1]
            data_without_ppp_bottom_y_value = data_without_ppp_center_y_value[-1] - data_rectangle_text_margin
            data_without_aa_center_y_value = common_center_y_value
            data_without_aa_bottom_y_value = data_without_aa_center_y_value[-1] - data_rectangle_text_margin
            data_without_tca_center_y_value = common_center_y_value[:len(tca_removed_str_list) + 1]
            data_without_tca_bottom_y_value = data_without_tca_center_y_value[-1] - data_rectangle_text_margin

            # each_column_width = 0.14
            margin = 0.02
            total_column_num = 4
            each_column_width = (total_width - margin * (total_column_num - 0.5)) / total_column_num
            other_metabolite_left_value = margin / 2
            other_metabolite_right_value = other_metabolite_left_value + each_column_width
            data_without_ppp_left_value = other_metabolite_right_value
            data_without_ppp_right_value = data_without_ppp_left_value + each_column_width
            data_without_aa_left_value = data_without_ppp_right_value + margin
            data_without_aa_right_value = data_without_aa_left_value + each_column_width
            data_without_tca_left_value = data_without_aa_right_value + margin
            data_without_tca_right_value = data_without_tca_left_value + each_column_width
            other_metabolite_left_right_x_value = Vector(other_metabolite_left_value, other_metabolite_right_value)
            data_without_ppp_left_right_x_value = Vector(data_without_ppp_left_value, data_without_ppp_right_value)
            data_without_aa_left_right_x_value = Vector(data_without_aa_left_value, data_without_aa_right_value)
            data_without_tca_left_right_x_value = Vector(data_without_tca_left_value, data_without_tca_right_value)
            other_metabolite_title_center_x_value = np.mean(other_metabolite_left_right_x_value)
            data_without_ppp_title_center_x_value = np.mean(data_without_ppp_left_right_x_value)
            data_without_aa_title_center_x_value = np.mean(data_without_aa_left_right_x_value)
            data_without_tca_title_center_x_value = np.mean(data_without_tca_left_right_x_value)
            data_without_ppp_rectangle_pair = [
                data_without_ppp_left_right_x_value,
                Vector(
                    data_without_ppp_bottom_y_value,
                    common_rectangle_top,
                )
            ]
            data_without_aa_rectangle_pair = [
                data_without_aa_left_right_x_value,
                Vector(
                    data_without_aa_bottom_y_value,
                    common_rectangle_top,
                )
            ]
            data_without_tca_rectangle_pair = [
                data_without_tca_left_right_x_value,
                Vector(
                    data_without_tca_bottom_y_value,
                    common_rectangle_top,
                )
            ]

            data_without_ppp_title_str = CommonFigureString.ppp_metabolites
            data_without_aa_title_str = CommonFigureString.aa_metabolites
            data_without_tca_title_str = CommonFigureString.tca_metabolites
        else:
            data_without_aa_center_y_value = numbered_even_sequence(
                bottom_panel_bottom_y, distance_inside_each_group, len(aa_removed_str_list) + 1)[::-1]
            data_without_tca_center_y_value = numbered_even_sequence(
                bottom_panel_bottom_y, distance_inside_each_group, len(tca_removed_str_list) + 1)[::-1]
            data_without_ppp_center_y_value = numbered_even_sequence(
                data_without_aa_center_y_value[0] + distance_between_group, distance_inside_each_group,
                len(ppp_removed_str_list) + 1)[::-1]
            other_metabolite_data_center_y_value = numbered_even_sequence(
                data_without_tca_center_y_value[0] + distance_between_group, distance_inside_each_group,
                len(other_metabolite_str_list) + 1)[::-1]
            left_panel_width = 0.14
            right_panel_width = 0.13
            left_panel_left_right_x_value = Vector(
                data_rectangle_overlap_area_margin, data_rectangle_overlap_area_margin + left_panel_width)
            right_panel_left_right_x_value = Vector(
                total_width - data_rectangle_overlap_area_margin - right_panel_width,
                total_width - data_rectangle_overlap_area_margin)
            text_left_offset = 0.02
            bottom_rectangle_common_bottom = data_rectangle_overlap_area_margin
            data_without_ppp_rectangle_pair = [
                right_panel_left_right_x_value,
                Vector(
                    data_without_ppp_center_y_value[-1] - data_rectangle_text_margin,
                    data_without_ppp_center_y_value[0] + data_rectangle_text_margin),
            ]  # [(left, right), (bottom, top)]
            data_without_aa_rectangle_pair = [
                right_panel_left_right_x_value,
                Vector(
                    bottom_rectangle_common_bottom,
                    data_without_aa_center_y_value[0] + data_rectangle_text_margin),
            ]
            data_without_tca_rectangle_pair = [
                left_panel_left_right_x_value,
                Vector(
                    bottom_rectangle_common_bottom,
                    data_without_tca_center_y_value[0] + data_rectangle_text_margin),
            ]
            left_panel_center_x = float(np.mean(left_panel_left_right_x_value))
            right_panel_center_x = float(np.mean(right_panel_left_right_x_value))
            other_metabolite_left_right_x_value = left_panel_left_right_x_value
            data_without_ppp_left_right_x_value = right_panel_left_right_x_value
            data_without_aa_left_right_x_value = right_panel_left_right_x_value
            data_without_tca_left_right_x_value = left_panel_left_right_x_value
            other_metabolite_title_center_x_value = left_panel_center_x
            data_without_ppp_title_center_x_value = right_panel_center_x
            data_without_aa_title_center_x_value = right_panel_center_x
            data_without_tca_title_center_x_value = left_panel_center_x

            data_without_ppp_title_str = result_label_name_dict[DataName.data_without_ppp]
            data_without_aa_title_str = result_label_name_dict[DataName.data_without_aa]
            data_without_tca_title_str = result_label_name_dict[DataName.data_without_tca]

        medium_data_without_combination_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        compartmental_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        all_data_result_label_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }

        flux_range_string_dict = {
            'other_metabolite_list': (
                CommonFigureString.other_metabolite_list,
                other_metabolite_left_right_x_value,
                Vector(other_metabolite_title_center_x_value, other_metabolite_data_center_y_value[0]),
                other_metabolite_data_center_y_value[1:],
                other_metabolite_str_list,
                None,
                {},
            ),
            DataName.data_without_ppp: (
                data_without_ppp_title_str,
                data_without_ppp_left_right_x_value,
                Vector(data_without_ppp_title_center_x_value, data_without_ppp_center_y_value[0]),
                data_without_ppp_center_y_value[1:],
                DataSensitivityMetabolicNetworkConfig.ppp_removed_list,
                data_without_ppp_rectangle_pair,
                medium_data_without_combination_rectangle_config,
            ),
            DataName.data_without_aa: (
                data_without_aa_title_str,
                data_without_aa_left_right_x_value,
                Vector(data_without_aa_title_center_x_value, data_without_aa_center_y_value[0]),
                data_without_aa_center_y_value[1:],
                aa_removed_str_list,
                data_without_aa_rectangle_pair,
                compartmental_data_rectangle_config,
            ),
            DataName.data_without_tca: (
                data_without_tca_title_str,
                data_without_tca_left_right_x_value,
                Vector(data_without_tca_title_center_x_value, data_without_tca_center_y_value[0]),
                data_without_tca_center_y_value[1:],
                DataSensitivityMetabolicNetworkConfig.tca_removed_list,
                data_without_tca_rectangle_pair,
                all_data_result_label_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.compartmental_data:
        medium_data_without_combination_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        compartmental_data_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order + 0.1,
        }
        all_data_result_label_rectangle_config = {
            ParameterName.face_color: ColorConfig.dark_light_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }

        if separate:
            experimentally_available_no_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_without_compartments_core)
            experimentally_available_with_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_with_compartments_core)
            all_available_with_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.all_available_data_list_with_compartments)
            total_row_num = len(experimentally_available_no_compartments_data_list)
            all_available_row_num = len(all_available_with_compartments_data_list)
            distance_between_group = 0.02
            title_distance = 0.01
            double_title_height = 0.06
            current_title_height = 0.038
            rectangle_minimal_bottom = data_rectangle_overlap_area_margin
            inner_rectangle_minimal_bottom = rectangle_minimal_bottom + data_rectangle_overlap_area_margin
            text_bottom = inner_rectangle_minimal_bottom + data_rectangle_text_margin
            common_y_array = numbered_even_sequence(text_bottom, distance_inside_each_group, total_row_num)[::-1]
            medium_data_title_y_location = common_y_array[0] + title_distance + double_title_height / 2
            medium_data_top = medium_data_title_y_location + double_title_height / 2
            all_data_title_y_location = medium_data_top + current_title_height / 2
            all_data_top = all_data_title_y_location + current_title_height / 2
            all_data_y_array = common_y_array[:all_available_row_num + 1]
            medium_data_y_array = common_y_array
            text_left_offset = 0.03
            inner_rectangle_bottom_top = Vector(inner_rectangle_minimal_bottom, medium_data_top)
            outer_rectangle_bottom_top = Vector(rectangle_minimal_bottom, all_data_top)

            mid_panel_expand = 0.01
            common_panel_width = (total_width - distance_between_group * 3 - data_rectangle_overlap_area_margin) / 3
            left_panel_left = distance_between_group
            left_panel_right = left_panel_left + common_panel_width
            left_x_range = Vector(left_panel_left, left_panel_right)
            right_panel_left = left_panel_right + distance_between_group - mid_panel_expand
            mid_panel_left = right_panel_left + data_rectangle_overlap_area_margin
            mid_panel_right = mid_panel_left + common_panel_width + mid_panel_expand
            mid_x_range = Vector(mid_panel_left, mid_panel_right)
            right_panel_right = mid_panel_right + common_panel_width
            right_x_range = Vector(mid_panel_right, right_panel_right)
            right_rectangle_range = Vector(right_panel_left, right_panel_right)

            medium_data_without_combination_rectangle_pair = [
                left_x_range, inner_rectangle_bottom_top]  # [(left, right), (bottom, top)]
            compartmental_data_rectangle_pair = [
                mid_x_range, inner_rectangle_bottom_top]
            all_data_result_rectangle_pair = [
                right_rectangle_range, outer_rectangle_bottom_top, ]
            medium_data_title_center = Vector(float(np.mean(left_x_range)), medium_data_title_y_location)
            compartmental_data_title_center = Vector(float(np.mean(mid_x_range)), medium_data_title_y_location)
            all_data_title_center = Vector(float(np.mean(right_rectangle_range)), all_data_title_y_location)
            medium_data_title_str = CommonFigureString.experimental_mixed_data_wrap
            compartmental_data_title_str = CommonFigureString.experimental_compartmentalized_data_wrap
            all_data_title_str = CommonFigureString.all_compartmentalized_data
        else:
            experimentally_available_no_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_without_compartments)
            experimentally_available_with_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.experimentally_available_data_list_with_compartments)
            all_available_with_compartments_data_list = (
                DataSensitivityMetabolicNetworkConfig.all_available_data_list_with_compartments_core)
            total_row_num = len(experimentally_available_no_compartments_data_list)
            all_available_row_num = len(all_available_with_compartments_data_list)
            title_distance = 0.045
            text_bottom = 0.03
            text_top = total_height - title_height - 0.02
            # common_y_array = np.linspace(text_top, text_bottom, total_row_num + 2)
            common_y_array = numbered_even_sequence(text_bottom, distance_inside_each_group, total_row_num)[::-1]
            # left_x_range = Vector(0.02, 0.12)
            left_panel_width = 0.14
            left_panel_left = data_rectangle_overlap_area_margin
            left_x_range = Vector(left_panel_left, left_panel_left + left_panel_width)
            mid_panel_left = left_x_range[1] + 0.02
            mid_panel_width = 0.15
            # mid_x_range = Vector(0.15, 0.25)
            mid_x_range = Vector(mid_panel_left, mid_panel_left + mid_panel_width)
            # right_x_range = Vector(0.25, 0.32)
            right_panel_left = mid_x_range[1] - 0.01
            right_x_range = Vector(right_panel_left, total_width - data_rectangle_overlap_area_margin)
            title_y_location = common_y_array[0] + title_distance
            all_data_y_array = common_y_array[1:all_available_row_num + 1]
            medium_data_y_array = common_y_array
            text_left_offset = 0.02

            rectangle_minimal_bottom = data_rectangle_overlap_area_margin
            inner_rectangle_bottom_top = Vector(
                rectangle_minimal_bottom + data_rectangle_overlap_area_margin,
                title_y_location + data_rectangle_text_margin + 0.005)
            outer_rectangle_bottom_top = inner_rectangle_bottom_top + Vector(-1, 1) * data_rectangle_overlap_area_margin
            # common_rectangle_bottom_top = Vector(
            #     text_bottom - data_rectangle_text_margin, text_top + data_rectangle_text_margin)
            medium_data_without_combination_rectangle_pair = [
                left_x_range, outer_rectangle_bottom_top, ]  # [(left, right), (bottom, top)]
            compartmental_data_rectangle_pair = [
                mid_x_range, inner_rectangle_bottom_top, ]
            all_data_result_rectangle_pair = [
                Vector(mid_panel_left - data_rectangle_overlap_area_margin, right_x_range[1]),
                outer_rectangle_bottom_top, ]
            medium_data_title_center = Vector(float(np.mean(left_x_range)), title_y_location)
            compartmental_data_title_center = Vector(float(np.mean(mid_x_range)), title_y_location)
            all_data_title_center = Vector(float(np.mean(right_x_range)), title_y_location)
            medium_data_title_str = CommonFigureString.experimental_available_mid_data_double_wrap
            compartmental_data_title_str = CommonFigureString.compartmental_data_wrap
            all_data_title_str = CommonFigureString.all_available_compartmental_data_double_wrap

        flux_range_string_dict = {
            DataName.medium_data_without_combination: (
                medium_data_title_str,
                left_x_range,
                medium_data_title_center,
                medium_data_y_array,
                experimentally_available_no_compartments_data_list,
                medium_data_without_combination_rectangle_pair,
                medium_data_without_combination_rectangle_config,
            ),
            DataName.compartmental_data: (
                compartmental_data_title_str,
                mid_x_range,
                compartmental_data_title_center,
                medium_data_y_array,
                experimentally_available_with_compartments_data_list,
                compartmental_data_rectangle_pair,
                compartmental_data_rectangle_config,
            ),
            DataName.raw_model_all_data: (
                all_data_title_str,
                right_x_range,
                all_data_title_center,
                all_data_y_array,
                all_available_with_compartments_data_list,
                all_data_result_rectangle_pair,
                all_data_result_label_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)
    else:
        raise ValueError()
    round_rectangle_obj_list = [
        RoundRectangle(**round_rectangle_config) for round_rectangle_config in round_rectangle_config_list
    ]
    return text_config_list, round_rectangle_obj_list, total_width, total_height


def config_sensitivity_layout_generator(mode, current_title, result_label_name_dict):
    if mode == DataName.different_constant_flux:
        total_width = 0.35
        total_height = 0.2
    elif mode == DataName.different_flux_range:
        total_width = 0.35
        total_height = 0.2
    else:
        raise ValueError()

    title_height = 0.05
    body_height = total_height - title_height

    data_rectangle_text_margin = 0.025
    data_rectangle_overlap_area_margin = 0.01

    round_rectangle_config_list = []
    text_config_list = [
        {
            **SensitivityConfig.title_text_config,
            ParameterName.name: ParameterName.figure_title,
            ParameterName.string: current_title,
            ParameterName.font_size: MetaboliteConfig.font_size + 4,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, body_height + title_height / 2)
        }
    ]

    text_width = 0.1
    common_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size - 1,
        ParameterName.height: 0.05,
        ParameterName.width: text_width,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    }
    normal_text_config = {
        **common_text_config,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
    }
    title_config = {
        **common_text_config,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: MetaboliteConfig.font_size + 1,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
    }
    common_round_rectangle_config_dict = CommonElementConfig.simulated_background_config_dict
    distance_inside_each_group = 0.025

    if mode == DataName.different_constant_flux:
        distance_between_group = 0.06
        bottom_y = 0.03
        distance_inside_each_group = 0.025
        text_left_offset = 0.05

        constant_flux_string_list = DataSensitivityMetabolicNetworkConfig.different_constant_flux_string_list
        constant_flux_center_y_value = numbered_even_sequence(
            bottom_y, distance_inside_each_group, len(constant_flux_string_list))[::-1]
        panel_x_range = Vector(
            data_rectangle_overlap_area_margin, total_width - data_rectangle_overlap_area_margin)

        flux_range_string_dict = {
            DataName.different_constant_flux: (
                None,
                panel_x_range,
                None,
                constant_flux_center_y_value,
                constant_flux_string_list,
                None,
                {},
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)

    elif mode == DataName.different_flux_range:
        distance_between_group = 0.06
        bottom_panel_bottom_y = 0.03
        flux_lower_bound_string_list = DataSensitivityMetabolicNetworkConfig.flux_lower_bound_string_list
        flux_upper_bound_string_list = DataSensitivityMetabolicNetworkConfig.flux_upper_bound_string_list
        lower_upper_bound_center_y_value = numbered_even_sequence(
            bottom_panel_bottom_y, distance_inside_each_group, len(flux_lower_bound_string_list) + 1)[::-1]
        panel_width = (total_width - 3 * data_rectangle_overlap_area_margin) / 2
        left_panel_start = data_rectangle_overlap_area_margin
        right_panel_end = total_width - data_rectangle_overlap_area_margin
        left_panel_left_right_x_value = Vector(left_panel_start, left_panel_start + panel_width)
        right_panel_left_right_x_value = Vector(right_panel_end - panel_width, right_panel_end)
        text_left_offset = 0.02
        lower_upper_bound_rectangle_config = {
            ParameterName.face_color: ColorConfig.light_medium_bright_blue,
            ParameterName.z_order: ZOrderConfig.default_patch_z_order,
        }
        rectangle_common_bottom = data_rectangle_overlap_area_margin

        rectangle_bottom_top_pair = Vector(
            rectangle_common_bottom, lower_upper_bound_center_y_value[0] + data_rectangle_text_margin)
        left_panel_rectangle_pair = [
            left_panel_left_right_x_value, rectangle_bottom_top_pair,
        ]  # [(left, right), (bottom, top)]
        right_panel_rectangle_pair = [
            right_panel_left_right_x_value, rectangle_bottom_top_pair]
        left_panel_center_x = float(np.mean(left_panel_left_right_x_value))
        right_panel_center_x = float(np.mean(right_panel_left_right_x_value))

        flux_range_string_dict = {
            'lower_bound': (
                CommonFigureString.lower_bound,
                left_panel_left_right_x_value,
                Vector(left_panel_center_x, lower_upper_bound_center_y_value[0]),
                lower_upper_bound_center_y_value[1:],
                flux_lower_bound_string_list,
                left_panel_rectangle_pair,
                lower_upper_bound_rectangle_config,
            ),
            'upper_bound': (
                CommonFigureString.upper_bound,
                right_panel_left_right_x_value,
                Vector(right_panel_center_x, lower_upper_bound_center_y_value[0]),
                lower_upper_bound_center_y_value[1:],
                flux_upper_bound_string_list,
                right_panel_rectangle_pair,
                lower_upper_bound_rectangle_config,
            ),
        }
        arrange_text_by_row(
            flux_range_string_dict, text_left_offset, text_config_list, title_config, normal_text_config,
            round_rectangle_config_list, common_round_rectangle_config_dict)
    else:
        raise ValueError()
    round_rectangle_obj_list = [
        RoundRectangle(**round_rectangle_config) for round_rectangle_config in round_rectangle_config_list
    ]
    return text_config_list, round_rectangle_obj_list, total_width, total_height


