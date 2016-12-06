import pytest

import io
import os
from contextlib import redirect_stderr
from contextlib import redirect_stdout

from falcon.util import *

def test_read_file():
    # lazily using the readme from home directory
    contents = read_file('README.md')
    assert len(contents) > 0

def test_does_file_exist():
    readme_exists = does_file_exist('README.md')
    no_such_file = does_file_exist('blahblah__.bar')
    assert readme_exists
    assert not no_such_file

def test_find_in_abspath():
    path = os.path.join(os.getcwd(), 'test')
    filename = 'README.md'
    assert file_exists_in_abspath(path, filename)

def test_exists():
    assert exists('hello')
    def raises_error():
        raise Exception("uh oh!")
    assert not exists(raises_error)
    assert not exists(dictionary={}, key='thing')

def test_run_shell_cmd():
    out, err = run_shell_cmd('echo "hi"')
    assert 'hi' in out

def test_run_failing_shell_cmd():
    out, err = run_shell_cmd('exit 1')
    assert '1' in err