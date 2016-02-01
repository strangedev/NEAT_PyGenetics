from Nodes import InputNode
from Nodes import OutputNode
from Nodes import HiddenNode
from Connections import Connection


class GeneticDescription():

    def __init__(self):

        self.nodes = {}
        self.connections = {}

        self.nodes.input_nodes = []
        self.nodes.output_nodes = []
        self.nodes.hidden_nodes = []

    def init_inputs(self, labels):

        pass

    def init_outputs(self, labels):

        pass

    def _m_add_node(self, node):
        """
        Only adds node, contains no logic
        """

        pass

    def _m_add_connection(self, connection):
        """
        Only adds connection, contains no logic
        """

        pass

    def mutate_add_connection(self):

        pass

    def mutate_add_node(self):

        pass
