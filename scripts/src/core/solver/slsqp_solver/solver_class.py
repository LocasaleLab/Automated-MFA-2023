from ..base_class import BaseSolver, BaseRecorder
from ..solver_construction_functions.common_construct_functions import right_side_array_constructor
from ...common.packages import np, optimize
from ...common.classes import OptionDict
from ...common.config import CoreConstants, ParamName

from .optimizer_generator_functions \
    import optimized_function_with_loss_generator_pure_python, combined_function_generator_pure_python


def matrix_constraint(matrix, right_side_vector):
    """
    A @ x - b ==/>= 0
    :param matrix:
    :param right_side_vector:
    :return:
    """
    minus_right_side_vector = -right_side_vector
    con_func = eq_func_constructor(matrix, minus_right_side_vector)
    con_func_jacob = eq_func_jacob_constructor(matrix, minus_right_side_vector)
    return con_func, con_func_jacob


def construct_constraint(
        flux_eq_constraint_matrix, flux_eq_constraint_right_side_vector, constraint_type='eq'):
    eq_func, eq_func_jacob = matrix_constraint(
        flux_eq_constraint_matrix, flux_eq_constraint_right_side_vector)
    if constraint_type not in ['eq', 'ineq']:
        raise ValueError("Constraint type should only be 'eq' or 'ineq'. ")
    eq_cons = {'type': constraint_type, 'fun': eq_func, 'jac': eq_func_jacob}
    return eq_cons


def eq_func_constructor(flux_constraint_matrix, flux_constraint_right_side_vector):
    def eq_func(complete_vector):
        result = flux_constraint_matrix @ complete_vector.reshape([-1, 1]) + \
                 flux_constraint_right_side_vector.reshape([-1, 1])
        return result.reshape([-1])

    return eq_func


def eq_func_jacob_constructor(flux_constraint_matrix, flux_constraint_right_side_vector):
    def eq_func_jacob(complete_vector):
        return flux_constraint_matrix

    return eq_func_jacob


def default_optimizer_options(_solver_option_dict):
    loss_type = _solver_option_dict.get_option(ParamName.loss_type, ParamName.cross_entropy_loss)
    embedding_obj = _solver_option_dict.get_option(ParamName.slsqp_embedding_obj, False)
    tolerance = _solver_option_dict.get_option(ParamName.slsqp_tolerance, 1e-9)
    max_iter = _solver_option_dict.get_option(ParamName.slsqp_max_iter, 500)
    return loss_type, embedding_obj, tolerance, max_iter


class SLSQPSolver(BaseSolver):
    def __new__(
            cls, base_solver: BaseSolver, solver_option_dict=None):
        base_solver.__class__ = cls
        return base_solver

    def __init__(self, base_solver: BaseSolver, solver_option_dict=None):
        if solver_option_dict is None:
            solver_option_dict = OptionDict()
        loss_type, embedding_obj, tolerance, max_iter = default_optimizer_options(solver_option_dict)
        self.solver_option_dict.merge(solver_option_dict)

        self.recorder = BaseRecorder(solver_option_dict)
        self.cross_entropy_jacobi_func = None
        self.constraint_list = []
        self.bounds = []
        self.dynamic_default_value = 0

        self.tolerance = tolerance
        self.max_iter = max_iter

        self.loss_type = loss_type
        self.embedding_obj = embedding_obj

    def _construct_bounds(self):
        self.bounds = optimize.Bounds(self.min_bound_vector, self.max_bound_vector)

    def _initialize_constraint(self):
        complete_right_side_array, dynamic_constraint_index_dict = right_side_array_constructor(
            self.complete_right_side_list, self.dynamic_default_value)
        self.complete_right_side_array = complete_right_side_array
        self.dynamic_constraint_index_dict = dynamic_constraint_index_dict
        self._set_dynamic_constraint = len(dynamic_constraint_index_dict) == 0
        eq_cons = construct_constraint(
            self.complete_flux_constraint_matrix, complete_right_side_array)
        self.constraint_list.append(eq_cons)
        self._construct_bounds()

    def _construct_mid_obj_func(self):
        (
            loss_func_calculation_func, mid_prediction_func, all_target_metabolite_mid_prediction_func,
            target_mid_data_dict, emu_name_experimental_name_dict
        ) = optimized_function_with_loss_generator_pure_python(
            self.emu_mid_equation_dict, self.flux_name_index_dict, self.input_emu_data_dict,
            self.experimental_mid_data_obj_dict, self.nested_mix_equation_dict, self.mix_ratio_multiplier,
            self.all_target_metabolite_name_carbon_num_dict, self.loss_type)
        self.objective_func = loss_func_calculation_func
        self.target_mid_dict_prediction_func = mid_prediction_func
        self.all_target_metabolite_mid_prediction_func = all_target_metabolite_mid_prediction_func
        self.target_experimental_mid_data_dict = target_mid_data_dict
        self.emu_name_experimental_name_dict = emu_name_experimental_name_dict

    def _construct_embedding_obj_func(self, target_flux_vector):
        self.objective_func = lambda flux_vector: np.sum(np.square(target_flux_vector - flux_vector))

    def set_right_side_vector(self, dynamic_flux_value_dict):
        super(SLSQPSolver, self).set_right_side_vector(dynamic_flux_value_dict)
        self.base_lp_sampler.set_right_side_vector(dynamic_flux_value_dict)
        target_vector = self.complete_right_side_array
        for flux_name, flux_value in dynamic_flux_value_dict.items():
            target_vector[self.dynamic_constraint_index_dict[flux_name]] = flux_value

    def initialize_solver(self, target_flux_vector=None):
        super(SLSQPSolver, self).initialize_solver()
        self._initialize_constraint()
        if self._base_lp:
            self._initialize_base_lp_sampler()
        self._set_dynamic_constraint = len(self.dynamic_constraint_index_dict) == 0
        if self.embedding_obj:
            if target_flux_vector is None:
                raise ValueError('Target flux vector must be assigned for embedding objective function')
            self._construct_embedding_obj_func(target_flux_vector)
        else:
            self._construct_mid_obj_func()
        print('SLSQP Solver initialized')

    def obj_eval(self, flux_vector):
        super(SLSQPSolver, self).obj_eval(flux_vector)
        return self.objective_func(flux_vector)

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
            self.objective_func, initial_vector, method='SLSQP', jac=self.cross_entropy_jacobi_func,
            constraints=self.constraint_list, bounds=self.bounds,
            options={'ftol': self.tolerance, 'maxiter': self.max_iter, 'disp': self.verbose})
        if current_result.status == CoreConstants.success_code or \
                current_result.status == CoreConstants.limit_reached_code:
            success_optimization = True
        else:
            success_optimization = False
        self.recorder.final(None, None)
        return current_result.x, current_result.fun, success_optimization

    def predict(self, flux_vector):
        super(SLSQPSolver, self).predict(flux_vector)
        return self.target_mid_dict_prediction_func(flux_vector)

    def predict_all_target(self, flux_vector):
        return self.all_target_metabolite_mid_prediction_func(flux_vector)


class SLSQPGroupSolver(SLSQPSolver):
    def __init__(self, base_solver: BaseSolver, solver_option_dict=None):
        def default_optimizer_options(_solver_option_dict):
            _ratio_dict_to_objective_func = _solver_option_dict.get_option(
                ParamName.slsqp_ratio_dict_to_objective_func)
            _list_of_case_name = _solver_option_dict.get_option(ParamName.slsqp_list_of_case_name)
            return _ratio_dict_to_objective_func, _list_of_case_name

        solver_option_dict.update({ParamName.slsqp_embedding_obj: False})
        super(SLSQPGroupSolver, self).__init__(base_solver, solver_option_dict)

        ratio_dict_to_objective_func, list_of_case_name = default_optimizer_options(solver_option_dict)

        self.ratio_dict_to_objective_func = ratio_dict_to_objective_func
        self.list_of_case_name = list_of_case_name

    # def __init__(
    #         self, flux_name_index_dict, complete_emu_dim_dict, complete_flux_constraint_matrix,
    #         complete_right_side_list, min_bound_vector, max_bound_vector, projection_matrix,
    #         emu_mid_equation_dict,
    #
    #         # Following parameters are all dicts of original parameters, with a specific name as in
    #         # list_of_case_name
    #         input_emu_data_dict, experimental_mid_data_obj_dict,
    #         nested_mix_equation_dict, mix_ratio_multiplier, all_target_metabolite_name_carbon_num_dict=None,
    #         verbose=False, solver_option_dict=None):
    #     def default_optimizer_options(_solver_option_dict):
    #         _ratio_dict_to_objective_func = _solver_option_dict.get_option(
    #             ParamName.slsqp_ratio_dict_to_objective_func)
    #         _list_of_case_name = _solver_option_dict.get_option(ParamName.slsqp_list_of_case_name)
    #         return _ratio_dict_to_objective_func, _list_of_case_name
    #
    #     solver_option_dict.update({ParamName.slsqp_embedding_obj: False})
    #     super(SLSQPGroupSolver, self).__init__(
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
        loss_func_calculation_func_dict = {}
        mid_prediction_func_dict = {}
        all_target_metabolite_mid_prediction_func_dict = {}
        target_mid_data_nested_dict = {}
        emu_name_experimental_name_nested_dict = {}
        for case_name in self.list_of_case_name:
            (
                loss_func_calculation_func, mid_prediction_func, all_target_metabolite_mid_prediction_func,
                target_mid_data_dict, emu_name_experimental_name_dict
            ) = optimized_function_with_loss_generator_pure_python(
                self.emu_mid_equation_dict, self.flux_name_index_dict,
                self.input_emu_data_dict[case_name], self.experimental_mid_data_obj_dict[case_name],
                self.nested_mix_equation_dict[case_name], self.mix_ratio_multiplier,
                self.all_target_metabolite_name_carbon_num_dict, self.loss_type)
            loss_func_calculation_func_dict[case_name] = loss_func_calculation_func
            mid_prediction_func_dict[case_name] = mid_prediction_func
            all_target_metabolite_mid_prediction_func_dict[case_name] = all_target_metabolite_mid_prediction_func
            target_mid_data_nested_dict[case_name] = target_mid_data_dict
            emu_name_experimental_name_nested_dict[case_name] = emu_name_experimental_name_dict
        (
            combined_loss_func_calculation, combined_mid_prediction,
            combined_all_target_metabolite_mid_prediction, combined_target_mid_data_dict,
            combined_emu_name_experimental_name_dict) = combined_function_generator_pure_python(
            loss_func_calculation_func_dict, mid_prediction_func_dict, all_target_metabolite_mid_prediction_func_dict,
            target_mid_data_nested_dict, emu_name_experimental_name_nested_dict,
            self.ratio_dict_to_objective_func, self.list_of_case_name)

        self.objective_func = combined_loss_func_calculation
        self.target_mid_dict_prediction_func = combined_mid_prediction
        self.target_experimental_mid_data_dict = combined_target_mid_data_dict
        self.emu_name_experimental_name_dict = combined_emu_name_experimental_name_dict
        self.all_target_metabolite_mid_prediction_func = combined_all_target_metabolite_mid_prediction

    def _construct_embedding_obj_func(self, target_flux_vector):
        raise AttributeError('The embedding obj should not be called in this function')

