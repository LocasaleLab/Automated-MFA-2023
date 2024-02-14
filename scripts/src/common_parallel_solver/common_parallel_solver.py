from .packages import np, mp, tqdm, threadpool_limits
from .config import Keywords, random_seed, specific_solver_constructor, base_solver_constructor

from .feasible_solution_generator import universal_feasible_solution_generator, complicated_feasible_solution_generator


def slsqp_solving(slsqp_solver_obj, input_matrix, verbose=False, report_interval=50, thread_num_constraint=None):
    final_time_list = []
    final_loss_list = []
    final_solution_list = []
    final_predicted_dict = {}
    for row_index, input_row in enumerate(input_matrix):
        if not verbose:
            print('Start solving row {}'.format(row_index))
        assert len(input_row.shape) == 1
        with threadpool_limits(limits=thread_num_constraint):
            final_solution, final_obj_value, success = slsqp_solver_obj.solve(input_row)
        if not success:
            continue
        final_solution_list.append(final_solution)
        final_loss_list.append(final_obj_value)
        final_time_list.append(slsqp_solver_obj.recorder.running_time)
        current_predicted_dict = slsqp_solver_obj.predict(final_solution)
        for emu_name, predicted_vector in current_predicted_dict.items():
            if emu_name not in final_predicted_dict:
                final_predicted_dict[emu_name] = []
            final_predicted_dict[emu_name].append(predicted_vector)
        if verbose and row_index > 0 and row_index % report_interval == 0:
            print('{} finished'.format(row_index))
    final_solution_array = np.array(final_solution_list)
    final_time_array = np.array(final_time_list)
    final_loss_array = np.array(final_loss_list)
    return final_solution_array, final_time_array, final_loss_array, final_predicted_dict


def each_case_optimization_distribution_iter_generator(
        each_case_optimization_num, each_process_optimization_num, total_initial_flux_input=None,
        solver_obj=None, max_optimization_each_generation=None, result_label=''):
    def simple_each_case_iter_generator(
            _total_initial_flux_input, _current_initial_point_num, _each_process_optimization_num,
            _current_optimization_start_index):
        for start_index in np.arange(0, _current_initial_point_num, _each_process_optimization_num):
            if start_index + _each_process_optimization_num > _current_initial_point_num:
                current_optimization_num = _current_initial_point_num - start_index
            else:
                current_optimization_num = _each_process_optimization_num
            current_initial_flux_input = _total_initial_flux_input[
                                         start_index: (start_index + _each_process_optimization_num)]
            yield current_initial_flux_input, current_optimization_num, \
                _current_optimization_start_index + start_index

    if total_initial_flux_input is not None:
        for result_tuple in simple_each_case_iter_generator(
                total_initial_flux_input, each_case_optimization_num, each_process_optimization_num, 0):
            yield result_tuple
    else:
        if each_case_optimization_num is None or solver_obj is None:
            raise ValueError(
                'Both solver_obj and each_case_optimization_num cannot be None '
                'if total_initial_flux_input not provided!')
        for current_optimization_start_index in np.arange(
                0, each_case_optimization_num, max_optimization_each_generation):
            if current_optimization_start_index + max_optimization_each_generation > each_case_optimization_num:
                current_initial_point_num = each_case_optimization_num - current_optimization_start_index
            else:
                current_initial_point_num = max_optimization_each_generation
            print(f'Generating {current_initial_point_num} initial value of {result_label}...')
            total_initial_flux_input = universal_feasible_solution_generator(solver_obj, current_initial_point_num)
            print(f'{result_label} initial value finished')
            for result_tuple in simple_each_case_iter_generator(
                    total_initial_flux_input, current_initial_point_num, each_process_optimization_num,
                    current_optimization_start_index):
                yield result_tuple


def generate_unoptimized_solutions(
        mfa_config, new_optimization_num, final_result_obj, base_solver_obj, result_label, result_information,
        each_case_target_optimization_num):
    total_target_size = 10 * new_optimization_num
    raw_unoptimized_solutions = complicated_feasible_solution_generator(
        base_solver_obj, total_target_size, thinning=50)
    unoptimized_solutions = raw_unoptimized_solutions[
        random_seed.choice(range(total_target_size), new_optimization_num, replace=False)]
    slsqp_solver_obj = specific_solver_constructor(base_solver_obj, mfa_config)

    time_array = np.zeros(len(unoptimized_solutions))
    loss_list = []
    final_predicted_dict = {}
    for initial_flux in unoptimized_solutions:
        loss_value = slsqp_solver_obj.obj_eval(initial_flux)
        loss_list.append(loss_value)
        current_predicted_dict = slsqp_solver_obj.predict(initial_flux)
        for emu_name, predicted_vector in current_predicted_dict.items():
            if emu_name not in final_predicted_dict:
                final_predicted_dict[emu_name] = []
            final_predicted_dict[emu_name].append(predicted_vector)
    loss_array = np.array(loss_list)
    result_list = (unoptimized_solutions, time_array, loss_array, final_predicted_dict)
    final_result_obj.parallel_add_and_save_result(
        result_list, result_label, result_information, slsqp_solver_obj.flux_name_index_dict,
        slsqp_solver_obj.target_experimental_mid_data_dict, 0, each_case_target_optimization_num)


def load_previous_results(result_label, final_result_obj, each_case_optimization_num):
    loaded_num = final_result_obj.load_previous_results(result_label)
    assert each_case_optimization_num is not None
    if loaded_num >= each_case_optimization_num:
        new_optimization_num = 0
    else:
        new_optimization_num = each_case_optimization_num - loaded_num
    return new_optimization_num


def parallel_parameter_generator(result_list, test_mode, report_interval, thread_num_constraint):
    for (
            base_solver_obj, mfa_config, each_case_iter, result_label, result_information,
            each_case_target_optimization_num) in result_list:
        print('{} started'.format(result_label))
        for current_initial_flux_input, current_optimization_num, start_index in each_case_iter:
            parameter_list = (
                base_solver_obj, mfa_config, current_initial_flux_input, test_mode,
                result_label, result_information, current_optimization_num,
                start_index, each_case_target_optimization_num, report_interval, thread_num_constraint)
            yield parameter_list

        # print('{} finished'.format(result_label))


def common_parallel_single_solver(parameter_list):
    (
        base_solver_obj, mfa_config, initial_flux_input, test_mode, result_label, result_information,
        current_optimization_num, start_index, each_case_target_optimization_num,
        report_interval, thread_num_constraint) = parameter_list
    slsqp_solver_obj = specific_solver_constructor(base_solver_obj, mfa_config)
    result_list = slsqp_solving(
        slsqp_solver_obj, initial_flux_input, verbose=not test_mode,
        report_interval=report_interval, thread_num_constraint=thread_num_constraint)
    return result_list, result_label, result_information, slsqp_solver_obj.flux_name_index_dict, \
        slsqp_solver_obj.target_experimental_mid_data_dict, current_optimization_num, start_index, \
        each_case_target_optimization_num


def common_parallel_solver(
        final_result_obj, total_optimization_num, parameter_list_iter, processes_num=4, parallel_test=False,
        **other_parameters):
    def process_result(current_raw_result):
        (
            result_list, result_label, result_information, flux_name_index_dict,
            target_experimental_mid_data_dict, current_optimization_num, start_index,
            each_case_target_optimization_num) = current_raw_result
        pbar.update(current_optimization_num)
        final_result_obj.parallel_add_and_save_result(
            result_list, result_label, result_information, flux_name_index_dict,
            target_experimental_mid_data_dict, start_index, each_case_target_optimization_num)

    pbar = tqdm.tqdm(
        total=total_optimization_num, smoothing=0, maxinterval=5,
        desc="Computation progress of {}".format(final_result_obj.result_name))
    if parallel_test:
        for parameter_list in parameter_list_iter:
            raw_result = common_parallel_single_solver(parameter_list)
            process_result(raw_result)

    with mp.Pool(processes=processes_num) as pool:
        raw_result_iter = pool.imap(common_parallel_single_solver, parameter_list_iter)
        for raw_result in raw_result_iter:
            process_result(raw_result)


def parallel_solver_wrap(
        result_list, final_result_obj, total_optimization_num, test_mode, report_interval, parallel_parameter_dict):
    thread_num_constraint = parallel_parameter_dict[Keywords.thread_num_constraint]
    parameter_list_iter = parallel_parameter_generator(
        result_list, test_mode, report_interval, thread_num_constraint)
    common_parallel_solver(
        final_result_obj, total_optimization_num, parameter_list_iter,
        **parallel_parameter_dict)


def serial_solver_wrap(
        result_list, final_result_obj, total_optimization_num, test_mode, report_interval, parallel_parameter_dict):
    pbar = tqdm.tqdm(
        total=total_optimization_num, smoothing=0, maxinterval=5,
        desc="Computation progress of {}".format(final_result_obj.result_name))
    for (
            base_solver_obj, mfa_config, this_case_optimization_num, result_label, result_information,
            each_case_target_optimization_num) in result_list:
        initial_flux_input = None
        if isinstance(this_case_optimization_num, int):
            if this_case_optimization_num == 0:
                print(f'No solutions of {result_label} needs to be generated.')
                continue
            else:
                print(f'{result_label} started: {this_case_optimization_num} solutions need to be generated')
        elif isinstance(this_case_optimization_num, (list, np.ndarray)):
            initial_flux_input = this_case_optimization_num
            this_case_optimization_num = len(initial_flux_input)
        else:
            raise ValueError()
        slsqp_obj = specific_solver_constructor(base_solver_obj, mfa_config)
        if initial_flux_input is None:
            initial_flux_input = universal_feasible_solution_generator(slsqp_obj, this_case_optimization_num)
        if initial_flux_input is None:
            print(f'{result_label} failed to generate initial flux')
        else:
            print('Initial flux generated')
            result_list = slsqp_solving(
                slsqp_obj, initial_flux_input, verbose=not test_mode, report_interval=report_interval)
            pbar.update(this_case_optimization_num)
            print(f'{result_label} ended')
            final_result_obj.add_and_save_result(
                result_label, result_information, result_list, slsqp_obj.flux_name_index_dict,
                slsqp_obj.target_experimental_mid_data_dict)


def solver_and_solution_list_construct(
        parameter_label_content_dict, final_result_obj, test_mode, each_case_target_optimization_num, load_results,
        parallel_parameters=None, predefined_initial_solution_matrix_loader=None):
    result_list = []
    total_optimization_num = 0
    if parallel_parameters is None:
        each_process_optimization_num = None
        max_optimization_each_generation = None
    else:
        each_process_optimization_num = parallel_parameters[Keywords.each_process_optimization_num]
        max_optimization_each_generation = parallel_parameters[Keywords.max_optimization_each_generation]
    for result_label, (
            label_tuple, (mfa_model, mfa_data, mfa_config),
            result_information, other_information_dict) in parameter_label_content_dict.items():
        if Keywords.predefined_initial_solution_matrix in mfa_config.miscellaneous_config:
            optimization_from_predefined_initial_solution_parameter_dict = mfa_config.miscellaneous_config[
                Keywords.predefined_initial_solution_matrix]
            averaged_solution_flux_matrix = predefined_initial_solution_matrix_loader(
                *label_tuple, optimization_from_predefined_initial_solution_parameter_dict)
            each_case_target_optimization_num = len(averaged_solution_flux_matrix)
        else:
            averaged_solution_flux_matrix = None
        if load_results:
            new_optimization_num = load_previous_results(
                result_label, final_result_obj, each_case_target_optimization_num)
        else:
            new_optimization_num = each_case_target_optimization_num
        if new_optimization_num == 0:
            print(f'No solution of {result_label} need to be obtained. Abort')
            continue
        base_solver_obj = base_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
        base_solver_obj.base_initialize_solver()
        if Keywords.unoptimized in mfa_config.miscellaneous_config:
            generate_unoptimized_solutions(
                mfa_config, new_optimization_num, final_result_obj, base_solver_obj, result_label,
                result_information, each_case_target_optimization_num)
            print(f'{new_optimization_num} number of unoptimized solutions have been saved.')
            continue
        elif Keywords.predefined_initial_solution_matrix in mfa_config.miscellaneous_config:
            averaged_solution_flux_matrix = averaged_solution_flux_matrix[-new_optimization_num:]
            if parallel_parameters is None:
                each_case_iter = averaged_solution_flux_matrix
            else:
                print(f'{new_optimization_num} initial value of {result_label} loaded')
                each_case_iter = each_case_optimization_distribution_iter_generator(
                    new_optimization_num, each_process_optimization_num, solver_obj=base_solver_obj,
                    total_initial_flux_input=averaged_solution_flux_matrix,
                    result_label=result_label)
        else:
            if parallel_parameters is None:
                each_case_iter = new_optimization_num
            else:
                print(f'{new_optimization_num} initial value of {result_label} needs to be generated')
                each_case_iter = each_case_optimization_distribution_iter_generator(
                    new_optimization_num, each_process_optimization_num, solver_obj=base_solver_obj,
                    max_optimization_each_generation=max_optimization_each_generation,
                    result_label=result_label)
        total_optimization_num += new_optimization_num
        result_list.append((
            base_solver_obj, mfa_config, each_case_iter, result_label, result_information,
            each_case_target_optimization_num))
    return result_list, total_optimization_num


def common_solver(
        parameter_label_content_dict, test_mode, final_result_obj, each_case_target_optimization_num,
        report_interval, parallel_parameter_dict=None, load_results=False,
        predefined_initial_solution_matrix_loader=None):
    if parallel_parameter_dict is None:
        solver_wrap = serial_solver_wrap
    else:
        solver_wrap = parallel_solver_wrap
    result_list, total_optimization_num = solver_and_solution_list_construct(
        parameter_label_content_dict, final_result_obj, test_mode, each_case_target_optimization_num,
        load_results, parallel_parameter_dict, predefined_initial_solution_matrix_loader)
    solver_wrap(
        result_list, final_result_obj, total_optimization_num, test_mode, report_interval,
        parallel_parameter_dict)

