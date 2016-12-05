"""
Parses config files and preps environments for testing.
"""

import os
import yaml
from falcon.util import *

class Environment:
    """
    Manage the configuration for this Falcon flight.
    """
    def __init__(self, falconf_path=None, falconf_string=None):
        """
        Construct an environment.

        Args:
            falconf_path (string): Path to falconf.yaml
            falconf_string (string): Basically a dumped yaml.
        """

        self.test = {}
        self.submit = {}

        self._cwd = os.getcwd()

        if falconf_string is None and falconf_path is not None:
            falconf_string = read_file(falconf_path)

        if falconf_string:
            self.parse_falconf(falconf_string)
        else:
            self.determine_defaults()

    def parse_falconf(self, falconf_string):
        loaded_something = False
        falconf = yaml.load(falconf_string)
        if exists(dictionary=falconf, key='test'):
            self.test = falconf['test']
            loaded_something = True
        if exists(dictionary=falconf, key='submit'):
            loaded_something = True
            self.submit = falconf['submit']

        if not loaded_something:
            raise Exception('Bad falconf! It should include test and/or submit!')

    def get_file_in_cwd(self, filename):
        """
        Get a file in the CWD.

        Args:
            filename (string): name.ext

        Returns:
            String contents of file if it exists, None otherwise.
        """
        ret = None
        if file_exists_in_abspath(self._cwd, filename):
            ret = read_file(os.path.join(self._cwd, filename))

        return ret

    def symlink_libraries(self):
        # symlink grader_libs
        pass

    def determine_defaults(self):
        """
        Look at cwd and try to find default files.
        """
        # look for falconf.yaml in the cwd
        # run defaults for detected(?) language if not
        # look for testMain.*, submitMain.*, studentMain.*
        pass

# MODES = [m.lower() for m in dir(enum.Mode()) if not m.startswith('__')]