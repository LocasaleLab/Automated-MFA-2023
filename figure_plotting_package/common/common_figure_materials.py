from .config import ParameterName
from .color import ColorConfig, ZOrderConfig, TextConfig


class CommonElementConfig(object):
    icon_text_size = 25
    normal_document_size = 15
    smaller_document_size = normal_document_size - 2
    larger_document_size = normal_document_size + 2
    bottom_document_size = normal_document_size + 1
    text_z_order = ZOrderConfig.default_text_z_order
    child_diagram_base_z_order = ZOrderConfig.default_axis_z_order
    child_diagram_z_order_increment = 0.01

    normal_chevron_width = 0.05
    arc_chevron_width = normal_chevron_width + 0.01
    chevron_config = {
        ParameterName.head_len_width_ratio: 0.4,
        ParameterName.width: normal_chevron_width,
        ParameterName.edge_width: None,
        ParameterName.face_color: ColorConfig.light_bright_sky,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order,
    }
    normal_chevron_head_len = normal_chevron_width * chevron_config[ParameterName.head_len_width_ratio]

    background_rectangle_config_dict = {
        ParameterName.width: 1,
        ParameterName.face_color: ColorConfig.light_gray,
        ParameterName.edge_width: None,
        ParameterName.z_order: ZOrderConfig.default_image_z_order,
    }

    simulated_background_config_dict = {
        # ParameterName.text: TextConfig.main_text_font,
        ParameterName.radius: 0.02,
        # ParameterName.face_color: ColorConfig.medium_light_blue,
        ParameterName.face_color: ColorConfig.medium_light_bright_blue,
        ParameterName.edge_width: None,
        ParameterName.z_order: ZOrderConfig.default_patch_z_order - 0.5,
    }

    common_text_config = {
        ParameterName.font: TextConfig.main_text_font,
        ParameterName.z_order: ZOrderConfig.default_text_z_order,
    }

