from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AnnounceBlockSizeCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AnnounceBlockSize"