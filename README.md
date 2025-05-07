# MidiFighter Twister Configuration Generator

This project provides Python scripts to generate configuration files for the Midi Fighter Twister controller. It automatically builds controller and main JSON files that can be imported into the MidiFighter Utility.

## About the Midi Fighter Twister

The Midi Fighter Twister is a MIDI controller featuring 16 push-button rotary encoders, designed for precise control over software parameters. For more information, visit: https://www.midifighter.com/#Twister

## Project Structure

- `twister.py` - Main entry point that reads configuration and generates controller files
- `config/` - Contains configuration files
  - `config.json` - Main configuration defining controller setup and mappings
- `definitions/` - Core controller definition modules
  - `guitar_rig/` - Guitar Rig specific control definitions
    - `button.py` - Button definitions for Guitar Rig
    - `encoder.py` - Encoder definitions for Guitar Rig
    - `sample.json` - Sample Guitar Rig configuration
  - `projection/` - Visual layout definitions
    - `button.py` - Button projection definitions
    - `encoder.py` - Encoder projection definitions
  - `tactile/` - Physical control definitions
    - `button.py` - Physical button definitions
    - `encoder.py` - Physical encoder definitions
- `helpers/` - Helper modules for file generation
  - `helpers.py` - Common helper functions
  - `helpers_controllers.py` - Functions for building controller configurations
  - `helpers_main.py` - Functions for building main configuration
- `output/` - Generated configuration files

## Features

- Generates complete controller configuration with:
  - Button mappings
  - Encoder mappings
  - Push encoder mappings
- Supports 4 banks of controls
- Configurable MIDI channels and control numbers
- Visual layout configuration for the MidiFighter Utility
- Configurable groups for organizing controls
- Guitar Rig specific configuration support
- Automatic backup of configurations
- Lua script generation support

## Configuration

The `config.json` file defines:
- Controller version
- Control groups
- Default controller settings
- Base configuration for buttons, encoders and push-encoders
- Visual layout settings
- Guitar Rig specific mappings

## Dependencies

### Required Python Packages
- jsonmerge: For merging JSON configurations
  ```
  pip install jsonmerge
  ```

## Usage

1. Configure settings in `config/config.json`
2. Run the generator:
   ```
   python twister.py
   ```
3. Import the generated files from `output/` into the MidiFighter Utility

## Generated Files

- `_twister_controller.json`: Contains all controller mappings and configurations
- `_twister_main.json`: Contains main program configuration
- Lua scripts for advanced functionality
- Backup files are automatically maintained in `output/backups/`

## Control Layout

The controller is organized into:
- 16 push-button encoders (4x4 grid)
- 3 control groups:
  - Buttons
  - Encoders
  - Push Encoders
- Each control has configurable:
  - MIDI channel
  - Control number
  - Response mode
  - Visual feedback settings
  - Guitar Rig specific parameters

