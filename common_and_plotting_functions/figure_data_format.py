from .functions import pickle_save, pickle_load, check_and_mkdir_of_direct
from .config import Direct


class FigureData(object):
    def __init__(self, data_prefix, data_name):
        if data_prefix is None:
            complete_data_name = data_name
        else:
            complete_data_name = f'{data_prefix}__{data_name}'
        self.save_path = f'{Direct.figure_raw_data_direct}/{complete_data_name}'
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