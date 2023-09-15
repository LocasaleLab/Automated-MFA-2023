from ...common_functions import initialize_vector_input, basic_shape_parameter_set, \
    load_required_parameter, convert_theta_to_coordinate
from .config import np, Vector, Arrow, ArcArrow, complete_arrow_parameter_set_dict, \
    ParameterName, Keyword, ZOrderConfig, ColorConfig
from .config import CompositeFigure, Circle, RoundRectangle


class NetworkDiagramConfig(object):
    height_to_width_ratio = 1.2

    metabolite_z_order = ZOrderConfig.default_axis_z_order + ZOrderConfig.z_order_increment
    metabolite_config = {
        ParameterName.radius: 0.055,
        ParameterName.face_color: ColorConfig.normal_metabolite_color,
        ParameterName.edge_width: None,
        ParameterName.z_order: metabolite_z_order
    }

    reaction_z_order = metabolite_z_order + ZOrderConfig.z_order_increment
    reaction_config = {
        ParameterName.face_color: ColorConfig.normal_reaction_color,
        ParameterName.edge_width: None,
        ParameterName.stem_width: 0.027,
        ParameterName.head_width: 0.07,
        ParameterName.head_len_width_ratio: 0.85,
        ParameterName.z_order: reaction_z_order,
        ParameterName.tail_arrow: False
    }

    background_config = {
        ParameterName.face_color: ColorConfig.light_blue,
        ParameterName.edge_width: None,
        ParameterName.radius: 0.25,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order
    }


class NetworkDiagram(CompositeFigure):
    total_width = 1
    height_to_width_ratio = NetworkDiagramConfig.height_to_width_ratio

    def __init__(self, **kwargs):
        total_height = self.total_width * self.height_to_width_ratio
        size_vector = Vector(self.total_width, total_height)

        circle_parameter_set = {
            ParameterName.radius,
        } | basic_shape_parameter_set
        common_circle_param_dict = {}
        load_required_parameter(common_circle_param_dict, NetworkDiagramConfig.metabolite_config, circle_parameter_set)
        kwargs_unused_set1 = load_required_parameter(common_circle_param_dict, kwargs, circle_parameter_set)
        radius = common_circle_param_dict[ParameterName.radius]
        (
            metabolite_circle_location_dict, reaction_location_tuple_dict, background_range,
            tca_cycle_center, tca_cycle_radius) = diagram_layout_generator(
            radius, self.height_to_width_ratio)

        metabolite_circle_param_dict_list = [
            {
                ParameterName.name: metabolite_name,
                ParameterName.center: metabolite_circle_location,
                **common_circle_param_dict
            } for metabolite_name, metabolite_circle_location in metabolite_circle_location_dict.items()
        ]
        # for metabolite_circle_param_dict in metabolite_circle_param_dict_list:
        #     move_and_scale_parameter_dict(metabolite_circle_param_dict, scale, bottom_left_offset)
        metabolite_list = [
            Circle(**metabolite_circle_param_dict)
            for metabolite_circle_param_dict in metabolite_circle_param_dict_list]

        reaction_class_list = []
        reaction_arrow_param_dict_list = []
        kwargs_unused_set = None
        for reaction_name, (state, param1, param2, param_list) in reaction_location_tuple_dict.items():
            if len(param_list) == 0:
                branch_list = None
            else:
                branch_list = [
                    {
                        ParameterName.stem_location: stem_location,
                        ParameterName.terminal_location: terminal_location,
                        ParameterName.arrow: arrow
                    }
                    for stem_location, terminal_location, arrow in param_list]
            if state == Keyword.normal:
                current_param_dict = {
                    ParameterName.tail: param1,
                    ParameterName.head: param2,
                    ParameterName.branch_list: branch_list
                }
                arrow_parameter_set = complete_arrow_parameter_set_dict[ParameterName.common] | \
                    complete_arrow_parameter_set_dict[Arrow.__name__] | basic_shape_parameter_set
                current_class = Arrow
            elif state == Keyword.cycle:
                current_param_dict = {
                    ParameterName.theta_tail: param1,
                    ParameterName.theta_head: param2,
                    ParameterName.center: tca_cycle_center,
                    ParameterName.radius: tca_cycle_radius,
                    ParameterName.branch_list: branch_list
                }
                arrow_parameter_set = complete_arrow_parameter_set_dict[ParameterName.common] | \
                    complete_arrow_parameter_set_dict[ArcArrow.__name__] | basic_shape_parameter_set
                current_class = ArcArrow
            else:
                raise ValueError()
            load_required_parameter(
                current_param_dict, NetworkDiagramConfig.reaction_config, arrow_parameter_set)
            current_kwargs_unused_set = load_required_parameter(current_param_dict, kwargs, arrow_parameter_set)
            reaction_arrow_param_dict_list.append(current_param_dict)
            reaction_class_list.append(current_class)
            if kwargs_unused_set is None:
                kwargs_unused_set = current_kwargs_unused_set
            else:
                kwargs_unused_set &= current_kwargs_unused_set
        # for reaction_arrow_param_dict in reaction_arrow_param_dict_list:
        #     move_and_scale_parameter_dict(reaction_arrow_param_dict, scale, bottom_left_offset, arrow=True)
        reaction_list = [
            current_class(**reaction_arrow_param_dict)
            for current_class, reaction_arrow_param_dict in zip(reaction_class_list, reaction_arrow_param_dict_list)]

        round_rectangle_parameter_set = {
            ParameterName.center,
            ParameterName.width,
            ParameterName.height,
            ParameterName.radius,
        } | basic_shape_parameter_set
        background_top, background_bottom, background_left, background_right = background_range
        background_center = Vector(background_left + background_right, background_top + background_bottom) / 2
        background_size = Vector(background_right - background_left, background_top - background_bottom)
        background_param_dict = {
            ParameterName.center: background_center,
            ParameterName.width: background_size.x,
            ParameterName.height: background_size.y,
        }
        load_required_parameter(
            background_param_dict, NetworkDiagramConfig.background_config, round_rectangle_parameter_set)
        kwargs_unused_set1 = load_required_parameter(
            background_param_dict, kwargs, round_rectangle_parameter_set)
        # move_and_scale_parameter_dict(background_param_dict, scale, bottom_left_offset)
        background = RoundRectangle(**background_param_dict)
        network_diagram_dict = {
            ParameterName.metabolite: {metabolite_obj.name: metabolite_obj for metabolite_obj in metabolite_list},
            ParameterName.reaction: {reaction_obj.name: reaction_obj for reaction_obj in reaction_list},
            ParameterName.background: {'background': background},
        }
        super().__init__(
            network_diagram_dict, Vector(0, 0), size_vector, **kwargs)


def diagram_layout_generator(metabolite_radius, height_to_width_ratio):
    # Suppose width = 1
    height = height_to_width_ratio
    left_right_margin = 0.05
    main_vertical_axis = 0.5
    branch_to_main_vertical_axis_distance = 0.2
    left_most_axis = left_right_margin
    right_most_axis = 1 - left_right_margin
    left_main_vertical_axis = main_vertical_axis - branch_to_main_vertical_axis_distance
    right_main_vertical_axis = main_vertical_axis + branch_to_main_vertical_axis_distance
    background_ratio = 0.6

    top_bottom_margin = left_right_margin
    top_most_horiz_axis = height - top_bottom_margin
    bottom_most_horiz_axis = top_bottom_margin
    pyr_horiz_axis = 0.6
    tca_cycle_top_horiz_axis = 0.5
    tca_cycle_bottom_horiz_axis = 0.2
    tca_cycle_radius = (tca_cycle_top_horiz_axis - tca_cycle_bottom_horiz_axis) / 2
    tca_cycle_center_horiz_axis = tca_cycle_top_horiz_axis - tca_cycle_radius
    tca_cycle_center = Vector(main_vertical_axis, tca_cycle_center_horiz_axis)

    glycolysis_name_list = ['glc_e', 'g6p_c', '3pg_c', 'pyr_c']
    glycolysis_reaction_list = ['glc_g6p', 'g6p_3pg', '3pg_pyr']
    glycolysis_y_loc_list = top_most_horiz_axis + np.arange(len(glycolysis_name_list)) * (
        pyr_horiz_axis - top_most_horiz_axis) / (len(glycolysis_name_list) - 1)
    glycolysis_center_dict = {
        key: Vector(main_vertical_axis, y_value) for key, y_value in zip(
            glycolysis_name_list, glycolysis_y_loc_list)}
    glycolysis_reaction_start_end_dict = {
        reaction_name: (
            Keyword.normal,
            Vector(main_vertical_axis, glycolysis_y_loc_list[reaction_index] - metabolite_radius),
            Vector(main_vertical_axis, glycolysis_y_loc_list[reaction_index + 1] + metabolite_radius),
            []
        )
        for reaction_index, reaction_name in enumerate(glycolysis_reaction_list)
    }
    branch_center_dict = {
        'rib_c': Vector(left_main_vertical_axis, glycolysis_center_dict['g6p_c'].y),
        'ser_c': Vector(right_main_vertical_axis, glycolysis_center_dict['3pg_c'].y),
        'lac_c': Vector(left_main_vertical_axis, glycolysis_center_dict['pyr_c'].y),
    }
    branch_reaction_dict = {
        'g6p_rib': (
            Keyword.normal,
            Vector(main_vertical_axis - metabolite_radius, branch_center_dict['rib_c'].y),
            Vector(left_main_vertical_axis + metabolite_radius, branch_center_dict['rib_c'].y),
            []
        ),
        '3pg_set': (
            Keyword.normal,
            Vector(main_vertical_axis + metabolite_radius, branch_center_dict['ser_c'].y),
            Vector(right_main_vertical_axis - metabolite_radius, branch_center_dict['ser_c'].y),
            []
        ),
        'pyr_lac': (
            Keyword.normal,
            Vector(main_vertical_axis - metabolite_radius, branch_center_dict['lac_c'].y),
            Vector(left_main_vertical_axis + metabolite_radius, branch_center_dict['lac_c'].y),
            []
        ),
    }

    tca_name_list = ['cit_m', 'akg_m', 'suc_m', 'oac_m']
    tca_angle_list = [45, -45, -135, -225]
    tca_center_dict = {
        key: convert_theta_to_coordinate(theta, tca_cycle_center, tca_cycle_radius)
        for key, theta in zip(tca_name_list, tca_angle_list)
    }

    metabolite_width_theta = 360 * metabolite_radius / (tca_cycle_radius * 2 * 3.1416)
    tca_reaction_name_list = ['cit_akg', 'akg_suc', 'suc_oac']
    tca_reaction_theta_dict = {
        key: (
            Keyword.cycle,
            tca_angle_list[index] - metabolite_width_theta,
            tca_angle_list[index + 1] + metabolite_width_theta,
            [])
        for index, key in enumerate(tca_reaction_name_list)
    }
    tca_reaction_theta_dict['oac_cit'] = (
        Keyword.cycle,
        tca_angle_list[-1] + 360 - metabolite_width_theta,
        tca_angle_list[0] + metabolite_width_theta,
        [
            (90, Vector(main_vertical_axis, glycolysis_center_dict['pyr_c'].y - metabolite_radius), False)
        ]
    )
    input_center_dict = {
        'glu_e': Vector(tca_center_dict['akg_m'].x, bottom_most_horiz_axis)
    }
    input_reaction_dict = {
        'glu_akg': (
            Keyword.normal,
            Vector(tca_center_dict['akg_m'].x, input_center_dict['glu_e'].y + metabolite_radius),
            Vector(tca_center_dict['akg_m'].x, tca_center_dict['akg_m'].y - metabolite_radius),
            []
        )
    }

    metabolite_circle_location_dict = {
        **glycolysis_center_dict,
        **branch_center_dict,
        **tca_center_dict,
        **input_center_dict
    }
    reaction_location_dict = {
        **glycolysis_reaction_start_end_dict,
        **branch_reaction_dict,
        **tca_reaction_theta_dict,
        **input_reaction_dict
    }

    background_ratio2 = 1 - background_ratio
    background_top = background_ratio * metabolite_circle_location_dict['glc_e'].y + \
        background_ratio2 * metabolite_circle_location_dict['g6p_c'].y
    background_bottom = background_ratio * metabolite_circle_location_dict['glu_e'].y + \
        background_ratio2 * metabolite_circle_location_dict['akg_m'].y
    background_left = background_ratio * left_most_axis + background_ratio2 * left_main_vertical_axis
    background_right = background_ratio * right_most_axis + background_ratio2 * right_main_vertical_axis
    background_range = (background_top, background_bottom, background_left, background_right)

    return metabolite_circle_location_dict, reaction_location_dict, background_range, \
        tca_cycle_center, tca_cycle_radius
