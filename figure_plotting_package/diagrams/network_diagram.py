from .config import basic_shape_parameter_set, load_required_parameter, convert_theta_to_coordinate, \
    unit_decorator
from .config import np, Vector, Arrow, ArcArrow, complete_arrow_parameter_set_dict, \
    ParameterName, ZOrderConfig, ColorConfig, common_text_config_dict, SegmentedLinearMappers
from .config import CompositeFigure, Capsule, Circle, RoundRectangle, Ellipse, TextBox


class SimpleTransparencyGenerator(SegmentedLinearMappers):
    min_transparency = 0.3
    max_transparency = 1
    input_ratio_output_value_dict = {
        0: 0.3,
        0.6: 0.8,
        1: 1
    }

    def __init__(self, flux_value_list, ):
        flux_value_array = np.array(flux_value_list)
        min_max_net_flux_value_pair = (np.min(flux_value_array), np.max(flux_value_array))
        super().__init__(
            min_max_input_value_pair=min_max_net_flux_value_pair,
            relative_ratio_output_value_dict=self.input_ratio_output_value_dict,
            min_max_output_value_pair=(self.min_transparency, self.max_transparency)
        )

    def __call__(self, net_flux_value):
        output_transparency = self.segment_linear_mapper_func(net_flux_value)
        return {ParameterName.alpha: output_transparency}


class NetworkDiagramConfig(object):
    normal_total_width = 1
    normal_height_to_width_ratio = 1.2
    data_sensitivity_total_width = 1.1
    data_sensitivity_height = 1.5
    data_sensitivity_height_to_width_ratio = data_sensitivity_height / data_sensitivity_total_width

    metabolite_z_order = ZOrderConfig.default_axis_z_order + ZOrderConfig.z_order_increment
    mixed_metabolite_z_order = ZOrderConfig.default_axis_z_order
    metabolite_config = {
        ParameterName.radius: 0.055,
        ParameterName.face_color: ColorConfig.normal_metabolite_color,
        ParameterName.edge_width: None,
        ParameterName.z_order: metabolite_z_order
    }
    mixed_metabolite_ellipse_config = {
        **metabolite_config,
        ParameterName.z_order: mixed_metabolite_z_order,
    }
    metabolite_capsule_config_dict = {
        ParameterName.width: 0.15,
        ParameterName.height: 0.08
    }
    metabolite_capsule_text_config = {
        **common_text_config_dict,
        ParameterName.font_color: ColorConfig.white_color,
        ParameterName.font_size: 29,
        ParameterName.z_order: metabolite_z_order + ZOrderConfig.z_order_increment
    }

    disabled_metabolite_color = ColorConfig.medium_light_gray
    measured_metabolite_color = ColorConfig.mid_metabolite_color

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
    cross_config = {
        **reaction_config,
        ParameterName.width: 0.07,
        ParameterName.stem_width: 0.022,
    }
    reaction_text_config = {
        **common_text_config_dict,
        ParameterName.font_size: 11,
        ParameterName.z_order: reaction_z_order + ZOrderConfig.z_order_increment
    }
    reaction_value_digit = 0

    common_background_config = {
        ParameterName.edge_width: None,
        ParameterName.radius: 0.25,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order
    }
    background_config = {
        **common_background_config,
        ParameterName.face_color: ColorConfig.light_blue,
    }
    mito_background_config = {
        **common_background_config,
        ParameterName.radius: 0.15,
        ParameterName.face_color: ColorConfig.light_medium_blue,
    }


def generate_background_obj(background_range, background_config, kwargs):
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
        background_param_dict, background_config, round_rectangle_parameter_set)
    kwargs_unused_set1 = load_required_parameter(
        background_param_dict, kwargs, round_rectangle_parameter_set)
    # move_and_scale_parameter_dict(background_param_dict, scale, bottom_left_offset)
    background = RoundRectangle(**background_param_dict)
    return background


def construct_mixed_metabolite_obj(
        metabolite_1_center, metabolite_2_center, metabolite_radius, orientation=ParameterName.vertical):
    final_center = (metabolite_1_center + metabolite_2_center) / 2
    if orientation == ParameterName.vertical:
        width = 4 * metabolite_radius
        y_distance = abs(metabolite_1_center.y - metabolite_2_center.y)
        height = np.sqrt(y_distance ** 2 + width ** 2)
    else:
        height = 4 * metabolite_radius
        x_distance = abs(metabolite_1_center.x - metabolite_2_center.x)
        width = np.sqrt(x_distance ** 2 + height ** 2)
    config_dict = {
        ParameterName.center: final_center,
        ParameterName.height: height,
        ParameterName.width: width
    }
    return config_dict


class NetworkDiagram(CompositeFigure):
    total_width = 1
    height_to_width_ratio = NetworkDiagramConfig.normal_height_to_width_ratio

    @staticmethod
    def _calculate_width_and_ratio(mode):
        if mode == ParameterName.normal:
            height_to_width_ratio = NetworkDiagramConfig.normal_height_to_width_ratio
            total_width = NetworkDiagramConfig.normal_total_width
        else:
            height_to_width_ratio = NetworkDiagramConfig.data_sensitivity_height_to_width_ratio
            total_width = NetworkDiagramConfig.data_sensitivity_total_width
        return total_width, height_to_width_ratio

    @staticmethod
    def calculate_center(self, scale, mode=ParameterName.normal, *args):
        total_width, height_to_width_ratio = self._calculate_width_and_ratio(mode)
        return Vector(total_width, total_width * height_to_width_ratio) / 2 * scale

    def __init__(self, mode=ParameterName.normal, layout_decorator=None, visualize_flux_value=None, **kwargs):
        total_width, height_to_width_ratio = self._calculate_width_and_ratio(mode)
        self.total_width = total_width
        total_height = self.total_width * height_to_width_ratio
        self.height_to_width_ratio = height_to_width_ratio
        size_vector = Vector(self.total_width, total_height)

        circle_parameter_set = {
            ParameterName.radius,
        } | basic_shape_parameter_set
        common_circle_param_dict = {}
        load_required_parameter(common_circle_param_dict, NetworkDiagramConfig.metabolite_config, circle_parameter_set)
        kwargs_unused_set1 = load_required_parameter(common_circle_param_dict, kwargs, circle_parameter_set)

        radius = common_circle_param_dict[ParameterName.radius]
        if visualize_flux_value is not None:
            flux_value_mapper = SimpleTransparencyGenerator(list(visualize_flux_value.values()))
            radius -= 0.015
            common_circle_param_dict[ParameterName.radius] = radius
        else:
            flux_value_mapper = None

        if layout_decorator is None:
            layout_decorator = unit_decorator
        else:
            assert callable(layout_decorator)
        (
            metabolite_circle_config_dict, metabolite_ellipse_config_dict, reaction_location_tuple_dict,
            background_range, mito_background_range, tca_cycle_center, tca_cycle_radius) = layout_decorator(
            default_diagram_layout_generator)(radius, self.total_width, self.height_to_width_ratio, mode)

        metabolite_circle_param_dict_list = [
            {
                **common_circle_param_dict,
                ParameterName.name: metabolite_name,
                **metabolite_circle_config,
            } for metabolite_name, metabolite_circle_config in metabolite_circle_config_dict.items()
        ]
        metabolite_list = [
            Circle(**metabolite_circle_param_dict)
            for metabolite_circle_param_dict in metabolite_circle_param_dict_list]
        metabolite_list.extend([
            Ellipse(**metabolite_ellipse_config)
            for metabolite_ellipse_config in metabolite_ellipse_config_dict.values()
        ])
        text_config_dict = {}

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
            if state == ParameterName.normal:
                current_param_dict = {
                    ParameterName.tail: param1,
                    ParameterName.head: param2,
                    ParameterName.branch_list: branch_list
                }
                arrow_parameter_set = complete_arrow_parameter_set_dict[ParameterName.common] | \
                    complete_arrow_parameter_set_dict[Arrow.__name__] | basic_shape_parameter_set
                current_class = Arrow
                text_center = (param1 + param2) / 2
            elif state == ParameterName.cycle:
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
                text_center = convert_theta_to_coordinate(
                    (param1 + param2) / 2, tca_cycle_center, tca_cycle_radius)
            else:
                raise ValueError()
            load_required_parameter(
                current_param_dict, NetworkDiagramConfig.reaction_config, arrow_parameter_set)
            current_kwargs_unused_set = load_required_parameter(current_param_dict, kwargs, arrow_parameter_set)
            if visualize_flux_value is not None and reaction_name in visualize_flux_value:
                reaction_value = visualize_flux_value[reaction_name]
                current_param_dict.update(flux_value_mapper(reaction_value))
                if reaction_name in default_reaction_offset_dict:
                    reaction_offset = default_reaction_offset_dict[reaction_name]
                else:
                    reaction_offset = Vector(0, 0)
                format_string = f'{{:.{NetworkDiagramConfig.reaction_value_digit}f}}'
                text_config_dict[f'{reaction_name}_value'] = {
                    **NetworkDiagramConfig.reaction_text_config,
                    ParameterName.font_size: 35,
                    ParameterName.width: 0.05,
                    ParameterName.height: 0.02,
                    ParameterName.string: format_string.format(reaction_value),
                    ParameterName.center: text_center + reaction_offset
                }
            reaction_arrow_param_dict_list.append(current_param_dict)
            reaction_class_list.append(current_class)
            if kwargs_unused_set is None:
                kwargs_unused_set = current_kwargs_unused_set
            else:
                kwargs_unused_set &= current_kwargs_unused_set
        reaction_list = [
            current_class(**reaction_arrow_param_dict)
            for current_class, reaction_arrow_param_dict in zip(reaction_class_list, reaction_arrow_param_dict_list)]

        background_obj = generate_background_obj(background_range, NetworkDiagramConfig.background_config, kwargs)
        network_diagram_dict = {
            ParameterName.metabolite: {metabolite_obj.name: metabolite_obj for metabolite_obj in metabolite_list},
            ParameterName.reaction: {reaction_obj.name: reaction_obj for reaction_obj in reaction_list},
            ParameterName.background: {'background': background_obj},
        }
        if mode != ParameterName.normal:
            mito_background_obj = generate_background_obj(
                mito_background_range, NetworkDiagramConfig.mito_background_config, kwargs)
            network_diagram_dict[ParameterName.background]['mitochondria_background'] = mito_background_obj
        if len(text_config_dict) > 0:
            network_diagram_dict[ParameterName.text] = {
                name: TextBox(**text_config) for name, text_config in text_config_dict.items()
            }
        super().__init__(
            network_diagram_dict, Vector(0, 0), size_vector, background=False, **kwargs)


center_name = ParameterName.center


def default_diagram_layout_generator(metabolite_radius, width, height_to_width_ratio, mode):
    height = width * height_to_width_ratio
    left_right_margin = 0.05
    background_ratio = 0.6
    if mode == ParameterName.normal:
        # width = 1
        # height = 1.2
        main_vertical_axis = 0.5
        branch_to_main_vertical_axis_distance = 0.2
        left_most_axis = left_right_margin
        right_most_axis = width - left_right_margin
        left_main_vertical_axis = main_vertical_axis - branch_to_main_vertical_axis_distance
        right_main_vertical_axis = main_vertical_axis + branch_to_main_vertical_axis_distance
        right_2_vertical_axis = right_main_vertical_axis

        top_bottom_margin = left_right_margin
        top_most_horiz_axis = height - top_bottom_margin
        bottom_most_horiz_axis = top_bottom_margin
        bottom_2_horiz_axis = bottom_most_horiz_axis
        pyr_horiz_axis = 0.6
        tca_cycle_top_horiz_axis = 0.5
        tca_cycle_bottom_horiz_axis = 0.2
    else:
        # width = 1.1
        # height = 1.5
        main_vertical_axis = 0.5
        branch_to_main_vertical_axis_distance = 0.19
        left_most_axis = left_right_margin
        right_most_axis = width - left_right_margin
        left_main_vertical_axis = main_vertical_axis - branch_to_main_vertical_axis_distance
        right_main_vertical_axis = main_vertical_axis + branch_to_main_vertical_axis_distance
        right_2_vertical_axis = right_main_vertical_axis + branch_to_main_vertical_axis_distance

        top_bottom_margin = left_right_margin
        top_most_horiz_axis = height - top_bottom_margin
        bottom_most_horiz_axis = top_bottom_margin
        bottom_2_horiz_axis = bottom_most_horiz_axis + 0.17
        pyr_horiz_axis = 0.75
        tca_cycle_top_horiz_axis = 0.65
        tca_cycle_bottom_horiz_axis = 0.35

    tca_cycle_radius = (tca_cycle_top_horiz_axis - tca_cycle_bottom_horiz_axis) / 2
    tca_cycle_center_horiz_axis = tca_cycle_top_horiz_axis - tca_cycle_radius
    tca_cycle_center = Vector(main_vertical_axis, tca_cycle_center_horiz_axis)

    if mode == ParameterName.normal:
        glycolysis_name_list = ['glc_e', 'g6p_c', '3pg_c', 'pyr_c']
        glycolysis_reaction_list = ['glc_g6p', 'g6p_3pg', '3pg_pyr']
    else:
        glycolysis_name_list = ['glc_e', 'g6p_c', '3pg_c', 'pyr_c', 'pyr_m']
        glycolysis_reaction_list = ['glc_g6p', 'g6p_3pg', '3pg_pyr', 'pyr_exchange']
    glycolysis_y_loc_list = top_most_horiz_axis + np.arange(len(glycolysis_name_list)) * (
        pyr_horiz_axis - top_most_horiz_axis) / (len(glycolysis_name_list) - 1)
    glycolysis_center_dict = {
        key: Vector(main_vertical_axis, y_value) for key, y_value in zip(
            glycolysis_name_list, glycolysis_y_loc_list)}
    glycolysis_reaction_start_end_dict = {
        reaction_name: (
            ParameterName.normal,
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
            ParameterName.normal,
            Vector(main_vertical_axis - metabolite_radius, branch_center_dict['rib_c'].y),
            Vector(left_main_vertical_axis + metabolite_radius, branch_center_dict['rib_c'].y),
            []
        ),
        '3pg_ser': (
            ParameterName.normal,
            Vector(main_vertical_axis + metabolite_radius, branch_center_dict['ser_c'].y),
            Vector(right_main_vertical_axis - metabolite_radius, branch_center_dict['ser_c'].y),
            []
        ),
        'pyr_lac': (
            ParameterName.normal,
            Vector(main_vertical_axis - metabolite_radius, branch_center_dict['lac_c'].y),
            Vector(left_main_vertical_axis + metabolite_radius, branch_center_dict['lac_c'].y),
            []
        ),
    }
    if mode != ParameterName.normal:
        branch_center_dict.update({
            'gly_c': Vector(right_2_vertical_axis, branch_center_dict['ser_c'].y),
        })
        branch_reaction_dict.update({
            'ser_gly': (
                ParameterName.normal,
                Vector(right_main_vertical_axis + metabolite_radius, branch_center_dict['ser_c'].y),
                Vector(right_2_vertical_axis - metabolite_radius, branch_center_dict['ser_c'].y),
                []
            )
        })

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
            ParameterName.cycle,
            tca_angle_list[index] - metabolite_width_theta,
            tca_angle_list[index + 1] + metabolite_width_theta,
            [])
        for index, key in enumerate(tca_reaction_name_list)
    }
    if mode == ParameterName.normal:
        branch_start_y = glycolysis_center_dict['pyr_c'].y
    else:
        branch_start_y = glycolysis_center_dict['pyr_m'].y
    tca_reaction_theta_dict['oac_cit'] = (
        ParameterName.cycle,
        tca_angle_list[-1] + 360 - metabolite_width_theta,
        tca_angle_list[0] + metabolite_width_theta,
        [
            (90, Vector(main_vertical_axis, branch_start_y - metabolite_radius), False)
        ]
    )
    input_center_dict = {
        'glu_e': Vector(tca_center_dict['akg_m'].x, bottom_most_horiz_axis)
    }
    input_reaction_dict = {}
    if mode == ParameterName.normal:
        input_reaction_dict['glu_akg'] = (
            ParameterName.normal,
            Vector(tca_center_dict['akg_m'].x, input_center_dict['glu_e'].y + metabolite_radius),
            Vector(tca_center_dict['akg_m'].x, tca_center_dict['akg_m'].y - metabolite_radius),
            []
        )
    else:
        glu_c_y_value = (tca_center_dict['akg_m'].y + input_center_dict['glu_e'].y) / 2
        cit_c_x_value = (right_main_vertical_axis + right_2_vertical_axis) / 2
        input_center_dict.update({
            'glu_c': Vector(tca_center_dict['akg_m'].x, glu_c_y_value),
            'cit_c': Vector(cit_c_x_value, tca_center_dict['cit_m'].y),
        })
        input_reaction_dict.update({
            'glu_c_akg': (
                ParameterName.normal,
                Vector(tca_center_dict['akg_m'].x, input_center_dict['glu_c'].y + metabolite_radius),
                Vector(tca_center_dict['akg_m'].x, tca_center_dict['akg_m'].y - metabolite_radius),
                [],),
            'glu_c_glu_e': (
                ParameterName.normal,
                Vector(tca_center_dict['akg_m'].x, input_center_dict['glu_e'].y + metabolite_radius),
                Vector(tca_center_dict['akg_m'].x, input_center_dict['glu_c'].y - metabolite_radius),
                [],),
            'cit_exchange': (
                ParameterName.normal,
                Vector(tca_center_dict['cit_m'].x + metabolite_radius, tca_center_dict['cit_m'].y),
                Vector(input_center_dict['cit_c'].x - metabolite_radius, tca_center_dict['cit_m'].y),
                [],),
        })

    background_ratio2 = 1 - background_ratio
    background_top = background_ratio * glycolysis_center_dict['glc_e'].y + \
        background_ratio2 * glycolysis_center_dict['g6p_c'].y
    if mode == ParameterName.normal:
        background_bottom = background_ratio * input_center_dict['glu_e'].y + \
            background_ratio2 * tca_center_dict['akg_m'].y
    else:
        background_bottom = background_ratio * input_center_dict['glu_e'].y + \
            background_ratio2 * input_center_dict['glu_c'].y
    background_left = background_ratio * left_most_axis + background_ratio2 * left_main_vertical_axis
    background_right = background_ratio * right_most_axis + background_ratio2 * right_2_vertical_axis
    background_range = (background_top, background_bottom, background_left, background_right)

    if mode != ParameterName.normal:
        mito_background_top = background_ratio * glycolysis_center_dict['pyr_c'].y + \
            background_ratio2 * glycolysis_center_dict['pyr_m'].y
        mito_background_bottom = background_ratio * input_center_dict['glu_c'].y + \
            background_ratio2 * tca_center_dict['akg_m'].y
        mito_background_left = background_ratio * left_main_vertical_axis + \
            background_ratio2 * (left_main_vertical_axis - 0.1)
        mito_background_right = 0.3 * input_center_dict['cit_c'].x + \
            0.7 * right_main_vertical_axis
        mito_background_range = (
            mito_background_top, mito_background_bottom, mito_background_left, mito_background_right)
    else:
        mito_background_range = None

    metabolite_circle_config_dict = {
        **{name: {center_name: center} for name, center in glycolysis_center_dict.items()},
        **{name: {center_name: center} for name, center in branch_center_dict.items()},
        **{name: {center_name: center} for name, center in tca_center_dict.items()},
        **{name: {center_name: center} for name, center in input_center_dict.items()},
    }
    metabolite_ellipse_config_dict = {}

    reaction_location_dict = {
        **glycolysis_reaction_start_end_dict,
        **branch_reaction_dict,
        **tca_reaction_theta_dict,
        **input_reaction_dict
    }

    return metabolite_circle_config_dict, metabolite_ellipse_config_dict, reaction_location_dict, \
        background_range, mito_background_range, tca_cycle_center, tca_cycle_radius


default_side_offset = 0.075
default_top_offset = 0.065
default_reaction_offset_dict = {
    'glc_g6p': Vector(default_side_offset, 0),
    'g6p_3pg': Vector(-default_side_offset, 0),
    '3pg_pyr': Vector(default_side_offset, 0),
    'g6p_rib': Vector(0, default_top_offset),
    '3pg_ser': Vector(0, default_top_offset),
    'pyr_lac': Vector(0, default_top_offset),
    'glu_akg': Vector(default_side_offset, 0),
    'oac_cit': Vector(0, -default_top_offset),
    'cit_akg': Vector(default_side_offset, 0),
    'akg_suc': Vector(0, -default_top_offset),
    'suc_oac': Vector(-default_side_offset, 0),
    'glu_c_akg': Vector(0, 0),
    'glu_c_glu_e': Vector(0, 0),
    'cit_exchange': Vector(0, 0),
}


class FreeNetworkDiagram(CompositeFigure):
    total_width = 1
    total_height = 1.2

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_height) / 2 * scale

    def __init__(self, diagram_layout_generator=None, **kwargs):
        total_width = self.total_width
        total_height = self.total_height
        height_to_width_ratio = total_height / total_width
        self.height_to_width_ratio = height_to_width_ratio
        size_vector = Vector(self.total_width, total_height)

        common_circle_param_dict = dict(NetworkDiagramConfig.metabolite_config)
        radius = common_circle_param_dict[ParameterName.radius]

        (
            metabolite_circle_config_dict, metabolite_ellipse_config_dict, reaction_location_tuple_dict,
            background_config_dict) = diagram_layout_generator(
            radius, total_width, total_height)

        metabolite_circle_param_dict_list = [
            {
                **common_circle_param_dict,
                ParameterName.name: metabolite_name,
                **metabolite_circle_config,
            } for metabolite_name, metabolite_circle_config in metabolite_circle_config_dict.items()
        ]
        metabolite_list = [
            Circle(**metabolite_circle_param_dict)
            for metabolite_circle_param_dict in metabolite_circle_param_dict_list]
        metabolite_list.extend([
            Ellipse(**metabolite_ellipse_config)
            for metabolite_ellipse_config in metabolite_ellipse_config_dict.values()
        ])

        reaction_class_list = []
        reaction_arrow_param_dict_list = []
        for reaction_name, (
                state, param1, param2, param_list, other_param_dict) in reaction_location_tuple_dict.items():
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
            if state == ParameterName.normal:
                current_param_dict = {
                    ParameterName.tail: param1,
                    ParameterName.head: param2,
                    ParameterName.branch_list: branch_list,
                    **other_param_dict,
                }
                current_class = Arrow
            elif state == ParameterName.cycle:
                current_param_dict = {
                    ParameterName.theta_tail: param1,
                    ParameterName.theta_head: param2,
                    ParameterName.branch_list: branch_list,
                    **other_param_dict,
                }
                current_class = ArcArrow
            else:
                raise ValueError()
            complete_param_dict = {
                **NetworkDiagramConfig.reaction_config,
                **current_param_dict,
            }
            reaction_arrow_param_dict_list.append(complete_param_dict)
            reaction_class_list.append(current_class)
        reaction_list = [
            current_class(**reaction_arrow_param_dict)
            for current_class, reaction_arrow_param_dict in zip(reaction_class_list, reaction_arrow_param_dict_list)]

        background_dict = {
            name: RoundRectangle(**{
                **NetworkDiagramConfig.background_config,
                **config_dict,
            }) for name, config_dict in background_config_dict.items()}

        network_diagram_dict = {
            ParameterName.metabolite: {metabolite_obj.name: metabolite_obj for metabolite_obj in metabolite_list},
            ParameterName.reaction: {reaction_obj.name: reaction_obj for reaction_obj in reaction_list},
            ParameterName.background: background_dict,
        }
        super().__init__(
            network_diagram_dict, Vector(0, 0), size_vector, background=False, **kwargs)


class FreeNetworkWithTextDiagram(CompositeFigure):
    total_width = 1
    total_height = 1.2

    def __init__(self, diagram_layout_generator=None, **kwargs):
        common_circle_param_dict = dict(NetworkDiagramConfig.metabolite_config)
        radius = common_circle_param_dict[ParameterName.radius]
        (
            total_width, total_height, metabolite_capsule_or_circle_config_dict, metabolite_text_config_dict,
            reaction_location_tuple_dict, reaction_text_config_dict, background_config_dict, other_element_config_dict,
        ) = diagram_layout_generator(radius)

        self.total_width = total_width
        self.total_height = total_height
        height_to_width_ratio = total_height / total_width
        self.height_to_width_ratio = height_to_width_ratio
        size_vector = Vector(self.total_width, total_height)

        metabolite_circle_param_dict_list = [
            {
                **common_circle_param_dict,
                ParameterName.name: metabolite_name,
                **metabolite_circle_config,
            } for metabolite_name, metabolite_circle_config in metabolite_capsule_or_circle_config_dict.items()
        ]
        metabolite_list = [
            Capsule(**metabolite_circle_param_dict)
            if ParameterName.width in metabolite_circle_param_dict
            else Circle(**metabolite_circle_param_dict)
            for metabolite_circle_param_dict in metabolite_circle_param_dict_list]
        metabolite_text_dict = {
            text_name: TextBox(**{
                **NetworkDiagramConfig.metabolite_capsule_text_config,
                ParameterName.name: text_name,
                **text_config_dict,
            }) for text_name, text_config_dict in metabolite_text_config_dict.items()
        }

        reaction_class_list = []
        reaction_arrow_param_dict_list = []
        for reaction_name, (
                state, param1, param2, param_list, other_param_dict) in reaction_location_tuple_dict.items():
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
            if state == ParameterName.normal:
                current_param_dict = {
                    ParameterName.tail: param1,
                    ParameterName.head: param2,
                    ParameterName.branch_list: branch_list,
                    **other_param_dict,
                }
                current_class = Arrow
            elif state == ParameterName.cycle:
                current_param_dict = {
                    ParameterName.theta_tail: param1,
                    ParameterName.theta_head: param2,
                    ParameterName.branch_list: branch_list,
                    **other_param_dict,
                }
                current_class = ArcArrow
            else:
                raise ValueError()
            complete_param_dict = {
                **NetworkDiagramConfig.reaction_config,
                **current_param_dict,
            }
            reaction_arrow_param_dict_list.append(complete_param_dict)
            reaction_class_list.append(current_class)
        reaction_list = [
            current_class(**reaction_arrow_param_dict)
            for current_class, reaction_arrow_param_dict in zip(reaction_class_list, reaction_arrow_param_dict_list)]
        reaction_text_dict = {
            text_name: TextBox(**{
                **NetworkDiagramConfig.reaction_text_config,
                ParameterName.name: text_name,
                **text_config_dict,
            }) for text_name, text_config_dict in reaction_text_config_dict.items()
        }

        background_dict = {
            name: RoundRectangle(**{
                **NetworkDiagramConfig.background_config,
                **config_dict,
            }) for name, config_dict in background_config_dict.items()}

        other_element_dict = {
            name: element_class(**element_dict)
            for name, (element_class, element_dict) in other_element_config_dict.items()
        }

        network_diagram_dict = {
            ParameterName.metabolite: {metabolite_obj.name: metabolite_obj for metabolite_obj in metabolite_list},
            ParameterName.reaction: {reaction_obj.name: reaction_obj for reaction_obj in reaction_list},
            ParameterName.background: background_dict,
            ParameterName.text: {
                **metabolite_text_dict,
                **reaction_text_dict,
            },
            ParameterName.other_obj: other_element_dict
        }
        super().__init__(
            network_diagram_dict, Vector(0, 0), size_vector, **kwargs)
