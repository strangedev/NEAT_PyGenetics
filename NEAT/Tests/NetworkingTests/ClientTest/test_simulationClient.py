import unittest
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec

from bson import ObjectId

from NEAT.Networking.Client.SimulationClient import SimulationClient
from NEAT.Networking.Commands import BaseCommand
from NEAT.Networking.Commands.AdvanceGenerationCommand import AdvanceGenerationCommand
from NEAT.Networking.Commands.AnnounceSessionCommand import AnnounceSessionCommand
from NEAT.Networking.Commands.GetBlockCommand import GetBlockCommand
from NEAT.Networking.Commands.GetOutputsCommand import GetOutputsCommand
from NEAT.Networking.Commands.SetFitnessValuesCommand import SetFitnessValuesCommand
from NEAT.Networking.Commands.SetInputsCommand import SetInputsCommand


def acknowledged_command(c: BaseCommand):     # TODO ...
    c.as_dict()
    c.result.__setitem__("acknowledged", True)
    c.result.__setitem__("block", {1: {"test": 1.8}})
    c.result.__setitem__("outputs", None)  # TODO: Type?
    return c


class TestSimulationClient(TestCase):
    def setUp(self):
        self.simulation_client = SimulationClient(None, None)
        self.mock_client = MagicMock()
        self.mock_client.run_command = create_autospec(acknowledged_command)
        self.simulation_client._client = self.mock_client

    @unittest.expectedFailure
    def test_announce_session_fail(self):
        self.mock_client.run_command = lambda x: x
        self.simulation_client.announce_session(2)

    def test_announce_session(self):
        self.assertIsNone(self.simulation_client.announce_session(2))

    @unittest.expectedFailure
    def test_get_block_fail(self):
        self.mock_client.run_command = lambda x: x
        command = GetBlockCommand()
        self.simulation_client.get_block(2)

    def test_get_block(self):
        command = acknowledged_command(GetBlockCommand())
        self.mock_client.run_command = create_autospec(acknowledged_command, return_value=command)
        self.assertDictEqual({1: {"test": 1.8}}, self.simulation_client.get_block(2))

    @unittest.expectedFailure
    def test_set_block_inputs_fail(self):
        id = ObjectId()
        dictionary = {id: {"test": 1.5}}
        block_id = 2
        self.mock_client.run_command = lambda x: x
        self.simulation_client.set_block_inputs(dictionary, block_id)

    def test_set_block_inputs(self):
        id = ObjectId()
        dictionary = {id: {"test": 1.5}}
        block_id = 2
        command = SetInputsCommand()
        command.set_inputs(dictionary, block_id)
        self.assertIsNone(self.simulation_client.set_block_inputs(dictionary, block_id))

    @unittest.expectedFailure
    def test_get_block_outputs_fail(self):
        self.mock_client.run_command = lambda x: x
        self.simulation_client.get_block_outputs(2)


    def test_get_block_outputs(self):
        command = acknowledged_command(GetOutputsCommand())
        self.mock_client.run_command = create_autospec(acknowledged_command, return_value=command)
        self.assertIsNone(
            self.simulation_client.get_block_outputs(2)
        )  # TODO: return value dict(ObjectId, dict(str, float)

    @unittest.expectedFailure
    def test_set_fitness_values_fail(self):
        self.mock_client.run_command = lambda x: x
        command = SetFitnessValuesCommand()
        self.simulation_client.set_fitness_values(command)

    def test_set_fitness_values(self):
        self.assertIsNone(self.simulation_client.set_fitness_values({1: 1.78}))

    @unittest.expectedFailure
    def test_advance_generation_fail(self):
        self.mock_client.run_command = lambda x: x
        self.simulation_client.advance_generation()

    def test_advance_generation(self):
        command = AdvanceGenerationCommand()
        self.assertIsNone(self.simulation_client.advance_generation())
