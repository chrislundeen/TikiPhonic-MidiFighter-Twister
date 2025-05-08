import pytest
from jsonschema import validate, ValidationError

# Define the schema for config.json
CONFIG_SCHEMA = {
    "type": "object",
    "required": ["controller", "objects"],
    "properties": {
        "controller": {
            "type": "object",
            "required": ["version", "groups"],
            "properties": {
                "version": {"type": "string"},
                "groups": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "objects": {
            "type": "object",
            "required": ["controller", "group"],
            "properties": {
                "controller": {
                    "type": "object",
                    "required": ["kind", "version", "value"],
                    "properties": {
                        "kind": {"type": "string"},
                        "version": {"type": "string"},
                        "value": {
                            "type": "object",
                            "required": ["groups", "mappings", "customData"],
                            "properties": {
                                "groups": {"type": "array"},
                                "mappings": {"type": "array"},
                                "customData": {"type": "object"}
                            }
                        }
                    }
                },
                "group": {
                    "type": "object",
                    "required": ["id", "name"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"}
                    }
                }
            }
        }
    }
}

def test_config_schema(config):
    """Validate that config.json matches the expected schema"""
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Config validation failed: {e.message}\nAt path: {' -> '.join(str(x) for x in e.path)}")

def test_required_groups(config):
    """Test that config contains all required control groups"""
    required_groups = {"Buttons", "Encoders", "Push Encoders"}
    config_groups = set(config["controller"]["groups"])
    missing_groups = required_groups - config_groups
    assert not missing_groups, f"Missing required groups: {missing_groups}"

def test_controller_version(config):
    """Test that controller version is valid"""
    assert config["controller"]["version"], "Controller version must be specified"
    # Could add more specific version format validation if needed