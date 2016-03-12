from NEAT.Networking.Commands.BaseCommand import BaseCommand
from typing import Dict
from bson import ObjectId

class GetBlockCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "GetBlock"
        self.parameters["block_id"] = 0

    def set_block_id(self, block_id: int):
        self.parameters["block_id"] = block_id

    def get_block_id(self):
        return self.parameters["block_id"]

    def get_block(self) -> Dict[ObjectId, Dict[str, float]]:
        return self._get_result_if_exists("block")

    def get_block_size(self) -> int:
        return self._get_result_if_exists("block_size")

    def get_resulting_block_id(self) -> int:
        return self._get_result_if_exists("block_id")

    def get_next_block_id(self) -> int:
        return self._get_result_if_exists("next_block_id")