from scripts.src.core.common.functions import natural_dist
from scripts.src.core.common.classes import CoreConstants
from scripts.src.core.data.data_class import MIDData, vector_normalize

from scripts.src.common.built_in_packages import warnings
from scripts.src.common.third_party_packages import np


class CompleteDataset(object):
    def __init__(self):
        self.complete_dataset = {}
        self.test_data = False
        self.anti_correction = False
        self._complete_data_parameter_dict_dict = None
        self._test_data_parameter_dict_dict = None

    def set_data_status(self, test_data=False):
        self.test_data = test_data

    def set_anti_correction(self, anti_correction=False):
        self.anti_correction = anti_correction

    def add_data_sheet(self, sheet_name, current_data_dict):
        pass

    def return_data_parameter_dict(self):
        if self.test_data:
            return self._test_data_parameter_dict_dict
        else:
            return self._complete_data_parameter_dict_dict

    def _complete_return_dataset(self, param_dict):
        pass

    def _test_return_dataset(self):
        pass

    def return_dataset(self, param_dict):
        if self.test_data:
            return self._test_return_dataset()
        else:
            return self._complete_return_dataset(param_dict)


class NaturalDistDict(dict):
    def __init__(self, *args, **kwargs):
        super(NaturalDistDict, self).__init__(*args, **kwargs)

    def __getitem__(self, item):
        if item not in self:
            new_natural_dist = natural_dist(item)
            self.__setitem__(item, new_natural_dist)
        return super(NaturalDistDict, self).__getitem__(item)


natural_dist_dict = NaturalDistDict()


def natural_distribution_anti_correction(raw_data_dict):
    for metabolite, corrected_mid_data_obj in raw_data_dict.items():
        current_natural_dist = natural_dist_dict[corrected_mid_data_obj.carbon_num].copy()
        corrected_data_vector = corrected_mid_data_obj.data_vector
        zero_item = current_natural_dist[0]
        current_natural_dist[0] = 0
        raw_data_array = corrected_data_vector * zero_item + current_natural_dist
        corrected_mid_data_obj.data_vector = raw_data_array


def normalize_negative_data_array(raw_data_array):
    minimal_abs = -np.min(raw_data_array)
    new_data_array = raw_data_array + minimal_abs
    normalized_new_data_array = vector_normalize(new_data_array, CoreConstants.eps_for_mid)
    return normalized_new_data_array


def check_negative_data_array(input_data_dict, label_list):
    for data_name, data_content in input_data_dict.items():
        if isinstance(data_content, dict):
            label_list.append(data_name)
            check_negative_data_array(data_content, label_list)
            label_list.pop()
        elif isinstance(data_content, MIDData):
            if np.any(data_content.data_vector < 0):
                previous_data_vector = data_content.data_vector
                new_data_vector = normalize_negative_data_array(previous_data_vector)
                data_content.data_vector = new_data_vector
                warnings.warn(
                    (
                        'Negative MID data!\nData name: {}\nData array name: {}\n'
                        'Previous data array value: {}\nModified data array value: {}').format(
                        '_'.join(label_list), data_content.name, previous_data_vector, new_data_vector))
        else:
            raise TypeError('Type not recognized!')

