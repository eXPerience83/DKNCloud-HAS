"""Sensor platform for DKN Cloud for HASS."""
import hashlib
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    config = entry.data
    from homeassistant.helpers.aiohttp_client import async_get_clientsession
    session = async_get_clientsession(hass)
    from .airzone_api import AirzoneAPI
    api = AirzoneAPI(config.get("username"), config.get("password"), session)
    if not await api.login():
        _LOGGER.error("Login to Airzone API failed in sensor setup.")
        return
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
        """Initialize the sensor entity using device data."""
        self._device_data = device_data
        # Set the sensor name as: "<Device Name> Temperature"
        self._attr_name = f"{device_data.get('name', 'Airzone Device')} Temperature"
        # Use the device id (if available) to form a unique id; otherwise, fallback to a hash of the name.
        device_id = device_data.get("id")
        if device_id and device_id.strip():
            self._attr_unique_id = f"{device_id}_temperature"
        else:
            self._attr_unique_id = hashlib.sha256(self._attr_name.encode("utf-8")).hexdigest()
        self._attr_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = "temperature"
        self._attr_state_class = "measurement"
        self._attr_icon = "mdi:thermometer"
        self.update_state()

    @property
    def native_value(self):
        """Return the current temperature reading."""
        return self._attr_native_value

    def update_state(self):
        """Update the state from device data."""
        try:
            # Update _attr_native_value with the temperature value from local_temp.
            self._attr_native_value = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._attr_native_value = None

    async def async_update(self):
        """Update the sensor state and write it to Home Assistant."""
        self.update_state()
        self.async_write_ha_state()
