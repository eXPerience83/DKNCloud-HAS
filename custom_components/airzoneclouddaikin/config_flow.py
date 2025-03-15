"""Config flow for DKN Cloud for HASS."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

DOMAIN = "airzoneclouddaikin"
# Use "scan_interval" as our custom key.
CONF_SCAN_INTERVAL = "scan_interval"

_LOGGER = logging.getLogger(__name__)

# Define the data schema. The default value is 10 seconds.
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SCAN_INTERVAL, default=10): vol.Coerce(int),
})

class AirzoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for DKN Cloud for HASS."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> dict:
        """Initial step of the config flow."""
        errors = {}

        if user_input is not None:
            # Validate that scan_interval is an integer greater than 0.
            try:
                scan_interval = int(user_input.get(CONF_SCAN_INTERVAL))
                if scan_interval < 1:
                    errors[CONF_SCAN_INTERVAL] = "scan_interval_no_valido"
            except ValueError:
                errors[CONF_SCAN_INTERVAL] = "scan_interval_no_valido"

            # Additional validation (e.g., connecting to the Airzone API) could be added here.
            if not errors:
                # Create the config entry with validated data.
                return self.async_create_entry(
                    title="DKN Cloud for HASS",
                    data=user_input,
                )

        # Help message for scan_interval.
        scan_interval_description = (
            "Value in seconds. Default is 10. "
            "It is not recommended to set a value lower than 10 seconds to avoid being banned by Airzone."
        )
        # Build the schema for showing the form.
        schema = vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Required(CONF_SCAN_INTERVAL, default=user_input.get(CONF_SCAN_INTERVAL, 10) if user_input else 10):
                vol.All(vol.Coerce(int)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={"scan_interval_description": scan_interval_description},
        )
