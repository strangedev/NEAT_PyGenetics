from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome

class Cluster(object):

    def __init__(
            self,
            id: int,
            representative: int
    ):

        self.id = id
        self.representative = representative # StorageGenome id
        self.fitness = 0
        self.max_population = 0
