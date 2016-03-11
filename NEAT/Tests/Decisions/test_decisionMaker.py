from unittest import TestCase

from NEAT.Decisions.DecisionMaker import DecisionMaker


class TestDecisionMaker(TestCase):
    def setUp(self):
        self.selection_parameter = {}
        self.decision_maker = DecisionMaker(self.selection_parameter)

    def test_advance_time(self):
        self.assertEqual(0, self.decision_maker._time)
        self.decision_maker.advance_time()
        self.assertEqual(1, self.decision_maker._time)

    def test_reset_time(self):
        self.decision_maker._time = 33
        self.assertEqual(33, self.decision_maker._time)
        self.decision_maker.reset_time()
        self.assertEqual(0, self.decision_maker._time)

    def test_mutation_percentage(self):
        self.fail()

    def test_inter_cluster_breeding_time(self):
        self.selection_parameter.__setitem__('inter_cluster_breeding_interval', 2)
        self.assertTrue(self.decision_maker.inter_cluster_breeding_time)
        self.decision_maker._time = 1
        self.assertFalse(self.decision_maker.inter_cluster_breeding_time)

    def test__cutoff_function(self):
        self.fail()
