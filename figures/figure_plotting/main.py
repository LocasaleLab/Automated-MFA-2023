from .figure_content.figure_content_loader import figure_content_loader, FigureName


def figure_plotting_main(figure_name):
    def single_plot(single_figure_name):
        print(single_figure_name)
        figure_obj = figure_content_loader(single_figure_name)
        figure_obj.draw()

    if figure_name == FigureName.all_figures:
        all_figure_list = FigureName.return_all()
        for figure_name in all_figure_list:
            single_plot(figure_name)
    else:
        single_plot(figure_name)
