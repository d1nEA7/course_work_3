from api_connect import ConnNominatim, ConnAPIOpensky
from DBMngr import DBManager


country = "Russia"

result_country = ConnNominatim(country).connect_nominatim()

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

for aircraft in aircraft_data["states"]:
    print(aircraft)

db = DBManager()

db.connect_to_db(
    "course_work_3",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

db.add_country(
    country,
    lamin,
    lomin,
    lamax,
    lomax
)
print(db.get_countries_and_aeroplanes_count())