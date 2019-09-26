import pandas as pd

# READING MERGED DATA
print("READING MERGED DATA")
data = pd.read_csv('merged.csv', delimiter=",", engine='python')
data = data.dropna(axis=0, how='any')

with open('data.csv', 'a') as f:
    f.write("Gender,Age,Occupation,Genre,Rating\n")

    for index, row in data.iterrows():
        Gender = row['Gender']
        Age = row['Age']
        Occupation = row['Occupation']
        Rating = row['Rating']
        Genres = row['Genres']
        Genres_list = Genres.split("|")

        for genre in Genres_list:
            f.write(str(Gender) + "," + str(Age) + "," + str(Occupation) + "," + str(genre) + "," + str(Rating) + "\n")
