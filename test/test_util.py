import pytest

import io
from contextlib import redirect_stderr
from contextlib import redirect_stdout

from falcon.util import exists, read_file

def test_read_file():
    # lazily using the readme from home directory
    contents = read_file('README.md')
    assert len(contents) > 0

def test_exists():
    assert exists('hello')
    def raises_error():
        raise Exception("uh oh!")
    assert not exists(raises_error)
    assert not exists(dictionary={}, key='thing')