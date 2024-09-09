from .data_figure import DataFigure
from .heatmap_data_figure import HeatmapConfig, ColorBarDataFigure, BasicHeatmapDataFigure
# from .violin_box_scatter_mix_data_figure import LossDistanceGridBoxScatterMixDataFigure
from .scatter_data_figure import BasicScatterDataFigure
from .bar_data_figure import BasicBarDataFigure, BasicMIDComparisonGridBarDataFigure, \
    BasicFluxErrorBarDataFigure, BasicSingleBarDataFigure
from .violin_box_data_figure import BasicViolinBoxDataFigure
from .histogram_data_figure import BasicHistogramDataFigure


class ElementName(object):
    DataFigure = 'DataFigure'
    HeatmapDataFigure = 'BasicHeatmapDataFigure'
    GridScatterDataFigure = 'GridScatterDataFigure'
    MIDComparisonGridBarDataFigure = 'MIDComparisonGridBarDataFigure'
    MIDComparisonGridBarWithLegendDataFigure = 'MIDComparisonGridBarWithLegendDataFigure'
    OptimizedAllFluxComparisonBarDataFigure = 'OptimizedAllFluxComparisonBarDataFigure'
    TimeLossGridBoxDataFigure = 'TimeLossGridBoxDataFigure'
    LossDistanceGridBoxDataFigure = 'LossDistanceGridBoxDataFigure'
    FluxComparisonViolinBoxDataFigure = 'FluxComparisonViolinBoxDataFigure'
    FluxComparisonScatterDataFigure = 'FluxComparisonScatterDataFigure'
    TimeLossHistogramDataFigure = 'TimeLossHistogramDataFigure'
    TimeLossStack = 'TimeLossStack'
    RandomOptimizedFluxLayout = 'RandomOptimizedFluxLayout'
    RandomOptimizedLossDistanceComparison = 'RandomOptimizedLossDistanceComparison'
    RandomOptimizedLossDistanceWithDiagramComparison = 'RandomOptimizedLossDistanceWithDiagramComparison'
    LossDistanceGridFigure = 'LossDistanceGridFigure'
    SingleLossOrDistanceFigure = 'SingleLossDistanceFigure'
    LossDistanceSinglePairFigure = 'LossDistanceSinglePairFigure'
    DistanceVariationScatterFigure = 'DistanceVariationScatterFigure'
    FluxComparisonScatterWithTitle = 'FluxComparisonScatterWithTitle'
    FluxComparisonViolinBoxWithTitleLegend = 'FluxComparisonViolinBoxWithTitleLegend'
    DistanceFluxAnalysisHeatmapDataFigure = 'DistanceFluxAnalysisHeatmapDataFigure'
    MeanSTDCombinedHeatmap = 'MeanSTDCombinedHeatmap'
    AllFluxComparisonBarFigure = 'AllFluxComparisonBarFigure'
    EuclideanHeatmapScatter = 'EuclideanHeatmapScatter'
    SensitivityAllFluxHeatmap = 'SensitivityAllFluxHeatmap'
    ProtocolAllFluxHeatmap = 'ProtocolAllFluxHeatmap'
    ExperimentalOptimizationLossComparison = 'ExperimentalOptimizationLossComparison'


class Elements(object):
    DataFigure = DataFigure
    HeatmapConfig = HeatmapConfig
    ColorBarDataFigure = ColorBarDataFigure
    HeatmapDataFigure = BasicHeatmapDataFigure
    ScatterDataFigure = BasicScatterDataFigure
    BarDataFigure = BasicBarDataFigure
    FluxErrorBarDataFigure = BasicFluxErrorBarDataFigure
    MIDComparisonGridBarDataFigure = BasicMIDComparisonGridBarDataFigure
    BasicSingleBarDataFigure = BasicSingleBarDataFigure
    ViolinBoxDataFigure = BasicViolinBoxDataFigure
    HistogramDataFigure = BasicHistogramDataFigure


element_dict = {
    ElementName.DataFigure: DataFigure,
    ElementName.HeatmapDataFigure: BasicHeatmapDataFigure,
}
