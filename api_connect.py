import json

import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class ConnAPIOpensky:
    """класс получения данных апи open sky самолёты в воздушных пространствах"""
    url = "https://opensky-network.org/api/states/all"
    def __init__(self, lamin, lomin, lamax, lomax):
        self.lamin = lamin          #координаты сетки
        self.lomin = lomin          #координаты сетки
        self.lamax = lamax          #координаты сетки
        self.lomax = lomax          #координаты сетки

    def connect_opensky(self):

        params = {
            "lamin": self.lamin,
            "lomin": self.lomin,
            "lamax": self.lamax,
            "lomax": self.lomax,
        }
        try:
            response = requests.get(self.url, params=params, timeout=3)
            print(response.status_code)
            print(response.text)
            return response.json()

        except:
            print("ошибка")


# result = requests.get("https://opensky-network.org/api/states/all?lamin=45.8389&lomin=5.9962&lamax=47.8229&lomax=10.5226", timeout=3)
# print(result.status_code)
# data = result.json()

# for state in data["states"]:
#     print(state)

class  ConnNominatim:
    url = "https://nominatim.openstreetmap.org/search"
    """класс получение географических координат страны"""

    def __init__(self,country):
        self.country = country

    def connect_nominatim(self):              #1.2.3.4
        params = {
            "q": self.country,
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        headers = {"User-Agent": "MyFlightApp/1.0 (contact @ example.com)"}
        try:
            response = requests.get(self.url, params=params, headers=headers, timeout=3)
            repos = response.json()
            return repos[0].get("boundingbox")
        except:
            print("ошибка подключения")

#result_country = ConnNominatim("russia").connect_nominatim()
#print(result_country)

#lamin = float(result_country[0])
#lomin = float(result_country[2])
#lamax = float(result_country[1])
#lomax = float(result_country[3])

#aircraft_1 = ConnAPIOpensky(lamin, lomin, lamax, lomax).connect_opensky()
#print(json.dumps(aircraft_1, indent=4))