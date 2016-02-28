from unittest import TestCase
from NEAT.Config.NEATConfig import NEATConfig

class TestNEATConfig(TestCase):

    def test_load_config(self):

        config = NEATConfig()

        self.assertIsNotNone(config.clustering_parameters)
        self.assertIsNotNone(config.selection_parameters)
        self.assertIsNotNone(config.decision_making_parameters)
        self.assertIsNotNone(config.discarding_parameters)

    def test_load_defaults(self):
        self.fail()
