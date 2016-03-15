from NEAT.Networking.Commands.BaseCommand import BaseCommand
from typing import Dict
from bson import ObjectId

class SetFitnessValuesCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "SetFitnessValues"
        self.parameters["fitness_values"] = dict({})

    def set_fitness_values(
            self,
            fitness_values: Dict[ObjectId, float]
    ):
        self.parameters["fitness_values"] = fitness_values

    def set_fitness_value(
            self,
            genome_id: ObjectId,
            fitness_value: float
    ):
        self.parameters["fitness_values"][genome_id] = fitness_value