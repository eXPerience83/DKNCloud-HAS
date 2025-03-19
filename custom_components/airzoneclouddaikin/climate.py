"""Climate platform for DKN Cloud for HASS using the Airzone Cloud API."""
import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF, HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_FAN_ONLY, HVAC_MODE_DRY, SUPPORT_TARGET_TEMPERATURE
)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from .const import DOMAIN
from .airzone_api import AirzoneAPI

_LOGGER = logging.getLogger(__name__)

class AirzoneClimate(ClimateEntity):
    """Representation of an Airzone Cloud Daikin climate device."""

    def __init__(self, api: AirzoneAPI, device_data: dict):
        """Initialize the climate entity.
        
        :param api: The AirzoneAPI instance.
        :param device_data: Dictionary with device information.
        """
        self._api = api
        self._device_data = device_data
        self._name = device_data.get("name", "Airzone Device")
        self._device_id = device_data.get("id")
        self._hvac_mode = HVAC_MODE_OFF
        self._target_temperature = None

    @property
    def name(self):
        """Return the name of the climate entity."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def hvac_modes(self):
        """Return the list of supported HVAC modes.
        
        Se añaden los modos estándar y se incluye 'heat-cold-auto' (P2=4) como opción forzada bajo responsabilidad del usuario.
        """
        return [HVAC_MODE_OFF, HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_FAN_ONLY, HVAC_MODE_DRY, "heat-cold-auto"]

    @property
    def hvac_mode(self):
        """Return the current HVAC mode."""
        return self._hvac_mode

    @property
    def target_temperature(self):
        """Return the current target temperature."""
        return self._target_temperature

    @property
    def supported_features(self):
        """Return the supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def fan_speed_range(self):
        """Return a list of valid fan speeds based on the available speeds from device data.
        
        The API returns 'availables_speeds' as a string (e.g., "3" or "4").
        If not present, default to 3.
        """
        speeds_str = self._device_data.get("availables_speeds", "3")
        try:
            speeds = int(speeds_str)
        except ValueError:
            speeds = 3
        return list(range(1, speeds + 1))

    def turn_on(self):
        """Turn on the device by sending P1=1."""
        self._send_command("P1", 1)
        # Se asume que al encender se activa un modo por defecto, por ejemplo, heat.
        self._hvac_mode = HVAC_MODE_HEAT
        self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off the device by sending P1=0."""
        self._send_command("P1", 0)
        self._hvac_mode = HVAC_MODE_OFF
        self.schedule_update_ha_state()

    def set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode.
        
        Mapea los siguientes modos:
         - HVAC_MODE_HEAT -> P2=2
         - HVAC_MODE_COOL -> P2=1
         - HVAC_MODE_FAN_ONLY -> P2=3
         - HVAC_MODE_DRY -> P2=5
         - "heat-cold-auto" -> P2=4 (modo automático forzado bajo responsabilidad del usuario)
        """
        mode_mapping = {
            HVAC_MODE_HEAT: "2",
            HVAC_MODE_COOL: "1",
            HVAC_MODE_FAN_ONLY: "3",
            HVAC_MODE_DRY: "5",
            "heat-cold-auto": "4",
        }
        if hvac_mode in mode_mapping:
            self._send_command("P2", mode_mapping[hvac_mode])
            self._hvac_mode = hvac_mode
            self.schedule_update_ha_state()
        else:
            _LOGGER.error("Unsupported HVAC mode: %s", hvac_mode)

    def set_temperature(self, **kwargs):
        """Set the target temperature.

        Debe llamarse después de haber cambiado el modo.
        Para modo heat (o heat-cold-auto) se usa P8; para modo cool se usa P7.
        El valor debe enviarse con decimales (por ejemplo, "23.0").
        """
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            temp = float(temp)
            if self._hvac_mode in [HVAC_MODE_HEAT, "heat-cold-auto"]:
                self._send_command("P8", f"{temp:.1f}")
            else:
                self._send_command("P7", f"{temp:.1f}")
            self._target_temperature = temp
            self.schedule_update_ha_state()

    def _send_command(self, option, value):
        """Send a command to the device using the events endpoint."""
        payload = {
            "event": {
                "cgi": "modmaquina",
                "device_id": self._device_id,
                "option": option,
                "value": value,
            }
        }
        _LOGGER.info("Sending command: %s", payload)
        self._api._send_event(payload)
