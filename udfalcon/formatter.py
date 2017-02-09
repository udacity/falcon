"""Formats remote execution output for the classroom or local debug."""

from collections import OrderedDict
import os
import pprint
import sys
import json
from udfalcon.util import *

pp = pprint.PrettyPrinter(indent=4)

"""
Formatter parses and formats output from each Step.
"""
class Formatter:
    def __init__(self, flyer=None, debug=False, elapsed_time=None):
        """
        Default constructor.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        self.elapsed_time = elapsed_time

        self.results = {
            'config_file': '',
            'elapsed_time': -1,
            'is_correct': False,
            'mode': '',
            'steps': [],
            'student_out': '',
            'student_err': ''
        }
        if flyer is not None and flyer.has_flown:
            self.generate_results(flyer)

        if elapsed_time is not None:
            self.results['elapsed_time'] = elapsed_time

    def generate_results(self, flyer):
        """
        Create the flight results dict.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        self.results['mode'] = flyer.mode
        steps = self.parse_steps(flyer)
        self.results['student_out'] = self.get_student_out(flyer)
        self.results['student_err'] = self.get_student_err(flyer)
        self.results['is_correct'] = self.get_is_correct()
        self.results['steps'] = steps

    def get_student_out(self, flyer):
        """
        Get output from student code. This is postprocess if it exists, otherwise custom grading output, otherwise main.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        postprocess_out = None
        grading_code_out = read_udacity_out()
        main_out = None

        if exists(dictionary=flyer.outs, key='main'):
            main_out = flyer.outs['main']

        if exists(dictionary=flyer.outs, key='postprocess'):
            postprocess_out = flyer.outs['postprocess']

        if postprocess_out:
            return postprocess_out
        elif grading_code_out:
            return grading_code_out
        elif main_out:
            return main_out
        else:
            return ''

    def get_student_err(self, flyer):
        """
        Get err from student code. This is postprocess if it exists, otherwise main.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        main_err = None
        postprocess_err = None

        if exists(dictionary=flyer.errs, key='main'):
            main_err = flyer.errs['main']

        if exists(dictionary=flyer.errs, key='postprocess'):
            postprocess_err = flyer.errs['postprocess']

        if postprocess_err:
            return postprocess_err
        elif main_err:
            return main_err
        else:
            return ''

    def get_is_correct(self, grading_code_out=None):
        """
        Pull is_correct from the file pulled from read_udacity_out(). Looks for the tags <::PASS> or <::FAIL>.

        Returns:
            bool: if <::PASS> or <::FAIL> exist
            None: if neither exist
        """
        if grading_code_out is None:
            grading_code_out = read_udacity_out()

        if '<::PASS>' in grading_code_out:
            return True
        elif '<::FAIL>' in grading_code_out:
            return False
        else:
            return None

    def get_step_result(self, name, flyer):
        """
        Pull info on a specific Step.

        Args:
            name (string): Name of the Step.
            flyer (Flyer): Flyer where it ran.
        """
        result = {
            'name': name,
            'command': flyer.sequence[name].falconf_command,
            'elapsed_time': flyer.sequence[name].elapsed_time,
            'type': flyer.sequence[name].type
        }
        result['out'] = flyer.outs[name]
        result['err'] = flyer.errs[name]
        return result

    def parse_steps(self, flyer):
        """
        Get info on each Step and the way it ran.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        result = OrderedDict()
        for name in flyer.outs:
            result[name] = self.get_step_result(name, flyer)

        return [v for v in result.values()]

    def json(self, dictionary):
        """
        Get a stringified JSON of a dict.

        Args:
            dictionary (dict)

        Returns:
            string: stringified JSON of the dict.
        """
        try:
            return json.dumps(dictionary)
        except Exception as e:
            return json.dumps(str(dictionary))

    def pipe_debug_to_stdout(self, flyer):
        """
        Print the flight results as a pretty, human-readable JSON.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        self.generate_results(flyer)
        print('------------\nOUTPUT SENT TO CLASSROOM:')
        pp.pprint(self.results)

    def pipe_to_stdout(self, flyer):
        """
        Print the flight results as a dict.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        self.generate_results(flyer)
        print(self.json(self.results))

    def return_results(self, flyer):
        """
        Return the results of the flight to the caller. This is only used when importing the library (eg. `udfalcon.fly()`).
        """
        self.generate_results(flyer)
        return self.results
