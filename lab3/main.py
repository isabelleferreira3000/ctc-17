import pandas as pd
import math
import operator
from Node import Node
import copy


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
    # print("CALCULATING ENTROPY")
    entropy = calculate_entropy(data, 'Rating')
    # print("Entropy: " + str(entropy))

    attribute_value_entropy = {}
    attribute_value_quantity = {}
    attribute_value_rating_quantity = {}
    total_rows = data.shape[0]

    # CALCULATING PARTIAL ENTROPY FOR EACH VALUE FROM A ATTRIBUTE
    # print("CALCULATING PARTIAL ENTROPY FOR EACH VALUE FROM A ATTRIBUTE")
    data_attributes = data.drop(columns=['Rating'])
    for attribute in data_attributes.columns:
        # print("Attribute: " + attribute)

        attribute_value_entropy[attribute] = {}
        attribute_value_quantity[attribute] = {}
        attribute_value_rating_quantity[attribute] = {}

        for value in data[attribute].unique():
            # print("Valor: " + str(value))
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
    # print("PARTIAL ENTROPY BY EACH VALUE FROM A ATTRIBUTE")
    gain_attribute = {}
    for attribute, _ in attribute_value_entropy.items():
        # print(attribute)
        gain_attribute[attribute] = entropy
        for value, partial_entropy in attribute_value_entropy[attribute].items():
            # print(value, '->', partial_entropy)
            gain_attribute[attribute] -= (attribute_value_quantity[attribute][value] / total_rows) * partial_entropy

    # QUANTITY BY EACH VALUE FROM A ATTRIBUTE
    # print("QUANTITY BY EACH VALUE FROM A ATTRIBUTE")
    # for attribute, _ in attribute_value_quantity.items():
        # print(attribute)
        # for value, quantity in attribute_value_quantity[attribute].items():
            # print(value, '->', quantity)

    # GAIN BY ATTRIBUTE
    # print("GAIN BY ATTRIBUTE")
    # for attribute, gain in gain_attribute.items():
    #     print(attribute, '->', gain)

    # print("MAX GAIN")
    max_gain_attribute = max(gain_attribute.items(), key=operator.itemgetter(1))[0]
    # print(max_gain_attribute)

    return max_gain_attribute


def decision_tree_learning(data, attributes, pattern):
    print("\nStart decision_tree_learning")
    print("data shape: " + str(data.shape))
    print("attributes: " + str(attributes))
    print("pattern: " + str(pattern))
    data = copy.deepcopy(data)
    attributes = copy.deepcopy(attributes)

    if data.shape[0] == 0:
        print("exemplos eh vazio, retornou: " + str(pattern))
        return int(pattern)

    elif len(data['Rating'].unique()) == 1:
        print("todos os exemplos tem a mesma classificacao, retornou: " + str(data['Rating'].unique()[0]))
        return int(data['Rating'].unique()[0])

    elif attributes is None:
        print("atributos eh None, retornou: " + str(data['Rating'].value_counts().idxmax()))
        return int(data['Rating'].value_counts().idxmax())
    elif len(attributes) == 0:
        print("atributos eh vazio, retornou: " + str(data['Rating'].value_counts().idxmax()))
        return int(data['Rating'].value_counts().idxmax())

    else:
        print("else")
        best_attribute = get_max_gain_attribute(data)
        print("best_attribute: " + str(best_attribute))
        tree = Node(best_attribute)
        m = data['Rating'].value_counts().idxmax()
        attributes.remove(best_attribute)

        for value_j in attributes_list_of_values[best_attribute]:
            print("value_j: " + str(value_j))
            data_j = data.loc[data[best_attribute] == value_j]
            data_j = data_j.drop(columns=[best_attribute])
            subtree = decision_tree_learning(data_j, attributes, m)
            print("End decision_tree_learning")

            if isinstance(subtree, Node):
                print("subtree is Node")
                subtree.set_parent(tree)
                tree.children[value_j] = subtree

            else:
                print("subtree is Classification")
                aux = Node()
                aux.set_classification(subtree)
                tree.children[value_j] = aux
                aux.set_parent(tree)

        return tree


attributes_list_of_values = {}


if __name__ == "__main__":

    # READING DATA
    print("READING DATA")
    dataset = pd.read_csv('data.csv', delimiter=",", engine='python')
    dataset = dataset.dropna(axis=0, how='any')

    for column in dataset.columns:
        print("coluna: " + str(column))
        attributes_list_of_values[column] = []
        for value in dataset[column].unique():
            print("value: " + str(value))
            attributes_list_of_values[column].append(value)

    attributes_list = dataset.columns.to_list()
    attributes_list.remove('Rating')
    decision_tree = decision_tree_learning(dataset, attributes_list, dataset['Rating'].value_counts().idxmax())
