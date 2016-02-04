class NetworkNode(object):

    def __init__(self, label):

        self.label = label
        self.successors = set([])  # a set of pairs of the form (node, weight)
        self.value = 0

    def reset(self):
        self.value = 0

    def add_successor(self, node, weight):
        """
        Adds a successor and an edge weight to the node.
        :param node: The successor
        :param weight: The weight of the edge to the successor
        """
        self.successors.add((node, weight))

    def fire(self):
        """
        Adds value to all successors of the node.
        """
        for node, weight in self.successors:
            node.addValue(self.value * weight)

    def add_value(self, value):
        """
        Adds value to the nodes stored value.
        How exactly that should be calculated is not decided yet.
        :param value: The value to be added
        """
        self.value += value  # TODO: such bs