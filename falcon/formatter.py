"""Formats remote execution output for the classroom."""

import os
import sys
import json
import falcon.util as util
import falcon.enum as enum
import falcon.grade as grade
import falcon.files as files

# class Formatter:



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
