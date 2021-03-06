import pytest
import io
from contextlib import contextmanager
from contextlib import redirect_stdout
import json

from udfalcon.environment import Environment
from udfalcon.flyer import Flyer
from udfalcon.formatter import Formatter
from udfalcon.util import *

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

def test_formatter_pipes_a_json_string_to_stdout():
    env = Environment('falconf.yaml')
    flyer = Flyer(mode='test', env=env)
    formatter = Formatter(flyer)
    out = capture_stdout(lambda : formatter.pipe_to_stdout(flyer))
    assert isinstance(json.loads(out), dict)

def test_formatter_pulls_info_from_each_step(successfulFlyer):
    successfulFlyer.debug = True
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    result = formatter.get_step_result('preprocess', successfulFlyer)
    assert result['name'] == 'preprocess'
    assert result['type'] is 'executable'
    assert 'preprocessing' in result['out']
    assert result['elapsed_time'] > 0

def test_formatter_parses_each_step_from_flyer(successfulFlyer):
    successfulFlyer.create_sequence()
    successfulFlyer.run_sequence()
    formatter = Formatter()
    results = formatter.parse_steps(successfulFlyer)
    assert len(results) == 5

def test_get_student_out_finds_main_out_if_no_postprocess():
    env = Environment(falconf_string="""
    test:
        main: python testMain.py
    """)
    flyer = Flyer(mode='test', env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    formatter = Formatter(flyer)
    steps = formatter.parse_steps(flyer)
    assert 'student_outtttt' in formatter.get_student_out(flyer)

def test_get_student_out_finds_postprocess_out_if_postprocess():
    env = Environment(falconf_string="""
    test:
        main: python testMain.py
        postprocess: echo 'possssst'
    """)
    flyer = Flyer(mode='test', env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    formatter = Formatter(flyer)
    steps = formatter.parse_steps(flyer)
    assert 'possssst' in formatter.get_student_out(flyer)

def test_get_student_out_finds_udacity_out_if_no_postprocess():
    env = Environment(falconf_string="""
    test:
        main: python testMain.py
    """)
    msg = 'this is a message'
    flyer = Flyer(mode='test', env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    formatter = Formatter(flyer)
    steps = formatter.parse_steps(flyer)
    write_udacity_out(msg)
    assert msg in formatter.get_student_out(flyer)

def test_get_is_correct_is_none_if_no_tag():
    env = Environment(falconf_string="""
    test:
        main: python testMain.py
    """)
    flyer = Flyer(mode='test', env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    formatter = Formatter(flyer)
    steps = formatter.parse_steps(flyer)
    student_out = formatter.get_student_out(flyer)
    assert formatter.get_is_correct(student_out) is None

def test_get_is_correct_is_false_if_fail_tag():
    # manually passes in output
    env = Environment(falconf_string="""
    test:
        main: echo '<::FAIL>'
    """)
    flyer = Flyer(mode='test', env=env)
    flyer.create_sequence()
    flyer.run_sequence()
    formatter = Formatter(flyer)
    steps = formatter.parse_steps(flyer)
    student_out = formatter.get_student_out(flyer)
    assert not formatter.get_is_correct(student_out)

def test_get_is_correct_is_true_if_pass_tag():
    # output pulled from udacity_out file
    msg = '<::PASS>'
    write_udacity_out(msg)
    formatter = Formatter()
    assert formatter.get_is_correct()
