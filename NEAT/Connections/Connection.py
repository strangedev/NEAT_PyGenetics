class NetworkConnection():

    def __init__(self, source, target, weight, innovation, enabled=True):

        self.source = source
        self.target = target

        self.weight = weight
        self.enabled = enabled

        self.innovation = innovation
