from unittest import TestCase
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.Generator.Mutator import Mutator
from NEAT.Tests.MockClasses.mock_GeneRepository import mock_GeneRepository
from fractions import Fraction
from unittest.mock import MagicMock

class TestMutator(TestCase):

    def setUp(self):

        self.fail()

        self.gene_repo = MagicMock()

        id_for_endpoints = {
            (4, 8): 9,
            (8, 5): 13
        }
        # TODO: Easier graph...
        # self.gene_repo.find_connecting_nodes = (lambda h, t: [8])
        # self.gene_repo.get_node_labels_by_gene_id = (lambda id: ((id -(id % 100))/100, id % 100))
        # self.gene_repo.get_gene_id_for_endpoints = (lambda h, t:  100*h + t)
        # self.gene_repo.get_next_node_label = (lambda : 8)

        self.fitter_genome = StorageGenome()
        self.fitter_genome.fitness = 22.74
        self.fitter_genome.genes = {
            0: (True, Fraction(0.21)),
            1: (True, Fraction(-0.56)),
            2: (True, Fraction(0.354)),
            3: (True, Fraction(0.98)),
            7: (True, Fraction(0.47)),
            8: (True, Fraction(-0.13))
        }
        self.fitter_genome_ana = AnalysisGenome(self.gene_repo, self.fitter_genome)

        mutation_parameters = dict(
            {
                "add_edge_probability": 0.5,
                "new_gene_enabled_probability": 0.7,
                "perturb_gene_weight_probability": 0.5
            }
        )

        self.mutator = Mutator(self.gene_repo, mutation_parameters)

    def test_mutate_genome(self):
        self.fail()

    def test_mutate_add_edge(self):

        self.fail()

        new_genome = self.mutator.mutate_add_edge(self.fitter_genome_ana, self.fitter_genome)

        differing_genes = [gid for gid in new_genome.genes.keys() \
                           if gid not in self.fitter_genome.genes.keys()]

        print(self.fitter_genome_ana.edges)

        self.assertEqual(len(differing_genes), 1)
        print("added edge: ", differing_genes)

    def test_mutate_add_node(self):
        new_genome = self.mutator.mutate_add_node(self.fitter_genome_ana, self.fitter_genome)

        differing_genes = [gid for gid in new_genome.genes.keys() \
                           if gid not in self.fitter_genome.genes.keys()]

        self.assertEqual(len(differing_genes), 2)
        self.assertListEqual(
            differing_genes,
            [9, 13]
        )

    def test_mutate_perturb_weights(self):
        self.fail()

    def test_perturb_weight(self):
        self.fail()
