"""
Handles any execution that needs to happen at any stage.
"""

from collections import OrderedDict
import os
import re
import shlex
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

        self.has_flown = False
        self.elapsed_time = -1
        self.times = {}
        self.sequence = OrderedDict()
        self.mode = mode
        self.debug = debug
        self.local = local
        self.errs = {}
        self.outs = {}
        if env is not None:
            self.prep_sequence(mode, env)

    def prep_sequence(self, mode, env):
        """
        Get the sequence ready to run based on the environment.

        Args:
            mode (string): 'test' or 'submit'.
            env (Environment): Includes info on where and what to execute.
        """
        self.falconf = env.get_falconf_for_mode(mode)
        self.falconf_dir = os.getcwd()

    def create_step(self, name=None):
        """
        Create a step where a command may be executed.

        Args:
            name (string): The name of the step.
        """
        step = Step(name=name)
        return step

    def create_sequence(self):
        """
        Start to finish, create the steps in the quiz.
        """

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
            self.sequence[event_name] = step

    def run_sequence(self):
        """
        Start to finish, run the steps in the quiz.
        """
        # run in ~/.falcontmp?
        if exists(dictionary=self.falconf, key='env_vars'):
            self.set_env_vars(self.falconf['env_vars'])
        self.symlink_libraries()
        for step in self.sequence.values():
            out, err = step.run()
            self.generate_output(step.name, out)
            self.generate_err(step.name, err)
        self.has_flown = True

    def figure_out_right_action(self, step):
        """
        Determines the action the step should perform based on a mix of
        the falconf.yaml file and the files in the cwd. These commands are best guesses. They are not validated as some files may not exist and some commands may depend on prior steps to work.

        The prioritization for actions is as follows:

               falconf          |      file       |       Action
        ------------------------|-----------------|---------------------
        1)  file.ext            |      <--        |   ./file.ext
        2)  falcon.action ...   |       *         |   falcon action
        3)  echo "bar"          |       *         |   echo "bar"
        4)      --              | stepname.ext    |   ./stepname.ext
        5)      --              |      --         |         --
        """
        default_file = self.get_default_file(step.name)

        # prioritize falconf commands
        if exists(dictionary=self.falconf, key=step.name):
            falconf = self.falconf[step.name]

            if self.has_executable_file(falconf):
                filepath = os.path.join(self.falconf_dir, falconf)
                step.set_shell_executable(filepath)
            elif self.has_falcon_command(falconf):
                step.set_falcon_command(falconf)
            elif self.has_shell_command(falconf):
                step.set_shell_command(falconf)
            else:
                raise Exception('Invalid falconf command for {}: {}'.format(step.name, falconf))

            # for reference later
            step.falconf_command = falconf

        # no falconf
        elif default_file is not None:
            step.set_shell_executable(default_file)
            step.falconf_command = default_file

        # don't do anything!
        else:
            step.set_noop()
            step.falconf_command = 'noop'


        return step

    def has_executable_file(self, falconf):
        """
        Match the falconf against a regex to find commands that start with a file with extension. The file does not need to exist.

        Args:
            falconf (string): Falcon command.

        Returns:
            bool
        """
        return re.match('^\S+\.\S+', falconf, re.I) and re.match('^falcon\.', falconf, re.I) is None

    def has_falcon_command(self, falconf):
        """
        FIXME: NOT READY YET!
        Match the falconf against a command of the style falcon.foo.

        Args:
            falconf (string): Falcon command.
        """
        return re.match('^falcon\.', falconf, re.I)

    def has_shell_command(self, falconf):
        """
        Look for a valid shell command as the first argument.
        """
        maybe_command = shlex.split(falconf)[0]
        return check_valid_shell_command(['which', maybe_command])

    def get_default_file(self, step_name):
        """
        Look in falconf path to get an executable file for the eponymous Step.

        Args:
            step_name (string): Name of the Step.

        Returns:
            string: abspath to file
        """
        filename = get_file_with_basename(self.falconf_dir, step_name)
        if filename:
            return os.path.join(self.falconf_dir, filename)
        else:
            return None

    def generate_err(self, stepname, err):
        """
        Handle an error.

        Args:
            stepname (string): Describes the generate step in execution when err occured.
            err (Exceptions): Err to record/display.
        """
        self.errs[stepname] = err
        if self.debug and len(str(err)) > 0:
            eprint(stepname + ' erred:\n' + str(err))
            raise Exception(err)

    def generate_output(self, stepname, out):
        """
        Handle output from a step.

        Args:
            stepname (string): Description of when this output occured.
            out (string): The output
        """
        self.outs[stepname] = out
        if self.debug:
            print(stepname + ':\n' + str(out))

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
