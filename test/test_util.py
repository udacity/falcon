import pytest

import io
import os
from contextlib import redirect_stdout

from falcon.util import *

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

def test_read_file():
    contents = read_file('falconf.yaml')
    assert len(contents) > 0

def test_does_file_exist():
    falconf_exists = does_file_exist('falconf.yaml')
    no_such_file = does_file_exist('blahblah__.bar')
    assert falconf_exists
    assert not no_such_file

def test_find_in_abspath():
    filename = 'falconf.yaml'
    assert file_exists(filename, path=os.getcwd())

def test_get_file_with_basename():
    assert get_file_with_basename(os.getcwd(), 'falconf') == 'falconf.yaml'

def test_not_get_file_with_basename():
    assert get_file_with_basename(os.getcwd(), 'asdfasdfasdf') is None

def test_exists():
    assert exists('hello')
    def raises_error():
        raise Exception("uh oh!")
    assert not exists(raises_error)
    assert not exists(dictionary={}, key='thing')

def test_get_abspath():
    assert 'test/sample/' in get_abspath('falconf.yaml')

def test_run_shell_cmd():
    out, err = run_shell_cmd('echo "hi"')
    assert 'hi' in out

def test_run_shell_cmd_python():
    out, err = run_shell_cmd('python preprocess.py')
    assert 'preprocessing' in out

def test_run_failing_shell_cmd():
    out, err = run_shell_cmd('exit 1')
    assert '1' in err

def test_run_shell_executable():
    out, err = run_shell_executable(['./sample_script.sh'])
    assert 'testing!' in out

def test_run_failing_shell_script(capsys):
    with capsys.disabled():
        out, err = run_shell_executable(['./sample_failing_script.sh'])
        assert 'fail' in out
        assert '1' in err

def test_check_valid_shell_command():
    is_valid = check_valid_shell_command('echo')
    assert is_valid

def test_check_valid_shell_command_with_arg():
    is_valid = check_valid_shell_command(['echo', '"bar"'])
    assert is_valid

def test_not_check_valid_shell_command():
    is_valid = check_valid_shell_command('asdfasdfasdfasdfasdf')
    assert not is_valid

def test_generate_udacity_out():
    msg = 'tesssstttststststsasdfasdf'
    write_udacity_out(msg)
    assert msg in read_udacity_out()

def test_concat_files():
    filename = 'deleteme'
    concat_files('concat_test1', 'concat_test2', filename)
    with open(filename, 'r') as d:
        contents = d.read()
        assert 'baby' in contents and 'honey' in contents
    delete_files(filename)

def test_delete_files():
    filename = 'deleteme'
    with open(filename, 'w') as d:
        d.write(filename)
    delete_files(filename)
    assert not does_file_exist(filename)
