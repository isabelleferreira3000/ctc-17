import pandas as pd
import math


def calculate_entropy(data, column_name):
    count = data[column_name].value_counts()
    count = pd.DataFrame({column_name: count.index, 'count': count.values})

    p_total = count['count'].sum()

    s = 0
    for value in count[column_name].unique():
        p_value = count.loc[count[column_name] == value]['count'].values[0]
        aux = p_value / p_total
        s -= aux * math.log2(aux)

    return s


# READING NEW USERS DATA
print("READING NEW USERS DATA")
users_data = pd.read_csv('new_users.csv', delimiter=",", engine='python')
users_data = users_data.dropna(axis=0, how='any')
users_data = users_data.drop(columns=['RowID'])  # removing RowID column

entropy = calculate_entropy(users_data, 'Genres')
print("Entropy: " + str(entropy))

attribute_value_entropy = {}
attribute_value_quantity = {}
# attribute_quantity = {"total": 0}
total_rows = users_data.shape[0]
users_data_attributes = users_data.drop(columns=['UserID', 'Genres'])
for attribute in users_data_attributes.columns:
    print("Attribute: " + attribute)
    # attribute_quantity[attribute] = users_data[attribute].shape[0]
    # attribute_quantity["total"] += attribute_quantity[attribute]
    attribute_value_entropy[attribute] = {}
    attribute_value_quantity[attribute] = {}
    for value in users_data[attribute].unique():
        print("Valor: " + str(value))
        resulting_data = users_data.loc[users_data[attribute] == value]
        attribute_value_quantity[attribute][value] = resulting_data.shape[0]
        attribute_value_entropy[attribute][value] = calculate_entropy(resulting_data, 'Genres')

gain_attribute = {}
for attribute, _ in attribute_value_entropy.items():
    print(attribute)
    gain_attribute[attribute] = entropy
    for value, partial_entropy in attribute_value_entropy[attribute].items():
        print(value, '->', partial_entropy)
        gain_attribute[attribute] -= (attribute_value_quantity[attribute][value] / total_rows) * partial_entropy

for attribute, _ in attribute_value_quantity.items():
    print(attribute)
    for value, quantity in attribute_value_quantity[attribute].items():
        print(value, '->', quantity)

for attribute, gain in gain_attribute.items():
    print(attribute, '->', gain)
