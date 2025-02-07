from .metabolic_network_elements import MetaboliteElement, ReactionElement, SubnetworkElement
from .layout_generator_functions.common_functions import (
    arrange_text_by_row, add_straight_reaction_between_metabolites, cycle_layout,
    calculate_reaction_between_adjacent_metabolites)
from .metabolic_network import set_and_convert_network_elements, MetabolicNetworkLegend, LegendConfig
from .metabolic_network_contents.content_list import Metabolite, Reaction, Subnetwork, assign_value_to_network
from .complex_metabolic_network_figure import MetabolicNetwork, MetabolicNetworkWithLegend, \
    ExchangeMetabolicNetworkWithTitle, QuadMetabolicNetworkComparison, NormalAndExchangeTwinNetwork, \
    NetworkMFAResultComparison, NormalAndExchangeNetworkMFAResultComparison
from .config import MetaboliteConfig, ReactionConfig, SubnetworkConfig, TransparencyGenerator, flux_value_mapper_dict


class ElementName(object):
    MetaboliteNode = 'MetaboliteNode'
    Reaction = 'Reaction'
    Subnetwork = 'Subnetwork'
    MetabolicNetwork = 'MetabolicNetwork'
    MetabolicNetworkWithLegend = 'MetabolicNetworkWithLegend'
    ExchangeMetabolicNetworkWithTitle = 'ExchangeMetabolicNetworkWithTitle'
    QuadMetabolicNetworkComparison = 'QuadMetabolicNetworkComparison'
    NormalAndExchangeTwinNetwork = 'NormalAndExchangeTwinNetwork'
    NetworkMFAResultComparison = 'ExchangeNetworkMFAResultComparison'
    NormalAndExchangeNetworkMFAResultComparison = 'NormalAndExchangeNetworkMFAResultComparison'


class Elements(object):
    MetaboliteConfig = MetaboliteConfig
    ReactionConfig = ReactionConfig
    SubnetworkConfig = SubnetworkConfig

    MetaboliteList = Metabolite
    ReactionList = Reaction
    SubnetworkList = Subnetwork

    Metabolite = MetaboliteElement
    Reaction = ReactionElement
    Subnetwork = SubnetworkElement
    MetabolicNetwork = MetabolicNetwork
    TransparencyGenerator = TransparencyGenerator
    MetabolicNetworkLegend = MetabolicNetworkLegend
    LegendConfig = LegendConfig
    MetabolicNetworkWithLegend = MetabolicNetworkWithLegend
    ExchangeMetabolicNetworkWithTitle = ExchangeMetabolicNetworkWithTitle
    QuadMetabolicNetworkComparison = QuadMetabolicNetworkComparison
    NormalAndExchangeTwinNetwork = NormalAndExchangeTwinNetwork
    NetworkMFAResultComparison = NetworkMFAResultComparison
    NormalAndExchangeNetworkMFAResultComparison = NormalAndExchangeNetworkMFAResultComparison

    arrange_text_by_row = arrange_text_by_row
    add_straight_reaction_between_metabolites = add_straight_reaction_between_metabolites
    cycle_layout = cycle_layout
    calculate_reaction_between_adjacent_metabolites = calculate_reaction_between_adjacent_metabolites
    set_and_convert_network_elements = set_and_convert_network_elements
    assign_value_to_network = assign_value_to_network
    flux_value_mapper_dict = flux_value_mapper_dict


element_dict = {
    ElementName.MetaboliteNode: MetaboliteElement,
    ElementName.Reaction: ReactionElement,
    ElementName.Subnetwork: SubnetworkElement,
    ElementName.MetabolicNetwork: MetabolicNetwork,
    ElementName.MetabolicNetworkWithLegend: MetabolicNetworkWithLegend,
    ElementName.ExchangeMetabolicNetworkWithTitle: ExchangeMetabolicNetworkWithTitle,
    ElementName.QuadMetabolicNetworkComparison: QuadMetabolicNetworkComparison,
    ElementName.NormalAndExchangeTwinNetwork: NormalAndExchangeTwinNetwork,
    ElementName.NormalAndExchangeNetworkMFAResultComparison: NormalAndExchangeNetworkMFAResultComparison,
    ElementName.NetworkMFAResultComparison: NetworkMFAResultComparison,
}
