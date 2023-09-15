

def arg_setting(computation_subparsers, standard_name_enum):
    def standard_name(args):
        main(standard_name_parser, args)

    standard_name_parser = computation_subparsers.add_parser(
        standard_name_enum.value, help='Output standard name of metabolites and reactions')
    standard_name_parser.set_defaults(func=standard_name)


def main(standard_name_parser, args):
    from .common_functions import standard_name_output
    standard_name_output()
