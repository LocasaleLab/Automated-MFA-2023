from .config import Direct
from common_and_plotting_functions.functions import pickle_save, pickle_load, check_and_mkdir_of_direct, npz_load, npz_save
from .built_in_packages import warnings
from .third_party_packages import np
from .functions import mid_name_process


class FinalResult(object):
    def __init__(
            self, project_output_direct, common_data_output_direct, result_name, maximal_save_point=5000,
            suffix=None):
        self.project_output_direct = project_output_direct
        self.project_common_data_output_direct = common_data_output_direct
        self.result_name = result_name

        self.this_result_output_direct = f'{self.project_output_direct}/{self.result_name}'
        self.raw_result_data_output_direct = f'{self.this_result_output_direct}/{Direct.raw_flux_analysis}'
        self.flux_comparison_output_direct = f'{self.this_result_output_direct}/{Direct.flux_comparison}'
        self.mid_prediction_output_direct = f'{self.this_result_output_direct}/' \
                                            f'{Direct.predicted_experimental_mid_comparison_direct}'
        self.metabolic_network_visualization_direct = f'{self.this_result_output_direct}/' \
                                                      f'{Direct.metabolic_network_visualization_direct}'
        self.raw_and_mid_experimental_data_display_direct = f'{self.this_result_output_direct}/' \
                                                            f'{Direct.raw_and_mid_experimental_data_display_direct}'

        self.this_result_submitted_data_output_direct = f'{self.project_common_data_output_direct}/{self.result_name}'
        self.flux_result_output_xlsx_path = f'{self.this_result_submitted_data_output_direct}/' \
                                            f'{Direct.flux_result_xlsx_filename}'
        self.mid_prediction_result_output_xlsx_path = f'{self.this_result_submitted_data_output_direct}/' \
                                                      f'{Direct.mid_result_xlsx_filename}'
        self.solver_descriptions_output_xlsx_path = f'{self.this_result_submitted_data_output_direct}/' \
                                                    f'{Direct.solver_description_xlsx_filename}'

        check_and_mkdir_of_direct(self.raw_result_data_output_direct)
        check_and_mkdir_of_direct(self.flux_comparison_output_direct)
        check_and_mkdir_of_direct(self.mid_prediction_output_direct)
        check_and_mkdir_of_direct(self.metabolic_network_visualization_direct)
        check_and_mkdir_of_direct(self.this_result_submitted_data_output_direct)

        self.target_experimental_mid_data_dict = None
        self.emu_name_experimental_name_dict = None

        self.final_solution_data_dict = {}
        self.final_time_data_dict = {}
        self.final_loss_data_dict = {}
        self.final_predicted_data_dict = {}
        self.final_information_dict = {}
        self.final_flux_name_index_dict = {}
        self.final_target_experimental_mid_data_dict = {}
        self.processed_mid_name_dict = {}
        self.final_solution_id_array_dict = {}

        self.data_count_dict = {}
        assert isinstance(maximal_save_point, int)
        self.maximal_save_point = maximal_save_point
        self.suffix = suffix

    def update_experimental_name_mid_value_dict(
            self, target_experimental_mid_data_dict, emu_name_experimental_name_dict):
        self.target_experimental_mid_data_dict = target_experimental_mid_data_dict
        self.emu_name_experimental_name_dict = emu_name_experimental_name_dict

    def _generate_path_given_result_path(self, current_result_path):
        solution_array_path = '{}/{}'.format(current_result_path, Direct.solution_array)
        time_array_path = '{}/{}'.format(current_result_path, Direct.time_array)
        loss_array_path = '{}/{}'.format(current_result_path, Direct.loss_array)
        predicted_dict_path = '{}/{}'.format(current_result_path, Direct.predicted_dict)
        information_path = '{}/{}'.format(current_result_path, Direct.result_information)
        flux_name_index_dict_path = '{}/{}'.format(current_result_path, Direct.flux_name_index_dict)
        target_experimental_mid_data_dict_path = '{}/{}'.format(current_result_path, Direct.experimental_data)
        return solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path, \
            flux_name_index_dict_path, target_experimental_mid_data_dict_path

    def _generate_path(self, current_result_label):
        current_result_path = '{}/{}'.format(self.raw_result_data_output_direct, current_result_label)
        check_and_mkdir_of_direct(current_result_path)
        return self._generate_path_given_result_path(current_result_path)

    def _generate_solution_id_path(self, current_result_label):
        current_solution_id_array_path = '{}/{}/{}'.format(
            self.raw_result_data_output_direct, current_result_label, Direct.solution_id_array)
        return current_solution_id_array_path

    def _check_and_convert_object_matrix_to_numeric(self, array_path, array_label):
        print(f'{array_label} array of {self.result_name} is not pure number. Checking it...')
        raw_array = npz_load(array_path, array_label, allow_pickle=True)
        new_array = np.zeros_like(raw_array, dtype='float64')
        new_array_list = []
        col_num_row_dict = {}
        col_num = None
        unaligned = False
        for row_index, row in enumerate(raw_array):
            row_array_list = []
            current_col_num = len(row)
            if current_col_num not in col_num_row_dict:
                col_num_row_dict[current_col_num] = []
            col_num_row_dict[current_col_num].append(row_index)
            if col_num is None:
                col_num = len(row)
            else:
                if len(row) != col_num:
                    unaligned = True
                    print(
                        f'Column number of row {row_index} has a different col length {len(row)},'
                        f' does not equal to previous column length {col_num}')
                    col_num = None
            for col_index, value in enumerate(row):
                if not isinstance(value, float):
                    print(row_index, col_index, value)
                    raise ValueError(
                        f'No-number item has been found: row {row_index} col {col_index} with value {value}')
                row_array_list.append(np.float64(value))
                # new_array[row_index, col_index] = value
            new_array_list.append(row_array_list)
        # new_array = np.array(new_array_list, dtype='float64')
        # npz_save(array_path, **{array_label: new_array})
        # print(f'All item is numeric. Converted it to numeric matrix and save.')
        return unaligned, raw_array, col_num_row_dict

    def _repair_solution_data(self, raw_solution_array, col_num, row_index_array):
        row_num = len(row_index_array)
        new_solution_array = np.zeros([row_num, col_num], dtype='float64')
        for new_row_index, previous_row_index in enumerate(row_index_array):
            new_solution_array[new_row_index, :] = raw_solution_array[previous_row_index]
        return new_solution_array

    def _repair_unaligned_data(
            self, col_num_row_range_dict, raw_solution_array,
            solution_array_path, time_array_path, loss_array_path, predicted_dict_path,
            information_path, flux_name_index_dict_path, target_experimental_mid_data_dict_path):
        time_array = npz_load(time_array_path, Direct.time_array)
        loss_array = npz_load(loss_array_path, Direct.loss_array)
        raw_predicted_dict = pickle_load(predicted_dict_path)
        result_information_dict = pickle_load(information_path)
        flux_name_index_dict = pickle_load(flux_name_index_dict_path)
        try:
            raw_target_experimental_mid_data_dict = pickle_load(target_experimental_mid_data_dict_path)
        except FileNotFoundError:
            raw_target_experimental_mid_data_dict = {}
        max_col_num = max(col_num_row_range_dict.keys())
        max_row_index_array = np.array(col_num_row_range_dict[max_col_num])
        modified_solution_array = self._repair_solution_data(raw_solution_array, max_col_num, max_row_index_array)
        modified_time_array, modified_loss_array, modified_predicted_dict = self._slice_data(
            max_row_index_array, time_array, loss_array, raw_predicted_dict)
        npz_save(solution_array_path, **{Direct.solution_array: modified_solution_array})
        npz_save(time_array_path, **{Direct.time_array: modified_time_array})
        npz_save(loss_array_path, **{Direct.loss_array: modified_loss_array})
        pickle_save(modified_predicted_dict, predicted_dict_path)
        pickle_save(result_information_dict, information_path)
        pickle_save(flux_name_index_dict, flux_name_index_dict_path)
        pickle_save(raw_target_experimental_mid_data_dict, target_experimental_mid_data_dict_path)
        return modified_solution_array

    def _repair_predicted_mid_data_dict(self, solver_obj, solution_array):
        new_mid_data_dict = {}
        total_solution_num = solution_array.shape[0]
        for solution_index, solution_vector in enumerate(solution_array):
            calculated_mid_data_dict = solver_obj.predict(solution_vector)
            for mid_name, mid_vector in calculated_mid_data_dict.items():
                if mid_name not in new_mid_data_dict:
                    new_mid_data_dict[mid_name] = []
                new_mid_data_dict[mid_name].append(mid_vector)
            if total_solution_num >= 10000 and solution_index % 2000 == 0:
                print(f'{solution_index} of {total_solution_num} are predicted.')
        return new_mid_data_dict

    @staticmethod
    def add_suffix_to_result_label(raw_result_label, suffix=None):
        if suffix is None:
            return raw_result_label
        else:
            return f'{raw_result_label}_{suffix}'

    def _update_result_label(self, raw_result_label):
        updated_result_label = self.add_suffix_to_result_label(raw_result_label, self.suffix)
        return updated_result_label

    def _load_data(
            self, solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
            flux_name_index_dict_path, target_experimental_mid_data_dict_path):
        try:
            solution_array = npz_load(solution_array_path, Direct.solution_array)
        except ValueError:
            unaligned, raw_solution_array, col_num_row_range_dict = self._check_and_convert_object_matrix_to_numeric(
                solution_array_path, Direct.solution_array)
            if unaligned:
                solution_array = self._repair_unaligned_data(
                    col_num_row_range_dict, raw_solution_array,
                    solution_array_path, time_array_path, loss_array_path, predicted_dict_path,
                    information_path, flux_name_index_dict_path, target_experimental_mid_data_dict_path)
            else:
                raise ValueError()
        time_array = npz_load(time_array_path, Direct.time_array)
        loss_array = npz_load(loss_array_path, Direct.loss_array)
        raw_predicted_dict = pickle_load(predicted_dict_path)
        try:
            result_information_dict = pickle_load(information_path)
        except ValueError:
            result_information_dict = None
        flux_name_index_dict = pickle_load(flux_name_index_dict_path)
        try:
            raw_target_experimental_mid_data_dict = pickle_load(target_experimental_mid_data_dict_path)
        except FileNotFoundError:
            raw_target_experimental_mid_data_dict = {}
        return solution_array, time_array, loss_array, raw_predicted_dict, result_information_dict, \
            flux_name_index_dict, raw_target_experimental_mid_data_dict

    def _load_solution_id(self, solution_id_array_path):
        solution_id_array = npz_load(solution_id_array_path, Direct.solution_id_array)
        return solution_id_array

    def _slice_data(
            self, index_array, final_time_array, final_loss_array,
            final_predicted_dict):
        modified_time_array = final_time_array[index_array]
        modified_loss_array = final_loss_array[index_array]
        modified_predicted_dict = {}
        for emu_name, predicted_vector_list in final_predicted_dict.items():
            modified_predicted_dict[emu_name] = [predicted_vector_list[index] for index in index_array]
        return modified_time_array, modified_loss_array, modified_predicted_dict

    def _save_data(
            self, current_result_label, final_solution_array, final_time_array, final_loss_array,
            final_predicted_dict, current_result_information, flux_name_index_dict, target_experimental_mid_data_dict):
        (
            solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
            flux_name_index_dict_path, target_experimental_mid_data_dict_path) = self._generate_path(
            current_result_label)
        npz_save(solution_array_path, **{Direct.solution_array: final_solution_array})
        npz_save(time_array_path, **{Direct.time_array: final_time_array})
        npz_save(loss_array_path, **{Direct.loss_array: final_loss_array})
        pickle_save(final_predicted_dict, predicted_dict_path)
        pickle_save(current_result_information, information_path)
        pickle_save(flux_name_index_dict, flux_name_index_dict_path)
        pickle_save(target_experimental_mid_data_dict, target_experimental_mid_data_dict_path)

    def _check_dim_of_new_solution_data(self, current_result_label, new_solution_array):
        current_solution_array_list = self.final_solution_data_dict[current_result_label]
        assert new_solution_array.dtype == np.float64 or np.float32
        if len(current_solution_array_list) != 0:
            current_solution_dim = len(current_solution_array_list[0])
            new_solution_dim = len(new_solution_array[0])
            if current_solution_dim != new_solution_dim:
                raise ValueError(
                    f'New solution has different dim {new_solution_dim} '
                    f'that is different from current solution dim {current_solution_dim}\n'
                    f'in result {current_result_label} in experiments {self.result_name}')

    def _merge_to_final_result_dict(
            self, current_result_label, current_solution_array, current_time_array, current_loss_array,
            current_predicted_dict, current_result_information, flux_name_index_dict,
            target_experimental_mid_data_dict):
        if current_result_label not in self.final_solution_data_dict:
            self.final_solution_data_dict[current_result_label] = []
            self.final_time_data_dict[current_result_label] = []
            self.final_loss_data_dict[current_result_label] = []
            self.final_predicted_data_dict[current_result_label] = {}
            self.final_information_dict[current_result_label] = current_result_information
            self.final_flux_name_index_dict[current_result_label] = flux_name_index_dict
            self.final_target_experimental_mid_data_dict[current_result_label] = target_experimental_mid_data_dict
        else:
            self._check_dim_of_new_solution_data(current_result_label, current_solution_array)
        self.final_solution_data_dict[current_result_label].extend(current_solution_array)
        self.final_time_data_dict[current_result_label].extend(current_time_array)
        self.final_loss_data_dict[current_result_label].extend(current_loss_array)
        this_result_predicted_dict = self.final_predicted_data_dict[current_result_label]
        for emu_name, predicted_vector_list in current_predicted_dict.items():
            if emu_name not in this_result_predicted_dict:
                this_result_predicted_dict[emu_name] = []
            this_result_predicted_dict[emu_name].extend(predicted_vector_list)
        if current_result_label not in self.data_count_dict:
            self.data_count_dict[current_result_label] = 0
        self.data_count_dict[current_result_label] += current_solution_array.shape[0]

    def parallel_add_and_save_result(
            self, result_list, raw_result_label, current_result_information, flux_name_index_dict,
            target_experimental_mid_data_dict, start_index, target_total_optimization_num):
        result_label = self._update_result_label(raw_result_label)
        current_solution_array, current_time_array, current_loss_array, current_predicted_dict = result_list
        self._merge_to_final_result_dict(
            result_label, current_solution_array, current_time_array, current_loss_array,
            current_predicted_dict, current_result_information, flux_name_index_dict, target_experimental_mid_data_dict)
        current_data_count = self.data_count_dict[result_label]
        if current_data_count >= target_total_optimization_num or current_data_count % self.maximal_save_point == 0:
            final_solution_array = np.array(self.final_solution_data_dict[result_label])
            final_time_array = np.array(self.final_time_data_dict[result_label])
            final_loss_array = np.array(self.final_loss_data_dict[result_label])
            self._save_data(
                result_label, final_solution_array, final_time_array, final_loss_array,
                self.final_predicted_data_dict[result_label],
                current_result_information, flux_name_index_dict, target_experimental_mid_data_dict)

    def add_and_save_result(
            self, current_result_label, current_result_information, result_list, flux_name_index_dict,
            target_experimental_mid_data_dict):
        final_solution_array, final_time_array, final_loss_array, final_predicted_dict = result_list
        self._save_data(
            current_result_label, final_solution_array, final_time_array, final_loss_array,
            final_predicted_dict, current_result_information, flux_name_index_dict, target_experimental_mid_data_dict)

    def iteration(self, raw_result_label, process_mid_name=True, result_label_suffix_tuple=()):
        # def mid_name_process(raw_mid_name):
        #     emu_sep = CoreConstants.emu_carbon_list_str_sep
        #     modified_str_list = []
        #     str_start = 0
        #     while True:
        #         emu_location = raw_mid_name.find(emu_sep, str_start)
        #         if emu_location == -1:
        #             break
        #         modified_str_list.append(raw_mid_name[str_start:emu_location])
        #         new_start = emu_location + len(emu_sep)
        #         while new_start != len(raw_mid_name) and raw_mid_name[new_start] == '1':
        #             new_start += 1
        #         str_start = new_start
        #     modified_str = ''.join(modified_str_list)
        #     return modified_str
        if len(result_label_suffix_tuple) == 0:
            with_suffix = False
            result_label_suffix_tuple = (None,)
        else:
            with_suffix = True
        loss_array_list = []
        time_array_list = []
        solution_array_list = []
        flux_name_index_dict = None
        processed_mid_name_dict = self.processed_mid_name_dict
        predicted_data_dict = {}
        target_experimental_mid_data_dict = {}
        result_information_dict = None

        for result_label_suffix in result_label_suffix_tuple:
            result_label = self.add_suffix_to_result_label(raw_result_label, result_label_suffix)

            (
                solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
                flux_name_index_dict_path, target_experimental_mid_data_dict_path) = self._generate_path(
                result_label)
            try:
                (
                    tmp_solution_array, tmp_time_array, tmp_loss_array, tmp_raw_predicted_dict,
                    tmp_result_information_dict, tmp_flux_name_index_dict, tmp_raw_target_experimental_mid_data_dict
                ) = self._load_data(
                    solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
                    flux_name_index_dict_path, target_experimental_mid_data_dict_path)
            except FileNotFoundError:
                continue
            print(f'Load data set named as {result_label} with {tmp_loss_array.shape[0]} items')
            if flux_name_index_dict is None:
                flux_name_index_dict = tmp_flux_name_index_dict
            else:
                assert flux_name_index_dict == tmp_flux_name_index_dict
            if result_information_dict is None:
                result_information_dict = tmp_result_information_dict
            else:
                assert result_information_dict == tmp_result_information_dict

            if not with_suffix:
                loss_array_list = tmp_loss_array
                time_array_list = tmp_time_array
                solution_array_list = tmp_solution_array
            else:
                loss_array_list.append(tmp_loss_array)
                time_array_list.append(tmp_time_array)
                solution_array_list.append(tmp_solution_array)

            for mid_name, mid_value in tmp_raw_predicted_dict.items():
                if process_mid_name:
                    if mid_name not in processed_mid_name_dict:
                        processed_mid_name = mid_name_process(mid_name)
                        processed_mid_name_dict[mid_name] = processed_mid_name
                    else:
                        processed_mid_name = processed_mid_name_dict[mid_name]
                else:
                    processed_mid_name = mid_name
                if processed_mid_name not in predicted_data_dict:
                    predicted_data_dict[processed_mid_name] = []
                predicted_data_dict[processed_mid_name].extend(mid_value)
            for raw_mid_name, experimental_mid_data in tmp_raw_target_experimental_mid_data_dict.items():
                if raw_mid_name in predicted_data_dict:
                    processed_mid_name = raw_mid_name
                elif raw_mid_name in processed_mid_name_dict:
                    processed_mid_name = processed_mid_name_dict[raw_mid_name]
                else:
                    processed_mid_name = raw_mid_name
                if processed_mid_name not in target_experimental_mid_data_dict:
                    target_experimental_mid_data_dict[processed_mid_name] = experimental_mid_data
                else:
                    assert np.all(experimental_mid_data == target_experimental_mid_data_dict[processed_mid_name])

            # if process_mid_name:
            #     processed_mid_name_dict = {}
            #     predicted_data_dict = {}
            #     for mid_name, mid_value in raw_predicted_dict.items():
            #         if mid_name not in processed_mid_name_dict:
            #             processed_mid_name = mid_name_process(mid_name)
            #             processed_mid_name_dict[mid_name] = processed_mid_name
            #         else:
            #             processed_mid_name = processed_mid_name_dict[mid_name]
            #         predicted_data_dict[processed_mid_name] = mid_value
            #     target_experimental_mid_data_dict = {}
            #     for raw_mid_name, experimental_mid_data in raw_target_experimental_mid_data_dict.items():
            #         if raw_mid_name in predicted_data_dict:
            #             processed_mid_name = raw_mid_name
            #         elif raw_mid_name in processed_mid_name_dict:
            #             processed_mid_name = processed_mid_name_dict[raw_mid_name]
            #         else:
            #             raise ValueError()
            #         target_experimental_mid_data_dict[processed_mid_name] = experimental_mid_data
            # else:
            #     predicted_data_dict = raw_predicted_dict
            #     # target_experimental_mid_data_dict = {}
            #     # for raw_mid_name in raw_predicted_dict.keys():
            #     #     processed_mid_name = mid_name_process(raw_mid_name)
            #     #     if processed_mid_name in raw_target_experimental_mid_data_dict:
            #     #         target_experimental_mid_data_dict[raw_mid_name] = raw_target_experimental_mid_data_dict[
            #     #             processed_mid_name]
            #     target_experimental_mid_data_dict = raw_target_experimental_mid_data_dict

        if with_suffix:
            loss_array = np.concatenate(loss_array_list)
            time_array = np.concatenate(time_array_list)
            solution_array = np.vstack(solution_array_list)
        else:
            loss_array = loss_array_list
            time_array = time_array_list
            solution_array = solution_array_list
        return loss_array, solution_array, flux_name_index_dict, result_information_dict, predicted_data_dict, \
            target_experimental_mid_data_dict, time_array

    def share_data(self, other_final_result_obj):
        (
            self.final_loss_data_dict, self.final_solution_data_dict,
            self.final_flux_name_index_dict,
            self.final_information_dict,
            self.final_predicted_data_dict,
            self.final_target_experimental_mid_data_dict,
            self.final_time_data_dict
        ) = (
            other_final_result_obj.final_loss_data_dict, other_final_result_obj.final_solution_data_dict,
            other_final_result_obj.final_flux_name_index_dict,
            other_final_result_obj.final_information_dict,
            other_final_result_obj.final_predicted_data_dict,
            other_final_result_obj.final_target_experimental_mid_data_dict,
            other_final_result_obj.final_time_data_dict
        )

    def load_current_result_label(self, result_label):
        (
            self.final_loss_data_dict[result_label], self.final_solution_data_dict[result_label],
            self.final_flux_name_index_dict[result_label],
            self.final_information_dict[result_label],
            self.final_predicted_data_dict[result_label],
            self.final_target_experimental_mid_data_dict[result_label],
            self.final_time_data_dict[result_label]
        ) = self.iteration(result_label)

    def load_previous_results(self, raw_result_label):
        result_label = self._update_result_label(raw_result_label)
        (
            solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
            flux_name_index_dict_path, target_experimental_mid_data_dict_path) = self._generate_path(result_label)
        try:
            (
                solution_array, time_array, loss_array, raw_predicted_dict, result_information_dict,
                flux_name_index_dict, raw_target_experimental_mid_data_dict) = self._load_data(
                solution_array_path, time_array_path, loss_array_path, predicted_dict_path, information_path,
                flux_name_index_dict_path, target_experimental_mid_data_dict_path)
        except FileNotFoundError:
            warnings.warn('Cannot find any previous data with label: {}'.format(result_label))
            return 0
        else:
            solution_id_array_path = self._generate_solution_id_path(result_label)
            try:
                solution_id_array = self._load_solution_id(solution_id_array_path)
            except FileNotFoundError:
                self._merge_to_final_result_dict(
                    result_label, solution_array, time_array, loss_array, raw_predicted_dict, result_information_dict,
                    flux_name_index_dict, raw_target_experimental_mid_data_dict)
            else:
                self._merge_to_final_result_dict_with_solution_id(
                    result_label, solution_array, time_array, loss_array, raw_predicted_dict, result_information_dict,
                    flux_name_index_dict, raw_target_experimental_mid_data_dict, solution_id_array)
            return self.data_count_dict[result_label]

    def repair_predicted_mid_dict_and_merge(self, solver_dict):
        for result_label, solver_obj in solver_dict.items():
            loss_array, solution_array, flux_name_index_dict, result_information_dict, predicted_data_dict, \
                target_experimental_mid_data_dict, time_array = self.iteration(result_label, process_mid_name=False)
            new_predicted_data_dict = self._repair_predicted_mid_data_dict(solver_obj, solution_array)
            replaced_mid_count = 0
            total_mid_count = None
            for raw_mid_name, old_mid_vector_list in predicted_data_dict.items():
                if total_mid_count is None:
                    total_mid_count = len(old_mid_vector_list)
                current_replaced_mid = 0
                modified_mid_vector_list = new_predicted_data_dict[raw_mid_name]
                for old_mid_vector, modified_mid_vector in zip(old_mid_vector_list, modified_mid_vector_list):
                    if np.any(np.abs(old_mid_vector - modified_mid_vector) > 1e-10):
                        current_replaced_mid += 1
                replaced_mid_count = np.maximum(replaced_mid_count, current_replaced_mid)
            print(
                f'{result_label}: {replaced_mid_count} MID replaced. '
                f'{total_mid_count - replaced_mid_count} MID not replaced')
            if replaced_mid_count > 0:
                print(f'Update {result_label} MID files')
                self._save_data(
                    result_label, solution_array, time_array, loss_array, new_predicted_data_dict,
                    result_information_dict, flux_name_index_dict, target_experimental_mid_data_dict)

    def repair_target_experimental_mid_data_dict(self, solver_dict):
        for result_label, solver_obj in solver_dict.items():
            loss_array, solution_array, flux_name_index_dict, result_information_dict, predicted_data_dict, \
                target_experimental_mid_data_dict, time_array = self.iteration(result_label, process_mid_name=False)
            new_target_experimental_mid_data_dict = {}
            for raw_target_mid_name, experimental_mid_data_vector in target_experimental_mid_data_dict.items():
                last_underline_index = raw_target_mid_name.rindex('_')
                mid_name = raw_target_mid_name[:last_underline_index]
                case_name = raw_target_mid_name[last_underline_index + 1:]
                new_target_mid_name = f'{case_name}_{mid_name}'
                new_target_experimental_mid_data_dict[new_target_mid_name] = experimental_mid_data_vector
            self._save_data(
                result_label, solution_array, time_array, loss_array, predicted_data_dict,
                result_information_dict, flux_name_index_dict, new_target_experimental_mid_data_dict)

    @staticmethod
    def process_existing_new_id_array(existing_id_array, new_id_array):
        if existing_id_array is None:
            complete_id_array = new_id_array
        else:
            complete_id_array = np.concatenate([existing_id_array, new_id_array])
        sorted_index = np.argsort(complete_id_array)
        sorted_complete_id_array = complete_id_array[sorted_index]
        return sorted_index, sorted_complete_id_array

    def _merge_to_final_result_dict_with_solution_id(
            self, current_result_label, current_solution_array, current_time_array, current_loss_array,
            current_predicted_dict, current_result_information, flux_name_index_dict,
            target_experimental_mid_data_dict, solution_id_array):
        if current_result_label in self.final_solution_data_dict:
            self._check_dim_of_new_solution_data(current_result_label, current_solution_array)
            existing_id_array = self.final_solution_id_array_dict[current_result_label]
            complete_solution_array = np.concatenate([
                self.final_solution_data_dict[current_result_label], current_solution_array])
            complete_time_array = np.concatenate([
                self.final_time_data_dict[current_result_label], current_time_array])
            complete_loss_array = np.concatenate([
                self.final_loss_data_dict[current_result_label], current_loss_array])
        else:
            existing_id_array = None
            self.final_information_dict[current_result_label] = current_result_information
            self.final_flux_name_index_dict[current_result_label] = flux_name_index_dict
            self.final_target_experimental_mid_data_dict[current_result_label] = target_experimental_mid_data_dict
            complete_solution_array = current_solution_array
            complete_time_array = current_time_array
            complete_loss_array = current_loss_array
            self.final_predicted_data_dict[current_result_label] = {}
        # if current_result_label not in self.final_solution_data_dict:
        #     self.final_solution_data_dict[current_result_label] = current_solution_array
        #     self.final_time_data_dict[current_result_label] = current_time_array
        #     self.final_loss_data_dict[current_result_label] = current_loss_array
        #     self.final_predicted_data_dict[current_result_label] = current_predicted_dict
        #     self.final_information_dict[current_result_label] = current_result_information
        #     self.final_flux_name_index_dict[current_result_label] = flux_name_index_dict
        #     self.final_target_experimental_mid_data_dict[current_result_label] = target_experimental_mid_data_dict
        #     self.final_solution_id_array_dict[current_result_label] = solution_id_array
        # else:
        #     self._check_dim_of_new_solution_data(current_result_label, current_solution_array)
        #     existing_id_array = self.final_solution_id_array_dict[current_result_label]
        sorted_index, self.final_solution_id_array_dict[current_result_label] = self.process_existing_new_id_array(
            existing_id_array, solution_id_array)
        # self.final_solution_data_dict[current_result_label] = np.concatenate([
        #     self.final_solution_data_dict[current_result_label], current_solution_array])[sorted_index]
        # self.final_loss_data_dict[current_result_label] = np.concatenate([
        #     self.final_loss_data_dict[current_result_label], current_loss_array])[sorted_index]
        # self.final_time_data_dict[current_result_label] = np.concatenate([
        #     self.final_time_data_dict[current_result_label], current_time_array])[sorted_index]
        self.final_solution_data_dict[current_result_label] = complete_solution_array[sorted_index]
        self.final_loss_data_dict[current_result_label] = complete_loss_array[sorted_index]
        self.final_time_data_dict[current_result_label] = complete_time_array[sorted_index]
        this_result_predicted_dict = self.final_predicted_data_dict[current_result_label]
        for emu_name, predicted_vector_list in current_predicted_dict.items():
            if emu_name not in this_result_predicted_dict:
                this_result_predicted_dict[emu_name] = np.array(predicted_vector_list)[sorted_index]
            else:
                this_result_predicted_dict[emu_name] = np.concatenate([
                    this_result_predicted_dict[emu_name], predicted_vector_list])[sorted_index]
        if current_result_label not in self.data_count_dict:
            self.data_count_dict[current_result_label] = 0
        self.data_count_dict[current_result_label] += current_solution_array.shape[0]

    def _save_solution_id(self, current_result_label, solution_id_array):
        current_solution_id_array_path = self._generate_solution_id_path(current_result_label)
        npz_save(current_solution_id_array_path, **{Direct.solution_id_array: solution_id_array})

    def final_process(self, *args):
        pass
