from collections import defaultdict
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

        analysis_genome._add_edge(1, 9, 1)
        analysis_genome._add_edge(1, 10, 2)
        analysis_genome._add_edge(2, 10, 3)
        analysis_genome._add_edge(2, 11, 4)
        analysis_genome._add_edge(3, 10, 5)
        analysis_genome._add_edge(3, 11, 6)
        analysis_genome._add_edge(3, 12, 7)
        analysis_genome._add_edge(4, 12, 8)
        analysis_genome._add_edge(9, 14, 9)
        analysis_genome._add_edge(9, 15, 10)
        analysis_genome._add_edge(10, 15, 11)
        analysis_genome._add_edge(11, 15, 12)
        analysis_genome._add_edge(11, 16, 13)
        analysis_genome._add_edge(12, 13, 14)
        analysis_genome._add_edge(12, 17, 15)
        analysis_genome._add_edge(13, 18, 16)
        analysis_genome._add_edge(14, 21, 17)
        analysis_genome._add_edge(15, 22, 18)
        analysis_genome._add_edge(16, 19, 19)
        analysis_genome._add_edge(17, 19, 20)
        analysis_genome._add_edge(17, 20, 21)
        analysis_genome._add_edge(18, 17, 22)
        analysis_genome._add_edge(18, 20, 23)
        analysis_genome._add_edge(19, 23, 24)
        analysis_genome._add_edge(19, 24, 25)
        analysis_genome._add_edge(20, 8, 26)
        analysis_genome._add_edge(20, 24, 27)
        analysis_genome._add_edge(21, 5, 28)
        analysis_genome._add_edge(21, 6, 29)
        analysis_genome._add_edge(21, 9, 30)
        analysis_genome._add_edge(22, 6, 31)
        analysis_genome._add_edge(22, 15, 32)
        analysis_genome._add_edge(22, 21, 33)
        analysis_genome._add_edge(23, 7, 34)
        analysis_genome._add_edge(23, 11, 35)
        analysis_genome._add_edge(23, 18, 36)
        analysis_genome._add_edge(24, 7, 37)
        analysis_genome._add_edge(24, 17, 38)

        analysis_genome._graph_initialized = True

        topologically_sorted_nodes = [4, 3, 12, 13, 2, 11, 16, 19, 23, 18, 17,
                                      20, 24, 8, 7, 1, 10, 9, 15, 22, 14, 21,
                                      6, 5]
        topologically_sorted_cycle_nodes = [24, 23, 22, 21, 17]

        gene_closes_cycle_map = defaultdict(bool)
        gene_closes_cycle_map[20] = True
        gene_closes_cycle_map[30] = True
        gene_closes_cycle_map[32] = True
        gene_closes_cycle_map[35] = True
        gene_closes_cycle_map[38] = True
    
        result = analyst.analyze(analysis_genome)

        self.assertDictEqual(gene_closes_cycle_map, result.gene_closes_cycle_map)
        self.assertListEqual(topologically_sorted_nodes,
                             result.topologically_sorted_nodes)
        self.assertListEqual(topologically_sorted_cycle_nodes,
                             result.topologically_sorted_cycle_nodes)
