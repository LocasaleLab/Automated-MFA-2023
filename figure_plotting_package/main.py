def draw_figure(figure_obj, output_svg=False, background=False):
    print(f'Drawing {figure_obj.figure_label}')
    figure_obj.draw(output_svg=output_svg, background=background)
