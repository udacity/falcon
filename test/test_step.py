import os
import pytest

from falcon.step import Step

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

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
    assert testStep.type == 'shell'

def test_set_failing_shell_command(testStep):
    testStep.set_shell_command('exit 1')
    out, err = testStep.run()
    assert '1' in err
    assert testStep.type == 'shell'

def test_chdir(testStep):
    def test():
        return [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    out = testStep.chdir('../../', test)
    assert 'README.md' in out

def test_set_shell_executable(testStep):
    filepath = os.path.join(os.getcwd(), 'sample_script.sh')
    # expects the full path
    testStep.set_shell_executable(filepath)
    out, err = testStep.run()
    assert 'testing!' in out
    assert testStep.type == 'executable'

def test_set_failing_shell_executable(testStep):
    filepath = os.path.join(os.getcwd(), 'sample_failing_script.sh')
    # expects the full path
    testStep.set_shell_executable(filepath)
    out, err = testStep.run()
    assert 'fail' in out
    assert '1' in err
    assert testStep.type == 'executable'

def test_set_noop(testStep):
    testStep.set_noop()
    out, err = testStep.run()
    assert out == ''
    assert testStep.type == 'noop'

def test_set_falcon_command(testStep):
    # TODO
    pass
