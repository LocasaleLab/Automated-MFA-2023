from scripts.src.core.common.config import CoreConstants
from scripts.src.core.data.data_class import InputMetaboliteData


glucose_labeled_ratio_list = [1] * 6
glucose_unlabeled_ratio_list = [CoreConstants.natural_c13_ratio] * 6
default_glucose_infusion_labeled_ratio = 0.4

glucose_6_labeled_input_metabolite_dict = {
    "GLC_e": [
        {
            "ratio_list": glucose_labeled_ratio_list,
            "abundance": 1,
        },
    ],
}


def input_mid_data_processor(input_raw_metabolite_dict):
    return {
        input_metabolite_name: InputMetaboliteData(input_metabolite_name, abundance_data_list)
        for input_metabolite_name, abundance_data_list in input_raw_metabolite_dict.items()}

