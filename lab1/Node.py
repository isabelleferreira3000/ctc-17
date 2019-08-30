import math


class CityNode:
    def __init__(self, city_id, city_name, lat, lng):
        self.id = city_id
        self.name = city_name
        self.x = lat
        self.y = lng
        self.neighborhood = []

    def calculate_straight_line_distance(self, other_city):
        return math.sqrt((self.x - other_city.x) ** 2 + (self.y - other_city.y) ** 2)

    def calculate_distance_by_road(self, other_city):
        return 1.1 * self.calculate_straight_line_distance(other_city)
