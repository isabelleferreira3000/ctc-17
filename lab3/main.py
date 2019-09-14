import pandas as pd

movies_data = pd.read_csv('ml-1m/movies.dat', delimiter="::", engine='python')
movies_data = movies_data.dropna(axis=0, how='any')

ratings_data = pd.read_csv('ml-1m/ratings.dat', delimiter="::", engine='python')
ratings_data = ratings_data.dropna(axis=0, how='any')

users_data = pd.read_csv('ml-1m/users.dat', delimiter="::", engine='python')
users_data = users_data.dropna(axis=0, how='any')

print(movies_data)
print(ratings_data)
print(users_data)
