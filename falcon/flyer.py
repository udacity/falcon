"""
Handles any execution that needs to happen at any stage.
"""

import formatter
from falcon.util import eprint

class Flyer:
    """
    Makes sure that unsafer execution happens safely and sanely.
    """
    def __init__(self, mode='submit', local=False, debug=False):
        """
        Default constructor.

        Args:
            mode (string): 'test' or 'submit'.
            local (bool): Whether this is run locally or remotely.
            debug (bool): Show debug output while running.
        """
        self.sequence = []
        self.mode = mode
        self.debug = debug
        self.local = local
        self.errs = {}
        self.outs = {}

    def generate_err(self, step, err):
        """
        Handle an error.

        Args:
            step (string): Describes the generate step in execution when err occured.
            err (Exceptions): Err to record/display.
        """
        self.errs[step] = err
        if self.debug:
            eprint(err)
            raise err

    def generate_output(self, step, out):
        """
        Handle output from a step.

        Args:
            step (string): Description of when this output occured.
            out (string): The output
        """
        self.outs[step] = out
        if self.debug:
            print(out)

    def run_shell_script(self, script):
        pass

    def run_shell_command(self, command):
        pass

    def run_python_file(self, filepath, args=[]):
        pass

    def run_sequence(self, env):
        """
        Start to finish, run the steps in the quiz.

        Args:
            env (Environment): Includes info on where to execute
        """
        pass


# if ARGS.debug:
#     util.set_testing(True)

# if running locally...
# if ARGS.run_local:
#     # setup local test
#     # STACK_MODULE.setup_local_test()
#     # remove any pre-existing text files
#     util.remove_temp_text_files()

# evaluate the student's code
# try:
#     if MODE_IDX == enum.Mode.test:
#         # STACK_MODULE.test(ARGS.run_local, BASH_CONFIG)
#     elif MODE_IDX == enum.Mode.submit:
#         # STACK_MODULE.submit(ARGS.run_local, BASH_CONFIG)
#     else:
#         sys.stdout.write('unsupported evaluation mode')
# except:
#     if ARGS.debug:
#         # if in debug mode, show the actual error (instead of "hiding it")
#         raise
#     else:
#         # if there was an issue, return partial results (the error output)
#         sys.stdout.write(formatter.format_results_as_json_string(MODE_IDX,
#                                                                  STACK_MODULE.submit_files(),
#                                                                  ARGS.show_pretty_submit,
#                                                                  STACK_MODULE.transform))