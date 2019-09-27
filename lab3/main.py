import pandas as pd
import math
import operator
from Node import Node
import copy
import numpy as np


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
    # print("\nStart decision_tree_learning")
    # print("data shape: " + str(data.shape))
    # print("attributes: " + str(attributes))
    # print("pattern: " + str(pattern))
    data = copy.deepcopy(data)
    attributes = copy.deepcopy(attributes)

    if data.shape[0] == 0:
        # print("exemplos eh vazio, retornou: " + str(pattern))
        return int(pattern)

    elif len(data['Rating'].unique()) == 1:
        # print("todos os exemplos tem a mesma classificacao, retornou: " + str(data['Rating'].unique()[0]))
        return int(data['Rating'].unique()[0])

    elif attributes is None:
        # print("atributos eh None, retornou: " + str(data['Rating'].value_counts().idxmax()))
        return int(data['Rating'].value_counts().idxmax())
    elif len(attributes) == 0:
        # print("atributos eh vazio, retornou: " + str(data['Rating'].value_counts().idxmax()))
        return int(data['Rating'].value_counts().idxmax())

    else:
        # print("else")
        best_attribute = get_max_gain_attribute(data)
        # print("best_attribute: " + str(best_attribute))
        tree = Node(best_attribute)
        m = data['Rating'].value_counts().idxmax()
        attributes.remove(best_attribute)

        for value_j in attributes_list_of_values[best_attribute]:
            # print("value_j: " + str(value_j))
            data_j = data.loc[data[best_attribute] == value_j]
            data_j = data_j.drop(columns=[best_attribute])
            subtree = decision_tree_learning(data_j, attributes, m)
            # print("End decision_tree_learning")

            if isinstance(subtree, Node):
                # print("subtree is Node")
                subtree.set_parent(tree)
                tree.children[value_j] = subtree

            else:
                # print("subtree is Classification")
                aux = Node()
                aux.set_classification(subtree)
                tree.children[value_j] = aux
                aux.set_parent(tree)

        return tree


attributes_list_of_values = {}


def predict(tree, data):
    result = []

    for index, row in data.iterrows():
        curr_node = tree

        if index % 1000 == 0:
            print("index: " + str(index))

        while True:
            if curr_node.is_classification:
                result.append(curr_node.classification)
                break

            for value, child_node in curr_node.children.items():
                if value == row[curr_node.attribute]:
                    curr_node = child_node
                    break

    return result


if __name__ == "__main__":

    # READING DATA
    print("READING DATA")
    dataset = pd.read_csv('data.csv', delimiter=",", engine='python')
    dataset = dataset.dropna(axis=0, how='any')

    dataset = dataset.sample(frac=1).reset_index(drop=True)

    num_of_rows = dataset.shape[0]
    print("total of rows: " + str(num_of_rows))

    train_ratio = 0.024
    validation_ratio = 0.008
    # test_ratio = 1 - train_ratio - validation_ratio
    test_ratio = 0.008

    # train_ratio = 0.6
    # validation_ratio = 0.2
    # test_ratio = 1 - train_ratio - validation_ratio
    # test_ratio = 0.008

    print("CREATING TRAIN, VALIDATION AND TEST SETS WITH RATIOS: " +
          str(train_ratio) + ", " + str(validation_ratio) + " AND " + str(test_ratio))

    train = int(train_ratio * num_of_rows)
    validation = int(validation_ratio * num_of_rows)
    test = int(test_ratio * num_of_rows)

    train_dataset = dataset[:train]
    aux_dataset = dataset[-(num_of_rows-train):]
    validation_dataset = aux_dataset[:validation]
    # test_dataset = dataset[-(num_of_rows-train-validation):]
    test_dataset = dataset[-test:]

    train_dataset_x = train_dataset.drop(columns=['Rating'])
    train_dataset_y = train_dataset['Rating']
    validation_dataset_x = validation_dataset.drop(columns=['Rating'])
    validation_dataset_y = validation_dataset['Rating']
    test_dataset_x = test_dataset.drop(columns=['Rating'])
    test_dataset_y = test_dataset['Rating']

    print("TRAINING DECISION TREE")

    for column in dataset.columns:
        # print("coluna: " + str(column))
        attributes_list_of_values[column] = []
        for value in dataset[column].unique():
            # print("value: " + str(value))
            attributes_list_of_values[column].append(value)

    attributes_list = dataset.columns.to_list()
    attributes_list.remove('Rating')
    decision_tree = decision_tree_learning(train_dataset, attributes_list, dataset['Rating'].value_counts().idxmax())

    print("PREDICT TO TRAIN SET")
    predicted_train_dataset = predict(decision_tree, train_dataset_x)
    predicted_diff = list(np.array(predicted_train_dataset) - np.array(train_dataset_y.to_list()))
    train_diff = np.count_nonzero(predicted_diff)
    # print("train acc: " + str((len(predicted_train_dataset) - diff)/len(predicted_train_dataset)))

    print("PREDICT TO VALIDATION SET")
    predicted_validation_dataset = predict(decision_tree, validation_dataset_x)
    predicted_diff = list(np.array(predicted_validation_dataset) - np.array(validation_dataset_y.to_list()))
    validation_diff = np.count_nonzero(predicted_diff)
    # print("validation acc: " + str((len(predicted_validation_dataset) - diff) / len(predicted_validation_dataset)))

    print("PREDICT TO TEST SET")
    predicted_test_dataset = predict(decision_tree, test_dataset_x)
    predicted_diff = list(np.array(predicted_test_dataset) - np.array(test_dataset_y.to_list()))
    test_diff = np.count_nonzero(predicted_diff)

    print("train acc: " +
          str((len(predicted_train_dataset) - train_diff) / len(predicted_train_dataset)))
    print("validation acc: " +
          str((len(predicted_validation_dataset) - validation_diff) / len(predicted_validation_dataset)))
    print("test acc: " +
          str((len(predicted_test_dataset) - test_diff) / len(predicted_test_dataset)))

    # predicted_validation_dataset = predict(decision_tree, validation_dataset_x)
    # predicted_test_dataset = predict(decision_tree, test_dataset_x)
