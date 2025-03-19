"""Sensor platform for DKN Cloud for HASS."""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    config = entry.data
    username = config.get("username")
    password = config.get("password")
    if not username or not password:
        _LOGGER.error("Missing username or password")
        return
    from homeassistant.helpers.aiohttp_client import async_get_clientsession
    from .airzone_api import AirzoneAPI
    session = async_get_clientsession(hass)
    api = AirzoneAPI(username, password, session)
    if not await api.login():
        _LOGGER.error("Login to Airzone API failed.")
        return
    installations = await api.fetch_installations()
    entities = []
    for relation in installations:
        installation = relation.get("installation")
        if not installation:
            continue
        installation_id = installation.get("id")
        if not installation_id:
            continue
        devices = await api.fetch_devices(installation_id)
        for device in devices:
            entities.append(AirzoneTemperatureSensor(device))
    async_add_entities(entities, True)

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

    def update_state(self):
        """Update the state from device data."""
        try:
            self._state = float(self._device_data.get("local_temp"))
        except (ValueError, TypeError):
            self._state = None

    def update(self):
        """Update the sensor state."""
        self.update_state()
