from figures.figure_plotting.common.built_in_packages import FigureName


def arg_setting(subparsers):
    def figure_running(args):
        main(figure_parser, args)

    figure_parser = subparsers.add_parser('figure', help='Run figure generation functions')
    figure_name_display = '{}'.format(',  '.join([figure_name.value for figure_name in FigureName]))
    figure_parser.add_argument(
        # 'figure_name', nargs='?', type=FigureName, choices=list(FigureName),
        'figure_name', nargs='?', type=str,
        help='The figure needs to plot', metavar=figure_name_display)
    figure_parser.add_argument(
        '-t', '--test_mode', action='store_true', default=False,
        help='Whether the code is executed in test mode, which means less sample number and shorter time.'
    )
    figure_parser.set_defaults(func=figure_running)


def main(figure_parser=None, args=None):
    figure_name = args.figure_name
    if figure_name is None:
        figure_parser.print_help()
    else:
        from figures.figure_plotting.main import figure_plotting_main
        figure_plotting_main(figure_name)


if __name__ == '__main__':
    main()

