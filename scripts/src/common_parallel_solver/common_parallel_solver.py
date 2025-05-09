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


def no_specific_initial_input_generator(
        slsqp_solver_obj, result_label, this_case_optimization_num, max_initial_num_each_generation):
    start_initial_index = 0
    saved_initial_input = None
    target_total_initial_num = int(1.3 * this_case_optimization_num)
    while True:
        default_initial_num = max_initial_num_each_generation
        this_turn_real_initial_num_to_generate = min(max(
            target_total_initial_num - start_initial_index, 0), max_initial_num_each_generation)
        if this_turn_real_initial_num_to_generate > 0:
            print(f'Generating {this_turn_real_initial_num_to_generate} initial value of {result_label}...')
            new_initial_input = universal_feasible_solution_generator(
                slsqp_solver_obj, this_turn_real_initial_num_to_generate)
            if new_initial_input is None:
                print(f'{result_label} failed to generate initial flux')
                exit(-1)
            else:
                print('Initial flux generated')
            if this_turn_real_initial_num_to_generate < default_initial_num:
                complete_new_initial_input = np.tile(
                    new_initial_input,
                    (int(np.ceil(default_initial_num / this_turn_real_initial_num_to_generate)), 1)
                )[:default_initial_num]
            else:
                complete_new_initial_input = new_initial_input
            if saved_initial_input is None:
                saved_initial_input = complete_new_initial_input
        else:
            complete_new_initial_input = saved_initial_input
        new_initial_id_array = np.arange(start_initial_index, start_initial_index + default_initial_num)
        start_initial_index += default_initial_num
        yield default_initial_num, complete_new_initial_input, new_initial_id_array, \
            this_turn_real_initial_num_to_generate


def specific_initial_input_generator(
        initial_flux_input, initial_flux_input_id, max_initial_num_each_generation):
    total_optimization_num = initial_flux_input.shape[0]
    if initial_flux_input_id is None:
        initial_flux_input_id = np.arange(0, total_optimization_num)
    start_initial_index = 0
    fake_step_num = -1
    fake_step_flux_input = None
    max_id = 0
    default_step_num = max_initial_num_each_generation
    while True:
        end_initial_index = start_initial_index + default_step_num
        if end_initial_index < total_optimization_num:
            real_input_num = default_step_num
            current_step_initial_input = initial_flux_input[start_initial_index:end_initial_index]
            if initial_flux_input_id is not None:
                current_step_initial_id_array = initial_flux_input_id[start_initial_index:end_initial_index]
                max_id = max(max_id, current_step_initial_id_array.max())
            else:
                current_step_initial_id_array = np.arange(
                    start_initial_index, start_initial_index + default_step_num)
                max_id += default_step_num
        elif start_initial_index < total_optimization_num:
            real_input_num = total_optimization_num - start_initial_index
            unreal_input_num = default_step_num - real_input_num
            real_initial_input = initial_flux_input[start_initial_index:]
            current_step_initial_input = np.tile(
                real_initial_input, (int(np.ceil(default_step_num / real_input_num)), 1)
            )[:default_step_num]
            if initial_flux_input_id is not None:
                real_initial_id_array = initial_flux_input_id[start_initial_index:]
                max_id = max(max_id, real_initial_id_array.max())
                current_step_initial_id_array = np.concatenate(
                    [real_initial_id_array, np.arange(max_id, max_id + unreal_input_num)])
                max_id += unreal_input_num
            else:
                current_step_initial_id_array = np.arange(
                    start_initial_index, start_initial_index + default_step_num)
                max_id += default_step_num
        else:
            real_input_num = 0
            current_step_initial_input = fake_step_flux_input
            current_step_initial_id_array = np.arange(max_id, max_id + default_step_num)
            max_id += default_step_num

        if fake_step_num < 0:
            fake_step_num = default_step_num
            fake_step_flux_input = current_step_initial_input
        start_initial_index += default_step_num
        yield default_step_num, current_step_initial_input, current_step_initial_id_array, real_input_num


def batch_continuously_solving_func(
        final_result_obj, result_label, result_information, base_solver_obj, mfa_config, initial_flux_input,
        this_case_optimization_num, pbar, update_q, parallel_parameter_dict, initial_flux_input_id=None, verbose=False):

    slsqp_solver_obj = specific_solver_constructor(base_solver_obj, mfa_config)
    max_initial_num_each_generation = parameter_extract(
        parallel_parameter_dict, Keywords.max_optimization_each_generation, this_case_optimization_num)
    """status: 0: new initial: start, 1: save, 2: more initial"""
    finish_status = False
    if initial_flux_input is None:
        initial_iterator = no_specific_initial_input_generator(
            slsqp_solver_obj, result_label, this_case_optimization_num, max_initial_num_each_generation)
    else:
        initial_iterator = specific_initial_input_generator(
            initial_flux_input, initial_flux_input_id, max_initial_num_each_generation)
        assert initial_flux_input.shape[0] == this_case_optimization_num
    print(f'Start solving {result_label}...')
    for (
            current_step_num, this_step_initial_input, this_step_initial_id_array, real_input_num
    ) in initial_iterator:
        process_new_input = True
        while not finish_status:
            (
                save, finish_status, final_solution_id_array, final_solution, final_obj_value,
                final_running_time
            ) = slsqp_solver_obj.continuously_solve(
                total_optimization_num=this_case_optimization_num, process_new_input=process_new_input,
                initial_flux_array=this_step_initial_input, initial_id_array=this_step_initial_id_array,
                real_input_num=real_input_num, pbar=pbar, update_q=update_q)
            if save:
                result_list = (final_solution, final_running_time, final_obj_value, {})
                final_result_obj.add_and_save_result(
                    result_label, result_information, result_list, slsqp_solver_obj.flux_name_index_dict,
                    slsqp_solver_obj.target_experimental_mid_data_dict, final_solution_id_array)
                process_new_input = False
            else:
                break
        if finish_status:
            break
    del slsqp_solver_obj
    print(f'{result_label} ended')
    if update_q is not None:
        update_q.put(-1)


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
    update_q = None
    if parallel_parameter_dict is not None:
        if Keywords.batch_solving in parallel_parameter_dict:
            batch_solving = True
            update_q = mp.Queue()
    for (
            base_solver_obj, mfa_config, this_case_optimization_num, result_label, result_information,
            each_case_target_optimization_num) in result_list:
        initial_flux_input = None
        if isinstance(this_case_optimization_num, int):
            if this_case_optimization_num == 0:
                print(f'No solutions of {result_label} needs to be obtained.')
                continue
            else:
                print(f'{result_label} started: {this_case_optimization_num} solutions need to be obtained.')
        elif isinstance(this_case_optimization_num, (list, np.ndarray)):
            initial_flux_input = this_case_optimization_num
            this_case_optimization_num = len(initial_flux_input)
        else:
            raise ValueError()
        if batch_solving:
            new_solving_process = mp.Process(
                target=batch_continuously_solving_func, args=(
                    final_result_obj, result_label, result_information, base_solver_obj, mfa_config, initial_flux_input,
                    this_case_optimization_num, None, update_q, parallel_parameter_dict, not test_mode))
            new_solving_process.start()
            while True:
                update_num = update_q.get()
                if update_num < 0:
                    break
                pbar.update(update_num)
            new_solving_process.join()
            new_solving_process.close()
        else:
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
        parallel_parameters=None, predefined_initial_solution_matrix_loader=None, batch_solving=False):
    result_list = []
    total_optimization_num = 0
    if parallel_parameters is None or batch_solving:
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
            elif test_mode:
                this_case_target_optimization_num = each_case_target_optimization_num
                predefined_solution_flux_matrix = predefined_solution_flux_matrix[:this_case_target_optimization_num]
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
        elif parallel_parameters is None or batch_solving:
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

