"""Sensor platform for DKN Cloud for HASS."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    installations = await api.fetch_installations()
    sensors = []
    for relation in installations:
        installation = relation.get("installation")
        if not installation:
            continue
        installation_id = installation.get("id")
        if not installation_id:
            continue
        devices = await api.fetch_devices(installation_id)
        for device in devices:
            sensors.append(AirzoneTemperatureSensor(device))
    async_add_entities(sensors, True)

class AirzoneTemperatureSensor(SensorEntity):
    """Representation of a temperature sensor for an Airzone device (local_temp)."""

    def __init__(self, device_data: dict):
        """Initialize the sensor."""
        self._device_data = device_data
        self._name = f"{device_data.get('name', 'Airzone Device')} Temperature"
        self._state = None
        self._unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        device_id = self._device_data.get("id")
        if device_id:
            return f"{device_id}_temperature"
        return None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the current temperature reading."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_class(self):
        """Return the device class."""
        return "temperature"

    @property
    def state_class(self):
        """Return the state class."""
        return "measurement"

    @property
    def device_info(self):
        """Return device info to link this sensor to a device in HA."""
        return {
            "identifiers": {(DOMAIN, self._device_data.get("id"))},
            "name": self._device_data.get("name"),
            "manufacturer": self._device_data.get("brand", "Daikin"),
            "model": self._device_data.get("firmware", "Unknown"),
        }

    async def async_update(self):
        """Update the sensor state.
        
        This method should be called periodically by Home Assistant.
        """
        try:
            self._state = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._state = None
        self.async_write_ha_state()

    @property
    def scan_interval(self):
        """Return the scan interval (in seconds) for the sensor."""
        return 10
