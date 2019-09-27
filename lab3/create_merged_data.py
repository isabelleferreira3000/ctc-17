import pandas as pd

# READING MOVIES, RATINGS AND USERS DATA
print("READING MOVIES, RATINGS AND USERS DATA")
movies_data = pd.read_csv('ml-1m/movies.dat', delimiter="::", engine='python')
movies_data = movies_data.dropna(axis=0, how='any')

ratings_data = pd.read_csv('ml-1m/ratings.dat', delimiter="::", engine='python')
ratings_data = ratings_data.dropna(axis=0, how='any')
ratings_data = ratings_data.drop(columns=['Timestamp'])  # removing Timestamp column

users_data = pd.read_csv('ml-1m/users.dat', delimiter="::", engine='python')
users_data = users_data.dropna(axis=0, how='any')
users_data = users_data.drop(columns=['Zip-code'])  # removing Zip-code column

# MERGING MOVIES, RATINGS AND USERS DATA
print("MERGING MOVIES, RATINGS AND USERS DATA")
merged_data = pd.merge(users_data, ratings_data, how='inner', on='UserID')
merged_data = pd.merge(merged_data, movies_data, how='inner', on='MovieID')

# EXPORTING MERGED DATA
print("EXPORTING MERGED DATA")
merged_data.to_csv(r'merged.csv')
