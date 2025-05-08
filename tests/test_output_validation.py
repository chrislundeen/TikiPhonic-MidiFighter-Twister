import os
import json
import pytest
from pathlib import Path
from twister import buildTwisterController, buildTwisterMain
from helpers.validation_helpers import validate_json_output, validate_lua_output, ValidationError

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_lua_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def test_controller_json_output(config, output_dir, backup_files):
    """Test that generated controller JSON matches reference"""
    # Generate fresh output
    buildTwisterController(config)

    generated_path = output_dir / "_twister_controller.json"
    assert generated_path.exists(), "Controller JSON was not generated"

    generated = load_json_file(generated_path)
    reference = load_json_file(backup_files['controller'])
    validate_json_output(generated, reference)

def test_main_lua_output(config, output_dir, backup_files):
    """Test that generated Lua file matches reference"""
    # Generate fresh output
    buildTwisterMain()

    generated_path = output_dir / "_twister_main.lua"
    assert generated_path.exists(), "Main Lua file was not generated"

    generated = load_lua_file(generated_path)
    reference = load_lua_file(backup_files['main'])
    validate_lua_output(generated, reference)

def test_full_generation(config, output_dir, backup_files):
    """Test complete generation process matches reference files"""
    # Generate both files
    buildTwisterController(config)
    buildTwisterMain()

    # Check both files exist and match references
    controller_path = output_dir / "_twister_controller.json"
    main_path = output_dir / "_twister_main.lua"

    assert controller_path.exists(), "Controller JSON was not generated"
    assert main_path.exists(), "Main Lua file was not generated"

    # Validate controller JSON
    generated_controller = load_json_file(controller_path)
    reference_controller = load_json_file(backup_files['controller'])
    validate_json_output(generated_controller, reference_controller)

    # Validate main Lua
    generated_main = load_lua_file(main_path)
    reference_main = load_lua_file(backup_files['main'])
    validate_lua_output(generated_main, reference_main)