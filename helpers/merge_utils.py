"""
Utilities for merging JSON objects.
This module provides a replacement for jsonmerge to avoid deprecation warnings.
"""
import copy
from typing import Any, Dict

def deep_merge(base: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges two dictionaries recursively.

    Args:
        base: The base dictionary to merge into
        schema: The dictionary with values to merge into the base

    Returns:
        A new dictionary containing the merged result
    """
    # Create a deep copy of the base to avoid modifying the original
    merged = copy.deepcopy(base)

    # Recursively merge schema into the merged dictionary
    for key, value in schema.items():
        # If both dictionaries have the same key and both values are dicts, merge recursively
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            # Otherwise, just update the value
            merged[key] = copy.deepcopy(value)

    return merged
