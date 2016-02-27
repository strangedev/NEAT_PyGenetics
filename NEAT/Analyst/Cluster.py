from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome

class Cluster(object):

    def __init__(
            self,
            cluster_id: int,
            representative: StorageGenome
    ):

        self.cluster_id = cluster_id
        self.representative = representative