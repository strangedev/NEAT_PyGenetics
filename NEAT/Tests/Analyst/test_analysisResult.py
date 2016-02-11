from unittest import TestCase
from NEAT.Analyst import AnalysisResult


class TestAnalysisResult(TestCase):

    def test_clear(self):

        result = AnalysisResult.AnalysisResult()

        result.nodes = {"A", "B", "C"}
        result.edges = {"A": ["B"]}
        result.cycle_nodes = {"C"}
        result.cycle_edges = {"C": ["A"]}

        result.clear()

        self.assertSetEqual(result.nodes, set({}))
        self.assertSetEqual(result.cycle_nodes, set({}))
        self.assertDictEqual(result.edges, {})
        self.assertDictEqual(result.cycle_edges, {})