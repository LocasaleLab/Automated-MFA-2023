from .basic_region import Region, move_and_scale_for_dict
from .composite_figure_and_axes import CompositeFigure, Figure, DataFigureAxes, Subfigure, transforms
from .shapes import BasicShape, \
    Circle, PathRectangle, RoundRectangle, Ellipse, Polygon, Capsule, Rectangle, \
    PathStep, PathOperation, PathShape, ellipse_arc_obj, Line, Brace
from .modified_text import TextBox, draw_text
from .arrow import ChevronArrow, Arrow, ArcChevronArrow, ArcArrow, ArcPathArrow, BentChevronArrow, BentArrow, \
    BrokenChevronArrow, BrokenArrow
from .legend import common_legend_generator


class ElementName(object):
    Region = 'Region'
    DataFigureAxes = 'DataFigureAxes'
    TextBox = 'TextBox'
    Circle = 'Circle'
    Rectangle = 'Rectangle'
    PathRectangle = 'PathRectangle'
    RoundRectangle = 'RoundRectangle'
    Ellipse = 'Ellipse'
    Polygon = 'Polygon'
    Line = 'Line'
    Brace = 'Brace'
    Arrow = 'Arrow'
    ChevronArrow = 'ChevronArrow'
    Capsule = 'Capsule'
    ArcChevronArrow = 'ArcChevronArrow'
    ArcArrow = 'ArcArrow'
    ArcPathArrow = 'ArcPathArrow'
    BentArrow = 'BentArrow'
    BentChevronArrow = 'BentChevronArrow'
    BrokenArrow = 'BrokenArrow'
    BrokenChevronArrow = 'BrokenChevronArrow'
    BasicShape = 'BasicShape'
    CompositeFigure = 'CompositeFigure'
    Subfigure = 'Subfigure'
    Figure = 'Figure'


class Elements(object):
    Region = Region
    PathShape = PathShape
    PathStep = PathStep
    PathOperation = PathOperation
    DataFigureAxes = DataFigureAxes
    TextBox = TextBox
    Circle = Circle
    Rectangle = Rectangle
    PathRectangle = PathRectangle
    RoundRectangle = RoundRectangle
    Ellipse = Ellipse
    Polygon = Polygon
    Line = Line
    Brace = Brace
    Arrow = Arrow
    ChevronArrow = ChevronArrow
    Capsule = Capsule
    ArcChevronArrow = ArcChevronArrow
    ArcArrow = ArcArrow
    ArcPathArrow = ArcPathArrow
    BentArrow = BentArrow
    BentChevronArrow = BentChevronArrow
    BrokenArrow = BrokenArrow
    BrokenChevronArrow = BrokenChevronArrow
    BasicShape = BasicShape
    CompositeFigure = CompositeFigure
    Subfigure = Subfigure
    Figure = Figure


element_dict = {
    ElementName.Region: Region,
    ElementName.DataFigureAxes: DataFigureAxes,
    ElementName.BasicShape: BasicShape,
    ElementName.Circle: Circle,
    ElementName.Rectangle: Rectangle,
    ElementName.PathRectangle: PathRectangle,
    ElementName.RoundRectangle: RoundRectangle,
    ElementName.Ellipse: Ellipse,
    ElementName.Polygon: Polygon,
    ElementName.Line: Line,
    ElementName.Brace: Brace,
    ElementName.ChevronArrow: ChevronArrow,
    ElementName.Capsule: Capsule,
    ElementName.TextBox: TextBox,
    ElementName.Arrow: Arrow,
    ElementName.ArcChevronArrow: ArcChevronArrow,
    ElementName.ArcArrow: ArcArrow,
    ElementName.ArcPathArrow: ArcPathArrow,
    ElementName.BentArrow: BentArrow,
    ElementName.BentChevronArrow: BentChevronArrow,
    ElementName.BrokenArrow: BrokenArrow,
    ElementName.BrokenChevronArrow: BrokenChevronArrow,
    ElementName.CompositeFigure: CompositeFigure,
    ElementName.Subfigure: Subfigure,
    ElementName.Figure: Figure
}
