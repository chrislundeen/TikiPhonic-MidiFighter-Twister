import pytest
import json
import os
from pathlib import Path
import tempfile
from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain
from twister import generate_configs
from helpers.validation_helpers import ValidationError
import copy

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

def test_midi_channel_edge_cases(midi_edge_case_config):
    """Test edge cases specific to MIDI channel configuration"""
    try:
        # Build the controller with MIDI edge case config
        buildTwisterController(midi_edge_case_config)

        # Check that the file was generated
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated"

        # Load the generated file
        with open(controller_path, 'r') as f:
            controller = json.load(f)

        # The test passes if the controller was generated without errors
        # even with MIDI-specific edge cases in the configuration
        assert True
    except Exception as e:
        assert False, f"Test failed with exception: {e}"

def test_midi_cc_number_range(complete_config):
    """Test different MIDI CC number ranges"""
    # Test with different CC values
    cc_values = [0, 1, 64, 127]

    for cc_value in cc_values:
        # Create a modified config for this test
        test_config = copy.deepcopy(complete_config)

        # Update the encoder CC number for this test
        test_config['objects']['tactile']['encoder']['source']['number'] = cc_value

        try:
            # Build the controller
            buildTwisterController(test_config)

            # Check that the file was generated
            controller_path = Path("output/_twister_controller.json")
            assert controller_path.exists(), f"Controller JSON was not generated for CC {cc_value}"

            # The test passes if the controller was generated without errors
            assert True
        except Exception as e:
            assert False, f"Test failed with CC {cc_value} with exception: {e}"

def test_controller_name_length_limits(complete_config):
    """Test varying lengths of controller names"""
    # Test with different name lengths
    test_names = [
        "",  # Empty name
        "A",  # One character
        "Test Controller",  # Normal name
        "A" * 50,  # Very long name
        "A" * 200,  # Extremely long name
        "Unicode 😀 🎹 🎵"  # Unicode characters
    ]

    for test_name in test_names:
        # Create a modified config for this test
        test_config = copy.deepcopy(complete_config)

        # Set a custom name for one of the groups
        if test_config['controller']['groups'] and len(test_config['controller']['groups']) > 0:
            test_config['controller']['groups'][0] = test_name

        try:
            # Build the controller
            buildTwisterController(test_config)

            # Check that the file was generated
            controller_path = Path("output/_twister_controller.json")
            assert controller_path.exists(), f"Controller JSON was not generated for name '{test_name}'"

            # The test passes if the controller was generated without errors
            assert True
        except Exception as e:
            assert False, f"Test failed with name '{test_name}' with exception: {e}"

def test_controller_with_invalid_projection(complete_config):
    """Test handling of invalid projection configuration"""
    # Create a modified config with projection issues
    test_config = copy.deepcopy(complete_config)

    # 1. Test with negative coordinates
    test_config['objects']['projection']['button']['width'] = -10
    test_config['objects']['projection']['button']['height'] = -20

    try:
        # Build the controller
        buildTwisterController(test_config)

        # We expect this to work (negative dimensions should be handled gracefully)
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated for negative dimensions"
    except Exception as e:
        # If this fails, it might be a legitimate validation error - we should check
        assert isinstance(e, ValidationError), f"Unexpected error type: {type(e).__name__}"

    # 2. Test with zero dimensions
    test_config = copy.deepcopy(complete_config)
    test_config['objects']['projection']['button']['width'] = 0
    test_config['objects']['projection']['button']['height'] = 0

    try:
        # Build the controller
        buildTwisterController(test_config)

        # Check that the file was generated
        controller_path = Path("output/_twister_controller.json")
        assert controller_path.exists(), "Controller JSON was not generated for zero dimensions"
    except Exception as e:
        # If this fails, it might be a legitimate validation error
        assert isinstance(e, ValidationError), f"Unexpected error type: {type(e).__name__}"

def test_controller_with_unusual_shapes(complete_config):
    """Test handling of unusual shape configurations"""
    # Create a modified config with unusual shape values
    test_config = copy.deepcopy(complete_config)

    # Test with different shape values
    shape_values = [
        "rectangle",  # Standard
        "circle",     # Standard
        "triangle",   # Unusual
        "hexagon",    # Unusual
        "",           # Empty
        "A" * 50      # Very long shape name
    ]

    for shape_value in shape_values:
        test_config = copy.deepcopy(complete_config)
        test_config['objects']['projection']['button']['shape'] = shape_value

        try:
            # Build the controller
            buildTwisterController(test_config)

            # Check that the file was generated
            controller_path = Path("output/_twister_controller.json")
            assert controller_path.exists(), f"Controller JSON was not generated for shape '{shape_value}'"

            # The test passes if the controller was generated without errors
            assert True
        except Exception as e:
            # Non-standard shapes might legitimately fail validation
            if shape_value not in ["rectangle", "circle"]:
                assert isinstance(e, ValidationError), f"Unexpected error type: {type(e).__name__}"
            else:
                assert False, f"Test failed with standard shape '{shape_value}' with exception: {e}"
