from .config import np, transforms, plt, float_type, axis_for_test, ParameterName, Vector, \
    SubfigureLabelLoc, VerticalAlignment, HorizontalAlignment, FontWeight, ColorConfig, TextConfig, ZOrderConfig, \
    initialize_vector_input

from .basic_region import Region
from .shapes import Rectangle
from .modified_text import TextBox


class Subplot(Region):
    def __init__(
            self, bottom_left: Vector, size: Vector, content: list = None, with_frame: bool = axis_for_test,
            axis_param_dict=None, **kwargs):
        # bottom_left and size are defined based on relative ratio of width and height to parent axis.
        super(Subplot, self).__init__(bottom_left, size, **kwargs)
        if content is None:
            content = []
        self.content_list = content
        self.with_frame = with_frame
        self.axis_param_dict = {} if axis_param_dict is None else axis_param_dict

    @property
    def rect(self):
        return [*self.bottom_left, *self.size]

    def generate_mpl_axes(self, fig, parent_ax):
        figure_width, figure_height = fig.get_size_inches()
        height_to_width_ratio = figure_height / figure_width
        # A point in matplotlib figure is located by its pixel.
        # Pixel of width/height is calculated by width/height (inches) * ppi.
        # All number in plotting instruction file is normalized by figure width.
        # Therefore, the basic transformation is to multiply raw number with real width and ppi
        complete_transformation = transforms.Affine2D(
            matrix=np.array([[figure_width, 0, 0], [0, figure_width, 0], [0, 0, 1]])) + fig.dpi_scale_trans
        if parent_ax is None:
            this_layer_transformation = complete_transformation
            current_axis = fig.add_axes(self.rect, **self.axis_param_dict)
        else:
            # If there is parent axis, axis construction need to use the relative value to parent axis.
            parent_axis_rect = parent_ax.get_position().bounds
            axis_rect_transformation = transforms.Affine2D(
                matrix=np.array([
                    [parent_axis_rect[2], 0, parent_axis_rect[0]],
                    [0, parent_axis_rect[3], parent_axis_rect[1]],
                    [0, 0, 1]], dtype=float_type))
            new_rect_loc = axis_rect_transformation.transform(self.bottom_left)
            new_rect_size = self.size * parent_axis_rect[2:]
            current_axis = fig.add_axes([*new_rect_loc, *new_rect_size], **self.axis_param_dict)
            # All shape in new axis will move based on offset of the new axis.
            # Notice that the height offset of the new axis is based on figure height,
            # but all coordinates will be stretched based on figure width.
            # Therefore, the height offset should be multiplied with height_to_width_ratio
            this_layer_transformation = transforms.ScaledTranslation(0, 0, transforms.Affine2D(
                matrix=np.array([
                    [1, 0, new_rect_loc[0]],
                    [0, 1, new_rect_loc[1] * height_to_width_ratio],
                    [0, 0, 1]], dtype=float_type)
            ))
            complete_transformation = this_layer_transformation + complete_transformation
        if not self.with_frame:
            current_axis.set_axis_off()
        return current_axis, complete_transformation

    def draw(self, fig=None, parent_ax=None, parent_transformation=None):
        assert fig is not None
        current_axis, complete_transformation = self.generate_mpl_axes(fig, parent_ax)
        content_obj_list = []
        for content_obj in self.content_list:
            content_obj_list.append(content_obj.draw(fig, current_axis, complete_transformation))
        return current_axis, complete_transformation, content_obj_list


class DataFigureAxes(Region):
    def __init__(
            self, bottom_left: Vector, size: Vector, axis_param_dict=None, twin_x_axis=False, twin_y_axis=False,
            broken_y_axis=None, **kwargs):
        # bottom_left and size are defined based on relative ratio of width of paper.
        self.axis_param_dict = {} if axis_param_dict is None else axis_param_dict
        self.twin_x_axis = twin_x_axis
        self.twin_y_axis = twin_y_axis
        if broken_y_axis is not None:
            assert isinstance(broken_y_axis, (tuple, list)) and np.ndim(broken_y_axis) == 2
        self.broken_y_axis = broken_y_axis
        if (twin_x_axis or twin_y_axis) and broken_y_axis:
            raise ValueError('Twin axis and broken axis cannot appear at the same time!')
        super().__init__(bottom_left, size, **kwargs)

    @staticmethod
    def _set_axis_parameter(ax, z_order=None):
        param_dict = {}
        if z_order is not None:
            param_dict['zorder'] = z_order
        ax.set(**param_dict)

    @staticmethod
    def _generate_scaled_translation_from_axis_location(axis_location, height_to_width_ratio):
        target_transformation = transforms.ScaledTranslation(0, 0, transforms.Affine2D(
            matrix=np.array([
                [1, 0, axis_location[0]],
                [0, 1, axis_location[1] * height_to_width_ratio],
                [0, 0, 1]], dtype=float_type)
        ))
        return target_transformation

    def generate_mpl_axes(self, fig, parent_ax):
        figure_width, figure_height = fig.get_size_inches()
        height_to_width_ratio = figure_height / figure_width
        complete_transformation = transforms.Affine2D(
            matrix=np.array([[figure_width, 0, 0], [0, figure_width, 0], [0, 0, 1]])) + fig.dpi_scale_trans
        parent_axis_rect = parent_ax.get_position().bounds
        axis_rect_transformation = transforms.Affine2D(
            matrix=np.array([
                [parent_axis_rect[2], 0, parent_axis_rect[0]],
                [0, parent_axis_rect[3], parent_axis_rect[1]],
                [0, 0, 1]], dtype=float_type))
        new_rect_loc = axis_rect_transformation.transform(self.bottom_left) * Vector(1, 1 / height_to_width_ratio)
        new_rect_size = self.size * parent_axis_rect[2:] * Vector(1, 1 / height_to_width_ratio)
        # new_rect_loc = self.bottom_left * Vector(1, 1 / height_to_width_ratio)
        # new_rect_size = self.size * Vector(1, 1 / height_to_width_ratio)
        # current_axis = fig.add_axes([*new_rect_loc, *new_rect_size], **self.axis_param_dict)
        this_layer_transformation = self._generate_scaled_translation_from_axis_location(
            new_rect_loc, height_to_width_ratio)
        if self.broken_y_axis is not None:
            new_rect_width, new_rect_height = new_rect_size
            y_ratio_pair_list = self.broken_y_axis
            current_axis_list = []
            complete_transformation_list = []
            total_pair_num = len(y_ratio_pair_list)
            current_axis = None
            for ratio_pair_index, current_y_ratio_pair in enumerate(y_ratio_pair_list):
                bottom, top = current_y_ratio_pair
                current_y_ratio = top - bottom
                current_rect_loc = new_rect_loc + Vector(0, new_rect_height * bottom)
                current_rect_size = Vector(new_rect_width, new_rect_height * current_y_ratio)
                new_axis = fig.add_axes([*current_rect_loc, *current_rect_size])
                self._set_axis_parameter(new_axis, **self.axis_param_dict)
                current_axis_list.append(new_axis)
                if ratio_pair_index != 0:
                    new_axis.spines['bottom'].set_visible(False)
                if ratio_pair_index != total_pair_num - 1:
                    new_axis.spines['top'].set_visible(False)
                this_layer_current_transformation = self._generate_scaled_translation_from_axis_location(
                    current_rect_loc, height_to_width_ratio)
                current_transformation = this_layer_current_transformation + complete_transformation
                complete_transformation_list.append(current_transformation)
            complete_transformation = complete_transformation_list

            # bottom_top_ratio, top_bottom_ratio = self.broken_y_axis
            # bottom_rect_size = Vector(new_rect_width, new_rect_height * bottom_top_ratio)
            # bottom_rect_loc = new_rect_loc
            # top_rect_size = Vector(new_rect_width, new_rect_height * (1 - top_bottom_ratio))
            # top_rect_loc = new_rect_loc + Vector(0, new_rect_height * top_bottom_ratio)
            # bottom_axis = fig.add_axes([*bottom_rect_loc, *bottom_rect_size])
            # self._set_axis_parameter(bottom_axis, **self.axis_param_dict)
            # top_axis = fig.add_axes([*top_rect_loc, *top_rect_size])
            # self._set_axis_parameter(top_axis, **self.axis_param_dict)
            # current_axis_list = [bottom_axis, top_axis]
            # current_axis = None
            # top_axis.spines['bottom'].set_visible(False)
            # bottom_axis.spines['top'].set_visible(False)
            # bottom_transformation = this_layer_transformation + complete_transformation
            # this_layer_top_transformation = self._generate_scaled_translation_from_axis_location(
            #     top_rect_loc, height_to_width_ratio)
            # top_transformation = this_layer_top_transformation + complete_transformation
            # complete_transformation = (bottom_transformation, top_transformation)
        else:
            current_axis = fig.add_axes([*new_rect_loc, *new_rect_size])
            self._set_axis_parameter(current_axis, **self.axis_param_dict)
            current_axis_list = [current_axis]
            complete_transformation = this_layer_transformation + complete_transformation
        if self.twin_x_axis:
            twin_x_axis = current_axis.twinx()
            # twin_x_axis.set(**self.axis_param_dict)
            self._set_axis_parameter(twin_x_axis, **self.axis_param_dict)
            current_axis_list.append(twin_x_axis)
        if self.twin_y_axis:
            twin_y_axis = current_axis.twiny()
            # twin_y_axis.set(**self.axis_param_dict)
            self._set_axis_parameter(twin_y_axis, **self.axis_param_dict)
            current_axis_list.append(twin_y_axis)
        if len(current_axis_list) > 1:
            current_axis = current_axis_list
        # this_layer_transformation = transforms.ScaledTranslation(0, 0, transforms.Affine2D(
        #     matrix=np.array([
        #         [1, 0, new_rect_loc[0]],
        #         [0, 1, new_rect_loc[1] * height_to_width_ratio],
        #         [0, 0, 1]], dtype=float_type)
        # ))
        return current_axis, complete_transformation

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert fig is not None
        current_axis, complete_transformation = self.generate_mpl_axes(fig, parent_ax)
        return current_axis, complete_transformation


class CompositeFigure(Region):
    total_width = 1
    height_to_width_ratio = 1

    def __init__(
            self, element_type_name_dict, bottom_left, size, background=False,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        self.element_dict_by_type_name = element_type_name_dict
        if background:
            element_type_name_dict[ParameterName.background] = {
                ParameterName.background: Rectangle(**{
                    ParameterName.center: bottom_left + size / 2,
                    ParameterName.width: size[0],
                    ParameterName.height: size[1],
                    ParameterName.face_color: ColorConfig.light_gray,
                    ParameterName.edge_width: 0.5,
                    ParameterName.z_order: 0
                })
            }
        super().__init__(bottom_left, size, **kwargs)
        self.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        pass

    def move_and_scale(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1):
        if scale == 1 and bottom_left_offset is None:
            return
        elif bottom_left_offset is not None:
            bottom_left_offset = initialize_vector_input(bottom_left_offset)
        for element_type, element_dict_by_name in self.element_dict_by_type_name.items():
            for element_name, element_obj in element_dict_by_name.items():
                element_obj.move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)
        super().move_and_scale(scale, bottom_left_offset, base_z_order, z_order_increment)

    def draw(self, fig, parent_ax=None, parent_transformation=None):
        assert parent_ax is not None
        axis_element_dict = {}
        for element_type, element_dict_by_name in self.element_dict_by_type_name.items():
            if element_type not in axis_element_dict:
                axis_element_dict[element_type] = {}
            for element_name, element_obj in element_dict_by_name.items():
                axis_element_dict[element_type][element_name] = element_obj.draw(fig, parent_ax, parent_transformation)
        return axis_element_dict

    @staticmethod
    def calculate_center(self, scale, *args):
        return Vector(self.total_width, self.total_width * self.height_to_width_ratio) / 2 * scale


class SubfigureConfig(object):
    label_top_bottom_margin = 0.01
    label_left_right_margin = 0.01
    label_width = 0.02
    label_height = 0.02

    common_label_text_config = {
        ParameterName.width: label_width,
        ParameterName.height: label_height,
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: 10,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.center,
        ParameterName.z_order: ZOrderConfig.default_subfigure_label_z_order,
    }

    @staticmethod
    def label_text_generator(
            bottom_left: Vector, size: Vector, subfigure_label: str, subfigure_label_loc: SubfigureLabelLoc):
        left_right_margin = SubfigureConfig.label_left_right_margin
        top_bottom_margin = SubfigureConfig.label_top_bottom_margin
        width = SubfigureConfig.label_width
        height = SubfigureConfig.label_height
        if subfigure_label_loc == SubfigureLabelLoc.upper_left:
            label_center = bottom_left + Vector(0, size[1]) + \
                Vector(left_right_margin, -top_bottom_margin) + Vector(width, -height) / 2
        elif subfigure_label_loc == SubfigureLabelLoc.bottom_left:
            label_center = bottom_left + \
                Vector(left_right_margin, top_bottom_margin) + Vector(width, height) / 2
        elif subfigure_label_loc == SubfigureLabelLoc.upper_right:
            label_center = bottom_left + size + \
                Vector(-left_right_margin, -top_bottom_margin) + Vector(-width, -height) / 2
        else:
            label_center = bottom_left + Vector(size[0], 0) + \
                Vector(-left_right_margin, top_bottom_margin) + Vector(-width, height) / 2
        text_config = {
            ParameterName.string: subfigure_label,
            ParameterName.center: label_center,
            **SubfigureConfig.common_label_text_config
        }
        return text_config


def subfigure_label_formatter(subfigure_label, lower_case=True, brackets=True):
    if lower_case:
        subfigure_label = subfigure_label.lower()
    else:
        subfigure_label = subfigure_label.upper()
    if brackets:
        format_string = '({})'
    else:
        format_string = '{}'
    return format_string.format(subfigure_label)


class Subfigure(CompositeFigure):
    def __init__(
            self, subfigure_element_dict, bottom_left, size, subfigure_label: str, subfigure_title: str,
            subfigure_label_loc=SubfigureLabelLoc.upper_left,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        self.subfigure_label = subfigure_label
        self.subfigure_title = subfigure_title
        self.subfigure_label_loc = subfigure_label_loc
        display_subfigure_label = subfigure_label_formatter(subfigure_label)
        text_config = SubfigureConfig.label_text_generator(
            bottom_left, size, display_subfigure_label, subfigure_label_loc)
        element_type_name_dict = {
            subfigure_title: subfigure_element_dict,
            ParameterName.subfigure_label: {subfigure_label: TextBox(**text_config)}
        }
        super(Subfigure, self).__init__(
            element_type_name_dict=element_type_name_dict, bottom_left=bottom_left, size=size,
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment, name=f'Subfigure_{subfigure_label}', **kwargs)


class FigureConfig(object):
    # default_figure_size = (12, 6)        # with unit inches
    default_figure_size = (8.5, 11)     # with unit inches

    default_top_margin_ratio = 0.05
    default_side_margin_ratio = 0.02

    title_top_margin = 0.01
    title_left_margin = 0.03
    title_width = 0.12
    title_height = 0.04
    top_left_offset = Vector(title_left_margin, -title_top_margin)
    size_offset = Vector(title_width, -title_height)

    common_title_text_config = {
        ParameterName.width: title_width,
        ParameterName.height: title_height,
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.font_weight: FontWeight.bold,
        ParameterName.font_size: 18,
        ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
        ParameterName.horizontal_alignment: HorizontalAlignment.left,
        ParameterName.z_order: ZOrderConfig.default_subfigure_label_z_order,
    }

    @staticmethod
    def title_text_generator(height_to_width_ratio, figure_title: str):
        label_center = Vector(0, height_to_width_ratio) + FigureConfig.top_left_offset + FigureConfig.size_offset / 2
        text_config = {
            ParameterName.string: figure_title,
            ParameterName.center: label_center,
            **FigureConfig.common_title_text_config
        }
        return text_config


def calculate_subfigure_layout(
        combined_figure_layout_list, single_subfigure_layout_dict, subfigure_class_list,
        height_to_width_ratio, top_margin_ratio, side_margin_ratio):
    subfigure_label_class_dict = {
        subfigure_class.subfigure_label: subfigure_class
        for subfigure_class in subfigure_class_list
    }
    subfigure_obj_list = []
    total_height = height_to_width_ratio - top_margin_ratio
    total_width = 1 - 2 * side_margin_ratio
    total_size = Vector(total_width, total_height)
    current_top = total_height
    for row_height, row_layout in combined_figure_layout_list:
        current_height = row_height * total_height
        current_bottom = current_top - current_height
        current_left = side_margin_ratio
        for col_width, subfigure_label in row_layout:
            current_width = total_width * col_width
            subfigure_class = subfigure_label_class_dict[subfigure_label]
            subfigure_obj_list.append(subfigure_class(
                subfigure_bottom_left=Vector(current_left, current_bottom),
                subfigure_size=Vector(current_width, current_height)))
            current_left += current_width
        current_top = current_bottom
    for subfigure_label, ((subfigure_center_x, subfigure_center_y), subfigure_size) in \
            single_subfigure_layout_dict.items():
        subfigure_real_size = subfigure_size * total_size
        subfigure_real_bottom_left = (Vector(
            subfigure_center_x * total_width + side_margin_ratio,
            total_height - subfigure_center_y * total_height) - subfigure_real_size / 2)
        subfigure_class = subfigure_label_class_dict[subfigure_label]
        subfigure_obj_list.append(subfigure_class(
            subfigure_bottom_left=subfigure_real_bottom_left,
            subfigure_size=subfigure_real_size))
    return subfigure_obj_list


class Figure(CompositeFigure):
    figure_label = 'basic_figure'
    figure_output_direct = None
    figure_size = None
    top_margin_ratio = None
    side_margin_ratio = None

    def __init__(
            self, figure_name=None, subfigure_class_list=None, combined_subfigure_layout_list=None,
            single_subfigure_layout_dict=None, other_obj_list=None,
            figure_size=None, figure_title=None, dpi=None, figure_output_direct=None):
        if figure_size is not None:
            self.figure_size = initialize_vector_input(figure_size)
        elif self.figure_size is None:
            self.figure_size = FigureConfig.default_figure_size
        figure_size = self.figure_size
        if self.top_margin_ratio is None:
            self.top_margin_ratio = FigureConfig.default_top_margin_ratio
        if self.side_margin_ratio is None:
            self.side_margin_ratio = FigureConfig.default_side_margin_ratio
        self.dpi = dpi
        if figure_name is None:
            figure_name = self.figure_label
        self.figure_name = figure_name
        self.figure_title = figure_title
        height_to_width_ratio = figure_size[1] / figure_size[0]
        self.height_to_width_ratio = height_to_width_ratio
        bottom_left = Vector(0, 0)
        size = Vector(1, height_to_width_ratio)

        if subfigure_class_list is None:
            subfigure_class_list = []
        if combined_subfigure_layout_list is None:
            combined_subfigure_layout_list = []
        if single_subfigure_layout_dict is None:
            single_subfigure_layout_dict = {}
        subfigure_obj_list = calculate_subfigure_layout(
            combined_subfigure_layout_list, single_subfigure_layout_dict, subfigure_class_list,
            height_to_width_ratio, self.top_margin_ratio, self.side_margin_ratio)
        if other_obj_list is None:
            other_obj_list = []
        figure_element_dict = {
            ParameterName.subfigure:
                {subfigure_obj.subfigure_label: subfigure_obj for subfigure_obj in subfigure_obj_list},
            'Other obj': {obj.name: obj for obj in other_obj_list}
        }
        if figure_title is not None:
            text_config = FigureConfig.title_text_generator(height_to_width_ratio, figure_title)
            figure_element_dict[ParameterName.figure_title] = {figure_title: TextBox(**text_config)}
        if figure_output_direct is not None:
            self.figure_output_direct = figure_output_direct
        super().__init__(figure_element_dict, bottom_left, size, name=figure_name)

    def draw(self, fig=None, parent_ax=None, parent_transformation=None, output_svg=False, background=False):
        fig = plt.figure(figsize=self.figure_size, dpi=self.dpi)
        height_width_distortion = Vector(1, 1 / self.height_to_width_ratio)
        axis_bottom_left = self.bottom_left * height_width_distortion
        axis_size = self.size * height_width_distortion
        complete_axis = fig.add_axes([*axis_bottom_left, *axis_size])
        complete_axis.set_axis_off()
        figure_width = self.figure_size[0]
        complete_transformation = transforms.Affine2D(
            matrix=np.array([[figure_width, 0, 0], [0, figure_width, 0], [0, 0, 1]])) + fig.dpi_scale_trans
        super().draw(fig, complete_axis, complete_transformation)
        if self.figure_output_direct is None:
            raise ValueError('No figure output direct')
        elif output_svg:
            save_path = '{}/{}.svg'.format(self.figure_output_direct, self.figure_name)
            if background:
                parameter_dict = {}
            else:
                parameter_dict = {'transparent': True}
        else:
            save_path = '{}/{}.pdf'.format(self.figure_output_direct, self.figure_name)
            parameter_dict = {}
        fig.savefig(save_path, dpi=fig.dpi, **parameter_dict)


