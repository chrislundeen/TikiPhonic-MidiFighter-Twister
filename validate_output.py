import json
from helpers.validation_helpers import validate_json_output, validate_lua_output

def load_json_file(path):
    with open(path) as f:
        return json.load(f)

def load_lua_file(path):
    with open(path) as f:
        return f.read()

def main():
    # Compare controller JSON
    generated_json = load_json_file("output/_twister_controller.json")
    reference_json = load_json_file("tests/mocks/_twister_controller.json")
    validate_json_output(generated_json, reference_json)
    print("✓ Controller JSON matches reference")

    # Compare main Lua
    generated_lua = load_lua_file("output/_twister_main.lua")
    reference_lua = load_lua_file("tests/mocks/_twister_main.lua")
    validate_lua_output(generated_lua, reference_lua)
    print("✓ Main Lua matches reference")

    print("\nAll generated files match reference files exactly!")

if __name__ == "__main__":
    main()