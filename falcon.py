"""Python middleware for evaluating programming quizzes."""

import os
import sys
import imp
# import json
import argparse
import falcon.enum as enum
import falcon.util as util
import falcon.files as files
import falcon.formatter as formatter

# init local bash config
BASH_CONFIG = ''

# create arrays containing all possible "enum" values
STACKS = [s.lower() for s in dir(enum.Stack()) if not s.startswith('__')]
MODES = [m.lower() for m in dir(enum.Mode()) if not m.startswith('__')]

# define arguments
PARSER = argparse.ArgumentParser(description='middleware for evaluating programming quizzes')
PARSER.add_argument('-s', '-stack',
                    action='store',
                    dest='stack',
                    required=True,
                    help='the language and test framework (' + str(', '.join(STACKS)) + ')')
PARSER.add_argument('-m', '-mode',
                    action='store',
                    dest='mode',
                    required=True,
                    help='the evaluation mode (' + str(', '.join(MODES)) + ')')
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

# parse arguments
ARGS = PARSER.parse_args()
STACK_PAIR = ARGS.stack.lower()
LANG = ARGS.stack.lower().split('_')[0]

# get stack and mode indices
STACK_IDX = None
MODE_IDX = None
for idx, s in enumerate(STACKS):
    if STACK_PAIR == s:
        STACK_IDX = idx
for idx, m in enumerate(MODES):
    if ARGS.mode.lower() == m:
        MODE_IDX = idx

# exit for unsupported STACKS
if STACK_IDX is None:
    PARSER.print_usage()
    print('falcon.py: error: argument -s/-stack must be supported (' + str(', '.join(STACKS)) + ')')
    sys.exit(0)

# exit for unsupported evaluation MODES
if MODE_IDX is None:
    PARSER.print_usage()
    print('falcon.py: error: argument -m/-mode must be supported (' + str(', '.join(MODES)) + ')')
    sys.exit(0)

# get stack-specific functionality
STACK_MODULE_PATH = 'falcon/stack/' + STACK_PAIR + '.py'
if os.path.exists(STACK_MODULE_PATH):
    STACK_MODULE = imp.load_source(LANG, STACK_MODULE_PATH)
else:
    print('functionality not defined for stack: ' + STACK_PAIR)
    sys.exit(0)

# if running locally...
if ARGS.run_local:
    # setup local test
    STACK_MODULE.setup_local_test()
    # remove any pre-existing text files
    util.remove_temp_text_files()
else:
    # setup remote
    STACK_MODULE.setup_remote()

# if specified, load bash config for the stack
BASH_CONFIG_PATH = files.CONFIG_DIR + '/' + STACK_PAIR + '.sh'
if os.path.isfile(BASH_CONFIG_PATH):
    with open(BASH_CONFIG_PATH) as bash_file:
        BASH_CONFIG = ''.join(bash_file.readlines())

# evaluate the student's code
try:
    if MODE_IDX == enum.Mode.test:
        STACK_MODULE.test(ARGS.run_local, BASH_CONFIG)
    elif MODE_IDX == enum.Mode.submit:
        STACK_MODULE.submit(ARGS.run_local, BASH_CONFIG)
    else:
        sys.stdout.write('unsupported evaluation mode')
except:
    if ARGS.debug:
        # if in debug mode, show the actual error (instead of "hiding it")
        raise
    else:
        # if there was an issue, return partial results (the error output)
        sys.stdout.write(formatter.format_results_as_json_string(MODE_IDX,
                                                                 STACK_MODULE.submit_files(),
                                                                 ARGS.show_pretty_submit,
                                                                 STACK_MODULE.transform))
else:
    # return full results
    RESULTS = formatter.format_results_as_json_string(MODE_IDX, STACK_MODULE.submit_files(),
                                                      ARGS.show_pretty_submit,
                                                      STACK_MODULE.transform)
    sys.stdout.write(RESULTS)
finally:
    # tear down any local files
    STACK_MODULE.tear_down_local_test()
