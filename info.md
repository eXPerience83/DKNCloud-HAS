-------------------------------------------------------
Detailed Information on "Px" Modes and Example Curl Commands
-------------------------------------------------------

1. Login and Obtain Token  
   Command:  
   curl -v -X POST "https://dkn.airzonecloud.com/users/sign_in" -H "Content-Type: application/json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"email\": \"YOUR_EMAIL@example.com\", \"password\": \"YOUR_PASSWORD\"}"  
   Expected response: JSON containing "authentication_token".

2. Get Installations  
   Command:  
   curl -v "https://dkn.airzonecloud.com/installation_relations/?format=json&user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

3. Get Devices  
   Command:  
   curl -v "https://dkn.airzonecloud.com/devices/?format=json&installation_id=YOUR_INSTALLATION_ID&user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

4. Mode Mapping (Px Options)  
   Original mapping from max13fr:

   MODES_CONVERTER = {
       "1": {"name": "cool", "type": "cold", "description": "Cooling mode"},
       "2": {"name": "heat", "type": "heat", "description": "Heating mode"},
       "3": {"name": "ventilate", "type": "cold", "description": "Ventilation in cold mode"},
       "4": {"name": "heat-cold-auto", "type": "cold", "description": "Auto mode"},
       "5": {"name": "dehumidify", "type": "cold", "description": "Dry mode"},
       "6": {"name": "cool-air", "type": "cold", "description": "Automatic cooling"},
       "7": {"name": "heat-air", "type": "heat", "description": "Automatic heating"},
       "8": {"name": "ventilate", "type": "heat", "description": "Ventilation in heating mode"}
   }
   
   In our tests (with the ADEQ125B2VEB model), the following produced an effect:
   - P1: Power On/Off.
   - P2: "1" → cool, "2" → heat, "3" → ventilate, "4" → Auto mode (if forced via configuration), "5" → dehumidify.
   - P3: Fan speed for cold/ventilate (values: 1, 2, 3).
   - P4: Fan speed for heat/auto (values: 1, 2, 3).
   - P7: Temperature setting for cold (e.g., "25.0").
   - P8: Temperature setting for heat (e.g., "23.0").

5. Example Curl Commands for Events  
   (Replace YOUR_EMAIL@example.com, YOUR_TOKEN, YOUR_DEVICE_ID, and YOUR_INSTALLATION_ID with generic placeholders.)

   - Power On (P1=1):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P1\", \"value\": 1}}"

   - Power Off (P1=0):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P1\", \"value\": 0}}"

   - Change Mode to HEAT (P2=2):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P2\", \"value\": \"2\"}}"

   - Force Auto Mode (HVACMode.AUTO) (P2=4):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P2\", \"value\": \"4\"}}"

   - Set Temperature to 23°C in heat mode (P8):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P8\", \"value\": \"23.0\"}}"

   - Set Temperature to 25°C in cold mode (P7):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P7\", \"value\": \"25.0\"}}"

-------------------------------------------------------

Device Raw Data Example:
{
    "id": "...",
    "mac": "AA:BB:CC:DD:EE:FF",
    "pin": "1234",
    "name": "Dknwserver",
    "status": "activated",
    "mode": "1",
    "state": null,
    "power": "0",
    "units": "0",
    "availables_speeds": "2",
    "local_temp": "26.0",
    "ver_state_slats": "0",
    "ver_position_slats": "0",
    "hor_state_slats": "0",
    "hor_position_slats": "0",
    "max_limit_cold": "32.0",
    "min_limit_cold": "16.0",
    "max_limit_heat": "32.0",
    "min_limit_heat": "16.0",
    "update_date": null,
    "progs_enabled": false,
    "scenary": "sleep",
    "sleep_time": 60,
    "min_temp_unoccupied": "16",
    "max_temp_unoccupied": "32",
    "connection_date": "2020-05-23T05:37:22.000+00:00",
    "last_event_id": "...",
    "firmware": "1.1.1",
    "brand": "Daikin",
    "cold_consign": "26.0",
    "heat_consign": "24.0",
    "cold_speed": "2",
    "heat_speed": "2",
    "machine_errors": null,
    "ver_cold_slats": "0001",
    "ver_heat_slats": "0000",
    "hor_cold_slats": "0000",
    "hor_heat_slats": "0000",
    "modes": "11101000",
    "installation_id": "...",
    "time_zone": "Europe/Madrid",
    "spot_name": "Madrid",
    "complete_name": "Madrid,Madrid,Community of Madrid,Spain",
    "location": {"latitude": 10.4155754, "longitude": -2.4037901998979576}
}
