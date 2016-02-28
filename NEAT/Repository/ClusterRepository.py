from typing import List
from NEAT.GenomeStructures.StorageStructure import StorageGenome
from NEAT.Analyst.Cluster import Cluster

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

    def get_current_clusters(self) -> List[Cluster]:
        pass

    def add_genome_to_cluster(
            self,
            genome: StorageGenome,
            cluster: Cluster
    ):
        pass

    def get_cluster_by_genome_id(self, genome_id: int):
        pass

    def get_cluster_count(self) -> int:
        pass