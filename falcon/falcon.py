#!/usr/bin/env python3

"""Python middleware for evaluating programming quizzes."""

import os
import sys
import argparse
from falcon.environment import Environment
from falcon.flyer import Flyer
from falcon.util import *

PARSER = None

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
                        dest='show_pretty_submit',
                        required=False,
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

def is_valid_falconf_specified(args=None):
    """
    Is there a valid falconf to be found? Uses the args and local directory to find out.

    Args:
        args (dict): From argparse.
    """
    return (exists(dictionary=args, key='config') and
            args['config'] is not None and
            file_exists(args['config']))

def fly(args, falconf, env):
    """
    Take off! Build the sequence and execute it.

    Args:
        args (dict): From argparse.
        falconf (string): falconf.yaml contents.
        env (Environment)

    Returns:
        Flyer
    """
    env.parse_falconf(falconf)
    flyer = Flyer(mode=args.mode, debug=args.debug, env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    return flyer

def main(args=None):
    """
    The main event.

    Args:
        args (dict): From argparse.

    Returns:
        int: Exit code.
    """
    exit_code = 1
    falconf = None
    local_falconf = None
    env = Environment()

    args = parse_args(args)

    # find a falconf file
    if is_valid_falconf_specified(args):
        falconf = args.config
        os.chdir(os.path.dirname(falconf))
    elif file_exists('falconf.yaml'):
        falconf = env.get_local_falconf()

    # run student code
    if falconf is not None:
        flyer = fly(args, falconf, env)
        # formatter(flyer)
        exit_code = 0

    # something is with the config or the config is missing
    else:
        PARSER.print_help()
        exit_code = 1

    return exit_code

if __name__ == '__main__':
    main(sys.argv[1:])
