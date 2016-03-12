from unittest import TestCase

from NEAT.Networking.Commands.BaseCommand import BaseCommand


class TestBaseCommand(TestCase):
    def setUp(self):
        self.base_command = BaseCommand()
        self.dictionary = self.base_command.__dict__

    def test_from_dict(self):
        self.assertDictEqual(self.dictionary, self.base_command.__dict__)
        self.base_command.from_dict({"test": "test"})
        self.assertDictEqual({"test": "test"}, self.base_command.__dict__)

    def test_as_dict(self):
        self.assertDictEqual(self.dictionary, self.base_command.as_dict())
