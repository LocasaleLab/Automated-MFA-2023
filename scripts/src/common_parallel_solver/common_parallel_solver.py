from .packages import np, mp, tqdm, threadpool_limits
from .config import Keywords, random_seed, specific_solver_constructor, base_solver_constructor, parameter_extract

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


def batch_solving_func(
        final_result_obj, result_label, result_information, slsqp_solver_obj, initial_flux_input,
        this_case_optimization_num, pbar, parallel_parameter_dict, verbose=False):
    def single_step_initial_input_generator(
            initial_flux_input, this_case_optimization_num, max_initial_num_each_generation, batch_size):
        if initial_flux_input is None:
            total_optimization_num = this_case_optimization_num
            rest_initial_num = 0
            rest_initial_input = None
        else:
            total_optimization_num = initial_flux_input.shape[0]
            rest_initial_input = initial_flux_input
            rest_initial_num = total_optimization_num
        for start_initial_index in range(0, total_optimization_num, batch_size):
            current_step_num = min(total_optimization_num - start_initial_index, batch_size)
            if initial_flux_input is None:
                if rest_initial_num < current_step_num:
                    initial_num_to_generate = min(
                        total_optimization_num - start_initial_index, max_initial_num_each_generation)
                    print(f'Generating {initial_num_to_generate} initial value of {result_label}...')
                    new_initial_input = universal_feasible_solution_generator(
                        slsqp_solver_obj, initial_num_to_generate)
                    if new_initial_input is None:
                        print(f'{result_label} failed to generate initial flux')
                        exit(-1)
                    else:
                        print('Initial flux generated')
                    diff = current_step_num - rest_initial_num
                    if rest_initial_input is None:
                        current_step_initial_input = new_initial_input[:diff]
                    else:
                        current_step_initial_input = np.vstack([rest_initial_input, new_initial_input[:diff]])
                    rest_initial_input = new_initial_input[diff:]
                else:
                    current_step_initial_input = rest_initial_input[:current_step_num]
                    rest_initial_input = rest_initial_input[current_step_num:]
            else:
                current_step_initial_input = initial_flux_input[
                    start_initial_index:start_initial_index + current_step_num]
            yield current_step_num, current_step_initial_input

    batch_size = parallel_parameter_dict[Keywords.batch_solving]
    max_initial_num_each_generation = parameter_extract(
        parallel_parameter_dict, Keywords.max_optimization_each_generation, this_case_optimization_num)
    maximal_save_point = parameter_extract(
        parallel_parameter_dict, Keywords.maximal_save_point, max_initial_num_each_generation)
    report_interval = 100
    # if initial_flux_input is None:
    #     initial_flux_input = universal_feasible_solution_generator(slsqp_solver_obj, this_case_optimization_num)
    # if initial_flux_input is None:
    #     print(f'{result_label} failed to generate initial flux')
    # else:
    #     print('Initial flux generated')
    final_time_list = []
    final_loss_list = []
    final_solution_list = []
    final_predicted_dict = {}
    calculated_solution_num = 0
    solution_num_since_last_save = 0
    for current_step_num, current_step_initial_input in single_step_initial_input_generator(
            initial_flux_input, this_case_optimization_num, max_initial_num_each_generation, batch_size):
        if verbose:
            print(f'Start solving solution # {calculated_solution_num} ~ {calculated_solution_num + current_step_num}')
        final_solution, final_obj_value = slsqp_solver_obj.solve(current_step_initial_input)
        time_array = np.ones(batch_size) * slsqp_solver_obj.recorder.running_time / batch_size
        print(time_array)
        exit()
        result_list = (final_solution, time_array, final_obj_value, {})
        calculated_solution_num += current_step_num
        final_result_obj.add_and_save_result(
            result_label, result_information, result_list, slsqp_solver_obj.flux_name_index_dict,
            slsqp_solver_obj.target_experimental_mid_data_dict)
        solution_num_since_last_save += current_step_num
        pbar.update(current_step_num)
        if verbose and solution_num_since_last_save >= report_interval:
            print('{} finished'.format(calculated_solution_num))
            solution_num_since_last_save = 0
    final_solution_array = np.array(final_solution_list)
    final_time_array = np.array(final_time_list)
    final_loss_array = np.array(final_loss_list)

    print(f'{result_label} ended')
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

    """Add day to elapsed and remaining will be very troublesome for tqdm. Abort it."""
    pbar = tqdm.tqdm(
        total=total_optimization_num, smoothing=0, maxinterval=5,
        desc='Computation progress of {}'.format(final_result_obj.result_name))
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
    batch_solving = False
    if parallel_parameter_dict is not None:
        if Keywords.batch_solving in parallel_parameter_dict:
            batch_solving = True
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
        if batch_solving:
            batch_solving_func(
                final_result_obj, result_label, result_information, slsqp_obj, initial_flux_input,
                this_case_optimization_num, pbar, parallel_parameter_dict, verbose=not test_mode)
        else:
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
        parallel_parameters=None, predefined_initial_solution_matrix_loader=None, batch_solving=False):
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
        if Keywords.specific_target_optimization_num in mfa_config.miscellaneous_config:
            this_case_target_optimization_num = mfa_config.miscellaneous_config[
                Keywords.specific_target_optimization_num]
            set_specific_target_optimization_num = True
        else:
            this_case_target_optimization_num = each_case_target_optimization_num
            set_specific_target_optimization_num = False
        if Keywords.predefined_initial_solution_matrix in mfa_config.miscellaneous_config:
            optimization_from_predefined_initial_solution_parameter_dict = mfa_config.miscellaneous_config[
                Keywords.predefined_initial_solution_matrix]
            predefined_solution_flux_matrix = predefined_initial_solution_matrix_loader(
                final_result_obj, *label_tuple, optimization_from_predefined_initial_solution_parameter_dict)
            if set_specific_target_optimization_num:
                assert this_case_target_optimization_num <= len(predefined_solution_flux_matrix)
            else:
                this_case_target_optimization_num = len(predefined_solution_flux_matrix)
        else:
            predefined_solution_flux_matrix = None
        if load_results:
            new_optimization_num = load_previous_results(
                result_label, final_result_obj, this_case_target_optimization_num)
        else:
            new_optimization_num = this_case_target_optimization_num
        if new_optimization_num == 0:
            print(f'No solution of {result_label} need to be obtained. Abort')
            continue
        base_solver_obj = base_solver_constructor(mfa_model, mfa_data, mfa_config, verbose=test_mode)
        base_solver_obj.base_initialize_solver()
        if Keywords.unoptimized in mfa_config.miscellaneous_config:
            print(f'Generating {new_optimization_num} number of unoptimized solutions...')
            generate_unoptimized_solutions(
                mfa_config, new_optimization_num, final_result_obj, base_solver_obj, result_label,
                result_information, this_case_target_optimization_num)
            print(f'{new_optimization_num} number of unoptimized solutions have been saved.')
            continue
        elif Keywords.predefined_initial_solution_matrix in mfa_config.miscellaneous_config:
            predefined_solution_flux_matrix = predefined_solution_flux_matrix[-new_optimization_num:]
            if parallel_parameters is None:
                each_case_iter = predefined_solution_flux_matrix
            else:
                print(f'{new_optimization_num} initial value of {result_label} loaded')
                each_case_iter = each_case_optimization_distribution_iter_generator(
                    new_optimization_num, each_process_optimization_num, solver_obj=base_solver_obj,
                    total_initial_flux_input=predefined_solution_flux_matrix,
                    result_label=result_label)
        else:
            if parallel_parameters is None or batch_solving:
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
            this_case_target_optimization_num))
    return result_list, total_optimization_num


def common_solver(
        parameter_label_content_dict, test_mode, final_result_obj, each_case_target_optimization_num,
        report_interval, parallel_parameter_dict=None, load_results=False,
        predefined_initial_solution_matrix_loader=None):
    batch_solving = False
    if parallel_parameter_dict is None:
        solver_wrap = serial_solver_wrap
    elif Keywords.batch_solving in parallel_parameter_dict:
        solver_wrap = serial_solver_wrap
        batch_solving = True
    else:
        solver_wrap = parallel_solver_wrap
    result_list, total_optimization_num = solver_and_solution_list_construct(
        parameter_label_content_dict, final_result_obj, test_mode, each_case_target_optimization_num,
        load_results, parallel_parameter_dict, predefined_initial_solution_matrix_loader, batch_solving)
    solver_wrap(
        result_list, final_result_obj, total_optimization_num, test_mode, report_interval,
        parallel_parameter_dict)

