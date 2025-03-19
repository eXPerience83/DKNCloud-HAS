from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature

from .airzone_api import AirzoneCloudDaikinAPI
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up climate entities."""
    api: AirzoneCloudDaikinAPI = hass.data[DOMAIN][entry.entry_id]
    devices = await api.async_get_devices()
    async_add_entities(AirzoneClimate(device, api) for device in devices)

class AirzoneClimate(ClimateEntity):
    """Representation of a Daikin Airzone Cloud climate entity."""

    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_temperature_unit = UnitOfTemperature.CELSIUS

    def __init__(self, device, api):
        """Initialize the climate entity."""
        self._device = device
        self._api = api
        self._attr_name = device["name"]
        self._attr_unique_id = device["id"]
        self._attr_hvac_modes = [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.FAN_ONLY,
            HVACMode.DRY,
        ]
        if self._api.allow_auto_mode:
            self._attr_hvac_modes.append(HVACMode.AUTO)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode."""
        mode_map = {
            HVACMode.OFF: "0",
            HVACMode.COOL: "1",
            HVACMode.HEAT: "2",
            HVACMode.FAN_ONLY: "3",
            HVACMode.DRY: "5",
        }
        if hvac_mode == HVACMode.AUTO and self._api.allow_auto_mode:
            mode_map[HVACMode.AUTO] = "4"

        await self._api.async_send_command(self._device["id"], "P2", mode_map[hvac_mode])

    async def async_set_temperature(self, **kwargs):
        """Set the target temperature."""
        temperature = kwargs.get("temperature")
        if temperature is None:
            return
        temperature = int(temperature)
        if self.hvac_mode == HVACMode.HEAT:
            await self._api.async_send_command(self._device["id"], "P8", f"{temperature}.0")
        elif self.hvac_mode == HVACMode.COOL:
            await self._api.async_send_command(self._device["id"], "P7", f"{temperature}.0")

    async def async_turn_on(self):
        """Turn on the device."""
        await self._api.async_send_command(self._device["id"], "P1", "1")

    async def async_turn_off(self):
        """Turn off the device."""
        await self._api.async_send_command(self._device["id"], "P1", "0")
