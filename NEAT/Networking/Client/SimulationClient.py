from typing import Dict

from bson import ObjectId

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
    def __init__(self, server_address, server_port):
        self._client = NEATClient(server_address, server_port)

    def announce_session(self, session_id, config_path=None, block_size=1):
        command = AnnounceSessionCommand()
        command.set_block_size(block_size)
        command.set_config_path(config_path)
        command.set_session_id(session_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't announce session to server.")

    def get_block(self, block_id: int) -> Dict[ObjectId, Dict[str, float]]:
        command = GetBlockCommand()
        command.set_block_id(block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't get block.")
        return response.result["block"]

    def set_block_inputs(self, inputs: Dict[ObjectId, Dict[str, float]], block_id: int) -> SetInputsCommand:
        command = SetInputsCommand()
        command.set_inputs(inputs, block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't set block inputs.")

    def get_block_outputs(self, block_id: int) -> GetOutputsCommand:
        command = GetOutputsCommand()
        command.set_block_id(block_id)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't get block outputs.")
        return response.result["outputs"]

    def set_fitness_values(
            self,
            fitness_values: Dict[ObjectId, float],
            block_id: int
    ) -> SetFitnessValuesCommand:
        command = SetFitnessValuesCommand()
        command.set_block_id(block_id)
        command.set_fitness_values(fitness_values)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't set fitness values.")

    def advance_generation(self) -> AdvanceGenerationCommand:
        command = AdvanceGenerationCommand()
        command.set_advance_generation(True)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't advance generation.")

    def archive_session(self):
        command = AdvanceGenerationCommand()
        command.set_advance_generation(False)
        response = self._client.run_command(command)
        if not response.result["acknowledged"]:
            raise NetworkProtocolException("Couldn't archive session.")
