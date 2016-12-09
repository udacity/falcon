"""
Represents a generic command that can be run against student code during execution.
"""

import os
import shlex
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
        self.dir = ''

    def chdir(self, directory, callback):
        """
        You're probably trying to hack something if you need to use this.
        """
        olddir = os.getcwd()
        os.chdir(directory)
        outs = callback()
        os.chdir(olddir)
        return outs

    def set_shell_command(self, cmd, tempdir=None):
        """
        Set a shell command. Runs from falconf.yaml directory. DON'T EVEN THINK OF RUNNING STUDENT CODE DIRECTLY AS CMD.

        Args:
            cmd (string): Shell command to call. CMD SHALL NOT BE CONTROLLED BY STUDENTS!!!
            tempdir (string): Temporary directory to execute command.
        """
        self.type = 'shell'
        if tempdir is not None:
            self.command = lambda : self.chdir(tempdir, lambda : run_shell_cmd(cmd))
        else:
            self.command = lambda : run_shell_cmd(cmd)

    def set_falcon_command(self, cmd, args, tempdir=None):
        pass

    def set_shell_executable(self, cmd, tempdir=None):
        """
        Set an executable file to run in the sequence. Called as `./path/to/file.sh` or `./path/to/file.py`, so use a #!

        Args:
            cmd (string): command with the executable
            args (list): Any additional arguments.
            tempdir (string): Temporary directory to execute command.
        """
        self.type = 'executable'
        if tempdir is not None:
            self.command = lambda : self.chdir(tempdir, lambda : run_shell_executable(cmd))
        else:
            self.command = lambda : run_shell_executable(cmd)

    def set_noop(self, cmd=None):
        """
        Don't do anything!
        """
        self.type = 'noop'
        def noop():
            return '', ''
        self.command = noop

    def run_falcon_command(self, command, args=[]):
        pass

    def run(self):
        out = None
        err = None

        out, err = self.command()

        return out, err