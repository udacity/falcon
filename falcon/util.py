"""Utility functions used by Falcon."""

import os
import sys
import shutil
from subprocess import *

def run_program(args, out_path=None, err_path=None):
    """Run a command line program and pipe the stdout and stderr into files.

    Args:
        args (list): Program arguments.
        out_path (string): Path to file that will contain stdout.
        err_path (string): Path to file that will contain stderr.

    Raises:
        Any errors stemming from the exection of the program.
    """
    # if out_path and err_path are None, then run program and don't pipe output anywhere
    if out_path is None and err_path is None:
        try:
            program = Popen(args)
            out, err = program.communicate()
            if err:
                return err
            else:
                return out
        except Exception as runerr:
            print(str(runerr))
            raise
        else:
            return

    # otherwise, create path to files if doesnt exist
    if not os.path.exists(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))
    if not os.path.exists(os.path.dirname(err_path)):
        os.makedirs(os.path.dirname(err_path))

    # create files for piping stdout and stderr
    out_file = open(out_path, 'w+')
    err_file = open(err_path, 'w+')
    # run the program and pipe stdout and stderr into files
    try:
        program = Popen(args, stdout=out_file, stderr=err_file)
        out, err = program.communicate()
        if err:
            sys.stderr.write('failed ' + str(program.returncode) + ' ' + err)
            raise CalledProcessError
    # incase of error when invoking program, write error to stderr file
    except Exception as runerr:
        with open(err_path, 'w+') as err_file:
            err_file.write(str(runerr))
        raise
    # close files
    else:
        out_file.close()
        err_file.close()

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
        os.remove('./temp/' + text_file)

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
