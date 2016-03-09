from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId

from NEAT.Analyst.Cluster import Cluster
from NEAT.Analyst.GenomeSelector import GenomeSelector
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Tests.MockClasses.mock_ClusterRepository import mock_ClusterRepository
from NEAT.Tests.MockClasses.mock_GenomeRepository import mock_GenomeRepository


class test_genomeSelector(TestCase):
    def setUp(self):
        self.mock_genome_repository = MagicMock()
        self.mock_cluster_repository = MagicMock()
        self.mock_selection_parameters = {"discarding_by_genome_fitness": 0.2,
                                          "discarding_by_cluster_fitness": 0.2}
        self.genome_selector = GenomeSelector(
            self.mock_genome_repository,
            self.mock_cluster_repository,
            self.mock_selection_parameters
        )

    def test_getGenomesInCluster(self):
        genomes = []
        genomes_in_tupel = []
        for g in range(1,10):
            genome = StorageGenome()
            genome.fitness = float(1/g)
            genomes.append(genome)
            genomes_in_tupel.append((genome, genome.fitness))
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genomes)

        self.assertListEqual(genomes_in_tupel, self.genome_selector.get_genomes_in_cluster(0))

    def test_getClusterAreaSortedByFitness(self):
        unsorted = [0.0, 1.0, 2.4, 0.4, 0.9, 0.12, 4.32, 3.2, 5.1, 0.55]
        chosen = [0.4, 0.55, 0.9, 1.0, 2.4, 3.2]
        discard = [0.0, 0.12]
        result = []
        cluster = []
        cluster_chosen = []
        cluster_discard = []
        for i in unsorted:
            c = Cluster()
            c.fitness = i
            cluster.append(c)
            if i in chosen:
                cluster_chosen.append(c)
            if i in discard:
                cluster_discard.append(c)
        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=cluster)

        cluster_chosen.sort(key= lambda c: c.fitness)

        self.assertListEqual(cluster_chosen, self.genome_selector.get_cluster_area_sorted_by_fitness(0.2, 0.8))
        self.assertListEqual(cluster_discard, self.genome_selector.select_clusters_for_discarding())

    def test_selectGenomesForBreeding_and_selectGenomesForMutation(self):
        offspring = [10, 10, 10, 10]
        cluster = []
        genome = []
        for i in offspring:
            c = Cluster()
            c.offspring = i
            cluster.append(c)
        for i in range(0,8):
            g = StorageGenome()
            g.fitness = float(1/(i+1))
            genome.append(g)
        c = Cluster()
        g = StorageGenome()

        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=cluster)
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genome)
        self.assertEqual(8, len(self.genome_selector.select_genomes_for_breeding(0.2)))
        self.assertEqual(type(g), type(self.genome_selector.select_genomes_for_breeding(0.2)[0][0]))
        self.assertEqual(type(g), type(self.genome_selector.select_genomes_for_mutation(0.2)[0]))
        self.assertEqual(8, len(self.genome_selector.select_genomes_for_mutation(0.2)))

    def test_selectClusterForCombination(self):
        offspring = [10, 10, 10, 10]
        cluster = []
        counter = 0
        for i in offspring:
            c = Cluster()
            c.offspring = i
            c.fitness = float(1/(counter+1))
            cluster.append(c)
            counter += 1
        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=cluster)
        c = Cluster()
        d = (c, c)
        test_comb = self.genome_selector.select_clusters_for_combinations()
        self.assertEqual(type(d), type(self.genome_selector.select_clusters_for_combinations()))
        self.assertFalse(
            test_comb[0].__eq__(
            test_comb[1]
            )
        )

    def test_selectClusterCombination(self):
        offspring = [10, 10]
        cluster = []
        genome = []
        for i in offspring:
            c = Cluster()
            c.offspring = i
            cluster.append(c)
        for i in range(0,8):
            g = StorageGenome()
            g.fitness = float(1/(i+1))
            genome.append(g)
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genome)
        test_comb = self.genome_selector.select_cluster_combination(cluster[0], cluster[1], 2)
        g = StorageGenome()
        g_type = (g, g)
        g_list = [g_type]
        self.assertEqual(2, len(test_comb))
        self.assertEqual(type(g_list), type(test_comb))
        self.assertEqual(2, len(test_comb[0]))
        self.assertEqual(type(g_type), type(test_comb[0]))

    def test_selectGenomesForDiscarding(self):
        """
        checks if 20% of worst cluster or genomes were selected
        :return:
        """
        cluster = []
        genome = []
        for i in range(0,4):
            c = Cluster()
            c.offspring = i
            cluster.append(c)
        for i in range(0,10):
            g = StorageGenome()
            g.fitness = float(1/(i+1))
            genome.append(g)
        self.mock_cluster_repository.get_current_clusters = MagicMock(return_value=cluster)
        self.mock_genome_repository.get_genomes_in_cluster = MagicMock(return_value=genome)
        self.assertEqual(8, len(self.genome_selector.select_genomes_for_discarding()))





