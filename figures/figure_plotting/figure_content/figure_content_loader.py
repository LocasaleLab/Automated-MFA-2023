from figures.figure_plotting.common.built_in_packages import FigureName


def figure_content_loader(figure_name):
    if figure_name == FigureName.test:
        # from .test import content as raw_content_list
        from .figure_test import FigureTest as Figure
    elif figure_name == FigureName.simple_test:
        # from .simple_test import content as raw_content_list
        from .figure_test import FigureSimpleTest as Figure
    elif figure_name == FigureName.figure_1:
        from .figure_1 import Figure1 as Figure
    elif figure_name == FigureName.figure_s1:
        from .figure_s1 import FigureS1 as Figure
    elif figure_name == FigureName.figure_2:
        from .figure_2 import Figure2 as Figure
    elif figure_name == FigureName.figure_s2:
        from .figure_s2 import FigureS2 as Figure
    elif figure_name == FigureName.figure_3:
        from .figure_3 import Figure3 as Figure
    elif figure_name == FigureName.figure_s3:
        from .figure_s3 import FigureS3 as Figure
    elif figure_name == FigureName.figure_4:
        from .figure_4 import Figure4 as Figure
    elif figure_name == FigureName.figure_s4:
        from .figure_s4 import FigureS4 as Figure
    elif figure_name == FigureName.figure_5:
        from .figure_5 import Figure5 as Figure
    elif figure_name == FigureName.figure_s5:
        from .figure_s5 import FigureS5 as Figure
    elif figure_name == FigureName.figure_s6:
        from .figure_s6 import FigureS6 as Figure
    elif figure_name == FigureName.figure_s7:
        from .figure_s7 import FigureS7 as Figure
    else:
        raise ValueError()
    # return raw_content_list
    return Figure()

