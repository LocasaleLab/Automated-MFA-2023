from ...common.common_figure_materials import DataName, CommonFigureString, \
    DataSensitivityMetabolicNetworkConfig, ModelDataSensitivityDataFigureConfig, MetabolicNetworkConfig
from ...common.config import np, Vector, ColorConfig, ZOrderConfig, TextBox, CompositeFigure, \
    ParameterName, FontWeight, HorizontalAlignment, VerticalAlignment, default_parameter_extract, GeneralElements, \
    CommonElementConfig, numbered_even_sequence

MetabolicNetworkWithLegend = GeneralElements.MetabolicNetworkWithLegend
MetabolicNetworkLegend = GeneralElements.MetabolicNetworkLegend
MetaboliteConfig = GeneralElements.MetaboliteConfig
ReactionConfig = GeneralElements.ReactionConfig


class SensitivityConfig(object):
    title_text_config = {
        **ReactionConfig.default_display_text_config,
        ParameterName.font_size: MetaboliteConfig.font_size + 5,
        ParameterName.font_weight: FontWeight.bold,
        # ParameterName.text_box: True
    }

