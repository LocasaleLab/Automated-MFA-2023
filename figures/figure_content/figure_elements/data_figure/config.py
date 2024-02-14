from ...common.config import it, np, Vector, ColorConfig, ZOrderConfig, LineStyle, \
    ParameterName, DataFigureParameterName, FontWeight, HorizontalAlignment, VerticalAlignment, \
    default_parameter_extract, GeneralElements, symmetrical_lim_tick_generator_with_zero, \
    net_flux_x_axis_labels_generator, merge_axis_format_dict, DataFigureConfig, t_test_of_two_groups, \
    initialize_vector_input, generate_violin_config_dict, Direct, BasicFigureData, \
    heatmap_and_box3d_parameter_preparation
from ...common.common_figure_materials import DataName, ModelDataSensitivityDataFigureConfig, Keywords, \
    CommonFigureString, ProtocolSearchingMaterials, CommonFigureMaterials

ColorBarDataFigure = GeneralElements.ColorBarDataFigure
HeatmapConfig = GeneralElements.HeatmapConfig
HeatmapDataFigure = GeneralElements.HeatmapDataFigure
ScatterDataFigure = GeneralElements.ScatterDataFigure
BarDataFigure = GeneralElements.BarDataFigure
BasicFluxErrorBarDataFigure = GeneralElements.FluxErrorBarDataFigure
BasicMIDComparisonGridBarDataFigure = GeneralElements.MIDComparisonGridBarDataFigure
ViolinBoxDataFigure = GeneralElements.ViolinBoxDataFigure
HistogramDataFigure = GeneralElements.HistogramDataFigure


def heatmap_highlight_ellipse_parameter(data_name, **kwargs):
    common_ellipse_config = {
        ParameterName.edge_width: 0.5,
        ParameterName.edge_color: ColorConfig.orange,
        ParameterName.face_color: None,
        ParameterName.z_order: ZOrderConfig.default_legend_z_order,
    }
    config_dict = {
        DataName.raw_model_all_data: {
            ParameterName.center: Vector(6.4, 5.4),
            ParameterName.width: 2,
            ParameterName.height: 5.5,
            ParameterName.angle: -45,
        },
        DataName.raw_model_raw_data: {
            ParameterName.center: Vector(6.5, 3.7),
            ParameterName.width: 3.8,
            ParameterName.height: 3,
            ParameterName.angle: 0,
        }
    }
    target_config_dict = config_dict[data_name]
    target_config_dict.update(common_ellipse_config)
    return target_config_dict


def sensitivity_heatmap_cbar_axis_label_dict(data_name, **kwargs):
    if data_name in {DataName.data_sensitivity, DataName.data_sensitivity_with_noise}:
        # return (-1, 1), [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1]
        data_lim = [-1, 1]
        data_tick_interval = 0.2
    else:
        # return (-0.5, 0.5), [-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5]
        data_lim = [-0.5, 0.5]
        data_tick_interval = 0.1
    data_tick = np.arange(data_lim[0], data_lim[1] + 1e-5, data_tick_interval)
    return data_lim, data_tick


def sensitivity_heatmap_y_axis_labels_generator(data_name, result_label_list, **kwargs):
    def analyze_one_list(_data_name, _current_label_dict, _result_label_list):
        if _data_name in _current_label_dict:
            replace = False
            label_dict_for_current_data = _current_label_dict[_data_name]
        elif _data_name in data_name_replace_dict:
            replace = True
            original_data_name = data_name_replace_dict[_data_name]
            label_dict_for_current_data = _current_label_dict[original_data_name]
        else:
            raise ValueError()

        last_separator_location = 0
        group_id_list = list(label_dict_for_current_data.keys())
        _final_tick_label_list = []
        _group_separator_list = [last_separator_location]
        _group_name_location_list = []
        _group_name_list = []
        current_group_index = 0
        current_group_id = group_id_list[current_group_index]
        current_group_label_dict = label_dict_for_current_data[current_group_id]
        for result_label_index, result_label in enumerate(_result_label_list + [None]):
            next_group = False
            # if result_label in raw_model_data_label_dict:
            #     # if _data_name in data_sensitivity_dict:
            #     #     if result_label == raw_data_label or result_label == raw_data_noise_label:
            #     #         # current_tick_label = 'Experimental data'
            #     #         current_tick_label = CommonFigureString.experimental_data
            #     #     else:
            #     #         # current_tick_label = 'All data'
            #     #         current_tick_label = CommonFigureString.all_data
            #     # else:
            #     #     if _data_name in model_sensitivity_dict or _data_name in model_sensitivity_all_data_dict:
            #     #         # current_tick_label = 'Raw model'
            #     #         current_tick_label = CommonFigureString.raw_model
            #     #     elif _data_name in {DataName.different_flux_range, DataName.different_flux_range_all_data}:
            #     #         # current_tick_label = 'Raw config (Low LB + Medium UB)'
            #     #         current_tick_label = CommonFigureString.raw_config_bound
            #     #     else:
            #     #         # current_tick_label = 'Raw config (GLC only)'
            #     #         current_tick_label = CommonFigureString.raw_config_input_flux
            #     #     new_separator_location = result_label_index + 1
            #     #     _group_separator_list.append(new_separator_location)
            #     #     last_separator_location = new_separator_location
            #     current_tick_label = group_id_name_dict[_data_name][result_label]
            #     _final_tick_label_list.append(current_tick_label)
            #     new_separator_location = result_label_index + 1
            #     _group_separator_list.append(new_separator_location)
            #     last_separator_location = new_separator_location
            # else:
            if result_label is None:
                next_group = True
                current_tick_label = None
            else:
                if replace:
                    result_label = ModelDataSensitivityDataFigureConfig.modify_all_data_to_raw_data(
                        ModelDataSensitivityDataFigureConfig.modify_noise_data_to_raw_data(result_label))
                if result_label not in current_group_label_dict:
                    next_group = True
                    current_tick_label = None
                else:
                    current_tick_label = current_group_label_dict[result_label]
            if next_group:
                new_separator_location = result_label_index
                _group_separator_list.append(new_separator_location)
                if isinstance(current_group_id, str):
                    _group_name_list.append(group_id_name_dict[current_group_id])
                    _group_name_location_list.append((last_separator_location + new_separator_location) / 2)
                last_separator_location = new_separator_location
                if result_label is not None:
                    current_group_index += 1
                    new_group_id = group_id_list[current_group_index]
                    new_group_label_dict = label_dict_for_current_data[new_group_id]
                    if current_tick_label is None:
                        current_tick_label = new_group_label_dict[result_label]
                    _final_tick_label_list.append(current_tick_label)
                    current_group_id = new_group_id
                    current_group_label_dict = new_group_label_dict
            else:
                _final_tick_label_list.append(current_tick_label)
        return _final_tick_label_list, _group_separator_list, _group_name_location_list, _group_name_list

    def multiple_list_raw_model_label_transform(_data_name):
        if _data_name == DataName.model_sensitivity or _data_name == DataName.model_sensitivity_all_data:
            current_tick_label = CommonFigureString.raw_model
        elif _data_name == DataName.config_sensitivity or _data_name == DataName.config_sensitivity_all_data:
            current_tick_label = CommonFigureString.raw_config_bound
        else:
            raise ValueError()
        return current_tick_label

    def analyze_model_sensitivity_multiple_list(_data_name, _current_label_dict, _result_label_list):
        _final_tick_label_list = []
        _minor_group_separator_list = []
        _major_group_separator_list = []
        _minor_group_name_location_list = []
        _minor_group_name_list = []
        _major_group_name_location_list = []
        _major_group_name_list = []
        model_sensitivity_label_dict = _current_label_dict[_data_name]
        previous_total_tick_num = 0
        for current_model_sensitivity_data_label, current_result_label_list in _result_label_list.items():
            if current_model_sensitivity_data_label in raw_model_data_label_dict:
                if len(_major_group_separator_list) == 0:
                    _major_group_separator_list.append(previous_total_tick_num)
                _major_group_separator_list.append(previous_total_tick_num + 1)
                # current_tick_label = multiple_list_raw_model_label_transform(_data_name)
                current_tick_label = group_id_name_dict[current_model_sensitivity_data_label][_data_name]
                _final_tick_label_list.append(current_tick_label)
                current_total_tick_num = 1
            else:
                (
                    current_tick_label_list, current_group_separator_list, current_group_name_location_list,
                    current_group_name_list) = analyze_one_list(
                    current_model_sensitivity_data_label, model_sensitivity_label_dict, current_result_label_list)
                current_total_tick_num = len(current_tick_label_list)
                current_group_separator_list = [
                    current_group_separator + previous_total_tick_num
                    for current_group_separator in current_group_separator_list
                ]
                current_group_name_location_list = [
                    current_group_name_location + previous_total_tick_num
                    for current_group_name_location in current_group_name_location_list
                ]
                _final_tick_label_list.extend(current_tick_label_list)
                _minor_group_separator_list.extend(current_group_separator_list[1:-1])
                if len(_major_group_separator_list) == 0:
                    _major_group_separator_list.append(current_group_separator_list[0])
                _major_group_separator_list.append(current_group_separator_list[-1])
                _minor_group_name_list.extend(current_group_name_list)
                _minor_group_name_location_list.extend(current_group_name_location_list)
                _major_group_name_list.append(group_id_name_dict[current_model_sensitivity_data_label])
                _major_group_name_location_list.append((current_total_tick_num + 2 * previous_total_tick_num) / 2)
            previous_total_tick_num += current_total_tick_num
        return _final_tick_label_list, _minor_group_separator_list, _minor_group_name_location_list, \
            _minor_group_name_list, _major_group_separator_list, _major_group_name_location_list, \
            _major_group_name_list

    def analyze_data_sensitivity_multiple_list(_data_name, _current_label_dict, _result_label_list):
        _final_tick_label_list = []
        _major_group_separator_list = []
        _major_group_name_location_list = []
        _major_group_name_list = []
        data_sensitivity_label_dict = _current_label_dict[data_name]
        previous_total_tick_num = 0
        for current_data_sensitivity_data_label, current_result_label_list in _result_label_list.items():
            (
                current_tick_label_list, *_) = analyze_one_list(
                current_data_sensitivity_data_label, data_sensitivity_label_dict, current_result_label_list)

        _minor_group_separator_list = None
        _minor_group_name_location_list = None
        _minor_group_name_list = None
        return _final_tick_label_list, _minor_group_separator_list, _minor_group_name_location_list, \
            _minor_group_name_list, _major_group_separator_list, _major_group_name_location_list, \
            _major_group_name_list

    data_name_replace_dict = {
        DataName.merge_reversible_reaction_all_data: DataName.merge_reversible_reaction,
        DataName.combine_consecutive_reactions_all_data: DataName.combine_consecutive_reactions,
        DataName.prune_branches_all_data: DataName.prune_branches,
        DataName.data_sensitivity_with_noise: DataName.data_sensitivity,
        DataName.different_constant_flux_all_data: DataName.different_constant_flux,
        DataName.different_constant_flux_with_noise: DataName.different_constant_flux,
        DataName.different_constant_flux_with_noise_all_data: DataName.different_constant_flux,
        DataName.different_flux_range_all_data: DataName.different_flux_range,
    }
    current_label_dict = ModelDataSensitivityDataFigureConfig.label_dict
    raw_model_data_label_dict = ModelDataSensitivityDataFigureConfig.raw_model_data_label_dict
    raw_data_label = ModelDataSensitivityDataFigureConfig.raw_data_result_label
    raw_data_noise_label = ModelDataSensitivityDataFigureConfig.raw_data_noise_result_label
    model_sensitivity_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
    model_sensitivity_all_data_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_all_data_dict
    data_sensitivity_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_label_dict
    group_id_name_dict = ModelDataSensitivityDataFigureConfig.group_id_name_dict

    if data_name == DataName.different_constant_flux_with_noise:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_model_sensitivity_multiple_list(
            DataName.config_sensitivity, current_label_dict, result_label_list)
    elif data_name in {
            DataName.model_sensitivity, DataName.model_sensitivity_all_data,
            DataName.config_sensitivity, DataName.config_sensitivity_all_data}:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_model_sensitivity_multiple_list(
            data_name, current_label_dict, result_label_list)
    elif data_name in {DataName.data_sensitivity, DataName.data_sensitivity_with_noise}:
        # (
        #     final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
        #     minor_group_name_list, major_group_separator_list, major_group_name_location_list,
        #     major_group_name_list) = analyze_data_sensitivity_multiple_list(
        #     data_name, current_label_dict, result_label_list)

        (
            final_tick_label_list, major_group_separator_list, major_group_name_location_list,
            major_group_name_list) = analyze_one_list(data_name, current_label_dict, result_label_list)
        minor_group_separator_list = None
        minor_group_name_location_list = None
        minor_group_name_list = None
    else:
        (
            final_tick_label_list, minor_group_separator_list, minor_group_name_location_list,
            minor_group_name_list) = analyze_one_list(data_name, current_label_dict, result_label_list)
        major_group_separator_list = None
        major_group_name_location_list = None
        major_group_name_list = None

    total_item_num = len(final_tick_label_list)
    if minor_group_name_list is not None:
        minor_group_separator_array = (total_item_num - np.array(minor_group_separator_list)) / total_item_num
        minor_group_name_location_array = (total_item_num - np.array(minor_group_name_location_list)) / total_item_num
    else:
        minor_group_separator_array = None
        minor_group_name_location_array = None
    if major_group_separator_list is not None:
        major_group_separator_location_array = (total_item_num - np.array(major_group_separator_list)) / total_item_num
        major_group_name_location_array = (total_item_num - np.array(major_group_name_location_list)) / total_item_num
    else:
        major_group_separator_location_array = None
        major_group_name_location_array = None
    return final_tick_label_list, minor_group_separator_array, minor_group_name_location_array, minor_group_name_list, \
        major_group_separator_location_array, major_group_name_location_array, major_group_name_list

