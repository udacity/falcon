import pytest

from falcon.falcon import *

def chdir_sample_dir():
    if 'test/sample' not in os.getcwd():
        os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'test/sample/falconf.yaml'))) # done in main()

chdir_sample_dir()

def test_works_without_falconf_given():
    # we're in a directory with it
    assert main() == 0

def test_works_with_falconf():
    assert main(['-c', 'falconf.yaml']) == 0

def test_errs_if_no_falconf_found():
    # use the error thing
    with pytest.raises(SystemExit):
        main(['-c', 'notarealfile'])