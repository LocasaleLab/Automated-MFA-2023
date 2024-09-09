from .mid_diagram import MIDDiagram
from .network_diagram import NetworkDiagram, FreeNetworkDiagram, NetworkDiagramConfig, construct_mixed_metabolite_obj
from .object_diagrams.element_dict import Mice, Human, CulturedCell
from .carbon_backbone import CarbonBackbone
from .axis_diagram import AxisDiagram, AxisDiagramConfig, CrossAxisDiagram, bidirectional_arrow_config_constructor


class ElementName(object):
    MIDDiagram = 'MIDDiagram'
    NetworkDiagram = 'NetworkDiagram'
    Mice = 'Mice'
    Human = 'Human'
    CulturedCell = 'CulturedCell'
    CarbonBackbone = 'CarbonBackbone'
    InitialDistributionDiagram = 'InitialDistributionDiagram'
    OptimumDistributionDiagram = 'OptimumDistributionDiagram'
    LossDistributionDiagram = 'LossDistributionDiagram'
    AverageDiagram = 'AverageDiagram'
    RandomOptimizedDistanceDiagram = 'RandomOptimizedDistanceDiagram'
    HorizontalComparisonDiagram = 'HorizontalComparisonDiagram'
    HorizontalLossDistributionDiagram = 'HorizontalLossDistributionDiagram'
    HeatmapDiagram = 'HeatmapDiagram'


class Elements(object):
    MIDDiagram = MIDDiagram
    NetworkDiagram = NetworkDiagram
    NetworkDiagramConfig = NetworkDiagramConfig
    FreeNetworkDiagram = FreeNetworkDiagram
    construct_mixed_metabolite_obj = construct_mixed_metabolite_obj
    Mice = Mice
    Human = Human
    CulturedCell = CulturedCell
    CarbonBackbone = CarbonBackbone
    AxisDiagram = AxisDiagram
    AxisDiagramConfig = AxisDiagramConfig
    CrossAxisDiagram = CrossAxisDiagram
    bidirectional_arrow_config_constructor = bidirectional_arrow_config_constructor


element_dict = {
    ElementName.MIDDiagram: MIDDiagram,
    ElementName.NetworkDiagram: NetworkDiagram,
    ElementName.Mice: Mice,
    ElementName.Human: Human,
    ElementName.CulturedCell: CulturedCell,
    ElementName.CarbonBackbone: CarbonBackbone,
}
