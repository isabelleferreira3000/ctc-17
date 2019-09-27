class Node:
    def __init__(self, attribute=None):
        self.attribute = attribute
        self.children = {}  # children[value] = other_node
        self.parent = None
        self.is_classification = False
        self.classification = 0

    def set_parent(self, parent):
        self.parent = parent

    def print_node(self):
        print("-----------")
        if self.parent is None:
            print("Root!")
        else:
            print("Parent Attribute: " + str(self.parent.attribute))

        if self.is_classification:
            print("Classification: " + str(self.classification))
        else:
            print("My Attribute: " + str(self.attribute))
            for value, node in self.children.items():
                print("Value: " + str(value))
                node.print_node()

    def set_classification(self, classification):
        self.is_classification = True
        self.classification = classification
