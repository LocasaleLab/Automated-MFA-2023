from .config import DataName, Vector, CompositeFigure, CommonElementConfig, ParameterName, \
    TextBox, default_parameter_extract, GeneralElements
from .config import ModelDataSensitivityDataFigureConfig, DataSensitivityMetabolicNetworkConfig, \
    SensitivityConfig, MetabolicNetworkConfig, MetabolicNetworkWithLegend
from .sensitivity_diagram_elements import ModelSensitivityDiagram, DataAvailabilityDiagram, ConfigSensitivityDiagram

RoundRectangle = GeneralElements.RoundRectangle
MetaboliteConfig = GeneralElements.MetaboliteConfig


class SingleSensitivityDiagram(CompositeFigure):
    def calculate_center(self, scale, *args):
        return self.total_size / 2 * scale

    def __init__(self, figure_data_parameter_dict, separate=False, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, None, pop=True)
        background = default_parameter_extract(figure_data_parameter_dict, ParameterName.background, True, pop=True)
        # model_sensitivity_set = {
        #     DataName.merge_reversible_reaction, DataName.combine_consecutive_reactions, DataName.prune_branches}
        # data_and_boundary_sensitivity_set = {
        #     DataName.smaller_data_size, DataName.data_without_pathway, DataName.different_constant_flux}
        model_sensitivity_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
        data_sensitivity_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_dict
        config_sensitivity_dict = ModelDataSensitivityDataFigureConfig.config_sensitivity_dict
        data_and_boundary_sensitivity_dict = {**data_sensitivity_dict, DataName.different_constant_flux: None}
        if mode in model_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'model_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                **figure_data_parameter_dict,
            }
            diagram_class = ModelSensitivityDiagram
        elif mode in data_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'data_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                ParameterName.separate: separate,
                **figure_data_parameter_dict,
            }
            diagram_class = DataAvailabilityDiagram
        elif mode in config_sensitivity_dict:
            effective_sensitivity_diagram_config_dict = {
                ParameterName.name: f'config_sensitivity_diagram_{mode}',
                ParameterName.mode: mode,
                **figure_data_parameter_dict,
            }
            diagram_class = ConfigSensitivityDiagram
        elif mode in data_and_boundary_sensitivity_dict:
            if mode == DataName.smaller_data_size:
                metabolic_network_config_dict = {
                    ParameterName.metabolite_data_sensitivity_state_dict:
                        DataSensitivityMetabolicNetworkConfig.smaller_size_data_sensitivity_dict,
                    ParameterName.input_metabolite_set: MetabolicNetworkConfig.common_input_metabolite_set,
                }
            elif mode == DataName.data_without_pathway:
                metabolic_network_config_dict = {
                    ParameterName.metabolite_data_sensitivity_state_dict:
                        DataSensitivityMetabolicNetworkConfig.remove_pathway_data_sensitivity_dict,
                    ParameterName.mid_data_metabolite_set:
                        MetabolicNetworkConfig.common_experimental_mid_metabolite_set,
                }
            elif mode == DataName.different_constant_flux:
                metabolic_network_config_dict = {
                    ParameterName.reaction_text_dict:
                        DataSensitivityMetabolicNetworkConfig.different_constant_flux_name_dict,
                    ParameterName.boundary_flux_set: set(
                        DataSensitivityMetabolicNetworkConfig.different_constant_flux_name_dict),
                }
            else:
                raise ValueError()
            effective_sensitivity_diagram_config_dict = {
                ParameterName.metabolic_network_config_dict: metabolic_network_config_dict,
                ParameterName.legend: True,
                ParameterName.metabolic_network_legend_config_dict: {ParameterName.mode: mode},
            }
            diagram_class = MetabolicNetworkWithLegend
        # elif mode == DataName.different_flux_range:
        #     effective_sensitivity_diagram_config_dict = {}
        #     diagram_class = FluxRangeTableDiagram
        else:
            raise ValueError()
        sensitivity_diagram_obj = diagram_class(**effective_sensitivity_diagram_config_dict)
        total_size = sensitivity_diagram_obj.size
        subfigure_element_dict = {'diagram': {'diagram': sensitivity_diagram_obj, }, }
        # if mode in data_and_boundary_sensitivity_dict:
        #     raw_total_height = total_size.y
        #     total_width = total_size.x
        #     title_text_height = 0.08
        #     total_height = raw_total_height + title_text_height
        #     figure_title_str = ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode]
        #     figure_title_config_dict = {
        #         **SensitivityConfig.title_text_config,
        #         ParameterName.font_size: MetaboliteConfig.font_size + 25,
        #         ParameterName.string: figure_title_str,
        #         ParameterName.width: total_width,
        #         ParameterName.height: title_text_height,
        #         ParameterName.center: Vector(total_width / 2 - 0.02, raw_total_height + title_text_height / 2)
        #     }
        #     title_text_obj = TextBox(**figure_title_config_dict)
        #     subfigure_element_dict['title'] = {'title': title_text_obj}
        #     total_size = Vector(total_width, total_height)
        if background:
            background_config_dict = {
                **CommonElementConfig.simulated_background_config_dict,
                ParameterName.center: total_size / 2,
                ParameterName.width: total_size.x,
                ParameterName.height: total_size.y,
            }
            subfigure_element_dict[ParameterName.background] = {
                ParameterName.background: RoundRectangle(**background_config_dict)
            }
        self.total_size = total_size
        self.total_width, self.total_height = self.total_size
        self.height_to_width_ratio = total_size[1] / total_size[0]
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class ComplexSensitivityDiagram(CompositeFigure):
    def calculate_center(self, scale, *args):
        return self.total_size / 2 * scale

    class Config(object):
        # model_sensitivity config:
        common_model_sensitivity_diagram_scale = 0.9
        model_sensitivity_size = Vector(0.8, 0.7)
        merge_reversible_reactions_center_x = 0.2
        combine_consecutive_reactions_center_x = 0.6
        upper_center_y = 0.53
        prune_branches_center_x = 0.4
        bottom_center_y = 0.17
        merge_reversible_reactions_target_center = Vector(merge_reversible_reactions_center_x, upper_center_y)
        combine_consecutive_reactions_target_center = Vector(combine_consecutive_reactions_center_x, upper_center_y)
        prune_branches_target_center = Vector(prune_branches_center_x, bottom_center_y)
        model_sensitivity_target_center_dict = {
            DataName.merge_reversible_reaction: merge_reversible_reactions_target_center,
            DataName.combine_consecutive_reactions: combine_consecutive_reactions_target_center,
            DataName.prune_branches: prune_branches_target_center,
        }

        # data_sensitivity config:
        common_data_sensitivity_diagram_scale = 0.8
        data_sensitivity_size = Vector(0.8, 0.67)
        top_panel_center_x = data_sensitivity_size.x / 2
        left_panel_center_x = 0.17
        smaller_data_size_center_y = 0.54
        data_without_pathway_center_y = 0.21
        right_panel_center_x = 0.55
        # right_center_y = 0.35
        smaller_data_size_target_center = Vector(top_panel_center_x, smaller_data_size_center_y)
        data_without_pathway_target_center = Vector(left_panel_center_x, data_without_pathway_center_y)
        compartmental_data_target_center = Vector(right_panel_center_x, data_without_pathway_center_y)
        data_sensitivity_target_center_dict = {
            DataName.smaller_data_size: smaller_data_size_target_center,
            DataName.data_without_pathway: data_without_pathway_target_center,
            DataName.compartmental_data: compartmental_data_target_center,
        }

        # config_sensitivity config:
        #################### Config with different flux range data #################
        # common_config_sensitivity_diagram_scale = 0.9
        # config_sensitivity_size = Vector(0.7, 0.4)
        # left_panel_center_x = 0.2
        # right_panel_center_x = 0.53
        # common_center_y = 0.3
        # different_constant_flux_target_center = Vector(left_panel_center_x, common_center_y)
        # different_flux_range_target_center = Vector(right_panel_center_x, common_center_y)
        #############################################################################
        common_config_sensitivity_diagram_scale = 1
        config_sensitivity_size = Vector(0.6, 0.4)
        center_x = config_sensitivity_size[0] / 2
        common_center_y = 0.3
        different_constant_flux_target_center = Vector(center_x, common_center_y)
        config_sensitivity_target_center_dict = {
            DataName.different_constant_flux: different_constant_flux_target_center,
        }

    @staticmethod
    def _arrange_subfigure_layout(content_dict, target_center_dict, common_scale, subfigure_obj_dict):
        for each_subfigure_mode in content_dict.keys():
            common_figure_parameter_dict = {
                ParameterName.bottom_left_offset: target_center_dict[each_subfigure_mode],
                ParameterName.scale: common_scale,
                ParameterName.separate: False,
                ParameterName.figure_data_parameter_dict: {
                    ParameterName.mode: each_subfigure_mode,
                    ParameterName.background: True,
                }
            }
            current_subfigure_diagram_obj = SingleSensitivityDiagram(**common_figure_parameter_dict)
            raw_center = current_subfigure_diagram_obj.calculate_center(common_scale)
            current_subfigure_diagram_obj.move_and_scale(bottom_left_offset=-raw_center)
            subfigure_obj_dict[each_subfigure_mode] = current_subfigure_diagram_obj

    def __init__(self, figure_data_parameter_dict, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode, pop=True)
        subfigure_obj_dict = {}
        if mode == DataName.model_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.model_sensitivity_dict
            target_center_dict = self.Config.model_sensitivity_target_center_dict
            scale = self.Config.common_model_sensitivity_diagram_scale
            total_size = self.Config.model_sensitivity_size
        elif mode == DataName.data_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.data_sensitivity_dict
            target_center_dict = self.Config.data_sensitivity_target_center_dict
            scale = self.Config.common_data_sensitivity_diagram_scale
            total_size = self.Config.data_sensitivity_size
        elif mode == DataName.config_sensitivity:
            content_dict = ModelDataSensitivityDataFigureConfig.config_sensitivity_dict
            target_center_dict = self.Config.config_sensitivity_target_center_dict
            scale = self.Config.common_config_sensitivity_diagram_scale
            total_size = self.Config.config_sensitivity_size
        else:
            raise ValueError()
        self._arrange_subfigure_layout(content_dict, target_center_dict, scale, subfigure_obj_dict)
        total_width, raw_total_height = total_size
        title_text_height = 0.08
        total_height = raw_total_height + title_text_height
        figure_title_str = ModelDataSensitivityDataFigureConfig.title_with_order_prefix[mode]
        title_config_dict = {
            **SensitivityConfig.title_text_config,
            ParameterName.font_size: MetaboliteConfig.font_size + 10,
            ParameterName.string: figure_title_str,
            ParameterName.width: total_width,
            ParameterName.height: title_text_height,
            ParameterName.center: Vector(total_width / 2 - 0.02, raw_total_height + title_text_height / 2)
        }
        subfigure_element_dict = {
            'diagram': subfigure_obj_dict,
            ParameterName.figure_title: {ParameterName.figure_title: TextBox(**title_config_dict)}
        }
        total_size = Vector(total_width, total_height)
        self.total_size = total_size
        self.total_width, self.total_height = total_size
        self.height_to_width_ratio = total_size[1] / total_size[0]
        super().__init__(
            subfigure_element_dict, Vector(0, 0), Vector(self.total_width, self.total_height), background=False,
            **kwargs)


class SensitivityDiagram(CompositeFigure):
    def __new__(cls, figure_data_parameter_dict, **kwargs):
        mode = default_parameter_extract(figure_data_parameter_dict, ParameterName.mode)
        complex_data_name_set = {
            DataName.model_sensitivity, DataName.data_sensitivity, DataName.config_sensitivity}
        if mode in complex_data_name_set:
            target_obj = ComplexSensitivityDiagram(figure_data_parameter_dict, **kwargs)
        else:
            target_obj = SingleSensitivityDiagram(figure_data_parameter_dict, separate=True, **kwargs)
        return target_obj

