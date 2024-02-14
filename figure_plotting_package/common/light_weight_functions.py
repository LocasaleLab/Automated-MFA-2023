from .built_in_packages import it
from .third_party_packages import np


def default_parameter_extract(
        option_dict: dict, key, default_value=None, force=False, pop=False, repeat_default_value=False):
    def single_extract(_option_dict, _key, _default_value):
        if force or _key in _option_dict:
            if pop:
                _value = _option_dict.pop(_key)
            else:
                _value = _option_dict[_key]
            return _value
        else:
            return _default_value

    if isinstance(key, str):
        return single_extract(option_dict, key, default_value)
    elif isinstance(key, (list, tuple)):
        result_list = []
        if isinstance(default_value, (list, tuple)):
            default_value_iter = default_value
        elif force or repeat_default_value:
            default_value_iter = it.repeat(default_value)
        else:
            raise ValueError()
        for each_key, each_default_value in zip(key, default_value_iter):
            result_list.append(single_extract(option_dict, each_key, each_default_value))
        return result_list
    else:
        raise ValueError()


def round_to_str_with_fixed_point(raw_num, decimal_num=0):
    sign = ''
    if decimal_num >= 0:
        if raw_num < 0:
            abs_raw_num = np.abs(raw_num)
            sign = '-'
        else:
            abs_raw_num = raw_num
        base_num = int(10 ** decimal_num)
        round_num = int(np.round(abs_raw_num * base_num, 0))
        integer_part = int(round_num / base_num)
        decimal_part = round_num % base_num
    else:
        integer_part = int(np.round(raw_num, decimal_num))
        decimal_part = 0
    if decimal_num <= 0:
        final_string = f'{sign}{integer_part}'
    else:
        decimal_part_str = f'{decimal_part}'
        decimal_part_rest_len = decimal_num - len(decimal_part_str)
        if decimal_part_rest_len > 0:
            decimal_part_str = f'{"0" * decimal_part_rest_len}{decimal_part_str}'
        final_string = f'{sign}{integer_part}.{decimal_part_str}'
    return final_string

