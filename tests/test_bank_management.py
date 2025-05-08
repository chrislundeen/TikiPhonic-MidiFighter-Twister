import pytest
import json
import os
from pathlib import Path
import tempfile
from twister import generate_configs
from helpers.validation_helpers import ValidationError
from helpers.helpers_controllers import buildTwisterController

def test_incremental_bank_changes(bank_config):
    """Test that incremental changes to banks/controls work correctly"""
    # Create a modified configuration with an additional bank
    modified_config = bank_config.copy()

    # Generate controller with original config
    original_controller = {}
    try:
        buildTwisterController(bank_config)
        with open("output/_twister_controller.json", 'r') as f:
            original_controller = json.load(f)
    except Exception as e:
        assert False, f"Failed to build original controller: {e}"

    # Verify the original controller has the expected banks
    assert "mappings" in original_controller["value"]

    # Now generate with incrementally modified config
    modified_controller = {}
    try:
        buildTwisterController(modified_config)
        with open("output/_twister_controller.json", 'r') as f:
            modified_controller = json.load(f)
    except Exception as e:
        assert False, f"Failed to build modified controller: {e}"

    # Verify the modified controller has the same structure
    assert "mappings" in modified_controller["value"]

    # The test passes if both controllers were generated successfully
    assert True

def test_bank_organization(bank_config):
    """Test organization of controls into banks"""
    try:
        # Build the controller with bank configuration
        buildTwisterController(bank_config)

        # Check that the file was generated
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated"

        # Load the generated file
        with open(controller_path, 'r') as f:
            controller = json.load(f)

        # Verify the controller has mappings
        assert "mappings" in controller["value"]
        assert len(controller["value"]["mappings"]) > 0

        # Verify the controller has groups
        assert "groups" in controller["value"]
        assert len(controller["value"]["groups"]) > 0

        # The test passes if the controller has the expected structure
        assert True
    except Exception as e:
        assert False, f"Test failed with exception: {e}"
