import psycopg2


class DBManager:
    def __init__(self):
        """Инициализирует менеджер базы данных."""
        self.conn = None

    def connect_to_db(self, database_name, **params):
        """Подключение к базе данных и создание таблиц."""

        self.conn = psycopg2.connect(dbname=database_name, **params)

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
        self.conn.close()

    def add_country(self, name, lamin, lomin, lamax, lomax, database_name, **params):
        """Добавляет страну и её координаты в базу данных."""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM countries
                WHERE name = %s;
            """,
                (name,),
            )

            result = cur.fetchone()

            if result:
                return result[0]

            cur.execute(
                """
                INSERT INTO countries
                    (name, lamin, lomin, lamax, lomax)
                VALUES
                    (%s, %s, %s, %s, %s)
                RETURNING id;
            """,
                (name, lamin, lomin, lamax, lomax),
            )

            country_id = cur.fetchone()[0]

        self.conn.commit()
        self.conn.close()

        return country_id

    def clear_aeroplanes(self, database_name, **params):
        """Удаляет все самолёты из таблицы."""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM aeroplanes;")

        self.conn.commit()
        self.conn.close()

    def get_countries_and_aeroplanes_count(self, database_name, **params):
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        self.conn = psycopg2.connect(dbname=database_name, **params)
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
            list_countries = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return list_countries

    def get_all_aeroplanes(self, database_name, **params):
        """получает список всех воздушных судов"""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM aeroplanes;
            """)
            list_aeroplanes = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return list_aeroplanes

    def get_avg_speed(self, database_name, **params):
        """получает среднюю скорость по самолетам"""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(velocity)
                FROM aeroplanes;
            """)
            avg_speed = cur.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return avg_speed

    def get_aeroplanes_with_higher_speed(self, database_name, **params):
        """получает список всех самолетов, у которых скорость выше средней"""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM aeroplanes
                WHERE velocity > (
                    SELECT AVG(velocity)
                    FROM aeroplanes
                );
            """)
            list_aeroplanes = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return list_aeroplanes

    def get_aeroplanes_with_keyword(self, keyword, database_name, **params):
        """Получает самолёты, в позывном которых содержатся переданные символы."""
        self.conn = psycopg2.connect(dbname=database_name, **params)
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM aeroplanes
                WHERE callsign ILIKE %s;
            """,
                (f"%{keyword}%",),
            )
            list_aeroplanes = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        return list_aeroplanes

    def add_aeroplanes(self, aircraft_list, country_id, database_name, **params):
        """Добавляет список самолётов в базу данных."""

        self.conn = psycopg2.connect(dbname=database_name, **params)

        with self.conn.cursor() as cur:
            for aircraft in aircraft_list:
                cur.execute(
                    """
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
                """,
                    (
                        aircraft[0],
                        aircraft[1].strip(),
                        aircraft[2],
                        aircraft[5],
                        aircraft[6],
                        aircraft[9],
                        country_id,
                    ),
                )

        self.conn.commit()
        self.conn.close()
