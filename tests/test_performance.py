import time
import pytest
import json
import tempfile
from pathlib import Path
from twister import generate_configs
from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain

@pytest.mark.performance
def test_controller_builder_performance(config):
    """Test the performance of the controller builder"""
    # Measure time to build controller
    start_time = time.time()
    buildTwisterController(config)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"\nController builder took {execution_time:.3f} seconds")

    # Check that it completes in a reasonable time (less than 5 seconds)
    assert execution_time < 5.0

@pytest.mark.performance
def test_main_lua_builder_performance():
    """Test the performance of the main LUA builder"""
    # Measure time to build main LUA
    start_time = time.time()
    buildTwisterMain()
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"\nMain LUA builder took {execution_time:.3f} seconds")

    # Check that it completes in a reasonable time (less than 2 seconds)
    assert execution_time < 2.0

@pytest.mark.performance
def test_full_generation_performance(config):
    """Test the performance of the complete generation process"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary config file
        temp_config = Path(temp_dir) / "config.json"
        with open(temp_config, 'w') as f:
            json.dump(config, f)

        # Create a temporary output directory
        temp_output = Path(temp_dir) / "output"

        # Measure time for full generation
        start_time = time.time()
        generate_configs(config_path=str(temp_config), output_dir=str(temp_output))
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"\nFull generation took {execution_time:.3f} seconds")

        # Check that it completes in a reasonable time (less than a7 seconds)
        assert execution_time < 7.0
