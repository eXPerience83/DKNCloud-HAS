# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-03-15
### Added
- Config Flow integration for DKN Airzone Cloud, enabling configuration via Home Assistant's UI.
- Validation for the `scan_interval` parameter (must be an integer ≥ 1, with a default value of 10 seconds) along with an informational message.
- Updated `manifest.json` with the new name "DKN Airzone Cloud", version set to 0.1.0, added `"config_flow": true`, and updated codeowners to include `eXPerience83`.
- Installation instructions added for HACS integration in the README.

### Changed
- Forked from [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant), which itself is a fork of [max13fr/Airzonecloud-HomeAssistant](https://github.com/max13fr/Airzonecloud-HomeAssistant).
- Minor documentation updates to reflect the new configuration options and installation process.
