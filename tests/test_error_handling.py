import pytest
import json
import copy
from pathlib import Path
from twister import generate_configs
from helpers.validation_helpers import ValidationError

# Minimal valid config template for testing
VALID_CONFIG = {
    "controller": {
        "version": "1.0.0",
        "groups": ["Buttons", "Encoders", "Push Encoders"]
    },
    "objects": {
        "controller": {
            "kind": "MainCompartment",
            "version": "1.0.0",
            "value": {
                "groups": [],
                "mappings": [],
                "customData": {
                    "companion": {
                        "controls": []
                    }
                }
            }
        },
        "group": {
            "id": "test",
            "name": "test"
        },
        "tactile": {
            "base": {
                "kind": "Virtual",
                "source": {
                    "kind": "Virtual",
                    "id": 0,
                    "channel": 0
                },
                "target": {
                    "kind": "FxParameterValue",
                    "parameter": {
                        "address": "ById",
                        "fx": {
                            "address": "ByName",
                            "chain": {
                                "address": "Track",
                                "track": {
                                    "address": "Selected"
                                }
                            },
                            "name": "VST3: Guitar Rig 6 (Native Instruments)"
                        },
                        "index": 0
                    }
                }
            },
            "button": {
                "kind": "Virtual",
                "source": {
                    "kind": "Virtual",
                    "id": 0,
                    "channel": 0
                },
                "target": {
                    "kind": "FxParameterValue",
                    "parameter": {
                        "address": "ById",
                        "fx": {
                            "address": "ByName",
                            "chain": {
                                "address": "Track",
                                "track": {
                                    "address": "Selected"
                                }
                            },
                            "name": "VST3: Guitar Rig 6 (Native Instruments)"
                        },
                        "index": 0
                    }
                },
                "glue": {
                    "absolute_mode": "ToggleButton",
                    "step_size_interval": [0.01, 0.05]
                }
            },
            "encoder": {
                "kind": "Virtual",
                "source": {
                    "kind": "Virtual",
                    "id": 0,
                    "channel": 0
                },
                "target": {
                    "kind": "FxParameterValue",
                    "parameter": {
                        "address": "ById",
                        "fx": {
                            "address": "ByName",
                            "chain": {
                                "address": "Track",
                                "track": {
                                    "address": "Selected"
                                }
                            },
                            "name": "VST3: Guitar Rig 6 (Native Instruments)"
                        },
                        "index": 0
                    }
                }
            },
            "pushencoder": {
                "kind": "Virtual",
                "source": {
                    "kind": "Virtual",
                    "id": 0,
                    "channel": 0
                },
                "target": {
                    "kind": "FxParameterValue",
                    "parameter": {
                        "address": "ById",
                        "fx": {
                            "address": "ByName",
                            "chain": {
                                "address": "Track",
                                "track": {
                                    "address": "Selected"
                                }
                            },
                            "name": "VST3: Guitar Rig 6 (Native Instruments)"
                        },
                        "index": 0
                    }
                }
            }
        },
        "projection": {
            "base": {
                "id": "",
                "height": 40,
                "width": 40,
                "shape": "circle",
                "x": 0,
                "y": 0,
                "mappings": [],
                "labelOne": {
                    "angle": 0,
                    "position": "aboveTop",
                    "sizeConstrained": True
                }
            },
            "button": {
                "shape": "rectangle",
                "width": 130,
                "height": 40,
                "mappings": []
            },
            "encoder": {
                "shape": "circle",
                "width": 80,
                "height": 80,
                "mappings": []
            },
            "pushencoder": {
                "shape": "circle",
                "width": 80,
                "height": 80,
                "mappings": []
            }
        }
    }
}

def test_missing_config_file(tmp_path):
    """Test handling of missing config file"""
    with pytest.raises(FileNotFoundError) as exc_info:
        config_path = tmp_path / "nonexistent_config.json"
        generate_configs(config_path=str(config_path))
    assert "Config file not found" in str(exc_info.value)

def test_invalid_config_json(tmp_path):
    """Test handling of malformed JSON in config"""
    config_path = tmp_path / "invalid_config.json"
    config_path.write_text("{invalid json")

    with pytest.raises(ValueError) as exc_info:
        generate_configs(config_path=str(config_path))
    assert "Invalid JSON in config file" in str(exc_info.value)

def test_missing_required_fields(tmp_path):
    """Test handling of config missing required fields"""
    config_path = tmp_path / "incomplete_config.json"
    config_path.write_text('{"controller": {}}')

    with pytest.raises(ValidationError) as exc_info:
        generate_configs(config_path=str(config_path))
    assert "Config validation failed" in str(exc_info.value)
    assert "'objects' is a required property" in str(exc_info.value)

def test_invalid_controller_version(tmp_path):
    """Test handling of invalid controller version"""
    config = copy.deepcopy(VALID_CONFIG)
    config["controller"]["version"] = ""

    config_path = tmp_path / "invalid_version.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)

    # The test should catch "ValidationError" with message about controller version
    with pytest.raises(ValidationError) as exc_info:
        generate_configs(config_path=str(config_path))

    error_msg = str(exc_info.value)
    # The validation happens in load_config after schema validation
    assert "Controller version must be specified" in error_msg

def test_output_dir_creation(tmp_path):
    """Test that output directory is created if it doesn't exist"""
    output_dir = tmp_path / "output"
    assert not output_dir.exists()

    # Create config with valid template
    config_path = tmp_path / "config.json"
    config = copy.deepcopy(VALID_CONFIG)
    with open(config_path, 'w') as f:
        json.dump(config, f)

    # Generate configs with custom output dir
    generate_configs(config_path=str(config_path), output_dir=str(output_dir))

    assert output_dir.exists()
    assert output_dir.is_dir()
    assert (output_dir / "backup").exists()