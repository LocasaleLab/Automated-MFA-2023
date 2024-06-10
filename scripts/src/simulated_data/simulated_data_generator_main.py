

def arg_setting(computation_subparsers, simulation_enum):
    def simulation(args):
        main(simulation_parser, args)

    simulation_parser = computation_subparsers.add_parser(
        simulation_enum.value, help='Generate simulated MID data')
    simulation_parser.add_argument(
        '-f', '--new_flux', action='store_true', default=False,
        help='Generate new flux optimized from PHDGH mass spectrometry data'
    )
    simulation_parser.add_argument(
        '-n', '--with_noise', action='store_true', default=False,
        help='Add noise to generated MID data to mimic real case.'
    )
    simulation_parser.add_argument(
        '--with_glns_m', action='store_true', default=False,
        help='Add GLNS_m flux to final model.'
    )
    simulation_parser.add_argument(
        '-i', '--index', type=int, default=None,
        help='Index to distinguish different simulated data.'
    )
    simulation_parser.add_argument(
        '-b', '--batch_num', type=int, default=1,
        help='Number to generate batched simulated solutions.'
    )
    simulation_parser.set_defaults(func=simulation)


def main(simulation_parser, args):
    from .common_functions import simulated_mid_data_generator
    simulated_mid_data_generator(args.new_flux, args.batch_num, args.index, args.with_noise, args.with_glns_m)
