import pytest

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

def test_can_load_yaml_file(testEnvWithYamlFile):
    assert testEnvWithYamlFile.test

def test_can_parse_yaml_string(testEnvWithYamlString):
    assert testEnvWithYamlString.test['env_vars']['CAM'] == 'is cool'