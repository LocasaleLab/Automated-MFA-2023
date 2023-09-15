from ..config import Vector, ParameterName, ColorConfig, ZOrderConfig
from ..config import CompositeFigure, PathStep, PathOperation, PathShape, Rectangle


class MiceConfig(object):
    common_z_order = ZOrderConfig.default_patch_z_order
    z_order_increment = ZOrderConfig.z_order_increment
    ear2_z_order = common_z_order + z_order_increment

    infusion_color = ColorConfig.slightly_light_orange
    common_edge_width = 9.5
    infusion_rect_edge_width = common_edge_width - 1

    mice_config = {
        ParameterName.edge_width: common_edge_width,
        ParameterName.edge_color: ColorConfig.black_color,
        ParameterName.face_color: None,
        ParameterName.z_order: common_z_order
    }
    infusion_inner_color_config = {
        ParameterName.edge_width: None,
        ParameterName.face_color: infusion_color,
        ParameterName.z_order: common_z_order - z_order_increment
    }
    infusion_bottom_small_rect_config = {
        ParameterName.edge_width: infusion_rect_edge_width,
        ParameterName.edge_color: ColorConfig.black_color,
        ParameterName.face_color: infusion_color,
        ParameterName.z_order: common_z_order
    }


class Mice(CompositeFigure):
    total_width = 1
    height_to_width_ratio = 0.9761904761904762

    def __init__(
            self, infusion=True, scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        total_width = self.total_width
        total_height = total_width * self.height_to_width_ratio
        mouse_path_param_dict_dict = {
            'body': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.9661285714285714, 0.2188833333333333)),
                PathStep(PathOperation.curve4, Vector(0.9439190476190477, 0.16858333333333336),
                         Vector(0.23670095238095237, 0.10215476190476185),
                         Vector(0.1503404761904762, 0.24164761904761908)),
                PathStep(PathOperation.curve4, Vector(0.12934, 0.5010333333333333),
                         Vector(0.3604047619047619, 0.5183642857142857),
                         Vector(0.3604047619047619, 0.5183642857142857)),
                PathStep(PathOperation.curve4, Vector(0.5011214285714286, 0.5415404761904762),
                         Vector(0.8153404761904761, 0.3231666666666667),
                         Vector(0.9661285714285714, 0.2188833333333333)),
                PathStep(PathOperation.closepoly),

            ]},

            'ear1': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.7441428571428572, 0.43995)),
                PathStep(PathOperation.curve4, Vector(0.7433380952380952, 0.4163928571428571),
                         Vector(0.7229976190476191, 0.39798809523809525),
                         Vector(0.6987071428571429, 0.3988404761904762)),
                PathStep(PathOperation.curve4, Vector(0.6744190476190476, 0.3996928571428572),
                         Vector(0.6553809523809524, 0.4194833333333333),
                         Vector(0.6561857142857144, 0.4430404761904762)),
                PathStep(PathOperation.curve4, Vector(0.6569904761904761, 0.46659761904761904),
                         Vector(0.6773333333333333, 0.4850047619047619),
                         Vector(0.7016214285714285, 0.48414999999999997)),
                PathStep(PathOperation.curve4, Vector(0.7259119047619047, 0.4832976190476191),
                         Vector(0.744947619047619, 0.4635095238095238), Vector(0.7441428571428572, 0.43995)),
                PathStep(PathOperation.closepoly),

            ]},

            'ear2': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.7941428571428572, 0.4113785714285714)),
                PathStep(PathOperation.curve4, Vector(0.7933380952380953, 0.38782142857142854),
                         Vector(0.7729952380952382, 0.36941666666666667),
                         Vector(0.7487071428571428, 0.3702690476190476)),
                PathStep(PathOperation.curve4, Vector(0.7244190476190475, 0.3711214285714286),
                         Vector(0.7053809523809523, 0.39091190476190474),
                         Vector(0.7061857142857143, 0.4144690476190476)),
                PathStep(PathOperation.curve4, Vector(0.7069904761904762, 0.43802619047619046),
                         Vector(0.7273333333333334, 0.4564333333333333),
                         Vector(0.7516214285714286, 0.4555785714285714)),
                PathStep(PathOperation.curve4, Vector(0.7759119047619047, 0.4547261904761905),
                         Vector(0.794947619047619, 0.43493809523809523),
                         Vector(0.7941428571428572, 0.4113785714285714)),
                PathStep(PathOperation.closepoly),

            ]},

            'eye1': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.7656380952380952, 0.2984785714285714)),
                PathStep(PathOperation.curve4, Vector(0.7655500000000001, 0.29585),
                         Vector(0.7633428571428571, 0.2937952380952381),
                         Vector(0.7607142857142857, 0.2938857142857143)),
                PathStep(PathOperation.curve4, Vector(0.7580857142857144, 0.29397619047619056),
                         Vector(0.7560309523809524, 0.2961833333333333),
                         Vector(0.7561214285714286, 0.2988095238095238)),
                PathStep(PathOperation.curve4, Vector(0.7562119047619047, 0.3014380952380952),
                         Vector(0.7584166666666667, 0.30349523809523815),
                         Vector(0.7610428571428571, 0.30340238095238087)),
                PathStep(PathOperation.curve4, Vector(0.7636738095238095, 0.3033142857142857),
                         Vector(0.7657309523809525, 0.3011071428571428),
                         Vector(0.7656380952380952, 0.2984785714285714)),
                PathStep(PathOperation.lineto, Vector(0.7656380952380952, 0.2984785714285714)),
                PathStep(PathOperation.closepoly),

            ]},

            'eye2': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.7588738095238095, 0.3020095238095238)),
                PathStep(PathOperation.curve4, Vector(0.7588738095238095, 0.29994523809523804),
                         Vector(0.7572, 0.29826904761904766), Vector(0.7551333333333333, 0.29826904761904766)),
                PathStep(PathOperation.curve4, Vector(0.7530666666666667, 0.29826904761904766),
                         Vector(0.7513904761904762, 0.29994523809523804),
                         Vector(0.7513904761904762, 0.3020095238095238)),
                PathStep(PathOperation.curve4, Vector(0.7513904761904762, 0.30407619047619044),
                         Vector(0.7530666666666667, 0.30575238095238094),
                         Vector(0.7551333333333333, 0.30575238095238094)),
                PathStep(PathOperation.curve4, Vector(0.7572, 0.30575238095238094),
                         Vector(0.7588738095238095, 0.30407619047619044),
                         Vector(0.7588738095238095, 0.3020095238095238)),
                PathStep(PathOperation.lineto, Vector(0.7588738095238095, 0.3020095238095238)),
                PathStep(PathOperation.closepoly),

            ]},

            'tail': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.1539354761904762, 0.24192619047619043)),
                PathStep(PathOperation.curve4, Vector(-0.12735619047619048, 0.11143333333333338),
                         Vector(0.3876928571428571, 0.062054761904761876),
                         Vector(0.39540714285714285, 0.060126190476190444)),
            ]},

            'beard': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.9109666666666667, 0.22592380952380947)),
                PathStep(PathOperation.curve4, Vector(0.8929380952380952, 0.1900642857142857),
                         Vector(0.8628214285714285, 0.16014999999999993),
                         Vector(0.8288214285714286, 0.13214285714285715)),
                PathStep(PathOperation.moveto, Vector(0.9089619047619047, 0.2251071428571429)),
                PathStep(PathOperation.curve4, Vector(0.8718666666666667, 0.231697619047619),
                         Vector(0.8070666666666667, 0.2383404761904762),
                         Vector(0.7333619047619048, 0.24499999999999994)),
                PathStep(PathOperation.moveto, Vector(0.9102142857142858, 0.22624523809523817)),
                PathStep(PathOperation.curve4, Vector(0.8740095238095238, 0.21295714285714287),
                         Vector(0.8114595238095238, 0.20266190476190474),
                         Vector(0.7404404761904763, 0.19332857142857138)),
                PathStep(PathOperation.moveto, Vector(0.9076809523809524, 0.22307380952380945)),
                PathStep(PathOperation.curve4, Vector(0.8785095238095237, 0.19674999999999998),
                         Vector(0.8286595238095238, 0.17521904761904758),
                         Vector(0.7721642857142857, 0.1552285714285715)),
            ]},
        }

        infusion_large_rect_width = 0.15714285714285714285714285714286
        infusion_large_rect_height = 0.30952380952380952380952380952381
        inner_color_ratio = 0.60769230769230769230769230769231
        small_rect_width_ratio = 0.666666
        small_rect_height_ratio = 0.14615384615384615384615384615385
        infusion_large_rect_center = Vector(
            infusion_large_rect_width / 2,
            self.height_to_width_ratio - infusion_large_rect_height / 2)
        infusion_inner_color_rect_height = infusion_large_rect_height * 0.6
        infusion_inner_color_rect_center = Vector(
            infusion_large_rect_center.x,
            infusion_large_rect_center.y - (1 - inner_color_ratio) / 2 * infusion_large_rect_height)
        infusion_small_rect_width = small_rect_width_ratio * infusion_large_rect_width
        infusion_small_rect_height = small_rect_height_ratio * infusion_large_rect_height
        infusion_small_rect_center = Vector(
            infusion_large_rect_center.x,
            infusion_large_rect_center.y - infusion_large_rect_height / 2 - infusion_small_rect_height / 2
        )

        infusion_obj_list = [
            Rectangle(**{
                ParameterName.center: infusion_large_rect_center,
                ParameterName.width: infusion_large_rect_width,
                ParameterName.height: infusion_large_rect_height,
                ParameterName.name: 'infusion_large_rect',
                **MiceConfig.mice_config,
                ParameterName.edge_width: MiceConfig.infusion_rect_edge_width
            }),
            Rectangle(**{
                ParameterName.center: infusion_inner_color_rect_center,
                ParameterName.width: infusion_large_rect_width,
                ParameterName.height: infusion_inner_color_rect_height,
                ParameterName.name: 'infusion_inner_color_rect',
                **MiceConfig.infusion_inner_color_config
            }),
            Rectangle(**{
                ParameterName.center: infusion_small_rect_center,
                ParameterName.width: infusion_small_rect_width,
                ParameterName.height: infusion_small_rect_height,
                ParameterName.name: 'infusion_small_rect',
                **MiceConfig.infusion_bottom_small_rect_config
            }),
            PathShape(
                [
                    PathStep(PathOperation.moveto, Vector(0.07976142857142857, 0.6202380952380953)),
                    PathStep(PathOperation.curve4, Vector(0.0797614285714286, 0.537295238095238),
                             Vector(0.15870380952380958, 0.45435214285714287),
                             Vector(0.23764571428571432, 0.45435214285714287)),
                    PathStep(PathOperation.curve4, Vector(0.3165880952380953, 0.45435214285714287),
                             Vector(0.3955304761904762, 0.37140952380952386),
                             Vector(0.3955304761904762, 0.2884666666666668)),
                ],
                **MiceConfig.mice_config
            )
        ]

        background_box = Rectangle(**{
            ParameterName.center: Vector(0.5, 0.5),
            ParameterName.width: total_width,
            ParameterName.height: total_height,
            ParameterName.face_color: ColorConfig.light_gray,
            ParameterName.z_order: 0
        })
        mouse_path_param_dict_dict['ear1'].update({
            ParameterName.face_color: ColorConfig.white_color,
            ParameterName.z_order: MiceConfig.ear2_z_order
        })
        eye_config_dict = {
            ParameterName.face_color: ColorConfig.black_color,
        }
        mouse_path_param_dict_dict['eye1'].update(eye_config_dict)
        mouse_path_param_dict_dict['eye2'].update(eye_config_dict)
        mouse_path_shape_obj_dict = {
            key:
            PathShape(**{
                **MiceConfig.mice_config,
                **mouse_path_param_dict,
                ParameterName.name: key,
            }) for key, mouse_path_param_dict in mouse_path_param_dict_dict.items()
        }
        mouse_dict = {
            # ParameterName.background: {'background': background_box},
            ParameterName.mouse: mouse_path_shape_obj_dict,
        }
        if infusion:
            mouse_dict[ParameterName.infusion] = {
                infusion_obj.name: infusion_obj for infusion_obj in infusion_obj_list
            }
        super().__init__(
            mouse_dict, bottom_left=Vector(0, 0), size=Vector(total_width, total_height),
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)

