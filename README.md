# DKN Cloud for HASS

**DKN Cloud for HASS** is a custom integration for Home Assistant that allows you to view and control all your zones registered on your Daikin Airzone Cloud (dkn.airzonecloud.com) account directly from Home Assistant.

![DKN Cloud for HASS Screenshot](screenshot.png)

## Why this Fork?

This project is a fork of [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant) (which itself is a fork of [max13fr/AirzonecloudDaikin-HomeAssistant](https://github.com/max13fr/AirzonecloudDaikin-HomeAssistant)) by the original authors @max13fr and @fitamix. For more details about the underlying API implementation, please refer to the original AirzoneCloudDaikin package.

## Introduction

This integration now uses our own API client (in the `airzone_api.py` module) to interact with the Airzone Cloud API for dkn.airzonecloud.com. The client authenticates via a POST request to the `/users/sign_in` endpoint and retrieves installations via the `/installation_relations` endpoint. For each installation, the devices are obtained via the `/devices` endpoint. If successful, the integration creates climate entities representing each device.

The configuration flow collects the following parameters:
- **Username:** Your Airzone Cloud account email.
- **Password:** Your Airzone Cloud account password.
- **Scan Interval:** Time in seconds between each update (default is 10 seconds, and it is recommended not to set this value too low to avoid bans).

## Installation

### Manual Installation

1. Create the `custom_components` folder in your Home Assistant configuration directory (if it doesn't already exist).
2. Copy the entire `airzoneclouddaikin` folder from this repository into the `custom_components` folder.
3. Restart Home Assistant.

### Installation via HACS

1. Open HACS in Home Assistant.
2. Go to **Integrations**.
3. Click on the three-dot menu in the top right corner and select **Custom repositories**.
4. Enter the URL:  
   `https://github.com/eXPerience83/DKNCloud-HASS`
5. Set the category to **Integration**.
6. Click **Add**.
7. Search for "DKN Cloud for HASS" in HACS and install the integration.
8. Restart Home Assistant if prompted.

## Configuration

After installation, add the integration via the Home Assistant UI by going to **Settings > Devices & Services > Add Integration**, searching for "DKN Cloud for HASS", and following the prompts.

## Debugging

Detailed logging is enabled in the integration. Refer to the Home Assistant documentation on logger configuration if you need to adjust the logging level.

## Issues

If you encounter any issues, please open an issue at the [issue tracker](https://github.com/eXPerience83/DKNCloud-HASS/issues).

## License

This project is licensed under the MIT License.
