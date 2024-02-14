from .packages import np

from ..core.solver.solver_construction_functions.solver_constructor import specific_solver_constructor, \
    base_solver_constructor, common_solver_constructor
from ..core.sampler.np_sampler.sampler_class import OptGpSampler

random_seed = np.random.default_rng(4536251)


class Keywords(object):
    thread_num_constraint = 'thread_num_constraint'
    each_process_optimization_num = 'each_process_optimization_num'
    max_optimization_each_generation = 'max_optimization_each_generation'
    predefined_initial_solution_matrix = 'predefined_initial_solution_matrix'
    parallel_test = 'parallel_test'
    processes_num = 'processes_num'
    unoptimized = 'unoptimized'
