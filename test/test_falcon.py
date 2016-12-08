import pytest

from falcon.falcon import *

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

@pytest.fixture
def good_args():
    return {'config': 'falconf.yaml', 'mode': 'submit', 'debug': True}

@pytest.fixture
def good_falconf():
    return read_file('falconf.yaml')

@pytest.fixture
def good_env():
    return Environment()

def test_not_is_valid_falconf_specified_when_missing():
    assert not is_valid_falconf_specified()

def test_not_is_valid_falconf_specified_when_not_found():
    assert not is_valid_falconf_specified({'config': 'asdfasdfasdf'})

def test_is_valid_falconf_specified_when_exists():
    assert not is_valid_falconf_specified({'config': 'falcon.yaml'})

def test_is_valid_falconf_specified():
    assert not is_valid_falconf_specified()

# def test_fly(good_args, good_falconf, good_env):
#     flyer = fly(good_args, good_falconf, good_env)

def test_works_without_falconf_given():
    # we're in a directory with it
    assert main() == 0

def test_works_with_falconf():
    assert main(['-c', 'falconf.yaml']) == 0

def test_errs_if_no_falconf_found():
    # use the error thing
    with pytest.raises(SystemExit):
        main(['-c', 'notarealfile'])

# test all the args and their combos
# test formatting