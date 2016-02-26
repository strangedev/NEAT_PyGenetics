
class GenomeClusterer(object):
    """
    A class used for clustering genomes into species.
    """

    def __init__(self):
        pass

    def cluster_genomes(self):
        """
        Compares all genomes of the current population by topological
        similarity and assigns a number to the genome, based on which
        cluster it is in.
        :return: None
        """
        pass

    def calculate_delta(self, genome_one, genome_two):
        """
        Returns a metric of topological difference for two given
        genomes.

        :param genome_one: The first genome
        :param genome_two: The second genome
        :return: The delta value (topological difference) of the input genomes
        """
        pass

    def calculate_shared_fitness(self, cluster_id):
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