import pytest

import io
import os
from contextlib import redirect_stderr
from contextlib import redirect_stdout

from falcon.environment import Environment
from falcon.flyer import Flyer
from falcon.step import Step

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
    submitFlyer.generate_output(step, msg)
    assert submitFlyer.outs[step] == msg

def test_out_displayed(debugFlyer):
    step = 'submitting'
    msg = '{"sample": "json"}'

    def make_output():
        debugFlyer.generate_output(step, msg)

    out = capture_stdout(make_output)
    assert msg in out

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
    assert falconfFlyer.get_default_file('asdfasdf') is None

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

def test_figure_out_right_action_python_file(falconfFlyer, capsys):
    # runs python main.py
    with capsys.disabled():
        step = falconfFlyer.create_step('main')
        step = falconfFlyer.figure_out_right_action(step)
        out, err = step.run()
        assert 'maining' in out

# test creating a temp directory and moving / symlinking files there?
# test symlinking libraries?