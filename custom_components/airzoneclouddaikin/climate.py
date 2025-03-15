"""Climate platform for DKN Cloud for HASS."""
import logging
from datetime import timedelta
from typing import Optional, List

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD

from AirzoneCloudDaikin import AirzoneCloudDaikin  # Asegúrate de que esta importación funciona

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
    """Set up the climate platform from a config entry."""
    config = entry.data
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    if not username or not password:
        _LOGGER.error("Missing username or password in config entry.")
        return

    try:
        api = AirzoneCloudDaikin(username, password)
        # Si es necesario, llama a un método para actualizar o iniciar sesión:
        # api.login() o api.refresh()
    except Exception as err:
        _LOGGER.error("Error connecting to AirzoneCloudDaikin: %s", err)
        return

    installations = getattr(api, "installations", [])
    _LOGGER.debug("Found %d installations", len(installations))

    entities = []
    for installation in installations:
        for device in getattr(installation, "devices", []):
            entities.append(AirzonecloudDaikinDevice(device))
    if not entities:
        _LOGGER.warning("No devices found in the API response.")
    async_add_entities(entities, True)

class AirzonecloudDaikinDevice(ClimateEntity):
    """Representation of an AirzoneCloud Daikin Device."""

    def __init__(self, azc_device):
        """Initialize the device."""
        self._azc_device = azc_device
        _LOGGER.info("Initializing device %s (%s)", self.name, self.unique_id)

    @property
    def unique_id(self) -> Optional[str]:
        return f"device_{self._azc_device.id}"

    @property
    def name(self):
        return f"{self._azc_device.installation.name} - {self._azc_device.name}"

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self) -> str:
        mode = self._azc_device.mode
        if self._azc_device.is_on:
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
        return AIRZONECLOUD_DEVICE_HVAC_MODES

    @property
    def current_temperature(self) -> Optional[float]:
        return self._azc_device.current_temperature

    @property
    def target_temperature(self) -> Optional[float]:
        return self._azc_device.target_temperature

    def set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            self._azc_device.set_temperature(round(float(temperature), 1))

    def set_hvac_mode(self, hvac_mode: str) -> None:
        if hvac_mode == HVACMode.OFF:
            self.turn_off()
        else:
            if not self._azc_device.is_on:
                self.turn_on()
            mode_map = {
                HVACMode.HEAT: "heat",
                HVACMode.COOL: "cool",
                HVACMode.DRY: "dehumidify",
                HVACMode.FAN_ONLY: "ventilate",
            }
            if hvac_mode in mode_map:
                self._azc_device.set_mode(mode_map[hvac_mode])

    def turn_on(self):
        self._azc_device.turn_on()

    def turn_off(self):
        self._azc_device.turn_off()

    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE
