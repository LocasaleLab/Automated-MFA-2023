from .config import Vector, ParameterName, CommonElementConfig, Line, FontWeight
from .config import CompositeFigure, TextBox, CommonFigureString, ColorConfig, ZOrderConfig


class AllExperimentalMIDBriefComparison(CompositeFigure):
    title_height = 0.1
    each_row_height = 0.08
    total_width = 1.2

    def __init__(self, **kwargs):
        flux_range_label_list = [
            ['Characteristic', CommonFigureString.all_available_mid_data, CommonFigureString.experimental_available_mid_data_wrap2],
            ['Metabolite coverage', 'Measures all metabolites', 'Measures only part of metabolites'],
            ['Compartmentalized MID', 'Compartmentalized MID\nmeasured separately', 'Compartmentalized MID\nmeasured together (mixed)'],
        ]
        column_width_list = [0.35, 0.4, 0.45]
        total_row_num = len(flux_range_label_list)
        total_width = self.total_width
        each_row_height = self.each_row_height
        title_height = self.title_height
        table_height = total_row_num * each_row_height
        total_height = table_height + title_height
        self.total_height = total_height
        self.height_to_width_ratio = total_height / total_width
        total_size = Vector(total_width, total_height)
        common_text_config = {
            **CommonElementConfig.common_text_config,
            ParameterName.font_size: CommonElementConfig.normal_document_size + 2,
            ParameterName.height: each_row_height,
        }
        common_border_config = {
            ParameterName.edge_width: 2,
            ParameterName.edge_color: ColorConfig.dark_blue,
            ParameterName.z_order: ZOrderConfig.default_text_z_order,
        }

        text_config_list = []
        table_border_list = []
        full_border_left = 0
        full_border_right = total_width
        for row_index, row_label_list in enumerate(flux_range_label_list):
            # current_col_num = len(row_label_list)
            # each_col_width = total_width / current_col_num
            current_y_loc = table_height - (row_index + 0.5) * each_row_height
            upper_y_loc = current_y_loc + 0.5 * each_row_height
            bottom_y_loc = current_y_loc - 0.5 * each_row_height
            start_x_loc = 0
            for col_index, each_string in enumerate(row_label_list):
                col_width = column_width_list[col_index]
                current_x_loc = start_x_loc + col_width / 2
                # current_x_loc = (col_index + 0.5) * col_width
                this_text_config = {
                    **common_text_config,
                    ParameterName.string: each_string,
                    ParameterName.width: col_width,
                    ParameterName.center: Vector(current_x_loc, current_y_loc),
                    ParameterName.text_box: False,
                }
                if row_index == 0:
                    this_text_config[ParameterName.font_weight] = FontWeight.bold
                text_config_list.append(this_text_config)
                start_x_loc += col_width
            if row_index == 0:
                table_border_list.extend([
                    {
                        **common_border_config,
                        ParameterName.start: Vector(full_border_left, upper_y_loc),
                        ParameterName.end: Vector(full_border_right, upper_y_loc),
                    },
                    {
                        **common_border_config,
                        ParameterName.start: Vector(full_border_left, bottom_y_loc),
                        ParameterName.end: Vector(full_border_right, bottom_y_loc),
                    },
                ])
            elif row_index == total_row_num - 1:
                table_border_list.append({
                    **common_border_config,
                    ParameterName.start: Vector(full_border_left, bottom_y_loc),
                    ParameterName.end: Vector(full_border_right, bottom_y_loc),
                })
        title_config_dict = {
            **CommonElementConfig.common_text_config,
            ParameterName.string: 'Difference in datasets',
            ParameterName.font_size: CommonElementConfig.icon_text_size + 2,
            ParameterName.width: total_width,
            ParameterName.height: title_height,
            ParameterName.center: Vector(0.5 * total_width, table_height + title_height / 2)
        }

        element_dict = {
            'title': {'title': TextBox(**title_config_dict)},
            'table': {},
            'border': {},
        }
        for text_config in text_config_list:
            text_box_obj = TextBox(**text_config)
            element_dict['table'][text_box_obj.name] = text_box_obj
        for border_config in table_border_list:
            border_box_obj = Line(**border_config)
            element_dict['border'][border_box_obj.name] = border_box_obj

        super().__init__(element_dict, Vector(0, 0), total_size, background=False, **kwargs)

