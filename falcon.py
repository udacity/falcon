"""Python middleware for evaluating programming quizzes."""

import os
import sys
import imp
import json
import argparse
import falcon.enum as enum
import falcon.util as util
import falcon.files as files
import falcon.formatter as formatter

# init local bash config
bash_config = ''

# create arrays containing all possible "enum" values
stacks = [s.lower() for s in dir(enum.Stack()) if not s.startswith('__')]
modes = [m.lower() for m in dir(enum.Mode()) if not m.startswith('__')]

# define arguments
parser = argparse.ArgumentParser(description = 'middleware for evaluating programming quizzes')
parser.add_argument('-s', '-stack', action = 'store', dest = 'stack', required = True, help = 'the language and test framework for the quiz (' + str(', '.join(stacks)) + ')')
parser.add_argument('-m', '-mode', action = 'store', dest = 'mode', required = True, help = 'the evaluation mode for the quiz (' + str(', '.join(modes)) + ')')
parser.add_argument('-l', '-local', action = 'store_true', dest = 'run_local', help = 'run falcon locally')
parser.add_argument('-p', '-pretty', action = 'store_true', dest = 'show_pretty_submit', help = 'show formatted submit output')
parser.add_argument('-d', '-debug', action = 'store_true', dest = 'debug', help = 'run falcon in debug mode')

# parse arguments
args = parser.parse_args()
stack_pair = args.stack.lower()
lang = args.stack.lower().split('_')[0]

# get stack and mode indices
stack_idx = None
mode_idx = None
for idx, s in enumerate(stacks):
    if stack_pair == s:
        stack_idx = idx
for idx, m in enumerate(modes):
    if args.mode.lower() == m:
        mode_idx = idx

# exit for unsupported stacks
if stack_idx == None:
    parser.print_usage()
    print 'falcon.py: error: argument -s/-stack must be supported (' + str(', '.join(stacks)) + ')'
    sys.exit(0)

# exit for unsupported evaluation modes
if mode_idx == None:
    parser.print_usage()
    print 'falcon.py: error: argument -m/-mode must be supported (' + str(', '.join(modes)) + ')'
    sys.exit(0)

# get stack-specific functionality
stack_module_path = 'falcon/stack/' + stack_pair + '.py'
if os.path.exists(stack_module_path):
    stack_module = imp.load_source(lang, stack_module_path)
else:
   print 'functionality not defined for stack: ' + stack_pair
   sys.exit(0)

# if running locally...
if args.run_local:
    # setup local test
    stack_module.setup_local_test()
    # remove any pre-existing text files
    util.remove_temp_text_files()
else:
    # setup remote
    stack_module.setup_remote()

# if specified, load bash config for the stack
bash_config_path = files.CONFIG_DIR + '/' + stack_pair + '.sh'
if os.path.isfile(bash_config_path):
    with open(bash_config_path) as bash_file:
        bash_config = ''.join(bash_file.readlines())

# evaluate the student's code
try:
    if mode_idx == enum.Mode.test:
        stack_module.test(args.run_local, bash_config)
    elif mode_idx == enum.Mode.submit:
        stack_module.submit(args.run_local, bash_config)
    else:
        sys.stdout.write('unsupported evaluation mode')
except:
    if args.debug:
        # if in debug mode, show the actual error (instead of "hiding it")
        raise
    else:
        # if there was an issue, return partial results (the error output)
        sys.stdout.write(formatter.format_results_as_json_string(mode_idx, stack_module.submit_files(), args.show_pretty_submit, stack_module.transform))
else:
    # return full results
    sys.stdout.write(formatter.format_results_as_json_string(mode_idx, stack_module.submit_files(), args.show_pretty_submit, stack_module.transform))
finally:
    # tear down any local files
    stack_module.tear_down_local_test()
