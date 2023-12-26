from ..inventory import DataModelType


def common_data_model_function_loader(model_name):
    if model_name == DataModelType.renal_carcinoma_invivo_infusion:
        from . import renal_carcinoma_invivo_infusion as data_model_object
    elif model_name == DataModelType.renal_carcinoma_invivo_infusion_squared_loss:
        from . import renal_carcinoma_invivo_infusion_squared_loss as data_model_object
    elif model_name == DataModelType.renal_carcinoma_invivo_infusion_traditional_method:
        from . import renal_carcinoma_invivo_infusion_traditional_method as data_model_object
    elif model_name == DataModelType.lung_tumor_invivo_infusion:
        from . import lung_tumor_invivo_infusion as data_model_object
    elif model_name == DataModelType.colon_cancer_cell_line:
        from . import colon_cancer_cell_line as data_model_object
    elif model_name == DataModelType.colon_cancer_cell_line_squared_loss:
        from . import colon_cancer_cell_line_squared_loss as data_model_object
    elif model_name == DataModelType.colon_cancer_cell_line_traditional_method:
        from . import colon_cancer_cell_line_traditional_method as data_model_object
    elif model_name == DataModelType.hct116_cultured_cell_line:
        from . import hct116_cultured_cell_line as data_model_object
    else:
        raise ValueError()
    return data_model_object
