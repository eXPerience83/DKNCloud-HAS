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

# Importar la biblioteca externa
from AirzoneCloudDaikin import AirzoneCloudDaikin

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
        # Si la biblioteca requiere un paso adicional para iniciar sesión, por ejemplo:
        if hasattr(api, "login"):
            api.login()  # O bien: await api.async_login() si es asíncrono
    except Exception as err:
        _LOGGER.error("Error connecting to AirzoneCloudDaikin: %s", err)
        return

    installations = getattr(api, "installations", [])
    _LOGGER.debug("Found %d installations", len(installations))
    if not installations:
        _LOGGER.warning("No installations found. Verify your credentials and API availability.")

    entities = []
    for installation in installations:
        # Asegurarse de que installation tiene el atributo devices
        devices = getattr(installation, "devices", [])
        for device in devices:
            entities.append(AirzonecloudDaikinDevice(device))

    if not entities:
        _LOGGER.warning("No devices found in the API response.")
    async_add_entities(entities, True)

class AirzonecloudDaikinDevice(ClimateEntity):
    """Representation of an AirzoneCloud Daikin Device."""

    def __init__(self, azc_device: Any):
        """Initialize the device."""
        self._azc_device = azc_device
        _LOGGER.info("Initializing device %s (%s)", self.name, self.unique_id)

    @property
    def unique_id(self) -> Optional[str]:
        """Return a unique ID."""
        return f"device_{self._azc_device.id}"

    @property
    def name(self) -> str:
        """Return the name of the device."""
        installation_name = getattr(self._azc_device, "installation", {}).get("name", "Unknown")
        return f"{installation_name} - {self._azc_device.name}"

    @property
    def temperature_unit(self) -> str:
        """Return the temperature unit."""
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation mode."""
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
        """Return the list of available hvac operation modes."""
        return AIRZONECLOUD_DEVICE_HVAC_MODES

    @property
    def current_temperature(self) -> Optional[float]:
        """Return the current temperature."""
        return self._azc_device.current_temperature

    @property
    def target_temperature(self) -> Optional[float]:
        """Return the target temperature."""
        return self._azc_device.target_temperature

    def set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            self._azc_device.set_temperature(round(float(temperature), 1))

    def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
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

    def turn_on(self) -> None:
        """Turn on the device."""
        self._azc_device.turn_on()

    def turn_off(self) -> None:
        """Turn off the device."""
        self._azc_device.turn_off()

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE
