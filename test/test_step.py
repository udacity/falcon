import os
import pytest

from falcon.step import Step
from falcon.util import *

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

def test_set_falcon_command_concat(testStep):
    testStep.set_falcon_command('falcon.concat concat_test1 concat_test2 deleteme')
    testStep.run()
    with open('deleteme', 'r') as f:
        assert 'baby' in f.read()
    delete_files('deleteme')

def test_set_falcon_command_delete(testStep):
    filename = 'deleeeeeeteme'
    testStep.set_falcon_command('falcon.delete {}'.format(filename))
    with open(filename, 'w') as f:
        f.write('deleteeeee')
    testStep.run()
    assert not does_file_exist(filename)

def test_set_invalid_falcon_command(testStep):
    with pytest.raises(KeyError):
        testStep.set_falcon_command('falcon.bad_command')
