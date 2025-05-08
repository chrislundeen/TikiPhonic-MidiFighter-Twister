import os
import json
import pytest
import copy
import shutil
from pathlib import Path

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "performance: mark test as a performance test")

@pytest.fixture
def config():
    """Load the configuration file"""
    config_path = "config/config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

@pytest.fixture
def output_dir():
    """Ensure output directory exists and return path"""
    output_path = Path("output")
    output_path.mkdir(exist_ok=True)
    return output_path

@pytest.fixture
def backup_files():
    """Get paths to reference backup files"""
    backup_dir = Path("output/backup")
    return {
        'controller': backup_dir / "_twister_controller.json",
        'main': backup_dir / "_twister_main.lua"
    }

@pytest.fixture(autouse=True)
def clean_output(output_dir):
    """Clean output files before each test"""
    # Remove only the generated files, not the backup directory
    files_to_clean = [
        output_dir / "_twister_controller.json",
        output_dir / "_twister_main.lua"
    ]
    for f in files_to_clean:
        if f.exists():
            f.unlink()

@pytest.fixture
def complete_config():
    """Create a complete configuration with all necessary templates for testing"""
    # Start with the real configuration
    config_path = "config/config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Make a deep copy to avoid modifying the original
    complete_config = copy.deepcopy(config)

    # The existing configuration already has the necessary template structure
    # We'll just ensure that it's complete for testing purposes

    # Make sure the tactile templates are complete
    tactile_templates = complete_config['objects']['tactile']
    if 'base' not in tactile_templates:
        tactile_templates['base'] = {
            "id": "",
            "name": "",
            "groupId": "",
            "source": {
                "channel": 0,
                "number": 0,
                "is14Bit": False
            },
            "mode": {
                "maxStepSize": 0.05,
                "minStepFactor": 1,
                "maxStepFactor": 1
            },
            "target": {
                "category": "virtual",
                "controlElementIndex": 0
            }
        }

    if 'button' not in tactile_templates:
        tactile_templates['button'] = {
            "source": {
                "channel": 1,
                "is14Bit": False
            }
        }

    if 'encoder' not in tactile_templates:
        tactile_templates['encoder'] = {
            "source": {"channel": 0},
            "mode": {"type": 3}
        }

    if 'pushencoder' not in tactile_templates:
        tactile_templates['pushencoder'] = {
            "source": {"channel": 4},
            "mode": {"type": 3}
        }

    # Make sure the projection templates are complete
    projection_templates = complete_config['objects']['projection']
    if 'base' not in projection_templates:
        projection_templates['base'] = {
            "id": "",
            "width": 0,
            "height": 0,
            "labelOne": {
                "angle": 0,
                "position": "aboveTop",
                "sizeConstrained": True
            },
            "mappings": [],
            "x": 0,
            "y": 0
        }

    if 'button' not in projection_templates:
        projection_templates['button'] = {
            "width": 130,
            "height": 40,
            "shape": "rectangle"
        }

    if 'encoder' not in projection_templates:
        projection_templates['encoder'] = {
            "width": 80,
            "height": 80,
            "shape": "circle"
        }

    if 'pushencoder' not in projection_templates:
        projection_templates['pushencoder'] = {
            "width": 80,
            "height": 80,
            "shape": "circle"
        }

    return complete_config

@pytest.fixture
def bank_config(complete_config):
    """Create a configuration with multiple banks for testing bank functionality"""
    # Make a copy of the complete config
    bank_config = copy.deepcopy(complete_config)

    # Ensure there are 4 banks defined
    if 'banks' not in bank_config['controller']:
        bank_config['controller']['banks'] = ["Bank 1", "Bank 2", "Bank 3", "Bank 4"]

    return bank_config

@pytest.fixture
def edge_case_config(complete_config):
    """Create a configuration with edge cases for testing edge case handling"""
    # Make a copy of the complete config
    edge_config = copy.deepcopy(complete_config)

    # Add some edge cases:
    # 1. Controls with special characters in the name
    if 'edge_cases' not in edge_config:
        edge_config['edge_cases'] = {}

    edge_config['edge_cases']['special_char_control'] = {
        "name": "Test & Special ! Characters @#$"
    }

    # 2. Control with very large values
    edge_config['edge_cases']['large_value_control'] = {
        "value": 999999999
    }

    # 3. Control with empty values
    edge_config['edge_cases']['empty_value_control'] = {
        "value": ""
    }

    return edge_config