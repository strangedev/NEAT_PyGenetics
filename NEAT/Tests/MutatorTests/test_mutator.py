from unittest import TestCase
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.Generator.Mutator import Mutator
from NEAT.Tests.MockClasses.mock_GeneRepository import mock_GeneRepository
from fractions import Fraction
from unittest.mock import MagicMock

mutation_parameters = dict(
    {
        "add_edge_probability": 0.5,
        "new_gene_enabled_probability": 0.7,
        "perturb_gene_weight_probability": 0.5
    }
)

class TestMutator(TestCase):
    def test_mutate_genome(self):
        self.fail()

    def test_mutate_add_edge(self):

        gene_repo = MagicMock()

        edges = {
            0: (0, 1),
            1: (2, 6),
            2: (6, 7),
            3: (7, 1),
            7: (7, 3),
            8: (4, 5),
            9: (4, 8),
            13: (8, 5),
        }

        gene_repo.get_node_labels_by_gene_id = (lambda id: edges[id])
        gene_repo.get_gene_id_for_endpoints = (lambda h, t: 14)

        fitter_genome = StorageGenome()
        fitter_genome.fitness = 22.74
        fitter_genome.genes = {
            0: (True, Fraction(0.21)),
            1: (True, Fraction(-0.56)),
            2: (True, Fraction(0.354)),
            3: (True, Fraction(0.98)),
            7: (True, Fraction(0.47)),
            8: (True, Fraction(-0.13))
        }
        fitter_genome_ana = AnalysisGenome(gene_repo, fitter_genome)

        mutator = Mutator(gene_repo, mutation_parameters)
        new_genome = mutator.mutate_add_edge(fitter_genome_ana, fitter_genome)

        differing_genes = [gid for gid in new_genome.genes.keys() \
                           if gid not in fitter_genome.genes.keys()]

        self.assertEqual(len(differing_genes), 1)
        self.assertEqual(differing_genes[0], 14)

    def test_mutate_add_node(self):
        self.fail()

    def test_mutate_perturb_weights(self):
        self.fail()

    def test_perturb_weight(self):
        self.fail()
