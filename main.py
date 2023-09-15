import argparse

from scripts.main import arg_setting as computation_arg_setting
from figures.main import arg_setting as figure_arg_setting


def main():
    parser = argparse.ArgumentParser(
        prog='MFA_development', description='Code for development of MFA by Shiyu Liu.')
    subparsers = parser.add_subparsers(
        title='Commands',
        description='Different command for this code',
        help='Decide to run analysis or to generate figures based on analysis')
    computation_arg_setting(subparsers)
    figure_arg_setting(subparsers)

    args = parser.parse_args()
    try:
        current_func = args.func
    except AttributeError:
        parser.print_help()
    else:
        args.func(args)


if __name__ == '__main__':
    main()
