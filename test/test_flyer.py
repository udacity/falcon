import pytest

import io
import os
import sys
from contextlib import contextmanager
from contextlib import redirect_stdout

from udfalcon.environment import Environment
from udfalcon.flyer import Flyer
from udfalcon.step import Step
from udfalcon.util import *


# from: http://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
# because contextlib.redirect_stderr does not exist in python3.4, which is what the unsafers currently have
@contextmanager
def redirect_stderr(stream):
    old_stderr = sys.stderr
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stderr = old_stderr

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

@pytest.fixture
def testFlyer():
    return Flyer(mode='test')

@pytest.fixture
def submitFlyer():
    return Flyer(mode='submit')

@pytest.fixture
def debugFlyer():
    return Flyer(debug=True)

@pytest.fixture
def localFlyer():
    return Flyer(local=True)

@pytest.fixture
def falconfFlyer():
    env = Environment('falconf.yaml')
    flyer = Flyer(mode='test', env=env)
    return flyer

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

def test_constructs(testFlyer):
    assert testFlyer.mode == 'test'

def test_err_stored(testFlyer):
    step = 'testing'
    msg = 'testing!'
    makedir('.falcontmp') # used in the next few tests
    testFlyer.generate_err(step, Exception(msg))
    assert isinstance(testFlyer.errs[step], Exception)
    assert str(testFlyer.errs[step]) == msg

def test_err_displayed(debugFlyer):
    step = 'testing'
    msg = 'testing!'

    def make_an_err():
        debugFlyer.generate_err(step, Exception(msg))

    err = capture_stderr(Exception, make_an_err)
    assert msg in err

def test_out_stored(submitFlyer):
    step = 'submitting'
    msg = '{"sample": "json"}'
    submitFlyer.generate_out(step, msg)
    assert submitFlyer.outs[step] == msg

def test_out_displayed(debugFlyer):
    step = 'submitting'
    msg = '{"sample": "json"}'

    def make_output():
        debugFlyer.generate_out(step, msg)

    out = capture_stdout(make_output)
    assert msg in out

def test_out_saved_to_file(debugFlyer):
    step = 'submitting'
    msg = '{"sample": "json"}'

    def make_output():
        debugFlyer.generate_out(step, msg)

    with open('.falcontmp/submit_submitting_out.txt', 'r') as f:
        assert msg in f.read()

def test_err_saved_to_file(debugFlyer):
    step = 'testing'
    msg = 'testing!'

    def make_output():
        debugFlyer.generate_err(step, msg)

    with open('.falcontmp/submit_testing_err.txt', 'r') as f:
        assert msg in f.read()

def test_set_env_var(debugFlyer):
    key = 'TEST'
    value = 'VALUE'
    debugFlyer.set_env_var(key, value)
    assert os.getenv(key) == value

def test_set_env_vars(debugFlyer):
    evars = [{'key': 'value'}, {'key2': 'value2'}]
    debugFlyer.set_env_vars(evars)
    assert os.getenv('key') == 'value'
    assert os.getenv('key2') == 'value2'

def test_create_steps(debugFlyer):
    name = 'asdfasdfasdf'
    step = debugFlyer.create_step(name)
    assert isinstance(step, Step)
    assert step.name == name

def test_has_executable_file(debugFlyer):
    falconf = 'foo.py'
    is_specified = debugFlyer.has_executable_file(falconf)
    assert is_specified

def test_not_has_executable_file(debugFlyer):
    falconf = 'python foo.py'
    is_specified = debugFlyer.has_executable_file(falconf)
    assert not is_specified

def test_has_executable_with_args_specified(debugFlyer):
    falconf = 'foo.sh -a some -b args'
    is_specified = debugFlyer.has_executable_file(falconf)
    assert is_specified

def test_not_has_executable_file(debugFlyer):
    falconf = 'falcon.concat file1 file2'
    is_specified = debugFlyer.has_executable_file(falconf)
    assert not is_specified

def test_has_falcon_command(debugFlyer):
    falconf = 'falcon.concat file1 file2'
    is_specified = debugFlyer.has_falcon_command(falconf)
    assert is_specified

def test_not_has_falcon_command(debugFlyer):
    falconf = 'foo.falcon'
    is_specified = debugFlyer.has_falcon_command(falconf)
    assert not is_specified

def test_has_shell_command(debugFlyer):
    falconf = 'echo "tesssst"'
    is_specified = debugFlyer.has_shell_command(falconf)
    assert is_specified

def test_has_shell_command_python(debugFlyer):
    falconf = 'python foo.py'
    is_specified = debugFlyer.has_shell_command(falconf)
    assert is_specified

def test_not_has_shell_command(debugFlyer):
    falconf = 'boooooboboboboobaob "tesssst"'
    is_specified = debugFlyer.has_shell_command(falconf)
    assert not is_specified

def test_can_be_initialized_with_env():
    env = Environment('falconf.yaml')
    flyer = Flyer(env=env)
    assert 'test/sample' in flyer.falconf_dir

def test_get_default_file(falconfFlyer):
    # using test/sample/falconf.yaml
    assert 'preprocess.py' in falconfFlyer.get_default_file('preprocess')

def test_not_get_default_file(falconfFlyer):
    # using test/sample/falconf.yaml
    # currently running test mode. there's a submit_postprocess but not a test_postprocess
    assert falconfFlyer.get_default_file('postprocess') is None

def test_figure_out_right_action_default(falconfFlyer):
    # test: preprocess isn't actually in the falconf
    step = falconfFlyer.create_step('preprocess')
    step = falconfFlyer.figure_out_right_action(step)
    out, err = step.run()
    assert 'preprocessing' in out

def test_figure_out_right_action_shell_command(falconfFlyer):
    # runs echo 'postprocessing'
    step = falconfFlyer.create_step('postprocess')
    step = falconfFlyer.figure_out_right_action(step)
    out, err = step.run()
    assert 'postprocessing' in out

def test_figure_out_right_action_shell_executable(falconfFlyer):
    # runs a shell script
    step = falconfFlyer.create_step('tear_down')
    step = falconfFlyer.figure_out_right_action(step)
    out, err = step.run()
    assert 'tearing down' in out

def test_figure_out_right_action_python_file(falconfFlyer):
    # runs python main.py
    step = falconfFlyer.create_step('main')
    step = falconfFlyer.figure_out_right_action(step)
    out, err = step.run()
    assert 'maining' in out

def test_decide_to_noop(falconfFlyer):
    # compile isn't in the sample yaml
    step = falconfFlyer.create_step('compile')
    step = falconfFlyer.figure_out_right_action(step)
    assert step.type == 'noop'

def test_create_correct_sequence_len(falconfFlyer):
    falconfFlyer.create_sequence()
    assert len(falconfFlyer.sequence) == 5

def test_create_correct_sequence_order(falconfFlyer):
    falconfFlyer.create_sequence()
    seq = [step for step in falconfFlyer.sequence.values()]
    assert seq[0].name == 'preprocess'
    assert seq[1].name == 'compile'
    assert seq[2].name == 'main'
    assert seq[3].name == 'postprocess'
    assert seq[4].name == 'tear_down'

def test_symlinking_libraries():
    env = Environment(falconf_string="""
    test:
        libraries:
            - cpp
    """)
    flyer = Flyer(mode='test', env=env)
    flyer.symlink_libraries()
    assert does_file_exist('cpp/include/Grader.h')
    remove_symlink('cpp')