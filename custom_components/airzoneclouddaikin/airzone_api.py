"""Module to interact with the Airzone Cloud API (adapted for dkn.airzonecloud.com).

This module implements:
- Authentication via the /users/sign_in endpoint.
- Fetching installations via the /api/installation_relations endpoint.

Refer to: https://developers.airzonecloud.com/docs/web-api for API details.
"""

import logging
import aiohttp
from typing import List, Dict

_LOGGER = logging.getLogger(__name__)

# Base URL as defined in the original package
BASE_URL = "https://dkn.airzonecloud.com"

# Update the login endpoint based on network inspection
API_LOGIN = "/users/sign_in"
# Assuming the installation relations endpoint remains with /api prefix; si no, se debe ajustar también.
API_INSTALLATION_RELATIONS = "/api/installation_relations"
API_DEVICES = "/api/devices"
API_EVENTS = "/api/events"

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
        
        Sends a POST request to the /users/sign_in endpoint.
        Returns True if successful, False otherwise.
        """
        url = f"{BASE_URL}{API_LOGIN}"
        payload = {"email": self._username, "password": self._password}
        headers = {"User-Agent": "DKNCloudForHASS/0.1.4"}
        try:
            async with self._session.post(url, json=payload, headers=headers) as response:
                if response.status == 201:  # 201 Created is expected
                    data = await response.json()
                    # In the original library, the token is obtained from data["user"]["authentication_token"]
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
        
        Sends a GET request to the /api/installation_relations endpoint.
        Returns a list of installations if successful.
        """
        if not self.token:
            _LOGGER.error("Cannot fetch installations without a valid token.")
            return []
        url = f"{BASE_URL}{API_INSTALLATION_RELATIONS}"
        params = {"format": "json"}
        headers = {
            "User-Agent": "DKNCloudForHASS/0.1.4",
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
