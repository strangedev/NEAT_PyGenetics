from NEAT.GenomeStructures.StorageStructure import StorageGenome

class ClusterRepository(object):

    def __init__(self):
        pass

    def archive_clusters(self):
        pass

    def add_cluster_with_representative(
            self,
            genome: StorageGenome
    ) -> None:

        pass

    def get_current_clusters(self):
        pass

    def add_genome_to_cluster(
            self,
            genome: StorageGenome,
            cluster: Cluster
    ):
        pass