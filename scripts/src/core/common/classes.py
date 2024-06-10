from .config import CoreConstants
from .packages import copy


class DictList(object):
    def __init__(self, raw_list=None, key_index_dict=None):
        if raw_list is None:
            raw_list = []
            key_index_dict = {}
        self.raw_list = raw_list
        self.key_index_dict = key_index_dict

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.raw_list[item]
        else:
            return self.raw_list[self.key_index_dict[item]]

    def __setitem__(self, key, value):
        if key in self.key_index_dict:
            current_index = self.key_index_dict[key]
            if self.raw_list[current_index] is None:
                self.raw_list[current_index] = value
        else:
            self.key_index_dict[key] = len(self.raw_list)
            self.raw_list.append(value)

    def add(self, key):
        if key not in self.key_index_dict:
            self.key_index_dict[key] = len(self.raw_list)
            self.raw_list.append(None)

    def index(self, key):
        return self.key_index_dict[key]

    def items(self):
        sorted_key_list = sorted(self.key_index_dict.keys(), key=lambda x: self.key_index_dict[x])
        return zip(sorted_key_list, self.raw_list)

    def __len__(self):
        return self.raw_list.__len__()

    def __contains__(self, item):
        return self.key_index_dict.__contains__(item)

    def __iter__(self):
        return self.raw_list.__iter__()

    def __repr__(self):
        new_list = [''] * len(self.raw_list)
        for key, index in self.key_index_dict.items():
            new_list[index] = '{}: {}'.format(key, self.raw_list[index])
        return ", ".join(new_list)

    def __str__(self):
        return self.__repr__()

    def __copy__(self):
        return DictList(list(self.raw_list), dict(self.key_index_dict))

    def copy(self):
        return self.__copy__()


class CircularQueue(list):
    def __init__(self, max_size):
        real_max_size = max_size + 1
        super(CircularQueue, self).__init__([0] * real_max_size)
        self.max_size = real_max_size
        self.head = 0
        self.tail = 0

    def is_empty(self):
        return self.head == self.tail

    def push(self, item):
        self[self.tail] = item
        self.tail = (self.tail + 1) % self.max_size
        if self.tail == self.head:
            self.head = (self.head + 1) % self.max_size

    def tail_peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty!")
        return self[self.tail - 1]

    def tail_out(self):
        if self.is_empty():
            raise IndexError("Queue is empty!")
        item = self[self.tail - 1]
        self.tail = (self.tail - 1) % self.max_size
        return item

    def front_peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty!")
        return self[self.head]

    def front_out(self):
        if self.is_empty():
            raise IndexError("Queue is empty!")
        item = self[self.head]
        self.head = (self.head + 1) % self.max_size
        return item

    # def __getitem__(self, item):
    #     raise AttributeError('Cannot visit it directly!')
    #
    # def __setitem__(self, key, value):
    #     raise AttributeError('Cannot set it directly!')


class TransformDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        else:
            return item


default_transform_dict = TransformDict()


class OptionDict(dict):
    def __init__(self, *args, **kwargs):
        super(OptionDict, self).__init__(*args, **kwargs)

    def get_option(self, key, default_value=None):
        if key in self:
            return self[key]
        elif default_value is not None:
            return default_value
        else:
            raise ValueError()

    def copy(self):
        return OptionDict(self)

    def merge(self, new_option_dict):
        for new_key, new_item in new_option_dict.items():
            if new_key in self:
                this_item = self[new_key]
                if this_item != new_item:
                    raise ValueError('Merge new different option!')
            else:
                self[new_key] = new_item


class DefaultDict(dict):
    def __init__(self, default_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_value = default_value

    def __getitem__(self, item):
        if not super().__contains__(item):
            super().__setitem__(item, copy.deepcopy(self.default_value))
        return super().__getitem__(item)


class MFAConfig(CoreConstants):
    def __init__(
            self, common_flux_range, specific_flux_range_dict, dynamic_constant_flux_list,
            preset_constant_flux_value_dict, common_mix_ratio_range, mix_ratio_multiplier,
            solver_type, solver_config_dict, combined_data=False, miscellaneous_config_dict=None):
        self.common_flux_range = common_flux_range
        self.specific_flux_range_dict = specific_flux_range_dict
        self.dynamic_constant_flux_list = dynamic_constant_flux_list
        self.preset_constant_flux_value_dict = preset_constant_flux_value_dict
        self.common_mix_ratio_range = common_mix_ratio_range
        self.mix_ratio_multiplier = mix_ratio_multiplier

        self.solver_type = solver_type
        self.solver_config_dict = solver_config_dict
        self.combined_data = combined_data
        if miscellaneous_config_dict is None:
            miscellaneous_config_dict = {}
        assert isinstance(miscellaneous_config_dict, dict)
        self.miscellaneous_config = miscellaneous_config_dict

    def copy(self):
        return copy.deepcopy(self)

    def update_miscellaneous_config(self, new_miscellaneous_config_dict):
        self.miscellaneous_config.update(new_miscellaneous_config_dict)
