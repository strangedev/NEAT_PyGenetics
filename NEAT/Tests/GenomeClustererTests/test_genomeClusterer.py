from fractions import Fraction
from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId

from NEAT.Analyst.Cluster import Cluster
from NEAT.Analyst.GenomeClusterer import GenomeClusterer
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.Tests.MockClasses.mock_ClusterRepository import mock_ClusterRepository
from NEAT.Tests.MockClasses.mock_GenomeRepository import mock_GenomeRepository


class TestGenomeClusterer(TestCase):
    def setUp(self):
        clustering_params = {"delta_threshold": 0.5, "excess_coefficient": 1, "disjoint_coefficient": 1,
                             "weight_difference_coefficient": 1, "max_population": 10, "discarding_percentage": 0.2}
        self.clustering_parameters = clustering_params

        self.db_connector = MagicMock()
        self.mock_genome_repository = GenomeRepository(self.db_connector)
        self.mock_cluster_repository = ClusterRepository(self.db_connector)
        # Will return 1, so _no_clusters will be false
        self.mock_cluster_repository.get_cluster_count = 1

        self.genome_clusterer = GenomeClusterer(
            self.mock_genome_repository,
            self.mock_cluster_repository,
            self.clustering_parameters
        )

    def test_cluster_genome_no_clusters(self):
        self.genome_clusterer._no_clusters = True
        self.mock_cluster_repository.add_cluster_with_representative = MagicMock()

        genome = StorageGenome()
        self.genome_clusterer.cluster_genome(genome)
        self.mock_cluster_repository.add_cluster_with_representative.assert_called_with(genome.object_id)
        self.assertFalse(self.genome_clusterer._no_clusters)

    def test_cluster_genome_no_delta_less(self):
        genome = StorageGenome()
        cluster1 = Cluster()
        cluster2 = Cluster()
        storageGenome1 = StorageGenome()
        storageGenome2 = StorageGenome()
        cluster1.representative = storageGenome1
        cluster2.representative = storageGenome2
        clusters = [cluster1, cluster2]

        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=clusters)
        self.genome_clusterer.calculate_delta = MagicMock(return_value=1.9)
        self.mock_genome_repository.get_genome_by_id = lambda x: x

        self.mock_cluster_repository.add_cluster_with_representative = MagicMock()
        self.mock_genome_repository.update_genome_cluster = MagicMock()
        self.mock_cluster_repository.get_cluster_by_representative = MagicMock(return_value=cluster1)

        self.genome_clusterer.cluster_genome(genome)

        self.genome_clusterer.calculate_delta.assert_any_call(genome, storageGenome1)
        self.genome_clusterer.calculate_delta.assert_any_call(genome, storageGenome2)
        self.mock_cluster_repository.add_cluster_with_representative.assert_called_with(genome.object_id)
        self.mock_cluster_repository.get_cluster_by_representative.assert_called_with(genome.object_id)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.object_id, cluster1.cluster_id)

    def test_cluster_genome_with_delta_less(self):
        genome = StorageGenome()
        cluster1 = Cluster()
        cluster2 = Cluster()
        storageGenome1 = StorageGenome()
        storageGenome2 = StorageGenome()
        cluster1.representative = storageGenome1
        cluster2.representative = storageGenome2
        clusters = [cluster1, cluster2]

        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=clusters)
        self.genome_clusterer.calculate_delta = MagicMock(return_value=0.1)
        self.mock_genome_repository.get_genome_by_id = lambda x: x

        self.mock_genome_repository.update_genome_cluster = MagicMock()
        self.mock_cluster_repository.get_cluster_by_representative = MagicMock(return_value=cluster1)

        self.genome_clusterer.cluster_genome(genome)

        self.genome_clusterer.calculate_delta.assert_called_with(genome, storageGenome1)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.object_id, cluster1.cluster_id)

    def test_calculate_delta(self):
        genome_one = StorageGenome()
        genome_two = StorageGenome()
        genome_three = StorageGenome()
        genome_one.genes = {
            1: (True, Fraction(1.1)),
            3: (True, Fraction(2.2)),
            2: (False, Fraction(1.1))
        }
        genome_two.genes = {
            2: (False, Fraction(1.1)),
            3: (True, Fraction(2.2)),
            4: (False, Fraction(2.2))
        }
        genome_three.genes = {
            2: (False, Fraction(1.1)),
            5: (True, Fraction(3.3))
        }

        smaller1 = [1,2,3]
        smaller2 = [2,5]

        matching1 = [2,3]
        diff1 = [1,4]

        matching2 = [2]
        diff2 = [5,1,3]

        self.genome_clusterer.calculate_disjoint_excess_count = MagicMock(return_value=(16, 17))
        self.genome_clusterer.calculate_w_bar = MagicMock(return_value=1.5)
        self.assertEqual(12.5, self.genome_clusterer.calculate_delta(genome_one, genome_two))
        self.genome_clusterer.calculate_disjoint_excess_count.assert_called_with(smaller1, diff1)
        self.genome_clusterer.calculate_w_bar.assert_called_with(genome_two, genome_one, matching1)

        self.assertEqual(12.5, self.genome_clusterer.calculate_delta(genome_one, genome_three))
        self.genome_clusterer.calculate_disjoint_excess_count.assert_called_with(smaller2, diff2)
        self.genome_clusterer.calculate_w_bar.assert_called_with(genome_one, genome_three, matching2)

    def test_calculate_disjoint_excess_count(self):
        smaller_genome_gene_ids = [1,2]
        differing_genes = [2,3,4]
        self.assertEqual(
            (1, 2),
            self.genome_clusterer.calculate_disjoint_excess_count(smaller_genome_gene_ids, differing_genes)
        )

    def test_calculate_w_bar(self):
        genome_one = StorageGenome()
        genome_two = StorageGenome()
        genome_one.genes = {
            2: (False, Fraction(12.1)),
            3: (True, Fraction(2.2)),
            4: (False, Fraction(2.2)),
            6: (True, Fraction(2.3))
        }
        genome_two.genes = {
            2: (False, Fraction(1.1)),
            5: (True, Fraction(3.3)),
            6: (True, Fraction(2.3))
        }
        matching_genes = [2,6]
        weight_two = 1.1
        weight_one = 12.1
        weights = [(weight_one, weight_two), (2.3, 2.3)]
        self.assertEqual(60.5, self.genome_clusterer.calculate_w_bar(genome_one, genome_two, matching_genes))

    def test_calculate_cluster_fitness(self):
        cluster_id = ObjectId()
        genomes = []
        for i in range(0,4):
            g = StorageGenome()
            g.fitness = float(i)
            genomes.append(g)
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genomes)
        self.assertEqual((6.0)/4, self.genome_clusterer.calculate_cluster_fitness(cluster_id))
        self.mock_genome_repository.get_genomes_in_cluster.assert_called_with(cluster_id)

"""
    def test_cluster_genomes(self):

        new_cluster_repo = mock_ClusterRepository()
        new_genome_repo = mock_GenomeRepository()
        new_clusterer = GenomeClusterer(
            new_genome_repo,
            new_cluster_repo,
            clustering_params
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

        disjoint_count, excess_count = clusterer.calculate_disjoint_excess_count([1, 2, 3, 4], [2, 5])

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
"""
