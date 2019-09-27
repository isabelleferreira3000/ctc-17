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
        if self.parent is not None:
            print("Parent Attribute: " + str(self.parent.attribute))
        else:
            print("Root!")

        for value, node in self.children.items():
            print("Value: " + str(value))
            node.print_node()

    def set_classification(self, classification):
        self.is_classification = True
        self.classification = classification
