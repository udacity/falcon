"""Utility functions used by Falcon."""

import io
import os
import re
import shutil
import stat
import sys
import subprocess
import tempfile

UD_TEMP_OUT = os.path.join(os.path.expanduser('~') + '/.ud_falcon_temp')

def eprint(*args, **kwargs):
    """
    Send errs to stderr.
    From: http://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
    """
    print(*args, file=sys.stderr, **kwargs)

def read_file(filepath):
    f = open(filepath, 'r')
    return f.read()

def does_file_exist(filepath):
    return os.path.isfile(filepath)

def does_something_exist(filepath):
    return os.path.exists(filepath)

def get_file_with_basename(path, basename):
    """
    Find a file where the basename (minus extension) matches the given basename in path.

    Args:
        path (string): Path to search.
        basename (string): Basename of the file (filename minus extension)

    Returns:
        string of filename (with extension) or None if nothing is found.
    """
    found_file = None

    for f in os.listdir(path):
        regex = '^{}\.\S+'.format(basename)
        filepath = os.path.join(path, f)
        if os.path.isfile(filepath) and re.match(regex, os.path.basename(f)):
            found_file = f
            break

    return found_file

def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def removedir(path):
    shutil.rmtree(path, ignore_errors=True)

def remove_symlink(path):
    try:
        os.remove(path)
    except:
        pass

def file_exists(filename, path=None):
    if path is not None:
        return does_file_exist(os.path.join(path, filename))
    else:
        return does_file_exist(filename)

def get_abspath(filepath):
    full_filepath = os.path.abspath(filepath)
    basename = os.path.basename(filepath)
    return full_filepath[:-(len(basename))]

def exists(thing=None, dictionary=None, key=None):
    """
    Figure out if something exists.

    Args:
        thing (any): Use by itself. Could be anything.
        dictionary (dict): Use with key.
        key (string): use with dictionary.
    """
    exists = False
    try:
        if callable(thing):
            thing()
            exists = True
        elif thing is None and dictionary is None:
            exists = False
        elif dictionary is not None and key is not None:
            dictionary[key]
            exists = True
        elif thing is not None:
            thing
            exists = True
    except:
        exists = False
    return exists

def run_shell_executable(args):
    """
    Run a command line program.

    Args:
        args (list): Program arguments.

    Returns:
        Tuple of strings: out, err
    """

    if does_file_exist(args[0]):
        os.chmod(args[0], stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    return call_subprocess(args)

def run_shell_cmd(cmd):
    """
    Run a command line program. HOLY CRAP YOU BETTER KNOW WHAT YOU'RE PUTTING IN HERE.

    Args:
        cmd (string): Shell command. THIS HAD BETTER NOT COME FROM STUDENTS!!!

    Returns:
        Tuple of strings: out, err
    """

    return call_subprocess(cmd, shell=True)

def call_subprocess(args, shell=False):
    """
    Run a subprocess.
    https://docs.python.org/3.5/library/subprocess.html#subprocess.run

    Args:
        args (string or list): Command to run.
        shell (bool): Whether or not to run the command through the shell.
    """
    out = None
    err = None
    # run the program and pipe stdout and stderr into files
    try:
        completedProcess = subprocess.Popen(args, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = completedProcess.communicate()
        if completedProcess.returncode != 0:
            err = '\n'.join(['return code: ' + str(completedProcess.returncode), err])
    except OSError as e:
        raise OSError('The file may not exist or you might have forgotten the #!', e)
    except ValueError as e:
        # bad args
        raise ValueError('Are these valid args? ' + ', '.join(args))
    except Exception as e:
        # something maybe wrong with the process? student code (or grading code) is bad
        raise e

    return out, err

def check_valid_shell_command(cmd):
    """
    Determine if a shell command returns a 0 error code.

    Args:
        cmd (string or list): Shell command. String of one command or list with arguments.

    Returns:
        bool
    """

    if isinstance(cmd, list):
        return shutil.which(cmd[0])
    else:
        return shutil.which(cmd)

def concat_files(*files):
    """
    Concat some files together.

    Args:
        *files: src1, src2, ..., srcN, dst.
    """
    dst_name = files[-1]
    sources = [files[f] for f in range(len(files)) if f < len(files) - 1]
    with open(dst_name, 'w') as dst:
        for f in sources:
            with open(f, 'r') as src:
                for line in src:
                    dst.write(line)

def delete_files(*files, rmdirs=False):
    """
    Delete some files. Deletes directories if rmdirs is true.

    Args:
        *files: filenames
        rmdir (boolean): Whether or not to remove directories too.
    """
    for f in files:
        try:
            os.remove(f)
        except OSError:
            if not rmdirs:
                raise Exception('{} is a directory. Cannot remove.'.format(f))
            else:
                os.rmdir(f)

def write_udacity_out(string):
    """
    Helper method to capture Udacity generated output. Generally use this to save grading code results. If used, the resulting file will be favored over main_out for creating student_out.

    USE OUTSIDE FALCON.

    Args:
        string (string): Write this string to a temp file.
    """
    with open(UD_TEMP_OUT, 'w') as f:
        f.write(string)
        TEMPFILE = f

def read_udacity_out():
    """
    Helper method to read the output of Udacity generated output (likely grading code results). Noop if you never called write_udacity_out(). Deletes the temp file after reading it.

    Returns:
        string (or None if nothing was written)
    """
    ret = None
    if does_file_exist(UD_TEMP_OUT):
        with open(UD_TEMP_OUT, 'r') as f:
            ret = f.read()
        os.remove(UD_TEMP_OUT)

    return ret
