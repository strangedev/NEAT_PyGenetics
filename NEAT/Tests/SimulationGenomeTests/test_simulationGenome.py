from typing import Dict, List
from fractions import Fraction
import unittest
from unittest.mock import MagicMock

from NEAT.Analyst.AnalysisResult import AnalysisResult
from NEAT.GenomeStructures.SimulationStructure.SimulationGenome \
    import SimulationGenome
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class TestSimulationGenome(unittest.TestCase):
    def test_basicExampleWithoutCycles(self):
        genes = {
            1: (1, 6),
            2: (2, 6),
            3: (1, 7),
            4: (3, 7),
            5: (6, 4),
            6: (7, 4),
            7: (2, 5),
            8: (7, 5),
        }

        storage_genome = StorageGenome()
        analysis_result = AnalysisResult()

        storage_genome.inputs['input_1'] = 1
        storage_genome.inputs['input_2'] = 2
        storage_genome.inputs['input_3'] = 3
        storage_genome.outputs['output_1'] = 4
        storage_genome.outputs['output_2'] = 5
        storage_genome.genes[1] = (False, Fraction(2, 10))
        storage_genome.genes[2] = (False, Fraction(7, 10))
        storage_genome.genes[3] = (False, Fraction(1, 10))
        storage_genome.genes[4] = (False, Fraction(3, 10))
        storage_genome.genes[5] = (False, Fraction(6, 10))
        storage_genome.genes[6] = (False, Fraction(8, 10))
        storage_genome.genes[7] = (False, Fraction(9, 10))
        storage_genome.genes[8] = (False, Fraction(5, 10))

        analysis_result.topologically_sorted_nodes = [3, 2, 1, 7, 5, 6, 4]
        analysis_result.topologically_sorted_cycle_nodes = []

        storage_genome.analysis_result = analysis_result

        mock_gene_repository = MagicMock()
        mock_gene_repository.get_node_labels_by_gene_id =\
            lambda node_id: genes[node_id]

        gen = SimulationGenome(
            mock_gene_repository,
            storage_genome
        )

        result = gen.calculate_step([
            ('input_1', Fraction(5, 10)),
            ('input_2', Fraction(5, 10)),
            ('input_3', Fraction(5, 10))
        ])  # type: Dict[str, float]

        self.assertEqual(Fraction(43, 100), result['output_1'])
        self.assertEqual(Fraction(55, 100), result['output_2'])

    def test_basicExampleWithCycles(self):
        genes = {
            1: (1, 5),
            2: (2, 5),
            3: (1, 6),
            4: (5, 6),
            5: (6, 7),
            6: (7, 5),
            7: (6, 3),
            8: (7, 4),
        }

        storage_genome = StorageGenome()
        analysis_result = AnalysisResult()

        storage_genome.inputs['input_1'] = 1
        storage_genome.inputs['input_2'] = 2
        storage_genome.outputs['output_1'] = 3
        storage_genome.outputs['output_2'] = 4
        storage_genome.genes[1] = (False, Fraction(7, 10))
        storage_genome.genes[2] = (False, Fraction(3, 10))
        storage_genome.genes[3] = (False, Fraction(6, 10))
        storage_genome.genes[4] = (False, Fraction(4, 10))
        storage_genome.genes[5] = (False, Fraction(3, 10))
        storage_genome.genes[6] = (False, Fraction(6, 10))
        storage_genome.genes[7] = (False, Fraction(7, 10))
        storage_genome.genes[8] = (False, Fraction(5, 10))

        analysis_result.topologically_sorted_nodes = [2, 1, 5, 6, 7, 4, 3]
        analysis_result.topologically_sorted_cycle_nodes = [7]
        analysis_result.gene_closes_cycle_map[6] = True

        storage_genome.analysis_result = analysis_result

        mock_gene_repository = MagicMock()
        mock_gene_repository.get_node_labels_by_gene_id =\
            lambda node_id: genes[node_id]

        gen = SimulationGenome(
            mock_gene_repository,
            storage_genome
        )

        result = gen.calculate_step([
            ('input_1', Fraction(5, 10)),
            ('input_2', Fraction(5, 10))
        ])

        self.assertEqual(Fraction(7, 20), result['output_1'])
        self.assertEqual(Fraction(3, 40), result['output_2'])
