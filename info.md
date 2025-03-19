Información Detallada sobre Modos "Px" y Ejemplos de Comandos Curl
-------------------------------------------------------

1. Login y Obtención del Token  
   Comando:
   curl -v -X POST "https://dkn.airzonecloud.com/users/sign_in" -H "Content-Type: application/json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"email\": \"YOUR_EMAIL@example.com\", \"password\": \"YOUR_PASSWORD\"}"
   Respuesta esperada: JSON con "authentication_token".

2. Obtener Instalaciones  
   curl -v "https://dkn.airzonecloud.com/installation_relations/?format=json" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -H "Authorization: Bearer YOUR_TOKEN"

3. Obtener Dispositivos  
   curl -v "https://dkn.airzonecloud.com/devices/?format=json&installation_id=YOUR_INSTALLATION_ID&user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

4. Mapeo de Modos (Opciones "P")  
   Según el paquete original de max13fr:
   
   MODES_CONVERTER = {
       "1": {"name": "cool", "type": "cold", "description": "Cooling mode"},
       "2": {"name": "heat", "type": "heat", "description": "Heating mode"},
       "3": {"name": "ventilate", "type": "cold", "description": "Ventilation in cold mode"},
       "4": {"name": "heat-cold-auto", "type": "cold", "description": "Auto mode"},
       "5": {"name": "dehumidify", "type": "cold", "description": "Dry mode"},
       "6": {"name": "cool-air", "type": "cold", "description": "Automatic cooling"},
       "7": {"name": "heat-air", "type": "heat", "description": "Automatic heating"},
       "8": {"name": "ventilate", "type": "heat", "description": "Ventilation in heating mode"},
   }
   
   En nuestras pruebas (con la máquina modelo ADEQ125B2VEB), solo han funcionado los siguientes:
   - P1: Encendido/Apagado.
   - P2: "1" → cool, "2" → heat, "3" → ventilate, "4" → heat-cold-auto (forzado si se activa en configuración), "5" → dehumidify.
   - P3: Velocidad del ventilador en modo frío (1, 2, 3).
   - P4: Velocidad del ventilador en modo calor (1, 2, 3).
   - P7: Ajuste de consigna para frío (enviar valores con decimales, por ejemplo, "25.0").
   - P8: Ajuste de consigna para calor (enviar valores con decimales, por ejemplo, "23.0").

5. Ejemplos de Comandos Curl para Eventos  
   (Reemplaza YOUR_EMAIL@example.com, YOUR_TOKEN, YOUR_DEVICE_ID y YOUR_INSTALLATION_ID por tus datos)
   
   - Encender el dispositivo (P1=1):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P1\", \"value\": 1}}"
   
   - Apagar el dispositivo (P1=0):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P1\", \"value\": 0}}"
   
   - Cambiar el modo a HEAT (P2=2):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P2\", \"value\": \"2\"}}"
   
   - Forzar modo automático (heat-cold-auto) (P2=4):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P2\", \"value\": \"4\"}}"
   
   - Ajustar temperatura a 23°C en modo calor (P8):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P8\", \"value\": \"23.0\"}}"
   
   - Ajustar temperatura a 25°C en modo frío (P7):  
     curl -v "https://dkn.airzonecloud.com/events/?user_email=YOUR_EMAIL@example.com&user_token=YOUR_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/json;charset=UTF-8" -H "Accept: application/json, text/plain, */*" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -d "{\"event\": {\"cgi\": \"modmaquina\", \"device_id\": \"YOUR_DEVICE_ID\", \"option\": \"P7\", \"value\": \"25.0\"}}"
