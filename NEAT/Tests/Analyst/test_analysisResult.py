from unittest import TestCase
from NEAT.Analyst.AnalysisResult import AnalysisResult


class TestAnalysisResult(TestCase):

    def test_equality_operator(self):
        result = AnalysisResult()
        new_result = AnalysisResult()

        result.disabled_nodes = {100, 2}
        result.edges = {36: [2]}
        result.topologically_sorted_nodes = [3, 2]
        result.cycle_edges = {1: [7]}
        result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertFalse(result.__eq__(new_result))

        new_result.disabled_nodes = {100, 2}
        new_result.edges = {36: [2]}
        new_result.topologically_sorted_nodes = [3, 2]
        new_result.cycle_edges = {1: [7]}
        new_result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertTrue(result.__eq__(new_result))

    def test_clear(self):
        result = AnalysisResult()

        result.disabled_nodes = {1, 2}
        result.edges = {1: [2]}
        result.topologically_sorted_nodes = [1, 2]
        result.cycle_edges = {1: [2]}
        result.topologically_sorted_cycle_nodes = [1, 2]

        result.clear()

        new_result = AnalysisResult()
        self.assertTrue(result.__eq__(new_result))

    def test_cycle_nodes(self):
        result = AnalysisResult()

        result.cycle_edges = {1: [2, 3, 4], 2: [3]}
        self.assertSetEqual({1, 2}, result.cycle_nodes)
