class ConnAPIOpensky:
    """класc получения данных апи open sky"""
    url = "https://opensky-network.org/api"
    def __init__(self,time, icao24, lamin, lomin, lamax, lomax,extended):
        self.time = time            #время(опционально)
        self.icao24 = icao24        #адрес(а) транспондеров ICAO24(опционально)

        self.lamin = lamin          #координаты сетки
        self.lomin = lomin          #координаты сетки
        self.lamax = lamax          #координаты сетки
        self.lomax = lomax          #координаты сетки
        self.extended = extended    #категория воздушных судов
    def connect_opensky(self):
