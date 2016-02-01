
class GeneticTemplate():

    def __init__(self, input_nodes=None, output_nodes=None):

        if not input_nodes:
            input_nodes = set({})

        if not output_nodes:
            output_nodes = set({})

        self.input_nodes = set(input_nodes)
        self.output_nodes = set(output_nodes)

    def add_input(self, node):

        self.input_nodes.add(node)

    def add_output(self, node):

        self.output_nodes.add(node)

    def add_inputs(self, nodes):

        for node in nodes:

            self.add_input(node)

    def add_outputs(self, nodes):

        for node in nodes:

            self.add_output(node)
