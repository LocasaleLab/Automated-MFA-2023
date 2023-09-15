from ...common.packages import np


def calculate_direction_range(
        current_location, unit_direction, lb, ub, a_ub, b_ub, eps):
    """
    Calculate the feasible maximal range of the given direction from current location.
    The current location should be feasible, the direction should be unit vector and satisfy linear constraints,
        and only positive value will be calculated.
    """

    # if lb is None and ub is None and a_ub is None and b_ub is None:
    #     raise ValueError("At least one of constraints should be provided!")

    # flux_lb_distance_vector = (lb - current_location + eps) / (unit_direction + eps)
    flux_lb_distance_vector = (lb + eps - current_location) / (unit_direction + eps)
    if np.all(flux_lb_distance_vector < 0):
        return None
    flux_lb_min_value = np.min(flux_lb_distance_vector[flux_lb_distance_vector > 0])
    # flux_ub_distance_vector = (ub - current_location + eps) / (unit_direction + eps)
    flux_ub_distance_vector = (ub - eps - current_location) / (unit_direction + eps)
    if np.all(flux_ub_distance_vector < 0):
        return None
    flux_ub_min_value = np.min(flux_ub_distance_vector[flux_ub_distance_vector > 0])
    flux_bound_min_value = min(flux_lb_min_value, flux_ub_min_value)
    if a_ub is not None and b_ub is not None:
        # ub_constraint_distance_vector = (b_ub - a_ub @ current_location + eps) / (a_ub @ unit_direction + eps)
        ub_constraint_distance_vector = (b_ub - eps - a_ub @ current_location) / (a_ub @ unit_direction + eps)
        if np.all(ub_constraint_distance_vector < 0):
            return None
        ub_constraint_min_value = np.min(ub_constraint_distance_vector[ub_constraint_distance_vector > 0])
        global_min_value = min(flux_bound_min_value, ub_constraint_min_value)
    elif a_ub is not None or b_ub is not None:
        raise ValueError("a_ub and b_ub should be both None or neither None!")
    else:
        global_min_value = flux_bound_min_value
    if global_min_value < eps:
        return None
    return global_min_value


def check_new_location(new_location, lb, ub, a_ub, b_ub, eps):
    if np.any(new_location - lb - eps < 0) or np.any(ub - new_location - eps < 0):
        return False
    if a_ub is not None and b_ub is not None:
        if np.any(b_ub - a_ub @ new_location - eps < 0):
            return False
    return True


def random_direction_pool_generator(variable_num, pool_size, projection_matrix, eps):
    np_rng = np.random.default_rng()
    mean = np.zeros(variable_num)
    cov = np.identity(variable_num)
    raw_direction_vector_pool = np_rng.multivariate_normal(mean, cov, pool_size).T
    if projection_matrix is not None:
        projected_direction_vector_pool = projection_matrix @ raw_direction_vector_pool
    else:
        projected_direction_vector_pool = raw_direction_vector_pool
    normalized_direction_vector_pool = projected_direction_vector_pool / (np.linalg.norm(
        projected_direction_vector_pool, axis=0) + eps)
    return normalized_direction_vector_pool


def chrr_ellipsoid_matrix_generation(lb, ub, a_ub, b_ub):
    pass

