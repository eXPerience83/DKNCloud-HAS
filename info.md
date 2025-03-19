Detailed Information on "Px" Modes and Example Curl Commands

    Login and Obtain Token
    Command:
    curl -v -X POST "https://dkn.airzonecloud.com/users/sign_in" -H "Content-Type: application/json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"email": "YOUR_EMAIL@example.com", "password": "YOUR_PASSWORD"}"
    Expected response: JSON containing "authentication_token".

    Get Installations
    (Includes user_email and user_token as query parameters)
    curl -v "https://dkn.airzonecloud.com/installation_relations/?format=json&user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    Get Devices
    curl -v "https://dkn.airzonecloud.com/devices/?format=json&installation_id=YOUR_INSTALLATION_ID&user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    Mode Mapping (Px Options)
    According to the original max13fr package:

    MODES_CONVERTER = { "1": {"name": "cool", "type": "cold", "description": "Cooling mode"}, "2": {"name": "heat", "type": "heat", "description": "Heating mode"}, "3": {"name": "ventilate", "type": "cold", "description": "Ventilation in cold mode"}, "4": {"name": "heat-cold-auto", "type": "cold", "description": "Auto mode"}, "5": {"name": "dehumidify", "type": "cold", "description": "Dry mode"}, "6": {"name": "cool-air", "type": "cold", "description": "Automatic cooling"}, "7": {"name": "heat-air", "type": "heat", "description": "Automatic heating"}, "8": {"name": "ventilate", "type": "heat", "description": "Ventilation in heating mode"} }

    In our tests (with the ADEQ125B2VEB model), only the following produced an effect:
        P1: Power On/Off.
        P2: "1" → cool, "2" → heat, "3" → ventilate, "4" → Auto mode (HVACMode.AUTO, if forced via configuration), "5" → dehumidify.
        P3: Fan speed for cold/ventilate (values: 1, 2, 3).
        P4: Fan speed for heat/auto (values: 1, 2, 3).
        P7: Temperature setting for cold (e.g., "25.0").
        P8: Temperature setting for heat (e.g., "23.0").

    Example Curl Commands for Events
    (Replace YOUR_EMAIL@example.com, YOUR_TOKEN, YOUR_DEVICE_ID, and YOUR_INSTALLATION_ID with your own data or generic placeholders)

        Power On (P1=1):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P1", "value": 1}}"

        Power Off (P1=0):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P1", "value": 0}}"

        Change Mode to HEAT (P2=2):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P2", "value": "2"}}"

        Force Auto Mode (HVACMode.AUTO) (P2=4):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P2", "value": "4"}}"

        Set Temperature to 23°C in heat mode (P8):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P8", "value": "23.0"}}"

        Set Temperature to 25°C in cold mode (P7):
        curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, /" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{"event": {"cgi": "modmaquina", "device_id": "YOUR_DEVICE_ID", "option": "P7", "value": "25.0"}}"
