from .config import GeneralElements
from ..figure_elements.diagrams import (
    OptimizationDiagram,
    DataAcquisitionDiagram,
    OptimumDistributionComparisonDiagram,
    ProtocolDiagram,
    ExperimentDiagram,
    NoisyDataDiagram,
    FluxSloppinessDiagram,
    MultipleFluxSloppinessDiagram,
    AllExperimentalMIDBriefComparison,
    DataSensitivityGeneratorDiagram,
)
from ..figure_elements.data_figure import (
    LossDistanceGridBoxDataFigure
)
from ..figure_elements.complex_figure import (
    MIDComparisonGridBarWithLegendDataFigure,
    OptimizedAllFluxComparisonBarDataFigure,
    TimeLossStack,
    RandomOptimizedFluxLayout,
    RandomOptimizedLossDistanceComparison,
    RandomOptimizedLossDistanceWithDiagramComparison,
    LossDistanceGridFigure,
    SingleLossOrDistanceFigure,
    LossDistanceSinglePairFigure,
    DistanceVariationScatterFigure,
    FluxComparisonScatterWithTitle,
    FluxComparisonViolinBoxWithTitleLegend,
    MeanSTDCombinedHeatmap,
    AllFluxComparisonBarFigure,
    EuclideanHeatmapScatter,
    SensitivityAllFluxHeatmap,
    ProtocolAllFluxHeatmap,
    ExperimentalOptimizationLossComparison,
)
from ..figure_elements.metabolic_network.sensitivity_diagram import SensitivityDiagram
from ..figure_elements.metabolic_network.loss_of_averaged_solutions_diagram import LossOfAveragedSolutionsDiagram


class Elements(GeneralElements):
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

    LossDistanceGridBoxDataFigure = LossDistanceGridBoxDataFigure

    MIDComparisonGridBarWithLegendDataFigure = MIDComparisonGridBarWithLegendDataFigure
    OptimizedAllFluxComparisonBarDataFigure = OptimizedAllFluxComparisonBarDataFigure
    TimeLossStack = TimeLossStack
    RandomOptimizedFluxLayout = RandomOptimizedFluxLayout
    RandomOptimizedLossDistanceComparison = RandomOptimizedLossDistanceComparison
    RandomOptimizedLossDistanceWithDiagramComparison = RandomOptimizedLossDistanceWithDiagramComparison
    LossDistanceGridFigure = LossDistanceGridFigure
    SingleLossOrDistanceFigure = SingleLossOrDistanceFigure
    LossDistanceSinglePairFigure = LossDistanceSinglePairFigure
    DistanceVariationScatterFigure = DistanceVariationScatterFigure
    FluxComparisonScatterWithTitle = FluxComparisonScatterWithTitle
    FluxComparisonViolinBoxWithTitleLegend = FluxComparisonViolinBoxWithTitleLegend
    MeanSTDCombinedHeatmap = MeanSTDCombinedHeatmap
    AllFluxComparisonBarFigure = AllFluxComparisonBarFigure
    EuclideanHeatmapScatter = EuclideanHeatmapScatter
    SensitivityAllFluxHeatmap = SensitivityAllFluxHeatmap
    ProtocolAllFluxHeatmap = ProtocolAllFluxHeatmap
    ExperimentalOptimizationLossComparison = ExperimentalOptimizationLossComparison

    SensitivityDiagram = SensitivityDiagram
    LossOfAveragedSolutionsDiagram = LossOfAveragedSolutionsDiagram
