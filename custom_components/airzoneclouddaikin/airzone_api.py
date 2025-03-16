"""Module to interact with the Airzone Cloud API (adapted for dkn.airzonecloud.com).

This module implements:
- Authentication via the /login endpoint.
- Fetching installations via the /installation_relations endpoint.

Refer to: https://developers.airzonecloud.com/docs/web-api for API details.
"""

import logging
import aiohttp
from typing import List, Dict

_LOGGER = logging.getLogger(__name__)

# Base URL as used in the official AirzoneCloudDaikin package
BASE_URL = "https://dkn.airzonecloud.com"

# Endpoints as defined in the original package
API_LOGIN = "/login"
API_INSTALLATION_RELATIONS = "/installation_relations"
API_DEVICES = "/devices"
API_EVENTS = "/events"

class AirzoneAPI:
    """Client to interact with the Airzone Cloud API."""

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        """Initialize with user credentials and an aiohttp session."""
        self._username = username
        self._password = password
        self._session = session
        self.token: str = ""
        self.installations: List[Dict] = []

    async def login(self) -> bool:
        """Authenticate with the API and obtain a token.

        Sends a POST request to the /login endpoint.
        Returns True if successful, False otherwise.
        """
        url = f"{BASE_URL}{API_LOGIN}"
        payload = {"email": self._username, "password": self._password}
        headers = {"User-Agent": "DKNCloudForHASS/0.1.3"}
        try:
            async with self._session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Según el código original, el token se obtiene de response["user"]["authentication_token"]
                    self.token = data.get("user", {}).get("authentication_token", "")
                    if self.token:
                        _LOGGER.debug("Login successful, token: %s", self.token)
                        return True
                    else:
                        _LOGGER.error("Login failed: No token received.")
                        return False
                else:
                    _LOGGER.error("Login failed, status code: %s", response.status)
                    return False
        except Exception as err:
            _LOGGER.error("Exception during login: %s", err)
            return False

    async def fetch_installations(self) -> List[Dict]:
        """Fetch installations using the obtained token.

        Sends a GET request to the /installation_relations endpoint.
        Returns a list of installations if successful.
        """
        if not self.token:
            _LOGGER.error("Cannot fetch installations without a valid token.")
            return []
        # La API original usa /installation_relations para obtener las instalaciones.
        url = f"{BASE_URL}{API_INSTALLATION_RELATIONS}"
        params = {"format": "json"}
        headers = {
            "User-Agent": "DKNCloudForHASS/0.1.3",
            "Authorization": f"Bearer {self.token}",
        }
        try:
            async with self._session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    installations = data.get("installation_relations", [])
                    _LOGGER.debug("Fetched installations: %s", installations)
                    return installations
                else:
                    _LOGGER.error("Failed to fetch installations, status code: %s", response.status)
                    return []
        except Exception as err:
            _LOGGER.error("Exception fetching installations: %s", err)
            return []
