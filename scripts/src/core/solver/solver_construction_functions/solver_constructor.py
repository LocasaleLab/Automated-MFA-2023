from ...common.config import ParamName
from ...common.classes import MFAConfig

from ...model.model_class import MFAModel
from ...data.data_class import MFAData
from ..base_class import BaseSolver

from .common_construct_functions import data_verification, input_emu_mid_generator, \
    flux_balance_horizontal_extend, mix_ratio_balance_constraint_constructor, \
    constant_flux_constraint_list_constructor, matrix_and_right_side_combine_and_projection_matrix, \
    flux_bounds_constructor, mixing_equation_constructor
from .solver_memo import solver_memo_constructor


def base_solver_constructor(
        mfa_model: MFAModel,
        mfa_data: MFAData,
        mfa_config: MFAConfig,
        verbose=False, name=None,
):
    combined_data = mfa_data.combined_data
    mix_ratio_multiplier = mfa_config.mix_ratio_multiplier

    if combined_data:
        list_of_case_name = mfa_data.list_of_case_name
        input_emu_data_dict = {}
        for case_name, current_input_metabolite_obj_data_dict in mfa_data.input_metabolite_obj_data_dict.items():
            input_emu_data_dict[case_name] = input_emu_mid_generator(
                current_input_metabolite_obj_data_dict, mfa_model.input_emu_dict)
        mfa_config.combined_data = True
        mfa_config.solver_config_dict.update({
            ParamName.slsqp_ratio_dict_to_objective_func: mfa_data.ratio_dict_to_objective_func,
            ParamName.slsqp_list_of_case_name: mfa_data.list_of_case_name
        })
        for case_name in list_of_case_name:
            current_experimental_mid_data_obj_dict = mfa_data.experimental_mid_data_obj_dict[case_name]
            data_verification(
                current_experimental_mid_data_obj_dict,
                mfa_model.bare_metabolite_dim_dict,
                mfa_model.model_metabolite_to_standard_name_dict)
    else:
        input_emu_data_dict = input_emu_mid_generator(
            mfa_data.input_metabolite_obj_data_dict, mfa_model.input_emu_dict)
        data_verification(
            mfa_data.experimental_mid_data_obj_dict,
            mfa_model.bare_metabolite_dim_dict,
            mfa_model.model_metabolite_to_standard_name_dict)
        list_of_case_name = None

    (
        nested_mix_equation_dict, mix_ratio_name_index_dict, mix_ratio_balance_list,
        updated_specific_flux_range_dict) = mixing_equation_constructor(
        mfa_data.experimental_mid_data_obj_dict,
        mfa_model.complete_tissue_compartment_metabolite_dict,
        mfa_model.model_metabolite_to_standard_name_dict,
        mfa_model.metabolite_bare_metabolite_name_dict,
        mfa_config.specific_flux_range_dict, mfa_config.common_mix_ratio_range, mix_ratio_multiplier,
        list_of_case_name)

    all_target_metabolite_name_carbon_num_dict = {
        target_metabolite_name: mfa_model.bare_metabolite_dim_dict[
            mfa_model.metabolite_bare_metabolite_name_dict[target_metabolite_name]]
        for target_metabolite_name in mfa_model.all_target_metabolite_name_set}

    updated_flux_name_index_dict = dict(mfa_model.flux_name_index_dict)
    previous_flux_size = len(updated_flux_name_index_dict)
    for mix_ratio_name, index in mix_ratio_name_index_dict.items():
        updated_flux_name_index_dict[mix_ratio_name] = previous_flux_size + index

    flux_balance_matrix = flux_balance_horizontal_extend(
        mfa_model.flux_balance_matrix, len(mix_ratio_name_index_dict))
    mix_ratio_balance_matrix_list, mix_ratio_balance_right_side_list = mix_ratio_balance_constraint_constructor(
        mix_ratio_balance_list, updated_flux_name_index_dict, mix_ratio_multiplier)
    constant_flux_multiply_array_list, constant_flux_right_side_list = constant_flux_constraint_list_constructor(
        mfa_config.dynamic_constant_flux_list, mfa_config.preset_constant_flux_value_dict, updated_flux_name_index_dict)
    (
        complete_flux_constraint_matrix, projection_matrix,
        complete_right_side_list) = matrix_and_right_side_combine_and_projection_matrix(
        flux_balance_matrix, constant_flux_multiply_array_list, mix_ratio_balance_matrix_list,
        mfa_model.flux_balance_right_side_vector, constant_flux_right_side_list, mix_ratio_balance_right_side_list,
        eps_for_computation=mfa_config.eps_for_computation)
    min_bound_vector, max_bound_vector = flux_bounds_constructor(
        mfa_config.common_flux_range, mfa_model.composite_reaction_dict,
        updated_specific_flux_range_dict, updated_flux_name_index_dict)
    solver_memo = solver_memo_constructor(
        name, nested_mix_equation_dict, mix_ratio_balance_list,
        mfa_model, mfa_data, mfa_config, combined_data=combined_data)
    base_solver = BaseSolver(
        updated_flux_name_index_dict, mfa_model.complete_emu_dim_dict, complete_flux_constraint_matrix,
        complete_right_side_list, min_bound_vector, max_bound_vector, projection_matrix=projection_matrix,
        emu_mid_equation_dict=mfa_model.emu_mid_equation_dict,
        emu_name_dependency_dict=mfa_model.emu_name_dependency_dict,
        complete_emu_obj_index_dict=mfa_model.complete_emu_obj_index_dict, input_emu_data_dict=input_emu_data_dict,
        experimental_mid_data_obj_dict=mfa_data.experimental_mid_data_obj_dict,
        nested_mix_equation_dict=nested_mix_equation_dict, mix_ratio_multiplier=mix_ratio_multiplier,
        all_target_metabolite_name_carbon_num_dict=all_target_metabolite_name_carbon_num_dict,
        verbose=verbose, solver_option_dict=mfa_config.solver_config_dict, solver_memo=solver_memo, name=name)
    return base_solver


def solver_converter(previous_solver: BaseSolver, new_solver_constructor, new_solver_option_dict, copy=False):
    if copy:
        previous_solver = previous_solver.__copy__()
    new_solver = new_solver_constructor(previous_solver, solver_option_dict=new_solver_option_dict)
    return new_solver


def specific_solver_constructor(
        base_solver: BaseSolver,
        mfa_config: MFAConfig
):
    if mfa_config.solver_type == ParamName.slsqp_solver:
        from ..slsqp_solver.solver_class import SLSQPSolver, SLSQPGroupSolver
        if mfa_config.combined_data:
            solver_constructor = SLSQPGroupSolver
        else:
            solver_constructor = SLSQPSolver
    elif mfa_config.solver_type == ParamName.slsqp_numba_solver or \
            mfa_config.solver_type == ParamName.slsqp_numba_python_solver or \
            mfa_config.solver_type == ParamName.slsqp_numba_nopython_solver:
        from ..slsqp_numba_solver.solver_class import SLSQPNumbaSolver, SLSQPNumbaGroupSolver
        if mfa_config.combined_data:
            solver_constructor = SLSQPNumbaGroupSolver
        else:
            solver_constructor = SLSQPNumbaSolver
        if mfa_config.solver_type == ParamName.slsqp_numba_python_solver:
            mfa_config.solver_config_dict[ParamName.numba_nopython] = False
    elif mfa_config.solver_type == ParamName.torch_solver:
        from ..pytorch_solver.solver_class import TorchSolver
        solver_constructor = TorchSolver
    elif mfa_config.solver_type == ParamName.tf2_solver:
        from ..tf2_solver.solver_class import TF2Solver
        solver_constructor = TF2Solver
    elif mfa_config.solver_type == ParamName.tf2_sampler_solver:
        from ..tf2_sample_solver.solver_class import TF2SampleSolver
        solver_constructor = TF2SampleSolver
    elif mfa_config.solver_type == ParamName.tf2_slsqp_solver:
        from ..tf2_slsqp_solver.solver_class import TF2SLSQPSolver
        solver_constructor = TF2SLSQPSolver
    elif mfa_config.solver_type == ParamName.tf2_sa_solver:
        from ..tf2_sa_solver.solver_class import TF2SASolver
        solver_constructor = TF2SASolver
    else:
        raise ValueError()
    if isinstance(base_solver, solver_constructor):
        return base_solver
    else:
        solver_obj = solver_converter(base_solver, solver_constructor, mfa_config.solver_config_dict)
        solver_obj.initialize_solver()
        return solver_obj


def common_solver_constructor(
        mfa_model: MFAModel,
        mfa_data: MFAData,
        mfa_config: MFAConfig,
        verbose=False, name=None
):
    base_solver = base_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=verbose, name=name)
    solver_obj = specific_solver_constructor(base_solver, mfa_config)
    return solver_obj
