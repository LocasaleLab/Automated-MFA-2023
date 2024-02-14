from .config import Vector, List, ParameterName, DataFigureConfig, move_and_scale_for_dict, \
    multiplied_parameter_set, initialize_vector_input
from .config import CompositeFigure, DataFigureAxes

from .data_figure_plotting_and_data_output_generator import set_ax_spine_parameter, set_ax_tick_parameter, \
    set_ax_patch_parameter


class DataFigure(CompositeFigure):
    def __init__(
            self, bottom_left: Vector, size: Vector,
            ax_bottom_left_list: List[Vector], ax_size_list: List[Vector],
            axis_param_dict=None, axis_spine_format_dict=None, axis_tick_format_dict=None,
            figure_config_dict=None, legend_obj=None, color_bar_obj=None, other_obj_list: List = None,
            background=False, twin_x_axis=False, twin_y_axis=False, broken_y_axis=None,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        # Never pass scale and bottom_left_offset to children node, but pass them to super().__init__() function.
        bottom_left = initialize_vector_input(bottom_left)
        size = initialize_vector_input(size)
        self.figure_config_dict = figure_config_dict
        self.ax_bottom_left_list = ax_bottom_left_list
        self.ax_size_list = ax_size_list
        content_axis_param_dict = {
            ParameterName.z_order: DataFigureConfig.axis_z_order,
            **({} if axis_param_dict is None else axis_param_dict)
        }
        self.twin_x_axis = twin_x_axis
        self.twin_y_axis = twin_y_axis
        self.broken_y_axis = broken_y_axis
        self.hidden_axis_parameter_dict = {
            ParameterName.visible: False,
            ParameterName.alpha: 0,
        }
        self.hidden_axis_bool_parameter_dict = {
            ParameterName.ax_top: True,
            ParameterName.ax_bottom: True,
            ParameterName.ax_left: True,
            ParameterName.ax_right: True,
        }
        self.hidden_axis_tick_bool_parameter_dict = {
            ParameterName.ax_top: False,
            ParameterName.ax_bottom: False,
            ParameterName.ax_left: False,
            ParameterName.ax_right: False,
        }
        self.axis_spine_format_dict = axis_spine_format_dict
        self.axis_tick_format_dict = axis_tick_format_dict
        assert len(ax_bottom_left_list) == len(ax_size_list)
        data_figure_axes_dict = {}
        hidden_data_figure_axes_dict = {}
        self.hidden_data_axes_transform_list = []
        for index, (raw_ax_bottom_left, raw_ax_size) in enumerate(zip(self.ax_bottom_left_list, self.ax_size_list)):
            axis_name = f'Axis_{index}'
            ax_bottom_left = bottom_left + raw_ax_bottom_left * size
            ax_size = size * raw_ax_size
            data_figure_axis_obj = DataFigureAxes(
                ax_bottom_left, ax_size, axis_param_dict=content_axis_param_dict,
                twin_x_axis=twin_x_axis, twin_y_axis=twin_y_axis, broken_y_axis=broken_y_axis)
            data_figure_axes_dict[axis_name] = data_figure_axis_obj
            hidden_data_figure_axes_dict[axis_name] = DataFigureAxes(
                ax_bottom_left, ax_size, axis_param_dict=content_axis_param_dict)
        element_type_name_dict = {
            ParameterName.data_figure_axes: data_figure_axes_dict,
            ParameterName.hidden_data_axes: hidden_data_figure_axes_dict,
        }

        if legend_obj is not None:
            self.legend = True
            element_type_name_dict[ParameterName.legend] = {ParameterName.legend: legend_obj}
        else:
            self.legend = False
        if color_bar_obj is not None:
            element_type_name_dict[ParameterName.cbar] = {ParameterName.cbar: color_bar_obj}
        if other_obj_list is not None:
            element_type_name_dict[ParameterName.other_obj] = {obj_item.name: obj_item for obj_item in other_obj_list}
        # super(DataFigure, self).__init__(bottom_left, size, figure_content_list, **kwargs)
        super(DataFigure, self).__init__(
            element_type_name_dict, bottom_left, size, background=background,
            scale=scale, bottom_left_offset=bottom_left_offset,
            base_z_order=base_z_order, z_order_increment=z_order_increment, **kwargs)

    def _set_axis_parameter(
            self, current_axis, twin_x_axis=False, twin_y_axis=False, broken_y_axis=None, hidden_axis=False):
        if hidden_axis:
            assert not isinstance(current_axis, (tuple, list))
            set_ax_spine_parameter(current_axis, {
                **self.axis_spine_format_dict,
                **self.hidden_axis_parameter_dict, }, **self.hidden_axis_bool_parameter_dict)
            set_ax_tick_parameter(current_axis, {
                **self.axis_tick_format_dict,
                **self.hidden_axis_parameter_dict, }, **self.hidden_axis_tick_bool_parameter_dict)
            set_ax_patch_parameter(current_axis, {
                **self.hidden_axis_parameter_dict, })
            return
        twin_x_setting = dict(right=True, left=False)
        twin_y_setting = dict(top=True, bottom=False)
        broken_y_top_extra_setting = dict(bottom=False)
        broken_y_middle_extra_setting = dict(bottom=False, top=False)
        setting_dict_list = [dict()]
        if not (twin_x_axis or twin_y_axis or (broken_y_axis is not None)):
            assert not isinstance(current_axis, (tuple, list))
            current_axis = [current_axis]
        elif twin_x_axis:
            setting_dict_list.append(twin_x_setting)
        elif twin_y_axis:
            setting_dict_list.append(twin_y_setting)
        elif broken_y_axis is not None:
            total_y_axis_num = len(broken_y_axis)
            for axis_index in range(1, total_y_axis_num):
                if axis_index == total_y_axis_num - 1:
                    setting_dict_list.append(broken_y_top_extra_setting)
                else:
                    setting_dict_list.append(broken_y_middle_extra_setting)
        for each_axis, setting_dict in zip(current_axis, setting_dict_list):
            set_ax_spine_parameter(each_axis, self.axis_spine_format_dict)
            set_ax_tick_parameter(each_axis, self.axis_tick_format_dict, **setting_dict)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        axis_element_dict = super(DataFigure, self).draw(fig, parent_ax, parent_transformation)
        data_figure_axis_trans_list = []
        for axis_name, (current_axis, current_axis_transformation) in \
                axis_element_dict[ParameterName.data_figure_axes].items():
            self._set_axis_parameter(current_axis, self.twin_x_axis, self.twin_y_axis, self.broken_y_axis)
            data_figure_axis_trans_list.append((current_axis, current_axis_transformation))
        for axis_name, (current_axis, current_axis_transformation) in \
                axis_element_dict[ParameterName.hidden_data_axes].items():
            self._set_axis_parameter(current_axis, hidden_axis=True)
            self.hidden_data_axes_transform_list.append((current_axis, current_axis_transformation))
        return data_figure_axis_trans_list

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        super().move_and_scale(
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)
        move_and_scale_for_dict(
            self.axis_spine_format_dict, scale=scale, multiplied_parameter_set=multiplied_parameter_set)
        move_and_scale_for_dict(
            self.axis_tick_format_dict, scale=scale, multiplied_parameter_set=multiplied_parameter_set)
        for config_name, config_dict in self.figure_config_dict.items():
            if isinstance(config_dict, dict):
                move_and_scale_for_dict(
                    config_dict, scale=scale, multiplied_parameter_set=multiplied_parameter_set)
            elif isinstance(config_dict, (tuple, list)):
                for each_config_dict in config_dict:
                    if isinstance(each_config_dict, dict):
                        move_and_scale_for_dict(
                            each_config_dict, scale=scale, multiplied_parameter_set=multiplied_parameter_set)


