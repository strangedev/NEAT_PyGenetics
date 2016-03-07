from unittest import TestCase
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome
from NEAT.Analyst import GenomeAnalyst


class TestGenomeAnalyst(TestCase):
    def test_analysisByExample(self):
        analyst = GenomeAnalyst.GenomeAnalyst()
        analysis_genome = AnalysisGenome.AnalysisGenome(None, None)

        analysis_genome._add_input_node(1, "input1")
        analysis_genome._add_input_node(2, "input2")
        analysis_genome._add_input_node(3, "input3")
        analysis_genome._add_input_node(4, "input4")

        analysis_genome._add_output_node(5, "output1")
        analysis_genome._add_output_node(6, "output2")
        analysis_genome._add_output_node(7, "output3")
        analysis_genome._add_output_node(8, "output4")

        analysis_genome._add_edge(1, 9)
        analysis_genome._add_edge(1, 10)
        analysis_genome._add_edge(2, 10)
        analysis_genome._add_edge(2, 11)
        analysis_genome._add_edge(3, 10)
        analysis_genome._add_edge(3, 11)
        analysis_genome._add_edge(3, 12)
        analysis_genome._add_edge(4, 12)
        analysis_genome._add_edge(9, 14)
        analysis_genome._add_edge(9, 15)
        analysis_genome._add_edge(10, 15)
        analysis_genome._add_edge(11, 15)
        analysis_genome._add_edge(11, 16)
        analysis_genome._add_edge(12, 13)
        analysis_genome._add_edge(12, 17)
        analysis_genome._add_edge(13, 18)
        analysis_genome._add_edge(14, 21)
        analysis_genome._add_edge(15, 22)
        analysis_genome._add_edge(16, 19)
        analysis_genome._add_edge(17, 19)
        analysis_genome._add_edge(17, 20)
        analysis_genome._add_edge(18, 17)
        analysis_genome._add_edge(18, 20)
        analysis_genome._add_edge(19, 23)
        analysis_genome._add_edge(19, 24)
        analysis_genome._add_edge(20, 8)
        analysis_genome._add_edge(20, 24)
        analysis_genome._add_edge(21, 5)
        analysis_genome._add_edge(21, 6)
        analysis_genome._add_edge(21, 9)
        analysis_genome._add_edge(22, 6)
        analysis_genome._add_edge(22, 15)
        analysis_genome._add_edge(22, 21)
        analysis_genome._add_edge(23, 7)
        analysis_genome._add_edge(23, 11)
        analysis_genome._add_edge(23, 18)
        analysis_genome._add_edge(24, 7)
        analysis_genome._add_edge(24, 17)

        analysis_genome._graph_initialized = True

        topologically_sorted_nodes = [4, 3, 12, 13, 2, 11, 16, 19, 23, 18, 17,
                                      20, 24, 1, 10, 9, 15, 22, 14, 21]
        topologically_sorted_cycle_nodes = [24, 23, 22, 21, 17]
        cycle_edges = {
            17: [19],
            21: [9],
            22: [15],
            23: [11],
            24: [17]
        }
        edges = {
            1: [9, 10],
            2: [10, 11],
            3: [10, 11, 12],
            4: [12],
            9: [14, 15],
            10: [15],
            11: [15, 16],
            12: [13, 17],
            13: [18],
            14: [21],
            15: [22],
            16: [19],
            17: [20],
            18: [17, 20],
            19: [23, 24],
            20: [8, 24],
            21: [5, 6],
            22: [6, 21],
            23: [7, 18],
            24: [7]
        }

        result = analyst.analyze(analysis_genome)

        self.assertListEqual(topologically_sorted_nodes,
                             result.topologically_sorted_nodes)
        self.assertDictEqual(edges, result.geneClosesCycleMap)
        self.assertListEqual(topologically_sorted_cycle_nodes,
                             result.topologically_sorted_cycle_nodes)
        self.assertDictEqual(cycle_edges, result.cycle_edges)
