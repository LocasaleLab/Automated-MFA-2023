from .common.config import enum
from figure_plotting_package.main import draw_figure


class FigureName(enum.Enum):
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
    all_figures = 'all'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value.__eq__(other)

    @staticmethod
    def return_all():
        return [
            FigureName.figure_1, FigureName.figure_2, FigureName.figure_3, FigureName.figure_4, FigureName.figure_5,
            FigureName.figure_s1, FigureName.figure_s2, FigureName.figure_s3, FigureName.figure_s4,
            FigureName.figure_s5, FigureName.figure_s6,
        ]


def figure_content_loader(figure_name):
    if figure_name == FigureName.figure_1:
        from .figures.figure_1 import Figure1 as Figure
    elif figure_name == FigureName.figure_s1:
        from .figures.figure_s1 import FigureS1 as Figure
    elif figure_name == FigureName.figure_2:
        from .figures.figure_2 import Figure2 as Figure
    elif figure_name == FigureName.figure_s2:
        from .figures.figure_s2 import FigureS2 as Figure
    elif figure_name == FigureName.figure_3:
        from .figures.figure_3 import Figure3 as Figure
    elif figure_name == FigureName.figure_s3:
        from .figures.figure_s3 import FigureS3 as Figure
    elif figure_name == FigureName.figure_4:
        from .figures.figure_4 import Figure4 as Figure
    elif figure_name == FigureName.figure_s4:
        from .figures.figure_s4 import FigureS4 as Figure
    elif figure_name == FigureName.figure_5:
        from .figures.figure_5 import Figure5 as Figure
    elif figure_name == FigureName.figure_s5:
        from .figures.figure_s5 import FigureS5 as Figure
    elif figure_name == FigureName.figure_s6:
        from .figures.figure_s6 import FigureS6 as Figure
    else:
        try:
            from .figures.other_test_figures import test_figure_content_loader
        except ImportError:
            raise ValueError()
        else:
            Figure = test_figure_content_loader(figure_name)
    return Figure()


def figure_plotting_main(figure_name):
    def single_plot(single_figure_name):
        figure_obj = figure_content_loader(single_figure_name)
        draw_figure(figure_obj)

    if figure_name == FigureName.all_figures:
        all_figure_list = FigureName.return_all()
        for figure_name in all_figure_list:
            single_plot(figure_name)
    else:
        single_plot(figure_name)
