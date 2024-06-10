from ..common.config import ParamName
from ..sampler.base_class import LPSampler
from ..common.packages import time, np, copy
from ..common.classes import OptionDict
from .solver_construction_functions.common_construct_functions import right_side_array_constructor
from .solver_construction_functions.solver_memo import SolverMemo


class BaseSolver(object):
    def __init__(
            self, flux_name_index_dict, complete_emu_dim_dict, complete_flux_constraint_matrix,
            complete_right_side_list, min_bound_vector, max_bound_vector, projection_matrix=None,
            emu_mid_equation_dict=None, emu_name_dependency_dict=None, complete_emu_obj_index_dict=None,
            input_emu_data_dict=None, experimental_mid_data_obj_dict=None,
            nested_mix_equation_dict=None, mix_ratio_multiplier=None, all_target_metabolite_name_carbon_num_dict=None,
            verbose=False, solver_option_dict=None, solver_memo: SolverMemo = None, name=None):
        if solver_option_dict is None:
            solver_option_dict = OptionDict()
        base_lp = solver_option_dict.get_option(ParamName.base_lp, True)
        variable_num = len(flux_name_index_dict)
        if not (
                variable_num == complete_flux_constraint_matrix.shape[1] == len(min_bound_vector)
                == len(max_bound_vector) == projection_matrix.shape[1] and
                complete_flux_constraint_matrix.shape[0] == len(complete_right_side_list)):
            raise ValueError()
        self.variable_num = variable_num
        self.solver_option_dict = solver_option_dict

        self.flux_name_index_dict = flux_name_index_dict
        self.complete_emu_dim_dict = complete_emu_dim_dict
        self.complete_flux_constraint_matrix = complete_flux_constraint_matrix
        self.complete_right_side_list = complete_right_side_list
        self.projection_matrix = projection_matrix
        self.min_bound_vector = min_bound_vector
        self.max_bound_vector = max_bound_vector

        self.emu_mid_equation_dict = emu_mid_equation_dict
        self.emu_name_dependency_dict = emu_name_dependency_dict
        self.complete_emu_obj_index_dict = complete_emu_obj_index_dict
        self.input_emu_data_dict = input_emu_data_dict
        self.experimental_mid_data_obj_dict = experimental_mid_data_obj_dict
        self.nested_mix_equation_dict = nested_mix_equation_dict
        self.mix_ratio_multiplier = mix_ratio_multiplier
        self.all_target_metabolite_name_carbon_num_dict = all_target_metabolite_name_carbon_num_dict

        self.target_experimental_mid_data_dict = None
        self.emu_name_experimental_name_dict = None

        self.objective_func = None
        self.target_mid_dict_prediction_func = None
        self.all_target_metabolite_mid_prediction_func = None
        self.complete_right_side_array = None
        self.verbose = verbose
        self._base_lp = base_lp
        self.base_lp_sampler = None

        self.dynamic_constraint_index_dict = None
        self._set_dynamic_constraint = False

        self.solver_memo = solver_memo
        self.name = name

    def __copy__(self):
        flux_name_index_dict = dict(self.flux_name_index_dict)
        complete_emu_dim_dict = self.complete_emu_dim_dict.copy()
        complete_flux_constraint_matrix = self.complete_flux_constraint_matrix.copy()
        complete_right_side_list = list(self.complete_right_side_list)
        min_bound_vector = self.min_bound_vector.copy()
        max_bound_vector = self.max_bound_vector.copy()
        projection_matrix = copy.copy(self.projection_matrix)
        emu_mid_equation_dict = copy.copy(self.emu_mid_equation_dict)
        input_emu_data_dict = copy.copy(self.input_emu_data_dict)
        emu_name_dependency_dict = copy.deepcopy(self.emu_name_dependency_dict)
        complete_emu_obj_index_dict = copy.deepcopy(self.complete_emu_obj_index_dict)
        experimental_mid_data_obj_dict = copy.copy(self.experimental_mid_data_obj_dict)
        nested_mix_equation_dict = copy.deepcopy(self.nested_mix_equation_dict)
        all_target_metabolite_name_carbon_num_dict = copy.copy(self.all_target_metabolite_name_carbon_num_dict)
        solver_option_dict = copy.copy(self.solver_option_dict)
        solver_memo = copy.copy(self.solver_memo)
        return BaseSolver(
            flux_name_index_dict=flux_name_index_dict, complete_emu_dim_dict=complete_emu_dim_dict,
            complete_flux_constraint_matrix=complete_flux_constraint_matrix,
            complete_right_side_list=complete_right_side_list, min_bound_vector=min_bound_vector,
            max_bound_vector=max_bound_vector, projection_matrix=projection_matrix,
            emu_mid_equation_dict=emu_mid_equation_dict, emu_name_dependency_dict=emu_name_dependency_dict,
            complete_emu_obj_index_dict=complete_emu_obj_index_dict, input_emu_data_dict=input_emu_data_dict,
            experimental_mid_data_obj_dict=experimental_mid_data_obj_dict,
            nested_mix_equation_dict=nested_mix_equation_dict, mix_ratio_multiplier=self.mix_ratio_multiplier,
            all_target_metabolite_name_carbon_num_dict=all_target_metabolite_name_carbon_num_dict,
            verbose=self.verbose, solver_option_dict=solver_option_dict, solver_memo=solver_memo, name=self.name)

    def _initialize_base_lp_sampler(self):
        if (
                self.complete_flux_constraint_matrix is None or self.complete_right_side_array is None or
                self.min_bound_vector is None or self.max_bound_vector is None):
            raise ValueError('All element for lp sampler required!')
        if not self._set_dynamic_constraint or self.dynamic_constraint_index_dict is None:
            raise ValueError('dynamic_constraint_index_dict has not been initialized!')
        self.base_lp_sampler = LPSampler(
            self.variable_num, self.complete_flux_constraint_matrix, self.complete_right_side_array,
            smaller_eq_matrix=None, smaller_eq_right_side_vector=None,
            min_value_vector=self.min_bound_vector, max_value_vector=self.max_bound_vector,
            dynamic_constraint_index_dict=self.dynamic_constraint_index_dict, verbose=self.verbose)

    def set_right_side_vector(self, dynamic_flux_value_dict):
        self._set_dynamic_constraint = True

    def _initialize_constraint(self):
        complete_right_side_array, dynamic_constraint_index_dict = right_side_array_constructor(
            self.complete_right_side_list, dynamic_default_value=0)
        self.complete_right_side_array = complete_right_side_array
        self.dynamic_constraint_index_dict = dynamic_constraint_index_dict
        self._set_dynamic_constraint = len(dynamic_constraint_index_dict) == 0

    @staticmethod
    def _check_valid(initial_vector, lb, ub):
        if np.any(initial_vector < lb) or np.any(initial_vector > ub):
            raise ValueError('Initial vector does not fit bounds!')

    def base_initialize_solver(self):
        self._initialize_constraint()
        if self._base_lp:
            self._initialize_base_lp_sampler()

    def initialize_solver(self, *args, **kwargs):
        pass

    def obj_eval(self, flux_vector):
        if self.objective_func is None:
            raise ValueError('No objective function!')
        pass

    def solve(self, initial_vector=None):
        if self.objective_func is None:
            raise ValueError('No objective function!')
        if not self._set_dynamic_constraint:
            raise ValueError('Dynamic flux value should be set first!')
        pass

    def predict(self, flux_vector):
        if self.target_mid_dict_prediction_func is None:
            raise ValueError('No prediction function!')
        pass


class BaseRecorder(object):
    def __init__(self, debug_options=None):
        if debug_options is None:
            debug_options = OptionDict()
        self.running_time = 0
        self.start_time = 0
        self.end_time = 0
        self.debug = debug_options.get_option(ParamName.debug, False)
        self.stop = False

    def start(self, flux_tensor=None, step=None):
        self.start_time = time.time()

    def step(self, flux_tensor=None, step=None):
        pass

    def final(self, flux_tensor=None, step=None):
        self.end_time = time.time()
        self.running_time = self.end_time - self.start_time



