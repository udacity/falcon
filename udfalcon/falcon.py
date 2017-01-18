"""Python middleware for evaluating programming quizzes."""

# import argparse
import os
import sys
import time
from udfalcon.environment import Environment
from udfalcon.flyer import Flyer
from udfalcon.formatter import Formatter
from udfalcon.util import *

CURRENT_MILLI_TIME = lambda: int(round(time.time() * 1000))
ELAPSED_TIME = 0

def is_valid_falconf_specified(args=None):
    """
    Is there a valid falconf to be found? Uses the args and local directory to find out.

    Args:
        args (dict): From argparse.
    """
    in_config = False
    does_exist = False

    in_config = exists(dictionary=args, key='config') and args['config'] is not None

    if in_config:
        try:
            does_exist = file_exists(args['config'])
        except KeyError as e:
            if args['debug']:
                eprint('Invalid config file: {}'.format(args['config']))

    return in_config and does_exist

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
    flyer = Flyer(mode=args['mode'], debug=args['debug'], env=env)
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

def main(args={}):
    """
    The main event.

    Args:
        args (dict)

    Returns:
        int: Exit code.
    """
    exit_code = 1
    falconf = None
    local_falconf = None
    env = Environment()

    if not exists(dictionary=args, key='mode'):
        args['mode'] = 'test'

    if not exists(dictionary=args, key='debug'):
        args['debug'] = False

    # symlink and then shortcircuit if they used --link
    if exists(dictionary=args, key='link') and args['link']:
        flyer = Flyer()
        if flyer.symlink_libraries(args['link']):
            return 0
        else:
            return 1

    # find a falconf file
    if is_valid_falconf_specified(args):
        with open(args['config'], 'r') as f:
            falconf = f.read()

        # change the path if the falconf is elsewhere
        newpath = os.path.dirname(falconf)
        if newpath != '':
            os.chdir(newpath)

    elif file_exists('falconf.yaml') or file_exists('falconf.yml'):
        if args['debug']:
            eprint('Using local falconf file.')
        falconf = env.get_local_falconf()

    # run student code
    if falconf is not None:
        flyer = fly(args, falconf, env)
        format_results(flyer, args['debug'])
        exit_code = 0
    elif args['debug']:
        eprint('No falconf found.')

    return exit_code
