# Copilot Instructions for MidiFighter Twister Configuration Generator

## Project Overview
This project generates configuration files for the Midi Fighter Twister controller. It creates JSON and Lua configurations that can be imported into the MidiFighter Utility.

## Key Components
- `twister.py`: Main entry point that reads config and generates controller files
- `validate_output.py`: Validates generated output against reference files
- `config/config.json`: Main configuration defining controller setup
- `definitions/`: Core controller definition modules for different control types
- `helpers/`: Helper modules for file generation
- `tests/`: Test suite for validating functionality

## Code Patterns to Follow
1. **Configuration Management**
   - Use the JSON configuration structure in `config/config.json`
   - do not edit `config/config.json` without explicit direction to do so.
   - Maintain backward compatibility with existing config structure
   - Follow the schema validation defined in `test_config_validation.py`

2. **Control Definitions**
   - Button and encoder controls follow consistent patterns
   - Each control has tactile (physical) and projection (visual) components
   - Controls are organized in a 4x4 grid with banks

3. **Output Generation**
   - Generated files must match reference files in `output/backup/`
   - Use `validate_output.py` to verify generated output

4. **Error Handling**
   - Follow the error handling pattern in `twister.py`
   - Use custom exception classes (ValidationError, ConfigError)
   - Provide detailed error messages for troubleshooting

## Testing Strategy
- Run tests with `pytest tests/`
- Validate output with `python validate_output.py`
- Any changes to generation logic must not change output format

## Common Tasks
- **Adding Control Types**: Add definitions in both `definitions/tactile/` and `definitions/projection/`
- **Modifying Control Behavior**: Update the builder functions in relevant definition files
- **Extending Configuration**: Add new properties to config schema and update validation

## Important Considerations
- Maintain exact output formatting to match reference files
- Pay attention to indentation and string formatting in generated files
- Keep consistent ID generation for controls