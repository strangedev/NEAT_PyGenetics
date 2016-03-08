from bson import ObjectId
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.GenomeStructures.StorageStructure import StorageGenome
from typing import List, Tuple, Dict

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

    def cluster_genomes(self, genomes: List[object]):

        for genome in genomes:
            self.cluster_genome(genome)

    def cluster_genome(self, genome: StorageGenome):

        if self._no_clusters: # TODO:
            self.cluster_repository.add_cluster_with_representative(genome._id) # TODO:
            self._no_clusters = False

        clusters = self.cluster_repository.get_current_clusters() # TODO:

        for cluster in clusters:

            delta = self.calculate_delta(
                genome,
                self.genome_repository.get_genome_by_id(cluster.representative) # TODO:
            )

            if delta < self.clustering_parameters["delta_threshold"]:
                self.genome_repository.update_cluster_for_genome( # TODO:
                    genome._id,
                    cluster._id
                )

                break
        else:
            self.cluster_repository.add_cluster_with_representative(genome._id) # TODO:
            self.genome_repository.update_cluster_for_genome( # TODO:
                genome._id,
                self.cluster_repository.get_cluster_by_representative(genome._id)._id # TODO:
            )

    def calculate_delta(
            self,
            genome_one: StorageGenome.StorageGenome,
            genome_two: StorageGenome.StorageGenome
    ) -> float:
        """
        Returns a metric of topological difference for two given
        genomes.

        :param genome_one: The first genome
        :param genome_two: The second genome
        :return: The delta value (topological difference) of the input genomes
        """
        excess_coeff = self.clustering_parameters["excess_coefficient"]
        disjoint_coeff = self.clustering_parameters["disjoint_coefficient"]
        weight_delta_coeff = self.clustering_parameters["weight_difference_coefficient"]

        bigger_genome, smaller_genome = (genome_one, genome_two) \
            if len(genome_one.genes) > len(genome_two.genes) \
            else (genome_two, genome_one)

        bigger_genome_gene_ids = [gene[0] for gene in bigger_genome.genes]
        smaller_genome_gene_ids = [gene[0] for gene in smaller_genome.genes]

        all_gene_ids = smaller_genome_gene_ids + bigger_genome_gene_ids

        matching_genes = [gene_id for gene_id in bigger_genome_gene_ids \
                          if gene_id in smaller_genome_gene_ids]

        differing_genes = [gene_id for gene_id in all_gene_ids \
                           if gene_id not in matching_genes]

        n = len(bigger_genome.genes)

        disjoint_count, excess_count = self.calculate_disjoint_excess_count(
            smaller_genome_gene_ids,
            bigger_genome_gene_ids,
            differing_genes
        )

        w_bar = self.calculate_w_bar(bigger_genome, smaller_genome, matching_genes)

        return ((excess_coeff * excess_count) / n) \
               + ((disjoint_coeff * disjoint_count) / n) \
               + (weight_delta_coeff * w_bar)

    def calculate_disjoint_excess_count(
            self,
            smaller_genome_gene_ids: List[int],
            bigger_genome_gene_ids: List[int],
            differing_genes: List[int]
    ) -> Tuple[int, int]:

        smaller_genome_range = 0 # type: int

        for gene_id in smaller_genome_gene_ids:

            if gene_id > smaller_genome_range:
                smaller_genome_range = gene_id

        excess_genes = [gene_id for gene_id in differing_genes \
                        if gene_id > smaller_genome_range]

        disjoint_genes = [gene_id for gene_id in differing_genes \
                          if gene_id not in excess_genes]

        return (len(disjoint_genes), len(excess_genes))

    def calculate_w_bar(
            self,
            genome_one: StorageGenome,
            genome_two: StorageGenome,
            matching_genes: List[int]
    ) -> float:

        weights = [] # type: List[int]

        for gene_id in matching_genes:

            weight_one = 0
            weight_two = 0

            for gene in genome_two.genes:

                if gene[0] == gene_id:
                    weight_one = gene[2]
                    break

            for gene in genome_one.genes:

                if gene[0] == gene_id:
                    weight_two = gene[2]
                    break

            weights.append((weight_one, weight_two))

        w_bar = sum(
                    [(weight_one - weight_two)**2 for (weight_one, weight_two) in weights]
                ) / len(matching_genes) # type: float

        return w_bar

    def calculate_cluster_fitness(self, cluster_id: ObjectId):
        """
        Calculates the shared fitness value for a given cluster based
        on the cluster size and the individual fitness values of the
        contained individuals.

        :param cluster_id: The id of the cluster
        :return: The shared fitness value for the input cluster
        """

        genomes = self.genome_repository.get_genomes_in_cluster(cluster_id) # TODO:

        cluster_fitness = 0

        for genome in genomes:
            cluster_fitness += genome.fitness

        return cluster_fitness / len(list(genomes))


    def calculate_cluster_offspring_values(self):
        """
        Calculates the number of offspring the clusters will generate
        in the next generation cycle, based on the compared
        shared fitness values of all active clusters. Fitter clusters
        will receive a bigger number of offspring.

        :return: None
        """

        clusters = self.cluster_repository.get_current_clusters() # TODO:
        max_population = self.clustering_parameters["max_population"]
        discarding_percentage = self.clustering_parameters["discarding_percentage"]

        to_replace = max_population * discarding_percentage

        for cluster in clusters:
            cluster.fitness = self.calculate_cluster_fitness(cluster._id)
            self.cluster_repository.update_fitness_for_cluster( # TODO:
                cluster._id,
                cluster.fitness
            )

        cluster_fitness_sum = sum([cluster.fitness for cluster in clusters])

        for cluster in clusters:

            cluster.offspring = int(
                round((cluster.fitness / cluster_fitness_sum) * to_replace)
            )
            self.cluster_repository.update_offspring_for_cluster( # TODO:
                cluster._id,
                cluster.offspring
            )

    def calculate_max_cluster_populations(self):
        """
        DEPRECATED

        Calculates the number of individuals the clusters will be able
        to contain until the next clustering, based on the compared
        shared fitness values of all active clusters. Fitter clusters
        will receive a bigger population.

        :return: None
        """

        max_population = self.clustering_parameters["max_population"]

        clusters = self.cluster_repository.get_current_clusters() # TODO:

        for cluster in clusters:
            cluster.fitness = self.calculate_cluster_fitness(cluster._id)
            self.cluster_repository.update_fitness_for_cluster( # TODO:
                cluster._id,
                cluster.fitness
            )

        cluster_fitness_sum = sum([cluster.fitness for cluster in clusters])

        for cluster in clusters:

            cluster.max_population = int((cluster.fitness / cluster_fitness_sum) * max_population)
            self.cluster_repository.update_max_population_for_cluster( # TODO:
                cluster._id,
                cluster.max_population
            )

