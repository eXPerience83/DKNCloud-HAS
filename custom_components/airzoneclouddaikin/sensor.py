"""Sensor platform for DKN Cloud for HASS."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from .airzone_api import AirzoneAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]  # Obtener la instancia de API desde hass.data
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
            sensors.append(AirzoneTemperatureSensor(api, installation_id, device))
    async_add_entities(sensors, True)

class AirzoneTemperatureSensor(SensorEntity):
    """Representation of a temperature sensor for an Airzone device (local_temp)."""

    def __init__(self, api: AirzoneAPI, installation_id: str, device_data: dict):
        """Initialize the sensor."""
        self._api = api
        self._installation_id = installation_id
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
        """Return device info to link the sensor to a device in HA."""
        return {
            "identifiers": {(DOMAIN, self._device_data.get("id"))},
            "name": self._device_data.get("name"),
            "manufacturer": self._device_data.get("brand", "Daikin"),
            "model": self._device_data.get("firmware", "Unknown"),
        }

    async def async_update(self):
        """Fetch the latest device data and update the state."""
        devices = await self._api.fetch_devices(self._installation_id)
        for dev in devices:
            if dev.get("id") == self._device_data.get("id"):
                self._device_data = dev
                break
        try:
            self._state = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._state = None
        self.async_write_ha_state()

    @property
    def scan_interval(self):
        """Return the scan interval for this entity."""
        return 10  # segundos
