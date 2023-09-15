from ...common.config import ParameterName as GeneralParameterName, DataName
from ...common.third_party_packages import np
from ...common.built_in_packages import warnings
from ...common.color import ColorConfig, TextConfig, ZOrderConfig
from ...common.classes import HorizontalAlignment, VerticalAlignment, Vector, LineStyle, JoinStyle, FontWeight, \
    FontStyle
from ...common.common_figure_materials import CommonElementConfig, CommonFigureString, CommonFigureMaterials
from ..basic_shape_elements.element_dict import common_legend_generator


class Keyword(object):
    orange = 'orange'
    blue = 'blue'
    gray = 'gray'

    normal = 'normal'
    cycle = 'cycle'
    branch = 'branch'


class ParameterName(GeneralParameterName):
    mid_diagram_suffix = 'mid_diagram'
    common = 'common'

    data_vector = 'data_vector'
    carbon_num = 'carbon_num'
    color_name = 'color_name'

    bound_box = 'bound_box'
    bar = 'bar'
    text = 'text'
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

