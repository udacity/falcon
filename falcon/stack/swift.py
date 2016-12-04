"""Functions for evaluating quizzes in Swift using pass/fail functions."""

import os
import falcon.enum as enum
import falcon.util as util
import falcon.files as files

def setup_local_test():
    """Configure environment (namely the root directory) for local execution."""
    util.move_sandbox_files_to_root('swift', ['SwizzleInclude.swift', 'SwizzleBefore.swift', 'StudentMain.swift', 'SwizzleAfter.swift'])

def setup_remote():
    """Configure environment (namely the root directory) for remote execution."""
    util.move_sandbox_files_to_root('swift', ['SwizzleInclude.swift'])

def tear_down_local_test():
    """Tear down environment (namely the root directory) after local execution."""
    util.remove_files_from_root(['SwizzleInclude.swift', 'SwizzleBefore.swift', 'StudentMain.swift', 'SwizzleAfter.swift', 'SwizzledMain.swift'])

def test(run_local, bash_config):
    """Test (run) student's code without evaluating it for correctness.

    This function should store the output of the student's code in
    files.STUDENT_OUT. It is recommended that you use util.run_program()
    to pipe the results of executing the student's code into
    files.STUDENT_OUT (stdout) and files.STUDENT_ERR (stderr).

    Args:
        run_local (bool): flag indicating if test is being run locally
        bash_config (string): bash commands for configuing environment

    Raises:
        Any errors stemming from the exection of the program(s) required to
        run the student's code.
    """
    try:
        util.run_program(['swift', 'StudentMain.swift'], files.STUDENT_OUT, files.STUDENT_ERR)
    except:
        raise

def submit(run_local, bash_config):
    """Evaluate the student's code by testing it for correctness.

    This function should store the output of evaluating the student's code
    in files.RESULTS_OUT. It is recommended that you use util.run_program()
    to pipe the results of evaluating the student's code into
    files.RESULTS_OUT (stdout) and files.RESULTS_ERR (stderr).

    Args:
        run_local (bool): flag indicating if test is being run locally
        bash_config (string): bash commands for configuing environment

    Raises:
        Any errors stemming from the exection of the program(s) required to
        evalute the student's code.
    """
    try:
        # generate swizzled main
        filenames = ['SwizzleInclude.swift', 'SwizzleBefore.swift', 'StudentMain.swift', 'SwizzleAfter.swift']
        errors = []
        with open('SwizzledMain.swift', 'w') as outfile:
            for fname in filenames:
                try:
                    with open(fname) as infile:
                        outfile.write(infile.read())
                except IOError:
                    errors.append('file ' + fname + ' not found')
                else:
                    outfile.write('\n')
        if len(errors) > 0:
            # pipe errors to file
            util.run_program(['echo', str(errors)], files.RESULTS_ERR, files.RESULTS_ERR)
        else:
            # run swizzled main
            util.run_program(['swift', '-suppress-warnings', 'SwizzledMain.swift'], files.RESULTS_OUT, files.RESULTS_ERR)
            # run student main (for extra debugging)
            util.run_program(['swift', 'StudentMain.swift'], files.STUDENT_OUT, files.STUDENT_ERR)
    except:
        raise

def submit_files():
    """Specifies a list of file paths to include in results when student submits quiz."""
    return ['StudentMain.swift']

def transform(test_output):
    """Transforms contents of 'files.RESULTS_OUT' into a classroom-friendly format.

    Currently, the classroom understands the following tags:
        - <PASS::>
        - <FAIL::>
        - <FEEDBACK::>

    All lines prepended with these tags will be auto-formatted:
        - <PASS::>
            represents something the student did correctly and is displayed
            in the "What Went Well" section
        - <FAIL::>
            represents something the student did incorrectly and is displayed
            in the "What Went Wrong" section
        - <FEEDBACK::>
            additional feedback to either guide or congradulate the student
            that appears in the "Feedback" section

    Note: If the contents of 'files.RESULTS_OUT' already use tags, then
    you can simply return the eval_output unmodified.

    Args:
        eval_output (string): Contents of 'files.RESULTS_OUT'

    Returns:
        A string with classroom-friendly tags that represents the results of
        evaluating the student's code for a programming quiz.
    """
    return test_output
