from ..config import ParameterName, MetaboliteConfig, ElementName, Arrow, ArcArrow, ArcPathArrow, BentArrow, \
    BrokenArrow


def modify_size_of_long_text(text_param_dict, display_name):
    if len(display_name) == 4:
        text_param_dict[ParameterName.font_size] = MetaboliteConfig.smaller_font_size
    elif len(display_name) >= 5:
        text_param_dict[ParameterName.font_size] = MetaboliteConfig.smallest_font_size


arrow_dict = {
    ElementName.Arrow: Arrow,
    ElementName.ArcArrow: ArcArrow,
    ElementName.ArcPathArrow: ArcPathArrow,
    ElementName.BentArrow: BentArrow,
    ElementName.BrokenArrow: BrokenArrow,
}

complete_arrow_parameter_set_dict = {
    ParameterName.common: {
        ParameterName.head_width,
        ParameterName.stem_width,
        ParameterName.head_len_width_ratio,
        ParameterName.tail_arrow,
        ParameterName.head_arrow,
        ParameterName.gap_line_pair_list,
        ParameterName.dash_solid_empty_width,
        ParameterName.branch_list,
    },
    ElementName.Arrow: {
        ParameterName.tail,
        ParameterName.head,
    },
    ElementName.ArcArrow: {
        ParameterName.center,
        ParameterName.radius,
        ParameterName.theta_head,
        ParameterName.theta_tail,
    },
    ElementName.ArcPathArrow: {
        ParameterName.tail,
        ParameterName.mid,
        ParameterName.head,
    },
    ElementName.BentArrow: {
        ParameterName.tail,
        ParameterName.head,
        ParameterName.radius,
        ParameterName.arrow_head_direction,
    },
    ElementName.BrokenArrow: {
        ParameterName.tail,
        ParameterName.head,
        ParameterName.transition_point_list,
    },
}


