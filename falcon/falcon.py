#!/usr/bin/env python3

"""Python middleware for evaluating programming quizzes."""

import os
import sys
import argparse
from falcon.environment import Environment
from falcon.flyer import Flyer
from falcon.util import *

PARSER = None

def main(args=None):
    """
    The main event.
    """
    exit_code = 1
    falconf = None
    local_falconf = None
    env = Environment()

    # if args is not None:
    args = parse_args(args)

    if exists(dictionary=args, key='config') and args.config is not None:
        falconf = args.config
        try:
            os.chdir(os.path.dirname(falconf))
        except:
            # TODO: something about a bad config file
            PARSER.print_help()
    else:
        falconf = env.find_local_falconf()

    if falconf is not None:
        env.parse_falconf(falconf)
        flyer = Flyer(mode=args.mode, debug=args.debug, env=env)
        flyer.create_sequence()
        flyer.run_sequence()
        # TODO: write output somewhere
        exit_code = 0
    else:
        PARSER.print_help()
        exit_code = 1

    return exit_code

def parse_args(args):
    PARSER = argparse.ArgumentParser(description='middleware for evaluating programming quizzes')
    PARSER.add_argument('-c', '--config',
                        type=argparse.FileType('r', errors='ignore'),
                        action='store',
                        dest='config',
                        required=False,
                        help='Path to falconf.yaml.')
    PARSER.add_argument('-m', '--mode',
                        action='store',
                        default='submit',
                        dest='mode',
                        required=False,
                        help='The evaluation mode ("test" or "submit"). Defaults to "submit".')
    PARSER.add_argument('-p', '--pretty',
                        action='store_true',
                        required=False,
                        dest='show_pretty_submit',
                        help='show formatted submit output')
    PARSER.add_argument('-d', '--debug',
                        action='store_true',
                        default=False,
                        dest='debug',
                        required=False,
                        help='Print output from each step.')
    # PARSER.add_argument(['-i', '--init'],
    #                     required=False,
    #                     help='Helper to create a new falconf.yaml file.')

    args = PARSER.parse_args(args)
    return args

if __name__ == '__main__':
    main(sys.argv[1:])
