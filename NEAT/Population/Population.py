class Population():
    """
    Manages a genome

    Contains logic to create offspring and keeps track of innovations.
    """

    def __init__(self):

        self.individuals = []
        self.gene_map = {}

        self._next_innovation = 0

    @property
    def next_innovation(self):

        self._next_innovation += 1
        return self._next_innovation
