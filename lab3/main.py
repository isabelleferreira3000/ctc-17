import pandas as pd
import numpy as np
import ast

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

# GETTING 5 OR 4 STARS MOVIES FROM MERGED_DATA
print("GETTING 5 OR 4 STARS MOVIES FROM MERGED_DATA")
data_with_five_stars = merged_data.loc[merged_data['Rating'] == 5]
data_with_four_stars = merged_data.loc[merged_data['Rating'] == 4]
merged_data_five_or_four_stars = pd.concat([data_with_five_stars, data_with_four_stars])

# CREATING GENRES COLUMN ON USERS DATA
print("CREATING GENRES COLUMN ON USERS DATA")
users_data['Genres'] = np.nan

# FILLING GENRES COLUMN ON USERS DATA
print("FILLING GENRES COLUMN ON USERS DATA")
for userID in merged_data_five_or_four_stars['UserID'].unique():
    data_from_userID = merged_data_five_or_four_stars.loc[merged_data_five_or_four_stars['UserID'] == userID]

    genres_count = data_from_userID['Genres'].value_counts()
    max_genres_count = genres_count.max()
    genres_count = pd.DataFrame({'Genres': genres_count.index, 'count': genres_count.values})

    genres_list_for_userID = genres_count.loc[genres_count['count'] == max_genres_count]['Genres'].to_list()
    genres_list_for_userID = sorted(genres_list_for_userID)
    users_data['Genres'] = np.where(users_data['UserID'] == userID,
                                    str(genres_list_for_userID),
                                    users_data['Genres'])

# [TUTORIAL] TO GET GENRES LIST TO A USER ID:
# TRANSFORMING STRING OF LIST ON LIST:
# x = ast.literal_eval(users_data.loc[users_data['UserID'] == 12]['Genres'].to_list()[0])
# for i in x:
#     print(i)
# print(users_data)
print(users_data['Genres'].unique()[8])

# ideias: pegar uma coisa como "Action|Adventure|Animation" e separar em Action, Adventure e Animation
# e só depois contar os gêneros que mais aparecem
