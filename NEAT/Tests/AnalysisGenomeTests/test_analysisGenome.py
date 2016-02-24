from unittest import TestCase
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome
from NEAT.Tests.MockClasses.MockGeneRepository import MockGeneRepository
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class TestAnalysisGenome(TestCase):
    def setUp(self):
        self.mock_gene_repository = MockGeneRepository()
        self.storage_genome = StorageGenome()

    def test__add_node(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertSetEqual(ana._nodes, set({}))

        ana._add_node(6)
        self.assertSetEqual(ana._nodes, {6})

        ana._add_node(10)
        self.assertSetEqual(ana._nodes, {6, 10})

    def test__add_edge(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_node(1)
        ana._add_node(2)

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test__add_edge_without_preadded_nodes(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test__add_edge_with_preadded_source_node(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._edges, {})

        ana._add_node(1)

        ana._add_edge(1, 2)
        self.assertDictEqual(ana._edges, {1: [2]})

    def test_init_from_storage_structure(self):
        self.storage_genome.inputs = {
            "input1": 1,
            "input2": 2,
            "input3": 3
        }
        self.storage_genome.outputs = {
            "output1": 4,
            "output2": 5,
            "output3": 6
        }
        self.storage_genome.genes = [
            (1, False, 0.5),
            (2, False, 0.5),
            (3, False, 0.5),
            (4, False, 0.5),
            (5, False, 0.5),
            (6, False, 0.5),
            (7, False, 0.5),
            (8, False, 0.5)
        ]
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)

        self.assertTrue(ana.initialised)
        self.assertDictEqual(
            {
                "input1": 1,
                "input2": 2,
                "input3": 3
            },
            ana.input_nodes)
        self.assertDictEqual(
            {
                "output1": 4,
                "output2": 5,
                "output3": 6
            },
            ana.output_nodes)
        self.assertDictEqual(
            {2 * node_id: [2 * node_id + 1]
             for (node_id, _, _) in self.storage_genome.genes},
            ana.edges
        )

    def test__add_input_node(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._input_nodes, {})

        ana._add_input_node(1, "A")
        self.assertDictEqual(ana._input_nodes, {"A": 1})

    def test__add_output_node(self):
        ana = AnalysisGenome.AnalysisGenome(
            self.mock_gene_repository,
            self.storage_genome)
        self.assertDictEqual(ana._output_nodes, {})

        ana._add_output_node(1, "A")
        self.assertDictEqual(ana._output_nodes, {"A": 1})
