from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AdvanceGenerationCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AdvanceGeneration"
        self.parameters["advance_generation"] = True

    def set_advance_generation(self, advance_generation: bool):
        self.parameters["advance_generation"] = advance_generation