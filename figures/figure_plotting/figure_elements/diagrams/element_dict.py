from .diagram_elements.element_dict import element_dict as diagram_elements, ElementName as DiagramElementName
from .diagrams.element_dict import element_dict as diagrams, ElementName as DiagramName


class ElementName(DiagramElementName, DiagramName):
    pass


def merge_dict_with_conflict(*dict_list):
    final_dict = {}
    for current_dict in dict_list:
        for key, value in current_dict.items():
            if key in final_dict:
                raise ValueError('Key {} exists in previous dict with value {}\nNew value: {}'.format(
                    key, final_dict[key], value))
            final_dict[key] = value
    return final_dict


element_dict = merge_dict_with_conflict(diagrams, diagram_elements)
