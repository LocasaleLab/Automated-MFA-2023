from ..common.packages import np
from ..common.classes import default_transform_dict, DefaultDict
from ..common.config import CoreConstants
from ..common.functions import np_list_conv, compartmental_mid_name_constructor, tissue_specific_name_constructor


class InputMetaboliteData(object):
    def __init__(self, metabolite_name, c13_ratio_abundance_list=None, carbon_num=None):
        """
        If c13_ratio_abundance_list is not set, then carbon_num is required and this input metabolite will be regarded
        as unlabeled.
        :param metabolite_name: Metabolite name.
        :param c13_ratio_abundance_list: Ratio list of 13C for each carbon in this metabolite.
        :param carbon_num: Number of carbon atom in this metabolite.
        """
        self.name = metabolite_name
        if c13_ratio_abundance_list is None:
            if carbon_num is None:
                raise ValueError(
                    'Carbon number is not set for unlabeled input metabolite! {}'.format(metabolite_name))
            c13_ratio_list = [np.array([CoreConstants.natural_c13_ratio] * carbon_num)]
            normalized_abundance_list = np.array([1])
        else:
            self.distribution_num = len(c13_ratio_abundance_list)
            c13_ratio_list = []
            abundance_list = []
            carbon_num = -1
            for data_dict in c13_ratio_abundance_list:
                current_ratio_list = data_dict['ratio_list']
                if carbon_num != -1:
                    if carbon_num != len(current_ratio_list):
                        raise ValueError(
                            'InputMetabolite_init: Not valid 13C ratio list: {}'.format(current_ratio_list))
                else:
                    carbon_num = len(current_ratio_list)
                c13_ratio_list.append(np.array(current_ratio_list))
                abundance_list.append(data_dict['abundance'])
            if abs(sum(abundance_list) - 1) > 1e-3:
                normalized_abundance_list = None
                raise ValueError(
                    'InputMetabolite_init: Not valid abundance distribution: {}'.format(abundance_list))
            else:
                abundance_list = np.array(abundance_list)
                normalized_abundance_list = abundance_list / np.sum(abundance_list)
        self.c13_ratio_list = c13_ratio_list
        self.abundance_list = normalized_abundance_list
        self.carbon_num = carbon_num

    def __hash__(self):
        return self.name.__hash__()

    def generate_mid_vector(self, emu_selected_carbon_list):
        final_mid_vector = None
        for c13_ratio_vector, abundance in zip(self.c13_ratio_list, self.abundance_list):
            convolution_list = []
            for carbon_index, selection_indicator in enumerate(emu_selected_carbon_list):
                if selection_indicator == 1:
                    c13_ratio = c13_ratio_vector[carbon_index]
                    convolution_list.append(np.array([1 - c13_ratio, c13_ratio]))
            new_mid_array = np_list_conv(convolution_list)
            if final_mid_vector is None:
                final_mid_vector = new_mid_array * abundance
            else:
                final_mid_vector += new_mid_array * abundance
        return final_mid_vector / np.sum(final_mid_vector)


def vector_normalize(raw_data_vector, eps_for_mid, metabolite_name=None, total_sum_threshold=None, warn_func=None):
    raw_data_sum = np.sum(raw_data_vector)
    # data_length = len(raw_data_vector)
    correct_sum = raw_data_sum * (1 + eps_for_mid)
    if correct_sum < 1000 * eps_for_mid or (total_sum_threshold is not None and correct_sum < total_sum_threshold):
        if warn_func is not None:
            warn_func('[Normalization] Data from {} is left out'.format(metabolite_name))
        return None
    return (raw_data_vector + raw_data_sum * eps_for_mid) / correct_sum
    # return (raw_data_vector + raw_data_sum / data_length * eps_for_mid) / correct_sum


class MIDData(object):
    def __init__(
            self, raw_data_list=None, raw_data_vector: np.ndarray = None, raw_name: str = None,
            data_vector: np.ndarray = None, combined_raw_name_list=(), compartment_list=None,
            tissue_list=None, to_standard_name_dict=None, ms_total_sum_threshold=None, excluded_from_mfa=False):
        if to_standard_name_dict is None:
            to_standard_name_dict = default_transform_dict
        combined = False
        if len(combined_raw_name_list) != 0:
            sorted_combined_name_list = sorted([to_standard_name_dict[name] for name in combined_raw_name_list])
            metabolite_name = CoreConstants.standard_metabolite_sep.join(sorted_combined_name_list)
            combined = True
            combined_standard_name_list = sorted_combined_name_list
        else:
            if raw_name is None:
                raise ValueError('Name must be given for non-combined MID model!')
            metabolite_name = to_standard_name_dict[raw_name]
            combined_standard_name_list = ()
        if raw_data_list is not None:
            true_raw_data_vector = np.array(raw_data_list)
            carbon_num = len(true_raw_data_vector) - 1
        elif raw_data_vector is not None:
            true_raw_data_vector = raw_data_vector
            carbon_num = len(true_raw_data_vector) - 1
        elif data_vector is not None:
            true_raw_data_vector = None
            carbon_num = len(data_vector) - 1
        else:
            raise ValueError('One of raw_data_list and raw_data_vector should be fed')
        if compartment_list is None:
            raise ValueError('Compartment is not specified')
        if tissue_list is None:
            tissue_list = (None,)

        self.combined = combined
        self.combined_standard_name_list = combined_standard_name_list
        self.raw_data_vector = true_raw_data_vector
        self.carbon_num = carbon_num
        self.data_vector = data_vector
        self.compartment = compartment_list
        self.tissue = tissue_list
        self.name = metabolite_name
        self.to_standard_name_dict = to_standard_name_dict
        self.ms_total_sum_threshold = ms_total_sum_threshold
        if len(compartment_list) > 1 or compartment_list[0] is None:
            compartment_list = None
        self.full_name = compartmental_mid_name_constructor(
            tissue_specific_name_constructor(metabolite_name, tissue_list),
            compartment_list)
        self.excluded_from_mfa = excluded_from_mfa

    def exclude_this_mid(self):
        self.excluded_from_mfa = True

    def normalize(self, eps_for_mid=CoreConstants.eps_for_mid):
        if self.data_vector is None and self.raw_data_vector is not None:
            normalized_data_array = vector_normalize(
                self.raw_data_vector, eps_for_mid, self.name, total_sum_threshold=self.ms_total_sum_threshold,
                warn_func=print)
            if normalized_data_array is not None:
                self.data_vector = normalized_data_array
                return True
        return False

    def copy(self):
        new_mid_data_obj = MIDData(
            raw_data_vector=np.copy(self.raw_data_vector),
            raw_name=self.name, combined_raw_name_list=list(self.combined_standard_name_list),
            compartment_list=self.compartment, tissue_list=self.tissue,
            to_standard_name_dict=self.to_standard_name_dict, ms_total_sum_threshold=self.ms_total_sum_threshold)
        if self.data_vector is not None:
            new_mid_data_obj.data_vector = self.data_vector
        return new_mid_data_obj

    def __repr__(self):
        if self.compartment is not None:
            name_str = '{}__{}'.format(self.name, self.compartment)
        else:
            name_str = self.name
        if self.data_vector is not None:
            data_str = self.data_vector.__repr__()
        else:
            data_str = self.raw_data_vector.__repr__()
        return '{}: {}'.format(name_str, data_str)


def average_multiple_mid_data(mid_data_list, output_std=False):
    first_mid_obj = mid_data_list[0]
    num_mid_obj = len(mid_data_list)
    assert first_mid_obj.data_vector is not None
    data_vector_list = [first_mid_obj.data_vector]
    complete_data_vector = np.copy(first_mid_obj.data_vector)
    common_name = first_mid_obj.name
    common_combined_standard_name_list = first_mid_obj.combined_standard_name_list
    common_compartment = first_mid_obj.compartment
    common_tissue = first_mid_obj.tissue
    for new_mid_obj in mid_data_list[1:]:
        assert new_mid_obj.name == common_name
        assert new_mid_obj.combined_standard_name_list == common_combined_standard_name_list
        assert new_mid_obj.compartment == common_compartment
        assert new_mid_obj.tissue == common_tissue
        assert new_mid_obj.data_vector is not None
        complete_data_vector += new_mid_obj.data_vector
        data_vector_list.append(new_mid_obj.data_vector)
    final_data_vector = complete_data_vector / num_mid_obj
    new_mid_data_obj = MIDData(
        raw_name=common_name,
        data_vector=final_data_vector, combined_raw_name_list=common_combined_standard_name_list,
        compartment_list=common_compartment,
        tissue_list=common_tissue, to_standard_name_dict=first_mid_obj.to_standard_name_dict,
        ms_total_sum_threshold=first_mid_obj.ms_total_sum_threshold)
    if not output_std:
        return new_mid_data_obj
    else:
        std_data_vector = np.std(data_vector_list, axis=0)
        return new_mid_data_obj, std_data_vector


class MFAData(object):
    def __init__(
            self, data_name, experimental_mid_data_obj_dict, input_metabolite_obj_data_dict,
            combined_data=False, ratio_dict_to_objective_func=None):
        self.data_name = data_name
        self.experimental_mid_data_obj_dict = experimental_mid_data_obj_dict
        self.input_metabolite_obj_data_dict = input_metabolite_obj_data_dict
        self.combined_data = combined_data
        if combined_data:
            list_of_case_name = list(experimental_mid_data_obj_dict.keys())
            example_mid_data_obj_key = list_of_case_name[0]
            mid_data_obj_dict_for_construction = experimental_mid_data_obj_dict[example_mid_data_obj_key]
            if ratio_dict_to_objective_func is None:
                ratio_dict_to_objective_func = DefaultDict(default_value=1)
        else:
            list_of_case_name = [data_name]
            mid_data_obj_dict_for_construction = experimental_mid_data_obj_dict
        self.ratio_dict_to_objective_func = ratio_dict_to_objective_func
        self.list_of_case_name = list_of_case_name
        self.mid_data_obj_dict_for_construction = mid_data_obj_dict_for_construction


def average_multiple_mfa_data(mfa_data_list, output_std=False, common_data_name=None):
    def average_experimental_mid_data_obj_dict(mid_data_obj_dict_list):
        mid_data_obj_list_dict = {}
        for mid_data_obj_dict in mid_data_obj_dict_list:
            for mid_name, mid_data_obj in mid_data_obj_dict.items():
                if mid_name not in mid_data_obj_list_dict:
                    mid_data_obj_list_dict[mid_name] = []
                mid_data_obj_list_dict[mid_name].append(mid_data_obj)
        mean_mid_data_obj_dict = {}
        std_mid_data_vector_dict = {}
        for mid_name, mid_data_obj_list in mid_data_obj_list_dict.items():
            new_mid_data_obj, std_data_vector = average_multiple_mid_data(mid_data_obj_list, output_std=True)
            mean_mid_data_obj_dict[mid_name] = new_mid_data_obj
            std_mid_data_vector_dict[mid_name] = std_data_vector
        return mean_mid_data_obj_dict, std_mid_data_vector_dict

    first_mfa_obj = mfa_data_list[0]
    assert len(first_mfa_obj.experimental_mid_data_obj_dict) != 0
    mid_data_obj_dict_list = [first_mfa_obj.experimental_mid_data_obj_dict]
    if common_data_name is None:
        common_data_name = 'Average'
    common_input_metabolite_obj_data_dict = first_mfa_obj.input_metabolite_obj_data_dict
    common_combined_data = first_mfa_obj.combined_data
    common_ratio_dict_to_objective_func = first_mfa_obj.ratio_dict_to_objective_func
    common_list_of_case_name = first_mfa_obj.list_of_case_name
    for new_mfa_obj in mfa_data_list[1:]:
        assert new_mfa_obj.input_metabolite_obj_data_dict == common_input_metabolite_obj_data_dict
        assert new_mfa_obj.combined_data == common_combined_data
        if new_mfa_obj.combined_data:
            assert new_mfa_obj.list_of_case_name == common_list_of_case_name
        assert len(new_mfa_obj.experimental_mid_data_obj_dict) != 0
        assert new_mfa_obj.ratio_dict_to_objective_func == common_ratio_dict_to_objective_func
        mid_data_obj_dict_list.append(new_mfa_obj.experimental_mid_data_obj_dict)
    mean_mid_data_obj_dict, std_mid_data_vector_dict = average_experimental_mid_data_obj_dict(mid_data_obj_dict_list)
    new_mfa_data_obj = MFAData(
        common_data_name, mean_mid_data_obj_dict,
        common_input_metabolite_obj_data_dict, combined_data=common_combined_data,
        ratio_dict_to_objective_func=common_ratio_dict_to_objective_func)
    if not output_std:
        return new_mfa_data_obj
    else:
        return new_mfa_data_obj, std_mid_data_vector_dict
