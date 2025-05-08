import os
import json
import pytest
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