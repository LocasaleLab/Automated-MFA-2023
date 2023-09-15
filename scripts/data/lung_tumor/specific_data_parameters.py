from .data_metabolite_to_standard_name_dict import data_metabolite_to_standard_name_dict
from ..complete_dataset_class import CompleteDataset, natural_distribution_anti_correction, check_negative_data_array
from scripts.src.common.config import Direct, Keywords as CommonKeywords, DataType
from ..common_functions import average_mid_data_dict, glucose_infusion_input_metabolite_obj_dict_generator
from ..config import default_glucose_infusion_labeled_ratio


class Keyword(object):
    experiments = 'experiments'
    patient = 'patient'
    tissue = 'tissue'
    index = 'index'

    labeling = 'labeling'
    glucose = 'glucose'
    lactate = 'lactate'

    mouse_lung_vs_tumor = 'mouse_lung_vs_tumor'
    mouse_tumor_ko = 'mouse_tumor_ko'

    mouse = 'mouse'
    human = 'human'
    lung = 'lung'
    flank = 'flank'
    tumor = 'tumor'

    hcc15 = 'HCC15'
    mct1ko = 'MCT1KO'
    mct4ko = 'MCT4KO'

    plasma = 'plasma'

    empty_patient_key = ''
    index_average_list = [1, 2, 3, 4, 5, 6]


class SpecificParameters(CompleteDataset):
    def __init__(self):
        super().__init__()
        self.mixed_compartment_list = ('c', 'm')
        self.current_direct = '{}/lung_tumor'.format(Direct.data_direct)
        self.file_path = '{}/data.xlsx'.format(self.current_direct)
        self.sheet_name_experiment_name_dict = {
            'Human': Keyword.human,
            'Mouse_H460_U13Glc': Keyword.mouse_lung_vs_tumor,
            'Mouse_HCC15_KO': Keyword.mouse_tumor_ko}
        self.sheet_name_information_dict = {
            'Human_glucose': {
                Keyword.experiments: Keyword.human,
                Keyword.labeling: Keyword.glucose,
                Keyword.plasma: False
            },
            'Human_glucose_plasma': {
                Keyword.experiments: Keyword.human,
                Keyword.labeling: Keyword.glucose,
                Keyword.plasma: True
            },
            'Mouse_H460_U13Glc': {
                Keyword.experiments: Keyword.mouse_lung_vs_tumor
            },
            'Mouse_HCC15_KO': {
                Keyword.experiments: Keyword.mouse_tumor_ko
            }
        }
        self.test_sheet_name = 'Mouse_HCC15_KO'
        self.test_tissue_name = 'HCC15'
        self.test_repeat_index = 1
        self.human_plasma_data_dict = {}
        self.patient_id_labeling_dict = {}

        self._complete_data_parameter_dict_dict = {
            current_sheet_name: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': current_sheet_name,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict}
            for current_sheet_name in self.sheet_name_information_dict.keys()}
        self._test_data_parameter_dict_dict = {
            DataType.test: {
                'xlsx_file_path': self.file_path,
                'xlsx_sheet_name': self.test_sheet_name,
                'index_col_name': CommonKeywords.metabolite_name_col,
                'to_standard_name_dict': data_metabolite_to_standard_name_dict}}
        self.complete_input_metabolite_data_dict = {}

    @staticmethod
    def project_name_generator(experiment_name, tissue_name, repeat_index, patient_id=''):
        return '{}__{}_{}_{}'.format(experiment_name, patient_id, tissue_name, repeat_index)

    def add_data_sheet(self, sheet_name, current_data_dict):
        if self.anti_correction:
            for column_name, each_column_data_dict in current_data_dict.items():
                natural_distribution_anti_correction(each_column_data_dict)
        check_negative_data_array(current_data_dict, [])
        final_result_dict = self.complete_dataset
        sheet_information_dict = self.sheet_name_information_dict[sheet_name]
        experiment_name = sheet_information_dict[Keyword.experiments]
        if experiment_name not in final_result_dict:
            final_result_dict[experiment_name] = {}
        for data_label, specific_data_dict in current_data_dict.items():
            if experiment_name == Keyword.human:
                labeling = sheet_information_dict[Keyword.labeling]
                patient_id, tissue_name, repeat_index_str = data_label.split('_')
                self.patient_id_labeling_dict[patient_id] = labeling
                plasma = sheet_information_dict[Keyword.plasma]
                if plasma:
                    if patient_id not in self.human_plasma_data_dict:
                        self.human_plasma_data_dict[patient_id] = specific_data_dict
                    continue
                else:
                    if patient_id not in final_result_dict[experiment_name]:
                        final_result_dict[experiment_name][patient_id] = {}
                    current_result_dict = final_result_dict[experiment_name][patient_id]
            else:
                tissue_name, repeat_index_str = data_label.split('_')
                current_result_dict = final_result_dict[experiment_name]
            repeat_index = int(repeat_index_str)
            if tissue_name not in current_result_dict:
                current_result_dict[tissue_name] = {}
            current_result_dict[tissue_name][repeat_index] = specific_data_dict

    def _complete_return_dataset(self, param_dict):
        experiment_name = param_dict[Keyword.experiments]
        if experiment_name == Keyword.human:
            patient_id = param_dict[Keyword.patient]
            current_result_dict = self.complete_dataset[experiment_name][patient_id]
            input_metabolite_data_dict = self.human_plasma_data_dict[patient_id]
            labeling_metabolite = self.patient_id_labeling_dict[patient_id]
            current_label_ratio = input_metabolite_data_dict[labeling_metabolite].data_vector[-1]
            if labeling_metabolite == Keyword.glucose:
                final_input_metabolite_data_obj_dict = glucose_infusion_input_metabolite_obj_dict_generator(
                    current_label_ratio)
            else:
                raise ValueError()
        else:
            patient_id = ''
            if experiment_name == Keyword.mouse_tumor_ko:
                glucose_infusion_ratio = 0.6
            else:
                glucose_infusion_ratio = default_glucose_infusion_labeled_ratio
            current_result_dict = self.complete_dataset[experiment_name]
            final_input_metabolite_data_obj_dict = glucose_infusion_input_metabolite_obj_dict_generator(
                    glucose_infusion_ratio)
        tissue_name = param_dict[Keyword.tissue]
        repeat_index = param_dict[Keyword.index]
        if repeat_index == CommonKeywords.average:
            final_target_metabolite_data_dict = average_mid_data_dict(
                current_result_dict[tissue_name], Keyword.index_average_list)
        else:
            final_target_metabolite_data_dict = current_result_dict[tissue_name][repeat_index]
        project_name = self.project_name_generator(
            experiment_name, tissue_name, repeat_index, patient_id)
        # final_input_metabolite_data_obj_dict = None
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_obj_dict

    def _test_return_dataset(self):
        final_target_metabolite_data_dict = self.complete_dataset[
            Keyword.mouse_tumor_ko][self.test_tissue_name][self.test_repeat_index]
        project_name = DataType.test
        final_input_metabolite_data_dict = None
        return project_name, final_target_metabolite_data_dict, final_input_metabolite_data_dict

