"""Switch platform for DKN Cloud for HASS."""
import asyncio
import logging
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .airzone_api import AirzoneAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the switch platform from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]  # Use the shared API instance
    installations = await api.fetch_installations()
    switches = []
    for relation in installations:
        installation = relation.get("installation")
        if not installation:
            continue
        installation_id = installation.get("id")
        if not installation_id:
            continue
        devices = await api.fetch_devices(installation_id)
        for device in devices:
            switches.append(AirzonePowerSwitch(api, device, entry.data, hass))
    async_add_entities(switches, True)

class AirzonePowerSwitch(SwitchEntity):
    """Representation of a power switch for an Airzone device."""

    def __init__(self, api: AirzoneAPI, device_data: dict, config: dict, hass):
        """Initialize the power switch."""
        self._api = api
        self._device_data = device_data
        self._config = config
        self._name = f"{device_data.get('name', 'Airzone Device')} Power"
        self._device_id = device_data.get("id")
        self._state = bool(int(device_data.get("power", 0)))
        self.hass = hass

    @property
    def unique_id(self):
        """Return a unique ID for this switch."""
        return f"{self._device_id}_power"

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return True if the device is on."""
        return self._state

    @property
    def device_info(self):
        """Return device info for the device registry."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_data.get("name"),
            "manufacturer": self._device_data.get("brand", "Daikin"),
            "model": self._device_data.get("firmware", "Unknown"),
        }

    async def async_turn_on(self, **kwargs):
        """Turn on the device."""
        self._send_command("P1", 1)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the device."""
        self._send_command("P1", 0)
        self._state = False
        self.async_write_ha_state()

    def _send_command(self, option, value):
        """Send a command to the device."""
        payload = {
            "event": {
                "cgi": "modmaquina",
                "device_id": self._device_id,
                "option": option,
                "value": value,
            }
        }
        _LOGGER.info("Sending power command: %s", payload)
        self.hass.async_create_task(self._api.send_event(payload))
