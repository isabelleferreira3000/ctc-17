import pandas as pd
from Node import CityNode

australia_dataset = pd.read_csv('australia.csv', delimiter=",", engine='python')
australia_dataset = australia_dataset.dropna(axis=0, how='any')

all_cities = []
num_cities = australia_dataset.values[:, 0].size

for i in range(num_cities):
    current_city_id = australia_dataset.values[i, 0]
    city_name = australia_dataset.values[i, 1]
    lat = australia_dataset.values[i, 2]
    lng = australia_dataset.values[i, 3]

    current_city = CityNode(current_city_id, city_name, lat, lng)
    all_cities.append(current_city)

for i in range(num_cities):
    current_city = all_cities[i]
    current_city_id = current_city.id
    # print(str(current_city_id) + ": " + str(current_city.name))

    # Se x > 1 e x é par, uma cidade com ID x se conecta com as cidades x + 2 e x - 1.
    # Se X é ímpar e x > 2, esta cidade x se conecta com as cidades x - 2 e x + 1
    if current_city_id > 1 and current_city_id % 2 == 0:
        if current_city_id + 2 <= num_cities:
            nearby_city = all_cities[(current_city_id - 1) + 2]

            if nearby_city not in current_city.neighborhood:
                current_city.neighborhood.append(nearby_city)
            if current_city not in nearby_city.neighborhood:
                nearby_city.neighborhood.append(current_city)

        if current_city_id - 1 > 0:
            nearby_city = all_cities[(current_city_id - 1) - 1]

            if nearby_city not in current_city.neighborhood:
                current_city.neighborhood.append(nearby_city)
            if current_city not in nearby_city.neighborhood:
                nearby_city.neighborhood.append(current_city)

    elif current_city_id > 2 and current_city_id % 2 == 1:
        if current_city_id - 2 > 0:
            nearby_city = all_cities[(current_city_id - 1) - 2]

            if nearby_city not in current_city.neighborhood:
                current_city.neighborhood.append(nearby_city)
            if current_city not in nearby_city.neighborhood:
                nearby_city.neighborhood.append(current_city)

        if current_city_id + 1 <= num_cities:
            nearby_city = all_cities[(current_city_id - 1) + 1]

            if nearby_city not in current_city.neighborhood:
                current_city.neighborhood.append(nearby_city)
            if current_city not in nearby_city.neighborhood:
                nearby_city.neighborhood.append(current_city)

for i in range(num_cities):
    current_city = all_cities[i]
    current_city_id = current_city.id
    print("CITY " + str(current_city_id) + ": " + str(current_city.name))
    for j in current_city.neighborhood:
        print("NEARBY " + str(j.id) + ": " + str(j.name))
