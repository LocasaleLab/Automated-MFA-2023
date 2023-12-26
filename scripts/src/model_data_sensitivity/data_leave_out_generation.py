from .sensitivity_config import data_keep_dict, Keywords, DataSetting
from .config import normal_simulated_experimental_mid_data_obj_dict, \
    all_metabolite_simulated_experimental_mid_data_obj_dict, \
    normal_simulated_experimental_mid_data_obj_dict_with_noise, \
    all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise
from scripts.data.simulated_data.simulated_data_loader import simulated_data_loader


def data_obj_generator(simulated_data_obj, specific_data_keep_list):
    new_simulated_experimental_mid_data_obj_dict = {
        metabolite_name: simulated_data_obj[metabolite_name]
        for metabolite_name in specific_data_keep_list}
    return new_simulated_experimental_mid_data_obj_dict


def information_dict_generator(process_type_label, simulated_flux_value_dict):
    return {
        Keywords.label: process_type_label,
        Keywords.simulated_flux_value_dict: simulated_flux_value_dict}


def simulated_list_data_and_information_dict_generator(
        process_type_label, simulated_flux_value_dict_list, simulated_experimental_mid_data_obj_dict_list,
        modified_data_dict, information_dict):
    assert len(simulated_flux_value_dict_list) == len(simulated_experimental_mid_data_obj_dict_list)
    common_or_dict_simulated_flux_value_dict = {}
    for simulated_index, (flux_value_dict, experimental_mid_data_obj_dict) in enumerate(zip(
            simulated_flux_value_dict_list, simulated_experimental_mid_data_obj_dict_list)):
        current_new_process_type_label = f'{process_type_label}_{simulated_index}'
        modified_data_dict[current_new_process_type_label] = experimental_mid_data_obj_dict
        information_dict[current_new_process_type_label] = information_dict_generator(
            process_type_label, flux_value_dict)
        common_or_dict_simulated_flux_value_dict[current_new_process_type_label] = flux_value_dict
    return common_or_dict_simulated_flux_value_dict


def data_loader(process_type_list):
    modified_data_dict = {}
    information_dict = {}
    if not isinstance(process_type_list, list):
        process_type_list = [process_type_list]
    common_or_dict_simulated_flux_value_dict = None
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
        if process_type in {DataSetting.raw_data_batch, DataSetting.all_data_batch}:
            batched_simulated_data = True
        else:
            batched_simulated_data = False
        if process_type in {
                DataSetting.raw_data, DataSetting.medium_data, DataSetting.medium_data_plus, DataSetting.few_data,
                DataSetting.data_without_ppp, DataSetting.data_without_aa, DataSetting.data_without_tca,
                DataSetting.raw_data_batch}:
            # if with_noise:
            #     simulated_experimental_mid_data_obj_dict = normal_simulated_experimental_mid_data_obj_dict_with_noise
            # else:
            #     simulated_experimental_mid_data_obj_dict = normal_simulated_experimental_mid_data_obj_dict
            simulated_flux_value_dict, simulated_experimental_mid_data_obj_dict, _ = simulated_data_loader(
                with_noise=with_noise, batched_data=batched_simulated_data)
            if batched_simulated_data:
                common_or_dict_simulated_flux_value_dict = simulated_list_data_and_information_dict_generator(
                    process_type_label, simulated_flux_value_dict, simulated_experimental_mid_data_obj_dict,
                    modified_data_dict, information_dict)
            else:
                if process_type == DataSetting.raw_data:
                    modified_data_dict[process_type_label] = simulated_experimental_mid_data_obj_dict
                else:
                    specific_data_keep_list = data_keep_dict[process_type]
                    modified_data_dict[process_type_label] = data_obj_generator(
                        simulated_experimental_mid_data_obj_dict, specific_data_keep_list)
                information_dict[process_type_label] = information_dict_generator(
                    process_type_label, simulated_flux_value_dict)
                if common_or_dict_simulated_flux_value_dict is None:
                    common_or_dict_simulated_flux_value_dict = simulated_flux_value_dict
        elif process_type in {
                DataSetting.medium_data_without_combination, DataSetting.all_data, DataSetting.all_data_batch}:
            # if with_noise:
            #     simulated_all_mid_data_obj_dict = \
            #         all_metabolite_simulated_experimental_mid_data_obj_dict_with_noise
            # else:
            #     simulated_all_mid_data_obj_dict = all_metabolite_simulated_experimental_mid_data_obj_dict
            simulated_flux_value_dict, _, simulated_all_mid_data_obj_dict = simulated_data_loader(
                with_noise=with_noise, batched_data=batched_simulated_data)
            if batched_simulated_data:
                common_or_dict_simulated_flux_value_dict = simulated_list_data_and_information_dict_generator(
                    process_type_label, simulated_flux_value_dict, simulated_all_mid_data_obj_dict,
                    modified_data_dict, information_dict)
            else:
                if process_type == DataSetting.all_data:
                    modified_data_dict[process_type_label] = simulated_all_mid_data_obj_dict
                else:
                    specific_data_keep_list = data_keep_dict[process_type]
                    modified_data_dict[process_type_label] = data_obj_generator(
                        simulated_all_mid_data_obj_dict, specific_data_keep_list)
                information_dict[process_type_label] = information_dict_generator(
                    process_type_label, simulated_flux_value_dict)
                if common_or_dict_simulated_flux_value_dict is None:
                    common_or_dict_simulated_flux_value_dict = simulated_flux_value_dict
        else:
            raise ValueError()
    return modified_data_dict, information_dict, common_or_dict_simulated_flux_value_dict
