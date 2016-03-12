from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AdvanceGenerationCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AdvanceGeneration"
