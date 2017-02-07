import pytest
from contextlib import contextmanager
from contextlib import redirect_stdout

from udfalcon.falcon import *

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

def capture_stderr(exceptionType, func):
    f = io.StringIO()
    with redirect_stderr(f), pytest.raises(exceptionType):
        func()
    return f.getvalue()

def capture_stdout(func):
    f = io.StringIO()
    with redirect_stdout(f):
        func()
    return f.getvalue()

@pytest.fixture
def good_args():
    return {'config': 'falconf.yaml', 'mode': 'submit', 'debug': True}

@pytest.fixture
def good_falconf():
    return read_file('falconf.yaml')

@pytest.fixture
def good_env():
    return Environment()

def test_not_is_valid_falconf_specified_when_missing():
    assert not is_valid_falconf_specified()

def test_not_is_valid_falconf_specified_when_not_found():
    assert not is_valid_falconf_specified({'config': 'asdfasdfasdf'})

def test_is_valid_falconf_specified_when_exists():
    assert not is_valid_falconf_specified({'config': 'falcon.yaml'})

def test_is_valid_falconf_specified():
    assert not is_valid_falconf_specified()

# def test_fly(good_args, good_falconf, good_env):
#     flyer = fly(good_args, good_falconf, good_env)

def test_works_without_falconf_given():
    # we're in a directory with it
    assert main() == 0

def test_works_with_falconf():
    # assert main(['-c', 'falconf.yaml']) == 0
    assert main({'config': 'falconf.yaml'}) == 0

def test_outputs_formatted_results(capsys):
    # the string 'Executing `' starts every command's output
    out = capture_stdout(lambda : main({'output': 'formatted'}))
    assert 'Executing `' in out

def test_outpust_clean_results():
    # this will break if the sample steps are ever changed.
    out = capture_stdout(lambda : main({'output': 'clean'}))
    assert 'preprocess\ncompile\nmain' in out

def test_outputs_return_results():
    assert isinstance(main({'output': 'return', 'mode': 'test'}), dict)
