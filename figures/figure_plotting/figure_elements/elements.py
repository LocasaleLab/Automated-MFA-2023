from .basic_shape_elements.elements import element_dict as basic_shape_elements, ElementName as BasicElementName, \
    Elements as BasicElements
from .metabolic_network.complex_metabolic_network_figure import ElementName as MetabolicNetworkName, \
    element_dict as metabolic_network, Elements as MetabolicNetworkElements
from .data_figure.elements import element_dict as data_figure, ElementName as DataFigureName, \
    Elements as DataFigureElements
from .diagrams.elements import element_dict as diagram_elements, ElementName as DiagramName, \
    Elements as DiagramElements


class ElementName(BasicElementName, MetabolicNetworkName, DataFigureName, DiagramName):
    pass


class Elements(BasicElements, MetabolicNetworkElements, DataFigureElements, DiagramElements):
    BasicElements = BasicElements
    MetabolicNetworkElements = MetabolicNetworkElements
    DataFigureElements = DataFigureElements
    DiagramElements = DiagramElements


def merge_dict_with_conflict(*dict_list):
    final_dict = {}
    for current_dict in dict_list:
        for key, value in current_dict.items():
            if key in final_dict:
                raise ValueError('Key {} exists in previous dict with value {}\nNew value: {}'.format(
                    key, final_dict[key], value))
            final_dict[key] = value
    return final_dict


element_dict = merge_dict_with_conflict(basic_shape_elements, metabolic_network, data_figure, diagram_elements)

