import pytest

from falcon.step import Step

@pytest.fixture
def testStep():
    return Step()

def test_step_constructor_name():
    name = 'test'
    step = Step(name=name)
    assert step.name == name

def test_set_shell_command(testStep):
    testStep.set_shell_command('echo "hi"')
    out, err = testStep.run()
    assert 'hi' in out

def test_set_shell_executable(testStep):
    testStep.set_shell_executable('test/sample_script.sh')
    out, err = testStep.run()
    assert 'testing!' in out

def test_set_failing_shell_executable(testStep):
    testStep.set_shell_executable('test/sample_failing_script.sh')
    out, err = testStep.run()
    assert 'fail' in out
    assert '1' in err