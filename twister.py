import json
import os
from pathlib import Path
from typing import Optional

from helpers.helpers_controllers import buildTwisterController
from helpers.helpers_main import buildTwisterMain
from helpers.validation_helpers import ValidationError
from jsonschema import validate
from tests.test_config_validation import CONFIG_SCHEMA

class ConfigError(Exception):
    """Base exception for configuration related errors"""
    pass

def ensure_output_dir(output_dir: str = "output") -> None:
    """Ensure output directory exists"""
    Path(output_dir).mkdir(exist_ok=True)
    backup_dir = Path(output_dir) / "backup"
    backup_dir.mkdir(exist_ok=True)

def validate_controller_version(config: dict) -> None:
    """Validate controller version separately from schema validation"""
    version = config.get("controller", {}).get("version")
    if not version:
        raise ValidationError("Controller version must be specified")

def load_config(config_path: str = "config/config.json") -> dict:
    """Load and validate configuration file"""
    try:
        with open(config_path) as configFile:
            try:
                config = json.load(configFile)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in config file")
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # First validate against schema
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
    except Exception as e:
        raise ValidationError(f"Config validation failed: {str(e)}")

    # Then validate controller version
    validate_controller_version(config)

    return config

def generate_configs(config_path: Optional[str] = None, output_dir: str = "output") -> None:
    """Generate both configuration files with error handling"""
    if config_path is None:
        config_path = "config/config.json"

    # Ensure output directory exists
    ensure_output_dir(output_dir)

    # Load and validate config
    config = load_config(config_path)

    try:
        # Generate controller configuration
        buildTwisterController(config)
        # Generate main configuration
        buildTwisterMain()
    except Exception as e:
        raise ConfigError(f"Error generating configurations: {str(e)}")

if __name__ == "__main__":
    try:
        generate_configs()
        print("Configuration files generated successfully")
    except (ConfigError, ValidationError, FileNotFoundError, ValueError) as e:
        print(f"Error: {str(e)}")
        exit(1)

