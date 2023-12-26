from .diagram_elements.mid_diagram import MIDDiagram
from .diagram_elements.network_diagram import NetworkDiagram
from .diagram_elements.object_diagrams.element_dict import Mice, Human, CulturedCell
from .diagram_elements.carbon_backbone import CarbonBackbone
from .diagram_elements.axis_diagrams.element_dict import OptimumDistributionDiagram, OptimumDistributionDiagramConfig, \
    InitialDistributionDiagram, LossDistributionDiagram, HorizontalLossDistributionDiagram, AverageDiagram, \
    HorizontalComparisonDiagram, HeatmapDiagram, RandomOptimizedDistanceDiagram

from .diagrams.optimization_diagram import OptimizationDiagram
from .diagrams.data_acquisition_diagram import DataAcquisitionDiagram
from .diagrams.optimum_distribution_comparison_diagram import OptimumDistributionComparisonDiagram
from .diagrams.protocol_diagram import ProtocolDiagram
from .diagrams.experiment_diagram import ExperimentDiagram
from .diagrams.noisy_data_diagram import NoisyDataDiagram
from .diagrams.flux_sloppiness_diagram import FluxSloppinessDiagram, MultipleFluxSloppinessDiagram
from .diagrams.mid_comparison_table import AllExperimentalMIDBriefComparison
from .diagrams.data_sensitivity_generator_diagram import DataSensitivityGeneratorDiagram


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

    OptimizationDiagram = 'OptimizationDiagram'
    DataAcquisitionDiagram = 'DataAcquisitionDiagram'
    OptimumDistributionComparisonDiagram = 'OptimumDistributionComparisonDiagram'
    ProtocolDiagram = 'ProtocolDiagram'
    ExperimentDiagram = 'ExperimentDiagram'
    NoisyDataDiagram = 'NoisyDataDiagram'
    FluxSloppinessDiagram = 'FluxSloppinessDiagram'
    MultipleFluxSloppinessDiagram = 'MultipleFluxSloppinessDiagram'
    AllExperimentalMIDBriefComparison = 'AllExperimentalMIDBriefComparison'


class Elements(object):
    MIDDiagram = MIDDiagram
    NetworkDiagram = NetworkDiagram
    Mice = Mice
    Human = Human
    CulturedCell = CulturedCell
    CarbonBackbone = CarbonBackbone
    InitialDistributionDiagram = InitialDistributionDiagram
    OptimumDistributionDiagram = OptimumDistributionDiagram
    LossDistributionDiagram = LossDistributionDiagram
    AverageDiagram = AverageDiagram
    RandomOptimizedDistanceDiagram = RandomOptimizedDistanceDiagram
    HorizontalComparisonDiagram = HorizontalComparisonDiagram
    HorizontalLossDistributionDiagram = HorizontalLossDistributionDiagram
    HeatmapDiagram = HeatmapDiagram

    OptimizationDiagram = OptimizationDiagram
    DataAcquisitionDiagram = DataAcquisitionDiagram
    OptimumDistributionComparisonDiagram = OptimumDistributionComparisonDiagram
    ProtocolDiagram = ProtocolDiagram
    ExperimentDiagram = ExperimentDiagram
    NoisyDataDiagram = NoisyDataDiagram
    FluxSloppinessDiagram = FluxSloppinessDiagram
    MultipleFluxSloppinessDiagram = MultipleFluxSloppinessDiagram
    AllExperimentalMIDBriefComparison = AllExperimentalMIDBriefComparison
    DataSensitivityGeneratorDiagram = DataSensitivityGeneratorDiagram


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

    ElementName.OptimizationDiagram: OptimizationDiagram,
    ElementName.DataAcquisitionDiagram: DataAcquisitionDiagram,
    ElementName.OptimumDistributionComparisonDiagram: OptimumDistributionComparisonDiagram,
    ElementName.ProtocolDiagram: ProtocolDiagram,
    ElementName.ExperimentDiagram: ExperimentDiagram,
    ElementName.NoisyDataDiagram: NoisyDataDiagram,
    ElementName.FluxSloppinessDiagram: FluxSloppinessDiagram,
    ElementName.MultipleFluxSloppinessDiagram: MultipleFluxSloppinessDiagram,
    ElementName.AllExperimentalMIDBriefComparison: AllExperimentalMIDBriefComparison,
}
