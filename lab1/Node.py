class CityNode:
    def __init__(self, id, city_name, lat, lng):
        self.id = id
        self.name = city_name
        self.lat = lat
        self.lng = lng
        self.neighborhood = []
