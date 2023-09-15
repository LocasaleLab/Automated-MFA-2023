from .data_metabolite_to_standard_name_dict import data_metabolite_to_standard_name_dict
from scripts.src.common.config import Direct, DataType, Keywords as CommonKeywords
from scripts.src.common.functions import excel_column_letter_to_0_index
from ..complete_dataset_class import CompleteDataset
from ..common_functions import average_mid_data_dict


class Keyword(object):
    cell_line = 'cell_line'
    glucose_level = 'glucose_level'
    index = 'index'

    high_glucose_level = 'H'
    low_glucose_level = 'L'

    high_low_glucose = 'high_low_glucose'
    index_average_list = [1, 2, 3]


class SpecificParameters(CompleteDataset):
    def __init__(self):
        super(SpecificParameters, self).__init__()
        self.mixed_compartment_list = ('c', 'm')
        self.current_direct = "{}/colon_cancer_cell_line".format(Direct.data_direct)
        self.file_path = "{}/data.xlsx".format(self.current_direct)
        self.experiment_name_prefix_list = ["colon_cancer"]
        self.test_experiment_name_prefix = "colon_cancer"
        self.test_cell_line_name = 'SW620-P3'
        self.test_glucose_level = Keyword.high_glucose_level
        self.test_repeat_index = 1

        col_range = (excel_column_letter_to_0_index('A'), excel_column_letter_to_0_index('AX'))

        self._complete_data_parameter_dict_dict = {
            current_sheet_name: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': current_sheet_name,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'mixed_compartment_list': self.mixed_compartment_list,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict,
                'col_range': col_range,
                'excluded_metabolite_name_set': {'pyrophosphate'}
            }
            for current_sheet_name in self.experiment_name_prefix_list}
        self._test_data_parameter_dict_dict = {
            DataType.test: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': self.test_experiment_name_prefix,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'mixed_compartment_list': self.mixed_compartment_list,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict,
                'col_range': col_range,
                'excluded_metabolite_name_set': {'pyrophosphate'}
            }
        }

        self.cell_line_id_name_dict = {
            '1': 'NCI.H716',
            '2': 'Colo.320',
            '3': 'SW1116',
            '4': 'SW620-P3',
            '5': 'SW480',
            '6': 'HCT8-P5',
            '7': 'HT29',
            '8': 'SW147',
            '9': 'HCT116-P3',
            '10': 'NCI-H5087',
            '11': 'SW48-P2',
            '12': 'SW948-P3',
            '13': 'LSI74T',
            '14': 'Caco2-P2',
        }

        glucose_fbp_set = {'glucose', 'fructose 1,6-bisphosphate'}
        gap = 'glyceraldehyde 3-phosphate'
        dhap = 'dihydroxyacetone phosphate'

        self.exclude_metabolites_dict = {
            'HCT8-P5': {
                Keyword.low_glucose_level: {
                    1: glucose_fbp_set,
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'HCT116-P3': {
                Keyword.low_glucose_level: {
                    1: glucose_fbp_set,
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'HT29': {
                Keyword.low_glucose_level: {
                    1: {*glucose_fbp_set, gap, dhap},
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'NCI-H5087': {
                Keyword.low_glucose_level: {
                    1: glucose_fbp_set,
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'SW48-P2': {
                Keyword.low_glucose_level: {
                    1: {*glucose_fbp_set, gap, dhap},
                    2: {*glucose_fbp_set, gap, dhap},
                    3: glucose_fbp_set,
                },
            },
            'SW480': {
                Keyword.low_glucose_level: {
                    1: glucose_fbp_set,
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'SW620-P3': {
                Keyword.low_glucose_level: {
                    1: {*glucose_fbp_set, gap, dhap},
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
            'SW948-P3': {
                Keyword.low_glucose_level: {
                    1: glucose_fbp_set,
                    2: glucose_fbp_set,
                    3: glucose_fbp_set,
                },
            },
        }

    @staticmethod
    def project_name_generator(cell_line, glucose_level, repeat_index):
        return '{}__{}_{}'.format(cell_line, glucose_level, repeat_index)

    def add_data_sheet(self, sheet_name, current_data_dict):
        final_result_dict = self.complete_dataset
        for data_label, specific_data_dict in current_data_dict.items():
            _, cell_line_id_str, repeat_index_str = data_label.split('_')
            repeat_index = int(repeat_index_str)
            cell_line_name = self.cell_line_id_name_dict[cell_line_id_str[:-1]]
            glucose_suffix = cell_line_id_str[-1]
            if cell_line_name not in final_result_dict:
                final_result_dict[cell_line_name] = {}
            if glucose_suffix not in final_result_dict[cell_line_name]:
                final_result_dict[cell_line_name][glucose_suffix] = {}
            try:
                current_excluded_metabolites_set = self.exclude_metabolites_dict[
                    cell_line_name][glucose_suffix][repeat_index]
            except KeyError:
                current_excluded_metabolites_set = {}
            for excluded_metabolite_name in current_excluded_metabolites_set:
                pop_item = specific_data_dict.pop(excluded_metabolite_name, None)
            final_result_dict[cell_line_name][glucose_suffix][repeat_index] = specific_data_dict

    def _complete_return_dataset(self, param_dict):
        cell_line = param_dict[Keyword.cell_line]
        glucose_level = param_dict[Keyword.glucose_level]
        repeat_index = param_dict[Keyword.index]
        if repeat_index == CommonKeywords.average:
            final_target_metabolite_data_dict = average_mid_data_dict(
                self.complete_dataset[cell_line][glucose_level], Keyword.index_average_list)
        else:
            final_target_metabolite_data_dict = self.complete_dataset[
                cell_line][glucose_level][repeat_index]
        final_input_metabolite_data_dict = None
        project_name = self.project_name_generator(cell_line, glucose_level, repeat_index)
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_dict

    def _test_return_dataset(self, param_dict=None):
        final_target_metabolite_data_dict = self.complete_dataset[
            self.test_cell_line_name][self.test_glucose_level][self.test_repeat_index]
        final_input_metabolite_data_dict = None
        project_name = DataType.test
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_dict
