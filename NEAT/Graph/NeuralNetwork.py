
class NeuralNetwork():

    def __init__(self, genedescription):

        self.description = genedescription
        self.fitness_level = 0

    def compute(self, inputs):

        for input_pair in inputs:

            input_label, input_value = input_pair


