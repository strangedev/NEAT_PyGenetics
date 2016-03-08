import random
from typing import List

from bson import ObjectId

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
        """
        :param genome_repository: GenomeRepository to select
        :param cluster_repository: ClusterRepository to select
        :param selection_parameters: saved in selection.conf
        :return:
        """

        self.genome_repository = genome_repository
        self.cluster_repository = cluster_repository
        self.selection_parameters = selection_parameters

    def get_genomes_from_cluster_id_by_given_percentage(
            self,
            cluster_id: ObjectId,
            begin: float,
            ending: float) -> [StorageGenome]:
        """
        Selects and Area of genomes in Cluster given by input
        :param cluster_id: ObjectId to load Genomes
        :param begin: float where to begin to select genomes
        :param ending: float where to end select genomes
        :return: [StorageGenome]
        """
        genomes = []
        for genome in self.genome_repository.get_current_population(cluster_id):
            genomes.append(genome)
        genomes.sort(key=lambda g: g.fitness)
        start = int(len(genomes)*begin)
        end = int(len(genomes)*ending)
        return genomes[start:end]

    def get_cluster_area_sorted_by_fitness(self, begin: float, ending: float) -> [Cluster]:
        """
        :param begin: float percentage starting area (0 is starting by weakest)
        :param ending: float ending area (1 is starting by fitt est)
        :return: List[Cluster] sorted by fitness
        """
        clusters = []
        for cluster in self.cluster_repository.get_current_clusters():
            clusters.append(cluster)
        clusters.sort(key=lambda cluster: cluster.fitness)
        start = int(len(clusters)*begin)
        end = int(len(clusters*ending))
        return clusters[start, end]

    def select_genomes_for_breeding(self) -> tuple(StorageGenome):
        """
        Selects genomes for breeding currently best two from all Clusters
        :return: tuple(Storage)
        """
        result = []
        for cluster in self.cluster_repository.get_current_clusters():
            result.append(self.get_genomes_from_cluster_id_by_given_percentage(
                cluster._id, #  TODO: write get id or sth.
                self.selection_parameters["start_percentage_to_breed_genomes"],  # TODO: ADD in config!
                self.selection_parameters["end_percentage_to_breed_genomes"]  # TODO: ADD in config!
            )[1])

        genome_one = random.choice(result)
        result.remove(genome_one)
        genome_two = random.choice(result)

        return tuple(genome_one, genome_two)

    def select_genome_for_mutation(self) -> StorageGenome:
        """
        Selects genome for mutation currently the best from all Clusters
        :return: StorageGenome the most fit
        """
        result = []
        for cluster in self.cluster_repository.get_current_clusters():
            result.append(self.get_genomes_in_cluster_from_cluster(
                cluster._id,  # TODO: write get id or sth.
                self.selection_parameters["start_percentage_to_mutate_genomes"],  # TODO: ADD in config!
                self.selection_parameters["end_percentage_to_mutate_genomes"]  # TODO: ADD in config!
            )[1])
        return random.choice(result)

    def select_clusters_for_combination(self) -> tuple(Cluster):
        result = self.get_current_cluster_sorted_by_fitness(
            self.selection_parameters["start_percentage_to_combinate_cluster"],  # TODO: ADD in config!
            self.selection_parameters["end_percantage_to_combinate_cluster"]  # TODO: ADD in config!
        )
        cluster_one = random.choice(result)
        result.remove(cluster_one)
        cluster_two = random.choice(result)
        return cluster_one, cluster_two

    def select_cluster_combination(self, cluster1: Cluster, cluster2: Cluster) -> List[tuple(StorageGenome)]:

        pass  # Todo

    def select_clusters_for_discarding(self) -> List[Cluster]:
        """
        select x percentage (given by selection.conf "discarding_by_cluster_fitness") of Cluster sorted ascending
        by fitness
        :return: List of Cluster wanted to be discarded
        """
        clusters = self.get_current_cluster_sorted_by_fitness()
        return clusters[:int(len(clusters)*self.selection_parameters["discarding_by_cluster_fitness"])]

    def select_genomes_for_discarding(self) -> List[StorageGenome]:
        """
        select "discarding_by_genome_fitness" percentage (in every Cluster) of genomes sorted ascending by fitness
        :return: List of Genomes wanted to be discarded
        """
        clusters = self.get_genomes_in_cluster_from_cluster()[1]
        self._reset()
        return clusters
