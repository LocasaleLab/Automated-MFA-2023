from common_and_plotting_functions.functions import check_and_mkdir_of_direct

from scripts.src.core.model.model_constructor import common_model_constructor
from scripts.src.core.solver.solver_construction_functions.solver_constructor import common_solver_constructor
from scripts.src.core.common.config import ParamName, CoreConstants
from scripts.src.core.common.functions import compartmental_mid_name_constructor
from scripts.src.core.data.data_class import MIDData

from scripts.model.model_loader import model_loader, ModelList
from scripts.data.common_functions import common_data_loader

from scripts.src.common.config import DataType
from scripts.src.common.third_party_packages import np, xlsxwriter
from ..common.result_output_functions import workbook_option_dict, \
    experimental_and_predicted_mid_materials_generator, experimental_and_predicted_mid_output_to_excel_sheet, \
    raw_flux_and_loss_output_to_excel_sheet

from .config import slsqp_mfa_config, Direct


class Keyword(object):
    metabolite_key_name = 'metabolite_key_name'
    raw_data_vector = 'raw_data_vector'
    raw_data_vector_str = 'raw_data_vector_str'
    standard_metabolite_name = 'standard_metabolite_name'
    combined_metabolite_list = 'combined_metabolite_list'
    combined_metabolite_list_str = 'combined_metabolite_list_str'
    mixed_compartment_list = 'mixed_compartment_list'
    mixed_compartment_list_str = 'mixed_compartment_list_str'

    normal_random = 'normal'
    uniform_random = 'uniform'


def output_file_name_constructor(output_py_direct, output_xlsx_direct, index: int = None, with_noise=False):
    base_name = 'simulated_flux_vector_and_mid_data'
    if index is not None:
        index_str = f'_{index}'
    else:
        index_str = ''
    if with_noise:
        noise_str = '_with_noise'
    else:
        noise_str = ''
    check_and_mkdir_of_direct(output_py_direct)
    check_and_mkdir_of_direct(output_xlsx_direct)
    output_py_file_path = f'{output_py_direct}/{base_name}{index_str}{noise_str}.py'
    output_xlsx_file_path = f'{output_xlsx_direct}/{base_name}{index_str}{noise_str}.xlsx'
    return output_py_file_path, output_xlsx_file_path


def add_noise_to_mid_data_obj(raw_mid_data_obj_dict, noise_sigma=0.1):
    new_mid_data_obj_dict = {}
    for data_name, mid_data_obj in raw_mid_data_obj_dict.items():
        new_mid_data_obj = mid_data_obj.copy()
        raw_data_vector = new_mid_data_obj.raw_data_vector
        ratio_vector = np.random.normal(scale=noise_sigma, size=len(raw_data_vector))
        modified_raw_data_vector = np.clip(raw_data_vector * (ratio_vector + 1), a_min=0, a_max=None)
        new_mid_data_obj.raw_data_vector = modified_raw_data_vector
        new_mid_data_obj.normalize()
        new_mid_data_obj_dict[data_name] = new_mid_data_obj
    return new_mid_data_obj_dict


def add_noise_to_mid_data_vector(raw_mid_data_vector_dict, noise_factor=0.1, random_func=Keyword.normal_random):
    new_mid_data_vector_dict = {}
    for data_name, mid_data_vector in raw_mid_data_vector_dict.items():
        data_size = len(mid_data_vector)
        if random_func == Keyword.normal_random:
            ratio_vector = np.random.normal(scale=noise_factor, size=data_size)
        elif random_func == Keyword.uniform_random:
            half_noise_factor = noise_factor / 2
            ratio_vector = (np.random.random(size=data_size) * half_noise_factor + half_noise_factor) * \
                np.sign(np.random.random(size=data_size) - 0.5)
        else:
            raise ValueError()
        modified_mid_data_vector = np.clip(
            mid_data_vector * (ratio_vector + 1), a_min=0, a_max=None) + CoreConstants.eps_for_mid
        normalized_modified_mid_data_vector = modified_mid_data_vector / np.sum(modified_mid_data_vector)
        new_mid_data_vector_dict[data_name] = normalized_modified_mid_data_vector
    return new_mid_data_vector_dict


def output_simulated_results_py_files(
        flux_name_index_dict, final_flux_vector, output_mid_data_dict, output_all_mid_data_dict,
        input_file_path, output_py_file_path):
    output_file_list = []
    output_mid_data_generator_string = (
        "    '{metabolite_key_name}': MIDData(\n"
        "        raw_data_vector=np.{raw_data_vector_str},\n"
        "        raw_name='{standard_metabolite_name}',\n"
        "        combined_raw_name_list={combined_metabolite_list_str},\n"
        "        compartment_list={mixed_compartment_list_str},\n"
        "        to_standard_name_dict=data_metabolite_to_standard_name_dict,\n"
        "        ),\n")
    with open(input_file_path) as f_in:
        state = None
        for line in f_in:
            if line.startswith('###FLUX_START'):
                output_file_list.append(line)
                state = 'flux'
                new_line = 'simulated_flux_vector = np.{}\n'.format(final_flux_vector.__repr__())
                output_file_list.append(new_line)
            elif line.startswith('###FLUX_END'):
                output_file_list.append(line)
                state = None
            elif line.startswith('###MIDDATA_START'):
                output_file_list.append(line)
                state = 'mid_data'
                for experimental_name, predicted_mid_dict in output_mid_data_dict.items():
                    new_line = output_mid_data_generator_string.format(**predicted_mid_dict)
                    output_file_list.append(new_line)
            elif line.startswith('###MIDDATA_END'):
                output_file_list.append(line)
                state = None
            elif line.startswith('###MIDALLDATA_START'):
                output_file_list.append(line)
                state = 'all_mid_data'
                for experimental_name, predicted_mid_dict in output_all_mid_data_dict.items():
                    new_line = output_mid_data_generator_string.format(**predicted_mid_dict)
                    output_file_list.append(new_line)
            elif line.startswith('###MIDALLDATA_END'):
                output_file_list.append(line)
                state = None
            elif line.startswith('###FLUX_NAME_INDEX_DICT_START'):
                state = 'flux_name_index_dict'
                output_file_list.append(line)
                for flux_name, flux_index in flux_name_index_dict.items():
                    output_file_list.append('    \'{}\': {},\n'.format(flux_name, flux_index))
            elif line.startswith('###FLUX_NAME_INDEX_DICT_END'):
                output_file_list.append(line)
                state = None
            else:
                if state is None:
                    output_file_list.append(line)

    with open(output_py_file_path, 'w', newline='\n') as f_out:
        f_out.write(''.join(output_file_list))


def output_simulated_results_xlsx_files(
        flux_name_index_dict, final_flux_vector, output_mid_data_dict, output_all_mid_data_dict,
        output_xlsx_file_path):
    def data_dict_for_df_generator(output_data_dict):
        data_dict_for_df = {
            'metabolite_name': [],
            'compartment_list': [],
            'mid_index': [],
            'mid_value': []
        }
        for experimental_name, predicted_mid_dict in output_data_dict.items():
            raw_data_vector = predicted_mid_dict[Keyword.raw_data_vector]
            for index, mid_value in enumerate(raw_data_vector):
                data_dict_for_df['metabolite_name'].append(predicted_mid_dict[Keyword.standard_metabolite_name])
                data_dict_for_df['compartment_list'].append(
                    ','.join(predicted_mid_dict[Keyword.mixed_compartment_list]))
                data_dict_for_df['mid_index'].append(index)
                data_dict_for_df['mid_value'].append(mid_value)
        return data_dict_for_df

    def mid_data_processor(raw_mid_data_dict):
        raw_mid_data_dict_for_df = {}
        for experimental_name, predicted_mid_dict in raw_mid_data_dict.items():
            current_standard_name = predicted_mid_dict[Keyword.standard_metabolite_name]
            current_compartment_list = predicted_mid_dict[Keyword.mixed_compartment_list]
            output_metabolite_name = compartmental_mid_name_constructor(
                current_standard_name, current_compartment_list)
            raw_data_vector = predicted_mid_dict[Keyword.raw_data_vector]
            raw_mid_data_dict_for_df[output_metabolite_name] = raw_data_vector
        mid_data_dict_for_df = {
            key: raw_mid_data_dict_for_df[key] for key in sorted(raw_mid_data_dict_for_df.keys())
        }
        return mid_data_dict_for_df

    flux_name_list = [0] * len(flux_name_index_dict)
    for flux_name, flux_index in flux_name_index_dict.items():
        flux_name_list[flux_index] = flux_name
    flux_name_value_dict = {
        flux_name: final_flux_vector[flux_index]
        for flux_index, flux_name in enumerate(flux_name_list)
    }

    mid_data_materials = experimental_and_predicted_mid_materials_generator(
        experimental_mid_data_dict=mid_data_processor(output_mid_data_dict),
        experimental_mid_column_name='mid_value')
    mid_all_data_materials = experimental_and_predicted_mid_materials_generator(
        experimental_mid_data_dict=mid_data_processor(output_all_mid_data_dict),
        experimental_mid_column_name='mid_value')
    with xlsxwriter.Workbook(output_xlsx_file_path, options=workbook_option_dict) as workbook:
        raw_flux_and_loss_output_to_excel_sheet(
            workbook, 'simulated_flux', flux_name_index_dict, final_flux_vector.reshape([1, -1]),
            index_list=['simulated_flux'])
        experimental_and_predicted_mid_output_to_excel_sheet(
            workbook, 'simulated_mid', *mid_data_materials)
        experimental_and_predicted_mid_output_to_excel_sheet(
            workbook, 'simulated_mid_all_data', *mid_all_data_materials)


def simulated_mid_data_generator(new_optimization_flux=False, index=None, with_noise=False):
    phgdh_data_class = 'phgdh_type'
    all_metabolite_data_class = 'all_metabolite'
    # data_class = phgdh_data_class
    # data_class = all_metabolite_data_class
    default_mixed_compartment_list = ('c', 'm')
    # with_noise = True
    # noise_factor = 0.3
    noise_factor = 0.2

    model_name = ModelList.base_model
    user_defined_model = model_loader(model_name)
    mfa_model = common_model_constructor(user_defined_model)
    data_wrap_obj, keyword = common_data_loader(DataType.hct116_cultured_cell_line, test_mode=True)
    mfa_data = data_wrap_obj.return_dataset()
    slsqp_solver_obj = common_solver_constructor(mfa_model, mfa_data, slsqp_mfa_config, verbose=True)

    if new_optimization_flux:
        final_flux_vector, final_obj, _ = slsqp_solver_obj.solve()
    else:
        from .simulated_flux_vector_and_mid_data import simulated_flux_vector
        final_flux_vector = simulated_flux_vector

    output_mid_data_dict = {}
    output_all_mid_data_dict = {}
    predicted_mid_data_dict = slsqp_solver_obj.predict(final_flux_vector)
    if with_noise:
        predicted_mid_data_dict = add_noise_to_mid_data_vector(predicted_mid_data_dict, noise_factor)
    # emu_name_experimental_name_dict = slsqp_solver_obj.emu_name_experimental_name_dict
    # predicted_experimental_name_mid_data_dict = {
    #     emu_name_experimental_name_dict[emu_name]: predicted_mid_array
    #     for emu_name, predicted_mid_array in predicted_mid_data_dict.items()
    # }
    for emu_name, predicted_mid_array in predicted_mid_data_dict.items():
        standard_name = slsqp_solver_obj.emu_name_experimental_name_dict[emu_name]
        combined_list = slsqp_solver_obj.experimental_mid_data_obj_dict[standard_name].combined_standard_name_list
        if combined_list is None:
            combined_list = ()
        output_mid_data_dict[standard_name] = {
            Keyword.raw_data_vector: predicted_mid_array,
            Keyword.raw_data_vector_str: predicted_mid_array.__repr__(),
            Keyword.metabolite_key_name: standard_name,
            Keyword.standard_metabolite_name: standard_name,
            Keyword.combined_metabolite_list: combined_list,
            Keyword.combined_metabolite_list_str: combined_list.__repr__(),
            Keyword.mixed_compartment_list: default_mixed_compartment_list,
            Keyword.mixed_compartment_list_str: default_mixed_compartment_list.__repr__(),
        }
    compartment_list = ['m', 'c', 'e']
    predicted_all_metabolite_mid_data_dict = slsqp_solver_obj.predict_all_target(final_flux_vector)
    if with_noise:
        predicted_all_metabolite_mid_data_dict = add_noise_to_mid_data_vector(
            predicted_all_metabolite_mid_data_dict, noise_factor)
    for predicted_metabolite_name, predicted_mid_value in predicted_all_metabolite_mid_data_dict.items():
        model_bare_name = mfa_model.metabolite_bare_metabolite_name_dict[predicted_metabolite_name]
        standard_name = mfa_model.model_metabolite_to_standard_name_dict[model_bare_name]
        metabolite_compartment = None
        for compartment in compartment_list:
            if predicted_metabolite_name.endswith('_{}'.format(compartment)):
                metabolite_compartment = compartment
                break
        compartmental_standard_name = compartmental_mid_name_constructor(standard_name, metabolite_compartment)
        output_all_mid_data_dict[compartmental_standard_name] = {
            Keyword.raw_data_vector: predicted_mid_value,
            Keyword.raw_data_vector_str: predicted_mid_value.__repr__(),
            Keyword.metabolite_key_name: compartmental_standard_name,
            Keyword.standard_metabolite_name: standard_name,
            Keyword.combined_metabolite_list: (),
            Keyword.combined_metabolite_list_str: '()',
            Keyword.mixed_compartment_list: metabolite_compartment,
            Keyword.mixed_compartment_list_str: "('{}',)".format(metabolite_compartment),
        }

    input_file_path = Direct.input_file_path
    output_py_file_path, output_xlsx_file_path = output_file_name_constructor(
        Direct.output_py_file_direct, Direct.output_xlsx_file_direct, index, with_noise)

    flux_name_index_dict = mfa_model.flux_name_index_dict

    output_simulated_results_xlsx_files(
        flux_name_index_dict, final_flux_vector, output_mid_data_dict, output_all_mid_data_dict,
        output_xlsx_file_path)
    exit()
    output_simulated_results_py_files(
        flux_name_index_dict, final_flux_vector, output_mid_data_dict, output_all_mid_data_dict,
        input_file_path, output_py_file_path)
    output_simulated_results_xlsx_files(
        flux_name_index_dict, final_flux_vector, output_mid_data_dict, output_all_mid_data_dict,
        output_xlsx_file_path)

