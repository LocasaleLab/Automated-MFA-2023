def excel_column_letter_to_0_index(raw_column_str):
    final_index = -1
    for loc_index, letter in enumerate(raw_column_str[::-1]):
        letter_index = ord(letter) - ord('A') + 1
        if not 0 <= letter_index <= 26:
            raise ValueError('Should pass letter between A to Z: {}'.format(raw_column_str))
        final_index += letter_index * (26 ** loc_index)
    return final_index


def update_parameter_object(original_parameter_object, new_parameter_object):
    for item_key, item_value in new_parameter_object.__class__.__dict__.items():
        if not item_key.startswith('__'):
            if hasattr(original_parameter_object, item_key) and isinstance(
                    getattr(original_parameter_object, item_key), dict):
                getattr(original_parameter_object, item_key).update(item_value)
            else:
                original_parameter_object.__setattr__(item_key, item_value)
    return original_parameter_object


def add_empty_obj(root_dict, final_empty_class, *args):
    current_dict = root_dict
    total_arg_num = len(args)
    for label_index, label in enumerate(args):
        if label not in current_dict:
            if label_index == total_arg_num - 1:
                current_dict[label] = final_empty_class()
            else:
                current_dict[label] = {}
        current_dict = current_dict[label]
