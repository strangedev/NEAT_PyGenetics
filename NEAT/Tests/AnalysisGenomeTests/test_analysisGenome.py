from unittest import TestCase
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome
from NEAT.Tests.MockClasses.MockGeneRepository import MockGeneRepository
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class TestAnalysisGenome(TestCase):
    def test__add_node(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertSetEqual(ana._nodes, set({}))

        ana._add_node(6)
        self.assertSetEqual(ana._nodes, {6})

        ana._add_node(10)
        self.assertSetEqual(ana._nodes, {6, 10})

    def test__add_edge(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_node(1)
        ana._add_node(2)

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test__add_edge_without_preadded_nodes(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test__add_edge_with_preadded_source_node(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_node(1)

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test_init_from_storage_structure(self):
        self.fail()

    def test__add_input_node(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._input_nodes, {})

        ana._add_input_node(1, "A")
        self.assertDictEqual(ana._input_nodes, {"A": 1})

    def test__add_output_node(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._output_nodes, {})

        ana._add_output_node(1, "A")
        self.assertDictEqual(ana._output_nodes, {"A": 1})
