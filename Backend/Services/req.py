from dotenv import load_dotenv
import requests
import os

load_dotenv()
XIRSYS_ENDPOINT = ""
XIRSYS_code =  os.getenv("XIRSYS_SECRET")
username = "warishayat" 
app_name = "ChatAPP" 
url = f"https://{username}:{XIRSYS_code}@global.xirsys.net/_turn/{app_name}"
response = requests.put(url, json={"format": "urls"})
ice_servers = response.json()["v"]["iceServers"]
print(ice_servers)