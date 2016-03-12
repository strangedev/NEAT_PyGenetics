from NEAT.Networking.Commands.BaseCommand import BaseCommand

class AnnounceSessionCommand(BaseCommand):

    def __init__(self):
        super().__init__()
        self._type = "AnnounceSession"
        self.parameters["session"] = dict({})

    def set_session_id(self, session_id):
        self.parameters["session"]["session_id"] = session_id

    def get_session_id(self):
        return self.parameters["session"]["session_id"]
