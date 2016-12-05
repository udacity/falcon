"""
Parses config files and preps environments for testing.
"""

class Environment:
    """
    Manage the configuration for this Falcon flight.
    """
    def __init__(self, config_path=None):
        self.env_vars = []
        self.preload_files = []
        self.grader_libs = [] # name and version
        self.preprocess = ''
        self.includes = []
        self.compile_test = ''
        self.compile_submit = ''
        self.testing_entry = ''
        self.submit_entry = ''
        self.postprocess = ''
        self.additional_output = {} # extra fields on the output JSON

        self.parse_config(config_path)

    def parse_config(self, config_path):
        if config_path is not None:
            # load it
            pass
        else:
            # look for falconf.yaml in the cwd
            # run defaults for detected(?) language if not
            # look for testMain.*, submitMain.*, studentMain.*
            pass

    def symlink_libraries(self):
        # symlink grader_libs
        pass

# MODES = [m.lower() for m in dir(enum.Mode()) if not m.startswith('__')]