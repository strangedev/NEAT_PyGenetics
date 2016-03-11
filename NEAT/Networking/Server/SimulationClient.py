from NEAT.Networking.Server.NEATServer import NEATServer
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
import time


class SimulationClient(object):
    """
    A class providing a high-level interface to
    a client connected via the REST API.
    It provides information on the state of the client
    and relays information from the client to NEAT.

    """

    @staticmethod
    def millis():
        return int(round(time.time() * 1000))

    def __init__(self):
        self._server = NEATServer()
        self._session = None

    @property
    def session(self):
        return self._session

    def _listen_for_command(self, type, timeout=2000):
        while True:  # TODO: timeouts, more error handling
            command = self._server.fetch()
            if not command._type == type:
                raise NetworkProtocolException()
            return command

    def wait_for_session(self):
        self._session = self._listen_for_command("AnnounceSession").session

    def get_config_path(self):
        return self._listen_for_command("AnnounceConfigPath").config_path

    def get_block_size(self):
        return self._listen_for_command("AnnounceBlockSize").block_size

    def send_block(self, block, block_id):
        block_to_send = {genome._id: {
            input_label: None
            for input_label in genome.inputs.keys()
            }
                         for genome in block}

    def get_fitness_values(self, block_id):
        pass