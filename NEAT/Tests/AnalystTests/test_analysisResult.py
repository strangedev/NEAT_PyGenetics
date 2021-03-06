from unittest import TestCase
from NEAT.Analyst.AnalysisResult import AnalysisResult


class TestAnalysisResult(TestCase):

    def test_equality_operator(self):
        result = AnalysisResult()
        new_result = AnalysisResult()

        result.gene_closes_cycle_map = {36: False, 1: True}
        result.topologically_sorted_nodes = [3, 2]
        result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertFalse(result.__eq__(new_result))

        new_result.gene_closes_cycle_map = {36: False, 1: True}
        new_result.topologically_sorted_nodes = [3, 2]
        new_result.topologically_sorted_cycle_nodes = [4, 2]

        self.assertTrue(result.__eq__(new_result))

    def test_clear(self):
        result = AnalysisResult()

        result.gene_closes_cycle_map = {1: False, 2: True}
        result.topologically_sorted_nodes = [1, 2]
        result.topologically_sorted_cycle_nodes = [1, 2]

        result.clear()

        new_result = AnalysisResult()
        self.assertTrue(result.__eq__(new_result))

    def test_cycle_nodes(self):
        result = AnalysisResult()

        result.topologically_sorted_cycle_nodes = [1, 2]
        self.assertSetEqual({1, 2}, result.cycle_nodes)

    def test_copyConstructor(self):
        ana1 = AnalysisResult()
        ana1.gene_closes_cycle_map[5] = True
        ana1.topologically_sorted_nodes = [1, 8, 3, 4, 6, 7]
        ana1.topologically_sorted_cycle_nodes = [6, 2, 4]
        ana2 = AnalysisResult(ana1)

        self.assertEqual(ana1, ana2)
        self.assertNotEqual(ana1.__repr__(), ana2.__repr__())
