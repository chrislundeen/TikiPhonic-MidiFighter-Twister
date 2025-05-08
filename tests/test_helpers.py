import pytest
from helpers.helpers import setTabs
from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain

def test_set_tabs():
    """Test tab setting function"""
    assert setTabs(0) == ''
    assert setTabs(1) == '\t'
    assert setTabs(2) == '\t\t'
    assert setTabs(3) == '\t\t\t'

def test_build_twister_controller(config):
    """Test controller building"""
    # Just make sure this doesn't crash
    try:
        buildTwisterController(config)
        # If we get here with no exceptions, the test passes
        assert True
    except Exception as e:
        assert False, f"buildTwisterController raised exception: {e}"

def test_build_twister_main():
    """Test main Lua building"""
    # Just make sure this doesn't crash
    try:
        buildTwisterMain()
        # If we get here with no exceptions, the test passes
        assert True
    except Exception as e:
        assert False, f"buildTwisterMain raised exception: {e}"
