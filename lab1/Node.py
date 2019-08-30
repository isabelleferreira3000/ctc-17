class CityNode:
    def __init__(self, city_id, city_name, lat, lng):
        self.id = city_id
        self.name = city_name
        self.lat = lat
        self.lng = lng
        self.neighborhood = []
