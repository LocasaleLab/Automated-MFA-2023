from .mid_diagram import MIDDiagram
from .network_diagram import (
    NetworkDiagram, FreeNetworkDiagram, FreeNetworkWithTextDiagram, NetworkDiagramConfig,
    construct_mixed_metabolite_obj)
from .object_diagrams.element_dict import (
    Mice, Human, FruitFly, CulturedCell, MiceBrain, Liver, Kidney, Heart, Muscle, Intestine,
    Adipose, OrganMouse, CircleVessel, BranchVessel)
from .carbon_backbone import CarbonBackbone
from .axis_diagram import AxisDiagram, AxisDiagramConfig, CrossAxisDiagram, bidirectional_arrow_config_constructor
from .simple_algorithm_diagram import SimpleAlgorithmDiagram, AlgorithmOutlineDiagram


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
    FreeNetworkWithTextDiagram = FreeNetworkWithTextDiagram
    SimpleAlgorithmDiagram = SimpleAlgorithmDiagram
    AlgorithmOutlineDiagram = AlgorithmOutlineDiagram
    construct_mixed_metabolite_obj = construct_mixed_metabolite_obj
    Mice = Mice
    Human = Human
    FruitFly = FruitFly
    MiceBrain = MiceBrain
    Liver = Liver
    Kidney = Kidney
    Heart = Heart
    Muscle = Muscle
    Intestine = Intestine
    Adipose = Adipose
    OrganMouse = OrganMouse
    CircleVessel = CircleVessel
    BranchVessel = BranchVessel
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
