class NetworkNode():

    def __init__(self, label):

        self.label = label
        self.value = 0

    def on_input(self, in_val):

        self.value += in_val

    def on_reset(self):

        self.value = 0
