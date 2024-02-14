from ..config import Vector, ParameterName, ColorConfig, ZOrderConfig
from ..config import CompositeFigure, PathStep, PathOperation, PathShape, Rectangle, Ellipse, ellipse_arc_obj


class CulturedCellConfig(object):
    common_z_order = ZOrderConfig.default_patch_z_order
    z_order_increment = ZOrderConfig.z_order_increment
    dish_outline_z_order = common_z_order + 2 * z_order_increment
    media_z_order = common_z_order
    cell_z_order = common_z_order - z_order_increment
    cell_nucleus_z_order = cell_z_order + z_order_increment

    media_color = ColorConfig.orange
    media_side_alpha = ColorConfig.lower_alpha_value
    media_top_alpha = ColorConfig.alpha_for_bar_plot
    common_edge_width = 9.5
    infusion_rect_edge_width = common_edge_width - 1
    cell_alpha = ColorConfig.higher_alpha
    cell_nucleus_alpha = 1

    dish_outline_config = {
        ParameterName.edge_width: common_edge_width,
        ParameterName.edge_color: ColorConfig.black_color,
        ParameterName.face_color: None,
        ParameterName.z_order: dish_outline_z_order
    }
    media_config = {
        ParameterName.edge_width: None,
        ParameterName.z_order: media_z_order
    }
    media_top_config = {
        **media_config,
        ParameterName.face_color: media_color.add_transparency(media_top_alpha)
    }
    media_side_config = {
        **media_config,
        ParameterName.face_color: media_color.add_transparency(media_side_alpha)
    }
    cell_config = {
        ParameterName.edge_width: None,
        ParameterName.z_order: cell_z_order,
        ParameterName.face_color: media_color.add_transparency(cell_alpha)
    }
    cell_nucleus_config = {
        ParameterName.edge_width: None,
        ParameterName.z_order: cell_nucleus_z_order,
        ParameterName.face_color: media_color.add_transparency(cell_nucleus_alpha)
    }


class CulturedCell(CompositeFigure):
    total_width = 1
    height_to_width_ratio = 0.4

    def __init__(self, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        total_width = self.total_width
        total_height = self.height_to_width_ratio * total_width
        ellipse_height_to_width_ratio = self.height_to_width_ratio / 2
        center_x = total_width / 2
        ellipse_width = total_width
        ellipse_height = ellipse_height_to_width_ratio * ellipse_width
        dish_height = (self.height_to_width_ratio - ellipse_height_to_width_ratio) * total_width

        bottom_ellipse_center_y = ellipse_height / 2
        top_ellipse_center_y = bottom_ellipse_center_y + dish_height
        media_height = dish_height * 0.6
        media_top_ellipse_center_y = bottom_ellipse_center_y + media_height

        cell_width = 0.15 * total_width
        cell_height = 0.17 * total_height
        cell_nucleus_width = 0.3 * cell_width
        cell_nucleus_height = 0.3 * cell_height

        cell_location_list = [
            Vector(center_x - 0.1 * total_width, bottom_ellipse_center_y - 0.12 * media_height),
            Vector(center_x + 0.254 * total_width, bottom_ellipse_center_y + 0.463 * media_height),
            Vector(center_x + 0.1 * total_width, bottom_ellipse_center_y + 0.32 * media_height),
            Vector(center_x - 0.34 * total_width, bottom_ellipse_center_y + 0.31 * media_height),
            Vector(center_x - 0.2386 * total_width, bottom_ellipse_center_y - 0.083 * media_height),
            Vector(center_x + 0.05 * total_width, bottom_ellipse_center_y - 0.33 * media_height),
            Vector(center_x + 0.325 * total_width, bottom_ellipse_center_y - 0.062 * media_height),
        ]
        cell_nucleus_relative_location = Vector(0, 0.1)

        cell_obj_list = []
        for cell_location in cell_location_list:
            cell_obj = Ellipse(**{
                ParameterName.center: cell_location,
                ParameterName.width: cell_width,
                ParameterName.height: cell_height,
                ParameterName.name: 'cell',
                **CulturedCellConfig.cell_config
            })
            cell_nucleus_location = cell_location + cell_nucleus_relative_location * Vector(cell_width, cell_height)
            cell_nucleus_obj = Ellipse(**{
                ParameterName.center: cell_nucleus_location,
                ParameterName.width: cell_nucleus_width,
                ParameterName.height: cell_nucleus_height,
                ParameterName.name: 'cell_nucleus',
                **CulturedCellConfig.cell_nucleus_config
            })
            cell_obj_list.extend([cell_obj, cell_nucleus_obj])

        bottom_half_ellipse = ellipse_arc_obj.generator(
            Vector(center_x, bottom_ellipse_center_y),
            -180, 0, ellipse_width / 2, ellipse_height / 2
        )
        left_vertical_path = [
            PathStep(PathOperation.moveto, Vector(center_x - ellipse_width / 2, top_ellipse_center_y)),
            PathStep(PathOperation.lineto, Vector(center_x - ellipse_width / 2, bottom_ellipse_center_y))
        ]
        right_vertical_path = [
            # PathStep(PathOperation.moveto, Vector(center_x + ellipse_width / 2, bottom_ellipse_center_y)),
            PathStep(PathOperation.lineto, Vector(center_x + ellipse_width / 2, top_ellipse_center_y))
        ]
        media_left_vertical_path = [
            PathStep(PathOperation.moveto, Vector(center_x - ellipse_width / 2, media_top_ellipse_center_y)),
            PathStep(PathOperation.lineto, Vector(center_x - ellipse_width / 2, bottom_ellipse_center_y))
        ]
        media_right_vertical_path = [
            # PathStep(PathOperation.moveto, Vector(center_x + ellipse_width / 2, bottom_ellipse_center_y)),
            PathStep(PathOperation.lineto, Vector(center_x + ellipse_width / 2, media_top_ellipse_center_y))
        ]
        media_top_half_ellipse = ellipse_arc_obj.generator(
            Vector(center_x, media_top_ellipse_center_y),
            0, -180, ellipse_width / 2, ellipse_height / 2
        )

        dish_outline_obj_list = [
            Ellipse(**{
                ParameterName.center: Vector(center_x, top_ellipse_center_y),
                ParameterName.width: ellipse_width,
                ParameterName.height: ellipse_height,
                ParameterName.name: 'top_outline_ellipse',
                **CulturedCellConfig.dish_outline_config
            }),
            PathShape(**{
                ParameterName.path_step_list: [*left_vertical_path, *bottom_half_ellipse, *right_vertical_path],
                ParameterName.closed: False,
                ParameterName.name: 'bottom_outline',
                **CulturedCellConfig.dish_outline_config
            })
        ]

        media_obj_list = [
            Ellipse(**{
                ParameterName.center: Vector(center_x, media_top_ellipse_center_y),
                ParameterName.width: ellipse_width,
                ParameterName.height: ellipse_height,
                ParameterName.name: 'media_top',
                **CulturedCellConfig.media_top_config,
            }),
            PathShape(**{
                ParameterName.path_step_list: [
                    *media_left_vertical_path, *bottom_half_ellipse, *media_right_vertical_path,
                    *media_top_half_ellipse],
                ParameterName.name: 'media_side',
                **CulturedCellConfig.media_side_config,
            })
        ]

        cultured_cell_dict = {
            ParameterName.dish_outline: {
                dish_outline_obj.name: dish_outline_obj for dish_outline_obj in dish_outline_obj_list},
            ParameterName.media: {
                media_obj.name: media_obj for media_obj in media_obj_list},
            ParameterName.cell: {
                cell_obj.name: cell_obj for cell_obj in cell_obj_list}
        }
        super().__init__(
            cultured_cell_dict, bottom_left=Vector(0, 0), size=Vector(total_width, total_height),
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)

