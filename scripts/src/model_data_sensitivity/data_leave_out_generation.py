from .sensitivity_config import data_keep_dict, Keywords, DataSetting
from .config import normal_simulated_experimental_mid_data_obj_dict, \
    all_metabolite_simulated_experimental_mid_data_obj_dict, \
    normal_simulated_experimental_mid_data_obj_dict_with_noise, \
    all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise


def data_obj_generator(simulated_data_obj, specific_data_keep_list):
    new_simulated_experimental_mid_data_obj_dict = {
        metabolite_name: simulated_data_obj[metabolite_name]
        for metabolite_name in specific_data_keep_list}
    return new_simulated_experimental_mid_data_obj_dict


def data_loader(process_type_list):
    modified_data_dict = {}
    information_dict = {}
    if not isinstance(process_type_list, list):
        process_type_list = [process_type_list]
    for process_type_element in process_type_list:
        with_noise = False
        if not isinstance(process_type_element, (list, tuple)):
            process_type = process_type_element
        else:
            process_type, *with_noise_list = process_type_element
            if len(with_noise_list) != 0:
                with_noise = with_noise_list[0]
        if with_noise:
            process_type_label = '{}_noise'.format(process_type)
        else:
            process_type_label = process_type
        if process_type in (
                DataSetting.raw_data, DataSetting.medium_data, DataSetting.medium_data_plus, DataSetting.few_data,
                DataSetting.data_without_ppp, DataSetting.data_without_aa, DataSetting.data_without_tca):
            if with_noise:
                simulated_experimental_mid_data_obj_dict = normal_simulated_experimental_mid_data_obj_dict_with_noise
            else:
                simulated_experimental_mid_data_obj_dict = normal_simulated_experimental_mid_data_obj_dict
            if process_type == DataSetting.raw_data:
                modified_data_dict[process_type_label] = simulated_experimental_mid_data_obj_dict
                information_dict[process_type_label] = process_type_label
            else:
                specific_data_keep_list = data_keep_dict[process_type]
                modified_data_dict[process_type_label] = data_obj_generator(
                    simulated_experimental_mid_data_obj_dict, specific_data_keep_list)
                information_dict[process_type_label] = process_type_label
        elif process_type in (DataSetting.medium_data_without_combination, DataSetting.all_data):
            if with_noise:
                simulated_experimental_mid_data_obj_dict = \
                    all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise
            else:
                simulated_experimental_mid_data_obj_dict = all_metabolite_simulated_experimental_mid_data_obj_dict
            if process_type == DataSetting.all_data:
                modified_data_dict[process_type_label] = simulated_experimental_mid_data_obj_dict
            else:
                specific_data_keep_list = data_keep_dict[process_type]
                modified_data_dict[process_type_label] = data_obj_generator(
                    simulated_experimental_mid_data_obj_dict, specific_data_keep_list)
            information_dict[process_type_label] = process_type_label
        else:
            raise ValueError()
    return modified_data_dict, information_dict
