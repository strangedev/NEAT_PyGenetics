from NEAT.Nodes import HiddenNode


class CycleNode(HiddenNode):
    """
    Extends the hidden nodes by the ability to store cycle nodes.
    Cycle nodes are nodes at the tail of a cycle closing edge. These are special
    cases in simulation and must be prepared prior to a full graph calculation.
    """
    def __init__(self, label):
        super(CycleNode, self).__init__(label)
        self.cycle_successors = set([])
        self.cycle_value = {}

    def add_cycle_successor(self, node, weight):
        """
        Adds a cycle successor to the node.
        :param node:
        :param weight:
        """
        self.cycle_successors.add((node, weight))
        self.cycle_value[node] = weight

    def add_cycle_successors(self, nodes_and_weights):
        """
        Adds a number of cycle successors and corresponding weights to the node.
        :param nodes_and_weights: A list of (node, weight) tuples.
        :return:
        """
        for node, weight in nodes_and_weights:
            self.add_cycle_successor(node, weight)

    def fire_cycles(self):
        """
        Adds value to all cycle nodes.
        """
        for node, weight in self.cycle_successors:
            node.add_value(self.cycle_value[node] * weight)