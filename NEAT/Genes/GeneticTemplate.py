
class GeneticTemplate():

    def __init__(self, input_labels=None, output_labels=None):

        if not input_labels:
            input_labels = set({})

        if not output_labels:
            output_labels = set({})

        self.input_labels = set(input_labels)
        self.output_labels = set(output_labels)

    def add_input(self, label):

        self.input_labels.add(label)

    def add_output(self, label):

        self.output_labels.add(label)

    def add_inputs(self, labels):

        for label in labels:

            self.add_input(label)

    def add_outputs(self, labels):

        for label in labels:

            self.add_output(label)
