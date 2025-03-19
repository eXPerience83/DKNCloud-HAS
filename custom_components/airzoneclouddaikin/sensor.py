"""Sensor platform for DKN Cloud for HASS."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)

class AirzoneTemperatureSensor(SensorEntity):
    """Representation of a temperature sensor for an Airzone device (local_temp)."""

    def __init__(self, device_data: dict):
        """Initialize the sensor."""
        self._device_data = device_data
        self._name = f"{device_data.get('name', 'Airzone Device')} Temperature"
        self._state = None
        self._unit_of_measurement = UnitOfTemperature.CELSIUS
        self.update_state()

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

    def update_state(self):
        """Update the state from device data."""
        try:
            self._state = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._state = None

    def update(self):
        """Update the sensor state."""
        self.update_state()
