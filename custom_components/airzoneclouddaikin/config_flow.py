"""Config flow for DKN Cloud for HASS."""
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

DOMAIN = "airzoneclouddaikin"
CONF_SCAN_INTERVAL = "scan_interval"

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SCAN_INTERVAL, default=10): vol.Coerce(int),
    vol.Optional("force_hvac_mode_auto", default=False): bool,
})

class AirzoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for DKN Cloud for HASS."""
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> dict:
        """Initial step of the config flow."""
        errors = {}

        if user_input is not None:
            try:
                scan_interval = int(user_input.get(CONF_SCAN_INTERVAL))
                if scan_interval < 10:
                    errors[CONF_SCAN_INTERVAL] = "scan_interval_too_low"
            except ValueError:
                errors[CONF_SCAN_INTERVAL] = "scan_interval_invalid"

            if not errors:
                return self.async_create_entry(title="DKN Cloud for HASS", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Required(CONF_SCAN_INTERVAL, default=10): vol.Coerce(int),
            vol.Optional("force_hvac_mode_auto", default=False): bool,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
