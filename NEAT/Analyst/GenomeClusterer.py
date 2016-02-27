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
        self.cluster_repository.archive_clusters() # new clusters will be created,
                                             # the old ones can be stored

        first_genome = current_genomes.pop(0)
        self.cluster_repository.add_cluster_with_representative(first_genome)

        for genome in current_genomes:

            clusters = self.cluster_repository.get_current_clusters()

            for cluster in clusters:

                delta = self.calculate_delta(genome, cluster.representative)

                if delta < self.clustering_parameters.delta_threshold:
                    self.cluster_repository.add_genome_to_cluster(genome, cluster)

                else:
                    self.cluster_repository.add_cluster_with_representative(genome)



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
        pass

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