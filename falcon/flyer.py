"""
Handles any execution that needs to happen at any stage.
"""

import os
import formatter
from falcon.step import Step
from falcon.util import *

class Flyer:
    """
    Makes sure that unsafer execution happens safely and sanely.
    """
    def __init__(self, mode='submit', local=False, debug=False, env=None):
        """
        Default constructor.

        Args:
            mode (string): 'test' or 'submit'.
            local (bool): Whether this is run locally or remotely.
            debug (bool): Show debug output while running.
            env (Environment): Includes info on where and what to execute.
        """

        self.sequence = []
        self.mode = mode
        self.debug = debug
        self.local = local
        self.errs = {}
        self.outs = {}
        if env is not None:
            self.prep_sequence(env)

    def prep_sequence(self, env):
        """
        Get the sequence ready to run based on the environment.

        Args:
            env (Environment): Includes info on where and what to execute.
        """
        self.falconf = env[mode]
        self.create_sequence(env)

    def create_step(self, name=None, cmd=None):
        """
        Create a step where a command may be executed.

        Args:
            name (string): The name of the step.
        """
        step = Step(name=name, cmd=cmd)
        return step

    def create_sequence(self, env):
        """
        Start to finish, create the steps in the quiz.

        Args:
            env (Environment): Includes info on where files can be found.
        """
        # Flyer will run defaults for detected(?) language if not
        # look for testMain.*, submitMain.*, studentMain.*

        # 1) do nothing and specify nothing in falconf.yaml, and nothing will happen
        # 2) add a preprocess.sh file and it will automatically run then
        sequence_of_events = [
            'preprocess',
            'compile',
            'main',
            'postprocess',
            'tear_down'
        ]
        step = None
        for event_name in sequence_of_events:
            step = self.create_step(name=event_name)
            step = self.figure_out_right_action(step)
        self.sequence.append(step)

    def figure_out_right_action(step):
        default_file = self.get_default_file(step.name)

        # prioritize falconf commands
        if exists(dictionary=self.falconf, key=self.mode):
            falconf = self.falconf[self.mode]

            if self.has_executable_specified(falconf):
                step.set_executable(falconf)
            elif self.has_falcon_command(falconf):
                step.set_falcon_command(falconf)
            elif self.has_shell_command(falconf):
                step.set_shell_command(falconf)
            else:
                raise Exception('Invalid falconf command: ' + falconf)

        # no falconf
        elif default_file:
            step.set_executable(default_file)

        # don't do anything!
        else:
            step.set_noop()

        return step

    def has_executable_specified(self, falconf):
        # ret = None
        # return does_file_exist(falconf)
        pass

    def get_default_file(self, step_name):
        # .py first, then .sh
        pass

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

    def set_env_var(self, key, value):
        """
        Set an environment for the entire Falcon flight.

        Args:
            key (string): The variable. Probably should be ALL_CAPS.
            value (*): The value
        """
        os.environ[key] = value

    def set_env_vars(self, env_vars=[]):
        """
        Set many environment variables.

        Args:
            env_vars (list of dicts): [{KEY: value}] for each env var.
        """
        for evar in env_vars:
            for key, value in evar.items():
                self.set_env_var(key, value)

    def symlink_libraries(self):
        # symlink grader_libs
        pass

    def run_sequence(self):
        """
        Start to finish, run the steps in the quiz.
        """
        self.set_env_vars(self.falconf.env_vars)
        self.symlink_libraries()
        for step in self.sequence:
            out, err = step.run()
            self.generate_output(out)
            self.generate_err(err)

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