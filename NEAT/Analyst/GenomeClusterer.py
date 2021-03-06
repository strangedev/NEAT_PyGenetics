from typing import List, Tuple, Dict

from bson import ObjectId

from NEAT.GenomeStructures.StorageStructure import StorageGenome
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.Repository.GenomeRepository import GenomeRepository


class GenomeClusterer(object):
    """
    A class used for clustering genomes into species.
    """

    def __init__(
            self,
            genome_repository: GenomeRepository,
            cluster_repository: ClusterRepository,
            clustering_parameters: Dict[str, object]
    ):

        self.genome_repository = genome_repository
        self.cluster_repository = cluster_repository
        self.clustering_parameters = clustering_parameters
        self._no_clusters = (self.cluster_repository.get_cluster_count == 0)

    def cluster_genomes(self, genomes: List['StorageGenome']):
        """
        Calculates the clusters in which the passed genomes belong
        individually and updates the database
        (cluster_repository, genome_repository) accordingly.
        :param genomes: The list of genomes to put in clusters
        :return: None
        """

        for genome in genomes:
            self.cluster_genome(genome)

    def cluster_genome(self, genome: StorageGenome):
        """
        Calculates in which cluster a single genome belongs and
        updates the database (cluster_repository, genome_repository)
        accordingly.
        :param genome: The StorageGenome to put in a cluster
        :return: None
        """

        if self._no_clusters:
            self.cluster_repository.add_cluster_with_representative(genome.genome_id)
            self._no_clusters = False

        clusters = self.cluster_repository.get_current_clusters()
        for cluster in clusters:

            delta = self.calculate_delta(
                genome,
                self.genome_repository.get_genome_by_id(cluster.representative)
            )

            if delta < self.clustering_parameters["delta_threshold"]:
                self.genome_repository.update_genome_cluster(
                    genome.genome_id,
                    cluster.cluster_id
                )

                break
        else:
            self.cluster_repository.add_cluster_with_representative(genome.genome_id)
            self.genome_repository.update_genome_cluster(
                genome.genome_id,
                self.cluster_repository.get_cluster_by_representative(
                    genome.genome_id
                ).cluster_id
            )

    def calculate_delta(
            self,
            genome_one: StorageGenome.StorageGenome,
            genome_two: StorageGenome.StorageGenome
    ) -> float:
        """
        Returns a metric of topological difference for two given
        genomes.
        See https://github.com/strangedev/NEAT_PyGenetics/wiki/Delta-Function
        for more information.

        :param genome_one: The first genome
        :param genome_two: The second genome
        :return: The delta value (topological difference) of the input genomes
        """
        excess_coefficient = float(
            self.clustering_parameters["excess_coefficient"]
        )
        disjoint_coefficient = float(
            self.clustering_parameters["disjoint_coefficient"]
        )
        weight_delta_coefficient = float(
            self.clustering_parameters["weight_difference_coefficient"]
        )

        bigger_genome, smaller_genome = (genome_one, genome_two) \
            if len(genome_one.genes) > len(genome_two.genes) \
            else (genome_two, genome_one)

        bigger_genome_gene_ids = [gene for gene in bigger_genome.genes]
        smaller_genome_gene_ids = [gene for gene in smaller_genome.genes]

        all_gene_ids = smaller_genome_gene_ids + bigger_genome_gene_ids

        matching_genes = [gene_id for gene_id in bigger_genome_gene_ids
                          if gene_id in smaller_genome_gene_ids]

        differing_genes = [gene_id for gene_id in all_gene_ids
                           if gene_id not in matching_genes]

        n = len(bigger_genome.genes)
        if n == 0:
            return 0

        disjoint_count, excess_count = self.calculate_disjoint_excess_count(smaller_genome_gene_ids, differing_genes)

        w_bar = self.calculate_average_weight_difference(bigger_genome, smaller_genome, matching_genes)

        return ((excess_coefficient * excess_count) / n) + \
               ((disjoint_coefficient * disjoint_count) / n) + \
               (weight_delta_coefficient * w_bar)

    @staticmethod
    def calculate_disjoint_excess_count(
            smaller_genome_gene_ids: List[ObjectId],
            differing_gene_ids: List[ObjectId]
    ) -> Tuple[int, int]:
        """
        Calculates the amount of excess and disjoint genes
        for two genomes, given the gene ids of the smaller
        genome and the set of differing genes.
        :param smaller_genome_gene_ids: A list of gene ids of the smaller genome
        :param differing_genes: A list of differing genes
        :return: The amount of excess and disjoint genes as tuple.
        """

        smaller_genome_timestamps = [
            gene_id.generation_time
            for gene_id in smaller_genome_gene_ids
        ]

        if len(smaller_genome_timestamps) > 0:
            max_timestamp = smaller_genome_timestamps[0] # type: 'ObjectID'
        else:
            return 0, 0

        for timestamp in smaller_genome_timestamps:

            if timestamp > max_timestamp:
                max_timestamp = timestamp

        excess_genes = [
            gene_id
            for gene_id in differing_gene_ids
            if gene_id.generation_time > max_timestamp
        ]

        disjoint_genes = [
            gene_id
            for gene_id in differing_gene_ids
            if gene_id not in excess_genes
        ]

        return len(disjoint_genes), len(excess_genes)

    @staticmethod
    def calculate_average_weight_difference(
            genome_one: StorageGenome,
            genome_two: StorageGenome,
            matching_genes: List[ObjectId]
    ) -> float:
        """
        Calculates the average quadratic weight differences
        of matching genes for two given genomes.
        :param genome_one: The first genome
        :param genome_two: The second genome
        :param matching_genes: A list of matching genes for
        the two given genomes.
        :return: The average quadratic weight difference
        of matching genes.
        """

        weights = []  # type: List[Tuple[float, float]]

        for matching_gene_id in matching_genes:

            weight_one = 0
            weight_two = 0

            for gene_id in genome_one.genes:

                if gene_id == matching_gene_id:
                    weight_one = float(genome_one.genes[gene_id][1])
                    break

            for gene_id in genome_two.genes:

                if gene_id == matching_gene_id:
                    weight_two = float(genome_two.genes[gene_id][1])
                    break

            weights.append((weight_one, weight_two))

        w_bar = sum(
            [(weight_one - weight_two) ** 2 for (weight_one, weight_two) in weights]
        ) / len(matching_genes) if len(matching_genes) > 0 else 0  # type: float

        return w_bar

    def calculate_cluster_fitness(self, cluster_id: ObjectId):
        """
        Calculates the shared fitness value for a given cluster based
        on the cluster size and the individual fitness values of the
        contained individuals.

        :param cluster_id: The id of the cluster
        :return: The shared fitness value for the input cluster
        """

        genomes = self.genome_repository.get_genomes_in_cluster(cluster_id)

        cluster_fitness = 0

        for genome in genomes:
            cluster_fitness += genome.fitness
        if cluster_fitness == 0:
            return 0

        return cluster_fitness / len(list(genomes))

    def calculate_cluster_offspring_values(self):
        """
        Calculates the number of offspring the clusters will generate
        in the next generation cycle, based on the compared
        shared fitness values of all active clusters. Fitter clusters
        will receive a bigger number of offspring.

        :return: None
        """

        clusters = self.cluster_repository.get_current_clusters()
        max_population = self.clustering_parameters["max_population"]
        discarding_percentage = self.clustering_parameters["discarding_percentage"]

        to_replace = int(max_population) * float(discarding_percentage)

        for cluster in clusters:
            cluster.fitness = self.calculate_cluster_fitness(cluster.cluster_id)
            self.cluster_repository.update_fitness_for_cluster(
                cluster.cluster_id,
                cluster.fitness
            )

        cluster_fitness_sum = sum([cluster.fitness for cluster in clusters])

        for cluster in clusters:
            if cluster_fitness_sum == 0:
                cluster.offspring = 0
            else:
                cluster.offspring = int(
                    round((cluster.fitness / cluster_fitness_sum) * to_replace)
                )
            self.cluster_repository.update_offspring_for_cluster(
                cluster.cluster_id,
                cluster.offspring
            )
