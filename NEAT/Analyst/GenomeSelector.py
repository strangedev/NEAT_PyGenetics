from fractions import Fraction
from typing import List, Tuple
from bson import ObjectId

from NEAT.Analyst.Cluster import Cluster
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.Utilities.ProbabilisticTools import weighted_choice_range


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

    def get_genomes_in_cluster(
            self,
            cluster_id: ObjectId,
            begin: float,
            ending: float) -> List[[StorageGenome], List[Tuple[StorageGenome, Fraction]]]:
        """
        Selects and Area of genomes in Cluster given by input
        offspring.
        :param cluster_id: ObjectId to load Genomes
        :param begin: float where to begin to select genomes
        :param ending: float where to end select genomes
        :return: [StorageGenome]
        """
        genomes1 = []
        genomes2 = []
        for genome in self.genome_repository.get_genomes_in_cluster(cluster_id):
            genomes1.append(genome)
            genomes2.append((genome, genome.fitness))
        genomes1.sort(key=lambda g: g.fitness)
        start = int(len(genomes1)*begin)
        end = int(len(genomes1)*ending)
        return [genomes1[start:end], genomes2]

    def get_cluster_area_sorted_by_fitness(self, begin: float, ending: float) -> [Cluster]:
        """
        :param begin: float percentage starting area (0 is starting by weakest)
        :param ending: float ending area (1 is starting by fitt est)
        :return: List[Cluster] sorted by fitness
        """
        clusters = []
        for cluster in self.cluster_repository.get_current_clusters():
            clusters.append(cluster)
        clusters.sort(key=lambda c: c.fitness)
        start = int(len(clusters)*begin)
        end = int(len(clusters*ending))
        return clusters[start:end]

    def select_genomes_for_breeding(self, mutation_percentage: float) -> List[tuple(StorageGenome)]:
        """
        Selects genomes for breeding currently best two from all Clusters
        :type mutation_percentage: float
        :return: tuple(Storage)
        """
        result = []
        for cluster in self.cluster_repository.get_current_clusters():
            genome_one = self.get_genomes_in_cluster(cluster._id)[1]
            genome_two = genome_one
            seats_to_mutation = int(cluster.offspring * mutation_percentage)
            result.append(list(zip(
                weighted_choice_range(genome_one, seats_to_mutation),
                weighted_choice_range(genome_two, seats_to_mutation)
            )))

        return result

    def select_genome_for_mutation(self, mutation_percentage: float) -> List[StorageGenome]:
        """
        Selects genome for mutation currently the best from all Clusters
        :param mutation_percentage: float
        :return: StorageGenome the most fit
        """
        result = []
        for cluster in self.cluster_repository.get_current_clusters():
            step = self.get_genomes_in_cluster(cluster._id)
            seats_to_mutation = int(cluster.offspring * mutation_percentage)

            result.append(weighted_choice_range(
                step,
                seats_to_mutation)
            )
        return result

    def select_clusters_for_combinations(self) -> Tuple[Cluster]:
        """

        :return: Tuple[Cluster] cluster chosen for combination
        """
        step = []
        for cluster in self.cluster_repository.get_current_clusters():
            step.append((cluster, cluster.fitness))

        cluster_one = weighted_choice_range(step, 2)[0]
        cluster_two = weighted_choice_range(step, 2)[1]
        return cluster_one, cluster_two

    def select_cluster_combination(
            self,
            cluster1: Cluster,
            cluster2: Cluster,
            genome_count: int) -> List[Tuple[StorageGenome]]:
        """
        :param cluster1: Cluster to choose 1
        :param cluster2: Cluster to choose 2
        :param genome_count: int number of seats which should be filled
        :return: List[Tuple[StorageGenome]] combination from given cluster
        """
        genomes1 = self.get_genomes_in_cluster(cluster1._id)[1]
        genomes2 = self.get_genomes_in_cluster(cluster2._id)[1]
        g1 = weighted_choice_range(genomes1, genome_count)
        g2 = weighted_choice_range(genomes2, genome_count)
        return list(zip(g1, g2))

    def select_clusters_for_discarding(self) -> List[Cluster]:
        """
        select x percentage (given by selection.conf "discarding_by_cluster_fitness") of Cluster sorted ascending
        by fitness
        :return: List of Cluster wanted to be discarded
        """
        clusters = self.get_cluster_area_sorted_by_fitness(
            0.0,
            self.selection_parameters["discarding_by_cluster_fitness"]
        )
        return clusters

    def select_genomes_for_discarding(self) -> List[StorageGenome]:
        """
        select "discarding_by_genome_fitness" percentage (in every Cluster) of genomes sorted ascending by fitness
        :return: List of Genomes wanted to be discarded
        """
        genomes = []
        for cluster in self.cluster_repository.get_current_clusters():
            genomes.append(self.get_genomes_in_cluster(
                cluster._id,
                0.0,
                self.selection_parameters["discarding_by_genome_fitness"]
            )[0])
        return genomes
