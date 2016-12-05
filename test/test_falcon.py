import pytest
from falcon.flyer import Flyer

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()