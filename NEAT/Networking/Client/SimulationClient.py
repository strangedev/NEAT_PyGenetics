from typing import Dict

from bson import ObjectId

from NEAT.Networking.Client.NEATClient import NEATClient
from NEAT.Config.StaticConfig.ServerConfig import server_address, server_port # TODO:
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
        return response

    def get_block(self, block_id: int) -> GetBlockCommand:
        command = GetBlockCommand()
        command.set_block_id(block_id)
        response = self._client.run_command(command)
        return response

    def set_block_inputs(self, inputs: Dict[ObjectId, Dict[str, float]], block_id: int) -> SetInputsCommand:
        command = SetInputsCommand()
        command.set_inputs(inputs, block_id)
        response = self._client.run_command(command)
        return response

    def get_block_outputs(self) -> GetBlockCommand:
        command = GetOutputsCommand()
        # TODO: Waiting for GetOutputCommand implementation
        response = self._client.run_command(command)
        return response

    def set_fitness_values(self) -> SetFitnessValuesCommand:
        command = SetFitnessValuesCommand()
        # TODO: Waiting for implementation of SetFitnessValues
        response = self._client.run_command(command)
        return response

    def advance_generation(self) -> AdvanceGenerationCommand:
        command = AdvanceGenerationCommand()
        # TODO: Waiting for Implementation of AdvanceGenerationCommand
        response = self._client.run_command(command)
        return response
