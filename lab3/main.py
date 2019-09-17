import pandas as pd
import math


def calculate_entropy():
    pass


# READING NEW USERS DATA
print("READING NEW USERS DATA")
users_data = pd.read_csv('new_users.csv', delimiter=",", engine='python')
users_data = users_data.dropna(axis=0, how='any')
users_data = users_data.drop(columns=['RowID'])  # removing RowID column

genres_count = users_data['Genres'].value_counts()
genres_count = pd.DataFrame({'Genres': genres_count.index, 'count': genres_count.values})

print(genres_count)

p_all_genres = genres_count['count'].sum()

entropy = 0
for genre in genres_count['Genres'].unique():
    p_genre = genres_count.loc[genres_count['Genres'] == genre]['count'].values[0]
    aux = p_genre/p_all_genres
    entropy -= aux * math.log2(aux)

print("Entropy: " + str(entropy))

users_data_attributes = users_data.drop(columns=['UserID', 'Genres'])
for column in users_data_attributes.columns:
    print("Column: " + column)
    for aux in users_data[column].unique():
        print("Valor: " + str(aux))
        resulting_data = users_data.loc[users_data[column] == aux]

        # genres_count = resulting_data['Genres'].value_counts()
        # genres_count = pd.DataFrame({'Genres': genres_count.index, 'count': genres_count.values})
        #
        # # print(genres_count)
        #
        # p_all_genres = genres_count['count'].sum()
        #
        # entropy = 0
        # for genre in genres_count['Genres'].unique():
        #     p_genre = genres_count.loc[genres_count['Genres'] == genre]['count'].values[0]
        #     aux = p_genre / p_all_genres
        #     entropy -= aux * math.log2(aux)
