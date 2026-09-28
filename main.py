import os

from dotenv import load_dotenv

from api_connect import ConnAPIOpensky, ConnNominatim
from DBMngr import DBManager

load_dotenv()
countries = [
    "Russia",
    "France",
    "Germany",
    "Poland",
    "Italy",
    "Spain",
    "United Kingdom",
    "Canada",
    "Japan",
    "Australia",
]

params = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

db = DBManager()

db.connect_to_db("course_work_3", **params)


# Очищаем старые данные о самолётах
db.clear_aeroplanes("course_work_3", **params)


for country in countries:

    result_country = ConnNominatim(country).connect_nominatim()

    if result_country is None:
        print(f"Не удалось получить координаты для страны: {country}")
        continue

    lamin = float(result_country[0])
    lomin = float(result_country[2])
    lamax = float(result_country[1])
    lomax = float(result_country[3])

    aircraft_data = ConnAPIOpensky(lamin, lomin, lamax, lomax).connect_opensky()

    if aircraft_data is None:
        print(f"Не удалось получить самолёты для страны: {country}")
        continue

    country_id = db.add_country(
        country, lamin, lomin, lamax, lomax, "course_work_3", **params
    )

    db.add_aeroplanes(aircraft_data["states"], country_id, "course_work_3", **params)


print(db.get_countries_and_aeroplanes_count("course_work_3", **params))
