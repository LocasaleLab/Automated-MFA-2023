from .packages import np, scipy_comb
from .config import CoreConstants


def remove_numerical_error(array, eps):
    array[np.abs(array) < eps] = 0


def natural_dist(carbon_num, c13_ratio=CoreConstants.natural_c13_ratio):
    c12_ratio = 1 - c13_ratio
    total_num = carbon_num + 1
    output = []
    for index in range(total_num):
        output.append(
            scipy_comb(carbon_num, index) * c13_ratio ** index * c12_ratio ** (carbon_num - index))
    return np.array(output)


def natural_dist_array(atom_num, isotope_abundance_vector):
    final_array = isotope_abundance_vector
    for _ in range(1, atom_num):
        final_array = np.convolve(final_array, isotope_abundance_vector, mode='full')
    return final_array


def np_list_conv(array_list):
    result_array = array_list[0]
    for input_array in array_list[1:]:
        result_array = np.convolve(result_array, input_array, mode='full')
    return result_array


def np_log_eps(experimental_vector, predicted_vector, eps):
    return -np.sum((experimental_vector + eps) * np.log(predicted_vector + eps))


def full_emu_name_constructor(metabolite_name, carbon_num=None):
    if carbon_num is None:
        return metabolite_name
    else:
        return '{}{}{}'.format(
            metabolite_name, CoreConstants.emu_carbon_list_str_sep, '1' * carbon_num)


def mix_flux_name_constructor(unique_id_name, index, case_name=None):
    if case_name is None:
        case_name = ''
    else:
        case_name = f'{case_name}_'
    return f'{CoreConstants.mix_ratio_prefix}{CoreConstants.mix_flux_sep}{case_name}{unique_id_name}_{index}'


def compartmental_mid_name_constructor(metabolite_name, compartment_name_list=None):
    if compartment_name_list is None:
        return metabolite_name
    if isinstance(compartment_name_list, str):
        compartment_name_str = compartment_name_list
    else:
        compartment_name_str = '_'.join(compartment_name_list)
    return '{}{}{}'.format(
        metabolite_name, CoreConstants.compartmental_mid_name_sep, compartment_name_str)


def tissue_specific_name_constructor(metabolite_or_reaction_name, tissue_name_list=None):
    if tissue_name_list is None:
        return metabolite_or_reaction_name
    if isinstance(tissue_name_list, str):
        tissue_name_str = tissue_name_list
    elif len(tissue_name_list) == 1 and tissue_name_list[0] is None:
        return metabolite_or_reaction_name
    else:
        tissue_name_str = '_'.join(tissue_name_list)
    return '{}{}{}'.format(
        tissue_name_str, CoreConstants.specific_tissue_sep, metabolite_or_reaction_name)


def group_emu_name_constructor(metabolite_name, case_name=None):
    if case_name is None:
        return metabolite_name
    else:
        return f'{case_name}_{metabolite_name}'


def isdigit(number):
    return isinstance(number, int) or isinstance(number, float)


def default_parameter_extract(option_dict, key, default_value):
    if key in option_dict:
        return option_dict[key]
    else:
        return default_value


def reverse_reaction_name(raw_reaction_id):
    return raw_reaction_id + CoreConstants.reverse_reaction_name_suffix


def search_sorted(item, seq, start, end):
    seq_len = end - start
    if seq_len <= 3:
        for index in range(start, end):
            if item == seq[index]:
                return index
        return -1
    else:
        mid_index = int((start + end) / 2)
        if item == seq[mid_index]:
            while mid_index != 0 and item == seq[mid_index - 1]:
                mid_index -= 1
            return mid_index
        else:
            index = search_sorted(item, seq, start, mid_index)
            if index != -1:
                return index
            index = search_sorted(item, seq, mid_index + 1, end)
            if index != -1:
                return index
            return -1


def check_if_subsequence(subseq, whole_seq, reverse=False):
    """
    Both subseq and whole_seq should be sorted in ascending order
    """
    subsequence = True
    if len(subseq) > len(whole_seq):
        return check_if_subsequence(whole_seq, subseq, True)
    elif len(subseq) == len(whole_seq):
        for subseq_item, whole_seq_item in zip(subseq, whole_seq):
            if subseq_item != whole_seq_item:
                subsequence = False
                break
    else:
        start_index = 0
        end_index = len(whole_seq)
        for element in subseq:
            current_index = search_sorted(element, whole_seq, start_index, end_index)
            if current_index == -1:
                subsequence = False
                break
            start_index = current_index + 1
    return subsequence, reverse


def check_if_mix_flux(flux_name: str):
    if flux_name.startswith(f'{CoreConstants.mix_ratio_prefix}{CoreConstants.mix_flux_sep}'):
        return True
    else:
        return False


def check_if_biomass_flux(flux_name: str):
    return flux_name == CoreConstants.biomass_flux_id
