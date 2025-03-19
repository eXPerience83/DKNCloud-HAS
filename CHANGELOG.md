# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-03-18
### Added
- Integration updated to version 0.2.0.
- Updated API endpoints and BASE_URL in const.py.
- Simplified const.py (eliminado MODES_CONVERTER del código; se documenta en info.md).
- Updated User-Agent in airzone_api.py to simulate a Windows browser.
- Implemented basic control methods in climate.py: turn_on, turn_off, set_hvac_mode (including support for "heat-cold-auto" via P2=4, forced under user responsibility), and set_temperature (using P8 for heat and P7 for cool, with temperature values sent as decimals).
- Added property `fan_speed_range` in climate.py to derive allowed fan speeds from "availables_speeds".
- Added sensor platform (sensor.py) for a temperature probe sensor to record the "local_temp".
- Added file info.md with detailed information about the "Px" modes and example curl commands (using placeholders for sensitive data).
- Documented that the original package defined modes up to "8", but in our tests only modes 1–5 produce an effect.
  
### Changed
- Version updated in manifest.json to 0.2.0.
- Minor adjustments in config_flow.py, __init__.py, and README.md.

### Pending (for future versions)
- Refinement of control actions in climate.py if needed.
- Further testing and potential implementation of additional options (P5, P6) if required.

## [0.1.5] - 2025-03-16
### Added
- **Airzone API Client:** Updated module `airzone_api.py` now uses the endpoints from the original AirzoneCloudDaikin package:
  - Login: `/users/sign_in`
  - Installation Relations: `/installation_relations`
  - Devices: `/devices`
  - Events: `/events`
- Added a method `fetch_devices(installation_id)` in `airzone_api.py` to retrieve devices for a given installation.
- Updated `climate.py` to fetch devices per installation using `fetch_devices`.
- Detailed logging added to all modules for debugging (login, fetching installations, fetching devices).

### Fixed
- Updated endpoints based on tests with curl.
- Adjusted the base URL to "https://dkn.airzonecloud.com" (without adding "/api") as used in the original package.
- Fixed import errors by ensuring `const.py` exports the required constants.
- Set version in manifest.json to 0.1.5.

### Changed
- Documentation in README.md updated to reflect these changes.

## [0.1.2] - 2025-03-16
### Added
- **Airzone API Client:** New module `airzone_api.py` implementing the official Airzone Cloud Web API (adapted for dkn.airzonecloud.com) for authentication and fetching installations.
- **Async Setup:** Updated `climate.py` now uses `async_setup_entry` to initialize the integration with config entries.
- Detailed logging in `airzone_api.py` and `climate.py` for better debugging of API calls and data retrieval.
- Added a new `const.py` with essential constants.

### Fixed
- Replaced external dependency on the AirzoneCloudDaikin package by using our own implementation.
- Updated the version in `manifest.json` to 0.1.2.
- Fixed import errors by creating/updating `const.py`.

### Changed
- Updated documentation in README.md to reflect changes.
- Updated repository URLs and HACS configuration.

## [0.1.1] - 2025-03-15
### Fixed
- Replaced `setup_platform` with `async_setup_entry` in `climate.py` to support Home Assistant's config entries.
- Fixed integration with `AirzoneCloudDaikin` library in `climate.py`.
- Updated entity setup to use `async_add_entities` instead of `add_entities`.
- Optimized HVAC mode handling.
- Removed unused `AirzonecloudDaikinInstallation` class.

### Changed
- Updated `manifest.json` version to `0.1.1`.

## [0.1.0] - 2025-03-15
### Added
- Config Flow integration for **DKN Cloud for HASS**, enabling configuration via Home Assistant's UI.
- Validation for the `scan_interval` parameter (must be an integer ≥ 1, with a default value of 10 seconds) along with an informational message.
- Updated `manifest.json` with the new name "DKN Cloud for HASS", version set to 0.1.0, added `"config_flow": true`, and updated codeowners to include `eXPerience83`.
- Installation instructions added for HACS integration in the README.
- Updated issue tracker link to point to [https://github.com/eXPerience83/DKNCloud-HASS/issues](https://github.com/eXPerience83/DKNCloud-HASS/issues).

### Changed
- Removed the external dependency on `AirzoneCloudDaikin` by eliminating the `"requirements"` field from `manifest.json`.
- Updated HACS configuration in `hacs.json` to reflect the new project name "DKN Cloud for HASS".
- Updated repository URL references from "DKNCloud-HAS" to "DKNCloud-HASS".
- Forked from [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant), which itself is a fork of [max13fr/Airzonecloud-HomeAssistant](https://github.com/max13fr/Airzonecloud-HomeAssistant).
- Minor documentation updates to reflect the new configuration options and installation process.
- 
### Fixed
- Added missing `__init__.py` to properly load the integration and avoid "No setup or config entry setup function defined" error.
