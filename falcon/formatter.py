"""Formats remote execution output for the classroom or local debug."""

import os
import sys
import json
from falcon.util import *

"""
Formatter parses and formats output from each Step.
"""
class Formatter:
    def __init__(self, flyer=None, debug=False):
        """
        Default constructor.

        Args:
            flyer (Flyer)
        """
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

    def generate_results(self, flyer, debug=False):
        self.results['mode'] = flyer.mode
        steps = self.parse_steps(flyer)
        self.results['elapsed_time'] = flyer.elapsed_time
        self.results['student_out'] = self.get_student_out(flyer)
        self.results['student_err'] = self.get_student_err(flyer)
        self.results['is_correct'] = self.get_is_correct(self.results['student_out'])
        if debug:
            self.results['steps'] = steps

    def get_student_out(self, flyer):
        """
        Get output from student code. This is postprocess if it exists, otherwise main.

        Args:
            flyer (Flyer): Flyer that has already completed its sequence.
        """
        main_out = None
        postprocess_out = None
        grading_code_out = read_udacity_out()

        # TODO: if we move main out to a temp file, this will change.
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

        # TODO: if we move main err to a temp file, this will change.
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
            # 'elapsed_time': flyer.times[name],
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

    def remove_trailing_whitespace(self, string):
        """
        Get rid of the newlines that subprocess likes to add.

        string (string): String to strip.

        Returns:
            string: string sans trailing whitespace.
        """
        return string

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

    def pipe_debug_to_stdout(self):
        pass

    def pipe_to_stdout(self):
        result = {}
        result_json = self.json(result)
        # result_json = self.json(self.results)
        print(result_json)
        return result_json



def format_results_as_json_string(mode_idx, extra_file_paths, show_pretty_submit, transformer = None):
    """Formats the results of remote execution steps for the classroom.

    mode_idx == enum.Mode.test

        If a student runs "Test" and no error is produced, then a string
        with the contents of files.STUDENT_OUT is returned to the classroom.

        If a student runs "Test" and an error is produced, then a json-like
        string with entries for files.STUDENT_OUT and files.STUDENT_ERR is
        returned to the classroom.

    mode_idx == enum.Mode.submit

        If a student runs "Submit" and no error is produced, then the results
        of each execution step and the contents of any extra files are returned
        in a JSON-like string with predictable key/value pairs. The classroom
        consumes this JSON-like string (specifically the key/value pair for
        files.RESULTS_OUT) to generate feedback.

        If a student runs "Submit" and an error is produced, then a json-like
        string with entries for each execution step and the contents of any
        extra files are returned to the classroom.

    Args:
        mode_idx (int): represents whether student is testing or submitting
        extra_file_paths (list): file paths w/ contents to include in results
        show_pretty_submit (bool): flag for making output human-readable
        transformer (func): transforms contents of 'files.RESULTS_OUT' into
        a classroom-friendly format

    Returns:
        A string containing the results of evaluating the student's code. when
        submitting, the string will be in a JSON-like format.
    """
    results = {}

    # student runs "Test"
    if mode_idx == enum.Mode.test:
        # add/check output of student main
        util.add_file_contents_to_dictionary(files.STUDENT_OUT, results)
        util.add_file_contents_to_dictionary(files.STUDENT_ERR, results)
        if results[files.STUDENT_ERR] != '':
            return json.dumps(results) + "\n"
        else:
            return results[files.STUDENT_OUT]

    # student runs "Submit"
    if mode_idx == enum.Mode.submit:
        # add results output
        if transformer != None:
            results[files.RESULTS_OUT] = transformer(util.get_file_contents(files.RESULTS_OUT))
        else:
            util.add_file_contents_to_dictionary(files.RESULTS_OUT, results)
        util.add_file_contents_to_dictionary(files.RESULTS_ERR, results)
        # add/check output of student main (for extra debugging)
        util.add_file_contents_to_dictionary(files.STUDENT_OUT, results)
        util.add_file_contents_to_dictionary(files.STUDENT_ERR, results)
        # add contents of extra files
        for path in extra_file_paths:
            util.add_file_contents_to_dictionary(path, results)
        if show_pretty_submit:
            # return results in pretty format (human-readable feedback)
            return grade.convert_json_string_to_feedback(results) + "\n"
        else:
            # return all output as JSON-like string
            return json.dumps(results) + "\n"
