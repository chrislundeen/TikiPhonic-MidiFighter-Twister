import pytest
import json
import os
from pathlib import Path
import tempfile
from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain
from twister import generate_configs
from helpers.validation_helpers import ValidationError

def test_controller_with_all_control_types(complete_config):
    """Test that all control types can be generated correctly"""
    try:
        # Build the controller with complete config
        buildTwisterController(complete_config)

        # Check that the file was generated
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated"

        # Load the generated file
        with open(controller_path, 'r') as f:
            controller = json.load(f)

        # Verify the controller has mappings
        assert "mappings" in controller["value"]
        assert len(controller["value"]["mappings"]) > 0

        # Check for different control types in the mappings
        control_types = set()
        for mapping in controller["value"]["mappings"]:
            if "id" in mapping:
                # Extract the control type from the ID (e.g., "Button0", "Encoder1")
                control_type = ''.join([c for c in mapping["id"] if not c.isdigit()])
                control_types.add(control_type)

        # Verify we have at least these control types
        expected_types = {"Button", "Encoder", "PushEncoder"}
        for expected_type in expected_types:
            assert expected_type in control_types, f"Missing control type: {expected_type}"

        # The test passes if all control types were generated
        assert True
    except Exception as e:
        assert False, f"Test failed with exception: {e}"

def test_controller_with_edge_cases(edge_case_config):
    """Test edge cases in control configuration"""
    try:
        # Build the controller with edge case config
        buildTwisterController(edge_case_config)

        # Check that the file was generated
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated"

        # Load the generated file
        with open(controller_path, 'r') as f:
            controller = json.load(f)

        # Verify the controller has mappings
        assert "mappings" in controller["value"]
        assert len(controller["value"]["mappings"]) > 0

        # The test passes if the controller was generated without errors
        # even with edge cases in the configuration
        assert True
    except Exception as e:
        assert False, f"Test failed with exception: {e}"
