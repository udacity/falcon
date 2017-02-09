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

def format_results(flyer, debug, output='json'):
    """
    Use debug and output to decide how to show results of the run.

    Args:
        flyer (Flyer)
        debug (boolean)
        output (string): One of 'json', 'formatted', 'clean', 'return'. Defaults to 'json'.

    Returns:
        None: if output != 'return'
        dict: if output == 'return'
    """
    formatter = Formatter(flyer, elapsed_time=ELAPSED_TIME)
    formatter.parse_steps(flyer)

    if debug:
        # print a pretty version of the results JSON
        formatter.pipe_debug_to_stdout(flyer)
        return None
    elif output == 'return':
        # just return the results dict
        return formatter.return_results(flyer)
    elif output == 'formatted':
        """
        print results as:

        ------------------
        Executing `command` ...
        stderr
        stdout
        ------------------
        """
        results = formatter.return_results(flyer)
        steps = results['steps']

        for s in range(len(steps)):
            if steps[s]['command'] is not 'noop':
                print('Executing `{}`...'.format(steps[s]['command']))
                stderr = steps[s]['err']
                if stderr != '':
                    eprint(stderr)
                stdout = steps[s]['out']
                if stdout != '':
                    print(stdout)
                if s < len(steps) - 1:
                    print('\n------------------')
        return None
    elif output == 'clean':
        """
        print results as a sequence of:

        stderr
        stdout
        """
        results = formatter.return_results(flyer)
        steps = results['steps']

        for s in range(len(steps)):
            if steps[s]['command'] is not 'noop':
                err = steps[s]['err']
                if err != '':
                    eprint(err)
                out = steps[s]['out']
                if out != '':
                    print(out)
    else:
        # print the results JSON
        formatter.pipe_to_stdout(flyer)
        return None

def main(args={}):
    """
    The main event.

    Args:
        args (dict)

    Returns:
        int: Exit code.
        string: If output == 'return'
    """
    exit_code = 1
    falconf = None
    local_falconf = None
    env = Environment()

    # this dictionary checking exists to rectify usage with command line args and the config dict passed to udfalcon.fly()
    if not exists(dictionary=args, key='mode'):
        args['mode'] = 'submit'

    if not exists(dictionary=args, key='debug'):
        args['debug'] = False

    if not exists(dictionary=args, key='output'):
        args['output'] = 'json'

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
            print('Using local falconf file.')
        falconf = env.get_local_falconf()

    possible_results_output = None

    # run student code
    if falconf is not None:
        flyer = fly(args, falconf, env)
        possible_results_output = format_results(flyer, args['debug'], args['output'])
        exit_code = 0
    elif args['debug']:
        eprint('No falconf found.')

    if possible_results_output is not None:
        return possible_results_output
    else:
        return exit_code
