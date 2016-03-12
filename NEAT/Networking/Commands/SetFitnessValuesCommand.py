from NEAT.Networking.Commands.BaseCommand import BaseCommand

class SetFitnessValuesCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "SetFitnessValues"