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

    def get_genomes_in_given_area_by_cluster_id(
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
        return clusters[start:end]

    def select_genomes_for_breeding(self) -> tuple(StorageGenome):
        """
        Selects genomes for breeding currently best two from all Clusters
        :return: tuple(Storage)
        """
        result = []
        for cluster in self.cluster_repository.get_current_clusters():
            result.append(self.get_genomes_in_given_area_by_cluster_id(
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
            result.append(self.get_genomes_in_given_area_by_cluster_id(
                cluster._id,  # TODO: write get id or sth.
                self.selection_parameters["start_percentage_to_mutate_genomes"],  # TODO: ADD in config!
                self.selection_parameters["end_percentage_to_mutate_genomes"]  # TODO: ADD in config!
            )[1])
        return random.choice(result)

    def select_clusters_for_combination(self) -> tuple(Cluster):
        result = self.get_cluster_area_sorted_by_fitness(
            self.selection_parameters["start_percentage_to_combination_cluster"],  # TODO: ADD in config!
            self.selection_parameters["end_percentage_to_combination_cluster"]  # TODO: ADD in config!
        )
        cluster_one = random.choice(result)
        result.remove(cluster_one)
        cluster_two = random.choice(result)
        return cluster_one, cluster_two

    def select_cluster_combination(self, cluster1: Cluster, cluster2: Cluster) -> List[tuple(StorageGenome)]:
        result = []
        length_cluster1 = len(list(self.genome_repository.get_current_population(cluster1._id)))
        length_cluster2 = len(list(self.genome_repository.get_current_population(cluster2._id)))
        dif_cluster1 = 0.0
        dif_cluster2 = 0.0

        if length_cluster1 >= length_cluster2:
            dif_cluster1 = float(length_cluster2) / float(length_cluster1)
        else:
            dif_cluster2 = float(length_cluster1) / float(length_cluster2)

        genomes_from_cluster1 = self.get_genomes_in_given_area_by_cluster_id(cluster1._id, dif_cluster1, 1.0)
        genomes_from_cluster2 = self.get_genomes_in_given_area_by_cluster_id(cluster2._id, dif_cluster2, 1.0)

        if len(genomes_from_cluster1) != len(genomes_from_cluster2):
            return None  # TODO: Throw exception!

        while len(genomes_from_cluster1) != 0:
            genome_one = random.choice(genomes_from_cluster1)
            genomes_from_cluster1.remove(genome_one)
            genome_two = random.choice(genomes_from_cluster2)
            genomes_from_cluster2.remove(genome_two)
            result.append((genome_one, genome_two))
        return result

    def select_clusters_for_discarding(self) -> List[Cluster]:
        """
        select x percentage (given by selection.conf "discarding_by_cluster_fitness") of Cluster sorted ascending
        by fitness
        :return: List of Cluster wanted to be discarded
        """
        clusters = self.get_cluster_area_sorted_by_fitness(0.0, self.selection_parameters["discarding_by_cluster_fitness"])
        return clusters

    def select_genomes_for_discarding(self) -> List[StorageGenome]:
        """
        select "discarding_by_genome_fitness" percentage (in every Cluster) of genomes sorted ascending by fitness
        :return: List of Genomes wanted to be discarded
        """
        genomes = []
        for cluster in self.cluster_repository.get_current_clusters()
            genomes.append(self.get_genomes_in_given_area_by_cluster_id(
                cluster._id,
                0.0,
                self.selection_parameters["discarding_by_genome_fitness"]
            )
        return genomes
