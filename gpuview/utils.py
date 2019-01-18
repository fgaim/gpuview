"""
Utility functions for gpuview.

@author Fitsum Gaim
@url https://github.com/fgaim
"""

import argparse

from gpustat import __version__ as __gpustat__
from . import __version__


class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print("Subparser '{}'".format(choice))
                print(subparser.format_help())
        parser.exit()


def arg_parser():
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(dest='action', help="Action")
    parser.add_argument('-v', '--version', action='version',
                        help='Print gpuview and gpustat versions',
                        version='gpuview %s || gpustat %s' %
                        (__version__, __gpustat__))
    parser.add_argument('-h', '--help', action=_HelpAction,
                        help='Print this help message')

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument('--host', default='0.0.0.0',
                             help="IP address of host (default: 0.0.0.0)")
    base_parser.add_argument('--port', default=9988,
                             help="Port number of host (default: 9988)")
    base_parser.add_argument('--safe-zone', action='store_true',
                             help="Report all details including usernames")
    base_parser.add_argument('--exclude-self', action='store_true',
                             help="Don't report to others but self-dashboard")

    run_parser = subparsers.add_parser("run", parents=[base_parser],
                                       help="Run gpuview server")
    run_parser.add_argument('-d', '--debug', action='store_true',
                            help="Run server in debug mode")

    add_parser = subparsers.add_parser("add", help="Register a new GPU host")
    add_parser.add_argument('--url', required=True,
                            help="URL of GPU host (IP:Port, eg. X.X.X.X:9988")
    add_parser.add_argument('--name', default=None,
                            help="An optional readable name for the GPU host")

    rem_parser = subparsers.add_parser("remove", help="Remove a GPU host")
    rem_parser.add_argument('--url', required=True,
                            help="Url of the GPU node to remove")

    subparsers.add_parser("hosts", help="Print all GPU hosts")

    subparsers.add_parser("service", parents=[base_parser],
                          help="Install gpuview as a service")

    return parser
