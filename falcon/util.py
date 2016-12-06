"""Utility functions used by Falcon."""

import io
import os
import stat
import sys
# import shutil
import subprocess

TESTING = False

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

def file_exists_in_abspath(path, filename):
    return does_file_exist(os.path.join(path, filename))

def exists(thing=None, dictionary=None, key=None):
    exists = False
    try:
        if callable(thing):
            thing()
        elif dictionary is not None and key is not None:
            dictionary[key]
        elif thing is not None:
            thing
        exists = True
    except:
        exists = False
    return exists

def run_program(args):
    """
    Run a command line program.

    Args:
        args (list): Program arguments.

    Returns:
        Tuple of strings: out, err
    """
    completedProcess = None
    error = None

    if does_file_exist(args[0]):
        os.chmod(args[0], stat.S_IEXEC)

    # run the program and pipe stdout and stderr into files
    try:
        completedProcess = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error = e
    except OSError as e:
        # file probably does not exist
        raise e
        # raise OSError('Is ' + args[0] + ' executable?')
    except ValueError:
        # bad args
        raise ValueError('Are these valid args? ' + ', '.join(args))
    except Exception as e:
        # something maybe wrong with the process? student code (or grading code) is bad
        raise e

    return completedProcess.stdout, completedProcess.stderr


def run_shell_cmd(cmd):
    """
    Run a command line program.

    Args:
        cmd (string): Shell command.

    Returns:
        Tuple of strings: out, err
    """
    completedProcess = None
    out = None
    err = None

    # run the program and pipe stdout and stderr into files
    try:
        # https://docs.python.org/3.5/library/subprocess.html#subprocess.run
        completedProcess = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out = completedProcess.stdout
        err = completedProcess.stderr
        completedProcess.check_returncode() # forces CalledProcessError if non-0 exit
    except subprocess.CalledProcessError as e:
        err = '\n'.join(['return code: ' + str(e.returncode), err, e.stderr])
    except OSError as e:
        raise e
    except ValueError as e:
        # bad args
        raise ValueError('Are these valid args? ' + ', '.join(args))
    except Exception as e:
        # something maybe wrong with the process? student code (or grading code) is bad
        raise e

    return out, err




# def get_file_contents(path):
#     """Returns the contents of a text file at a specified path.

#     Args:
#         path (string): Path to text file.

#     Returns:
#         If a file exists at the specified path, then the contents of the file
#         are returned. Otherwise, an empty string is returned.
#     """
#     if os.path.isfile(path):
#         with open(path, 'r') as file_handle:
#             file_content = file_handle.read()
#         return file_content
#     else:
#         return ''

# def add_file_contents_to_dictionary(path, dict):
#     """Add the contents of a file into a specified dictionary.

#     The newly added entry will use the file path as the key, and the value
#     will be the contents of the file at the file path.

#     Args:
#         dict (dict): Dictionary where file contents will be added.
#         path (string): Path to file contents.
#     """
#     # if file exists, open file and add contents to dictionary
#     if os.path.isfile(path):
#         with open(path, 'r') as file_handle:
#             file_content = file_handle.read()
#         dict[path] = file_content
#     else:
#         dict[path] = 'file does not exist'

# def remove_temp_text_files():
#     """Remove temporary text files from local temp directory."""
#     temp_text_files = [f for f in os.listdir('./temp') if f.endswith('.txt')]
#     for text_file in temp_text_files:
#         os.remove('./.tmp/' + text_file)

# def clear_temp():
#     """
#     Clears out the temporary directory.
#     """
#     folder = './.tmp'
#     for the_file in os.listdir(folder):
#         file_path = os.path.join(folder, the_file)
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             was_stderr(e)

# def copy_to_tmp(files):
#     """
#     Copy a file to the temporary directory that gets cleared out at the end of falcon.
#     Fails silently.

#     Args:
#         files (list of paths): Files to copy.
#     """
#     # TODO: could this be symlinked?
#     for filepath in files:
#         if os.path.isfile(filepath):
#             shutil.copyfile(filepath, os.path.join('./tmp/', os.path.basename(filepath)))

# def copy_dir_to_tmp(path):
#     """
#     Copy a whole directory to temporary. It'll get cleared out after the falcon run.

#     Args:
#         path (string): Path to directory
#     """
#     # TODO: could this be symlinked?
#     # check that the directory exists
#     # copy it
#     pass

# def move_sandbox_files_to_root(stack, files):
#     """Move files needed to execute source code to the root directory.

#     Args:
#         stack (string): Name of stack for sandbox files.
#         files (list): List of files in sandbox to move to root.
#     """
#     for filename in files:
#         if os.path.isfile('sandbox/' + stack + '/' + filename):
#             shutil.copyfile('sandbox/' + stack + '/' + filename, filename)

# def remove_files_from_root(files):
#     """Remove files needed to execute source code from the root directory.

#     Args:
#         stack (string): Name of stack for sandbox files.
#         files (list): List of files to remove from root.
#     """
#     for filename in files:
#         if os.path.isfile(filename):
#             os.remove(filename)
