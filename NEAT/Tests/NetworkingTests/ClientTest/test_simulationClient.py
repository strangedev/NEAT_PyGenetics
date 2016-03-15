from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId

from NEAT.Networking.Client.SimulationClient import SimulationClient
from NEAT.Networking.Commands.AdvanceGenerationCommand import AdvanceGenerationCommand
from NEAT.Networking.Commands.AnnounceSessionCommand import AnnounceSessionCommand
from NEAT.Networking.Commands.GetBlockCommand import GetBlockCommand
from NEAT.Networking.Commands.GetOutputsCommand import GetOutputsCommand
from NEAT.Networking.Commands.SetFitnessValuesCommand import SetFitnessValuesCommand
from NEAT.Networking.Commands.SetInputsCommand import SetInputsCommand


class TestSimulationClient(TestCase):
    def setUp(self):
        self.simulation_client = SimulationClient()
        self.mock_client = MagicMock()
        self.simulation_client._client = self.mock_client
        self.mock_client.run_command = lambda x: x

    def test_announce_session(self):
        command = AnnounceSessionCommand()
        command.set_block_size(1)
        command.set_config_path(None)
        command.set_session_id(2)
        self.assertEqual(command, self.simulation_client.announce_session(2))

    def test_get_block_id(self):
        command = GetBlockCommand()
        command.set_block_id(2)
        self.assertEqual(command, self.simulation_client.get_block(2))

    def test_set_block_inputs(self):
        id = ObjectId()
        dictionary = {id: {"test": 1.5}}
        block_id = 2
        command = SetInputsCommand()
        command.set_inputs(dictionary, block_id)
        self.assertEqual(command, self.simulation_client.set_block_inputs(dictionary, block_id))

    def test_get_block_outputs(self):
        command = GetOutputsCommand()
        self.assertEqual(command, self.simulation_client.get_block_outputs())

    def test_set_fitness_values(self):
        command = SetFitnessValuesCommand()
        self.assertEqual(command, self.simulation_client.set_fitness_values())

    def test_advance_generation(self):
        command = AdvanceGenerationCommand()
        self.assertEqual(command, self.simulation_client.advance_generation())
