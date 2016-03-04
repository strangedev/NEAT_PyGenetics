from unittest import TestCase
from NEAT.Config.NEATConfig import NEATConfig

class TestNEATConfig(TestCase):

    def test_load_config(self):

        config = NEATConfig()

        self.assertIsNotNone(config.parameters["breeding"])
        self.assertIsNotNone(config.parameters["clustering"])
        self.assertIsNotNone(config.parameters["decision_making"])
        self.assertIsNotNone(config.parameters["mutating"])
        self.assertIsNotNone(config.parameters["selection"])

    def test_load_defaults(self):

        config = NEATConfig()
        config.parameters.clear()
        config.load_defaults()

        self.assertIsNotNone(config.parameters["breeding"])
        self.assertIsNotNone(config.parameters["clustering"])
        self.assertIsNotNone(config.parameters["decision_making"])
        self.assertIsNotNone(config.parameters["mutating"])
        self.assertIsNotNone(config.parameters["selection"])

