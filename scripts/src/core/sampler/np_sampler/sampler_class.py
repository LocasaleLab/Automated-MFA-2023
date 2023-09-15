from ...common.classes import CircularQueue
from ...common.packages import np, warnings
from ...common.config import ParamName

from ..base_class import default_random_min_factor, default_random_max_factor, \
    default_maximal_failed_time, eps, BaseSampler, LPSampler
from .common_sampler_functions import calculate_direction_range, check_new_location, \
    random_direction_pool_generator


class HRSampler(BaseSampler):
    """The abstract base class for hit-and-run samplers.

    Parameters
    ----------
    thinning : int
        The thinning factor of the generated sampling chain. A thinning of 10
        means samples are returned every 10 steps.

    Attributes
    ----------
    thinning : int
        The currently used thinning factor.

    """

    def __init__(
            self, variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, projection_matrix, thinning=50,
            initial_random_min_factor=default_random_min_factor, initial_random_max_factor=default_random_max_factor,
            initial_maximal_failed_time=default_maximal_failed_time,
            dynamic_constraint_index_dict=None, numeric_eps=eps, verbose=False):
        if dynamic_constraint_index_dict is None:
            dynamic_constraint_index_dict = {}
        super(HRSampler, self).__init__(
            variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, dynamic_constraint_index_dict=dynamic_constraint_index_dict,
            numeric_eps=numeric_eps, verbose=verbose)

        self.lp_sampler = LPSampler(
            variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, random_min_factor=initial_random_min_factor,
            random_max_factor=initial_random_max_factor, maximal_failed_time=initial_maximal_failed_time,
            dynamic_constraint_index_dict=dynamic_constraint_index_dict, numeric_eps=numeric_eps, verbose=verbose)
        self.thinning = thinning

        self.warmup_array = None  # Need refresh
        self.warmup_num = 100

        self.projection_matrix = projection_matrix

        self.random_direction_pool = None  # Need refresh
        self.random_direction_pool_size = 1000
        self.maximal_direction_sample_num = round(self.random_direction_pool_size * np.sqrt(self.variable_num))
        # self.current_direction_sample_num = self.maximal_direction_sample_num  # Need refresh
        self.current_direction_sample_num = None  # Need refresh

        self.maximal_range_ratio = 0.95  # For numerical stability

        self.maximal_trial_num = 15
        self.recent_points_num = 20
        self.recent_points_store_interval = 100
        # self.recent_points_circular_queue = CircularQueue(self.recent_points_num)
        self.recent_points_circular_queue = None  # Need refresh
        HRSampler.refresh(self)

    def refresh(self):
        self._lp_warmup()
        self.random_direction_pool = None
        self.current_direction_sample_num = self.maximal_direction_sample_num
        self.recent_points_circular_queue = CircularQueue(self.recent_points_num)

    def _lp_warmup(self):
        failed_count = 0
        warmup_list = self.lp_sampler.sample(self.warmup_num)
        while warmup_list is None and failed_count < 3:
            failed_count += 1
            warnings.warn("Cannot generate enough warm-up solutions. Relax random condition")
            self.lp_sampler.set_random_factor(
                new_random_min_factor=self.lp_sampler.random_min_factor / 2,
                new_random_max_factor=self.lp_sampler.random_max_factor / 2)
            warmup_list = self.lp_sampler.sample(self.warmup_num)
        if warmup_list is None:
            raise ValueError("Cannot generate enough warm-up solutions")
        self.warmup_array = np.array(warmup_list)

    def random_warmup_point(self):
        """Find an approximately random point in the flux cone."""

        index_array = np.random.randint(
            self.warmup_num, size=min(3, np.ceil(np.sqrt(self.warmup_num)))
        )
        return self.warmup_array[index_array, :].mean(axis=0)

    def generate_random_direction(self):
        if self.current_direction_sample_num >= self.maximal_direction_sample_num:
            self.random_direction_pool = random_direction_pool_generator(
                self.variable_num, self.random_direction_pool_size, self.projection_matrix, self.numeric_eps)
            self.current_direction_sample_num = 0
        self.current_direction_sample_num += 1
        random_col_index = np.random.randint(self.random_direction_pool_size)
        return self.random_direction_pool[:, random_col_index]

    def _store_current_location(self, current_location, sample_index=None):
        pass

    def _trace_back(self):
        pass

    def set_right_side_vector(self, dynamic_flux_value_dict):
        super(HRSampler, self).set_right_side_vector(dynamic_flux_value_dict)
        # if eq_or_smaller_eq == ParameterName.eq_right_side:
        #     target_vector = self.eq_right_side_vector
        # elif eq_or_smaller_eq == ParameterName.smaller_or_eq_right_side:
        #     target_vector = self.smaller_eq_right_side_vector
        # else:
        #     raise ValueError()
        target_vector = self.eq_right_side_vector
        for flux_name, flux_value in dynamic_flux_value_dict.items():
            target_vector[self.dynamic_constraint_index_dict[flux_name]] = flux_value


class OptGpSampler(HRSampler):
    def __init__(
            self, variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, projection_matrix, thinning=50,
            initial_random_min_factor=default_random_min_factor, initial_random_max_factor=default_random_max_factor,
            initial_maximal_failed_time=default_maximal_failed_time, dynamic_constraint_index_dict=None,
            numeric_eps=eps, verbose=False):
        if dynamic_constraint_index_dict is None:
            dynamic_constraint_index_dict = {}
        super().__init__(
            variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, projection_matrix, thinning,
            initial_random_min_factor, initial_random_max_factor, initial_maximal_failed_time,
            dynamic_constraint_index_dict=dynamic_constraint_index_dict, numeric_eps=numeric_eps, verbose=verbose)
        self.current_sample_num = None  # Need refresh
        self.current_sum_vector = None  # Need refresh
        self.current_center = None  # Need refresh
        # self.total_output_sample_list = []  # Need refresh

        self.maximal_sample_index = 10000
        self.saved_sample_num = 200
        self.saved_sample_update_rate = 0.05
        # self.saved_sample_list = list(self.warmup_array)
        self.saved_sample_list = []  # Need refresh
        OptGpSampler.refresh(self)

    def refresh(self):
        super().refresh()
        self.current_sample_num = self.warmup_num
        self.current_sum_vector = np.sum(self.warmup_array, axis=0)
        self.current_center = self.current_sum_vector / self.current_sample_num
        # self.total_output_sample_list = []

        self.saved_sample_list = list(self.warmup_array)

    def _random_center_unit_direction(self):
        raw_direction = self.saved_sample_list[np.random.randint(len(self.saved_sample_list))] - self.current_center
        # Numpy will deal with this vector product automatically
        projected_direction = self.projection_matrix @ raw_direction
        unit_direction = projected_direction / np.linalg.norm(projected_direction)
        return unit_direction

    def _update_center(self, new_sample_point):
        self.current_sample_num += 1
        self.current_sum_vector += new_sample_point
        self.current_center = self.current_sum_vector / self.current_sample_num

    def _trace_back_center(self, added_sample_point):
        self.current_sample_num -= 1
        self.current_sum_vector -= added_sample_point
        self.current_center = self.current_sum_vector / self.current_sample_num

    def _update_saved_sample(self, new_sample_point):
        if len(self.saved_sample_list) < self.saved_sample_num:
            self.saved_sample_list.append(new_sample_point)
        else:
            if np.random.random() < self.saved_sample_update_rate:
                self.saved_sample_list[np.random.randint(len(self.saved_sample_list))] = new_sample_point

    def _new_step(self, current_location):
        final_next_location = None
        # Add a trace back mechanism
        for _ in range(self.maximal_trial_num):
            random_unit_direction = self._random_center_unit_direction()
            direction_range = calculate_direction_range(
                current_location, random_unit_direction, self.min_value_vector, self.max_value_vector,
                self.smaller_eq_matrix, self.smaller_eq_right_side_vector, self.numeric_eps)
            if direction_range is None:
                continue
            random_range = np.random.random() * direction_range * self.maximal_range_ratio
            next_location = current_location + random_unit_direction * random_range
            valid_new_location = check_new_location(
                next_location, self.min_value_vector, self.max_value_vector,
                self.smaller_eq_matrix, self.smaller_eq_right_side_vector, self.numeric_eps)
            if valid_new_location:
                final_next_location = next_location
                break
        return final_next_location

    def _store_current_location(self, current_location, sample_index=None):
        self._update_center(current_location)
        self._update_saved_sample(current_location)
        if sample_index is None or sample_index % self.recent_points_store_interval == 0:
            self.recent_points_circular_queue.push(current_location)

    def _trace_back(self):
        if self.recent_points_circular_queue.is_empty():
            return None
        current_point = self.recent_points_circular_queue.tail_out()
        self._trace_back_center(current_point)
        return current_point

    def sample(self, n=1):
        super(OptGpSampler, self).sample(n)
        output_sample_list = []
        thinning_value = self.thinning
        current_point = self.random_warmup_point()
        sample_index = 1
        while len(output_sample_list) < n:
            if sample_index % thinning_value == 0:
                output_sample_list.append(current_point)
            new_sample_point = self._new_step(current_point)
            if new_sample_point is None:
                current_point = self._trace_back()
            else:
                self._store_current_location(current_point, sample_index)
                current_point = new_sample_point
                sample_index += 1
            if current_point is None or sample_index >= self.maximal_sample_index:
                sample_index = 0
                current_point = self.random_warmup_point()
        return output_sample_list


# Deprecated
class CHRRSampler(HRSampler):
    def __init__(
            self, variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, projection_matrix, thinning=50,
            initial_random_min_factor=default_random_min_factor, initial_random_max_factor=default_random_max_factor,
            initial_maximal_failed_time=default_maximal_failed_time, numeric_eps=eps, verbose=False):
        super().__init__(
            variable_num, eq_matrix, eq_right_side_vector, smaller_eq_matrix, smaller_eq_right_side_vector,
            min_value_vector, max_value_vector, projection_matrix, thinning=thinning,
            initial_random_min_factor=initial_random_min_factor, initial_random_max_factor=initial_random_max_factor,
            initial_maximal_failed_time=initial_maximal_failed_time, numeric_eps=numeric_eps, verbose=verbose)
        pass

