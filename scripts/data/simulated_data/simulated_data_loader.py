from common_and_plotting_functions.functions import pickle_load
from scripts.src.core.data.data_class import MIDData, MFAData
from scripts.src.common.functions import simulated_output_file_name_constructor, Keywords
from ..common_functions import glucose_6_input_metabolite_obj_generator


def mfa_data_obj_generation(experimental_mid_data_obj_dict):
    return MFAData(
        'simulated_data', experimental_mid_data_obj_dict, glucose_6_input_metabolite_obj_generator(),
    )


def simulated_data_loader(index=None, with_noise=False, batched_data=False, with_glns_m=False):
    simulated_py_file_path, _, simulated_pickle_file_path = simulated_output_file_name_constructor(
        index, with_noise, batched_data, with_glns_m)
    if not batched_data:
        import importlib
        simulated_py_module_path = simulated_py_file_path[:-len('.py')].replace('/', '.')
        simulated_obj = importlib.import_module(simulated_py_module_path)
        simulated_flux_value_dict = simulated_obj.simulated_flux_value_dict
        experimental_mid_data_obj_dict = simulated_obj.simulated_experimental_mid_data_obj_dict
        all_mid_data_obj_dict = simulated_obj.simulated_all_mid_data_obj_dict
    else:
        data_dict = pickle_load(simulated_pickle_file_path)
        flux_name_index_dict = data_dict[Keywords.simulated_flux_name_index_dict]
        final_flux_vector_list = data_dict[Keywords.simulated_final_flux_vector_list]
        experimental_mid_data_obj_dict = data_dict[Keywords.simulated_output_mid_data_dict_list]
        all_mid_data_obj_dict = data_dict[Keywords.simulated_output_all_mid_data_dict_list]
        simulated_flux_value_dict = [
            {flux_name: final_flux_vector[flux_index] for flux_name, flux_index in flux_name_index_dict.items()}
            for final_flux_vector in final_flux_vector_list
        ]
    return simulated_flux_value_dict, experimental_mid_data_obj_dict, all_mid_data_obj_dict
