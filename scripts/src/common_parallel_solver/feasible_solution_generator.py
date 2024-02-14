from .packages import np, mp
from .config import OptGpSampler


def universal_feasible_solution_generator(solver_obj, target_size):
    if target_size < 500:
        return simple_feasible_solution_generator(solver_obj, target_size)
    elif target_size < 10000:
        return complicated_feasible_solution_generator(solver_obj, target_size)
    else:
        return complicated_feasible_solution_generator(solver_obj, target_size)


def optimized_feasible_solution_generator_sampler(solver_obj, target_size, tf2_sampler_option_dict):
    from scripts.src.core.solver.tf2_sample_solver.solver_class import TF2SampleSolver
    from scripts.src.core.solver.solver_construction_functions.solver_constructor import solver_converter
    tf2_sample_solver = solver_converter(solver_obj, TF2SampleSolver, tf2_sampler_option_dict)
    tf2_sample_solver.initialize_solver()
    final_solution, final_obj = tf2_sample_solver.solve(target_size)
    print(final_obj)
    return final_solution


def optimized_feasible_solution_generator_sa(solver_obj, target_size, tf2_sa_option_dict):
    from scripts.src.core.solver.tf2_sa_solver.solver_class import TF2SASolver
    from scripts.src.core.solver.solver_construction_functions.solver_constructor import solver_converter
    tf2_sa_solver = solver_converter(solver_obj, TF2SASolver, tf2_sa_option_dict)
    tf2_sa_solver.initialize_solver()
    final_solution, final_obj = tf2_sa_solver.solve(target_size)
    print(final_obj)
    return final_solution


def simple_feasible_solution_generator(base_solver_obj, target_size):
    maximal_trial_num = 10 * target_size
    count = 0
    initial_vector_list = []
    while len(initial_vector_list) < target_size:
        initial_vector = base_solver_obj.base_lp_sampler.sample()
        if initial_vector is not None:
            initial_vector_list.append(initial_vector)
        count += 1
        if count > maximal_trial_num:
            return None
    return np.array(initial_vector_list)


def complicated_feasible_solution_generator(solver_obj, target_size, thinning=30):
    result_vector_list = []
    single_denovo_generator(
        solver_obj.variable_num, solver_obj.complete_flux_constraint_matrix,
        solver_obj.complete_right_side_array, solver_obj.min_bound_vector,
        solver_obj.max_bound_vector, solver_obj.projection_matrix, thinning, target_size, result_vector_list)
    return np.array(result_vector_list)


def single_denovo_generator(
        variable_num, complete_flux_constraint_matrix, complete_right_side_array,
        min_bound_vector, max_bound_vector, projection_matrix, thinning, single_thread_size,
        final_result_list):
    sampler = OptGpSampler(
        variable_num, complete_flux_constraint_matrix,
        complete_right_side_array, smaller_eq_matrix=None,
        smaller_eq_right_side_vector=None, min_value_vector=min_bound_vector,
        max_value_vector=max_bound_vector, projection_matrix=projection_matrix,
        thinning=thinning)
    sampled_result_list = sampler.sample(single_thread_size)
    final_result_list.extend(sampled_result_list)


def parallel_denovo_generator(solver_obj, target_size, parallel_size, thinning):
    single_thread_size_list = [int(target_size / parallel_size)] * parallel_size
    for index in range(target_size % parallel_size):
        single_thread_size_list[index] += 1
    with mp.Manager() as manager:
        manager_result_list = manager.list()
        p_list = []
        for p_index in range(parallel_size):
            current_single_thread_size = single_thread_size_list[p_index]
            p = mp.Process(target=single_denovo_generator, args=(
                solver_obj.variable_num, solver_obj.complete_flux_constraint_matrix,
                solver_obj.complete_right_side_array, solver_obj.min_bound_vector,
                solver_obj.max_bound_vector, solver_obj.projection_matrix, thinning,
                current_single_thread_size, manager_result_list))
            p_list.append(p)
            p.start()
        for p in p_list:
            p.join()
        final_result_matrix = np.array(manager_result_list)
    return final_result_matrix


# def generate_and_save_feasible_solutions(solver_obj, target_size, result_storage_path=None):
#     parallel_size = 4
#     thinning = 30
#     minimal_sample_size = 100
#     if target_size < minimal_sample_size:
#         sample_size = minimal_sample_size
#     else:
#         sample_size = target_size
#     current_result_matrix = parallel_denovo_generator(solver_obj, sample_size, parallel_size, thinning)
#     if result_storage_path is not None:
#         check_and_mkdir_of_direct(result_storage_path, file_path=True)
#         npz_save(result_storage_path, input_matrix=current_result_matrix)
#     if target_size < sample_size:
#         current_result_matrix = current_result_matrix[:target_size, :]
#     return current_result_matrix


# def feasible_flux_input_generator(solver_obj, target_size, result_storage_path, refresh=False):
#     import os
#     if not os.path.isfile(result_storage_path) or refresh:
#         input_matrix = generate_and_save_feasible_solutions(solver_obj, target_size, result_storage_path)
#     else:
#         input_matrix = npz_load(result_storage_path, 'input_matrix')
#         if input_matrix.shape[0] < target_size:
#             input_matrix = generate_and_save_feasible_solutions(solver_obj, target_size, result_storage_path)
#         elif input_matrix.shape[0] > target_size:
#             input_matrix = input_matrix[:target_size, :]
#     return input_matrix


def flux_vector_tensor_generator(raw_solution_flux_input, batch_size, flux_input_tensor_func):
    total_batch_num = len(raw_solution_flux_input)
    current_batch_num = 0
    while current_batch_num < total_batch_num:
        current_array = raw_solution_flux_input[current_batch_num:current_batch_num + batch_size, :]
        current_num = current_array.shape[0]
        if current_num < batch_size:
            current_array = np.append(current_array, raw_solution_flux_input[:batch_size-current_num, :], axis=0)
        current_tensor = flux_input_tensor_func(current_array)
        current_batch_num += batch_size
        yield current_tensor, current_num
