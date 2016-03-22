from NEAT.GenomeStructures.SimulationStructure.SimulationGenome import SimulationGenome
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.GeneRepository import GeneRepository
from typing import Dict
from fractions import Fraction
from bson import ObjectId


class Simulator(object):

    def __init__(self, gene_repository: GeneRepository):
        self._gene_repository = gene_repository

    def simulate_genome(
            self,
            storage_genome: StorageGenome,
            inputs: Dict[str, float]
    ) -> Dict[str, float]:
        simulation_genome = SimulationGenome(
            self._gene_repository,
            storage_genome
        )
        inputs = {k: Fraction(v) for k, v in inputs.items()} #  TODO: use fractions all the way
        return simulation_genome.calculate_step(inputs)
