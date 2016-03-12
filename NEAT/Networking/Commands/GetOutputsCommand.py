from NEAT.Networking.Commands.BaseCommand import BaseCommand

class GetOutputsCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "GetOutputs"