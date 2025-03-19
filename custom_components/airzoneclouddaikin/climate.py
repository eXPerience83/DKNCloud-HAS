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

HVAC_MODE_AUTO = "auto"  # Renombrado de "heat-cold-auto"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the climate platform from a config entry."""
    config = entry.data
    username = config.get("username")
    password = config.get("password")
    if not username or not password:
        _LOGGER.error("Missing username or password")
        return
    from homeassistant.helpers.aiohttp_client import async_get_clientsession
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
            entities.append(AirzoneClimate(api, device, config))
    async_add_entities(entities, True)

class AirzoneClimate(ClimateEntity):
    """Representation of an Airzone Cloud Daikin climate device."""

    def __init__(self, api: AirzoneAPI, device_data: dict, config: dict):
        """Initialize the climate entity.
        
        :param api: The AirzoneAPI instance.
        :param device_data: Dictionary with device information.
        :param config: Integration configuration (contains, e.g., force_hvac_mode_auto).
        """
        self._api = api
        self._device_data = device_data
        self._config = config
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
        
        Se incluyen los modos estándar y, si se ha habilitado 'force_hvac_mode_auto'
        en la configuración, se añade HVAC_MODE_AUTO.
        """
        modes = [HVAC_MODE_OFF, HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_FAN_ONLY, HVAC_MODE_DRY]
        if self._config.get("force_hvac_mode_auto", False):
            modes.append(HVAC_MODE_AUTO)
        return modes

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
        """Return a list of valid fan speeds based on 'availables_speeds' from device data.
        
        The API returns 'availables_speeds' as a string (e.g., "3" or "4"). Default is 3.
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
        self._hvac_mode = HVAC_MODE_HEAT  # Por defecto, se asume que se enciende en modo heat.
        self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off the device by sending P1=0."""
        self._send_command("P1", 0)
        self._hvac_mode = HVAC_MODE_OFF
        self.schedule_update_ha_state()

    def set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode.
        
        Mapea los siguientes modos:
         - HVAC_MODE_COOL -> P2=1
         - HVAC_MODE_HEAT -> P2=2
         - HVAC_MODE_FAN_ONLY -> P2=3
         - HVAC_MODE_DRY -> P2=5
         - HVAC_MODE_AUTO -> P2=4 (modo automático forzado, si se habilita en la configuración)
        """
        mode_mapping = {
            HVAC_MODE_COOL: "1",
            HVAC_MODE_HEAT: "2",
            HVAC_MODE_FAN_ONLY: "3",
            HVAC_MODE_DRY: "5",
            HVAC_MODE_AUTO: "4",
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
        Para modo heat (o HVAC_MODE_AUTO) se usa P8; para modo cool se usa P7.
        Se usan los rangos de temperatura proporcionados por la API y se fuerza un valor entero formateado con ".0".
        """
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            temp = int(float(temp))  # Se convierte a entero
            # Seleccionamos límites según el modo
            if self._hvac_mode in [HVAC_MODE_HEAT, HVAC_MODE_AUTO]:
                min_temp = int(float(self._device_data.get("min_limit_heat", 16)))
                max_temp = int(float(self._device_data.get("max_limit_heat", 32)))
                command = "P8"
            else:
                min_temp = int(float(self._device_data.get("min_limit_cold", 16)))
                max_temp = int(float(self._device_data.get("max_limit_cold", 32)))
                command = "P7"
            if temp < min_temp:
                temp = min_temp
            elif temp > max_temp:
                temp = max_temp
            self._send_command(command, f"{temp}.0")
            self._target_temperature = temp
            self.schedule_update_ha_state()

    def set_fan_speed(self, speed):
        """Set the fan speed.
        
        Usa P3 para modos de ventilación en frío y P4 para modos de calor (HVAC_MODE_AUTO).
        """
        try:
            speed = int(speed)
        except ValueError:
            _LOGGER.error("Invalid fan speed: %s", speed)
            return
        if speed not in self.fan_speed_range:
            _LOGGER.error("Fan speed %s not in valid range %s", speed, self.fan_speed_range)
            return
        if self._hvac_mode in [HVAC_MODE_COOL] or self._hvac_mode == "ventilate":
            self._send_command("P3", speed)
        elif self._hvac_mode in [HVAC_MODE_HEAT, HVAC_MODE_AUTO]:
            self._send_command("P4", speed)
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
