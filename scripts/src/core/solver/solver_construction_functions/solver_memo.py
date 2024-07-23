from ...common.classes import MFAConfig
from ...model.model_class import MFAModel, CompositeNode, CompositeReaction
from ...data.data_class import MFAData


class ContentName(object):
    reaction_name = 'Name'
    sub_name = 'Substrate name'
    sub_carbon = 'Substrate carbon'
    sub_coeff = 'Substrate coefficient'
    pro_name = 'Product name'
    pro_carbon = 'Product carbon'
    pro_coeff = 'Product coefficient'
    reversible = 'Reversible'
    element_reaction_coeff = 'Reaction coefficient'
    element_reaction_name = 'Reaction name'
    data_name = 'Data name'
    metabolite_name = 'Metabolite(s) name'
    mid_name = 'Target node name'
    mid_mass = 'Isotopologue mass'
    mid_value = 'Isotopologue ratio'
    min_value = 'Min value'
    max_value = 'Max value'
    fixed_value = 'Fixed value'
    excluded_metabolites = 'Excluded metabolites'
    symmetrical_metabolites = 'Symmetrical metabolites'
    added_input_metabolites = '13C-labeled substrates'


class SolverMemo(object):
    def __init__(
            self, name, complete_reaction_list, complete_composite_reaction_dict,
            emu_excluded_metabolite_set, symmetrical_metabolite_set, added_input_metabolite_set,
            common_flux_range, specific_flux_range_dict,
            complete_constant_flux_dict, flatten_mix_equation_dict, mapped_mid_data_obj_dict, combined_data):
        if name is None:
            name = ''
        self.name = name
        self.complete_reaction_list = complete_reaction_list
        self.complete_composite_reaction_dict = complete_composite_reaction_dict
        self.emu_excluded_metabolite_set = emu_excluded_metabolite_set
        self.symmetrical_metabolite_set = symmetrical_metabolite_set
        self.added_input_metabolite_set = added_input_metabolite_set
        self.common_flux_range = common_flux_range
        self.specific_flux_range_dict = specific_flux_range_dict
        self.complete_constant_flux_dict = complete_constant_flux_dict
        self.flatten_mix_equation_dict = flatten_mix_equation_dict
        self.mapped_mid_data_obj_dict = mapped_mid_data_obj_dict
        self.combined_data = combined_data

    def output_sheet_in_excel(self, target_worksheet=None, target_workbook=None, same_model=False, same_data=False):
        if target_worksheet is None:
            worksheet_name = self.name
            target_worksheet = target_workbook.add_worksheet(worksheet_name)
        bold_format = target_workbook.add_format({'bold': True})
        solver_memo_output_to_excel_sheet(self, target_worksheet, same_model, same_data, bold_format)


def solver_memo_constructor(
        name, nested_mix_equation_dict, mix_ratio_balance_list,
        mfa_model: MFAModel, mfa_data: MFAData, mfa_config: MFAConfig, combined_data=False):
    def flatten_nested_mix_equation_dict(_nested_mix_equation, current_mix_name=None):
        if isinstance(_nested_mix_equation, str):
            if current_mix_name is not None:
                current_flatten_mix_equation_dict[current_mix_name] = _nested_mix_equation
            return _nested_mix_equation
        elif isinstance(_nested_mix_equation, dict):
            current_mix_item_dict = {}
            for _mix_ratio_name, _child_mix_equation in _nested_mix_equation.items():
                if current_mix_name is None:
                    current_mix_name = mix_ratio_name_mix_name_dict[_mix_ratio_name]
                current_mix_item = flatten_nested_mix_equation_dict(_child_mix_equation)
                current_mix_item_dict[_mix_ratio_name] = current_mix_item
            current_flatten_mix_equation_dict[current_mix_name] = current_mix_item_dict
            return current_mix_name
        else:
            raise ValueError()

    def nest_mix_equation_dict_converter(_nested_mix_equation_dict):
        for experimental_mid_data_name, mix_equation in _nested_mix_equation_dict.items():
            flatten_nested_mix_equation_dict(mix_equation, experimental_mid_data_name)

    complete_constant_flux_dict = dict(mfa_config.preset_constant_flux_value_dict)
    if len(mfa_config.dynamic_constant_flux_list) != 0:
        raise ValueError('Implement the dynamic constant flux list!')
    complete_reaction_list = list(mfa_model.user_defined_model.reaction_list)
    emu_excluded_metabolite_set = set(mfa_model.user_defined_model.emu_excluded_metabolite_set)
    symmetrical_metabolite_set = set(mfa_model.user_defined_model.symmetrical_metabolite_set)
    added_input_metabolite_set = set(mfa_model.user_defined_model.added_input_metabolite_set)
    specific_flux_range_dict = dict(mfa_config.specific_flux_range_dict)
    common_flux_range = mfa_config.common_flux_range
    mix_ratio_multiplier = mfa_config.mix_ratio_multiplier
    common_mix_range = tuple(
        [mix_ratio_multiplier * mix_ratio for mix_ratio in mfa_config.common_mix_ratio_range])
    mix_ratio_name_mix_name_dict = {}
    complete_composite_reaction_dict = dict(mfa_model.composite_reaction_dict)

    for mix_ratio_balance in mix_ratio_balance_list:
        compose_list = []
        mix_name = None
        for mix_ratio_name in mix_ratio_balance:
            if mix_name is None:
                mix_name = mix_ratio_name[:mix_ratio_name.rindex('_')]
            if mix_ratio_name not in mix_ratio_name_mix_name_dict:
                mix_ratio_name_mix_name_dict[mix_ratio_name] = mix_name
            current_composite_node = CompositeNode(mix_ratio_name)
            compose_list.append(current_composite_node)
            specific_flux_range_dict[mix_ratio_name] = common_mix_range
        compose_reaction = CompositeReaction(id=mix_name, comp=compose_list)
        complete_composite_reaction_dict[mix_name] = compose_reaction
        complete_constant_flux_dict[mix_name] = mix_ratio_multiplier

    raw_experimental_mid_data_obj_dict = mfa_data.experimental_mid_data_obj_dict
    if combined_data:
        target_flatten_mix_equation_dict = {}
        mapped_mid_data_obj_dict = {}
        for case_name, each_case_nested_mix_equation_dict in nested_mix_equation_dict.items():
            current_flatten_mix_equation_dict = {}
            mapped_mid_data_obj_dict[case_name] = {
                key: raw_experimental_mid_data_obj_dict[case_name][key] for key in each_case_nested_mix_equation_dict}
            nest_mix_equation_dict_converter(each_case_nested_mix_equation_dict)
            target_flatten_mix_equation_dict[case_name] = current_flatten_mix_equation_dict
    else:
        current_flatten_mix_equation_dict = {}
        mapped_mid_data_obj_dict = {key: raw_experimental_mid_data_obj_dict[key] for key in nested_mix_equation_dict}
        nest_mix_equation_dict_converter(nested_mix_equation_dict)
        target_flatten_mix_equation_dict = current_flatten_mix_equation_dict

    solver_memo_obj = SolverMemo(
        name, complete_reaction_list, complete_composite_reaction_dict, emu_excluded_metabolite_set,
        symmetrical_metabolite_set, added_input_metabolite_set, common_flux_range,
        specific_flux_range_dict, complete_constant_flux_dict,
        target_flatten_mix_equation_dict, mapped_mid_data_obj_dict, combined_data)
    return solver_memo_obj


def solver_memo_output_to_excel_sheet(self: SolverMemo, ws, same_model=False, same_data=False, bold_format=None):
    def sub_pro_output(sub_pro_obj_list, current_ws, current_row_index, begin_col_index):
        for sub_pro_row_index, (sub_name, sub_carbon, *coeff) in enumerate(sub_pro_obj_list):
            if len(coeff) == 0:
                coeff = 1
            else:
                coeff = coeff[0]
            current_content_list = (coeff, sub_name, sub_carbon)
            current_ws.write_row(current_row_index + sub_pro_row_index, begin_col_index, current_content_list)
        return len(sub_pro_obj_list)

    def mix_equation_output(_mixed_metabolite, _mix_equation_obj, current_ws, current_row_index, begin_col_index):
        if isinstance(_mix_equation_obj, str):
            current_content_list = [_mixed_metabolite, '', _mix_equation_obj]
            current_ws.write_row(current_row_index, begin_col_index, current_content_list)
            max_mix_index = 1
        elif isinstance(_mix_equation_obj, dict):
            max_mix_index = len(_mix_equation_obj)
            for mix_item_index, (mix_ratio_name, mix_mid_name) in enumerate(_mix_equation_obj.items()):
                if mix_item_index == 0:
                    current_content_list = [_mixed_metabolite, mix_ratio_name, mix_mid_name]
                else:
                    current_content_list = ['', mix_ratio_name, mix_mid_name]
                current_ws.write_row(
                    current_row_index + mix_item_index, begin_col_index, current_content_list)
        else:
            raise ValueError()
        return max_mix_index

    def composite_output(compose_list, current_ws, current_row_index, begin_col_index):
        for sub_pro_row_index, composite_node in enumerate(compose_list):
            current_content_list = (composite_node.coefficient, composite_node.reaction_id)
            current_ws.write_row(current_row_index + sub_pro_row_index, begin_col_index, current_content_list)
        return len(compose_list)

    def metabolite_mid_output(current_mid_data_obj, current_ws, current_row_index, begin_col_index):
        metabolite_name = current_mid_data_obj.full_name
        metabolite_data_vector = current_mid_data_obj.data_vector
        for data_vector_index, data_value in enumerate(metabolite_data_vector):
            data_vector_index_str = f'm+{data_vector_index}'
            if data_vector_index == 0:
                current_content_list = [metabolite_name, data_vector_index_str, data_value]
            else:
                current_content_list = ['', data_vector_index_str, data_value]
            current_ws.write_row(current_row_index + data_vector_index, begin_col_index, current_content_list)
        return len(metabolite_data_vector)

    complete_reaction_list = self.complete_reaction_list
    combined_data = self.combined_data
    flatten_mix_equation_dict = self.flatten_mix_equation_dict
    complete_composite_reaction_dict = self.complete_composite_reaction_dict
    emu_excluded_metabolite_set = self.emu_excluded_metabolite_set
    symmetrical_metabolite_set = self.symmetrical_metabolite_set
    added_input_metabolite_set = self.added_input_metabolite_set
    mid_data_obj_dict = self.mapped_mid_data_obj_dict
    common_flux_range = self.common_flux_range
    specific_flux_range_dict = self.specific_flux_range_dict
    complete_constant_flux_dict = self.complete_constant_flux_dict

    row_index = 0
    title_col = 0
    content_begin_col = 1
    interval_row_num = 2

    column_width_list = [15, 20, 20, 20, 15, 10, 20, 15]
    for column_index, column_width in enumerate(column_width_list):
        ws.set_column(column_index, column_index, column_width)

    # Reaction list
    ws.write(row_index, title_col, 'Metabolic network model', bold_format)
    row_index += 1
    if not same_model:
        ws.write(row_index, content_begin_col, 'Reaction list', bold_format)
        row_index += 1
        title_row_content = [
            ContentName.reaction_name,
            ContentName.sub_coeff, ContentName.sub_name, ContentName.sub_carbon,
            ContentName.pro_coeff, ContentName.pro_name, ContentName.pro_carbon,
            ContentName.reversible
        ]
        content_col_index_dict = {
            content: content_begin_col + content_index for content_index, content in enumerate(title_row_content)}
        ws.write_row(row_index, content_begin_col, title_row_content, bold_format)
        row_index += 1
        for reaction_obj in complete_reaction_list:
            ws.write(
                row_index, content_col_index_dict[ContentName.reaction_name], reaction_obj['id'])
            sub_num = sub_pro_output(
                reaction_obj['sub'], ws, row_index, content_col_index_dict[ContentName.sub_coeff])
            pro_num = sub_pro_output(
                reaction_obj['pro'], ws, row_index, content_col_index_dict[ContentName.pro_coeff])
            max_row_num = max(sub_num, pro_num)
            if 'reverse' in reaction_obj:
                reversible_reaction = reaction_obj['reverse']
            else:
                reversible_reaction = False
            ws.write(row_index, content_col_index_dict[ContentName.reversible], reversible_reaction)
            row_index += max_row_num
        row_index += 1

        # Excluded metabolites, symmetric metabolites and added metabolites
        title_row_content = [
            ContentName.excluded_metabolites, ContentName.symmetrical_metabolites, ContentName.added_input_metabolites
        ]
        excluded_metabolite_col = content_begin_col
        symmetrical_metabolite_col = content_begin_col + 1
        added_metabolite_col = content_begin_col + 2
        ws.write_row(row_index, content_begin_col, title_row_content, bold_format)
        row_index += 1
        max_row_index = len(emu_excluded_metabolite_set)
        for excluded_index, excluded_metabolite in enumerate(emu_excluded_metabolite_set):
            ws.write(row_index + excluded_index, excluded_metabolite_col, excluded_metabolite)
        max_row_index = max(max_row_index, len(symmetrical_metabolite_set))
        for symmetrical_index, symmetrical_metabolite in enumerate(symmetrical_metabolite_set):
            ws.write(row_index + symmetrical_index, symmetrical_metabolite_col, symmetrical_metabolite)
        max_row_index = max(max_row_index, len(added_input_metabolite_set))
        for added_index, added_metabolite in enumerate(added_input_metabolite_set):
            ws.write(row_index + added_index, added_metabolite_col, added_metabolite)
        row_index += max_row_index
    else:
        ws.write(row_index, title_col + 1, 'Same as before', bold_format)
    row_index += interval_row_num

    # Mix and MID reactions
    ws.write(row_index, title_col, 'Mixing and MID predictions', bold_format)
    row_index += 1
    if not same_data:
        if not combined_data:
            title_row_content = [
                '', ContentName.metabolite_name, ContentName.element_reaction_name, ContentName.mid_name]
            content_col_index_dict = {
                content: content_begin_col + content_index - 1
                for content_index, content in enumerate(title_row_content)}
            ws.write_row(row_index, content_begin_col - 1, title_row_content, bold_format)
            row_index += 1
            for mixed_metabolite, mix_equation_obj in flatten_mix_equation_dict.items():
                max_row_num = mix_equation_output(
                    mixed_metabolite, mix_equation_obj, ws, row_index, content_col_index_dict[ContentName.metabolite_name])
                row_index += max_row_num
        else:
            title_row_content = [
                ContentName.data_name, ContentName.metabolite_name, ContentName.element_reaction_name, ContentName.mid_name]
            content_col_index_dict = {
                content: content_begin_col + content_index - 1
                for content_index, content in enumerate(title_row_content)}
            ws.write_row(row_index, content_begin_col - 1, title_row_content, bold_format)
            row_index += 1
            for case_name, each_case_flatten_mix_equation_dict in flatten_mix_equation_dict.items():
                row_index += 1
                ws.write(row_index, content_col_index_dict[ContentName.data_name], case_name)
                for mixed_metabolite, mix_equation_obj in flatten_mix_equation_dict.items():
                    max_row_num = mix_equation_output(
                        mixed_metabolite, mix_equation_obj, ws, row_index,
                        content_col_index_dict[ContentName.metabolite_name])
                    row_index += max_row_num
    else:
        ws.write(row_index, title_col + 1, 'Same as before', bold_format)
    row_index += interval_row_num

    # Composite reactions
    ws.write(row_index, title_col, 'Composite reactions', bold_format)
    row_index += 1
    if not same_data:
        title_row_content = [
            ContentName.reaction_name, ContentName.element_reaction_coeff, ContentName.element_reaction_name,
        ]
        content_col_index_dict = {
            content: content_begin_col + content_index for content_index, content in enumerate(title_row_content)}
        ws.write_row(row_index, content_begin_col, title_row_content, bold_format)
        row_index += 1
        for compose_reaction in complete_composite_reaction_dict.values():
            ws.write(
                row_index, content_col_index_dict[ContentName.reaction_name],
                compose_reaction.reaction_id)
            reaction_num = composite_output(
                compose_reaction.compose_list, ws, row_index,
                content_col_index_dict[ContentName.element_reaction_coeff])
            row_index += reaction_num
    else:
        ws.write(row_index, title_col + 1, 'Same as before', bold_format)
    row_index += interval_row_num

    # MID data
    ws.write(row_index, title_col, 'MID data', bold_format)
    row_index += 1
    if not same_data:
        if not combined_data:
            title_row_content = [
                '', ContentName.metabolite_name, ContentName.mid_mass, ContentName.mid_value]
            content_col_index_dict = {
                content: content_begin_col + content_index - 1
                for content_index, content in enumerate(title_row_content)}
            ws.write_row(row_index, content_begin_col - 1, title_row_content, bold_format)
            row_index += 1
            for mid_data_obj in mid_data_obj_dict.values():
                max_row_num = metabolite_mid_output(
                    mid_data_obj, ws, row_index,
                    content_col_index_dict[ContentName.metabolite_name])
                row_index += max_row_num
        else:
            title_row_content = [
                ContentName.data_name, ContentName.metabolite_name, ContentName.mid_mass, ContentName.mid_value]
            content_col_index_dict = {
                content: content_begin_col + content_index - 1
                for content_index, content in enumerate(title_row_content)}
            ws.write_row(row_index, content_begin_col - 1, title_row_content, bold_format)
            row_index += 1
            for case_name, each_case_mid_data_obj_dict in mid_data_obj_dict.items():
                row_index += 1
                ws.write(row_index, content_col_index_dict[ContentName.data_name], case_name)
                for mid_data_obj in each_case_mid_data_obj_dict.values():
                    max_row_num = metabolite_mid_output(
                        mid_data_obj, ws, row_index, content_col_index_dict[ContentName.metabolite_name])
                    row_index += max_row_num
    else:
        ws.write(row_index, title_col + 1, 'Same as before', bold_format)
    row_index += interval_row_num

    # Flux range
    ws.write(row_index, title_col, 'Flux range', bold_format)
    row_index += 1
    title_row_content = [ContentName.reaction_name, ContentName.min_value, ContentName.max_value]
    ws.write_row(row_index, content_begin_col, title_row_content, bold_format)
    row_index += 1
    ws.write_row(row_index, content_begin_col, ['Common', *common_flux_range])
    row_index += 1
    for specific_flux_name, specific_flux_range in specific_flux_range_dict.items():
        ws.write_row(row_index, content_begin_col, [specific_flux_name, *specific_flux_range])
        row_index += 1
    row_index += interval_row_num

    # Constant flux
    ws.write(row_index, title_col, 'Constant flux', bold_format)
    row_index += 1
    title_row_content = [ContentName.reaction_name, ContentName.fixed_value]
    ws.write_row(row_index, content_begin_col, title_row_content, bold_format)
    row_index += 1
    for constant_flux_name, constant_flux_value in complete_constant_flux_dict.items():
        ws.write_row(row_index, content_begin_col, [constant_flux_name, constant_flux_value])
        row_index += 1
