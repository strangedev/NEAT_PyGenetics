from unittest import TestCase

from bson import ObjectId

from NEAT.Analyst.GenomeClusterer import GenomeClusterer
from NEAT.Tests.MockClasses.mock_ClusterRepository import mock_ClusterRepository
from NEAT.Tests.MockClasses.mock_GenomeRepository import mock_GenomeRepository

cluster_repo = mock_ClusterRepository()
genome_repo = mock_GenomeRepository()

clustering_params = {}
clustering_params["delta_threshold"] = 0.5
clustering_params["excess_coefficient"] = 1
clustering_params["disjoint_coefficient"] = 1
clustering_params["weight_difference_coefficient"] = 1
clustering_params["max_population"] = 10
clustering_params["discarding_percentage"] = 0.2


clusterer = GenomeClusterer(genome_repo, cluster_repo, clustering_params)

class TestGenomeClusterer(TestCase):

    def test_cluster_genomes(self):

        new_cluster_repo = mock_ClusterRepository()
        new_genome_repo = mock_GenomeRepository()
        new_clusterer = GenomeClusterer(
            new_cluster_repo,
            new_genome_repo,
            new_clustering_params
        )

        new_clusterer.cluster_genomes(genome_repo.mock_population)

        self.assertEqual(
            cluster_repo.get_cluster_count(),
            2,
            "Genomes have not been put into 2 different clusters."
        )

    def test_calculate_delta(self):

        genomes = genome_repo.get_current_population()

        delta = clusterer.calculate_delta(
            genomes[0],
            genomes[1]
        )

        self.assertEqual(
            delta,
            2/3,
            "The delta value for genomes in mock_GenomeRepository does not match."
        )

    def test_calculate_disjoint_excess_count(self):

        disjoint_count, excess_count = clusterer.calculate_disjoint_excess_count(
            [1, 2, 3, 4],
            [1, 3, 4, 5],
            [2, 5]
        )

        self.assertEqual(
            disjoint_count,
            1,
            "The number of disjoint genes does not match."
        )

        self.assertEqual(
            excess_count,
            1,
            "The number of excess genes does not match."
        )

    def test_calculate_w_bar(self):

        genomes = genome_repo.get_current_population()

        w_bar = clusterer.calculate_w_bar(

            genomes[0],
            genomes[1],
            [1, 3, 4]

        )

        self.assertEqual(
            w_bar,
            1/6,
            "The average quadratic difference of gene weights does not match."
        )

    def test_calculate_cluster_fitness(self):

        clusterer.cluster_genomes(genome_repo.mock_population)

        cluster_zero_fitness = clusterer.calculate_cluster_fitness(ObjectId("000000000000000000000000"))

        self.assertEqual(
            cluster_zero_fitness,
            0.5,
            "The cluster fitness for cluster 0 does not match."
        )

        cluster_one_fitness = clusterer.calculate_cluster_fitness(ObjectId("000000000000000000000001"))

        self.assertEqual(
            cluster_one_fitness,
            0.7,
            "The cluster fitness for cluster 1 does not match."
        )

    def test_calculate_max_cluster_populations(self):

        clusterer.cluster_genomes(genome_repo.mock_population)

        clusterer.calculate_max_cluster_populations()

        self.assertEqual(
            cluster_repo.clusters[0].max_population,
            4,
            "The maximum population size for cluster 0 does not match."
        )

        self.assertEqual(
            cluster_repo.clusters[1].max_population,
            5,
            "The maximum population size for cluster 1 does not match."
        )

    def test_calculate_cluster_offspring_values(self):

        clusterer.cluster_genomes(genome_repo.mock_population)

        clusterer.calculate_cluster_offspring_values()

        self.assertEqual(
            cluster_repo.clusters[0].offspring,
            1,
            "The cluster offspring does not match the expected size."
        )

        self.assertEqual(
            cluster_repo.clusters[1].offspring,
            1,
            "The cluster offspring does not match the expected size."
        )