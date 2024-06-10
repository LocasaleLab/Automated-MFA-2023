from ..config import np, Vector, ModeName, MetaboliteConfig, ParameterName, LegendConfig

from ..metabolic_network_contents.metabolite import Metabolite
from ..metabolic_network_contents.reaction import Reaction


metabolite_width = MetaboliteConfig.width


class NormalLegendConfig(LegendConfig):
    metabolite_content_dict = {
        'G6P': Metabolite('G6P'),
        'LAC': Metabolite('LAC').set_mid_data_state(True),
        'MAL': Metabolite('MAL').set_mid_data_state(True).set_mixed_mid_data_state(True),
        'GLU': Metabolite('GLU').set_biomass_flux_state(True),
        'GLY': Metabolite('GLY').set_input_state(True),
        'GLC': Metabolite('GLC').set_input_state(True).set_c13_labeling_state(True),
    }
    reaction_content_dict = {
        'fluxes': (Reaction('unidirectional'), Reaction('bidirectional', reversible=True)),
        'boundary_flux': Reaction('boundary_flux').set_boundary_flux(True),
    }
    text_content_dict = {
        'G6P': 'Metabolites without MID data',
        'LAC': 'Metabolites with MID data',
        'MAL': 'Metabolites with mixed MID\ndata (mitochondria and cytosol)',
        'GLU': 'Metabolites with biomass flux',
        'GLY': 'Input or output metabolites\nwith fixed MID',
        'GLC': 'Input metabolites with $\mathregular{^{13}}$C\nlabelled',
        'fluxes': 'Normal fluxes (unidirectional\nor reversible)',
        'boundary_flux': 'Boundary fluxes with fixed value',
    }


class SmallerSizeLegendConfig(LegendConfig):
    metabolite_content_dict = {
        'GLN': Metabolite('GLN').set_input_state(True),
        'OAC': Metabolite('OAC'),
        # 'MAL': Metabolite('MAL').set_data_sensitivity_state(DataName.raw_model_raw_data),
        # '3PG': Metabolite('3PG').set_data_sensitivity_state(DataName.medium_data),
        # 'GLC': Metabolite('GLC').set_data_sensitivity_state(DataName.few_data),
        'MAL': Metabolite('MAL').set_other_color_state(MetaboliteConfig.raw_model_raw_data_color),
        '3PG': Metabolite('3PG').set_other_color_state(MetaboliteConfig.medium_data_color),
        'GLC': Metabolite('GLC').set_other_color_state(MetaboliteConfig.few_data_color),
    }
    reaction_content_dict = {}
    text_content_dict = {
        'GLN': 'Input or output metabolites\nwith fixed MID',
        'OAC': 'With MID data in all data set',
        'MAL': 'With MID data in all + experimental\ndata set',
        '3PG': 'With MID data in all + experimental\n+ medium data set',
        'GLC': 'With MID data in all + experimental\n+ medium + small data set',
    }


class RemovePathwayLegendConfig(LegendConfig):
    metabolite_content_dict = {
        'LAC': Metabolite('LAC').set_mid_data_state(True),
        # 'R5P': Metabolite('R5P').set_data_sensitivity_state(DataName.data_without_ppp),
        # 'MAL': Metabolite('MAL').set_data_sensitivity_state(DataName.data_without_tca),
        # 'GLU': Metabolite('GLU').set_data_sensitivity_state(DataName.data_without_aa),
        # 'CIT': Metabolite('CIT').set_data_sensitivity_state(DataName.medium_data_without_combination),
        'R5P': Metabolite('R5P').set_other_color_state(MetaboliteConfig.data_without_ppp_color),
        'MAL': Metabolite('MAL').set_other_color_state(MetaboliteConfig.data_without_tca_color),
        'GLU': Metabolite('GLU').set_other_color_state(MetaboliteConfig.data_without_aa_color),
    }
    reaction_content_dict = {}
    text_content_dict = {
        'LAC': 'Experimental data set',
        'R5P': 'Removed MID data of PPP metabolites',
        'MAL': 'Removed MID data of TCA metabolites',
        'GLU': 'Removed MID data of AA metabolites',
        # 'CIT': 'Added compartmental MID',
    }


class ConstantFluxLegendConfig(LegendConfig):
    metabolite_content_dict = {}
    reaction_content_dict = {
        'fluxes': (Reaction('unidirectional'), Reaction('bidirectional', reversible=True)),
        'boundary_fluxes': Reaction('boundary_flux').set_boundary_flux(True),
    }
    text_content_dict = {
        'fluxes': 'Normal fluxes (unidirectional\nor reversible)',
        'boundary_fluxes': 'Preset fixed boundary fluxes',
    }


def legend_layout_generator(mode=ParameterName.normal, preset_legend_config=None):
    if preset_legend_config is not None:
        legend_config = preset_legend_config
    elif mode == ParameterName.normal or mode == ParameterName.horizontal:
        legend_config = NormalLegendConfig
    elif mode == ModeName.smaller_data_size:
        legend_config = SmallerSizeLegendConfig
    elif mode == ModeName.data_without_pathway:
        legend_config = RemovePathwayLegendConfig
    elif mode == ModeName.different_constant_flux:
        legend_config = ConstantFluxLegendConfig
    else:
        raise ValueError()
    metabolite_content_dict, reaction_content_dict, text_content_dict = \
        legend_config.metabolite_content_dict, legend_config.reaction_content_dict, legend_config.text_content_dict

    total_item_list = []
    for metabolite_key, metabolite_content in metabolite_content_dict.items():
        text_content = text_content_dict[metabolite_key]
        total_item_list.append((ParameterName.metabolite, metabolite_key, metabolite_content, text_content))
    for reaction_key, reaction_content in reaction_content_dict.items():
        text_content = text_content_dict[reaction_key]
        total_item_list.append((ParameterName.reaction, reaction_key, reaction_content, text_content))

    total_item_num = len(total_item_list)
    each_row_height = legend_config.legend_each_row_height
    if mode == ParameterName.horizontal:
        total_row_num = 2
        total_col_num = np.ceil(total_item_num / 2)
        total_width = legend_config.legend_horizontal_width
    else:
        total_row_num = total_item_num
        total_col_num = 1
        total_width = legend_config.legend_width
    layout_index_list = [
        (item_index % total_row_num, item_index // total_row_num) for item_index in range(total_item_num)]
    total_height = total_row_num * each_row_height
    each_col_width = total_width / total_col_num

    # patch_center_x_axis = 0.15 * total_width
    # text_left_x_axis = 0.3 * total_width
    # text_width = total_width - text_left_x_axis
    multiple_reaction_up_down_distance = 0.005
    flux_width = metabolite_width
    base_patch_center_x_axis = 0.15 * each_col_width
    base_text_left_x_axis = 0.3 * each_col_width
    text_width = each_col_width - base_text_left_x_axis

    patch_raw_obj_dict = {}
    text_param_dict = {}
    for (row_index, col_index), (item_type, item_key, item_content, text_content) \
            in zip(layout_index_list, total_item_list):
        patch_center_x_axis = col_index * each_col_width + base_patch_center_x_axis
        text_left_x_axis = col_index * each_col_width + base_text_left_x_axis
        flux_left_x_value, flux_right_x_value = (
            patch_center_x_axis - flux_width / 2, patch_center_x_axis + flux_width / 2)
        irreversible_flux_right_x_value = 0.03 * flux_left_x_value + 0.97 * flux_right_x_value

        current_row_center_y_value = (total_row_num - row_index - 0.5) * each_row_height
        text_param_dict[item_key] = {
            ParameterName.center: Vector(text_left_x_axis + text_width / 2, current_row_center_y_value),
            ParameterName.string: text_content,
            ParameterName.width: text_width,
            ParameterName.height: each_row_height,
        }
        if item_type == ParameterName.metabolite:
            item_content.set_center(Vector(patch_center_x_axis, current_row_center_y_value))
            patch_raw_obj_dict[item_key] = item_content
        elif item_type == ParameterName.reaction:
            if isinstance(item_content, tuple):
                reaction_num = len(item_content)
                reaction_subrow_height = (each_row_height - 2 * multiple_reaction_up_down_distance) / reaction_num
                for reaction_subindex, reaction_obj in enumerate(item_content):
                    current_subrow_y_value = (
                            current_row_center_y_value + each_row_height / 2 - multiple_reaction_up_down_distance -
                            (reaction_subindex + 0.5) * reaction_subrow_height)
                    if reaction_obj.reversible:
                        current_flux_right_x_value = flux_right_x_value
                    else:
                        current_flux_right_x_value = irreversible_flux_right_x_value
                    reaction_obj.extend_reaction_start_end_list([
                        (
                            ParameterName.normal,
                            Vector(current_flux_right_x_value, current_subrow_y_value),
                            Vector(flux_left_x_value, current_subrow_y_value),
                            {}
                        )
                    ])
                    patch_raw_obj_dict[reaction_obj.reaction_name] = reaction_obj
            elif isinstance(item_content, Reaction):
                if item_content.reversible:
                    current_flux_right_x_value = flux_right_x_value
                else:
                    current_flux_right_x_value = irreversible_flux_right_x_value
                item_content.extend_reaction_start_end_list([
                    (
                        ParameterName.normal,
                        Vector(current_flux_right_x_value, current_row_center_y_value),
                        Vector(flux_left_x_value, current_row_center_y_value),
                        {}
                    )
                ])
                patch_raw_obj_dict[item_key] = item_content
            else:
                raise ValueError()
        row_index += 1
    # row_index = 0
    # for reaction_key, reaction_content in reaction_content_dict.items():
    #     current_row_center_y_value = (total_row_num - row_index - 0.5) * each_row_height
    #     text_content = text_content_dict[reaction_key]
    #     text_param_dict[reaction_key] = {
    #         ParameterName.center: Vector(text_left_x_axis + text_width / 2, current_row_center_y_value),
    #         ParameterName.string: text_content,
    #         ParameterName.width: text_width,
    #         ParameterName.height: each_row_height,
    #     }
    #     if isinstance(reaction_content, tuple):
    #         reaction_num = len(reaction_content)
    #         reaction_subrow_height = (each_row_height - 2 * multiple_reaction_up_down_distance) / reaction_num
    #         for reaction_subindex, reaction_obj in enumerate(reaction_content):
    #             current_subrow_y_value = (
    #                     current_row_center_y_value + each_row_height / 2 - multiple_reaction_up_down_distance -
    #                     (reaction_subindex + 0.5) * reaction_subrow_height)
    #             if reaction_obj.reversible:
    #                 current_flux_right_x_value = flux_right_x_value
    #             else:
    #                 current_flux_right_x_value = irreversible_flux_right_x_value
    #             reaction_obj.extend_reaction_start_end_list([
    #                 (
    #                     ParameterName.normal,
    #                     Vector(current_flux_right_x_value, current_subrow_y_value),
    #                     Vector(flux_left_x_value, current_subrow_y_value),
    #                     {}
    #                 )
    #             ])
    #             patch_raw_obj_dict[reaction_obj.reaction_name] = reaction_obj
    #     elif isinstance(reaction_content, Reaction):
    #         if reaction_content.reversible:
    #             current_flux_right_x_value = flux_right_x_value
    #         else:
    #             current_flux_right_x_value = irreversible_flux_right_x_value
    #         reaction_content.extend_reaction_start_end_list([
    #             (
    #                 ParameterName.normal,
    #                 Vector(current_flux_right_x_value, current_row_center_y_value),
    #                 Vector(flux_left_x_value, current_row_center_y_value),
    #                 {}
    #             )
    #         ])
    #         patch_raw_obj_dict[reaction_key] = reaction_content
    #     else:
    #         raise ValueError()
    #     row_index += 1
    return patch_raw_obj_dict, text_param_dict, total_width, total_height
