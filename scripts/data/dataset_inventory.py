from scripts.src.common.config import DataType


def return_dataset_and_keyword(dataset_name):
    if dataset_name == DataType.hct116_cultured_cell_line:
        from .hct116_cultured_cell_line.specific_data_parameters import SpecificParameters, Keyword
    elif dataset_name == DataType.renal_carcinoma:
        from .renal_carcinoma.specific_data_parameters import SpecificParameters, Keyword
    elif dataset_name == DataType.lung_tumor:
        from .lung_tumor.specific_data_parameters import SpecificParameters, Keyword
    elif dataset_name == DataType.colon_cancer:
        from .colon_cancer_cell_line.specific_data_parameters import SpecificParameters, Keyword
    else:
        raise ValueError()
    dataset_obj = SpecificParameters()
    return dataset_obj, Keyword
