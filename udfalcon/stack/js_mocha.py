"""Functions for evaluating quizzes in Javascript using Mocha."""

import os
import json
import falcon.enum as enum
import falcon.util as util
import falcon.files as files

def setup_local_test():
    """Configure environment (namely the root directory) for local execution."""
    util.move_sandbox_files_to_root('js_mocha', ['SwizzleInclude.js', 'SwizzleBefore.js', 'StudentMain.js', 'SwizzleAfter.js'])

def setup_remote():
    """Configure environment (namely the root directory) for remote execution."""
    util.move_sandbox_files_to_root('js_mocha', ['SwizzleInclude.js'])

def tear_down_local_test():
    """Tear down environment (namely the root directory) after local execution."""
    util.remove_files_from_root(['SwizzleInclude.js', 'SwizzleBefore.js', 'StudentMain.js', 'SwizzleAfter.js', 'SwizzledMain.js'])

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
    # create script for execution
    if run_local:
        run_student_bash = '#!/bin/bash\n' + bash_config + 'node StudentMain.js'
    else:
        run_student_bash = '''#!/bin/bash
        export NVM_DIR=/usr/nvm
        source /opt/nvm/nvm.sh
        node StudentMain.js
        '''

    with open('student_runner.sh', 'w') as f:
        f.write(run_student_bash)
    os.chmod('./student_runner.sh', 0755)

    # run script
    try:
        util.run_program(['./student_runner.sh'], files.STUDENT_OUT, files.STUDENT_ERR)
    except:
        raise
    finally:
        os.remove('student_runner.sh')

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
    # create script for execution
    if run_local:
        run_student_bash = '#!/bin/bash\n' + bash_config + 'node StudentMain.js'
        run_swizzled_bash = '#!/bin/bash\n' + bash_config + 'mocha --reporter json SwizzledMain.js'
    else:
        run_student_bash = '''#!/bin/bash
        export NVM_DIR=/usr/nvm
        source /opt/nvm/nvm.sh
        node StudentMain.js
        '''
        run_swizzled_bash = """#!/bin/bash
        # Launches Mocha with the default NVM version of Node.js.
        export NVM_DIR=/usr/nvm
        . /opt/nvm/nvm.sh
        NODE_VERSION=$(nvm current)
        NODE_ROOT=${NVM_DIR}/versions/node/${NODE_VERSION}
        # Put global modules on the Node.js path
        export NODE_PATH=${NODE_ROOT}/lib/node_modules
        exec mocha --reporter json SwizzledMain.js
        """

    with open('student_runner.sh', 'w') as f:
        f.write(run_student_bash)
    os.chmod('./student_runner.sh', 0755)

    with open('swizzled_runner.sh', 'w') as f:
        f.write(run_swizzled_bash)
    os.chmod('./swizzled_runner.sh', 0755)

    # generate files, run scripts
    try:
        # generate swizzled main
        filenames = ['SwizzleInclude.js', 'SwizzleBefore.js', 'StudentMain.js', 'SwizzleAfter.js']
        errors = []
        with open('SwizzledMain.js', 'w') as outfile:
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

def submit_files():
    """Specifies a list of file paths to include in results when student submits quiz."""
    return ['StudentMain.js']

def transform(eval_output):
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
    lines = []
    try:
        grading_response = json.loads(eval_output)
    except:
        print "student-err.txt ==> " + util.get_file_contents(files.STUDENT_ERR)
        print "results-err.txt ==> " + util.get_file_contents(files.RESULTS_ERR)
        raise

    # loop through tests that failed
    for fails in grading_response['failures']:
        # remove expected statement added by chai on a failed assert
        fails['err']['message'] = fails['err']['message'].split(": expected", 1)[0]
        lines.append("<FAIL::>" + fails['err']['message'])

    # loop through tests that passed
    for good in grading_response['passes']:
        lines.append("<PASS::>" + good['fullTitle'])

    return '\n'.join(lines)
