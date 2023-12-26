from scripts.src.core.common.classes import OptionDict, MFAConfig
from scripts.src.core.common.config import ParamName

from .sensitivity_config import raw_config_first, ConfigSetting, Keywords, flux_range_dict, \
    constant_flux_value_nested_dict, constant_flux_value_nested_dict_with_noise
from .config import analysis_solver, average_solution_optimization_selection_parameters_dict

slsqp_solver_config_dict = OptionDict({
    ParamName.loss_type: ParamName.cross_entropy_loss,
    ParamName.debug: True,
})

mean_squared_loss_slsqp_solver_config_dict = OptionDict({
    ParamName.loss_type: ParamName.mean_squared_loss,
    ParamName.debug: True,
})

base_flux_range = (1, 1000)
base_constant_flux_value_dict = {'GLC_input': 200}
base_mix_ratio_range = (0.05, 0.95)
base_mix_ratio_multiplier = 100
base_slsqp_mfa_config = MFAConfig(
    common_flux_range=base_flux_range, specific_flux_range_dict={}, dynamic_constant_flux_list=[],
    preset_constant_flux_value_dict=base_constant_flux_value_dict,
    common_mix_ratio_range=base_mix_ratio_range, mix_ratio_multiplier=base_mix_ratio_multiplier,
    solver_type=analysis_solver, solver_config_dict=slsqp_solver_config_dict)


mean_squared_loss_slsqp_mfa_config = MFAConfig(
    common_flux_range=base_flux_range, specific_flux_range_dict={}, dynamic_constant_flux_list=[],
    preset_constant_flux_value_dict=base_constant_flux_value_dict,
    common_mix_ratio_range=base_mix_ratio_range, mix_ratio_multiplier=base_mix_ratio_multiplier,
    solver_type=analysis_solver, solver_config_dict=mean_squared_loss_slsqp_solver_config_dict)


def boundary_condition_processor(process_type, simulated_flux_value_dict):
    # parameter_dict = {Keywords.raw_type: (base_flux_range, base_constant_flux_value_dict)}
    # information_dict = {Keywords.raw_type: Keywords.raw_type}
    parameter_dict = {}
    information_dict = {}
    final_config_dict = {}
    with_raw_type = False
    if process_type == ConfigSetting.different_flux_range:
        with_raw_type = True
        for current_config_name, current_flux_range in flux_range_dict.items():
            parameter_dict[current_config_name] = (current_flux_range, base_constant_flux_value_dict)
            information_dict[current_config_name] = f'flux_range: {current_flux_range}'
    elif process_type == ConfigSetting.different_constant_flux:
        with_raw_type = True
        for current_config_name, current_constant_flux_name_set in constant_flux_value_nested_dict.items():
            current_constant_flux_value_dict = {
                constant_flux_name: simulated_flux_value_dict[constant_flux_name]
                for constant_flux_name in current_constant_flux_name_set}
            parameter_dict[current_config_name] = (base_flux_range, current_constant_flux_value_dict)
            constant_flux_name_list = ', '.join(current_constant_flux_name_set)
            information_dict[current_config_name] = f'constant_flux_name: {constant_flux_name_list}'
    elif process_type == ConfigSetting.different_constant_flux_with_noise:
        with_raw_type = True
        for current_config_name, current_constant_flux_name_noise_ratio_dict in \
                constant_flux_value_nested_dict_with_noise.items():
            current_constant_flux_value_dict = {
                constant_flux_name: simulated_flux_value_dict[constant_flux_name] * noise_ratio
                for constant_flux_name, noise_ratio in current_constant_flux_name_noise_ratio_dict.items()}
            parameter_dict[current_config_name] = (base_flux_range, current_constant_flux_value_dict)
            constant_flux_name_noise_ratio_pair_list = ', '.join([
                f'{flux_name}: {noise_ratio}'
                for flux_name, noise_ratio in current_constant_flux_name_noise_ratio_dict.items()
            ])
            information_dict[current_config_name] = f'constant_flux_name: ' \
                                                    f'{constant_flux_name_noise_ratio_pair_list}'
    elif process_type in {
            ConfigSetting.optimization_from_average_solutions,
            ConfigSetting.optimization_from_average_solutions_with_mean_squared_loss}:
        for current_config_name, current_optimization_selection_parameter_dict in \
                average_solution_optimization_selection_parameters_dict.items():
            miscellaneous_config_dict = {
                Keywords.predefined_initial_solution_matrix: dict(current_optimization_selection_parameter_dict)
            }
            if process_type == ConfigSetting.optimization_from_average_solutions:
                current_slsqp_mfa_config = base_slsqp_mfa_config.copy()
            else:
                current_slsqp_mfa_config = mean_squared_loss_slsqp_mfa_config.copy()
                current_config_name = f'{Keywords.squared_loss}_{current_config_name}'
            current_slsqp_mfa_config.miscellaneous_config = miscellaneous_config_dict
            information_dict[current_config_name] = dict(current_optimization_selection_parameter_dict)
            final_config_dict[current_config_name] = current_slsqp_mfa_config
    elif process_type == ConfigSetting.mean_squared_loss:
        current_config_name = process_type
        information_dict[current_config_name] = {Keywords.label: process_type}
        final_config_dict[current_config_name] = mean_squared_loss_slsqp_mfa_config.copy()
    elif process_type == Keywords.raw_type:
        with_raw_type = True
    else:
        raise ValueError()
    if with_raw_type:
        if raw_config_first:
            raw_parameter_dict = {Keywords.raw_type: (base_flux_range, base_constant_flux_value_dict)}
            raw_parameter_dict.update(parameter_dict)
            raw_information_dict = {Keywords.raw_type: Keywords.raw_type}
            raw_information_dict.update(information_dict)
            parameter_dict = raw_parameter_dict
            information_dict = raw_information_dict
        else:
            parameter_dict[Keywords.raw_type] = (base_flux_range, base_constant_flux_value_dict)
            information_dict[Keywords.raw_type] = Keywords.raw_type
    for config_label, (flux_range, constant_flux_value_dict) in parameter_dict.items():
        slsqp_mfa_config = MFAConfig(
            common_flux_range=flux_range, specific_flux_range_dict={}, dynamic_constant_flux_list=[],
            preset_constant_flux_value_dict=constant_flux_value_dict,
            common_mix_ratio_range=base_mix_ratio_range, mix_ratio_multiplier=base_mix_ratio_multiplier,
            solver_type=analysis_solver, solver_config_dict=slsqp_solver_config_dict)
        final_config_dict[config_label] = slsqp_mfa_config
    return final_config_dict, information_dict
