from fractions import Fraction
from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId

from NEAT.Analyst.Cluster import Cluster
from NEAT.Analyst.GenomeClusterer import GenomeClusterer
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.ClusterRepository import ClusterRepository
from NEAT.Repository.GenomeRepository import GenomeRepository


# noinspection PyUnresolvedReferences
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
        self.mock_cluster_repository.add_cluster_with_representative.assert_called_with(genome.genome_id)
        self.assertFalse(self.genome_clusterer._no_clusters)

    def test_cluster_genome_no_delta_less(self):
        genome = StorageGenome()
        cluster1 = Cluster()
        cluster2 = Cluster()
        storage_genome1 = StorageGenome()
        storage_genome2 = StorageGenome()
        cluster1.representative = storage_genome1
        cluster2.representative = storage_genome2
        clusters = [cluster1, cluster2]

        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=clusters)
        self.genome_clusterer.calculate_delta = MagicMock(return_value=1.9)
        self.mock_genome_repository.get_genome_by_id = lambda x: x

        self.mock_cluster_repository.add_cluster_with_representative = MagicMock()
        self.mock_genome_repository.update_genome_cluster = MagicMock()
        self.mock_cluster_repository.get_cluster_by_representative = MagicMock(return_value=cluster1)

        self.genome_clusterer.cluster_genome(genome)

<<<<<<< HEAD
        self.genome_clusterer.calculate_delta.assert_any_call(genome, storageGenome1)
        self.genome_clusterer.calculate_delta.assert_any_call(genome, storageGenome2)
        self.mock_cluster_repository.add_cluster_with_representative.assert_called_with(genome.genome_id)
        self.mock_cluster_repository.get_cluster_by_representative.assert_called_with(genome.genome_id)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.genome_id, cluster1.cluster_id)
=======
        self.genome_clusterer.calculate_delta.assert_any_call(genome, storage_genome1)
        self.genome_clusterer.calculate_delta.assert_any_call(genome, storage_genome2)
        self.mock_cluster_repository.add_cluster_with_representative.assert_called_with(genome.object_id)
        self.mock_cluster_repository.get_cluster_by_representative.assert_called_with(genome.object_id)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.object_id, cluster1.cluster_id)
>>>>>>> origin/master

    def test_cluster_genome_with_delta_less(self):
        genome = StorageGenome()
        cluster1 = Cluster()
        cluster2 = Cluster()
        storage_genome1 = StorageGenome()
        storage_genome2 = StorageGenome()
        cluster1.representative = storage_genome1
        cluster2.representative = storage_genome2
        clusters = [cluster1, cluster2]

        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=clusters)
        self.genome_clusterer.calculate_delta = MagicMock(return_value=0.1)
        self.mock_genome_repository.get_genome_by_id = lambda x: x

        self.mock_genome_repository.update_genome_cluster = MagicMock()
        self.mock_cluster_repository.get_cluster_by_representative = MagicMock(return_value=cluster1)

        self.genome_clusterer.cluster_genome(genome)

<<<<<<< HEAD
        self.genome_clusterer.calculate_delta.assert_called_with(genome, storageGenome1)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.genome_id, cluster1.cluster_id)
=======
        self.genome_clusterer.calculate_delta.assert_called_with(genome, storage_genome1)
        self.mock_genome_repository.update_genome_cluster.assert_called_with(genome.object_id, cluster1.cluster_id)
>>>>>>> origin/master

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

        smaller1 = [1, 2, 3]
        smaller2 = [2, 5]

        matching1 = [2, 3]
        diff1 = [1, 4]

        matching2 = [2]
        diff2 = [5, 1, 3]

        self.genome_clusterer.calculate_disjoint_excess_count = MagicMock(return_value=(16, 17))
        self.genome_clusterer.calculate_average_weight_difference = MagicMock(return_value=1.5)
        self.assertEqual(12.5, self.genome_clusterer.calculate_delta(genome_one, genome_two))
        self.genome_clusterer.calculate_disjoint_excess_count.assert_called_with(smaller1, diff1)
        self.genome_clusterer.calculate_average_weight_difference.assert_called_with(genome_two, genome_one, matching1)

        self.assertEqual(12.5, self.genome_clusterer.calculate_delta(genome_one, genome_three))
        self.genome_clusterer.calculate_disjoint_excess_count.assert_called_with(smaller2, diff2)
        self.genome_clusterer.calculate_average_weight_difference.assert_called_with(
            genome_one,
            genome_three,
            matching2
        )

    def test_calculate_disjoint_excess_count(self):
        smaller_genome_gene_ids = [1, 2]
        differing_genes = [2, 3, 4]
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
        matching_genes = [2, 6]
        self.assertEqual(60.5, self.genome_clusterer.calculate_average_weight_difference(genome_one,
                                                                                         genome_two,
                                                                                         matching_genes))

    def test_calculate_cluster_fitness(self):
        cluster_id = ObjectId()
        genomes = []
        for i in range(0, 4):
            g = StorageGenome()
            g.fitness = float(i)
            genomes.append(g)
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genomes)
        self.assertEqual(6.0 / 4, self.genome_clusterer.calculate_cluster_fitness(cluster_id))
        self.mock_genome_repository.get_genomes_in_cluster.assert_called_with(cluster_id)

    def test_calculate_cluster_offspring_values(self):
        clusters = []
        for i in range(0, 4):
            c = Cluster()
            c._id = i
            clusters.append(c)
        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=clusters)
        self.mock_cluster_repository.update_fitness_for_cluster = MagicMock()
        self.genome_clusterer.calculate_cluster_fitness = lambda x: x
        self.mock_cluster_repository.update_offspring_for_cluster = MagicMock()

        self.genome_clusterer.calculate_cluster_offspring_values()

        self.mock_cluster_repository.update_fitness_for_cluster.assert_any_call(0, 0)
        self.mock_cluster_repository.update_fitness_for_cluster.assert_any_call(1, 1)
        self.mock_cluster_repository.update_fitness_for_cluster.assert_any_call(2, 2)
        self.mock_cluster_repository.update_fitness_for_cluster.assert_any_call(3, 3)

        self.mock_cluster_repository.update_offspring_for_cluster.assert_any_call(0, 0)
        self.mock_cluster_repository.update_offspring_for_cluster.assert_any_call(1, 0)
        self.mock_cluster_repository.update_offspring_for_cluster.assert_any_call(2, 1)
        self.mock_cluster_repository.update_offspring_for_cluster.assert_any_call(3, 1)
