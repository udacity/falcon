import pytest
import os

from udfalcon.environment import Environment

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

@pytest.fixture
def testEnvWithYamlFile():
    return Environment(falconf_path='falconf.yaml')

@pytest.fixture
def testEnvWithYamlString():
    return Environment(falconf_string="""
    test:
        env_vars:
            CAM: 'is cool'
    """)

@pytest.fixture
def testEnvWithNothing():
    return Environment()

def test_can_load_yaml_file(testEnvWithYamlFile):
    assert testEnvWithYamlFile.test

def test_can_parse_yaml_string(testEnvWithYamlString):
    assert testEnvWithYamlString.test['env_vars']['CAM'] == 'is cool'

def test_can_find_local_falconf(testEnvWithNothing):
    assert testEnvWithNothing.get_local_falconf()

def test_get_file_in_cwd(testEnvWithYamlFile):
    assert 'submit' in testEnvWithYamlFile.get_file_in_cwd('falconf.yaml')

def test_parse_falconf_mode(testEnvWithYamlFile):
    assert testEnvWithYamlFile.submit['tear_down'] == "echo 'tear_down'"
