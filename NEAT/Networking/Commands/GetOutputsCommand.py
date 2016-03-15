from NEAT.Networking.Commands.BaseCommand import BaseCommand

class GetOutputsCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "GetOutputs"
        self.parameters["block_id"] = 1

    def set_block_id(self, block_id: int):
        self.parameters["block_id"] = block_id

    def get_block_id(self):
        return self.parameters["block_id"]

