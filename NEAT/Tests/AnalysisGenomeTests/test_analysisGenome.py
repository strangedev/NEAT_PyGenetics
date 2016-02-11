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

    def test__add_cycle_node(self):

        ana = AnalysisGenome.AnalysisGenome()
        self.assertSetEqual(ana._cycle_nodes, set({}))

        ana._add_cycle_node("A")
        self.assertSetEqual(ana._cycle_nodes, {"A"})

        ana._add_cycle_node("A")
        self.assertSetEqual(ana._cycle_nodes, {"A"})

    def test__add_cycle_edge(self):

        ana = AnalysisGenome.AnalysisGenome()
        self.assertDictEqual(ana._cycle_edges, {})

        ana._add_cycle_node("A")
        ana._add_cycle_node("B")

        ana._add_cycle_edge("A", "B")
        self.assertDictEqual(ana._cycle_edges, {"A": ["B"]})

    def test_init_from_storage_structure(self):
        self.fail()

    def test_analyse(self):
        self.fail()

    def test__reset_analysis(self):
        self.fail()

    def test__set_working_graph(self):
        self.fail()

    def test__dfs(self):
        self.fail()

    def test__dfs_visit(self):
        self.fail()

    def test_result(self):
        self.fail()
