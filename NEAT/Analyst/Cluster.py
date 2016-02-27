from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome

class Cluster(object):

    def __init__(
            self,
            id: int,
            representative: StorageGenome
    ):

        self.id = id
        self.representative = representative