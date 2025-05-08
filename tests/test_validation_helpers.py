import pytest
import json
import os
from pathlib import Path
from helpers.validation_helpers import validate_json_output, validate_lua_output, ValidationError, format_json_diff
from deepdiff import DeepDiff

def test_validate_json_output_identical():
    """Test validation of identical JSON output"""
    reference = {"key1": "value1", "key2": {"nested": "value2"}}
    generated = {"key1": "value1", "key2": {"nested": "value2"}}

    # Should not raise any error
    validate_json_output(generated, reference)

def test_validate_json_output_different_values():
    """Test validation with different values in JSON"""
    reference = {"key1": "value1", "key2": {"nested": "value2"}}
    generated = {"key1": "value1", "key2": {"nested": "different"}}

    with pytest.raises(ValidationError) as exc_info:
        validate_json_output(generated, reference)

    # Check that the error message contains the difference
    assert "Values that changed" in str(exc_info.value)
    assert "Expected: value2" in str(exc_info.value)
    assert "Got: different" in str(exc_info.value)

def test_validate_json_output_missing_items():
    """Test validation with missing items in JSON"""
    reference = {"key1": "value1", "key2": {"nested": "value2"}, "key3": "value3"}
    generated = {"key1": "value1", "key2": {"nested": "value2"}}

    with pytest.raises(ValidationError) as exc_info:
        validate_json_output(generated, reference)

    # Check that the error message contains the missing item
    assert "Missing items in generated file" in str(exc_info.value)
    assert "key3" in str(exc_info.value)

def test_validate_json_output_extra_items():
    """Test validation with extra items in JSON"""
    reference = {"key1": "value1", "key2": {"nested": "value2"}}
    generated = {"key1": "value1", "key2": {"nested": "value2"}, "extra": "value"}

    with pytest.raises(ValidationError) as exc_info:
        validate_json_output(generated, reference)

    # Check that the error message contains the extra item
    assert "Extra items in generated file" in str(exc_info.value)
    assert "extra" in str(exc_info.value)

def test_validate_lua_output_identical():
    """Test validation of identical Lua output"""
    reference = "function test()\n  return true\nend"
    generated = "function test()\n  return true\nend"

    # Should not raise any error
    validate_lua_output(generated, reference)

def test_validate_lua_output_different():
    """Test validation with different Lua"""
    reference = "function test()\n  return true\nend"
    generated = "function test()\n  return false\nend"

    with pytest.raises(ValidationError) as exc_info:
        validate_lua_output(generated, reference)

    # Check that the error message contains the difference
    assert "Line 2" in str(exc_info.value)
    assert "return true" in str(exc_info.value)
    assert "return false" in str(exc_info.value)

def test_format_json_diff():
    """Test formatting of JSON diff output"""
    diff = {
        'values_changed': {
            "root['key1']": {'old_value': 'old', 'new_value': 'new'}
        },
        'dictionary_item_added': ["root['extra']"],
        'dictionary_item_removed': ["root['missing']"]
    }

    result = format_json_diff(diff)

    # Check that the result contains formatted information
    assert "Values that changed:" in result
    assert "Expected: old" in result
    assert "Got: new" in result
    assert "Extra items in generated file:" in result
    assert "root['extra']" in result
    assert "Missing items in generated file:" in result
    assert "root['missing']" in result

def test_format_json_diff_empty():
    """Test formatting of empty diff"""
    diff = {}
    result = format_json_diff(diff)
    assert result == ""  # Should be empty string
