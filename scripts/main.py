from scripts.src.common.built_in_packages import ValueEnum


class ComputationFunction(ValueEnum):
    simulation = 'simulation'
    sensitivity = 'sensitivity'
    experiments = 'experiments'
    standard_name = 'standard_name'


def arg_setting(subparsers):
    def print_computation_help(args):
        computation_parser.print_help()

    computation_parser = subparsers.add_parser('computation', help='Run computation functions')

    computation_subparsers = computation_parser.add_subparsers(
        title='Commands',
        description='Different content for computation',
        help='Decide to run different analysis functions')

    from scripts.src.simulated_data.simulated_data_generator_main import arg_setting as simulation_arg_setting
    simulation_arg_setting(computation_subparsers, ComputationFunction.simulation)

    from scripts.src.experimental_data_analysis.experimental_data_analysis_main import arg_setting as \
        experiments_arg_setting
    experiments_arg_setting(computation_subparsers, ComputationFunction.experiments)

    from scripts.src.model_data_sensitivity.model_data_sensitivity_main import arg_setting as \
        model_data_sensitivity_arg_setting
    model_data_sensitivity_arg_setting(computation_subparsers, ComputationFunction.sensitivity)

    from scripts.src.standard_name_output.standard_name_output_main import arg_setting as \
        standard_name_output_arg_setting
    standard_name_output_arg_setting(computation_subparsers, ComputationFunction.standard_name)

    computation_parser.set_defaults(func=print_computation_help)
