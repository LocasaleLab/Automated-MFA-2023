from .data_metabolite_to_standard_name_dict import data_metabolite_to_standard_name_dict
from ..complete_dataset_class import CompleteDataset, natural_distribution_anti_correction, check_negative_data_array
from scripts.src.common.config import DataType, Direct, Keywords as CommonKeywords
from ..common_functions import average_mid_data_dict, glucose_infusion_input_metabolite_obj_dict_generator
from ..config import default_glucose_infusion_labeled_ratio
from .c13_glucose_enrichment_plasma import glucose_enrichment_plasma_dict


class Keyword(object):
    tissue = 'tissue'
    patient = 'patient'
    index = 'index'

    kidney = 'kidney'
    carcinoma = 'carcinoma'
    brain = 'brain'

    index_average_list = [1, 2, 3]


def input_metabolite_data_obj_dict_generator(tissue_name, tissue_index):
    if tissue_name == Keyword.kidney or tissue_name == Keyword.carcinoma:
        current_label_ratio = glucose_enrichment_plasma_dict[tissue_index]
    else:
        current_label_ratio = default_glucose_infusion_labeled_ratio
    current_input_metabolite_obj_dict = glucose_infusion_input_metabolite_obj_dict_generator(
        current_label_ratio)
    return current_input_metabolite_obj_dict


class SpecificParameters(CompleteDataset):
    def __init__(self):
        super().__init__()
        self.mixed_compartment_list = ('c', 'm')
        self.current_direct = '{}/renal_carcinoma'.format(Direct.data_direct)
        self.file_path = '{}/data.xlsx'.format(self.current_direct)
        self.experiment_name_prefix_list = ['kidney', 'carcinoma', 'brain']
        self.test_experiment_name_prefix = 'brain'
        self.test_tissue_index = 1
        self.test_repeat_index = 1

        self.exclude_metabolites_dict = {
            'brain': {'3-phosphoglycerate'}
        }

        self._complete_data_parameter_dict_dict = {
            current_sheet_name: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': current_sheet_name,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'mixed_compartment_list': self.mixed_compartment_list,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict}
            for current_sheet_name in self.experiment_name_prefix_list}
        self._test_data_parameter_dict_dict = {
            DataType.test: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': self.test_experiment_name_prefix,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'mixed_compartment_list': self.mixed_compartment_list,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict}}
        self.complete_input_metabolite_data_dict = {}

    @staticmethod
    def project_name_generator(tissue_name, tissue_index, repeat_index):
        return '{}__{}_{}'.format(tissue_name, tissue_index, repeat_index)

    def add_data_sheet(self, sheet_name, current_data_dict):
        if self.anti_correction:
            for column_name, each_column_data_dict in current_data_dict.items():
                natural_distribution_anti_correction(each_column_data_dict)
        check_negative_data_array(current_data_dict, [])
        final_result_dict = self.complete_dataset
        if sheet_name not in final_result_dict:
            final_result_dict[sheet_name] = {}
        for data_label, specific_data_dict in current_data_dict.items():
            _, tissue_index_str, repeat_index_str = data_label.split('_')
            tissue_index = int(tissue_index_str)
            repeat_index = int(repeat_index_str)
            try:
                current_excluded_metabolites_set = self.exclude_metabolites_dict[sheet_name]
            except KeyError:
                current_excluded_metabolites_set = {}
            for excluded_metabolite_name in current_excluded_metabolites_set:
                pop_item = specific_data_dict.pop(excluded_metabolite_name, None)
            if tissue_index not in final_result_dict[sheet_name]:
                final_result_dict[sheet_name][tissue_index] = {}
            final_result_dict[sheet_name][tissue_index][repeat_index] = specific_data_dict

    def _complete_return_dataset(self, param_dict):
        tissue_name = param_dict[Keyword.tissue]
        tissue_index = param_dict[Keyword.patient]
        repeat_index = param_dict[Keyword.index]
        if repeat_index == CommonKeywords.average:
            final_target_metabolite_data_dict = average_mid_data_dict(
                self.complete_dataset[tissue_name][tissue_index], Keyword.index_average_list)
        else:
            final_target_metabolite_data_dict = self.complete_dataset[
                tissue_name][tissue_index][repeat_index]
        project_name = self.project_name_generator(tissue_name, tissue_index, repeat_index)
        final_input_metabolite_data_obj_dict = input_metabolite_data_obj_dict_generator(tissue_name, tissue_index)
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_obj_dict

    def _test_return_dataset(self):
        final_target_metabolite_data_dict = self.complete_dataset[
            DataType.test][self.test_tissue_index][self.test_repeat_index]
        project_name = DataType.test
        final_input_metabolite_data_dict = None
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_dict
