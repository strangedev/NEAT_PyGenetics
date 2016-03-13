from NEAT.Networking.Commands.BaseCommand import BaseCommand
from bson import ObjectId
from typing import Dict

class SetInputsCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "SetInputs"
        self.parameters["block"] = None
        self.parameters["block_id"] = None

    def set_inputs(self, inputs: Dict[ObjectId, Dict[str, float]], block_id: int):
        self.parameters 