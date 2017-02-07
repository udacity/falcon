# eventually copy from falcon.py

import argparse
import sys

from udfalcon.falcon import main as falcon_main

def parse_args(args):
    """
    Argparse sys.argv[1:]

    Args:
        args (list): From sys.argv[1:]
    """
    parser = argparse.ArgumentParser(description='middleware for evaluating programming quizzes')
    parser.add_argument('-c', '--config',
                        action='store',
                        dest='config',
                        required=False,
                        help='Path to falconf.yaml.')
    parser.add_argument('-m', '--mode',
                        action='store',
                        default='submit',
                        dest='mode',
                        required=False,
                        help='The evaluation mode ("test" or "submit"). Defaults to "submit".')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        default=False,
                        dest='debug',
                        required=False,
                        help='Get more information along the way and print output from each step.')
    parser.add_argument('-l', '--link',
                        action='store',
                        default=False,
                        dest='link',
                        required=False,
                        help='Symlink a falcon library here for testing.')
    parser.add_argument('-o', '--output',
                        action='store',
                        choices=['json', 'formatted', 'clean', 'return'],
                        default='json',
                        dest='output',
                        required=False,
                        help='Output type. Note that if in "debug" mode, output is always "json".')

    args = parser.parse_args(args)
    return args, parser

def main():
    """
    Parse args and run falcon.
    """
    args, parser = parse_args(sys.argv[1:])
    exit_code = falcon_main(vars(args))

    if exit_code != 0:
        parser.print_help()

if __name__ == '__main__':
    main()
