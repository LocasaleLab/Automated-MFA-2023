from .basic_data_figure.data_figure import DataFigure
from .basic_data_figure.heatmap_data_figure import BasicHeatmapDataFigure
from .basic_data_figure.scatter_data_figure import GridScatterDataFigure, FluxComparisonScatterDataFigure
# from .basic_data_figure.violin_box_scatter_mix_data_figure import LossDistanceGridBoxScatterMixDataFigure
from .basic_data_figure.bar_data_figure import MIDComparisonGridBarDataFigure
from .basic_data_figure.violin_box_data_figure import TimeLossGridBoxDataFigure, FluxComparisonViolinBoxDataFigure, \
    LossDistanceGridBoxDataFigure
from .basic_data_figure.histogram_data_figure import TimeLossDistanceHistogramDataFigure
from .basic_data_figure.heatmap_data_figure import DistanceFluxAnalysisHeatmapDataFigure

from .complex_data_figure.mid_comparison_figure import MIDComparisonGridBarWithLegendDataFigure
from .complex_data_figure.time_loss_stack_figure import TimeLossStack
from .complex_data_figure.random_and_optimized_flux_comparison_figure import \
    RandomOptimizedFluxLayout, RandomOptimizedLossDistanceComparison, RandomOptimizedLossDistanceWithDiagramComparison
from .complex_data_figure.raw_model_loss_and_distance_grid_figure import LossDistanceGridFigure, \
    SingleLossOrDistanceFigure, LossDistanceSinglePairFigure
from .complex_data_figure.flux_comparison_scatter_with_title import FluxComparisonScatterWithTitle
from .complex_data_figure.flux_comparison_violin_box_with_title_legend import FluxComparisonViolinBoxWithTitleLegend
from .complex_data_figure.distance_variation_scatter_figure import DistanceVariationScatterFigure
from .complex_data_figure.complex_heatmap import MeanSTDCombinedHeatmap, EuclideanHeatmapScatter, \
    SensitivityAllFluxHeatmap, ProtocolAllFluxHeatmap
from .complex_data_figure.all_flux_comparison_bar_figure import AllFluxComparisonBarFigure, \
    OptimizedAllFluxComparisonBarDataFigure
from .complex_data_figure.experimental_optimization_loss_comparison import ExperimentalOptimizationLossComparison


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
    HeatmapDataFigure = BasicHeatmapDataFigure
    GridScatterDataFigure = GridScatterDataFigure
    MIDComparisonGridBarDataFigure = MIDComparisonGridBarDataFigure
    MIDComparisonGridBarWithLegendDataFigure = MIDComparisonGridBarWithLegendDataFigure
    OptimizedAllFluxComparisonBarDataFigure = OptimizedAllFluxComparisonBarDataFigure
    TimeLossGridBoxDataFigure = TimeLossGridBoxDataFigure
    LossDistanceGridBoxDataFigure = LossDistanceGridBoxDataFigure
    FluxComparisonViolinBoxDataFigure = FluxComparisonViolinBoxDataFigure
    FluxComparisonScatterDataFigure = FluxComparisonScatterDataFigure
    TimeLossHistogramDataFigure = TimeLossDistanceHistogramDataFigure
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
    DistanceFluxAnalysisHeatmapDataFigure = DistanceFluxAnalysisHeatmapDataFigure
    MeanSTDCombinedHeatmap = MeanSTDCombinedHeatmap
    AllFluxComparisonBarFigure = AllFluxComparisonBarFigure
    EuclideanHeatmapScatter = EuclideanHeatmapScatter
    SensitivityAllFluxHeatmap = SensitivityAllFluxHeatmap
    ProtocolAllFluxHeatmap = ProtocolAllFluxHeatmap
    ExperimentalOptimizationLossComparison = ExperimentalOptimizationLossComparison


element_dict = {
    ElementName.DataFigure: DataFigure,
    ElementName.HeatmapDataFigure: BasicHeatmapDataFigure,
    ElementName.GridScatterDataFigure: GridScatterDataFigure,
    ElementName.MIDComparisonGridBarDataFigure: MIDComparisonGridBarDataFigure,
    ElementName.MIDComparisonGridBarWithLegendDataFigure: MIDComparisonGridBarWithLegendDataFigure,
    ElementName.OptimizedAllFluxComparisonBarDataFigure: OptimizedAllFluxComparisonBarDataFigure,
    ElementName.TimeLossGridBoxDataFigure: TimeLossGridBoxDataFigure,
    ElementName.LossDistanceGridBoxDataFigure: LossDistanceGridBoxDataFigure,
    ElementName.FluxComparisonViolinBoxDataFigure: FluxComparisonViolinBoxDataFigure,
    ElementName.FluxComparisonScatterDataFigure: FluxComparisonScatterDataFigure,
    ElementName.TimeLossHistogramDataFigure: TimeLossDistanceHistogramDataFigure,
    ElementName.TimeLossStack: TimeLossStack,
    ElementName.RandomOptimizedFluxLayout: RandomOptimizedFluxLayout,
    ElementName.RandomOptimizedLossDistanceComparison: RandomOptimizedLossDistanceComparison,
    ElementName.RandomOptimizedLossDistanceWithDiagramComparison: RandomOptimizedLossDistanceWithDiagramComparison,
    ElementName.LossDistanceGridFigure: LossDistanceGridFigure,
    ElementName.SingleLossOrDistanceFigure: SingleLossOrDistanceFigure,
    ElementName.LossDistanceSinglePairFigure: LossDistanceSinglePairFigure,
    ElementName.DistanceVariationScatterFigure: DistanceVariationScatterFigure,
    ElementName.FluxComparisonScatterWithTitle: FluxComparisonScatterWithTitle,
    ElementName.FluxComparisonViolinBoxWithTitleLegend: FluxComparisonViolinBoxWithTitleLegend,
    ElementName.DistanceFluxAnalysisHeatmapDataFigure: DistanceFluxAnalysisHeatmapDataFigure,
    ElementName.MeanSTDCombinedHeatmap: MeanSTDCombinedHeatmap,
    ElementName.AllFluxComparisonBarFigure: AllFluxComparisonBarFigure,
    ElementName.EuclideanHeatmapScatter: EuclideanHeatmapScatter,
    ElementName.SensitivityAllFluxHeatmap: SensitivityAllFluxHeatmap,
    ElementName.ProtocolAllFluxHeatmap: ProtocolAllFluxHeatmap,
    ElementName.ExperimentalOptimizationLossComparison: ExperimentalOptimizationLossComparison,
}
