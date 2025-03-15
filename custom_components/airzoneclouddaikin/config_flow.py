"""Config flow para DKN Airzone Cloud."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv

DOMAIN = "airzoneclouddaikin"
# Usaremos "scan_interval" como clave personalizada.
CONF_SCAN_INTERVAL = "scan_interval"

_LOGGER = logging.getLogger(__name__)

# Definimos el schema de datos. Se usa el valor por defecto de 10 segundos.
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_SCAN_INTERVAL, default=10): vol.Coerce(int),
})

class AirzoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el config flow para la integración DKN Airzone Cloud."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> dict:
        """Paso inicial del config flow."""
        errors = {}

        if user_input is not None:
            # Validar que el scan_interval sea un entero mayor a 0
            try:
                scan_interval = int(user_input.get(CONF_SCAN_INTERVAL))
                if scan_interval < 1:
                    errors[CONF_SCAN_INTERVAL] = "scan_interval_no_valido"
            except ValueError:
                errors[CONF_SCAN_INTERVAL] = "scan_interval_no_valido"

            # Se podría incluir aquí alguna validación extra (por ejemplo, intentar conectarse a la API de Airzone y comprobar credenciales).
            if not errors:
                # Se crea la configuración con los datos validados.
                return self.async_create_entry(
                    title="DKN Airzone Cloud",
                    data=user_input,
                )

        # Agregar en la descripción del campo scan_interval un mensaje de ayuda
        scan_interval_description = (
            "Valor en segundos. Por defecto 10. "
            "No se recomienda un valor inferior a 10 segundos para evitar ser baneado por Airzone."
        )
        # Construimos el esquema para mostrar el formulario.
        schema = vol.Schema({
            vol.Required(CONF_USERNAME): cv.string,
            vol.Required(CONF_PASSWORD): cv.string,
            vol.Required(CONF_SCAN_INTERVAL, default=user_input.get(CONF_SCAN_INTERVAL, 10) if user_input else 10):
                vol.All(vol.Coerce(int)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={"scan_interval_description": scan_interval_description},
        )
