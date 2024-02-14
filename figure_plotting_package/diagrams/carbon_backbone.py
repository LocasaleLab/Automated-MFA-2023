from .config import Vector, ParameterName, ColorConfig, ZOrderConfig
from .config import CompositeFigure, PathStep, PathOperation, PathShape, Rectangle, Circle, cos_sin


class CarbonBackboneConfig(object):
    common_z_order = ZOrderConfig.default_patch_z_order
    z_order_increment = ZOrderConfig.z_order_increment
    ear2_z_order = common_z_order + z_order_increment

    carbon_radius = 0.04
    unlabeled_color = ColorConfig.light_blue
    labeled_color = ColorConfig.slightly_light_orange

    single_carbon_backbone_config = {
        ParameterName.edge_width: None,
        ParameterName.radius: carbon_radius,
        ParameterName.z_order: common_z_order
    }


class SingleCarbonBackbone(CompositeFigure):
    def __init__(
            self, center: Vector, carbon_num: int, radius: float, angle=0,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        short_edge = radius * 2
        long_edge = radius * 2 * carbon_num
        assert -90 <= angle <= 90
        if -45 <= angle <= 45:
            width = long_edge
            height = short_edge
            bound_angle = angle
        else:
            if angle > 45:
                bound_angle = angle - 90
            else:
                bound_angle = angle + 90
            width = short_edge
            height = long_edge
        bound_rectangle = Rectangle(center, width, height, bound_angle)
        circle_center_dict = {
            f'circle_{index}': center - radius * (2 * index - carbon_num + 1) * cos_sin(angle)
            for index in range(carbon_num)}
        circle_obj_dict = {
            name: Circle(**{
                ParameterName.center: circle_center,
                ParameterName.radius: radius,
                ParameterName.name: name,
                ParameterName.z_order: ZOrderConfig.default_patch_z_order,
                **kwargs
            })
            for name, circle_center in circle_center_dict.items()
        }
        single_carbon_backbone_dict = {
            # 'bound': {'bound_rectangle': bound_rectangle},
            'circles': circle_obj_dict,
        }
        super().__init__(
            single_carbon_backbone_dict, bottom_left=bound_rectangle.bottom_left, size=bound_rectangle.size,
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)


class CarbonBackbone(CompositeFigure):
    total_width = 1
    height_to_width_ratio = 1

    def __init__(
            self, carbon_num: int, labeled=True,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        total_width = self.total_width
        total_height = total_width * self.height_to_width_ratio
        carbon_backbone_center_angle_dict_list = [
            {
                ParameterName.center: Vector(0.65, 0.15),
                ParameterName.angle: 30,
            },
            {
                ParameterName.center: Vector(0.4, 0.8),
                ParameterName.angle: 10,
            },
            {
                ParameterName.center: Vector(0.2, 0.5),
                ParameterName.angle: 23,
            },
            {
                ParameterName.center: Vector(0.31, 0.23),
                ParameterName.angle: -10,
            },
            {
                ParameterName.center: Vector(0.55, 0.61),
                ParameterName.angle: 41,
            },
        ]
        carbon_backbone_common_dict = {
            **CarbonBackboneConfig.single_carbon_backbone_config,
            ParameterName.carbon_num: carbon_num,
            ParameterName.face_color: (
                CarbonBackboneConfig.labeled_color if labeled else CarbonBackboneConfig.unlabeled_color),
            **kwargs
        }

        background_box = Rectangle(**{
            ParameterName.center: Vector(0.5, 0.5),
            ParameterName.width: total_width,
            ParameterName.height: total_height,
            ParameterName.face_color: ColorConfig.light_gray,
            ParameterName.z_order: 0
        })
        single_carbon_backbone_obj_dict = {
            f'single_backbone_{index}':
                SingleCarbonBackbone(**{
                    **carbon_backbone_common_dict,
                    **single_backbone_center_angle_dict,
                    ParameterName.name: f'single_backbone_{index}',
                }) for index, single_backbone_center_angle_dict in enumerate(carbon_backbone_center_angle_dict_list)
        }
        carbon_backbone_dict = {
            # ParameterName.background: {'background': background_box},
            'single_carbon_backbone': single_carbon_backbone_obj_dict,
        }
        super().__init__(
            carbon_backbone_dict, bottom_left=Vector(0, 0), size=Vector(total_width, total_height),
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)
