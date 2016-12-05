"""Utility functions used by Falcon."""

import os
import sys
import shutil
from subprocess import Popen, CalledProcessError, check_call

TESTING = False

def set_testing(testing):
    """
    Do you want to see errors raised or just pipe them to files? Should be True
    while you're debugging / building a quiz and False in produciton.

    Args:
        testing (bool): Well? Are you testing?
    """
    TESTING = testing

def handle_output(out, err, out_path=None, err_path=None):
    """
    Student code just ran. This takes care of the output.
    """
    was_stdout(out, out_path)
    was_stderr(err, err_path)

def was_stderr(err, err_path=None):
    """
    Handle stderr from any point in the execution of student code.

    Args:
        err (Exception): The thing that went wrong.
        err_path (string): Where to pipe the output
    """
    if TESTING:
        sys.stderr.write(err)
        if err.child_traceback:
            sys.stderr.write(err.child_traceback)
    if err_path is not None:
        with open(err_path, 'w+') as err_path:
            err_path.write(str(err))

def was_stdout(out, out_path=None):
    """
    Handle stdout from any point in the execution of student code.

    Args:
        out (string): The output!
        out_path (string): Where to pipe the output.
    """
    if TESTING:
        print(out)
    if out_path is not None:
        with open(out_path, 'w+') as out_file:
            out_file.write(str(out))

def run_program(args, out_path=None, err_path=None):
    """Run a command line program and pipe the stdout and stderr into files.

    Args:
        args (list): Program arguments.
        out_path (string): Path to file that will contain stdout.
        err_path (string): Path to file that will contain stderr.
        testing (bool): If True, show output and errors for debugging as well.

    Returns:
        Bool. False if any errors occured during execution.
    """
    ret_status = False
    out_file = None
    err_file = None

    # create path to files if they don't exist
    if out_path is not None:
        if not os.path.exists(os.path.dirname(out_path)):
            os.makedirs(os.path.dirname(out_path))
        out_file = open(out_path, 'w+')

    if err_path is not None:
        if not os.path.exists(os.path.dirname(err_path)):
            os.makedirs(os.path.dirname(err_path))
        err_file = open(err_path, 'w+')

    # run the program and pipe stdout and stderr into files
    try:
        program = Popen(args, stdout=out_file, stderr=err_file)
        out, err = program.communicate()
        handle_output(out, err, out_file, err_file)
    except OSError:
        # file probably does not exist
        raise OSError('Is ' + args[0] + ' executable?')
    except ValueError:
        # bad args
        raise ValueError('Are these valid args? ' + ', '.join(args))
    except Exception as e:
        # something maybe wrong with the process? student code (or grading code) is bad
        was_stderr(e, err_path)

    if out_file is not None:
        out_file.close()
    if err_file is not None:
        err_path.close()

    return ret_status

def get_file_contents(path):
    """Returns the contents of a text file at a specified path.

    Args:
        path (string): Path to text file.

    Returns:
        If a file exists at the specified path, then the contents of the file
        are returned. Otherwise, an empty string is returned.
    """
    if os.path.isfile(path):
        with open(path, 'r') as file_handle:
            file_content = file_handle.read()
        return file_content
    else:
        return ''

def add_file_contents_to_dictionary(path, dict):
    """Add the contents of a file into a specified dictionary.

    The newly added entry will use the file path as the key, and the value
    will be the contents of the file at the file path.

    Args:
        dict (dict): Dictionary where file contents will be added.
        path (string): Path to file contents.
    """
    # if file exists, open file and add contents to dictionary
    if os.path.isfile(path):
        with open(path, 'r') as file_handle:
            file_content = file_handle.read()
        dict[path] = file_content
    else:
        dict[path] = 'file does not exist'

def remove_temp_text_files():
    """Remove temporary text files from local temp directory."""
    temp_text_files = [f for f in os.listdir('./temp') if f.endswith('.txt')]
    for text_file in temp_text_files:
        os.remove('./.tmp/' + text_file)

def clear_temp():
    """
    Clears out the temporary directory.
    """
    folder = './.tmp'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            was_stderr(e)

def copy_to_tmp(files):
    """
    Copy a file to the temporary directory that gets cleared out at the end of falcon.
    Fails silently.

    Args:
        files (list of paths): Files to copy.
    """
    # TODO: could this be symlinked?
    for filepath in files:
        if os.path.isfile(filepath):
            shutil.copyfile(filepath, os.path.join('./tmp/', os.path.basename(filepath)))

def copy_dir_to_tmp(path):
    """
    Copy a whole directory to temporary. It'll get cleared out after the falcon run.

    Args:
        path (string): Path to directory
    """
    # TODO: could this be symlinked?
    # check that the directory exists
    # copy it
    pass

def move_sandbox_files_to_root(stack, files):
    """Move files needed to execute source code to the root directory.

    Args:
        stack (string): Name of stack for sandbox files.
        files (list): List of files in sandbox to move to root.
    """
    for filename in files:
        if os.path.isfile('sandbox/' + stack + '/' + filename):
            shutil.copyfile('sandbox/' + stack + '/' + filename, filename)

def remove_files_from_root(files):
    """Remove files needed to execute source code from the root directory.

    Args:
        stack (string): Name of stack for sandbox files.
        files (list): List of files to remove from root.
    """
    for filename in files:
        if os.path.isfile(filename):
            os.remove(filename)
