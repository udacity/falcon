#!/usr/bin/env python3

"""Python middleware for evaluating programming quizzes."""

import sys
import argparse
from environment import Environment
from flyer import Flyer

def main(args):
    """
    The main event.
    """
    exit_code = 0 # I suppose there should be an opportunity for this to change?
    env = Environment(args.config) # could be mode, etc
    flyer = Flyer(mode=args.mode, local=args.local, debug=args.debug, env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    # TODO: write output somewhere
    sys.exit(exit_code)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='middleware for evaluating programming quizzes')
    PARSER.add_argument('-c', '-config',
                        action='store',
                        dest='config',
                        required=False,
                        help='path to falconf.yaml')
    PARSER.add_argument('-m', '-mode',
                        action='store',
                        dest='mode',
                        required=False,
                        help='the evaluation mode ("test" or "submit")')
    PARSER.add_argument('-l', '-local',
                        action='store_true',
                        dest='run_local',
                        help='run falcon locally')
    PARSER.add_argument('-p', '-pretty',
                        action='store_true',
                        dest='show_pretty_submit',
                        help='show formatted submit output')
    PARSER.add_argument('-d', '-debug',
                        action='store_true',
                        dest='debug',
                        help='run falcon in debug mode')
    PARSER.add_argument('-i', '-init',
                        help='helper to create a new falconf.yaml file')

    # parse arguments
    ARGS = PARSER.parse_args()
    main(ARGS)
