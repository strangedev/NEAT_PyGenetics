from NEAT.Networking.Client.NEATClient import NEATClient
from NEAT.Config.StaticConfig.ServerConfig import server_address, server_port # TODO:
from NEAT.Networking.Commands.AnnounceSessionCommand import AnnounceSessionCommand

class SimulationClient(object):

    def __init__(self):
        self._client = NEATClient(server_address, server_port)

    def announce_session(self, session_id, config_path=None, block_size=1):
        command = AnnounceSessionCommand()
        command.set_block_size(block_size)
        command.set_config_path(config_path)
        command.set_session_id(session_id)
        response = self._client.run_command(command)
        return response # TODO: Error Handling