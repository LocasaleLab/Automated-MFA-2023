from .sensitivity_config import RunningMode, ExperimentName, model_data_config_dict, Keywords
from ..common.built_in_packages import argparse, mp


def arg_setting(computation_subparsers, sensitivity_enum):
    def sensitivity(args):
        main(model_data_sensitivity_parser, args)

    model_data_sensitivity_parser = computation_subparsers.add_parser(
        sensitivity_enum.value, help='Analyze protocol, model, data and config sensitivity of MFA',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Definition of experiment_name:\n\n{}'.format(
            '\n'.join([
                f'{enum_item.name:<60}{model_data_config_dict[enum_item][Keywords.comment]}'
                for enum_item in ExperimentName
            ])
        )
    )
    model_data_sensitivity_parser.add_argument(
        '-t', '--test_mode', action='store_true', default=False,
        help='Whether the code is executed in test mode, which means less sample number and shorter time.'
    )
    model_data_sensitivity_parser.add_argument(
        '-p', '--parallel_num', type=int, default=None,
        help='Number of parallel processes. If not provided, it will be selected according to CPU cores.'
    )
    running_mode_display = '{}'.format(',  '.join([running_mode.value for running_mode in RunningMode]))
    model_data_sensitivity_parser.add_argument(
        'running_mode', nargs='?', type=RunningMode, choices=list(RunningMode),
        help='Running mode of model data sensitivity analysis', default=None, metavar=running_mode_display)
    model_data_sensitivity_parser.add_argument(
        'experiment_name', nargs='?', type=ExperimentName, choices=list(ExperimentName),
        help='Experiments that need to run. Detailed list is attached below', default=None, metavar='experiment_name')
    model_data_sensitivity_parser.set_defaults(func=sensitivity)


def main(model_data_sensitivity_parser, args):
    running_mode = args.running_mode
    if running_mode is None:
        model_data_sensitivity_parser.print_help()
    else:
        from .common_functions import model_data_sensitivity
        mp.set_start_method('spawn')
        model_data_sensitivity(running_mode, args.experiment_name, args.test_mode, args.parallel_num)
