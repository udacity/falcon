import pytest
import os

from falcon.environment import Environment

@pytest.fixture
def testEnvWithYamlFile():
    return Environment('test/falconf.yaml')

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

def test_can_load_from_local_falconf(testEnvWithNothing):
    # uses the sample falconf.yaml that's in the root
    assert testEnvWithNothing.test

def test_get_file_in_cwd(testEnvWithYamlFile):
    assert 'Falcon' in testEnvWithYamlFile.get_file_in_cwd('README.md')

def test_sets_falconf_directory(testEnvWithYamlFile):
    assert testEnvWithYamlFile.falconf_dir == os.path.join(os.getcwd(), 'test/')
