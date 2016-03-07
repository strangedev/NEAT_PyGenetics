from unittest import TestCase
from NEAT.Analyst.AnalysisResult import AnalysisResult


class TestAnalysisResult(TestCase):

    def test_equality_operator(self):
        result = AnalysisResult()
        new_result = AnalysisResult()

        result.genomeDisabledMap = {36: False, 1: True}
        result.topologically_sorted_nodes = [3, 2]
        result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertFalse(result.__eq__(new_result))

        new_result.genomeDisabledMap = {36: False, 1: True}
        new_result.topologically_sorted_nodes = [3, 2]
        new_result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertTrue(result.__eq__(new_result))

    def test_clear(self):
        result = AnalysisResult()

        result.genomeDisabledMap = {1: False, 2: True}
        result.topologically_sorted_nodes = [1, 2]
        result.topologically_sorted_cycle_nodes = [1, 2]

        result.clear()

        new_result = AnalysisResult()
        self.assertTrue(result.__eq__(new_result))

    def test_cycle_nodes(self):
        result = AnalysisResult()

        result.topologically_sorted_cycle_nodes = [1, 2]
        self.assertSetEqual({1, 2}, result.cycle_nodes)
