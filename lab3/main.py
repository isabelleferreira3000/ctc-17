import pandas as pd
import math
import operator


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


def get_max_gain_attribute(data):
    # CALCULATING ENTROPY
    print("CALCULATING ENTROPY")
    entropy = calculate_entropy(data, 'Rating')
    print("Entropy: " + str(entropy))

    attribute_value_entropy = {}
    attribute_value_quantity = {}
    attribute_value_rating_quantity = {}
    total_rows = data.shape[0]

    # CALCULATING PARTIAL ENTROPY FOR EACH VALUE FROM A ATTRIBUTE
    print("CALCULATING PARTIAL ENTROPY FOR EACH VALUE FROM A ATTRIBUTE")
    data_attributes = data.drop(columns=['Rating'])
    for attribute in data_attributes.columns:
        print("Attribute: " + attribute)

        attribute_value_entropy[attribute] = {}
        attribute_value_quantity[attribute] = {}
        attribute_value_rating_quantity[attribute] = {}

        for value in data[attribute].unique():
            print("Valor: " + str(value))
            resulting_data = data.loc[data[attribute] == value]
            attribute_value_quantity[attribute][value] = resulting_data.shape[0]
            attribute_value_entropy[attribute][value] = calculate_entropy(resulting_data, 'Rating')

            attribute_value_rating_quantity[attribute][value] = {}
            aux_data = data.loc[data[attribute] == value]
            attribute_value_rating_quantity[attribute][value][1] = aux_data.loc[data['Rating'] == 1].shape[0]
            attribute_value_rating_quantity[attribute][value][2] = aux_data.loc[data['Rating'] == 2].shape[0]
            attribute_value_rating_quantity[attribute][value][3] = aux_data.loc[data['Rating'] == 3].shape[0]
            attribute_value_rating_quantity[attribute][value][4] = aux_data.loc[data['Rating'] == 4].shape[0]
            attribute_value_rating_quantity[attribute][value][5] = aux_data.loc[data['Rating'] == 5].shape[0]

    # PARTIAL ENTROPY BY EACH VALUE FROM A ATTRIBUTE
    print("PARTIAL ENTROPY BY EACH VALUE FROM A ATTRIBUTE")
    gain_attribute = {}
    for attribute, _ in attribute_value_entropy.items():
        print(attribute)
        gain_attribute[attribute] = entropy
        for value, partial_entropy in attribute_value_entropy[attribute].items():
            print(value, '->', partial_entropy)
            gain_attribute[attribute] -= (attribute_value_quantity[attribute][value] / total_rows) * partial_entropy

    # QUANTITY BY EACH VALUE FROM A ATTRIBUTE
    print("QUANTITY BY EACH VALUE FROM A ATTRIBUTE")
    for attribute, _ in attribute_value_quantity.items():
        print(attribute)
        for value, quantity in attribute_value_quantity[attribute].items():
            print(value, '->', quantity)

    # GAIN BY ATTRIBUTE
    print("GAIN BY ATTRIBUTE")
    for attribute, gain in gain_attribute.items():
        print(attribute, '->', gain)

    print("MAX GAIN")
    max_gain_attribute = max(gain_attribute.items(), key=operator.itemgetter(1))[0]
    print(max_gain_attribute)

    # QUANTITY FOR MAX GAIN
    print("QUANTITY FOR MAX GAIN")
    count_zeros = 0
    for value, _ in attribute_value_rating_quantity[max_gain_attribute].items():
        print(value)
        for rating, quantity in attribute_value_rating_quantity[max_gain_attribute][value].items():
            print(rating, '->', quantity)
            if quantity == 0:
                count_zeros += 1

    if count_zeros == 4:
        return max_gain_attribute, True
    else:
        return max_gain_attribute, False


if __name__ == "__main__":

    # READING DATA
    print("READING DATA")
    data = pd.read_csv('data.csv', delimiter=",", engine='python')
    data = data.dropna(axis=0, how='any')

    max_gain_attribute, is_finished = get_max_gain_attribute(data)

    print("IS FINISHED? " + str(is_finished))
