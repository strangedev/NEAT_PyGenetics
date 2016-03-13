from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AnnounceSessionCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AnnounceSession"
        self.parameters["session_id"] = "default"
        self.parameters["block_size"] = 1
        self.parameters["config_path"] = None

    def set_config_path(self, config_path):
        self.parameters["config_path"] = config_path

    def get_config_path(self):
        return self.parameters["config_path"]

    def set_session_id(self, session_id):
        self.parameters["session_id"] = session_id

    def get_session_id(self):
        return self.parameters["session_id"]

    def set_block_size(self, block_size: int):
        self.parameters["block_size"] = block_size

    def get_block_size(self):
        return self.parameters["block_size"]

