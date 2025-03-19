"""Constants for DKN Cloud for HASS integration.

This file includes the API endpoints.
"""

DOMAIN = "airzoneclouddaikin"
CONF_USERNAME = "username"      # Use your Airzone Cloud account email in configuration
CONF_PASSWORD = "password"      # Use your Airzone Cloud account password in configuration

# API Endpoints (as defined in the original package)
API_LOGIN = "/users/sign_in"
API_INSTALLATION_RELATIONS = "/installation_relations"
API_DEVICES = "/devices"
API_EVENTS = "/events"

BASE_URL = "https://dkn.airzonecloud.com"
