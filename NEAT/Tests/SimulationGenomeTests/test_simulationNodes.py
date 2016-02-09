import unittest
from unittest.mock import MagicMock
from random import Random
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import Node
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import CycleNode


class TestSimulationNode(unittest.TestCase):
    pass


class TestSimulationCycleNode(unittest.TestCase):
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
                    Node(val)
            else:
                node = Node(val)
                self.assertEqual(val, node.initial_value)
                self.assertEqual(val, node.value)

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
                    test_node.add_successor(new_node, val)
            else:
                test_node.add_successor(new_node, val)

    def test_addSuccessorThatAlreadyExists(self):
        """
        Adds the same node multiple times to another node and expects it to
        raise an Exception.
        TODO: Specify type of Exception.
        :return:
        """
        test_node = Node()
        add_node = Node()
        with self.assertRaises(Exception):
            test_node.add_successor(add_node, 0)
            test_node.add_successor(add_node, 0)

    def test_addSuccessors(self):
        """
        Generates a list of nodes, appends it to a test node and checks, if
        add_successor was called for every node.
        :return:
        """
        test_node = Node()
        test_node.add_successor = MagicMock()
        node_list = [(Node(), 0) for _ in range(10)]
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
        node_list = [(duplicate_node, 0)]
        node_list.extend([(Node(), 0) for _ in range(10)])
        node_list.append((duplicate_node, 0))

        with self.assertRaises(Exception):
            test_node.add_successors(node_list)
