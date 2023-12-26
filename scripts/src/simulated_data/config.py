from scripts.src.core.common.classes import MFAConfig, OptionDict
from scripts.src.core.common.config import ParamName

from ..common.config import Direct as CommonDirect


slsqp_solver_config_dict = OptionDict({
    # ParamName.loss_type: ParameterName.mean_squared_loss,
    ParamName.loss_type: ParamName.cross_entropy_loss,
})
slsqp_mfa_config = MFAConfig(
    common_flux_range=(1, 1000), specific_flux_range_dict={}, dynamic_constant_flux_list=[],
    preset_constant_flux_value_dict={'GLC_input': 200},
    common_mix_ratio_range=(0.05, 0.95), mix_ratio_multiplier=100,
    solver_type=ParamName.slsqp_solver, solver_config_dict=slsqp_solver_config_dict)

