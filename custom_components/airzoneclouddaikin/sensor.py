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
    async_add_entities(sensors)  # Let HA assign entity_id after adding entities.

class AirzoneTemperatureSensor(SensorEntity):
    """Representation of a temperature sensor for an Airzone device (local_temp)."""

    def __init__(self, device_data: dict):
        """Initialize the sensor entity using device data."""
        self._device_data = device_data
        # Construct sensor name: "<Device Name> Temperature"
        name = f"{device_data.get('name', 'Airzone Device')} Temperature"
        self._attr_name = name

        # Use the device 'id' to form a unique id; fallback to a hash of the name if not available.
        device_id = device_data.get("id")
        if device_id and device_id.strip():
            self._attr_unique_id = f"{device_id}_temperature"
        else:
            self._attr_unique_id = hashlib.sha256(name.encode("utf-8")).hexdigest()

        self._attr_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = "temperature"
        self._attr_state_class = "measurement"
        self._attr_icon = "mdi:thermometer"
        # Initialize the native value from device data
        self.update_state()

    @property
    def unique_id(self):
        """Return the unique id for this sensor."""
        return self._attr_unique_id

    @property
    def native_value(self):
        """Return the current temperature reading."""
        return self._attr_native_value

    @property
    def device_info(self):
        """Return device info to link this sensor to a device in Home Assistant."""
        return {
            "identifiers": {("airzoneclouddaikin", self._device_data.get("id"))},
            "name": self._device_data.get("name"),
            "manufacturer": self._device_data.get("brand", "Daikin"),
            "model": self._device_data.get("firmware", "Unknown"),
        }

    async def async_update(self):
        """Update the sensor state from the device data."""
        self.update_state()
        self.async_write_ha_state()

    def update_state(self):
        """Update the native value from device data."""
        try:
            self._attr_native_value = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._attr_native_value = None
