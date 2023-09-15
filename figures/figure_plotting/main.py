from .figure_content.figure_content_loader import figure_content_loader


def figure_plotting_main(figure_name):
    print(figure_name)
    figure_obj = figure_content_loader(figure_name)
    figure_obj.draw()
