from unittest import TestCase

from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder


class TestCommandTranscoder(TestCase):
    def setUp(self):
        self.base_command = BaseCommand()
        self.command_transcoder = CommandTranscoder()

    def test_encode_command(self):
        self.assertDictEqual(self.base_command.as_dict(), self.command_transcoder.encode_command(self.base_command))

    def test_decode_command(self):
        dictionary = self.base_command.__dict__
        self.assertEqual(self.base_command, self.command_transcoder.decode_command(dictionary))
