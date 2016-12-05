import pytest

import io
from contextlib import redirect_stderr
from contextlib import redirect_stdout

from falcon.flyer import Flyer

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

def capture_stderr(exceptionType, func):
    f = io.StringIO()
    with redirect_stderr(f), pytest.raises(exceptionType):
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
    submitFlyer.generate_out(step, msg)
    assert submitFlyer.outs[step] == msg