from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.GenomeStructures.StorageStructure import StorageGenome
from NEAT.Analyst.Cluster import Cluster

class GenomeClusterer(object):
    """
    A class used for clustering genomes into species.
    """

    def __init__(
            self,
            genome_repository: GenomeRepository,
            cluster_repository: ClusterRepository,
            clustering_parameters
    ):

        self.genome_repository = genome_repository
        self.cluster_repository = cluster_repository
        self.clustering_parameters = clustering_parameters


    def cluster_genomes(self):
        """
        Compares all genomes of the current population by topological
        similarity and assigns a number to the genome, based on which
        cluster it is in.
        :return: None
        """

        current_genomes = list(self.genome_repository.get_current_population())

        if self.cluster_repository.get_cluster_count == 0:
            first_genome = current_genomes.pop(0)
            self.cluster_repository.add_cluster_with_representative(first_genome.id)


        for genome in current_genomes:

            genome_placed_in_cluster = False
            clusters = self.cluster_repository.get_current_clusters()

            for cluster in clusters:

                delta = self.calculate_delta(genome, cluster.representative)

                if delta < self.clustering_parameters.delta_threshold:
                    self.genome_repository.update_cluster_for_genome(
                        genome.id,
                        cluster.id
                    )

                    genome_placed_in_cluster = True

                    break

            if not genome_placed_in_cluster:
                self.cluster_repository.add_cluster_with_representative(genome)
                self.genome_repository.update_cluster_for_genome(
                    genome.id,
                    self.cluster_repository.get_cluster_by_representative(genome.id).id
                )

    def calculate_delta(
            self,
            genome_one: StorageGenome.StorageGenome,
            genome_two: StorageGenome.StorageGenome
    ):
        """
        Returns a metric of topological difference for two given
        genomes.

        :param genome_one: The first genome
        :param genome_two: The second genome
        :return: The delta value (topological difference) of the input genomes
        """
        excess_coeff = self.clustering_parameters.excess_coefficient
        disjoint_coeff = self.clustering_parameters.disjoint_coefficient
        weight_delta_coeff = self.clustering_parameters.weight_difference_coefficient

        bigger_genome, smaller_genome = (genome_one, genome_two) \
            if len(genome_one.genes) > len(genome_two.genes) \
            else (genome_two, genome_one)

        all_genes = smaller_genome.genes + bigger_genome.genes

        matching_genes = [gene_id for gene_id in genome_one.genes \
                          if gene_id in genome_two.genes]

        differing_genes = [gene_id for gene_id in all_genes \
                           if gene_id not in matching_genes]

        n = len(bigger_genome.genes)
        disjoint_count, excess_count = self.calculate_disjoint_excess_count(
            smaller_genome,
            bigger_genome,
            differing_genes
        )
        w_bar = self.calculate_w_bar(bigger_genome, smaller_genome)

        return ((excess_coeff * excess_count) / n) \
               + ((disjoint_coeff * disjoint_count) / n) \
               + (weight_delta_coeff * w_bar)

    def calculate_disjoint_excess_count(
            self,
            smaller_genome,
            bigger_genome,
            differing_genes
    ):
        smaller_genome_range = 0

        for gene_id in smaller_genome.genes:

            if gene_id > smaller_genome_range:
                smaller_genome_range = gene_id

        excess_genes = [gene_id for gene_id in differing_genes \
                        if gene_id > smaller_genome_range]

        disjoint_genes = [gene_id for gene_id in differing_genes \
                          if gene_id not in excess_genes]

        return (len(disjoint_genes), len(excess_genes))

    def calculate_w_bar(self, genome_one, genome_two, matching_genes):

        weights = []

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
                ) / len(matching_genes)

        return w_bar


    def calculate_shared_fitness(self, cluster_id: int):
        """
        Calculates the shared fitness value for a given cluster based
        on the cluster size and the individual fitness values of the
        contained individuals.

        :param cluster_id: The id of the cluster
        :return: The shared fitness value for the input cluster
        """
        pass

    def calculate_max_cluster_populations(self):
        """
        Calculates the number of individuals the clusters will be able
        to contain until the next clustering, based on the compared
        shared fitness values of all active clusters. Fitter clusters
        will receive a bigger population.

        :return: None
        """
        pass