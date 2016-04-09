import unittest
from unittest.mock import MagicMock
from random import Random
from fractions import Fraction

from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import Node
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import CycleNode


class TestSimulationNode(unittest.TestCase):
    def setUp(self):
        self.rand = Random()
        self.rand.seed(1337)

    def test_createNodeWithoutInitialValue(self):
        """
        Checks, that casually initializing a Node works as intended.
        :return:
        """
        node = Node()
        self.assertEqual(0, node.initial_value)
        self.assertEqual(0, node.value)
        self.assertListEqual([], node.successors)
        self.assertDictEqual({}, node.weights)

    def test_createNodeWithInitialValue(self):
        """
        Generates 100 random values from -1 to 2 and creates nodes with them as
        initial values. Checks, that for values below zero and above one a
        ValueError is raised.
        :return:
        """
        for val in [self.rand.uniform(-1, 2) for _ in range(100)]:
            if val < 0 or val > 1:
                with self.assertRaises(ValueError):
                    Node(Fraction.from_float(val))
            else:
                node = Node(Fraction.from_float(val))
                self.assertEqual(val, node.initial_value)
                self.assertEqual(val, node.value)

    def test_resetNode(self):
        """
        Tests, that resetting a node returns its value to zero.
        :return:
        """
        node = Node()
        node.value = float(Fraction(7, 10))
        node.reset()
        self.assertEqual(0, node.value)

    def test_resetNodeWithInitialValue(self):
        """
        Tests, that resetting a node that was initialized with a value returns
        its value to that initial value.
        :return:
        """
        node_with_initial_value = Node(float(Fraction(1, 5)))
        node_with_initial_value.value = float(Fraction(1, 2))
        node_with_initial_value.reset()
        self.assertEqual(float(Fraction(1, 5)), node_with_initial_value.value)

    def test_addSuccessor(self):
        """
        Generates 100 random values from -1 to 2. Creates new nodes for every
        value and adds them using the generated value as the weight.
        Checks, that for values below zero and above one a
        ValueError is raised.
        :return:
        """
        test_node = Node()
        for val in [self.rand.uniform(-1, 2) for _ in range(100)]:
            new_node = Node()
            if val < 0 or val > 1:
                with self.assertRaises(ValueError):
                    test_node.add_successor(new_node, Fraction.from_float(val))
            else:
                test_node.add_successor(new_node, Fraction.from_float(val))

    def test_addSuccessorThatAlreadyExists(self):
        """
        Adds the same node multiple times to another node and expects it to
        raise an Exception.
        :return:
        """
        # TODO: Specify type of Exception.
        test_node = Node()
        add_node = Node()
        with self.assertRaises(Exception):
            test_node.add_successor(add_node, float(Fraction(0)))
            test_node.add_successor(add_node, float(Fraction(0)))

    def test_addSuccessors(self):
        """
        Generates a list of nodes, appends it to a test node and checks, if
        add_successor was called for every node.
        :return:
        """
        test_node = Node()
        test_node.add_successor = MagicMock()
        node_list = [(Node(), float(Fraction(0))) for _ in range(10)]
        test_node.add_successors(node_list)
        for elem in node_list:
            self.assertIn((elem,), test_node.add_successor.call_args_list)

    def test_addSuccessorsOfWhichOneAlreadyExists(self):
        """
        Generates a list of nodes and duplicates some of them.
        Then checks, if appending the list to a node raises an Exception.
        :return:
        """
        test_node = Node()
        duplicate_node = Node()
        node_list = [(duplicate_node, float(Fraction(0)))]
        node_list.extend([(Node(), float(Fraction(0))) for _ in range(10)])
        node_list.append((duplicate_node, float(Fraction(0))))

        with self.assertRaises(Exception):
            test_node.add_successors(node_list)

    def test_fireNode(self):
        """
        Generates a list of nodes and weights, and a test node and their initial
        value. Then adds the list as successors to the node and calls fire.
        Checks that all values are calculated correctly.
        Also checks that firing multiple times sums the values.
        :return:
        """
        # TODO: check for transformation function
        value_list = [self.rand.uniform(0, 1) for _ in range(100)]
        node_list = [(Node(), Fraction.from_float(val)) for val in value_list]
        test_node = Node(float(Fraction(1, 2)))
        test_node.add_successors(node_list)

        # Creates a copy of the node list and manually calculates their values
        # after firing the test node
        fired_node_list = node_list.copy()
        for node, value in fired_node_list:
            node.add_value(0.5 * value)

        test_node.fire()
        self.assertListEqual(node_list, fired_node_list)

        # manually calculates values again
        for node, value in fired_node_list:
            node.add_value(0.5 * value)

        test_node.fire()
        self.assertListEqual(node_list, fired_node_list)

    def test_addValueToNode(self):
        """
        Tests, that add_value simply adds a given value to the stored value.
        :return:
        """
        node = Node()
        node.add_value(float(Fraction(1, 5)))
        self.assertEqual(float(Fraction(1, 5)), node.value)


class TestSimulationCycleNode(unittest.TestCase):
    def setUp(self):
        self.rand = Random()
        self.rand.seed(1337)

    def test_createNode(self):
        cycle_node = CycleNode(float(Fraction(1, 5)))
        self.assertEqual(float(Fraction(1, 5)), cycle_node.memory_value)
        self.assertListEqual([], cycle_node.cycle_successors)
        self.assertDictEqual({}, cycle_node.cycle_weights)

    def test_preserveMemory(self):
        cycle_node = CycleNode(float(Fraction(2, 10)))
        cycle_node.preserve_memory()
        self.assertEqual(float(Fraction(0)), cycle_node.memory_value)

    def test_preserveMemoryWithInitialValue(self):
        cycle_node = CycleNode(float(Fraction(2, 10)), float(Fraction(3, 10)))
        cycle_node.preserve_memory()
        self.assertEqual(float(Fraction(3, 10)), cycle_node.memory_value)

    def test_addCycleSuccessor(self):
        """
        Generates 100 random values from -1 to 2. Creates new nodes for every
        value and adds them using the generated value as the weight.
        Checks, that for values below zero and above one a
        ValueError is raised.
        :return:
        """
        test_node = CycleNode(float(Fraction(0)))
        for val in [self.rand.uniform(-1, 2) for _ in range(100)]:
            new_node = Node()
            if val < 0 or val > 1:
                with self.assertRaises(ValueError):
                    test_node.add_cycle_successor(
                        new_node,
                        Fraction.from_float(val)
                    )
            else:
                test_node.add_cycle_successor(
                    new_node,
                    Fraction.from_float(val)
                )

    def test_addCycleSuccessorThatAlreadyExists(self):
        """
        Adds the same node multiple times to another node and expects it to
        raise an Exception.
        :return:
        """
        # TODO: Specify type of Exception.
        test_node = CycleNode(float(Fraction(0)))
        add_node = CycleNode(float(Fraction(0)))
        with self.assertRaises(Exception):
            test_node.add_cycle_successor(add_node, float(Fraction(0)))
            test_node.add_cycle_successor(add_node, float(Fraction(0)))

    def test_addCycleSuccessors(self):
        """
        Generates a list of nodes, appends it to a test node and checks, if
        add_successor was called for every node.
        :return:
        """
        test_node = CycleNode(float(Fraction(0)))
        test_node.add_cycle_successor = MagicMock()
        node_list = [(Node(), float(Fraction(0))) for _ in range(10)]
        test_node.add_cycle_successors(node_list)
        for elem in node_list:
            self.assertIn((elem,), test_node.add_cycle_successor.call_args_list)

    def test_addCycleSuccessorsOfWhichOneAlreadyExists(self):
        """
        Generates a list of nodes and duplicates some of them.
        Then checks, if appending the list to a node raises an Exception.
        :return:
        """
        test_node = CycleNode(float(Fraction(0)))
        duplicate_node = CycleNode(float(Fraction(0)))
        node_list = [(duplicate_node, float(Fraction(0)))]
        node_list.extend(
            [(CycleNode(float(Fraction(0))), float(Fraction(0))) for _ in range(10)]
        )
        node_list.append((duplicate_node, float(Fraction(0))))

        with self.assertRaises(Exception):
            test_node.add_cycle_successors(node_list)

    def test_fireCycles(self):
        """
        Generates a list of nodes and weights, and a test node and their initial
        value. Then adds the list as cycle_successors to the node and calls
        fire.
        Checks that all values are calculated correctly.
        Also checks that firing multiple times sums the values.
        :return:
        """
        # TODO: check for transformation function
        value_list = [self.rand.uniform(0, 1) for _ in range(100)]
        node_list = [
            (CycleNode(float(Fraction(0))), Fraction.from_float(val))
            for val in value_list
            ]
        test_node = CycleNode(float(Fraction(0)), float(Fraction(1, 2)))
        test_node.add_successors(node_list)

        # Creates a copy of the node list and manually calculates their values
        # after firing the test node
        fired_node_list = node_list.copy()
        for node, value in fired_node_list:
            node.add_value(0.5 * value)

        test_node.fire()
        self.assertListEqual(node_list, fired_node_list)
