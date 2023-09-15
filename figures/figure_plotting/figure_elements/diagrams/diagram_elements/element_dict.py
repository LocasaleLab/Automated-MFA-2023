from .mid_diagram import MIDDiagram
from .network_diagram import NetworkDiagram
from .object_diagrams.element_dict import Mice, Human, CulturedCell
from .carbon_backbone import CarbonBackbone
from .axis_diagrams.element_dict import OptimumDistributionDiagram, OptimumDistributionDiagramConfig, \
    InitialDistributionDiagram, LossDistributionDiagram, HorizontalLossDistributionDiagram, AverageDiagram, \
    HorizontalComparisonDiagram, HeatmapDiagram, RandomOptimizedDistanceDiagram


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


element_dict = {
    ElementName.MIDDiagram: MIDDiagram,
    ElementName.NetworkDiagram: NetworkDiagram,
    ElementName.Mice: Mice,
    ElementName.Human: Human,
    ElementName.CulturedCell: CulturedCell,
    ElementName.CarbonBackbone: CarbonBackbone,
    ElementName.InitialDistributionDiagram: InitialDistributionDiagram,
    ElementName.OptimumDistributionDiagram: OptimumDistributionDiagram,
    ElementName.LossDistributionDiagram: LossDistributionDiagram,
    ElementName.AverageDiagram: AverageDiagram,
    ElementName.RandomOptimizedDistanceDiagram: RandomOptimizedDistanceDiagram,
    ElementName.HorizontalComparisonDiagram: HorizontalComparisonDiagram,
    ElementName.HorizontalLossDistributionDiagram: HorizontalLossDistributionDiagram,
    ElementName.HeatmapDiagram: HeatmapDiagram,
}

