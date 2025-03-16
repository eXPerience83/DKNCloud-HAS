"""Module to interact with the Airzone Cloud API (adapted for dkn.airzonecloud.com).

This module implements:
- Authentication via the /login endpoint.
- Fetching installations (and devices) via the /installations endpoint.

Refer to: https://developers.airzonecloud.com/docs/web-api for API details.
"""

import logging
import aiohttp
from typing import List, Dict

_LOGGER = logging.getLogger(__name__)

# Base URL for dkn.airzonecloud.com API; adjust if versioning is required (e.g., /api/v1)
BASE_URL = "https://dkn.airzonecloud.com/api"

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
        url = f"{BASE_URL}/login"
        payload = {"username": self._username, "password": self._password}
        try:
            async with self._session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data.get("token", "")
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
        
        Sends a GET request to the /installations endpoint.
        Returns a list of installations if successful.
        """
        if not self.token:
            _LOGGER.error("Cannot fetch installations without a valid token.")
            return []
        url = f"{BASE_URL}/installations"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            async with self._session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.installations = data.get("installations", [])
                    _LOGGER.debug("Fetched installations: %s", self.installations)
                    return self.installations
                else:
                    _LOGGER.error("Failed to fetch installations, status code: %s", response.status)
                    return []
        except Exception as err:
            _LOGGER.error("Exception fetching installations: %s", err)
            return []
