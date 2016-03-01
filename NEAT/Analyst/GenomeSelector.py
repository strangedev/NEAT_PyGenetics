from typing import List

from NEAT.Analyst.Cluster import Cluster
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Repository.ClusterRepository import ClusterRepository


class GenomeSelector(object):
    def __init__(
            self,
            genome_repository: GenomeRepository,
            cluster_repository: ClusterRepository,
            selection_parameters
    ):
        self.genome_repository = genome_repository
        self.cluster_repository = cluster_repository
        self.selection_parameters = selection_parameters

    def select_clusters_for_discarding(self) -> List[Cluster]:
        clusters = []
        for cluster in self.cluster_repository.get_current_clusters():
            clusters.append(cluster)
        clusters.sort(key=lambda cluster: cluster.fitness)
        return clusters[:int(len(clusters)*self.selection_parameters.discarding_threshold)]

    def select_genomes_for_discarding(self) -> List[StorageGenome]:
        """
        discarding_threshold should be in [0 , 1]
        :return: List of genomes wanted to be discarded
        """
        clusters = []
        for cluster in self.cluster_repository.get_current_clusters():
            genomes = []
            for genome in self.genome_repository.get_genomes_in_cluster(cluster.id):
                genomes.append(genome)
            genomes.sort(key=lambda genome: genome.fitness)
            clusters.extend(genomes[:int(len(genomes)*self.selection_parameters.discarding_threshold)])
        return clusters
