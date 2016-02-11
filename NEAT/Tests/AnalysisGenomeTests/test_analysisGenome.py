from unittest import TestCase
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome


class TestAnalysisGenome(TestCase):

    def test__add_node(self):

        ana = AnalysisGenome.AnalysisGenome()
        self.assertSetEqual(ana._nodes, set({}))

        ana._add_node("A")
        self.assertSetEqual(ana._nodes, {"A"})

        ana._add_node("A")
        self.assertSetEqual(ana._nodes, {"A"})

    def test__add_edge(self):

        ana = AnalysisGenome.AnalysisGenome()
        self.assertDictEqual(ana._edges, {})

        ana._add_node("A")
        ana._add_node("B")

        ana._add_edge("A", "B")
        self.assertDictEqual(ana._edges, {"A": ["B"]})

    def test_init_from_storage_structure(self):
        self.fail()
