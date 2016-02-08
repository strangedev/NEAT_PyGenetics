from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome

from unittest import TestCase


class TestAnalysisGenome(TestCase):

    def test_init_from_storage_structure(self):
        self.fail()

    def test_init_from_simulation_structure(self):
        self.fail()

    def test_get_dag_nodes(self):

        analysis_genome = AnalysisGenome.AnalysisGenome()

        analysis_genome.__add_edge("A_i", "B", 1)
        analysis_genome.__add_edge("C_i", "B", 1)
        analysis_genome.__add_edge("D_i", "E", 1)
        analysis_genome.__add_edge("E", "B", 1)
        analysis_genome.__add_edge("B", "F", 1)
        analysis_genome.__add_edge("F", "E", 1)
        analysis_genome.__add_edge("F", "G_o", 1)

        analysis_genome.analyse()

        self.fail()

    def test_get_predecessors(self):
        self.fail()

    def test_get_cycle_nodes(self):
        self.fail()
