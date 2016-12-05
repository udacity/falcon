"""Functions for evaluating quizzes in C++ using pass/fail functions."""

import os
import falcon.util as util
import falcon.files as files

def setup_local_test():
    """Configure environment (namely the root directory) for local execution."""
    util.copy_to_tmp('SwizzleInclude.cpp',
                     'SwizzleBefore.cpp',
                     'StudentMain.cpp',
                     'SwizzleAfter.cpp',
                     'Makefile')

def setup_remote():
    """Configure environment (namely the root directory) for remote execution."""
    util.move_sandbox_files_to_root('cpp', ['SwizzleInclude.cpp'])

def tear_down_local_test():
    """Tear down environment (namely the root directory) after local execution."""
    util.remove_files_from_root(['SwizzleInclude.cpp',
                                 'SwizzleBefore.cpp',
                                 'StudentMain.cpp',
                                 'SwizzleAfter.cpp',
                                 'SwizzledMain.cpp',
                                 'Makefile',
                                 'student_main'])

def pre_evaluate(for_submission=True):
    """
    Compile test/submit code.

    Args:
        for_submission (bool): Whether or not this is for submission or just test run.
        Submission will compile against submitMain.cpp, while testing compiles
        against testMain.cpp.
    """
    # call the compile shell script
    os.chmod('./compile.sh', '0755')
    util.run_program(['./compile.sh', for_submission],
                     '.tmp/compile-out.txt',
                     '.tmp/compile-err.txt')

def evaluate():
    """
    Actually run the compiled code.
    """
    util.run_program(['./main.o'], files.STUDENT_OUT, files.STUDENT_ERR)

def test(run_local):
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
    pre_evaluate(False)
    evaluate()

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

    # create script for running student's code + our testing code
    run_swizzled_bash = '#!/bin/bash\n' + bash_config + 'make submit; ./grader_main'
    with open('swizzled_runner.sh', 'w') as f:
        f.write(run_swizzled_bash)
    os.chmod('./swizzled_runner.sh', '0755')

    try:
        # generate swizzled main
        filenames = ['SwizzleInclude.cpp', 'SwizzleBefore.cpp', 'StudentMain.cpp', 'SwizzleAfter.cpp']
        errors = []
        with open('SwizzledMain.cpp', 'w') as outfile:
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
            util.run_program(['./swizzled_runner.sh'], files.RESULTS_OUT, files.RESULTS_ERR)
            # run student main (for extra debugging)
            util.run_program(['./student_runner.sh'], files.STUDENT_OUT, files.STUDENT_ERR)
    except:
        raise
    finally:
        os.remove('swizzled_runner.sh')
        os.remove('student_runner.sh')

    pre_evaluate(True)
    evaluate()

def submit_files():
    """Specifies a list of file paths to include in results when student submits quiz."""
    return ['StudentMain.cpp']

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
            additional feedback to either guide or congratulate the student
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
