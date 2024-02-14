from .config import ParameterName, DataName, construct_mixed_metabolite_obj, NetworkDiagram as BasicNetworkDiagram, \
    NetworkDiagramConfig


class NetworkDiagram(BasicNetworkDiagram):
    def __init__(self, mode=ParameterName.normal, **kwargs):
        super().__init__(mode=mode, layout_decorator=network_diagram_decorator, **kwargs)


center_name = ParameterName.center


def network_diagram_decorator(raw_diagram_layout_generator):
    def new_diagram_layout_generator(metabolite_radius, width, height_to_width_ratio, mode):
        (
            metabolite_circle_config_dict, metabolite_ellipse_config_dict, reaction_location_dict,
            background_range, mito_background_range, tca_cycle_center, tca_cycle_radius
        ) = raw_diagram_layout_generator(
            metabolite_radius, width, height_to_width_ratio, mode)
        if mode != ParameterName.normal:
            measured_metabolite_color = NetworkDiagramConfig.measured_metabolite_color
            if mode == DataName.smaller_data_size:
                metabolite_color_dict = {
                    'g6p_c': measured_metabolite_color,
                    'pyr_c': measured_metabolite_color,
                    'cit_m': measured_metabolite_color,
                    'suc_m': measured_metabolite_color,
                    'ser_c': measured_metabolite_color,
                    'glu_c': measured_metabolite_color,
                }
            elif mode == DataName.data_without_pathway:
                metabolite_color_dict = {
                    '3pg_c': measured_metabolite_color,
                    'g6p_c': measured_metabolite_color,
                    'rib_c': measured_metabolite_color,
                    'pyr_c': measured_metabolite_color,
                    'lac_c': measured_metabolite_color,
                    'ser_c': measured_metabolite_color,
                    'gly_c': measured_metabolite_color,
                    'glu_c': measured_metabolite_color,
                }
            elif mode == DataName.medium_data_without_combination:
                mixed_metabolite_basic_config_dict = {
                    'pyr': construct_mixed_metabolite_obj(
                        metabolite_circle_config_dict['pyr_c'][center_name],
                        metabolite_circle_config_dict['pyr_m'][center_name],
                        metabolite_radius, orientation=ParameterName.vertical),
                    'cit': construct_mixed_metabolite_obj(
                        metabolite_circle_config_dict['cit_c'][center_name],
                        metabolite_circle_config_dict['cit_m'][center_name],
                        metabolite_radius, orientation=ParameterName.horizontal),
                    'glu': construct_mixed_metabolite_obj(
                        metabolite_circle_config_dict['glu_c'][center_name],
                        metabolite_circle_config_dict['akg_m'][center_name],
                        metabolite_radius, orientation=ParameterName.vertical),
                }
                for metabolite_name, mixed_metabolite_basic_config in mixed_metabolite_basic_config_dict.items():
                    metabolite_ellipse_config_dict[metabolite_name] = {
                        **NetworkDiagramConfig.mixed_metabolite_ellipse_config,
                        ParameterName.name: metabolite_name,
                        ParameterName.face_color: measured_metabolite_color,
                        **mixed_metabolite_basic_config,
                    }
                smaller_metabolite_list = [
                    'pyr_c', 'pyr_m', 'cit_c', 'cit_m', 'glu_c', 'akg_m'
                ]
                for metabolite_name in smaller_metabolite_list:
                    metabolite_circle_config_dict[metabolite_name].update({
                        ParameterName.radius: metabolite_radius * 0.9
                    })
                metabolite_color_dict = {
                    'g6p_c': measured_metabolite_color,
                    'suc_m': measured_metabolite_color,
                    'oac_m': measured_metabolite_color,
                    'ser_c': measured_metabolite_color,
                }
            elif mode == DataName.data_sensitivity:
                metabolite_color_dict = {}
            else:
                raise ValueError()
            for metabolite_name, metabolite_color in metabolite_color_dict.items():
                metabolite_circle_config_dict[metabolite_name].update({
                    ParameterName.face_color: metabolite_color
                })
        return (
            metabolite_circle_config_dict, metabolite_ellipse_config_dict, reaction_location_dict,
            background_range, mito_background_range, tca_cycle_center, tca_cycle_radius)

    return new_diagram_layout_generator
