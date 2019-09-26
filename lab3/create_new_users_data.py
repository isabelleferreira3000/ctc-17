import pandas as pd
import numpy as np
import operator

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
dict_aux = {}
for userID in merged_data_five_or_four_stars['UserID'].unique():
    data_from_userID = merged_data_five_or_four_stars.loc[merged_data_five_or_four_stars['UserID'] == userID]

    for multi_genre in data_from_userID['Genres'].to_list():

        genre_list = multi_genre.split("|")
        for genre in genre_list:
            if genre in dict_aux:
                dict_aux[genre] += 1
            else:
                dict_aux[genre] = 1

    most_frequent_genre = max(dict_aux.items(), key=operator.itemgetter(1))[0]

    users_data['Genres'] = np.where(users_data['UserID'] == userID,
                                    str(most_frequent_genre),
                                    users_data['Genres'])
    dict_aux = {}

# EXPORTING NEW USERS DATA
print("EXPORTING NEW USERS DATA")
users_data.to_csv(r'new_users.csv')
