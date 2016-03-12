from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AnnounceConfigPathCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AnnounceConfigPath"
        self.parameters["config_path"] = None

    def set_config_path(self, config_path):
        self.parameters["config_path"] = config_path

    def get_config_path(self):
        return self.parameters["config_path"]
