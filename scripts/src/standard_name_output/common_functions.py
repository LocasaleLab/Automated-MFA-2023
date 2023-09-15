from scripts.model.model_metabolite_to_standard_name_dict import model_metabolite_to_standard_name_dict
from scripts.model.model_reaction_to_standard_name_dict import model_reaction_to_standard_name_dict
from common_and_plotting_functions.functions import check_and_mkdir_of_direct
from ..common.config import Direct
from ..common.third_party_packages import xlsxwriter
from ..common.result_output_functions import index_and_title_format_dict, workbook_option_dict


def write_excel_by_xlsxwriter(
        output_xlsx_file_path, metabolite_sheet_name, reaction_sheet_name, model_name_title, standard_name_title,
        index_label):
    def output_standard_name_dict_to_excel_sheet(standard_name_dict, current_worksheet, start_row=0, start_col=0):
        for column_index, column_width in enumerate(column_width_list):
            current_worksheet.set_column(column_index, column_index, column_width)
        current_row = start_row
        current_worksheet.write_row(
            current_row, start_col, [index_label, model_name_title, standard_name_title], index_and_title_format)
        current_row += 1
        for index, (key, value) in enumerate(standard_name_dict.items()):
            current_worksheet.write(current_row, start_col, index + 1, index_and_title_format)
            current_worksheet.write_row(current_row, start_col + 1, [key, value])
            current_row += 1

    column_width_list = [8, 20, 20]
    with xlsxwriter.Workbook(
            output_xlsx_file_path, options=workbook_option_dict) as workbook:
        index_and_title_format = workbook.add_format(index_and_title_format_dict)
        metabolite_worksheet = workbook.add_worksheet(name=metabolite_sheet_name)
        output_standard_name_dict_to_excel_sheet(model_metabolite_to_standard_name_dict, metabolite_worksheet)
        reaction_worksheet = workbook.add_worksheet(name=reaction_sheet_name)
        output_standard_name_dict_to_excel_sheet(model_reaction_to_standard_name_dict, reaction_worksheet)


def write_excel_by_pd(
        output_xlsx_file_path, metabolite_sheet_name, reaction_sheet_name,
        model_name_title, standard_name_title, index_label):
    from ..common.third_party_packages import pd

    def convert_standard_name_dict_to_df(standard_name_dict):
        model_name_list = standard_name_dict.keys()
        standard_name_list = standard_name_dict.values()
        return pd.DataFrame.from_dict(
            data={model_name_title: model_name_list, standard_name_title: standard_name_list})

    metabolite_to_standard_name_df = convert_standard_name_dict_to_df(model_metabolite_to_standard_name_dict)
    reaction_to_standard_name_df = convert_standard_name_dict_to_df(model_reaction_to_standard_name_dict)
    with pd.ExcelWriter(
            output_xlsx_file_path, engine_kwargs={'options': workbook_option_dict}) as writer:
        metabolite_to_standard_name_df.to_excel(writer, sheet_name=metabolite_sheet_name, index_label=index_label)
        reaction_to_standard_name_df.to_excel(writer, sheet_name=reaction_sheet_name, index_label=index_label)


def output_to_xlsx_file(output_xlsx_file_path):

    index_label = 'Index'
    metabolite_sheet_name = 'Metabolites'
    reaction_sheet_name = 'Reactions'
    model_name_title = 'Model name'
    standard_name_title = 'Standard name'

    write_excel_by_xlsxwriter(
        output_xlsx_file_path, metabolite_sheet_name, reaction_sheet_name, model_name_title, standard_name_title,
        index_label)


def standard_name_output():
    standard_name_list_direct = Direct.common_submitted_raw_data_direct
    check_and_mkdir_of_direct(standard_name_list_direct)
    xlsx_file_path = f'{standard_name_list_direct}/standard_name.xlsx'
    output_to_xlsx_file(xlsx_file_path)
