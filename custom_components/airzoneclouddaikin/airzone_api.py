import logging
import aiohttp
from typing import List, Dict

_LOGGER = logging.getLogger(__name__)

# Base URL según la biblioteca original
BASE_URL = "https://dkn.airzonecloud.com"

# Endpoints definidos sin el prefijo /api, tal como en la biblioteca original
API_LOGIN = "/login"
API_INSTALLATION_RELATIONS = "/installation_relations"
API_DEVICES = "/devices"
API_EVENTS = "/events"

class AirzoneAPI:
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self._username = username
        self._password = password
        self._session = session
        self.token: str = ""
        self.installations: List[Dict] = []

    async def login(self) -> bool:
        url = f"{BASE_URL}{API_LOGIN}"
        payload = {"email": self._username, "password": self._password}
        headers = {"User-Agent": "DKNCloudForHASS/0.1.x"}
        try:
            async with self._session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
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
        if not self.token:
            _LOGGER.error("Cannot fetch installations without a valid token.")
            return []
        url = f"{BASE_URL}{API_INSTALLATION_RELATIONS}"
        params = {"format": "json"}
        headers = {
            "User-Agent": "DKNCloudForHASS/0.1.x",
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
