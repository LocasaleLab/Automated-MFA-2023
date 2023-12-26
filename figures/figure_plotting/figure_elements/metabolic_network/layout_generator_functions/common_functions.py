from ..config import np, Vector, MetaboliteConfig, ParameterName, convert_theta_to_coordinate, LegendConfig

metabolite_height = MetaboliteConfig.height
metabolite_width = MetaboliteConfig.width


def calculate_reaction_between_adjacent_metabolites(
        start_metabolite_center_location, end_metabolite_center_location, horizontal_or_vertical,
        start_arrow, end_arrow):
    if horizontal_or_vertical == ParameterName.horizontal:
        metabolite_length_this_direction = metabolite_width
    elif horizontal_or_vertical == ParameterName.vertical:
        metabolite_length_this_direction = metabolite_height
    else:
        raise ValueError()
    arrow_interval = MetaboliteConfig.interval_to_metabolite_ratio[
        ParameterName.arrow][horizontal_or_vertical]
    blunt_interval = MetaboliteConfig.interval_to_metabolite_ratio[
        ParameterName.blunt][horizontal_or_vertical]
    interval_to_metabolite_start = arrow_interval if start_arrow else blunt_interval
    interval_to_metabolite_end = arrow_interval if end_arrow else blunt_interval
    if end_metabolite_center_location < start_metabolite_center_location:
        metabolite_length_this_direction = -metabolite_length_this_direction
        interval_to_metabolite_end = -interval_to_metabolite_end
        interval_to_metabolite_start = -interval_to_metabolite_start
    reaction_end_location = end_metabolite_center_location - metabolite_length_this_direction / 2 - \
        interval_to_metabolite_end
    reaction_start_location = start_metabolite_center_location + metabolite_length_this_direction / 2 + \
        interval_to_metabolite_start
    return reaction_start_location, reaction_end_location


def add_straight_reaction_between_metabolites(
        start_metabolite_center_location, end_metabolite_center_location, horizontal_or_vertical,
        other_coordinate_value, target_reaction_obj, extra_param_dict=None):
    start_location, end_location = calculate_reaction_between_adjacent_metabolites(
        start_metabolite_center_location, end_metabolite_center_location, horizontal_or_vertical,
        *target_reaction_obj.judge_bidirectional_flag())
    if horizontal_or_vertical == ParameterName.horizontal:
        start_vector = Vector(start_location, other_coordinate_value)
        end_vector = Vector(end_location, other_coordinate_value)
    elif horizontal_or_vertical == ParameterName.vertical:
        start_vector = Vector(other_coordinate_value, start_location)
        end_vector = Vector(other_coordinate_value, end_location)
    else:
        raise ValueError()
    if extra_param_dict is None:
        extra_param_dict = {}
    target_reaction_obj.extend_reaction_start_end_list([
        (ParameterName.normal, start_vector, end_vector, extra_param_dict)])
    return target_reaction_obj


def add_bent_reaction_between_metabolites(
        start_metabolite_location, start_metabolite_other_coordinate, start_metabolite_direction,
        end_metabolite_location, end_metabolite_other_coordinate,
        target_reaction_obj, extra_param_dict=None):
    start_arrow, end_arrow = target_reaction_obj.judge_bidirectional_flag()
    rotation_direction_indicator = (end_metabolite_location - start_metabolite_other_coordinate) * \
        (end_metabolite_other_coordinate - start_metabolite_location)
    if start_metabolite_direction == ParameterName.horizontal:
        direction_tuple = (ParameterName.horizontal, ParameterName.vertical)
        start_end_location_index_tuple = (0, 1)
        start_vector_array = np.array([0, start_metabolite_other_coordinate])
        end_vector_array = np.array([end_metabolite_other_coordinate, 0])
        if rotation_direction_indicator > 0:
            rotation_direction = ParameterName.ccw
        else:
            rotation_direction = ParameterName.cw
    elif start_metabolite_direction == ParameterName.vertical:
        direction_tuple = (ParameterName.vertical, ParameterName.horizontal)
        start_end_location_index_tuple = (1, 0)
        start_vector_array = np.array([start_metabolite_other_coordinate, 0])
        end_vector_array = np.array([0, end_metabolite_other_coordinate])
        if rotation_direction_indicator > 0:
            rotation_direction = ParameterName.cw
        else:
            rotation_direction = ParameterName.ccw
    else:
        raise ValueError()
    start_location, _ = calculate_reaction_between_adjacent_metabolites(
        start_metabolite_location, end_metabolite_other_coordinate, direction_tuple[0], start_arrow, False)
    _, end_location = calculate_reaction_between_adjacent_metabolites(
        start_metabolite_other_coordinate, end_metabolite_location, direction_tuple[1], False, end_arrow)
    if extra_param_dict is None:
        extra_param_dict = {}
    start_vector_array[start_end_location_index_tuple[0]] = start_location
    end_vector_array[start_end_location_index_tuple[1]] = end_location
    target_reaction_obj.extend_reaction_start_end_list([
        (
            ParameterName.bent,
            Vector(array=start_vector_array),
            Vector(array=end_vector_array),
            rotation_direction,
            extra_param_dict
        )
    ])
    return target_reaction_obj


def cycle_layout(
        cycle_center, cycle_radius, cycle_metabolite_obj_list, cycle_metabolite_theta_list,
        cycle_reaction_obj_list, cycle_reaction_theta_list, display_text_theta_list, display_text_radius_ratio_list):
    for metabolite_index, metabolite_obj in enumerate(cycle_metabolite_obj_list):
        current_metabolite_theta = cycle_metabolite_theta_list[metabolite_index]
        current_metabolite_coordinate = convert_theta_to_coordinate(
            current_metabolite_theta, cycle_center, cycle_radius)
        metabolite_obj.set_center(current_metabolite_coordinate)
        display_text_theta = display_text_theta_list[metabolite_index]
        display_text_radius_ratio = display_text_radius_ratio_list[metabolite_index]
        reaction_obj = cycle_reaction_obj_list[metabolite_index]
        theta_tail_tuple, theta_head_tuple = cycle_reaction_theta_list[metabolite_index]
        tail_arrow, head_arrow = reaction_obj.judge_bidirectional_flag()
        reaction_obj.extend_reaction_start_end_list([
            (
                ParameterName.cycle,
                theta_tail_tuple[1 if tail_arrow else 0],
                theta_head_tuple[1 if head_arrow else 0],
                cycle_center,
                cycle_radius,
                {}
            )
        ]).set_display_text_config_dict({
            ParameterName.center: convert_theta_to_coordinate(
                display_text_theta, cycle_center, cycle_radius * display_text_radius_ratio),
        })


def arrange_text_by_row(
        current_flux_range_string_dict, text_left_offset, output_text_config_list, title_config, normal_text_config,
        round_rectangle_config_list, common_round_rectangle_config_dict):
    for data_label, (
            current_title_str, left_right_x_range, title_center_vector, normal_text_row_y_location_list,
            normal_text_string_list, data_rectangle_pair, data_rectangle_config
    ) in current_flux_range_string_dict.items():
        if current_title_str is not None:
            output_text_config_list.append({
                **title_config,
                ParameterName.string: current_title_str,
                ParameterName.center: title_center_vector,
            })
        current_text_item_left, current_text_item_right = left_right_x_range
        for row_index, (row_y_location, string_row) in enumerate(zip(
                normal_text_row_y_location_list, normal_text_string_list)):
            current_col_num = len(string_row)
            col_width = (current_text_item_right - current_text_item_left) / current_col_num
            each_col_left_x_location = \
                np.linspace(current_text_item_left, current_text_item_right, current_col_num + 1)[:-1] \
                + text_left_offset
            for left_x_location, current_string in zip(each_col_left_x_location, string_row):
                output_text_config_list.append({
                    **normal_text_config,
                    ParameterName.string: current_string,
                    ParameterName.center: Vector(
                        left_x_location + normal_text_config[ParameterName.width] / 2, row_y_location)
                })
        if data_rectangle_pair is not None:
            (rectangle_left, rectangle_right), (rectangle_bottom, rectangle_top) = data_rectangle_pair
            round_rectangle_config_list.append({
                **common_round_rectangle_config_dict,
                ParameterName.name: data_label,
                ParameterName.center: Vector(
                    (rectangle_left + rectangle_right) / 2, (rectangle_bottom + rectangle_top) / 2),
                ParameterName.width: (rectangle_right - rectangle_left),
                ParameterName.height: (rectangle_top - rectangle_bottom),
                **data_rectangle_config,
            })


def text_comment_layout_generator(mode, metabolic_network_text_comment_config_dict):
    total_width = LegendConfig.legend_width
    total_height = 0.2
    reaction_flux_num = metabolic_network_text_comment_config_dict[ParameterName.reaction_flux_num]
    total_flux_num = metabolic_network_text_comment_config_dict[ParameterName.total_flux_num]
    total_mid_num = metabolic_network_text_comment_config_dict[ParameterName.total_mid_num]
    mid_metabolite_num = metabolic_network_text_comment_config_dict[ParameterName.mid_metabolite_num]
    text_str_dict = {
        'reaction_flux_num': f'{reaction_flux_num} reaction fluxes',
        'total_flux_num': f'{total_flux_num} total fluxes',
        'total_mid_num': f'{total_mid_num} independent MIDs',
        'mid_metabolite_num': f'{mid_metabolite_num} metabolite with MIDs',
    }
    total_text_num = len(text_str_dict)
    each_width = total_width
    each_height = total_height / total_text_num
    common_center_x = total_width / 2

    text_param_dict = {}
    for text_index, (text_name, text_str) in enumerate(text_str_dict.items()):
        current_center_y = total_height - each_height * (text_index + 0.5)
        current_param_dict = {
            ParameterName.string: text_str,
            ParameterName.center: Vector(common_center_x, current_center_y),
            ParameterName.width: each_width,
            ParameterName.height: each_height,
        }
        text_param_dict[text_name] = current_param_dict
    return text_param_dict, total_width, total_height
