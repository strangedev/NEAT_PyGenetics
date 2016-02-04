from NEAT.Nodes import InputNode
from NEAT.Nodes import OutputNode
from NEAT.Nodes import HiddenNode
from NEAT.Connections import Connection


class NeuralGraph():

    def __init__(self):

        self.connections = dict({})  # src -> Connection

        self.input_nodes = set({})  # nodes only
        self.output_nodes = set({})
        self.hidden_nodes = set({})

    def add_input(self, node):

        new_node = InputNode.InputNode(node)
        self.input_nodes.add(new_node)

    def add_inputs(self, nodes):

        for node in nodes:

            self.add_input(node)

    def add_output(self, node):

        new_node = OutputNode.OutputNode(node)
        self.output_nodes.add(new_node)

    def add_outputs(self, nodes):

        for node in nodes:

            self.add_output(node)

    def add_hidden_node(self, node):

        new_node = HiddenNode.HiddenNode(node)
        self.hidden_nodes.add(new_node)

    def add_hidden_nodes(self, nodes):

        for node in nodes:

            self.add_hidden_node(node)

    def init_from_template(self, template):

        self.add_inputs(template.input_nodes)
        self.add_outputs(template.output_nodes)

    def add_connection(self, src, target, weight, innovation, enabled=True):

        conn = Connection.NetworkConnection(
            src, target, weight, innovation, enabled)

        if src not in self.connections.keys():
            self.connections[src] = []

        self.connections[src].append(conn)

    def get_connections(self, label):

        return self.connections[label]
