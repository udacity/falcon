"""
Parses config files and preps environments for testing.
"""

import yaml
from falcon.util import exists, read_file

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

        if falconf_string is None and falconf_path is not None:
            falconf_string = read_file(falconf_path)

        if falconf_string:
            self.parse_falconf(falconf_string)
        else:
            self.determine_defaults()

    def parse_falconf(self, falconf_string):
        falconf = yaml.load(falconf_string)
        if exists(dictionary=falconf, key='test'):
            self.test = falconf['test']
        if exists(dictionary=falconf, key='submit'):
            self.submit = falconf['submit']

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