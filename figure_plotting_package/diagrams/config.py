from ..common.config import ParameterName as GeneralParameterName
from ..common.third_party_packages import np
from ..common.built_in_packages import warnings
from ..common.classes import Vector, LineStyle, JoinStyle, VerticalAlignment, HorizontalAlignment, FontWeight
from ..common.color import ZOrderConfig, ColorConfig, TextConfig
from ..common.common_functions import default_parameter_extract, basic_shape_parameter_set, load_required_parameter, \
    convert_theta_to_coordinate, unit_decorator, cos_sin

from ..basic_shape_elements import ElementName, Arrow, ArcArrow, CompositeFigure, Circle, TextBox, \
    Rectangle, RoundRectangle, PathStep, PathOperation, PathShape, Ellipse, ellipse_arc_obj, Line, Brace


class ParameterName(GeneralParameterName):
    mid_diagram_suffix = 'mid_diagram'
    common = 'common'

    color_name = 'color_name'

    bound_box = 'bound_box'
    cross_axis = 'cross_axis'
    bar = 'bar'
    chevron_arrow = 'chevron_arrow'
    constructed_obj = 'constructed_obj'
    metabolite = 'metabolite'
    reaction = 'reaction'
    axis_content = 'axis_content'

    mouse = 'mouse'

    human = 'human'
    dish_outline = 'dish_outline'
    media = 'media'
    cell = 'cell'

    optimum_distribution_diagram = 'optimum_distribution_diagram'

    orange = 'orange'
    blue = 'blue'
    gray = 'gray'

    cycle = 'cycle'
    branch = 'branch'


arrow_dict = {
    ElementName.Arrow: Arrow,
    ElementName.ArcArrow: ArcArrow,
}

complete_arrow_parameter_set_dict = {
    ParameterName.common: {
        ParameterName.head_width,
        ParameterName.stem_width,
        ParameterName.head_len_width_ratio,
        ParameterName.tail_arrow,
        ParameterName.head_arrow,
        ParameterName.gap_line_pair_list,
        ParameterName.dash_solid_empty_width,
        ParameterName.branch_list,
    },
    ElementName.Arrow: {
        ParameterName.tail,
        ParameterName.head,
    },
    ElementName.ArcArrow: {
        ParameterName.center,
        ParameterName.radius,
        ParameterName.theta_head,
        ParameterName.theta_tail,
    }
}

common_text_config_dict = {
    ParameterName.font: TextConfig.main_text_font,
    ParameterName.horizontal_alignment: HorizontalAlignment.center,
    ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
    ParameterName.z_order: ZOrderConfig.default_text_z_order,
}
