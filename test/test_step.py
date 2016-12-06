import pytest

from falcon.step import Step
from falcon.flyer import Flyer

@pytest.fixture
def testStep():
    return Step()

def test_step_constructor_name():
    name = 'test'
    step = Step(name=name)
    assert step.name == name

def test_set_shell_command():
    step = Step()
    step.set_shell_command('echo "hi"')
    out, err = step.run()
    assert 'hi' in out