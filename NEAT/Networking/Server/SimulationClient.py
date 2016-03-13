from NEAT.Networking.Server.NEATServer import NEATServer
from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
from bson import ObjectId
from typing import Dict

class SimulationClient(object):
    """
    A class providing a high-level interface to
    a client connected via the REST API.
    It provides information on the state of the client
    and relays information from the client to NEAT.

    """

    def __init__(self):
        self._server = NEATServer()
        self._session = None

    @property
    def session(self):
        return self._session

    def _listen_for_command(self, types, filter=None, timeout=2000):
        # TODO: timeouts, more error handling
        command = self._server.fetch()

        if not type(types) == type(list([])):
            types = [types]
        if not command._type in types:
            raise NetworkProtocolException("Wrong command type encountered")

        if filter:
            for key, value in filter.items():
                if not key in command.parameters.keys():
                    raise NetworkProtocolException("Filter key not in command parameters")
                if not value == command.parameters[key]:
                    raise  NetworkProtocolException("Filter values do not match in command parameters")

        return command

    def _respond_to_command(
            self,
            command: BaseCommand,
            result: dict=None,
            acknowledged=True,
            timeout=2000
    ):
        if not result:
            result = {
                "acknowledged": acknowledged
            }
        command.result = result
        self._server.respond(command)

    def wait_for_session(self):
        session_command = self._listen_for_command("AnnounceSession")
        self._session = session_command.parameters["session"]
        self._respond_to_command(session_command)

    def get_config_path(self):
        announce_command = self._listen_for_command("AnnounceConfigPath")
        self._respond_to_command(announce_command)
        return announce_command.parameters["config_path"]

    def get_block_size(self):
        announce_command = self._listen_for_command("AnnounceBlockSize")
        self._respond_to_command(announce_command)
        return announce_command.parameters["block_size"]

    def send_block(self, block, block_id):
        block_to_send = {
            genome._id:
                {
                    input_label: None
                    for input_label in genome.inputs.keys()
                }
            for genome in block
        }
        result = {
            "block": block_to_send,
            "block_id": block_id,
            "next_block_id": block_id + 1,
            "block_size": len(list(block_to_send.keys()))
        }

        get_command = self._listen_for_command("GetBlock", {"block_id": block_id})
        self._respond_to_command(
            get_command,
            result
        )

    def get_block_inputs(self, block_id) -> Dict[ObjectId, Dict[str, float]]:
        set_command = self._listen_for_command("SetInputs", {"block_id": block_id})
        self._respond_to_command(set_command)
        return set_command.parameters["block"]

    def send_block_outputs(self, outputs, block_id):
        get_command = self._listen_for_command("GetOutputs", {"block_id": block_id})
        get_command.result["outputs"] = outputs
        self._respond_to_command(get_command)

    def get_fitness_values(self, block_id):
        set_command = self._listen_for_command(
            "SetFitnessValues",
            {"block_id": block_id}
        )
        self._respond_to_command(set_command)
        return set_command.parameters["fitness_values"]

    def get_advance_generation(self):
        advance_command = self._listen_for_command(
            ["AdvanceGeneration", "ArchiveSession"]
        )
        self._respond_to_command(advance_command)
        return advance_command._type == "AdvanceGeneration"