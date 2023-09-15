
from common_and_plotting_functions.functions import replace_result_label_to_sheet_name, isdigit

from .third_party_packages import np, pd, xlsxwriter
from .config import Keywords
from scripts.src.core.common.functions import check_if_mix_flux, check_if_biomass_flux


index_and_title_format_dict = {
    'border': True,
    'align': 'center',
    'bold': True,
}

workbook_option_dict = {'strings_to_formulas': False, 'strings_to_urls': False}


def excel_sheet_information_process(
        result_label, result_information_dict, sheet_name_dict, sheet_information_dict,
        pandas=False):
    current_sheet_name = replace_result_label_to_sheet_name(result_label)
    suffix = 1
    new_sheet_name = current_sheet_name
    while new_sheet_name in sheet_information_dict:
        new_sheet_name = f'{current_sheet_name}_{suffix}'
        suffix += 1
    current_sheet_information_dict = {
        Keywords.complete_result_name_str: result_label,
    }
    if not pandas:
        current_sheet_information_dict[Keywords.sheet_name] = new_sheet_name
    for result_information_label, result_information_obj in result_information_dict.items():
        current_sheet_information_dict[result_information_label] = str(result_information_obj)
    sheet_information_dict[new_sheet_name] = current_sheet_information_dict
    sheet_name_dict[result_label] = new_sheet_name
    sheet_information_item_name_dict = {
        Keywords.sheet_name: None,
        Keywords.complete_result_name_str: None,
    }
    for key in result_information_dict.keys():
        sheet_information_item_name_dict[key] = None
    return sheet_information_item_name_dict


def sheet_information_output_to_excel_sheet(
        target_workbook, sheet_information_dict, sheet_information_item_name_list=None):
    column_width_list = [35, 35, 20, 10, 10, 15]
    sheet_information_ws = target_workbook.add_worksheet(name=Keywords.sheet_information_str)
    title_format = target_workbook.add_format(index_and_title_format_dict)
    for column_index, column_width in enumerate(column_width_list):
        sheet_information_ws.set_column(column_index, column_index, column_width)
    if sheet_information_item_name_list is not None:
        sheet_information_ws.write_row(0, 0, sheet_information_item_name_list, title_format)
    for row_index, (sheet_name, current_sheet_information_dict) in enumerate(sheet_information_dict.items()):
        if sheet_information_item_name_list is None:
            sheet_information_item_name_list = list(current_sheet_information_dict.keys())
            sheet_information_ws.write_row(0, 0, sheet_information_item_name_list, title_format)
        current_row = row_index + 1
        sheet_information_ws.write(
            current_row, 0, current_sheet_information_dict[sheet_information_item_name_list[0]], title_format)
        sheet_information_ws.write_row(
            current_row, 1,
            [
                current_sheet_information_dict[key] for key in sheet_information_item_name_list[1:]
                if key in current_sheet_information_dict])


def raw_flux_and_loss_output_to_excel_sheet(
        target_workbook, sheet_name, flux_name_index_dict, solution_array, loss_data_array=None,
        other_label_column_dict=None, index_list=None):
    total_data_size = solution_array.shape[0]
    if loss_data_array is not None:
        assert len(loss_data_array) == total_data_size
    if other_label_column_dict is None:
        other_label_column_dict = {}
    else:
        for other_label_list in other_label_column_dict.values():
            assert len(other_label_list) == total_data_size
    if index_list is None:
        index_list = [str(index + 1) for index in range(total_data_size)]
        index_column_width = 5
    else:
        index_column_width = 15
    normal_flux_column_width = 12
    mix_flux_column_width = 20
    sheet_information_ws = target_workbook.add_worksheet(name=sheet_name)
    title_format = target_workbook.add_format(index_and_title_format_dict)

    index_column_num = len(other_label_column_dict) + 1
    start_column_num = 0
    sheet_information_ws.set_column(start_column_num, start_column_num + index_column_num - 1, index_column_width)
    normal_flux_num = 0 if loss_data_array is None else 1
    mix_flux_num = 0
    for flux_name in flux_name_index_dict.keys():
        if check_if_mix_flux(flux_name) or check_if_biomass_flux(flux_name):
            mix_flux_num += 1
        else:
            normal_flux_num += 1
    start_column_num = index_column_num
    sheet_information_ws.set_column(
        start_column_num, start_column_num + normal_flux_num - 1, normal_flux_column_width)
    start_column_num = index_column_num + normal_flux_num
    sheet_information_ws.set_column(
        start_column_num, start_column_num + mix_flux_num - 1, mix_flux_column_width)

    loss_flux_array = np.vstack(
        [loss_data_array if loss_data_array is not None else np.zeros([0, total_data_size])] +
        [solution_array[:, flux_index] for flux_index in flux_name_index_dict.values()]).T

    complete_column_name_list = [Keywords.index_name]
    complete_column_name_list.extend(other_label_column_dict.keys())
    if loss_data_array is not None:
        complete_column_name_list.append(Keywords.loss)
    complete_column_name_list.extend(flux_name_index_dict.keys())
    sheet_information_ws.write_row(0, 0, complete_column_name_list, title_format)
    for index in range(total_data_size):
        current_row = index + 1
        sheet_information_ws.write(current_row, 0, index_list[index], title_format)
        current_row_list = []
        for other_label_list in other_label_column_dict.values():
            current_row_list.append(other_label_list[index])
        current_row_list.extend(loss_flux_array[index, :])
        sheet_information_ws.write_row(current_row, 1, current_row_list)


# def output_raw_flux_data_pd(
#         output_xlsx_file_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
#         final_information_dict, subset_index_dict=None, other_label_column_dict=None):
#     from .third_party_packages import pd
#
#     sheet_name_dict = {}
#     sheet_information_dict = {}
#     result_df_dict = {}
#     for result_label, raw_solution_array in final_solution_data_dict.items():
#         flux_name_index_dict = final_flux_name_index_dict[result_label]
#         raw_loss_data_array = final_loss_data_dict[result_label]
#         if subset_index_dict is not None:
#             filtered_index_array = subset_index_dict[result_label]
#             solution_array = raw_solution_array[filtered_index_array, :]
#             loss_data_array = raw_loss_data_array[filtered_index_array]
#         else:
#             solution_array = raw_solution_array
#             loss_data_array = raw_loss_data_array
#         data_size = len(loss_data_array)
#         if other_label_column_dict is not None and result_label in other_label_column_dict:
#             current_df_data_dict = {
#                 **other_label_column_dict[result_label],
#                 Keywords.loss: loss_data_array,
#             }
#         else:
#             current_df_data_dict = {
#                 Keywords.loss: loss_data_array,
#             }
#         for flux_name, flux_index in flux_name_index_dict.items():
#             current_df_data_dict[flux_name] = solution_array[:, flux_index]
#         result_df_dict[result_label] = pd.DataFrame(
#             data=current_df_data_dict, index=range(1, data_size + 1))
#         # current_sheet_name = replace_result_label_to_sheet_name(result_label)
#         # suffix = 1
#         # new_sheet_name = current_sheet_name
#         # while new_sheet_name in sheet_information_dict:
#         #     new_sheet_name = f'{current_sheet_name}_{suffix}'
#         #     suffix += 1
#         # sheet_information_dict[new_sheet_name] = {
#         #     Keywords.complete_result_name_str: result_label,
#         #     **final_information_dict[result_label]
#         # }
#         # sheet_name_dict[result_label] = new_sheet_name
#         excel_sheet_information_process(
#             result_label, final_information_dict[result_label], sheet_name_dict, sheet_information_dict,
#             pandas=True)
#     sheet_information_df = pd.DataFrame.from_dict(data=sheet_information_dict, orient='index')
#     with pd.ExcelWriter(
#             output_xlsx_file_path, engine_kwargs={'options': workbook_option_dict}) as writer:
#         sheet_information_df.to_excel(
#             writer, sheet_name=Keywords.sheet_information_str, index_label=Keywords.sheet_name)  # 'sheet_name'
#         for result_label, result_df in result_df_dict.items():
#             sheet_name = sheet_name_dict[result_label]
#             result_df.to_excel(writer, sheet_name=sheet_name, index_label='Index')


def output_raw_flux_data(
        output_xlsx_file_path, final_loss_data_dict, final_solution_data_dict, final_flux_name_index_dict,
        final_information_dict, subset_index_dict=None, other_label_column_dict=None):
    sheet_name_dict = {}
    sheet_information_dict = {}
    result_data_dict = {}
    for result_label, raw_solution_array in final_solution_data_dict.items():
        flux_name_index_dict = final_flux_name_index_dict[result_label]
        raw_loss_data_array = final_loss_data_dict[result_label]
        if subset_index_dict is not None:
            filtered_index_array = subset_index_dict[result_label]
            solution_array = raw_solution_array[filtered_index_array, :]
            loss_data_array = raw_loss_data_array[filtered_index_array]
        else:
            solution_array = raw_solution_array
            loss_data_array = raw_loss_data_array
        if other_label_column_dict is not None and result_label in other_label_column_dict:
            current_other_label_column_dict = other_label_column_dict[result_label]
        else:
            current_other_label_column_dict = None
        result_data_dict[result_label] = (
            flux_name_index_dict, solution_array, loss_data_array, current_other_label_column_dict)
        excel_sheet_information_process(
            result_label, final_information_dict[result_label], sheet_name_dict, sheet_information_dict,
            pandas=False)
    with xlsxwriter.Workbook(output_xlsx_file_path, options=workbook_option_dict) as workbook:
        sheet_information_output_to_excel_sheet(workbook, sheet_information_dict)
        for result_label, (flux_name_index_dict, solution_array, loss_data_array, current_other_label_column_dict) in \
                result_data_dict.items():
            sheet_name = sheet_name_dict[result_label]
            raw_flux_and_loss_output_to_excel_sheet(
                workbook, sheet_name, flux_name_index_dict, solution_array, loss_data_array,
                current_other_label_column_dict)


# def mid_dataframe_generator(
#         experimental_mid_data_dict=None, experimental_mid_column_name='experiment',
#         mid_data_dict=None, output_mid_num=None, mid_column_name_list=None,
#         extra_row_name_list_dict=None):
#     def add_one_mid_vector(
#             current_metabolite_name, current_mid_vector, current_metabolite_name_list=None,
#             current_output_metabolite_name_list=None, current_mid_index_list=None, current_mid_value_list_list=None):
#         if current_metabolite_name_list is not None:
#             current_metabolite_name_list.append(current_metabolite_name)
#         if len(current_mid_value_list_list) == 0 or not isinstance(current_mid_value_list_list[0], list):
#             example_mid_vector = current_mid_vector
#             current_mid_value_list_list.extend(example_mid_vector)
#         else:
#             example_mid_vector = current_mid_vector[0]
#             for current_complete_mid_value_vector, current_mid_value_list in zip(
#                     current_mid_vector, current_mid_value_list_list):
#                 for mid_value in current_complete_mid_value_vector:
#                     current_mid_value_list.append(mid_value)
#         for index, _ in enumerate(example_mid_vector):
#             if current_output_metabolite_name_list is not None:
#                 current_output_metabolite_name_list.append(current_metabolite_name)
#             if current_mid_index_list is not None:
#                 current_mid_index_list.append(index)
#
#     metabolite_name_list = []
#     output_metabolite_name_list = []
#     compartment_list = []
#     mid_index_list = []
#     experimental_value_list = []
#     empty_row_num = 0
#     empty_cell = ''
#     if mid_data_dict is not None:
#         if mid_column_name_list is None:
#             assert output_mid_num is not None
#             mid_column_name_list = [str(i + 1) for i in range(output_mid_num)]
#         mid_value_nested_list = [[] for _ in enumerate(mid_column_name_list)]
#     else:
#         mid_value_nested_list = []
#     if extra_row_name_list_dict is not None:
#         for item_name, item_value_list in extra_row_name_list_dict.items():
#             empty_row_num += 1
#             output_metabolite_name_list.append(item_name)
#             mid_index_list.append(empty_cell)
#             experimental_value_list.append(empty_cell)
#             for item_value, current_mid_value_list in zip(item_value_list, mid_value_nested_list):
#                 current_mid_value_list.append(item_value)
#     if experimental_mid_data_dict is not None:
#         for metabolite_name, mid_vector in experimental_mid_data_dict.items():
#             add_one_mid_vector(
#                 metabolite_name, mid_vector, metabolite_name_list, output_metabolite_name_list,
#                 mid_index_list, experimental_value_list)
#     if mid_data_dict is not None:
#         if len(experimental_value_list) != 0:
#             for metabolite_name in metabolite_name_list:
#                 current_mid_data_vector_list = mid_data_dict[metabolite_name]
#                 add_one_mid_vector(
#                     metabolite_name, current_mid_data_vector_list,
#                     current_mid_value_list_list=mid_value_nested_list)
#         else:
#             for metabolite_name, mid_vector in mid_data_dict.items():
#                 add_one_mid_vector(
#                     metabolite_name, mid_vector, metabolite_name_list, output_metabolite_name_list,
#                     mid_index_list, mid_value_nested_list)
#
#     current_data_dict_for_df = {
#         'metabolite_name': output_metabolite_name_list,
#         # 'compartment_list': compartment_list,
#         'mid_index': mid_index_list,
#     }
#     if experimental_mid_data_dict is not None:
#         current_data_dict_for_df[experimental_mid_column_name] = experimental_value_list
#     if mid_data_dict is not None:
#         for mid_column_name, current_column_mid_value_list in zip(mid_column_name_list, mid_value_nested_list):
#             current_data_dict_for_df[mid_column_name] = current_column_mid_value_list
#     current_df = pd.DataFrame(data=current_data_dict_for_df)
#     return current_df
#
#
# def output_predicted_mid_data_pd(
#         output_xlsx_file_path, final_loss_data_dict, final_predicted_mid_data_dict,
#         final_target_experimental_mid_data_dict, final_information_dict,
#         subset_index_dict=None):
#     sheet_name_dict = {}
#     sheet_information_dict = {}
#     result_df_dict = {}
#     for result_label, raw_predicted_mid_data_dict in final_predicted_mid_data_dict.items():
#         target_experimental_mid_data_dict = final_target_experimental_mid_data_dict[result_label]
#         raw_loss_data_array = final_loss_data_dict[result_label]
#         if subset_index_dict is not None:
#             predicted_mid_data_dict = {}
#             filtered_index_array = subset_index_dict[result_label]
#             loss_data_array = raw_loss_data_array[filtered_index_array]
#             for metabolite_name, mid_list in raw_predicted_mid_data_dict.items():
#                 predicted_mid_data_dict[metabolite_name] = [mid_list[i] for i in filtered_index_array]
#         else:
#             loss_data_array = raw_loss_data_array
#             predicted_mid_data_dict = raw_predicted_mid_data_dict
#         data_size = len(loss_data_array)
#         excel_sheet_information_process(
#             result_label, final_information_dict[result_label], sheet_name_dict, sheet_information_dict,
#             pandas=True)
#         result_df_dict[result_label] = mid_dataframe_generator(
#             experimental_mid_data_dict=target_experimental_mid_data_dict, experimental_mid_column_name='experiment',
#             mid_data_dict=predicted_mid_data_dict, output_mid_num=data_size,
#             extra_row_name_list_dict={'loss': loss_data_array})
#     sheet_information_df = pd.DataFrame.from_dict(data=sheet_information_dict, orient='index')
#     with pd.ExcelWriter(
#             output_xlsx_file_path, engine_kwargs={'options': workbook_option_dict}) as writer:
#         sheet_information_df.to_excel(
#             writer, sheet_name=Keywords.sheet_information_str, index_label=Keywords.sheet_name)  # 'sheet_name'
#         for result_label, result_df in result_df_dict.items():
#             sheet_name = sheet_name_dict[result_label]
#             result_df.to_excel(writer, sheet_name=sheet_name, index=False)


def experimental_and_predicted_mid_materials_generator(
        experimental_mid_data_dict=None, experimental_mid_column_name='experiment',
        mid_data_dict=None, extra_row_name_list_dict=None):
    def add_one_mid_vector(
            current_mid_data_dict, _guide_metabolite_name_list=None, current_output_metabolite_name_list=None,
            current_mid_index_list=None):
        append_name_and_mid = False
        if _guide_metabolite_name_list is None:
            append_name_and_mid = True
            _guide_metabolite_name_list = list(current_mid_data_dict.keys())
        mid_vector_list = []
        single_vector = None
        for metabolite_name in _guide_metabolite_name_list:
            current_mid_vector = current_mid_data_dict[metabolite_name]
            mid_vector_list.append(current_mid_vector)
            if single_vector is None:
                if isdigit(current_mid_vector[0]):
                    single_vector = True
                else:
                    single_vector = False
            current_vector_len = len(current_mid_vector)
            if append_name_and_mid and current_output_metabolite_name_list is not None:
                current_output_metabolite_name_list.extend((metabolite_name for _ in range(current_vector_len)))
            if append_name_and_mid and current_mid_index_list is not None:
                current_mid_index_list.extend(range(current_vector_len))
        if single_vector:
            _mid_vector_array = np.concatenate(mid_vector_list).reshape(-1, 1)
            _vector_num = 1
        else:
            _mid_vector_array = np.concatenate(mid_vector_list, axis=1).T
            _vector_num = _mid_vector_array.shape[1]
        _mid_dim = _mid_vector_array.shape[0]
        return _guide_metabolite_name_list, _mid_vector_array, _mid_dim, _vector_num

    guide_metabolite_name_list = None
    sheet_column_name_list = ['metabolite_name', 'mid_index']
    output_metabolite_name_list = []
    mid_index_list = []
    extra_row_value_array = None
    empty_cell = ''
    if extra_row_name_list_dict is not None:
        extra_row_value_list = []
        for item_name, item_value_list in extra_row_name_list_dict.items():
            output_metabolite_name_list.append(item_name)
            mid_index_list.append(empty_cell)
            extra_row_value_list.append(item_value_list)
        extra_row_value_array = np.array(extra_row_value_list)
    mid_dim = 0
    vector_num = 0
    experimental_vector_num = 0
    experimental_mid_vector_array = None
    mid_vector_array = None
    if experimental_mid_data_dict is not None:
        (
            guide_metabolite_name_list, experimental_mid_vector_array, mid_dim,
            experimental_vector_num) = add_one_mid_vector(
            experimental_mid_data_dict, guide_metabolite_name_list, output_metabolite_name_list, mid_index_list)
        sheet_column_name_list.append(experimental_mid_column_name)
    if mid_data_dict is not None:
        _, mid_vector_array, mid_dim, vector_num = add_one_mid_vector(
            mid_data_dict, guide_metabolite_name_list, output_metabolite_name_list, mid_index_list)
        sheet_column_name_list.extend([str(index + 1) for index in range(vector_num)])
    if experimental_mid_vector_array is None:
        experimental_mid_vector_array = np.zeros([mid_dim, 0])
    if mid_vector_array is None:
        mid_vector_array = np.zeros([mid_dim, 0])
    if extra_row_value_array is None:
        extra_row_value_array = np.zeros([0, vector_num])
    extra_row_num = extra_row_value_array.shape[0]
    final_numeric_array = np.block([
        [np.zeros([extra_row_num, experimental_vector_num]), extra_row_value_array],
        [experimental_mid_vector_array, mid_vector_array]
    ])
    return sheet_column_name_list, output_metabolite_name_list, mid_index_list, final_numeric_array


def experimental_and_predicted_mid_output_to_excel_sheet(
        target_workbook, sheet_name, sheet_column_name_list, output_metabolite_name_list, mid_index_list,
        final_numeric_array):
    metabolite_name_width = 20
    metabolite_index_width = 10
    mid_value_width = 15
    sheet_information_ws = target_workbook.add_worksheet(name=sheet_name)
    title_format = target_workbook.add_format(index_and_title_format_dict)

    sheet_information_ws.set_column(0, 0, metabolite_name_width)
    sheet_information_ws.set_column(1, 1, metabolite_index_width)
    sheet_information_ws.set_column(2, len(sheet_column_name_list) - 1, mid_value_width)
    total_data_size = len(output_metabolite_name_list)

    sheet_information_ws.write_row(0, 0, sheet_column_name_list, title_format)
    for index in range(total_data_size):
        current_row = index + 1
        current_row_list = [output_metabolite_name_list[index], mid_index_list[index]]
        current_row_list.extend(final_numeric_array[index, :])
        sheet_information_ws.write_row(current_row, 0, current_row_list)


def output_predicted_mid_data(
        output_xlsx_file_path, final_loss_data_dict, final_predicted_mid_data_dict,
        final_target_experimental_mid_data_dict, final_information_dict, subset_index_dict=None,
        other_label_row_dict=None):
    sheet_name_dict = {}
    sheet_information_dict = {}
    result_data_dict = {}
    if other_label_row_dict is None:
        other_label_row_dict = {}
    for result_label, raw_predicted_mid_data_dict in final_predicted_mid_data_dict.items():
        target_experimental_mid_data_dict = final_target_experimental_mid_data_dict[result_label]
        raw_loss_data_array = final_loss_data_dict[result_label]
        if subset_index_dict is not None:
            predicted_mid_data_dict = {}
            filtered_index_array = subset_index_dict[result_label]
            loss_data_array = raw_loss_data_array[filtered_index_array]
            for metabolite_name, mid_list in raw_predicted_mid_data_dict.items():
                predicted_mid_data_dict[metabolite_name] = [mid_list[i] for i in filtered_index_array]
        else:
            loss_data_array = raw_loss_data_array
            predicted_mid_data_dict = raw_predicted_mid_data_dict
        if result_label in other_label_row_dict:
            current_other_label_row = other_label_row_dict[result_label]
        else:
            current_other_label_row = {}
        extra_row_name_list_dict = {**current_other_label_row, Keywords.loss: loss_data_array}
        excel_sheet_information_process(
            result_label, final_information_dict[result_label], sheet_name_dict, sheet_information_dict,
            pandas=False)
        result_data_dict[result_label] = experimental_and_predicted_mid_materials_generator(
            experimental_mid_data_dict=target_experimental_mid_data_dict,
            experimental_mid_column_name=Keywords.experiments, mid_data_dict=predicted_mid_data_dict,
            extra_row_name_list_dict=extra_row_name_list_dict)
    with xlsxwriter.Workbook(output_xlsx_file_path, options=workbook_option_dict) as workbook:
        sheet_information_output_to_excel_sheet(workbook, sheet_information_dict)
        for result_label, (
                sheet_column_name_list, output_metabolite_name_list, mid_index_list, final_numeric_array) in \
                result_data_dict.items():
            sheet_name = sheet_name_dict[result_label]
            experimental_and_predicted_mid_output_to_excel_sheet(
                workbook, sheet_name, sheet_column_name_list, output_metabolite_name_list, mid_index_list,
                final_numeric_array)


def solver_memo_output(
        output_xlsx_file_path, sheet_name_dict, sheet_information_dict, solver_obj_dict,
        sheet_information_item_name_list, same_model_dict=None, same_data_dict=None):
    with xlsxwriter.Workbook(output_xlsx_file_path, options=workbook_option_dict) as workbook:
        # sheet_information_ws = workbook.add_worksheet(name=Keywords.sheet_information_str)
        # title_format = workbook.add_format({'bold': True})
        # sheet_information_ws.write_row(0, 0, sheet_information_item_name_list, title_format)
        # for row_index, (sheet_name, current_sheet_information_dict) in enumerate(sheet_information_dict.items()):
        #     sheet_information_ws.write_row(
        #         row_index + 1, 0,
        #         [
        #             current_sheet_information_dict[key] for key in sheet_information_item_name_list
        #             if key in current_sheet_information_dict])
        sheet_information_output_to_excel_sheet(
            workbook, sheet_information_dict, sheet_information_item_name_list)
        for result_label, solver_obj in solver_obj_dict.items():
            sheet_name = sheet_name_dict[result_label]
            current_solver_ws = workbook.add_worksheet(name=sheet_name)
            if same_model_dict is None:
                same_model = False
            else:
                same_model = same_model_dict[result_label]
            if same_data_dict is None:
                same_data = False
            else:
                same_data = same_data_dict[result_label]
            solver_obj.solver_memo.output_sheet_in_excel(
                current_solver_ws, target_workbook=workbook, same_model=same_model, same_data=same_data)


def solver_output(
        solver_dict, final_information_dict, final_result_obj, same_model_dict, same_data_dict):
    sheet_name_dict = {}
    sheet_information_dict = {}
    sheet_information_item_name_dict = {}
    for result_label, result_information_dict in final_information_dict.items():
        tmp_information_item_dict = excel_sheet_information_process(
            result_label, result_information_dict, sheet_name_dict, sheet_information_dict)
        sheet_information_item_name_dict.update(tmp_information_item_dict)
    solver_memo_output(
        final_result_obj.solver_descriptions_output_xlsx_path, sheet_name_dict, sheet_information_dict,
        solver_dict, list(sheet_information_item_name_dict.keys()), same_model_dict=same_model_dict,
        same_data_dict=same_data_dict)

