from .inventory import DataModelType, RunningMode, data_model_comment
from ..common.built_in_packages import argparse, mp


def arg_setting(computation_subparsers, experiments_enum):
    def experiments(args):
        main(experimental_data_analysis_parser, args)

    experimental_data_analysis_parser = computation_subparsers.add_parser(
        experiments_enum.value, help='Run MFA for several experimental data analyses',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Definition of data_model_name:\n\n{}'.format(
            '\n'.join([
                f'{enum_item.name:<50}{data_model_comment[enum_item]}'
                for enum_item in DataModelType
            ])
        )
    )
    experimental_data_analysis_parser.add_argument(
        '-t', '--test_mode', action='store_true', default=False,
        help='Whether the code is executed in test mode, which means less sample number and shorter time.'
    )
    experimental_data_analysis_parser.add_argument(
        '-p', '--parallel_num', type=int, default=None,
        help='Number of parallel processes. If not provided, it will be selected according to CPU cores.'
    )
    running_mode_display = '{}'.format(',  '.join([running_mode.value for running_mode in RunningMode]))
    experimental_data_analysis_parser.add_argument(
        'running_mode', nargs='?', type=RunningMode, choices=list(RunningMode),
        help='Running mode of experimental data analysis', default=None, metavar=running_mode_display)
    experimental_data_analysis_parser.add_argument(
        'data_model', nargs='?', type=DataModelType, choices=list(DataModelType),
        help='The data-model combination that need to calculate. Detailed list is attached below',
        default=None, metavar='data_model_name')
    experimental_data_analysis_parser.set_defaults(func=experiments)


def main(experimental_data_analysis_parser, args):
    running_mode = args.running_mode
    if running_mode is None:
        experimental_data_analysis_parser.print_help()
    else:
        from .common_functions import data_analysis_main
        mp.set_start_method('spawn')
        data_analysis_main(running_mode, args.data_model, args.test_mode, args.parallel_num)
