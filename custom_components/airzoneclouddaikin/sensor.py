from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

from .airzone_api import AirzoneCloudDaikinAPI
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor entities."""
    api: AirzoneCloudDaikinAPI = hass.data[DOMAIN][entry.entry_id]
    devices = await api.async_get_devices()
    async_add_entities(AirzoneTemperatureSensor(device, api) for device in devices)

class AirzoneTemperatureSensor(SensorEntity):
    """Representation of the Daikin Airzone Cloud temperature sensor."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = "temperature"

    def __init__(self, device, api):
        """Initialize the sensor."""
        self._device = device
        self._api = api
        self._attr_name = f"{device['name']} Temperature"
        self._attr_unique_id = f"{device['id']}_temperature"

    async def async_update(self):
        """Fetch new state data."""
        await self._api.async_update()
        self._attr_native_value = self._api.get_device_temperature(self._device["id"])
