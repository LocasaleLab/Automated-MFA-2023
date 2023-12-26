from .optimization_diagram import OptimizationDiagram
from .data_acquisition_diagram import DataAcquisitionDiagram
from .optimum_distribution_comparison_diagram import OptimumDistributionComparisonDiagram
from .protocol_diagram import ProtocolDiagram
from .experiment_diagram import ExperimentDiagram
from .noisy_data_diagram import NoisyDataDiagram
from .flux_sloppiness_diagram import FluxSloppinessDiagram, MultipleFluxSloppinessDiagram
from .mid_comparison_table import AllExperimentalMIDBriefComparison


class ElementName(object):
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
    OptimizationDiagram = OptimizationDiagram
    DataAcquisitionDiagram = DataAcquisitionDiagram
    OptimumDistributionComparisonDiagram = OptimumDistributionComparisonDiagram
    ProtocolDiagram = ProtocolDiagram
    ExperimentDiagram = ExperimentDiagram
    NoisyDataDiagram = NoisyDataDiagram
    FluxSloppinessDiagram = FluxSloppinessDiagram
    MultipleFluxSloppinessDiagram = MultipleFluxSloppinessDiagram
    AllExperimentalMIDBriefComparison = AllExperimentalMIDBriefComparison


element_dict = {
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
