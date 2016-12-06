"""
Represents a generic command that can be run against student code during execution.
"""

import os
from falcon.util import *

class Step:
    """
    A generic command.
    """
    def __init__(self, name=None, cmd=None, executable=None):
        """
        Construct the Step.

        Args:
            name (string): The name of the step. Used to find file names!
        """

        self.command = None
        self.name = name
        self.type = None

    def set_shell_command(self, cmd):
        """
        Set a shell command. DON'T EVEN THINK OF RUNNING STUDENT CODE DIRECTLY AS CMD.

        Args:
            cmd (string): Shell command to call. CMD SHALL NOT BE CONTROLLED BY STUDENTS!!!
        """
        self.type = 'shell'
        self.command = lambda : run_shell_cmd(cmd)

    def set_falcon_command(self, cmd, args):
        pass

    def set_executable(self, filename):
        pass

    def set_noop(self):
        """
        Don't do anything!
        """
        def noop():
            return '', ''
        self.command = noop

    def run_shell_script(self, script):
        pass

    def run_shell_command(self, command):
        pass

    def run_python_file(self, filepath, args=[]):
        pass

    def run_falcon_command(self, command, args=[]):
        pass

    def run(self):
        out = None # from student code
        err = None # from student code

        out, err = self.command()

        return out, err