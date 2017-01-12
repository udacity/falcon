#!/usr/bin/env python3

"""Python middleware for evaluating programming quizzes."""

import argparse
import os
import sys
import time
from udfalcon.environment import Environment
from udfalcon.flyer import Flyer
from udfalcon.formatter import Formatter
from udfalcon.util import *

CURRENT_MILLI_TIME = lambda: int(round(time.time() * 1000))
PARSER = None
ELAPSED_TIME = 0

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
    PARSER.add_argument('-l', '--link',
                        action='store',
                        default=False,
                        dest='link',
                        required=False,
                        help='Symlink a falcon library here for testing.')
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
    start_time = CURRENT_MILLI_TIME()
    env.parse_falconf(falconf)
    flyer = Flyer(mode=args.mode, debug=args.debug, env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    end_time = CURRENT_MILLI_TIME()
    ELAPSED_TIME = end_time - start_time
    return flyer

def format_results(flyer, debug):
    formatter = Formatter(flyer, elapsed_time=ELAPSED_TIME)
    formatter.parse_steps(flyer)
    if debug:
        formatter.pipe_debug_to_stdout(flyer)
    else:
        formatter.pipe_to_stdout(flyer)

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

    # symlink and then shortcircuit if they used --link
    if args.link:
        flyer = Flyer()
        if flyer.symlink_libraries(args.link):
            return 0
        else:
            return 1

    # find a falconf file
    if is_valid_falconf_specified(args):
        falconf = args.config
        os.chdir(os.path.dirname(falconf))
    elif file_exists('falconf.yaml'):
        falconf = env.get_local_falconf()

    # run student code
    if falconf is not None:
        flyer = fly(args, falconf, env)
        format_results(flyer, args.debug)
        exit_code = 0

    # something is with the config or the config is missing
    else:
        PARSER.print_help()
        exit_code = 1

    return exit_code

if __name__ == '__main__':
    main(sys.argv[1:])
