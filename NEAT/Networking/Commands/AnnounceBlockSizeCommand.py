from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AnnounceBlockSizeCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AnnounceBlockSize"
        self.parameters["block_size"] = 1

    def set_block_size(self, block_size: int):
        self.parameters["block_size"] = block_size

    def get_block_size(self):
        return self.parameters["block_size"]
