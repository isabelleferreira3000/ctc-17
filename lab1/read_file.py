import pandas as pd

dataset = pd.read_csv('australia.csv', delimiter=",", engine='python')
dataset = dataset.dropna(axis=0, how='any')

print(dataset.values[:, 0][0])
# print(dataset)
# train_X = dataset.values[:, :46]
# train_Y = dataset.values[:, 46:]
