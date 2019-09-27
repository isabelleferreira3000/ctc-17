class Node:
    def __init__(self, attribute=None):
        self.attribute = attribute
        self.children = {}  # children[value] = other_node
        self.parent = None
        self.is_classification = False
        self.classification = 0

    def set_parent(self, parent):
        self.parent = parent

    def set_classification(self, classification):
        self.is_classification = True
        self.classification = classification
