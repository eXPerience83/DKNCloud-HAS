"""Climate platform for DKN Cloud for HASS using the Airzone Cloud API."""
import asyncio
import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from .const import DOMAIN
from .airzone_api import AirzoneAPI

_LOGGER = logging.getLogger(__name__)

# Forced Auto mode constant
HVAC_MODE_AUTO = HVACMode("auto")

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the climate platform from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
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
            entities.append(AirzoneClimate(api, device, entry.data, hass))
    async_add_entities(entities, True)

class AirzoneClimate(ClimateEntity):
    """Representation of an Airzone Cloud Daikin climate device."""

    def __init__(self, api: AirzoneAPI, device_data: dict, config: dict, hass):
        """Initialize the climate entity."""
        self._api = api
        self._device_data = device_data
        self._config = config
        self._name = device_data.get("name", "Airzone Device")
        self._device_id = device_data.get("id")
        # Initialize HVAC mode from device data if available; otherwise default to off.
        self._hvac_mode = HVACMode("off")
        self._target_temperature = None
        self._fan_mode = None  # current fan speed as string
        self.hass = hass

    @property
    def unique_id(self):
        """Return a unique ID for this climate entity."""
        return self._device_id

    @property
    def name(self):
        """Return the name of the climate entity."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_modes(self):
        """Return supported HVAC modes.
        
        Standard modes are: off, cool, heat, fan_only, and dry. If force_hvac_mode_auto is enabled,
        HVAC_MODE_AUTO is added.
        """
        modes = [HVACMode.OFF, HVACMode.COOL, HVACMode.HEAT, HVACMode.FAN_ONLY, HVACMode.DRY]
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
        """Return supported features: target temperature and fan mode."""
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE

    @property
    def fan_modes(self):
        """Return a list of valid fan speeds as strings."""
        speeds = self.fan_speed_range
        return [str(speed) for speed in speeds]

    @property
    def fan_mode(self):
        """Return the current fan speed."""
        return self._fan_mode

    @property
    def device_info(self):
        """Return device info for grouping in the HA device registry."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_data.get("name"),
            "manufacturer": self._device_data.get("brand", "Daikin"),
            "model": self._device_data.get("firmware", "Unknown"),
        }

    async def async_update(self):
        """Poll updated device data from the API and update the entity state."""
        installations = await self._api.fetch_installations()
        for relation in installations:
            installation = relation.get("installation")
            if installation and installation.get("id") == self._device_data.get("installation_id"):
                devices = await self._api.fetch_devices(installation.get("id"))
                for dev in devices:
                    if dev.get("id") == self._device_id:
                        self._device_data = dev
                        # Update HVAC mode based on power and mode fields.
                        if int(dev.get("power", 0)) == 1:
                            mode_val = dev.get("mode")
                            if mode_val == "1":
                                self._hvac_mode = HVACMode.COOL
                            elif mode_val == "2":
                                self._hvac_mode = HVACMode.HEAT
                            elif mode_val == "3":
                                self._hvac_mode = HVACMode.FAN_ONLY
                            elif mode_val == "5":
                                self._hvac_mode = HVACMode.DRY
                            elif mode_val == "4":
                                self._hvac_mode = HVAC_MODE_AUTO
                            else:
                                self._hvac_mode = HVACMode.HEAT
                        else:
                            self._hvac_mode = HVACMode.OFF
                        # Update target temperature.
                        if self._hvac_mode in [HVACMode.HEAT, HVAC_MODE_AUTO]:
                            self._target_temperature = int(float(dev.get("heat_consign", "0")))
                        else:
                            self._target_temperature = int(float(dev.get("cold_consign", "0")))
                        # Update fan speed.
                        self._fan_mode = str(dev.get("current_fan_speed", ""))
                        break
        self.async_write_ha_state()

    def turn_on(self):
        """Turn on the device (send P1=1)."""
        self._send_command("P1", 1)
        self.schedule_update_ha_state()

    def turn_off(self):
        """Turn off the device (send P1=0)."""
        self._send_command("P1", 0)
        self._hvac_mode = HVACMode.OFF
        self.schedule_update_ha_state()

    def set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode.
        
        If hvac_mode is a string, convert it to HVACMode.
        Mapping:
          - HVACMode.OFF: call turn_off() and return.
          - HVACMode.COOL -> P2=1
          - HVACMode.HEAT -> P2=2
          - HVACMode.FAN_ONLY -> P2=3
          - HVACMode.DRY -> P2=5
          - HVAC_MODE_AUTO -> P2=4
        """
        if isinstance(hvac_mode, str):
            hvac_mode = HVACMode(hvac_mode)
        if hvac_mode == HVACMode.OFF:
            self.turn_off()
            return
        mode_mapping = {
            HVACMode.COOL: "1",
            HVACMode.HEAT: "2",
            HVACMode.FAN_ONLY: "3",
            HVACMode.DRY: "5",
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
        
        Must be called after changing the mode.
        For HEAT or AUTO modes, use P8; for COOL mode use P7.
        Temperature adjustments are disabled in DRY and FAN_ONLY modes.
        """
        if self._hvac_mode in [HVACMode.DRY, HVACMode.FAN_ONLY]:
            _LOGGER.warning("Temperature adjustment not supported in mode %s", self._hvac_mode)
            return
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is not None:
            temp = int(float(temp))
            if self._hvac_mode in [HVACMode.HEAT, HVAC_MODE_AUTO]:
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
        
        Uses P3 for COOL and FAN_ONLY modes, and P4 for HEAT/AUTO modes.
        Fan speed adjustment is disabled in DRY mode.
        """
        try:
            speed = int(speed)
        except ValueError:
            _LOGGER.error("Invalid fan speed: %s", speed)
            return
        if speed not in self.fan_speed_range:
            _LOGGER.error("Fan speed %s not in valid range %s", speed, self.fan_speed_range)
            return
        if self._hvac_mode == HVACMode.DRY:
            _LOGGER.warning("Fan speed adjustment not supported in DRY mode")
            return
        if self._hvac_mode in [HVACMode.COOL, HVACMode.FAN_ONLY]:
            self._send_command("P3", speed)
        elif self._hvac_mode in [HVACMode.HEAT, HVAC_MODE_AUTO]:
            self._send_command("P4", speed)
        self._fan_mode = str(speed)
        self.schedule_update_ha_state()

    def set_preset_mode(self, preset_mode):
        """Set the preset mode (if supported). Supported values: 'away', 'none'."""
        if preset_mode not in ["away", "none"]:
            _LOGGER.error("Unsupported preset mode: %s", preset_mode)
            return
        self._send_command("P5", preset_mode)
        self._device_data["preset_mode"] = preset_mode
        self.schedule_update_ha_state()

    @property
    def fan_speed_range(self):
        """Return a list of valid fan speeds based on 'availables_speeds' from device data."""
        speeds_str = self._device_data.get("availables_speeds", "3")
        try:
            speeds = int(speeds_str)
        except ValueError:
            speeds = 3
        return list(range(1, speeds + 1))

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
        # Use run_coroutine_threadsafe to safely schedule the async API call from a thread.
        asyncio.run_coroutine_threadsafe(self._api.send_event(payload), self.hass.loop)
