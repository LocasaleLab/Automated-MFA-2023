from scripts.src.core.common.classes import OptionDict, MFAConfig
from scripts.src.core.common.config import ParamName

from .sensitivity_config import raw_config_first, ConfigSetting, Keywords, flux_range_dict, \
    constant_flux_value_nested_dict, constant_flux_value_nested_dict_with_noise
from .config import analysis_solver

slsqp_solver_config_dict = OptionDict({
    ParamName.loss_type: ParamName.cross_entropy_loss,
    ParamName.debug: True,
})

base_flux_range = (1, 1000)
base_constant_flux_value_dict = {'GLC_input': 200}


def boundary_condition_processor(process_type, simulated_flux_value_dict):
    # parameter_dict = {Keywords.raw_type: (base_flux_range, base_constant_flux_value_dict)}
    # information_dict = {Keywords.raw_type: Keywords.raw_type}
    parameter_dict = {}
    information_dict = {}
    if process_type == ConfigSetting.different_flux_range:
        for current_config_name, current_flux_range in flux_range_dict.items():
            parameter_dict[current_config_name] = (current_flux_range, base_constant_flux_value_dict)
            information_dict[current_config_name] = f'flux_range: {current_flux_range}'
    elif process_type == ConfigSetting.different_constant_flux:
        for current_config_name, current_constant_flux_name_set in constant_flux_value_nested_dict.items():
            current_constant_flux_value_dict = {
                constant_flux_name: simulated_flux_value_dict[constant_flux_name]
                for constant_flux_name in current_constant_flux_name_set}
            parameter_dict[current_config_name] = (base_flux_range, current_constant_flux_value_dict)
            constant_flux_name_list = ', '.join(current_constant_flux_name_set)
            information_dict[current_config_name] = f'constant_flux_name: {constant_flux_name_list}'
    elif process_type == ConfigSetting.different_constant_flux_with_noise:
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
    elif process_type == Keywords.raw_type:
        pass
    else:
        raise ValueError()
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
    final_config_dict = {}
    for config_label, (flux_range, constant_flux_value_dict) in parameter_dict.items():
        slsqp_mfa_config = MFAConfig(
            common_flux_range=flux_range, specific_flux_range_dict={}, dynamic_constant_flux_list=[],
            preset_constant_flux_value_dict=constant_flux_value_dict,
            common_mix_ratio_range=(0.05, 0.95), mix_ratio_multiplier=100,
            solver_type=analysis_solver, solver_config_dict=slsqp_solver_config_dict)
        final_config_dict[config_label] = slsqp_mfa_config
    return final_config_dict, information_dict
