import requests
import time

time.sleep(2)  # wait for API to start

try:
    resp = requests.get("http://api:5000/")
    print("Klient otrzymał:", resp.text)
except Exception as e:
    print("Błąd klienta:", e)
