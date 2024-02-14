from .built_in_packages import gzip, pickle, pathlib


def pickle_save(obj, file_path):
    with gzip.open(file_path, 'wb') as f_out:
        pickle.dump(obj, f_out)


class RenameUnpickler(pickle.Unpickler):
    # This guarantee the movement of class
    def find_class(self, module, name):
        renamed_module = module
        if module == 'common_and_plotting_functions.figure_data_format':
            renamed_module = 'figure_plotting_package.common.figure_data_format'

        return super(RenameUnpickler, self).find_class(renamed_module, name)


def pickle_load(file_path):
    with gzip.open(file_path, 'rb') as f_in:
        obj = RenameUnpickler(f_in).load()
        # obj = pickle.load(f_in)
    return obj


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


class FigureData(object):
    def __init__(self, data_direct, data_prefix, data_name):
        if data_prefix is None:
            complete_data_name = data_name
        else:
            complete_data_name = f'{data_prefix}__{data_name}'
        self.save_path = f'{data_direct}/{complete_data_name}'
        self.data_dict = None

    def save_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data_dict = kwargs
        check_and_mkdir_of_direct(self.save_path, file_path=True)
        pickle_save(self, self.save_path)

    def load_data(self):
        target_obj = pickle_load(self.save_path)
        return target_obj


class BasicFigureData(object):
    data_direct = None
    data_prefix = None

    def __init__(self):
        self.figure_raw_data_dict = {}

    def _return_figure_data(self, data_name):
        if data_name in self.figure_raw_data_dict:
            return self.figure_raw_data_dict[data_name]
        else:
            current_figure_data = FigureData(self.data_direct, self.data_prefix, data_name).load_data()
            self.figure_raw_data_dict[data_name] = current_figure_data
            return current_figure_data
