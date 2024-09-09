
class CoreConstants(object):
    float_type = "float64"
    eps_for_log = 1e-10
    eps_for_mid = 1e-5
    eps_for_computation = 1e-10
    # eps_for_sampling = 1e-11
    eps_for_sampling = 1e-20
    natural_c13_ratio = 0.01109
    maximal_unconstrained_flux_value = 1e8

    lp_random_min_factor = 2
    lp_random_max_factor = 0.2
    maximal_failed_time = 10

    graph_name = 'solver_graph'

    # Special strings
    unlabeled = 'unlabeled'
    mix_ratio_prefix = 'MIX'
    mix_flux_sep = ':'
    # undefined_compartment = 'undefined'
    carbon_list_unofficial_sep = '-'
    emu_carbon_list_str_sep = '__'
    convolution_emu_sep = '___'
    reverse_reaction_name_suffix = '__R'
    space_replacer = '_'
    standard_metabolite_sep = '/'
    common_metabolite_sep_list = [' or ']
    compartmental_mid_name_sep = '~'
    specific_tissue_sep = '--'

    comment_label = '#'
    alias_to_standard_name_sep = ':: '
    alias_sep = ';; '

    # biomass_flux_id = 'BIOMASS_maintenance'
    biomass_flux_id = 'BIOMASS_REACTION'
    convolution_id = 'CONV'
    cycle_solve_id = 'CYCLE_SOLVE'
    single_emu_id = 'SINGLE_EMU'

    success_code = 0
    limit_reached_code = 9


class ParamName(object):
    finished = 'finished'
    # numpy slsqp parameter
    slsqp_tolerance = 'tolerance'
    slsqp_max_iter = 'max_iter'
    slsqp_embedding_obj = 'embedding_obj'

    slsqp_ratio_dict_to_objective_func = 'ratio_dict_to_objective_func'
    slsqp_list_of_case_name = 'list_of_case_name'
    slsqp_trust_region = 'trust_region'

    base_lp = 'base_lp'
    loss_type = 'loss_type'
    batch_size = 'batch_size'
    emu_value_parallel_num = 'emu_value_parallel_num'
    emu_gradient_hessian_parallel_num = 'emu_gradient_hessian_parallel_num'
    each_portion_flux_num = 'each_portion_flux_num'
    optimization_mode = 'optimization_mode'
    thinning = 'thinning'

    # solver type
    base_solver = 'base'
    slsqp_solver = 'slsqp'
    slsqp_numba_solver = 'slsqp_numba'
    torch_solver = 'torch'
    tf2_solver = 'tf2'
    tf2_sampler_solver = 'tf2_sampler'
    tf2_optimized_sampler_solver = 'tf2_op_sampler'
    tf2_slsqp_solver = 'tf2_slsqp'
    tf2_sa_solver = 'tf2_sa'

    # analysis mode
    acyclic_constructor = 'acyclic'
    traditional_constructor = 'traditional'

    normal_mode = 'normal'
    bounds_only_mode = 'bounds-only'
    all_penalty_mode = 'all-penalty'

    cross_entropy_loss = 'cross_entropy_loss'
    mean_squared_loss = 'mean_squared_loss'

    eq_right_side = 'eq_right_side'
    smaller_or_eq_right_side = 'smaller_or_eq_right_side'

    # loss names
    mid_loss = 'mid_loss'
    flux_balance_loss = 'flux_balance_loss'
    constant_flux_loss = 'constant_flux_loss'
    mix_ratio_loss = 'mix_ratio_loss'
    flux_constraint_loss = 'flux_constraint_loss'
    inequality_loss = 'inequality_loss'

    # gradient descent optimization parameters
    maximal_training_steps = 'maximal_training_steps'
    preset_constraint_coefficient_dict = 'preset_constraint_coefficient_dict'
    initial_noise = 'initial_noise'
    final_noise = 'final_noise'
    noise_decay_rate = 'noise_decay_rate'
    learning_rate = 'learning_rate'
    beta1 = 'beta1'
    beta2 = 'beta2'
    epsilon = 'epsilon'
    singular_eps_ratio = 'singular_eps_ratio'

    # debug option
    debug = 'debug'
    stop_in_advance = 'stop_in_advance'
    print_interval = 'print_interval'
    min_step = 'min_step'
    loss_terminate_value = 'loss_terminate_value'

    # result output
    batch_mid_loss_tensor = 'batch_mid_loss_tensor'
    raw_difference_tensor = 'raw_difference_tensor'
    total_batch_loss_tensor = 'total_batch_loss_tensor'
    target_emu_value_list = 'target_emu_value_list'

    # sample option
    initial_random_min_factor = 'initial_random_min_factor'
    initial_random_max_factor = 'initial_random_max_factor'
    initial_maximal_failed_time = 'initial_maximal_failed_time'
    numeric_eps = 'numeric_eps'
    warmup_multiplier = 'warmup_multiplier'
    random_direction_pool_multiplier = 'random_direction_pool_multiplier'
    maximal_range_ratio = 'maximal_range_ratio'
    maximal_fail_num = 'maximal_fail_num'

    # sample-solver parameters
    temperature = 'temperature'
    multiple = 'multiple'
    sample_batch_multiplier = 'sample_batch_multiplier'
    after_sample_optimization = 'after_sample_optimization'
    parameter_selection = 'parameter_selection'
    one_percent_item_probability = 'one_percent_item_probability'
    one_millesimal_item_probability = 'one_millesimal_item_probability'
    total_stored_distribution_num = 'total_stored_distribution_num'

    # tf2 slsqp parameter
    nnls_batch_size = 'nnls_batch_size'
    nnls_parallel_num = 'nnls_parallel_num'
    max_output_stock_num = 'max_output_stock_num'
    final_loss_threshold = 'final_loss_threshold'
    recent_mid_monitor_num = 'recent_mid_monitor_num'
    recent_mid_average_update_threshold = 'recent_mid_average_update_threshold'
    report_interval = 'report_interval'
    finished_solution_report_interval = 'finished_solution_report_interval'
    recent_average_flux_update_threshold = 'recent_average_flux_update_threshold'
    allowed_update_failed_time = 'allowed_update_failed_time'
    sqp_less_update_threshold_ratio = 'sqp_less_update_threshold_ratio'
    allowed_sqp_search_failed_time = 'allowed_sqp_search_failed_time'
    refresh_hessian_threshold = 'refresh_hessian_threshold'
    less_update_ratio_for_hessian_refresh = 'less_update_ratio_for_hessian_refresh'
    one_time_fail_sqp_threshold_for_hessian_refresh = 'one_time_fail_sqp_threshold_for_hessian_refresh'
    add_perturbation_threshold = 'add_perturbation_threshold'
    gradient_repeat_time = 'gradient_repeat_time'
    hessian_reset_threshold_time = 'hessian_reset_threshold_time'
    hessian_refresh_block_time = 'hessian_refresh_block_time'
    hessian_refresh_max_interval = 'hessian_refresh_max_interval'
    division_eps = 'division_eps'
    boundary_eps = 'boundary_eps'
    alpha_eps = 'alpha_eps'
    lamb = 'lamb'
    rel_tol = 'rel_tol'
    red_c = 'red_c'
    exp_c = 'exp_c'
    qr_approximate = 'qr_approximate'
    adjust_ratio = 'adjust_ratio'
    step_size_c_one = 'step_size_c_one'
    step_size_c_two = 'step_size_c_two'
    step_size_rho = 'step_size_rho'
    step_size_min_shrink_factor = 'step_size_min_shrink_factor'
    min_step_size = 'min_step_size'

    # tf2 sa parameter
    batch_index_tensor = 'batch_index_tensor'
    result_flux_storage_tensor = 'result_flux_storage_tensor'
    result_obj_storage_tensor = 'result_obj_storage_tensor'
    initial_temperature_value = 'initial_temperature_value'
    maximal_running_step = 'maximal_running_step'
    zero_temperature_ratio = 'zero_temperature_ratio'

    # numba parameter
    slsqp_numba_python_solver = 'slsqp_python_solver'
    slsqp_numba_nopython_solver = 'slsqp_nopython_solver'
    numba_nopython = 'nopython'


class ModelKeyword(object):
    id = 'id'
    sub = 'sub'
    pro = 'pro'

    comp = 'comp'
    flux_range = 'flux_range'

    normal_range_type = 'normal'
    add_range_type = 'add'
    no_range_type = 'none'
    specific_range_type = 'specific'

    general = 'general'
    serum = 'serum'
    liver = 'liver'
    kidney = 'kidney'
    heart = 'heart'
    brain = 'brain'
    spleen = 'spleen'
    pancreas = 'pancreas'
    lung = 'lung'
    small_intestine = 'small_intestine'
    muscle = 'muscle'
    q_muscle = 'quadriceps_muscle'
    vastus_muscle = 'vastus_muscle'
    soleus_muscle = 'soleus_muscle'
    gastroc_muscle = 'gastroc_muscle'
    brown_adipose = 'brown_adipose'
    white_adipose = 'white_adipose'
    po_adipose = 'periovarian_adipose'
    sq_adipose = 'sub_q_fat'
    go_adipose = 'gonadal_adipose'
    in_adipose = 'inguinal_adipose'

