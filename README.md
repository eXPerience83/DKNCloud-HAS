# DKN Cloud for HASS

**DKN Cloud for HASS** is a custom integration for Home Assistant that allows you to view and control all your zones registered on your Daikin Airzone Cloud (dkn.airzonecloud.com) account directly from Home Assistant.

## Why this Fork?

This project is a fork of [fitamix/DaikinDKNCloud-HomeAssistant](https://github.com/fitamix/DaikinDKNCloud-HomeAssistant) (which itself is a fork of [max13fr/Airzonecloud-HomeAssistant](https://github.com/max13fr/Airzonecloud-HomeAssistant)) by the original authors @max13fr and @fitamix.  
In our fork, we have added a configuration interface via Home Assistant's config flow. This allows users to configure the integration through the UI instead of manually editing the `configuration.yaml`. In addition, we have updated the installation instructions to include an option for installation via HACS.

## Introduction

The integration lets you view and control your Daikin Airzone Cloud zones from Home Assistant. It resolves previous issues such as errors with temperature conversion by commenting out the problematic code. In this version, we've also added a configuration flow that validates user input.  
For example, the `scan_interval` parameter is now validated as an integer (with a default value of 10 seconds) and includes a warning not to set it too low to avoid potential bans from Airzone.

If you're looking for the main Airzone Cloud (airzonecloud.com) integration, please refer to [max13fr/Airzonecloud-HomeAssistant](https://github.com/max13fr/Airzonecloud-HomeAssistant).

## Installation

### Manual Installation

1. Create the directory `custom_components` in your Home Assistant configuration folder (if it doesn't already exist).
2. Copy the entire `airzoneclouddaikin` folder from this repository into the `custom_components` folder.
3. Restart Home Assistant.

Make sure to update your configuration (if needed) as the integration is now configured via the UI.

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

After installation, you can add the integration via the Home Assistant UI. Click on **Settings** > **Devices & Services** > **Add Integration**, search for "DKN Cloud for HASS", and follow the prompts.  
The configuration form includes the following parameters:
- **Username**: Your Airzone Cloud account email.
- **Password**: Your Airzone Cloud account password.
- **Scan Interval**: Time in seconds between each update. (Default is 10 seconds. It is recommended not to set this value too low to avoid bans from Airzone.)

## Issues

If you encounter any issues, please open an issue at the [issue tracker](https://github.com/eXPerience83/DKNCloud-HASS/issues) of this repository.

## License

This project is licensed under the MIT License.
