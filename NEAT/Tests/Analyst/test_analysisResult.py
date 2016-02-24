from unittest import TestCase
from NEAT.Analyst.AnalysisResult import AnalysisResult


class TestAnalysisResult(TestCase):

    def test_clear(self):
        result = AnalysisResult()

        result.disabled_nodes = {1, 2}
        result.edges = {1: [2]}
        result.topologically_sorted_nodes = [1, 2]
        result.cycle_edges = {1: [2]}
        result.topologically_sorted_cycle_nodes = [1, 2]

        result.clear()

        self.assertSetEqual(set({}), result.disabled_nodes)
        self.assertDictEqual({}, result.edges)
        self.assertListEqual([], result.topologically_sorted_nodes)
        self.assertDictEqual({}, result.cycle_edges)
        self.assertListEqual([], result.topologically_sorted_cycle_nodes)

    def test_cycle_nodes(self):
        result = AnalysisResult()

        result.cycle_edges = {1: [2, 3, 4], 2: [3]}
        self.assertSetEqual({1, 2}, result.cycle_nodes)
