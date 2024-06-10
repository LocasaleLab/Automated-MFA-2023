from ...common.packages import np, optimize, os
from ...common.classes import OptionDict
from ...common.config import CoreConstants, ParamName

from ..slsqp_solver.solver_class import SLSQPSolver


class SLSQPNumbaSolver(SLSQPSolver):
    def __init__(self, base_solver, solver_option_dict=None):
        if solver_option_dict is None:
            solver_option_dict = OptionDict()
        nopython = solver_option_dict.get_option(ParamName.numba_nopython, True)
        if os is not None:
            # os.environ['NUMBA_PARFOR_MAX_TUPLE_SIZE'] = '500'
            os.environ['NUMBA_NUM_THREADS'] = '5'
        super(SLSQPNumbaSolver, self).__init__(base_solver, solver_option_dict)

        self.all_target_emu_index_dict = None
        self.all_target_emu_name_metabolite_name_dict = None
        self.objective_function_args = None
        if nopython:
            from . import nopython_initializer_optimizer_functions
            self.optimizer_functions = nopython_initializer_optimizer_functions
        else:
            from . import python_initializer_optimizer_functions
            self.optimizer_functions = python_initializer_optimizer_functions
        self.nopython = nopython

    def _construct_mid_obj_func(self):
        (
            self.objective_function_args, self.all_target_emu_index_dict,
            self.all_target_emu_name_metabolite_name_dict, self.target_experimental_mid_data_dict,
            self.emu_name_experimental_name_dict) = self.optimizer_functions.solver_initializer(
            self.emu_mid_equation_dict, self.flux_name_index_dict, self.input_emu_data_dict,
            self.experimental_mid_data_obj_dict, self.nested_mix_equation_dict,
            self.all_target_metabolite_name_carbon_num_dict, self.loss_type, self.mix_ratio_multiplier)
        self.objective_func = \
            self.optimizer_functions.solver_objective_func
        self.target_mid_dict_prediction_func = \
            self.optimizer_functions.solver_target_mid_dict_prediction_func
        self.all_target_metabolite_mid_prediction_func = \
            self.optimizer_functions.solver_all_target_metabolite_mid_prediction_func

    def initialize_solver(self, target_flux_vector=None):
        super(SLSQPSolver, self).initialize_solver()
        self._initialize_constraint()
        if self._base_lp:
            self._initialize_base_lp_sampler()
        self._set_dynamic_constraint = len(self.dynamic_constraint_index_dict) == 0
        self._construct_mid_obj_func()
        print('SLSQP Solver ({} mode) initialized'.format('Numba nopython' if self.nopython else 'python'))

    def solve(self, initial_vector=None):
        super(SLSQPSolver, self).solve(initial_vector)
        if initial_vector is None:
            if not self._base_lp:
                raise ValueError('No LP initializer!')
            initial_vector = self.base_lp_sampler.sample()
            if initial_vector is None:
                raise ValueError('Cannot find a valid initial solution!')
        if self.verbose:
            print('Initial loss is: {}'.format(self.obj_eval(initial_vector)))
        self._check_valid(initial_vector, self.bounds.lb, self.bounds.ub)
        self.recorder.start(None, None)
        current_result = optimize.minimize(
            self.objective_func, initial_vector, args=self.objective_function_args,
            method='SLSQP', jac=self.cross_entropy_jacobi_func,
            constraints=self.constraint_list, bounds=self.bounds,
            options={'ftol': self.tolerance, 'maxiter': self.max_iter, 'disp': self.verbose})
        if current_result.status == CoreConstants.success_code or \
                current_result.status == CoreConstants.limit_reached_code:
            success_optimization = True
        else:
            success_optimization = False
        self.recorder.final(None, None)
        return current_result.x, current_result.fun, success_optimization

    def obj_eval(self, flux_vector):
        super(SLSQPSolver, self).obj_eval(flux_vector)
        return self.objective_func(flux_vector, *self.objective_function_args)

    def predict(self, flux_vector):
        super(SLSQPSolver, self).predict(flux_vector)
        return self.target_mid_dict_prediction_func(
            flux_vector, *self.objective_function_args)

    def predict_all_target(self, flux_vector):
        return self.all_target_metabolite_mid_prediction_func(
            flux_vector, self.all_target_emu_index_dict, self.all_target_emu_name_metabolite_name_dict,
            *self.objective_function_args)


class SLSQPNumbaGroupSolver(SLSQPNumbaSolver):
    def __init__(self, base_solver, solver_option_dict=None):
        def default_optimizer_options(_solver_option_dict):
            _ratio_dict_to_objective_func = _solver_option_dict.get_option(
                ParamName.slsqp_ratio_dict_to_objective_func)
            _list_of_case_name = _solver_option_dict.get_option(ParamName.slsqp_list_of_case_name)
            return _ratio_dict_to_objective_func, _list_of_case_name

        solver_option_dict.update({ParamName.slsqp_embedding_obj: False})
        super(SLSQPNumbaGroupSolver, self).__init__(base_solver, solver_option_dict)

        ratio_dict_to_objective_func, list_of_case_name = default_optimizer_options(solver_option_dict)

        self.ratio_dict_to_objective_func = ratio_dict_to_objective_func
        self.list_of_case_name = list_of_case_name

    # def __init__(
    #         self, flux_name_index_dict, complete_emu_dim_dict, complete_flux_constraint_matrix,
    #         complete_right_side_list, min_bound_vector, max_bound_vector, projection_matrix,
    #         emu_mid_equation_dict,
    #         #############################
    #         # These parameters are all dicts of original parameters, with a specific name as in
    #         # list_of_case_name
    #         input_emu_data_dict, experimental_mid_data_obj_dict, nested_mix_equation_dict,
    #         #################################
    #         mix_ratio_multiplier, all_target_metabolite_name_carbon_num_dict=None,
    #         verbose=False, solver_option_dict=None):
    #     def default_optimizer_options(_solver_option_dict):
    #         _ratio_dict_to_objective_func = _solver_option_dict.get_option(
    #             ParamName.slsqp_ratio_dict_to_objective_func)
    #         _list_of_case_name = _solver_option_dict.get_option(ParamName.slsqp_list_of_case_name)
    #         return _ratio_dict_to_objective_func, _list_of_case_name
    #
    #     solver_option_dict.update({ParamName.slsqp_embedding_obj: False})
    #     super(SLSQPNumbaGroupSolver, self).__init__(
    #         flux_name_index_dict, complete_emu_dim_dict,
    #         complete_flux_constraint_matrix, complete_right_side_list,
    #         min_bound_vector, max_bound_vector, projection_matrix,
    #         emu_mid_equation_dict, input_emu_data_dict, experimental_mid_data_obj_dict,
    #         nested_mix_equation_dict, mix_ratio_multiplier, all_target_metabolite_name_carbon_num_dict,
    #         verbose=verbose, solver_option_dict=solver_option_dict)
    #
    #     ratio_dict_to_objective_func, list_of_case_name = default_optimizer_options(solver_option_dict)
    #
    #     self.ratio_dict_to_objective_func = ratio_dict_to_objective_func
    #     self.list_of_case_name = list_of_case_name

    def _construct_mid_obj_func(self):
        from .group_optimizer_functions import solver_objective_func_generator, \
            solver_target_mid_dict_prediction_func_generator, \
            solver_all_target_metabolite_mid_prediction_func_generator, group_emu_name_constructor
        complete_target_experimental_mid_data_dict = {}
        complete_emu_name_experimental_name_dict = {}
        ratio_list_to_objective_func = []
        objective_function_args_list = []
        all_target_emu_index_dict_list = []
        all_target_emu_name_metabolite_name_dict_list = []
        for case_name in self.list_of_case_name:
            (
                objective_function_args, all_target_emu_index_dict,
                all_target_emu_name_metabolite_name_dict, target_experimental_mid_data_dict,
                emu_name_experimental_name_dict) = self.optimizer_functions.solver_initializer(
                self.emu_mid_equation_dict, self.flux_name_index_dict, self.input_emu_data_dict[case_name],
                self.experimental_mid_data_obj_dict[case_name], self.nested_mix_equation_dict[case_name],
                self.all_target_metabolite_name_carbon_num_dict, self.loss_type, self.mix_ratio_multiplier)
            ratio_list_to_objective_func.append(self.ratio_dict_to_objective_func[case_name])
            objective_function_args_list.append(objective_function_args)
            all_target_emu_index_dict_list.append(all_target_emu_index_dict)
            all_target_emu_name_metabolite_name_dict_list.append(all_target_emu_name_metabolite_name_dict)
            for emu_name, mid_value in target_experimental_mid_data_dict.items():
                complete_target_experimental_mid_data_dict[
                    group_emu_name_constructor(emu_name, case_name)] = mid_value
            for emu_name, experimental_name in emu_name_experimental_name_dict.items():
                complete_emu_name_experimental_name_dict[
                    group_emu_name_constructor(emu_name, case_name)] = experimental_name

        self.objective_func = solver_objective_func_generator(
            self.optimizer_functions.solver_objective_func, ratio_list_to_objective_func)
        self.target_mid_dict_prediction_func = solver_target_mid_dict_prediction_func_generator(
            self.optimizer_functions.solver_target_mid_dict_prediction_func, self.list_of_case_name)
        self.all_target_metabolite_mid_prediction_func = solver_all_target_metabolite_mid_prediction_func_generator(
            self.optimizer_functions.solver_all_target_metabolite_mid_prediction_func, self.list_of_case_name)
        self.objective_function_args = tuple(objective_function_args_list)
        self.all_target_emu_index_dict = all_target_emu_index_dict_list
        self.all_target_emu_name_metabolite_name_dict = all_target_emu_name_metabolite_name_dict_list
        self.target_experimental_mid_data_dict = complete_target_experimental_mid_data_dict
        self.emu_name_experimental_name_dict = complete_emu_name_experimental_name_dict

    def _construct_embedding_obj_func(self, target_flux_vector):
        raise AttributeError('The embedding obj should not be called in this function')


