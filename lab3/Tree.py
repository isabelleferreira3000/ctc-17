class Tree:
    def __init__(self, root):
        self.root = root

    def print_tree(self):
        print("Root")
        print("Attribute: " + str(self.root.attribute))
        for value, node in self.root.children.items():
            print(value)
            node.print_node()
