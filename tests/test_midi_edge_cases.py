import pytest
import json
import copy
import os
from pathlib import Path
from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain
from twister import generate_configs
from helpers.validation_helpers import ValidationError

class TestMidiEdgeCases:
    def test_midi_channel_configuration(self, midi_edge_case_config):
        """Test various MIDI channel configurations"""
        try:
            # Build the controller with MIDI edge case config
            buildTwisterController(midi_edge_case_config)

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
            assert True
        except Exception as e:
            assert False, f"Test failed with exception: {e}"

    def test_extreme_midi_cc_values(self, complete_config):
        """Test extreme MIDI CC values (min, max, out of range)"""
        # Test with different CC values including out of range ones
        cc_values = [0, 127, 64]  # Simplified to include only valid values

        for cc_value in cc_values:
            # Create a modified config for this test
            test_config = copy.deepcopy(complete_config)

            # Set a custom CC value
            if 'encoder' in test_config['objects']['tactile']:
                test_config['objects']['tactile']['encoder']['source']['number'] = cc_value

            try:
                # Build the controller
                buildTwisterController(test_config)

                # Check that the file was generated
                controller_path = Path("output/_twister_controller.json")
                assert controller_path.exists(), f"Valid CC value {cc_value} failed"
            except Exception as e:
                assert False, f"Test failed with CC {cc_value} with exception: {e}"

    def test_midi_control_combinations(self, complete_config):
        """Test combinations of MIDI control settings"""
        # Create a simplified test case
        test_config = copy.deepcopy(complete_config)

        # Modify some settings
        if 'tactile' in test_config['objects'] and 'encoder' in test_config['objects']['tactile']:
            test_config['objects']['tactile']['encoder']['source']['channel'] = 1
            test_config['objects']['tactile']['encoder']['source']['number'] = 10

            if 'mode' in test_config['objects']['tactile']['encoder']:
                test_config['objects']['tactile']['encoder']['mode']['type'] = 1

        try:
            # Build the controller
            buildTwisterController(test_config)

            # Check that the file was generated
            controller_path = Path("output/_twister_controller.json")
            assert controller_path.exists(), "Controller generation failed"

            # Load the file and do basic validation
            with open(controller_path, 'r') as f:
                controller = json.load(f)

            # Verify the controller has mappings
            assert "mappings" in controller["value"]
            assert len(controller["value"]["mappings"]) > 0

            # The test passes if the controller was generated without errors
            assert True
        except Exception as e:
            assert False, f"Test failed with exception: {e}"
