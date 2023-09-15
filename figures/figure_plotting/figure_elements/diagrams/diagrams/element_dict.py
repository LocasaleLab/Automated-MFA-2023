from .optimization_diagram import OptimizationDiagram
from .data_acquisition_diagram import DataAcquisitionDiagram
from .optimum_distribution_comparison_diagram import OptimumDistributionComparisonDiagram
from .protocol_diagram import ProtocolDiagram
from .experiment_diagram import ExperimentDiagram
from .noisy_data_diagram import NoisyDataDiagram


class ElementName(object):
    OptimizationDiagram = 'OptimizationDiagram'
    DataAcquisitionDiagram = 'DataAcquisitionDiagram'
    OptimumDistributionComparisonDiagram = 'OptimumDistributionComparisonDiagram'
    ProtocolDiagram = 'ProtocolDiagram'
    ExperimentDiagram = 'ExperimentDiagram'
    NoisyDataDiagram = 'NoisyDataDiagram'


element_dict = {
    ElementName.OptimizationDiagram: OptimizationDiagram,
    ElementName.DataAcquisitionDiagram: DataAcquisitionDiagram,
    ElementName.OptimumDistributionComparisonDiagram: OptimumDistributionComparisonDiagram,
    ElementName.ProtocolDiagram: ProtocolDiagram,
    ElementName.ExperimentDiagram: ExperimentDiagram,
    ElementName.NoisyDataDiagram: NoisyDataDiagram,
}
