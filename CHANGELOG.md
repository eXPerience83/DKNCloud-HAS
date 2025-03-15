# Changelog

All notable changes to this project will be documented in this file.

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
