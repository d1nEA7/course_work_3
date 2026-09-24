import psycopg2

from api_connect import ConnAPIOpensky


class DBManager:
    def __init__(self):
        self.conn = None

    def connect_to_db(self, database_name, **params):
        """Подключение к базе данных и создание таблиц."""

        self.conn = psycopg2.connect(
            dbname=database_name,
            **params
        )

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    lamin FLOAT,
                    lomin FLOAT,
                    lamax FLOAT,
                    lomax FLOAT
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS aeroplanes (
                    id SERIAL PRIMARY KEY,
                    icao24 VARCHAR(20),
                    callsign VARCHAR(20),
                    origin_country VARCHAR(100),
                    longitude FLOAT,
                    latitude FLOAT,
                    velocity FLOAT,
                    country_id INTEGER REFERENCES countries(id)
                );
            """)

        self.conn.commit()


    def add_country(self, name, lamin, lomin, lamax, lomax):
        """Добавляет страну и её координаты в базу данных."""

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO countries
                    (name, lamin, lomin, lamax, lomax)
                VALUES
                    (%s, %s, %s, %s, %s);
            """, (name, lamin, lomin, lamax, lomax))

        self.conn.commit()

    def get_countries_and_aeroplanes_count(self):
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    countries.name,
                    COUNT(aeroplanes.id)
            
                FROM countries
                LEFT JOIN aeroplanes
                    ON countries.id = aeroplanes.country_id
                GROUP BY countries.name;
            """)
            return cur.fetchall()

    def get_all_aeroplanes(self):
        """получает список всех воздушных судов"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM aeroplanes;
            """)

            return cur.fetchall()

    def get_avg_speed(self):
        """получает среднюю скорость по самолетам"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(velocity)
                FROM aeroplanes;
            """)

            return cur.fetchone()[0]

    def get_aeroplanes_with_higher_speed(self):
        """получает список всех самолетов, у которых скорость выше средней"""
        pass

    def get_aeroplanes_with_keyword(self):
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        pass

    def add_aeroplane(
            self,
            icao24,
            callsign,
            origin_country,
            longitude,
            latitude,
            velocity,
            country_id
    ):
        """Добавляет самолёт в базу данных."""

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO aeroplanes
                    (
                        icao24,
                        callsign,
                        origin_country,
                        longitude,
                        latitude,
                        velocity,
                        country_id
                    )
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s);
            """, (
                icao24,
                callsign,
                origin_country,
                longitude,
                latitude,
                velocity,
                country_id
            ))

        self.conn.commit()