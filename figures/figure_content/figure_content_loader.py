from .common.config import enum
from figure_plotting_package.main import draw_figure

normal_figure = 'normal'
short_figure = 'short'

# figure_type = normal_figure
figure_type = short_figure


class BaseFigureName(enum.Enum):
    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value.__eq__(other)

    @staticmethod
    def return_all():
        pass


def test_figure_content_loader(figure_direct, figure_name):
    import importlib
    current_file_name = f'figure_{figure_name}'
    current_direct = __name__[:__name__.rindex('.')]
    current_file_path = f'{current_direct}.{figure_direct}.{current_file_name}'
    imported_lib = importlib.import_module(current_file_path)
    Figure = imported_lib.Figure
    return Figure


class NormalFigureName(BaseFigureName):
    figure_1 = '1'
    figure_2 = '2'
    figure_3 = '3'
    figure_4 = '4'
    figure_5 = '5'
    figure_s1 = 's1'
    figure_s2 = 's2'
    figure_s3 = 's3'
    figure_s4 = 's4'
    figure_s5 = 's5'
    figure_s6 = 's6'
    figure_schematic_flux_name = 'schematic_flux_name'
    loss_of_averaged_solutions = 'loss_of_averaged_solutions'
    all_figures = 'all'

    @staticmethod
    def return_all():
        return [
            NormalFigureName.figure_1,
            NormalFigureName.figure_2,
            NormalFigureName.figure_3,
            NormalFigureName.figure_4,
            NormalFigureName.figure_5,
            NormalFigureName.figure_s1,
            NormalFigureName.figure_s2,
            NormalFigureName.figure_s3,
            NormalFigureName.figure_s4,
            NormalFigureName.figure_s5,
            NormalFigureName.figure_s6,
        ]


class ShortFigureName(BaseFigureName):
    figure_1 = '1'
    figure_s1 = 's1'
    figure_s2 = 's2'
    figure_s3 = 's3'
    figure_s4 = 's4'
    figure_s5 = 's5'
    figure_s6 = 's6'
    figure_s7 = 's7'
    figure_s8 = 's8'
    all_figures = 'all'

    @staticmethod
    def return_all():
        return [
            ShortFigureName.figure_1,
            ShortFigureName.figure_s1,
            ShortFigureName.figure_s2,
            ShortFigureName.figure_s3,
            ShortFigureName.figure_s4,
            ShortFigureName.figure_s5,
            ShortFigureName.figure_s6,
            ShortFigureName.figure_s7,
        ]


if figure_type == normal_figure:
    FigureName = NormalFigureName
elif figure_type == short_figure:
    FigureName = ShortFigureName


def normal_figure_content_loader(figure_name):
    if figure_name == NormalFigureName.figure_1:
        from .figures.figure_1 import Figure1 as Figure
    elif figure_name == NormalFigureName.figure_s1:
        from .figures.figure_s1 import FigureS1 as Figure
    elif figure_name == NormalFigureName.figure_2:
        from .figures.figure_2 import Figure2 as Figure
    elif figure_name == NormalFigureName.figure_s2:
        from .figures.figure_s2 import FigureS2 as Figure
    elif figure_name == NormalFigureName.figure_3:
        from .figures.figure_3 import Figure3 as Figure
    elif figure_name == NormalFigureName.figure_s3:
        from .figures.figure_s3 import FigureS3 as Figure
    elif figure_name == NormalFigureName.figure_4:
        from .figures.figure_4 import Figure4 as Figure
    elif figure_name == NormalFigureName.figure_s4:
        from .figures.figure_s4 import FigureS4 as Figure
    elif figure_name == NormalFigureName.figure_5:
        from .figures.figure_5 import Figure5 as Figure
    elif figure_name == NormalFigureName.figure_s5:
        from .figures.figure_s5 import FigureS5 as Figure
    elif figure_name == NormalFigureName.figure_s6:
        from .figures.figure_s6 import FigureS6 as Figure
    elif figure_name == NormalFigureName.figure_schematic_flux_name:
        from .figures.figure_schematic_flux_name import Figure
    elif figure_name == NormalFigureName.loss_of_averaged_solutions:
        from .figures.figure_loss_of_averaged_solutions import Figure
    else:
        Figure = test_figure_content_loader('figures', figure_name)
    return Figure()


def short_figure_content_loader(figure_name):
    if figure_name == ShortFigureName.figure_1:
        from .short_figures.figure_1 import Figure1 as Figure
    elif figure_name == ShortFigureName.figure_s1:
        from .short_figures.figure_s1 import FigureS1 as Figure
    elif figure_name == ShortFigureName.figure_s2:
        from .short_figures.figure_s2 import FigureS2 as Figure
    elif figure_name == ShortFigureName.figure_s3:
        from .short_figures.figure_s3 import FigureS3 as Figure
    elif figure_name == ShortFigureName.figure_s4:
        from .short_figures.figure_s4 import FigureS4 as Figure
    elif figure_name == ShortFigureName.figure_s5:
        from .short_figures.figure_s5 import FigureS5 as Figure
    elif figure_name == ShortFigureName.figure_s6:
        from .short_figures.figure_s6 import FigureS6 as Figure
    elif figure_name == ShortFigureName.figure_s7:
        from .short_figures.figure_s7 import FigureS7 as Figure
    else:
        Figure = test_figure_content_loader('short_figures', figure_name)
    return Figure()


def figure_plotting_main(figure_name, output_svg=False):
    def single_plot(single_figure_name):
        if figure_type == normal_figure:
            figure_content_loader = normal_figure_content_loader
        elif figure_type == short_figure:
            figure_content_loader = short_figure_content_loader
        else:
            raise ValueError()
        figure_obj = figure_content_loader(single_figure_name)
        draw_figure(figure_obj, output_svg)

    if figure_name == NormalFigureName.all_figures:
        all_figure_list = NormalFigureName.return_all()
        for figure_name in all_figure_list:
            single_plot(figure_name)
    else:
        single_plot(figure_name)
