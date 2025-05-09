"""
Optimized deep copy utility for the MidiFighter Twister Configuration Generator.
This module provides alternatives to copy.deepcopy for specific use cases to improve performance.
"""

from typing import Dict, Any, TypeVar, List, Optional

T = TypeVar('T')

def shallow_copy_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a shallow copy of a dictionary. This is much faster than a deep copy
    when you know the dictionary contains only immutable values.

    Args:
        d: The dictionary to copy

    Returns:
        A new dictionary with the same keys and values
    """
    return {k: v for k, v in d.items()}

def optimized_deep_copy_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a deep copy of a dictionary, optimized for dictionaries with simple values.
    This is faster than copy.deepcopy for dictionaries with strings, numbers, and nested dictionaries.

    Args:
        d: The dictionary to copy

    Returns:
        A deep copy of the dictionary
    """
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = optimized_deep_copy_dict(v)
        elif isinstance(v, list):
            result[k] = [
                optimized_deep_copy_dict(x) if isinstance(x, dict)
                else x[:] if isinstance(x, list)
                else x for x in v
            ]
        else:
            # Immutable types (str, int, float, bool, etc.) can be assigned directly
            result[k] = v
    return result

def optimized_list_append(target_list: List[T], template: T, **kwargs) -> None:
    """
    Efficiently append a copy of a template object to a list with modifications.
    This avoids a full deep copy when only a few fields need to be changed.

    Args:
        target_list: The list to append to
        template: The template object to copy and modify
        **kwargs: Key-value pairs to modify in the copied object
    """
    if isinstance(template, dict):
        # Create a new dictionary based on the template with modifications
        new_item = optimized_deep_copy_dict(template)
        # Apply modifications
        for k, v in kwargs.items():
            if '.' in k:
                # Handle nested keys like 'source.number'
                parts = k.split('.')
                current = new_item
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = v
            else:
                new_item[k] = v
        target_list.append(new_item)
    else:
        # For non-dict types, fallback to the standard approach
        import copy
        new_item = copy.deepcopy(template)
        # Apply modifications (assuming object with attributes)
        for k, v in kwargs.items():
            setattr(new_item, k, v)
        target_list.append(new_item)
