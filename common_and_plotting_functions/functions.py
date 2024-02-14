from .built_in_packages import gzip, pickle, pathlib, it
from .third_party_packages import np


def isdigit(number):
    return isinstance(number, (float, int))


def pickle_save(obj, file_path):
    with gzip.open(file_path, 'wb') as f_out:
        pickle.dump(obj, f_out)


def pickle_load(file_path):
    with gzip.open(file_path, 'rb') as f_in:
        obj = pickle.load(f_in)
    return obj


def check_file_existence(file_path):
    file_path_obj = pathlib.Path(file_path)
    return file_path_obj.exists()


def check_and_mkdir_of_direct(direct_str, file_path=False):
    direct_obj = pathlib.Path(direct_str)
    if file_path:
        direct_obj = direct_obj.parent
    dir_stack = []
    while not direct_obj.exists():
        dir_stack.append(direct_obj)
        direct_obj = direct_obj.parent
    while len(dir_stack) != 0:
        missed_direct = dir_stack.pop()
        missed_direct.mkdir()


def npz_load(raw_path, *args, allow_pickle=False):
    result_list = []
    suffix_path = '{}.npz'.format(raw_path)
    with np.load(suffix_path, allow_pickle=allow_pickle) as data:
        for label in args:
            result_list.append(data[label])
    if len(result_list) == 1:
        return result_list[0]
    else:
        return result_list


def npz_save(path, **kwargs):
    np.savez_compressed(path, **kwargs)


def replace_invalid_file_name(file_name):
    file_name = file_name.replace(':', '__')
    file_name = file_name.replace('/', '_')
    return file_name


def replace_result_label_to_sheet_name(result_label):
    maximal_sheet_name_len = 28             # Maximal length of sheet name
    result_label = replace_invalid_file_name(result_label).replace('__', '_')
    return result_label[:maximal_sheet_name_len]


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

