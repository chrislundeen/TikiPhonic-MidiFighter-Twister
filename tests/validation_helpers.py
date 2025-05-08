import json
from typing import Dict, Any
from deepdiff import DeepDiff

class ValidationError(Exception):
    pass

def format_json_diff(diff: Dict[str, Any]) -> str:
    """Format DeepDiff output into readable error message"""
    messages = []

    if diff.get('values_changed'):
        messages.append("\nValues that changed:")
        for path, change in diff['values_changed'].items():
            messages.append(f"  {path}:")
            messages.append(f"    Expected: {change['old_value']}")
            messages.append(f"    Got: {change['new_value']}")

    if diff.get('dictionary_item_added'):
        messages.append("\nExtra items in generated file:")
        for item in diff['dictionary_item_added']:
            messages.append(f"  {item}")

    if diff.get('dictionary_item_removed'):
        messages.append("\nMissing items in generated file:")
        for item in diff['dictionary_item_removed']:
            messages.append(f"  {item}")

    return "\n".join(messages)

def validate_json_output(generated: Dict[str, Any], reference: Dict[str, Any]) -> None:
    """Compare generated JSON against reference with detailed error reporting"""
    diff = DeepDiff(reference, generated, ignore_order=True)
    if diff:
        raise ValidationError(f"Generated output differs from reference:{format_json_diff(diff)}")

def validate_lua_output(generated: str, reference: str) -> None:
    """Compare generated Lua against reference with detailed error reporting"""
    if generated != reference:
        # Create line-by-line diff
        gen_lines = generated.splitlines()
        ref_lines = reference.splitlines()

        differences = []
        for i, (gen, ref) in enumerate(zip(gen_lines, ref_lines), 1):
            if gen != ref:
                differences.append(f"\nLine {i}:")
                differences.append(f"  Expected: {ref}")
                differences.append(f"  Got: {gen}")

        raise ValidationError("Generated Lua differs from reference:\n" + "\n".join(differences))