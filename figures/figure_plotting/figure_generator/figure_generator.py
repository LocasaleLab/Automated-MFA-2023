from figures.figure_plotting.common.config import Keyword, Direct, Constant
from .rendering_functions import initialize_elements, draw_and_save_figure


def figure_generator_and_save(figure_name, raw_content_list):
    final_figure_obj = initialize_elements(figure_name, raw_content_list)
    figure_size = Constant.default_figure_size
    draw_and_save_figure(figure_name, figure_size, final_figure_obj)
