import pandas as pd
from Node import CityNode

australia_dataset = pd.read_csv('australia.csv', delimiter=",", engine='python')
australia_dataset = australia_dataset.dropna(axis=0, how='any')


num_cities = australia_dataset.values[:, 0].size

for i in range(num_cities):
    city_id = australia_dataset.values[i, 0]
    city_name = australia_dataset.values[i, 1]
    lat = australia_dataset.values[i, 2]
    lng = australia_dataset.values[i, 3]

    city = CityNode(city_id, city_name, lat, lng)


# print(australia_dataset.values[:, 0].size)
# print(australia_dataset.values[:, 0])
# print(australia_dataset)
# train_X = dataset.values[:, :46]
# train_Y = dataset.values[:, 46:]
