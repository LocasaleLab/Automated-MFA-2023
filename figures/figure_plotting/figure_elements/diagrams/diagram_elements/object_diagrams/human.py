from ..config import Vector, ParameterName, ColorConfig, ZOrderConfig, common_text_config_dict, FontWeight
from ..config import CompositeFigure, PathStep, PathOperation, PathShape, Rectangle, TextBox


class HumanConfig(object):
    common_z_order = ZOrderConfig.default_patch_z_order
    z_order_increment = ZOrderConfig.z_order_increment

    infusion_color = ColorConfig.slightly_light_orange
    common_edge_width = 9.5
    infusion_rect_edge_width = common_edge_width - 1

    human_config = {
        ParameterName.edge_width: common_edge_width,
        ParameterName.edge_color: ColorConfig.black_color,
        ParameterName.face_color: None,
        ParameterName.z_order: common_z_order,
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
    text_label_config = {
        **common_text_config_dict,
        ParameterName.font_size: 45,
        ParameterName.width: 0.45,
        ParameterName.height: 0.1,
        ParameterName.font_weight: FontWeight.bold
        # ParameterName.text_box: True,
    }


class Human(CompositeFigure):
    total_width = 1
    height_to_width_ratio = 1

    def __init__(
            self, infusion=True, text_label=None,
            scale=1, bottom_left_offset=None, base_z_order=0, z_order_increment=1, **kwargs):
        human_path_param_dict_dict = {
            'human': {ParameterName.path_step_list: [
                PathStep(PathOperation.moveto, Vector(0.2687963917525773, 0.10522313195876265)),
                PathStep(PathOperation.curve4, Vector(0.2683925360824742, 0.16193120309278353),
                         Vector(0.2701524536082474, 0.18256062886597935),
                         Vector(0.27847088659793817, 0.21862518556701005)),
                PathStep(PathOperation.curve4, Vector(0.2832612680412371, 0.23939389690721624),
                         Vector(0.2883782989690722, 0.25509936082474205),
                         Vector(0.2922407010309278, 0.26088827835051553)),
                PathStep(PathOperation.curve4, Vector(0.2996252989690722, 0.27195614432989634),
                         Vector(0.30968705154639176, 0.27966782474226815),
                         Vector(0.3243125154639175, 0.28546930927835)),
                PathStep(PathOperation.curve4, Vector(0.3322610721649485, 0.2886222577319586),
                         Vector(0.3357644742268041, 0.2904065360824739),
                         Vector(0.3458762268041237, 0.29645182474226806)),
                PathStep(PathOperation.curve4, Vector(0.34899478350515467, 0.2983162474226799),
                         Vector(0.35610529896907217, 0.30153738144329845),
                         Vector(0.3616772577319588, 0.30360991752577293)),
                PathStep(PathOperation.curve4, Vector(0.3856209690721649, 0.3125158969072164),
                         Vector(0.4421793195876289, 0.3396933505154638),
                         Vector(0.45670096907216495, 0.3492707938144326)),
                PathStep(PathOperation.curve4, Vector(0.4666521030927835, 0.3558338453608245),
                         Vector(0.4730414845360824, 0.36213104123711304),
                         Vector(0.47534632989690717, 0.3676473195876291)),
                PathStep(PathOperation.curve4, Vector(0.47758261855670103, 0.3729996391752577),
                         Vector(0.47990169072164945, 0.38948674226804103),
                         Vector(0.4804277731958764, 0.4037742783505154)),
                PathStep(PathOperation.curve4, Vector(0.48088911340206186, 0.41630093814432945),
                         Vector(0.4807985979381444, 0.41703393814432976),
                         Vector(0.47797509278350514, 0.4236309690721649)),
                PathStep(PathOperation.curve4, Vector(0.47174004123711344, 0.4381992577319589),
                         Vector(0.46834725773195873, 0.45018847422680386),
                         Vector(0.4649995257731958, 0.4694824536082476)),
                PathStep(PathOperation.curve4, Vector(0.46328334020618556, 0.4793738762886597),
                         Vector(0.46288107216494845, 0.4804808659793811),
                         Vector(0.46100313402061854, 0.4804808659793811)),
                PathStep(PathOperation.curve4, Vector(0.4603177731958763, 0.4804808659793811),
                         Vector(0.4579698350515464, 0.4816952061855666),
                         Vector(0.4557857113402062, 0.4831793917525773)),
                PathStep(PathOperation.curve4, Vector(0.45050643298969073, 0.4867667216494844),
                         Vector(0.44493849484536085, 0.49875504123711334),
                         Vector(0.44134880412371136, 0.5142630721649484)),
                PathStep(PathOperation.curve4, Vector(0.4382675670103092, 0.5275747731958762),
                         Vector(0.43804447422680415, 0.5326574123711336),
                         Vector(0.4401816907216495, 0.5408624432989688)),
                PathStep(PathOperation.curve4, Vector(0.4417906597938145, 0.5470399896907212),
                         Vector(0.44286014432989695, 0.5488613608247421),
                         Vector(0.4467182886597938, 0.5519948453608245)),
                PathStep(PathOperation.curve4, Vector(0.44878065979381443, 0.5536698969072162),
                         Vector(0.44901055670103096, 0.5545151237113397),
                         Vector(0.44840261855670105, 0.558187154639175)),
                PathStep(PathOperation.curve4, Vector(0.44801550515463917, 0.5605260103092782),
                         Vector(0.44729035051546395, 0.5632177835051544),
                         Vector(0.44679127835051546, 0.5641688762886594)),
                PathStep(PathOperation.curve4, Vector(0.446292206185567, 0.5651199587628866),
                         Vector(0.44537962886597937, 0.5718467628865977),
                         Vector(0.4447633402061856, 0.5791173298969068)),
                PathStep(PathOperation.curve4, Vector(0.4441470515463918, 0.586387886597938),
                         Vector(0.4431499381443299, 0.593360206185567),
                         Vector(0.44254746391752575, 0.5946113505154638)),
                PathStep(PathOperation.curve4, Vector(0.44177096907216495, 0.5962238762886596),
                         Vector(0.4417868453608247, 0.599825618556701), Vector(0.4426021030927836, 0.6069824845360823)),
                PathStep(PathOperation.curve4, Vector(0.4433374639175257, 0.6134384639175257),
                         Vector(0.443391587628866, 0.6172027113402061), Vector(0.4427523092783505, 0.617422443298969)),
                PathStep(PathOperation.curve4, Vector(0.4414703505154639, 0.6178630721649485),
                         Vector(0.44144921649484536, 0.621408855670103), Vector(0.4427238556701031, 0.622196628865979)),
                PathStep(PathOperation.curve4, Vector(0.44325818556701035, 0.6225268144329892),
                         Vector(0.4439777731958763, 0.6249897628865977),
                         Vector(0.4443231340206186, 0.6276698453608245)),
                PathStep(PathOperation.curve4, Vector(0.44466839175257733, 0.6303499278350513),
                         Vector(0.44539107216494844, 0.6333482783505153),
                         Vector(0.44592911340206187, 0.6343328556701029)),
                PathStep(PathOperation.curve4, Vector(0.44646705154639177, 0.6353174329896909),
                         Vector(0.4469071546391753, 0.6373537525773196),
                         Vector(0.4469071546391753, 0.6388580103092782)),
                PathStep(PathOperation.curve4, Vector(0.4469071546391753, 0.6403622783505152),
                         Vector(0.44837808247422684, 0.6439639278350517),
                         Vector(0.45017591752577324, 0.6468616907216496)),
                PathStep(PathOperation.curve4, Vector(0.4519736494845361, 0.6497594536082474),
                         Vector(0.45493849484536086, 0.6547527835051548),
                         Vector(0.45676426804123704, 0.6579579793814432)),
                PathStep(PathOperation.curve4, Vector(0.45980622680412375, 0.6632979999999997),
                         Vector(0.46874529896907213, 0.6748625773195873),
                         Vector(0.47774292783505157, 0.6850982164948451)),
                PathStep(PathOperation.curve4, Vector(0.4821318969072165, 0.6900910618556697),
                         Vector(0.4909080824742268, 0.6968307010309278),
                         Vector(0.4940721030927835, 0.6976381958762885)),
                PathStep(PathOperation.curve4, Vector(0.49534787628865984, 0.6979637731958759),
                         Vector(0.49639169072164946, 0.6986641237113402),
                         Vector(0.49639169072164946, 0.699194525773196)),
                PathStep(PathOperation.curve4, Vector(0.49639169072164946, 0.6997249175257729),
                         Vector(0.49697158762886595, 0.7000510103092785),
                         Vector(0.4976803505154639, 0.6999191752577318)),
                PathStep(PathOperation.curve4, Vector(0.4983891134020618, 0.6997873402061856),
                         Vector(0.5004265360824742, 0.7000248041237107),
                         Vector(0.5022079793814433, 0.7004468659793814)),
                PathStep(PathOperation.curve4, Vector(0.5047027216494846, 0.7010379072164947),
                         Vector(0.5053312783505155, 0.701656917525773), Vector(0.504943237113402, 0.7031405567010305)),
                PathStep(PathOperation.curve4, Vector(0.5045199381443299, 0.7047595051546391),
                         Vector(0.5052340618556701, 0.7051860103092777),
                         Vector(0.5094191134020619, 0.7058135979381439)),
                PathStep(PathOperation.curve4, Vector(0.5121578762886598, 0.7062243092783507),
                         Vector(0.5159345773195877, 0.7072020618556696), Vector(0.5178116907216495, 0.707986391752577)),
                PathStep(PathOperation.curve4, Vector(0.5196889072164949, 0.7087707113402062),
                         Vector(0.5216885979381444, 0.7091257835051543),
                         Vector(0.5222554020618557, 0.7087754226804126)),
                PathStep(PathOperation.curve4, Vector(0.5228223092783505, 0.7084250721649483),
                         Vector(0.5239346804123711, 0.708676649484536), Vector(0.5247273608247423, 0.7093344948453604)),
                PathStep(PathOperation.curve4, Vector(0.5255200412371134, 0.7099923402061856),
                         Vector(0.5283991134020619, 0.7106003402061853),
                         Vector(0.5311255051546392, 0.7106856082474224)),
                PathStep(PathOperation.curve4, Vector(0.5338517938144329, 0.71077087628866),
                         Vector(0.5364129278350516, 0.7113155051546389),
                         Vector(0.5368168453608247, 0.7118958969072167)),
                PathStep(PathOperation.curve4, Vector(0.5373005567010309, 0.7125909587628865),
                         Vector(0.5392831340206186, 0.7123360206185567),
                         Vector(0.5426252989690722, 0.7111489999999998)),
                PathStep(PathOperation.curve4, Vector(0.5485904536082474, 0.7090303711340207),
                         Vector(0.5517267422680412, 0.70885706185567), Vector(0.5523123092783505, 0.7106136907216496)),
                PathStep(PathOperation.curve4, Vector(0.5526261237113402, 0.7115552577319586),
                         Vector(0.5533916907216495, 0.7114499484536081), Vector(0.5552939587628866, 0.710203525773196)),
                PathStep(PathOperation.curve4, Vector(0.557712412371134, 0.7086189072164948),
                         Vector(0.5616597319587628, 0.7085954948453606), Vector(0.565463855670103, 0.7101432268041235)),
                PathStep(PathOperation.curve4, Vector(0.5663143711340206, 0.7104892577319584),
                         Vector(0.568402, 0.7108861030927831), Vector(0.570103030927835, 0.711025103092783)),
                PathStep(PathOperation.curve4, Vector(0.5718040618556701, 0.7111641030927829),
                         Vector(0.5747694226804124, 0.7116015567010305), Vector(0.576692824742268, 0.7119972268041237)),
                PathStep(PathOperation.curve4, Vector(0.5790945773195877, 0.7124913298969071),
                         Vector(0.5799737525773196, 0.7123671855670102),
                         Vector(0.5795001443298969, 0.7116008453608247)),
                PathStep(PathOperation.curve4, Vector(0.5790343711340207, 0.7108472783505153),
                         Vector(0.580792206185567, 0.7104945257731958), Vector(0.5849147835051547, 0.7105142474226804)),
                PathStep(PathOperation.curve4, Vector(0.5914577731958763, 0.7105455463917525),
                         Vector(0.5954196288659793, 0.7089869690721651),
                         Vector(0.5991983917525774, 0.7048951958762886)),
                PathStep(PathOperation.curve4, Vector(0.6004584948453608, 0.7035306494845357),
                         Vector(0.6035858144329896, 0.7018272886597936), Vector(0.6061479793814433, 0.70110993814433)),
                PathStep(PathOperation.curve4, Vector(0.6087100412371134, 0.7003925876288659),
                         Vector(0.6118542680412371, 0.6987662474226806),
                         Vector(0.6131350927835051, 0.6974958350515461)),
                PathStep(PathOperation.curve4, Vector(0.6144159175257732, 0.6962254329896904),
                         Vector(0.6177834432989691, 0.6939985360824736), Vector(0.6206184948453608, 0.69254718556701)),
                PathStep(PathOperation.curve4, Vector(0.6291772577319587, 0.6881656701030927),
                         Vector(0.6370877731958763, 0.6797737113402063),
                         Vector(0.6523998350515464, 0.6588313814432989)),
                PathStep(PathOperation.curve4, Vector(0.6542654020618556, 0.6562798350515462),
                         Vector(0.6563855051546391, 0.6525684948453603),
                         Vector(0.6571111752577319, 0.6505839587628865)),
                PathStep(PathOperation.curve4, Vector(0.6578367422680412, 0.6485994226804119),
                         Vector(0.6591087010309278, 0.6457043917525769),
                         Vector(0.6599377731958762, 0.6441505567010308)),
                PathStep(PathOperation.curve4, Vector(0.6620079793814433, 0.6402702989690723),
                         Vector(0.6636391134020619, 0.6311411443298964),
                         Vector(0.6641299381443299, 0.6206870515463918)),
                PathStep(PathOperation.curve4, Vector(0.6646237525773195, 0.6101704329896904),
                         Vector(0.6646554020618556, 0.6115199175257731),
                         Vector(0.6634645773195876, 0.5923365360824739)),
                PathStep(PathOperation.curve4, Vector(0.662253030927835, 0.5728204742268037),
                         Vector(0.6608193195876289, 0.5620908144329895),
                         Vector(0.6585812783505155, 0.5557894020618552)),
                PathStep(PathOperation.lineto, Vector(0.6568216907216494, 0.5508352268041237)),
                PathStep(PathOperation.lineto, Vector(0.6595695257731958, 0.5475696185567007)),
                PathStep(PathOperation.curve4, Vector(0.6625284948453608, 0.5440531237113402),
                         Vector(0.6664947835051547, 0.532692391752577), Vector(0.6664947835051547, 0.5277335773195873)),
                PathStep(PathOperation.curve4, Vector(0.6664947835051547, 0.5224851237113399),
                         Vector(0.6614675670103093, 0.5019947938144327),
                         Vector(0.6579794226804123, 0.4930262474226801)),
                PathStep(PathOperation.curve4, Vector(0.6558833402061855, 0.48763661855670115),
                         Vector(0.6533271546391752, 0.48312473195876304),
                         Vector(0.6511167422680413, 0.48091284536082446)),
                PathStep(PathOperation.curve4, Vector(0.6475843711340206, 0.4773779690721649),
                         Vector(0.6469304536082474, 0.4771151546391752),
                         Vector(0.6412766391752577, 0.4769576597938139)),
                PathStep(PathOperation.lineto, Vector(0.6382234432989691, 0.4768726185567007)),
                PathStep(PathOperation.lineto, Vector(0.6352875670103092, 0.4624396288659791)),
                PathStep(PathOperation.curve4, Vector(0.6309670515463918, 0.4411994123711338),
                         Vector(0.630713237113402, 0.4400428041237112), Vector(0.629632618556701, 0.43666643298969054)),
                PathStep(PathOperation.curve4, Vector(0.6286587010309278, 0.4336231030927835),
                         Vector(0.6287700412371133, 0.4196598969072163),
                         Vector(0.6298940618556701, 0.4038998969072165)),
                PathStep(PathOperation.curve4, Vector(0.6307572577319587, 0.39179673195876275),
                         Vector(0.6340866391752576, 0.37678969072164925),
                         Vector(0.6370184948453609, 0.3717868350515463)),
                PathStep(PathOperation.curve4, Vector(0.6406998350515464, 0.3655051855670104),
                         Vector(0.6492884948453608, 0.3580263505154635),
                         Vector(0.6588255051546391, 0.35279773195876274)),
                PathStep(PathOperation.curve4, Vector(0.6987633402061856, 0.33090206185566995),
                         Vector(0.7366391134020618, 0.3122954020618556),
                         Vector(0.7597937525773196, 0.30319651546391757)),
                PathStep(PathOperation.curve4, Vector(0.7781711752577319, 0.2959748969072167),
                         Vector(0.7813672577319587, 0.2943718762886598),
                         Vector(0.7943298350515464, 0.28587427835051527)),
                PathStep(PathOperation.curve4, Vector(0.809242, 0.27609864948453566),
                         Vector(0.8209752989690722, 0.2663982577319586),
                         Vector(0.825742412371134, 0.25990423711340194)),
                PathStep(PathOperation.curve4, Vector(0.8348533402061855, 0.24749264948453575),
                         Vector(0.8414830309278349, 0.22559872164948436),
                         Vector(0.8469831340206185, 0.18975920618556685)),
                PathStep(PathOperation.curve4, Vector(0.8491114845360824, 0.1758907731958761),
                         Vector(0.8492952989690721, 0.1707886185567009),
                         Vector(0.8495269484536083, 0.11914065773195848)),
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
        infusion_small_rect_bottom = infusion_small_rect_center + Vector(0, -infusion_small_rect_height / 2)

        infusion_obj_list = [
            Rectangle(**{
                ParameterName.center: infusion_large_rect_center,
                ParameterName.width: infusion_large_rect_width,
                ParameterName.height: infusion_large_rect_height,
                ParameterName.name: 'infusion_large_rect',
                **HumanConfig.human_config,
                ParameterName.edge_width: HumanConfig.infusion_rect_edge_width
            }),
            Rectangle(**{
                ParameterName.center: infusion_inner_color_rect_center,
                ParameterName.width: infusion_large_rect_width,
                ParameterName.height: infusion_inner_color_rect_height,
                ParameterName.name: 'infusion_inner_color_rect',
                **HumanConfig.infusion_inner_color_config
            }),
            Rectangle(**{
                ParameterName.center: infusion_small_rect_center,
                ParameterName.width: infusion_small_rect_width,
                ParameterName.height: infusion_small_rect_height,
                ParameterName.name: 'infusion_small_rect',
                **HumanConfig.infusion_bottom_small_rect_config
            }),
            PathShape(
                [
                    # PathStep(PathOperation.moveto, Vector(0.07976142857142857, 0.6202380952380953)),
                    PathStep(PathOperation.moveto, infusion_small_rect_bottom),
                    PathStep(PathOperation.curve4, Vector(0.0797614285714286, 0.537295238095238),
                             Vector(0.15870380952380958, 0.45435214285714287),
                             Vector(0.23764571428571432, 0.45435214285714287)),
                    PathStep(PathOperation.curve4, Vector(0.3165880952380953, 0.45435214285714287),
                             Vector(0.3955304761904762, 0.37140952380952386),
                             # Vector(0.3955304761904762, 0.2884666666666668)),
                             Vector(0.3955304761904762, 0.23)),
                ],
                **HumanConfig.human_config
            )
        ]
        human_path_shape_obj_dict = {
            key:
            PathShape(**{
                **HumanConfig.human_config,
                **human_path_param_dict,
                ParameterName.name: key,
                ParameterName.closed: False,
            }) for key, human_path_param_dict in human_path_param_dict_dict.items()
        }
        human_dict = {
            ParameterName.human: human_path_shape_obj_dict,
        }
        if infusion:
            human_dict[ParameterName.infusion] = {
                infusion_obj.name: infusion_obj for infusion_obj in infusion_obj_list
            }
        if text_label is not None:
            text_obj = TextBox(**{
                **HumanConfig.text_label_config,
                ParameterName.string: text_label,
                ParameterName.center: Vector(0.57, 0.15)
            })
            human_dict[ParameterName.text] = {text_obj.name: text_obj}

        super().__init__(
            human_dict, bottom_left=Vector(0, 0),
            size=Vector(self.total_width, self.total_width * self.height_to_width_ratio),
            scale=scale, bottom_left_offset=bottom_left_offset, base_z_order=base_z_order,
            z_order_increment=z_order_increment)

