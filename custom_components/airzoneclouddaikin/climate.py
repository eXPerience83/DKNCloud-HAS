"""Climate platform for DKN Cloud for HASS using the official Airzone Cloud API."""
import logging
from datetime import timedelta
from typing import Optional, List, Any, Dict

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .airzone_api import AirzoneAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)

AIRZONECLOUD_DEVICE_HVAC_MODES = [
    HVACMode.OFF,
    HVACMode.HEAT,
    HVACMode.COOL,
    HVACMode.DRY,
    HVACMode.FAN_ONLY,
]

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the climate platform from a config entry using our AirzoneAPI client."""
    config: Dict[str, Any] = entry.data
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    if not username or not password:
        _LOGGER.error("Missing username or password in config entry.")
        return

    session = async_get_clientsession(hass)
    api = AirzoneAPI(username, password, session)

    # Authenticate with the API
    if not await api.login():
        _LOGGER.error("Login to Airzone API failed.")
        return

    installations = await api.fetch_installations()
    _LOGGER.debug("Found %d installations", len(installations))
    if not installations:
        _LOGGER.warning("No installations found. Verify your credentials or API availability.")

    entities = []
    # Each installation is assumed to be a dict with a 'installation' key and a 'devices' key
    for relation in installations:
        installation = relation.get("installation")
        if not installation:
            continue
        devices: List[Dict] = installation.get("devices", [])
        _LOGGER.debug("Installation '%s' has %d devices", installation.get("name", "Unknown"), len(devices))
        for device in devices:
            entities.append(AirzonecloudDaikinDevice(device, installation))

    if not entities:
        _LOGGER.warning("No devices found in the API response.")
    async_add_entities(entities, True)

class AirzonecloudDaikinDevice(ClimateEntity):
    """Representation of an Airzone Cloud Daikin device."""

    def __init__(self, device_data: Dict, installation: Dict):
        """Initialize the climate entity.

        :param device_data: Dictionary with device information.
        :param installation: Dictionary with installation information.
        """
        self._device = device_data
        self._installation = installation
        _LOGGER.info("Initializing device %s (%s)", self.name, self.unique_id)

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID for the device."""
        return f"device_{self._device.get('id', 'unknown')}"

    @property
    def name(self) -> str:
        """Return the name of the device, combining installation and device names."""
        inst_name = self._installation.get("name", "Unknown Installation")
        dev_name = self._device.get("name", "Unknown Device")
        return f"{inst_name} - {dev_name}"

    @property
    def temperature_unit(self) -> str:
        """Return the temperature unit (Celsius)."""
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return the current HVAC mode of the device."""
        mode = self._device.get("mode", "")
        is_on = self._device.get("is_on", False)
        if is_on:
            if mode in ["cool", "cool-air"]:
                return HVACMode.COOL
            if mode in ["heat", "heat-air"]:
                return HVACMode.HEAT
            if mode == "ventilate":
                return HVACMode.FAN_ONLY
            if mode == "dehumidify":
                return HVACMode.DRY
        return HVACMode.OFF

    @property
    def hvac_modes(self) -> List[str]:
        """Return the list of available HVAC modes."""
        return AIRZONECLOUD_DEVICE_HVAC_MODES

    @property
    def current_temperature(self) -> Optional[float]:
        """Return the current temperature reported by the device."""
        return self._device.get("current_temperature")

    @property
    def target_temperature(self) -> Optional[float]:
        """Return the target temperature."""
        return self._device.get("target_temperature")

    def set_temperature(self, **kwargs) -> None:
        """Set a new target temperature.
        
        Here you should implement the API call to change the device's temperature.
        """
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            _LOGGER.debug("Setting temperature to %s", temperature)
            # TODO: Implement the API call here.
            pass

    def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set a new HVAC mode.
        
        Here you should implement the API call to change the device's mode.
        """
        _LOGGER.debug("Setting HVAC mode to %s", hvac_mode)
        if hvac_mode == HVACMode.OFF:
            self.turn_off()
        else:
            if not self._device.get("is_on", False):
                self.turn_on()
            mode_map = {
                HVACMode.HEAT: "heat",
                HVACMode.COOL: "cool",
                HVACMode.DRY: "dehumidify",
                HVACMode.FAN_ONLY: "ventilate",
            }
            if hvac_mode in mode_map:
                _LOGGER.debug("Changing mode via API to %s", mode_map[hvac_mode])
                # TODO: Implement the API call here.
                pass

    def turn_on(self) -> None:
        """Turn on the device.
        
        Implement the API call to turn on the device.
        """
        _LOGGER.debug("Turning device on.")
        # TODO: Implement the API call here.
        pass

    def turn_off(self) -> None:
        """Turn off the device.
        
        Implement the API call to turn off the device.
        """
        _LOGGER.debug("Turning device off.")
        # TODO: Implement the API call here.
        pass

    @property
    def supported_features(self) -> int:
        """Return the supported features (target temperature control)."""
        return ClimateEntityFeature.TARGET_TEMPERATURE
