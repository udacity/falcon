"""Formats remote execution output for the classroom or local debug."""

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
            flyer (Flyer)
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
            self.generate_results(flyer, debug)

        if elapsed_time is not None:
            self.results['elapsed_time'] = elapsed_time

    def generate_results(self, flyer, debug=True):
        self.results['mode'] = flyer.mode
        steps = self.parse_steps(flyer)
        self.results['student_out'] = self.get_student_out(flyer)
        self.results['student_err'] = self.get_student_err(flyer)
        self.results['is_correct'] = self.get_is_correct(self.results['student_out'])
        self.results['steps'] = steps

    def get_student_out(self, flyer):
        """
        Get output from student code. This is postprocess if it exists, otherwise main.

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

    def get_is_correct(self, student_out, key=None):
        """
        Pull is_correct from student_out.

        Args:
            student_out (stringified json): Student output.
            key (string): If present, use the boolean from the key to determine is_correct.

        Returns:
            bool: True if confirmed, False if missing or malformed.
        """
        pass

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
        """
        result = {}
        for name in flyer.outs:
            result[name] = self.get_step_result(name, flyer)

        return [v for v in result.values()]

    def get_meta_info(self, flyer):
        pass

    def pipe_student_out(self):
        self.results[student_out] = student_out
        pass

    def pipe_student_err(self):
        pass

    def json(self, dictionary):
        """
        Get a stringified JSON of a dict.

        Args:
            dictionary (dict)

        Returns:
            string: stringified JSON of the dict.
        """
        return json.dumps(dictionary)

    def pipe_debug_to_stdout(self, flyer):
        self.generate_results(flyer, True)
        print('------------\nOUTPUT SENT TO CLASSROOM:')
        pp.pprint(self.results)

    def pipe_to_stdout(self, flyer):
        self.generate_results(flyer, True)
        print(self.json(self.results))
