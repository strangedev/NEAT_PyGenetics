from typing import Dict

from bson import ObjectId

from NEAT.Config.StaticConfig.ServerConfig import server_address, server_port  # TODO:
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
from NEAT.Networking.Client.NEATClient import NEATClient
from NEAT.Networking.Commands.AdvanceGenerationCommand import AdvanceGenerationCommand
from NEAT.Networking.Commands.AnnounceSessionCommand import AnnounceSessionCommand
from NEAT.Networking.Commands.GetBlockCommand import GetBlockCommand
from NEAT.Networking.Commands.GetOutputsCommand import GetOutputsCommand
from NEAT.Networking.Commands.SetFitnessValuesCommand import SetFitnessValuesCommand
from NEAT.Networking.Commands.SetInputsCommand import SetInputsCommand


class SimulationClient(object):
    # TODO: Error Handling! on every response
    def __init__(self):
        self._client = NEATClient(server_address, server_port)

    def announce_session(self, session_id, config_path=None, block_size=1):
        command = AnnounceSessionCommand()
        command.set_block_size(block_size)
        command.set_config_path(config_path)
        command.set_session_id(session_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException

    def get_block(self, block_id: int) -> Dict[ObjectId, Dict[str, float]]:
        command = GetBlockCommand()
        command.set_block_id(block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException
        return response.result["block"]

    def set_block_inputs(self, inputs: Dict[ObjectId, Dict[str, float]], block_id: int) -> SetInputsCommand:
        command = SetInputsCommand()
        command.set_inputs(inputs, block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException

    def get_block_outputs(self, block_id: int) -> GetBlockCommand:
        command = GetOutputsCommand()
        command.set_block_id(block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException
        return response.result["outputs"]

    def set_fitness_values(
            self,
            fitness_values: Dict[ObjectId, float]
    ) -> SetFitnessValuesCommand:
        command = SetFitnessValuesCommand()
        command.set_fitness_values(fitness_values)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException

    def advance_generation(self) -> AdvanceGenerationCommand:
        command = AdvanceGenerationCommand()
        command.set_advance_generation(True)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException

    def archive_session(self):
        command = AdvanceGenerationCommand()
        command.set_advance_generation(False)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException
