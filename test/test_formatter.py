import pytest
import json

from falcon.environment import Environment
from falcon.flyer import Flyer
from falcon.formatter import Formatter

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

def test_formatter_creates_a_json_string(successfulFormat):
    ex = successfulFormat.json()
    assert isinstance(json.loads(ex), dict)