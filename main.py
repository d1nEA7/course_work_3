from api_connect import ConnNominatim, ConnAPIOpensky
from DBMngr import DBManager


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
    "Australia"
]
for country in countries:

    result_country = ConnNominatim(country).connect_nominatim()

    if result_country is None:
        print(f"Не удалось получить координаты для страны: {country}")
        continue

    lamin = float(result_country[0])
    lomin = float(result_country[2])
    lamax = float(result_country[1])
    lomax = float(result_country[3])

    aircraft_data = ConnAPIOpensky(
        lamin,
        lomin,
        lamax,
        lomax
    ).connect_opensky()

    #for aircraft in aircraft_data["states"]:
        #print(aircraft)

    db = DBManager()

    db.connect_to_db(
        "course_work_3",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

    country_id = db.add_country(
        country,
        lamin,
        lomin,
        lamax,
        lomax
    )

    for aircraft in aircraft_data["states"]:
        db.add_aeroplane(
            aircraft[0],
            aircraft[1].strip(),
            aircraft[2],
            aircraft[5],
            aircraft[6],
            aircraft[9],
            country_id
        )

print(db.get_aeroplanes_with_keyword("ACA"))