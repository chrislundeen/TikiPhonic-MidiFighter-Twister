import pytest
import json
import os
from pathlib import Path
import shutil
import tempfile
from twister import load_config, ensure_output_dir, generate_configs, ConfigError
from helpers.validation_helpers import ValidationError

def test_load_config_valid():
    """Test loading valid configuration"""
    # Create a temporary valid config file
    valid_config = {
        "controller": {
            "version": "1.0.0",
            "groups": ["Group1", "Group2"]
        },
        "objects": {
            "controller": {
                "kind": "MainCompartment",
                "version": "1.0.0",
                "value": {
                    "groups": [],
                    "mappings": [],
                    "customData": {}
                }
            },
            "group": {
                "id": "test",
                "name": "test"
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(valid_config, f)
        temp_path = f.name

    try:
        # Test that the configuration loads correctly
        config = load_config(temp_path)
        assert config["controller"]["version"] == "1.0.0"
        assert "Group1" in config["controller"]["groups"]
    finally:
        # Clean up temporary file
        os.unlink(temp_path)

def test_load_config_invalid_json():
    """Test loading invalid JSON file"""
    # Create a temporary invalid JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"invalid": json}')
        temp_path = f.name

    try:
        # Test that loading invalid JSON raises error
        with pytest.raises(ValueError, match="Invalid JSON in config file"):
            load_config(temp_path)
    finally:
        # Clean up temporary file
        os.unlink(temp_path)

def test_load_config_missing_file():
    """Test loading non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_file.json")

def test_load_config_schema_validation():
    """Test schema validation on load"""
    # Create a temporary config file with schema errors
    invalid_config = {
        "controller": {
            # Missing required "version" field
            "groups": ["Group1"]
        },
        "objects": {
            "controller": {
                "kind": "MainCompartment",
                "version": "1.0.0",
                "value": {
                    "groups": [],
                    "mappings": [],
                    "customData": {}
                }
            },
            "group": {
                "id": "test",
                "name": "test"
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(invalid_config, f)
        temp_path = f.name

    try:
        # Test that schema validation fails
        with pytest.raises(ValidationError, match="Config validation failed"):
            load_config(temp_path)
    finally:
        # Clean up temporary file
        os.unlink(temp_path)

def test_ensure_output_dir():
    """Test output directory creation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up a temporary output path
        output_path = Path(temp_dir) / "test_output"

        # Test directory creation
        ensure_output_dir(str(output_path))

        # Verify directories were created
        assert output_path.exists()
        assert (output_path / "backup").exists()

        # Test idempotence (calling again shouldn't error)
        ensure_output_dir(str(output_path))
        assert output_path.exists()

def test_generate_configs_integration():
    """Test the full config generation process"""
    # This test is skipped because it requires a complete valid config with tactile templates
    # In a real test, we would either mock the dependencies or use a fixture with a complete config
    pytest.skip("Integration test requires complete valid config with tactile templates")
