# DKN Cloud for HASS

DKN Cloud for HASS is a custom integration for Home Assistant that allows you to view and control your Daikin Airzone Cloud (dkn.airzonecloud.com) devices directly from Home Assistant.

## Why this Fork?

This project is a fork of [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant) (which itself is a fork of [max13fr/AirzonecloudDaikin-HomeAssistant](https://github.com/max13fr/AirzonecloudDaikin-HomeAssistant)). It is based on the original AirzoneCloudDaikin package by max13fr and has been adapted for Home Assistant.

## Introduction

This integration uses an API client (in `airzone_api.py`) to:
- Authenticate via the `/users/sign_in` endpoint.
- Retrieve installations via the `/installation_relations` endpoint.
- Retrieve devices for each installation via the `/devices` endpoint.
- Control actions are implemented by sending events via the `/events` endpoint.

In addition, a sensor platform is included to record the temperature from the probe (local_temp) so that you can generate historical data and create automations or scenes based on the temperature.

Basic control methods have been implemented in `climate.py`:
- **turn_on:** Sends an event with P1=1.
- **turn_off:** Sends an event with P1=0.
- **set_hvac_mode:** Sends an event with P2 with the following mapping:
  - "1" for cool, "2" for heat, "3" for ventilate, "5" for dehumidify, and "4" for heat-cold-auto (an extra mode that can be forced under user responsibility).
- **set_temperature:** Sends an event with P8 (for heat or heat-cold-auto) or P7 (for cool) to adjust the target temperature. Temperature values must include a decimal (e.g., "23.0") for correct processing.

The API also returns additional data (such as firmware, brand, available fan speeds, etc.) that can be used to create additional sensors or for device information.

## Installation

### Manual Installation
1. Create the `custom_components` folder in your Home Assistant configuration directory (if it doesn't already exist).
2. Copy the entire `airzoneclouddaikin` folder from this repository into the `custom_components` folder.
3. Restart Home Assistant.

### Installation via HACS
1. Open HACS in Home Assistant.
2. Go to **Integrations**.
3. Click the three-dot menu in the top right and select **Custom repositories**.
4. Enter the URL of this repository:  
   `https://github.com/eXPerience83/DKNCloud-HASS`
5. Set the category to **Integration**.
6. Click **Add**.
7. Search for "DKN Cloud for HASS" in HACS and install the integration.
8. Restart Home Assistant if prompted.

## Configuration

After installation, add the integration via the Home Assistant UI by going to **Settings > Devices & Services > Add Integration**, searching for "DKN Cloud for HASS", and following the prompts.

## Usage

The integration retrieves your installations and devices, and creates:
- A **climate entity** for each device (allowing control of power, mode, and target temperature).
- A **sensor entity** for the temperature probe (local_temp), which Home Assistant can record in its history.

You can control the device (e.g., turn on/off, change mode, adjust temperature) from the Home Assistant UI. The integration sends the corresponding events (P1, P2, P7, P8) to the API.

> **Important:** Daikin climate equipment uses two consigns (one for heat and one for cold). Change the mode first (for example, to heat) and then adjust the temperature. Although the original package defined modes up to "8", our tests indicate that only modes 1–5 produce an effect. The integration also extracts the available fan speeds from the API response to limit the valid fan speed options.

## API Examples

For further testing, refer to the file `info.md` which contains detailed information and example curl commands.

## License

This project is licensed under the MIT License.
