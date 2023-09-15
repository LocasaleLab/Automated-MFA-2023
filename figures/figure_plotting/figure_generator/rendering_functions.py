from ..common.config import Keyword, figure_path_generator, figure_data_path_generator
from ..common.third_party_packages import plt
from ..figure_elements.element_dict import ElementName, element_dict


def initialize_elements(figure_name, raw_content_list):
    def initialize_content_dict(raw_content_dict):
        content_type_str = raw_content_dict[Keyword.type]
        if content_type_str not in element_dict:
            raise TypeError()
        else:
            name = raw_content_dict[Keyword.name]
            parameter_dict = raw_content_dict[Keyword.parameters]
            if content_type_str == ElementName.Subplot:
                new_content_list = []
                for child_content_dict in raw_content_dict[Keyword.content]:
                    new_content_list.append(initialize_content_dict(child_content_dict))
                final_obj = element_dict[ElementName.Subplot](**parameter_dict, content=new_content_list, name=name)
            elif content_type_str == ElementName.DataFigure:
                # TODO: add data figure
                final_obj = None
            else:
                final_obj = element_dict[content_type_str](**parameter_dict, name=name)
        return final_obj

    complete_content_list = []
    for content_dict in raw_content_list:
        complete_content_list.append(initialize_content_dict(content_dict))
    final_figure_obj = element_dict[ElementName.Subplot]((0, 0), (1, 1), complete_content_list, name=figure_name)
    return final_figure_obj


def draw_and_save_figure(figure_name, figure_size, final_figure_obj):
    fig = plt.figure(figsize=figure_size)
    final_figure_obj.draw(fig=fig)
    fig.savefig(figure_path_generator(figure_name), dpi=fig.dpi)

