# DKN Cloud for HASS

DKN Cloud for HASS is a custom integration for Home Assistant that allows you to view and control your Daikin Airzone Cloud (dkn.airzonecloud.com) devices directly from Home Assistant.  
This fork is designed for the "DAIKIN ES.DKNWSERVER Wifi adapter."

## Why this Fork?

This project is a fork of [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant) (which itself is a fork of [max13fr/AirzonecloudDaikin-HomeAssistant](https://github.com/max13fr/AirzonecloudDaikin-HomeAssistant)). It is based on the original AirzoneCloudDaikin package by max13fr and has been adapted for Home Assistant.

## Introduction

This integration uses an API client (in `airzone_api.py`) to:
- Authenticate via the `/users/sign_in` endpoint.
- Retrieve installations via the `/installation_relations` endpoint (using user_email and user_token in query parameters).
- Retrieve devices for each installation via the `/devices` endpoint.
- Send control events via the `/events` endpoint.

Additionally, a sensor platform is included to record the temperature from the probe (`local_temp`), enabling historical data and automations.

Basic control methods have been implemented in `climate.py`:
- **turn_on:** Sends an event with P1=1.
- **turn_off:** Sends an event with P1=0.
- **set_hvac_mode:** Sends an event with P2. Supported mappings:
  - HVACMode.OFF: calls turn_off().
  - HVACMode.COOL: sends P2=1.
  - HVACMode.HEAT: sends P2=2.
  - HVACMode.FAN_ONLY: sends P2=3.
  - HVACMode.DRY: sends P2=5.
  - HVACMode.AUTO (forced via configuration): sends P2=4.
- **set_temperature:** Sends an event with P8 for HEAT/AUTO modes or P7 for COOL mode, using the device’s temperature limits and formatting the value as an integer with ".0" appended.
- **set_fan_speed:** Uses P3 to adjust fan speed in COOL and FAN_ONLY mode and P4 in HEAT/AUTO mode.

The API returns additional data (firmware, brand, available fan speeds, temperature limits, etc.) that the integration uses:
- The field `availables_speeds` defines the valid fan speed options.
- The fields `min_limit_cold`, `max_limit_cold`, `min_limit_heat`, and `max_limit_heat` define the valid temperature ranges.
- Temperatures are always sent as integer values with a ".0" appended (e.g., 23 → "23.0").

> **Important:**  
> Daikin climate equipment uses two consigns (one for heat and one for cold). Change the mode first (e.g., to heat) and then adjust the temperature. Although the original package defined modes up to "8", our tests indicate that only modes 1–5 produce an effect. Note that fan speed commands differ for cold and heat modes.

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

The configuration will ask for:
- **Username and Password:** Your Airzone Cloud account credentials.
- **Scan Interval:** Time in seconds between updates.
- **Force HVAC Mode Auto:** (Optional checkbox) If enabled, the mode "auto" (HVACMode.AUTO) will be available for selection. Use this mode under your own responsibility.

## Usage

The integration retrieves your installations and devices, and creates:
- A **climate entity** for each device (allowing control of power, HVAC mode, target temperature, and fan speed).
- A **sensor entity** for the temperature probe (`local_temp`), which Home Assistant will record historically.

When you interact with the climate entity, the integration sends the corresponding events (P1, P2, P7, P8, and fan speed commands P3/P4) to the API. The sensor entity updates based on the device’s reported temperature.

## API Examples

For further testing, refer to the file `info.md` for detailed information and example curl commands.

## License

This project is licensed under the MIT License.
