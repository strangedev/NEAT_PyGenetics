from Nodes import InputNode
from Nodes import OutputNode
from Nodes import HiddenNode
from Connections import Connection


class GeneticDescription():

    def __init__(self, population):

        self.population = population

        self.connections = dict({})  # src -> Connection

        self.input_nodes = set({})  # labels only
        self.output_nodes = set({})
        self.hidden_nodes = set({})

    def add_input(self, label):

        new_node = InputNode.InputNode(label)
        self.nodes.input_nodes.add(new_node)

    def add_inputs(self, labels):

        for label in labels:

            self.add_input.add(label)

    def add_output(self, label):

        new_node = OutputNode.OutputNode(label)
        self.nodes.output_nodes.add(new_node)

    def add_outputs(self, labels):

        for label in labels:

            self.add_output(label)

    def add_hidden_node(self, label):

        new_node = HiddenNode.HiddenNode(label)
        self.hidden_nodes.add(new_node)

    def add_hidden_nodes(self, labels):

        for label in labels:

            self.add_hidden_node(label)

    def init_from_template(self, template):

        self.add_inputs(template.input_labels)
        self.add_outputs(template.output_labels)

    def add_connection(self, src, target, weight, enabled=True):

        innovation = self.population.next_innovation()
        conn = Connection.Connection(src, target, weight, innovation, enabled)

        if not self.connections[src]:
            self.connections[src] = []

        self.connections[src].append(conn)

    def mutate_add_connection(self):

        pass

    def mutate_add_node(self):

        pass

    def get_connections(self, node):

        label = node

        if not type(node) == int:
            label = node.label

        return self.connections[label]
