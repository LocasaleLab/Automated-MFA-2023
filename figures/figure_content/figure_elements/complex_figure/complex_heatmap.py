from ...common.config import np, DataFigureConfig, DataFigureParameterName as ParameterName, \
    Vector, FontWeight, CompositeFigure, TextBox, VerticalAlignment, default_parameter_extract, CommonElementConfig
from ...common.common_figure_materials import CommonFigureString
from ..data_figure.heatmap_data_figure import DistanceFluxAnalysisHeatmapDataFigure, \
    SensitivityAnalysisHeatmapDataFigure
from ..data_figure.figure_data_loader import all_fluxes_relative_error_data
from .distance_variation_scatter_figure import DistanceVariationScatterFigure


class MeanSTDCombinedHeatmap(CompositeFigure):
    total_width = 0.73
    # total_height = 0.47
    total_height = 0.44
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        figure_class = figure_data_parameter_dict[ParameterName.figure_class]
        data_name = figure_data_parameter_dict[ParameterName.data_name]
        figure_title = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_title, True)
        if figure_class == ParameterName.net_euclidean_distance:
            flux_name = None
            title_string = CommonFigureString.euclidean_distance
            decimal_num = 0
        elif figure_class == ParameterName.flux_relative_distance:
            flux_name = figure_data_parameter_dict[ParameterName.flux_name]
            title_string = flux_name
            decimal_num = None
        else:
            raise ValueError()

        total_width = self.total_width
        heatmap_scale = 1
        heatmap_size = Vector(0.3, 0.3)
        heatmap_width, heatmap_height = heatmap_size
        cbar_height = 0.03
        cbar_distance = 0.05
        cbar_bottom = 0.02
        heatmap_bottom = cbar_bottom + cbar_height + cbar_distance
        heatmap_top = heatmap_bottom + heatmap_height  # 0.4
        # title_heatmap_distance = 0.014
        sub_title_area_height = 0.04
        title_area_height = 0.03
        heatmap_horizontal_distance = 0.055
        x_loc_offset = 0.01
        mean_x_loc = total_width / 2 - heatmap_horizontal_distance / 2 - heatmap_width + x_loc_offset
        std_x_loc = total_width / 2 + heatmap_horizontal_distance / 2 + x_loc_offset
        sub_title_center_y = heatmap_top + sub_title_area_height / 2

        if figure_title:
            self.total_height += title_area_height

        common_cbar_figure_data_parameter_dict = {}
        common_distance_figure_parameter_dict = {
            ParameterName.figure_class: figure_class,
            ParameterName.flux_name: flux_name,
            ParameterName.data_name: data_name,
        }
        common_distance_config_dict = {
            ParameterName.size: heatmap_size,
            ParameterName.scale: heatmap_scale,
            ParameterName.cbar_size: Vector(heatmap_width, cbar_height),
            ParameterName.cbar_scale: heatmap_scale,
            ParameterName.cbar: True,
            # ParameterName.highlight: True,
        }
        mean_distance_config_dict = {
            **common_distance_config_dict,
            ParameterName.bottom_left: Vector(mean_x_loc, heatmap_bottom),
            ParameterName.figure_data_parameter_dict: {
                **common_distance_figure_parameter_dict,
                ParameterName.mean_or_std: ParameterName.mean,
            },
            ParameterName.cbar_bottom_left: Vector(mean_x_loc, cbar_bottom),
            ParameterName.cbar_figure_data_parameter_dict: {
                **common_cbar_figure_data_parameter_dict,
                ParameterName.decimal_num: decimal_num,
            },
        }
        std_distance_config_dict = {
            **common_distance_config_dict,
            ParameterName.bottom_left: Vector(std_x_loc, heatmap_bottom),
            ParameterName.figure_data_parameter_dict: {
                **common_distance_figure_parameter_dict,
                ParameterName.mean_or_std: ParameterName.std,
            },
            ParameterName.cbar_bottom_left: Vector(std_x_loc, cbar_bottom),
            ParameterName.cbar_figure_data_parameter_dict: {
                **common_cbar_figure_data_parameter_dict,
                ParameterName.decimal_num: decimal_num,
            },
        }
        common_heatmap_mean_std_title_config_dict = {
            **DataFigureConfig.common_title_config_dict,
            ParameterName.font_size: 15,
            ParameterName.width: heatmap_width,
            ParameterName.height: sub_title_area_height,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline
        }
        title_config_dict = {
            **common_heatmap_mean_std_title_config_dict,
            ParameterName.string: title_string,
            ParameterName.font_size: 20,
            ParameterName.width: total_width,
            ParameterName.height: title_area_height,
            ParameterName.center: Vector(
                total_width / 2,
                heatmap_top + sub_title_area_height + title_area_height / 2,
            ),
            # ParameterName.text_box: True,
        }
        mean_title_config_dict = {
            **common_heatmap_mean_std_title_config_dict,
            ParameterName.font_weight: FontWeight.normal,
            ParameterName.string: CommonFigureString.mean,
            ParameterName.center: Vector(mean_x_loc + heatmap_width / 2, sub_title_center_y),
        }
        std_title_config_dict = {
            **common_heatmap_mean_std_title_config_dict,
            ParameterName.font_weight: FontWeight.normal,
            ParameterName.string: CommonFigureString.std,
            ParameterName.center: Vector(std_x_loc + heatmap_width / 2, sub_title_center_y),
        }

        subfigure_element_dict = {
            'heatmap': {
                'mean': DistanceFluxAnalysisHeatmapDataFigure(**mean_distance_config_dict),
                'STD': DistanceFluxAnalysisHeatmapDataFigure(**std_distance_config_dict),
            },
            'title': {
                'mean': TextBox(**mean_title_config_dict),
                'STD': TextBox(**std_title_config_dict),
            },
        }
        if figure_title:
            subfigure_element_dict['title']['complete'] = TextBox(**title_config_dict)
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False, **kwargs)


class EuclideanFluxCombinedHeatmap(CompositeFigure):
    total_width = 1
    total_height = 0.75
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        current_data_name = figure_data_parameter_dict[ParameterName.data_name]
        left_flux_name, right_flux_name = figure_data_parameter_dict[ParameterName.flux_name]

        # upper_heatmap_bottom = 0.3
        # flux_heatmap_scale = 0.65
        upper_heatmap_left = 0
        upper_heatmap_bottom = 0.35
        euclidean_distance_scale = 0.8
        distance_variation_scatter_scale = euclidean_distance_scale
        flux_heatmap_scale = 0.65
        bottom_left_heatmap_center_x = 0.25
        bottom_right_heatmap_center_x = 0.75
        distance_heatmap_scatter_distance = 0
        euclidean_heatmap_config_dict = {
            ParameterName.bottom_left_offset: Vector(upper_heatmap_left, upper_heatmap_bottom),
            ParameterName.scale: euclidean_distance_scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: current_data_name,
            },
        }
        euclidean_mean_std_heatmap = MeanSTDCombinedHeatmap(**euclidean_heatmap_config_dict)
        euclidean_mean_std_heatmap_total_size = euclidean_mean_std_heatmap.calculate_center(
            euclidean_mean_std_heatmap, euclidean_distance_scale) * 2

        distance_variation_scatter_left = upper_heatmap_left + \
            euclidean_mean_std_heatmap_total_size.x + distance_heatmap_scatter_distance
        distance_variation_scatter_figure_config_dict = {
            ParameterName.bottom_left_offset: Vector(distance_variation_scatter_left, upper_heatmap_bottom),
            ParameterName.scale: distance_variation_scatter_scale,
            ParameterName.data_name: current_data_name
        }
        distance_variation_scatter_figure = DistanceVariationScatterFigure(
            **distance_variation_scatter_figure_config_dict)

        combined_heatmap_center = MeanSTDCombinedHeatmap.calculate_center(MeanSTDCombinedHeatmap, flux_heatmap_scale)
        left_flux_heatmap_config_dict = {
            ParameterName.bottom_left_offset: Vector(bottom_left_heatmap_center_x - combined_heatmap_center.x, 0),
            ParameterName.scale: flux_heatmap_scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.flux_relative_distance,
                ParameterName.data_name: current_data_name,
                ParameterName.flux_name: left_flux_name
            },
        }
        right_flux_heatmap_config_dict = {
            ParameterName.bottom_left_offset: Vector(bottom_right_heatmap_center_x - combined_heatmap_center.x, 0),
            ParameterName.scale: flux_heatmap_scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.flux_relative_distance,
                ParameterName.data_name: current_data_name,
                ParameterName.flux_name: right_flux_name
            },
        }

        subfigure_element_dict = {
            'euclidean_distance': {
                'euclidean_distance': euclidean_mean_std_heatmap,
                'distance_variation_scatter_figure': distance_variation_scatter_figure,
            },
            'left_flux': {
                'left_flux': MeanSTDCombinedHeatmap(**left_flux_heatmap_config_dict),
            },
            'right_flux': {
                'right_flux': MeanSTDCombinedHeatmap(**right_flux_heatmap_config_dict),
            },
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False, **kwargs)


class EuclideanHeatmapScatter(CompositeFigure):
    total_width = 1
    total_height = 0.39
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        current_data_name = figure_data_parameter_dict[ParameterName.data_name]
        total_width = self.total_width
        total_height = self.total_height
        upper_heatmap_left = 0
        upper_heatmap_bottom = 0
        title_area_height = 0.03

        euclidean_distance_scale = 0.8
        distance_variation_scatter_scale = euclidean_distance_scale
        distance_heatmap_scatter_distance = 0
        euclidean_heatmap_config_dict = {
            ParameterName.bottom_left_offset: Vector(upper_heatmap_left, upper_heatmap_bottom),
            ParameterName.scale: euclidean_distance_scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.figure_class: ParameterName.net_euclidean_distance,
                ParameterName.data_name: current_data_name,
                ParameterName.figure_title: False,
            },
        }
        euclidean_mean_std_heatmap = MeanSTDCombinedHeatmap(**euclidean_heatmap_config_dict)
        euclidean_mean_std_heatmap_total_size = euclidean_mean_std_heatmap.calculate_center(
            euclidean_mean_std_heatmap, euclidean_distance_scale) * 2

        distance_variation_scatter_left = upper_heatmap_left + \
            euclidean_mean_std_heatmap_total_size.x + distance_heatmap_scatter_distance
        distance_variation_scatter_figure_config_dict = {
            ParameterName.bottom_left_offset: Vector(distance_variation_scatter_left, upper_heatmap_bottom),
            ParameterName.scale: distance_variation_scatter_scale,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: current_data_name
            },
        }
        distance_variation_scatter_figure = DistanceVariationScatterFigure(
            **distance_variation_scatter_figure_config_dict)

        data_figure_height = euclidean_mean_std_heatmap_total_size.y
        title_center_y = data_figure_height + title_area_height / 2

        title_config_dict = {
            **DataFigureConfig.common_title_config_dict,
            ParameterName.vertical_alignment: VerticalAlignment.center_baseline,
            ParameterName.string: CommonFigureString.euclidean_distance,
            ParameterName.font_size: 15,
            ParameterName.width: total_width,
            ParameterName.height: title_area_height,
            ParameterName.center: Vector(total_width / 2, title_center_y),
            # ParameterName.text_box: True,
        }

        subfigure_element_dict = {
            'euclidean_distance': {
                'euclidean_distance': euclidean_mean_std_heatmap,
                'distance_variation_scatter_figure': distance_variation_scatter_figure,
            },
            'title': {
                'main_title': TextBox(**title_config_dict),
            }
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False, **kwargs)


class ProtocolAllFluxHeatmap(CompositeFigure):
    total_width = 1
    total_height = 0.35
    height_to_width_ratio = total_height / total_width

    def __init__(self, figure_data_parameter_dict, **kwargs):
        current_data_name = figure_data_parameter_dict[ParameterName.data_name]
        flux_name_list = figure_data_parameter_dict[ParameterName.flux_name_list]
        figure_title = figure_data_parameter_dict[ParameterName.figure_title]

        flux_heatmap_scale = 0.33
        boundary = 0.02
        col_num = 4
        row_num = 2
        # heatmap_total_height = 0.3
        heatmap_total_height = flux_heatmap_scale
        heatmap_location_y_offset = 0.078
        title_box_height = 0.02
        # title_box_bottom = 0.3
        title_box_bottom = heatmap_total_height + 0.005

        heatmap_center_x_list = (
            np.linspace(boundary, 1 - boundary, (col_num + 1)) + (1 - 2 * boundary) / (2 * col_num))[:-1]
        # [0.125, 0.375, 0.625, 0.875]
        # heatmap_center_y_list = [0.075, 0.225]
        heatmap_center_y_list = np.linspace(0, heatmap_total_height, row_num + 1)[:-1] + heatmap_location_y_offset

        self.total_height = title_box_bottom + title_box_height
        title_box_center = Vector(self.total_width / 2, title_box_bottom + title_box_height / 2)
        title_config_dict = {
            **CommonElementConfig.common_text_config,
            # ParameterName.font: DataFigureConfig.main_text_font,
            ParameterName.vertical_alignment: VerticalAlignment.baseline,
            # ParameterName.z_order: DataFigureConfig.figure_text_z_order,
            ParameterName.font_size: 10,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.text_box: False,
            ParameterName.string: figure_title,
            ParameterName.center: title_box_center,
            ParameterName.width: self.total_width,
            ParameterName.height: title_box_height,
        }

        flux_name_heatmap_obj_dict = {}
        for row_index, flux_name_row_list in enumerate(flux_name_list):
            for col_index, flux_name in enumerate(flux_name_row_list):
                center_location = Vector(
                    heatmap_center_x_list[col_index],
                    heatmap_center_y_list[len(heatmap_center_y_list) - row_index - 1])
                flux_heatmap_config_dict = {
                    ParameterName.bottom_left_offset: center_location,
                    ParameterName.scale: flux_heatmap_scale,
                    ParameterName.figure_data_parameter_dict: {
                        ParameterName.figure_class: ParameterName.flux_relative_distance,
                        ParameterName.data_name: current_data_name,
                        ParameterName.flux_name: flux_name
                    },
                }
                each_flux_mean_std_heatmap = MeanSTDCombinedHeatmap(**flux_heatmap_config_dict)
                flux_mean_std_heatmap_center = each_flux_mean_std_heatmap.calculate_center(
                    each_flux_mean_std_heatmap, flux_heatmap_scale)
                each_flux_mean_std_heatmap.move_and_scale(bottom_left_offset=-flux_mean_std_heatmap_center)
                flux_name_heatmap_obj_dict[flux_name] = each_flux_mean_std_heatmap
        subfigure_element_dict = {
            'flux_heatmap': flux_name_heatmap_obj_dict,
            'title': {'title': TextBox(**title_config_dict)}
        }
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class SensitivityAllFluxHeatmap(CompositeFigure):
    total_width = 1
    heatmap_width = 0.9
    each_row_height = heatmap_width / 55
    bottom_tick_label_height = 0.16
    cbar_area_height = 0.1
    cbar_height = 0.03
    cbar_bottom = 0.06
    title_area_height = 0.055

    @staticmethod
    def get_row_num(data_name):
        data_matrix, *_ = all_fluxes_relative_error_data.return_data(data_name=data_name)
        heatmap_row_num = data_matrix.shape[0]
        return heatmap_row_num

    @staticmethod
    def calculate_heatmap_height(self, row_num):
        return self.each_row_height * row_num

    @staticmethod
    def calculate_total_height(self, heatmap_height, cbar, figure_title=None):
        return heatmap_height + self.bottom_tick_label_height + (self.cbar_area_height if cbar else 0) + \
            (self.title_area_height if figure_title is not None else 0)

    @staticmethod
    def calculate_center(self, scale, *args):
        cbar = False
        figure_title = None
        if len(args) == 1:
            data_name = args[0]
        elif len(args) == 2:
            data_name, cbar = args
        elif len(args) == 3:
            data_name, cbar, figure_title = args
        else:
            raise ValueError()
        heatmap_height = self.calculate_heatmap_height(self, self.get_row_num(data_name))
        total_height = self.calculate_total_height(self, heatmap_height, cbar, figure_title)
        return Vector(self.total_width, total_height) * scale / 2

    def __init__(self, figure_data_parameter_dict, cbar=False, **kwargs):
        current_data_name = figure_data_parameter_dict[ParameterName.data_name]
        row_num = self.get_row_num(current_data_name)
        figure_title = default_parameter_extract(figure_data_parameter_dict, ParameterName.figure_title, None)
        heatmap_height = self.calculate_heatmap_height(self, row_num)
        total_height = self.calculate_total_height(self, heatmap_height, cbar, figure_title)
        self.total_height = total_height
        self.height_to_width_ratio = total_height / self.total_width

        heatmap_width = self.heatmap_width
        heatmap_left = self.total_width - heatmap_width
        heatmap_bottom = self.bottom_tick_label_height + (self.cbar_area_height if cbar else 0)
        heatmap_top = self.calculate_total_height(self, heatmap_height, cbar)
        cbar_config = {
            ParameterName.cbar_bottom_left: Vector(heatmap_left, self.cbar_bottom),
            ParameterName.cbar_size: Vector(heatmap_width, self.cbar_height),
            ParameterName.cbar_scale: 1,
            ParameterName.cbar_figure_data_parameter_dict: {},
        }

        sensitivity_analysis_config_dict = {
            ParameterName.bottom_left: Vector(heatmap_left, heatmap_bottom),
            ParameterName.size: Vector(heatmap_width, heatmap_height),
            ParameterName.scale: 1,
            ParameterName.figure_data_parameter_dict: {
                ParameterName.data_name: current_data_name,
            },
            ParameterName.cbar: cbar,
            **cbar_config
        }

        title_config_dict = {
            **CommonElementConfig.common_text_config,
            ParameterName.string: figure_title,
            ParameterName.font_weight: FontWeight.bold,
            ParameterName.font_size: 17,
            ParameterName.width: heatmap_width,
            ParameterName.height: self.title_area_height,
            ParameterName.center: Vector(heatmap_left + heatmap_width / 2, heatmap_top + self.title_area_height / 2)
        }

        subfigure_element_dict = {
            'sensitivity_all_flux': {
                'sensitivity_all_flux': SensitivityAnalysisHeatmapDataFigure(
                    **sensitivity_analysis_config_dict),
            },
        }
        if figure_title is not None:
            subfigure_element_dict['heatmap_title'] = {'heatmap_title': TextBox(**title_config_dict)}
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)



