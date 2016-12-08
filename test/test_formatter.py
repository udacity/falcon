import pytest
import io
from contextlib import contextmanager
from contextlib import redirect_stdout
import json

from falcon.environment import Environment
from falcon.flyer import Flyer
from falcon.formatter import Formatter

@pytest.fixture
def successfulFlyer():
    env = Environment('falconf.yaml')
    return Flyer(mode='test', env=env)

@pytest.fixture
def successfulFormat():
    env = Environment('falconf.yaml')
    flyer = Flyer(mode='test', env=env)
    return Formatter(flyer)

@pytest.fixture
def successfulDebugFormat():
    env = Environment('falconf.yaml')
    flyer = Flyer(mode='test', debug=True, env=env)
    return Formatter(flyer)

@pytest.fixture
def unsuccessfulDebugFormat():
    env = Environment('erring_falconf.yaml')
    flyer = Flyer(mode='test', debug=True, env=env)
    return Formatter(flyer)

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

def test_formatter_pipes_a_json_string_to_stdout(successfulFormat):
    out = capture_stdout(lambda : successfulFormat.pipe_to_stdout())
    assert isinstance(json.loads(out), dict)

def test_formatter_pulls_info_from_each_step(successfulFlyer):
    successfulFlyer.debug = True
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    result = formatter.get_step_result('preprocess', successfulFlyer)
    assert result['name'] == 'preprocess'
    assert result['type'] is 'executable'

def test_formatter_pulls_more_info_from_each_step_with_debug(successfulFlyer):
    successfulFlyer.debug = True
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    result = formatter.get_step_result('preprocess', successfulFlyer, True)
    assert 'preprocessing' in result['out']

def test_formatter_pulls_something_from_all_steps(successfulFlyer):
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    results = formatter.pull_each_step(successfulFlyer)
    assert len(results) == 5

def test_formatter_parses_each_step_from_flyer(successfulFlyer):
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    results = formatter.parse_steps(successfulFlyer)
    assert len(results) == 5
