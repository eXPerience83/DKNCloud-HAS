"""Constants for DKN Cloud for HASS integration.

This file includes the API endpoints.
"""

DOMAIN = "airzoneclouddaikin"
CONF_USERNAME = "username"      # Replace with your Airzone Cloud account email when configuring
CONF_PASSWORD = "password"      # Replace with your Airzone Cloud account password when configuring

# API Endpoints as defined in the original package
API_LOGIN = "/users/sign_in"
API_INSTALLATION_RELATIONS = "/installation_relations"
API_DEVICES = "/devices"
API_EVENTS = "/events"

BASE_URL = "https://dkn.airzonecloud.com"
