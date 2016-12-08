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
        # else:
        #     self.find_local_falconf()

    def get_falconf_for_mode(self, mode):
        """
        Get falconf for a mode.

        Args:
            mode (string): Either 'test' or 'submit'
        """
        if mode == 'test':
            return self.test
        elif mode == 'submit':
            return self.submit

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
        if file_exists(filename, path=self._cwd):
            ret = read_file(os.path.join(self._cwd, filename))

        return ret

    def get_local_falconf(self):
        """
        Look at cwd to try to find falconf.yaml in cwd.

        Returns:
            string: contents of falconf.yaml if found, otherwise None
        """
        # local_falconf = self.get_file_in_cwd('falconf.yaml')
        # if local_falconf is not None:
        #     self.parse_falconf(local_falconf)
        return self.get_file_in_cwd('falconf.yaml')
