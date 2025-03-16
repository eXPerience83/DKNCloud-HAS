# DKN Cloud for HASS

**DKN Cloud for HASS** is a custom integration for Home Assistant that allows you to view and control all your zones registered on your Daikin Airzone Cloud (dkn.airzonecloud.com) account directly from Home Assistant.

![DKN Cloud for HASS Screenshot](screenshot.png)

## Why this Fork?

This project is a fork of [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant) (which itself is a fork of [max13fr/AirzonecloudDaikin-HomeAssistant](https://github.com/max13fr/AirzonecloudDaikin-HomeAssistant)) by the original authors @max13fr and @fitamix.  
For more details about the underlying API implementation, please refer to the official Airzone Cloud Web API documentation at [developers.airzonecloud.com/docs/web-api](https://developers.airzonecloud.com/docs/web-api) and the [AirzoneCloudDaikin package](https://pypi.org/project/AirzoneCloudDaikin/) (which we are no longer using).

## Introduction

This integration now uses our own API client (in the `airzone_api.py` module) to interact with the official Airzone Cloud API—adapted for dkn.airzonecloud.com.  
The client authenticates by sending a POST request to the `/login` endpoint and then fetches installations (and their devices) via the `/installation_relations` endpoint. If successful, the integration creates climate entities representing each device.

The configuration flow collects the following parameters:
- **Username**: Your Airzone Cloud account email.
- **Password**: Your Airzone Cloud account password.
- **Scan Interval**: Time in seconds between each update. (Default is 10 seconds. It is recommended not to set this value too low to avoid bans from Airzone.)

## Installation

### Manual Installation

1. Create the directory `custom_components` in your Home Assistant configuration folder (if it doesn't already exist).
2. Copy the entire `airzoneclouddaikin` folder from this repository into the `custom_components` folder.
3. Restart Home Assistant.

### Installation via HACS

**DKN Cloud for HASS** can now be installed as a custom integration through HACS.

1. Open HACS in Home Assistant.
2. Go to **Integrations**.
3. Click on the three-dot menu in the top right corner and select **Custom repositories**.
4. Enter the URL of this repository:  
   `https://github.com/eXPerience83/DKNCloud-HASS`
5. Set the **Category** to **Integration**.
6. Click **Add**.
7. Once added, search for "DKN Cloud for HASS" in HACS and install the integration.
8. Restart Home Assistant if prompted.

## Configuration

After installation, add the integration via the Home Assistant UI by going to **Settings** > **Devices & Services** > **Add Integration**, searching for "DKN Cloud for HASS", and following the prompts.

## Debugging

To help troubleshoot, the integration includes detailed logging in the API client and climate platform:
- The client logs the result of the login attempt and the number of installations fetched.
- If no installations or devices are found, a warning is logged.

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.airzoneclouddaikin: debug
    AirzoneAPI: debug
