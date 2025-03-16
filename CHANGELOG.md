# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-03-16
### Added
- **Airzone API Client:** New module `airzone_api.py` implementing the official Airzone Cloud Web API (adapted for dkn.airzonecloud.com) for authentication and fetching installations.
- **Async Setup:** Updated `climate.py` now uses `async_setup_entry` to initialize the integration with config entries.
- Detailed logging in `airzone_api.py` and `climate.py` for better debugging of API calls and data retrieval.

### Fixed
- Replaced external dependency on the AirzoneCloudDaikin package by using our own implementation.
- Updated the version in `manifest.json` to 0.1.2.

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
