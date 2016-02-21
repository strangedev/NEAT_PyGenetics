from typing import Dict, List
from fractions import Fraction
import unittest
from NEAT.GenomeStructures.SimulationStructure.SimulationGenome \
    import SimulationGenome
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes \
    import Node, CycleNode


class TestSimulationGenome(unittest.TestCase):
    def test_basicExampleWithoutCycles(self):
        input_layer = {}  # type: Dict[str, Node]
        output_layer = {}  # type: Dict[str, Node]
        hidden_layer = []  # type: List[Node]
        cycle_nodes = []  # type: List[CycleNode]

        input_layer['input_1'] = Node()
        input_layer['input_2'] = Node()
        input_layer['input_3'] = Node()

        output_layer['output_1'] = Node()
        output_layer['output_2'] = Node()

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[0], Fraction(2, 10))
        input_layer['input_2'].add_successor(hidden_layer[0], Fraction(7, 10))

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[1], Fraction(1, 10))
        input_layer['input_3'].add_successor(hidden_layer[1], Fraction(3, 10))

        hidden_layer[0].add_successor(output_layer['output_1'], Fraction(6, 10))
        hidden_layer[1].add_successor(output_layer['output_1'], Fraction(8, 10))
        input_layer['input_2'].add_successor(
            output_layer['output_2'],
            Fraction(9, 10)
        )
        hidden_layer[1].add_successor(output_layer['output_2'], Fraction(5, 10))

        gen = SimulationGenome(
            0,
            input_layer=input_layer,
            output_layer=output_layer,
            hidden_layer=hidden_layer,
            cycle_nodes=cycle_nodes
        )

        result = gen.calculate_step([
            ('input_1', Fraction(5, 10)),
            ('input_2', Fraction(5, 10)),
            ('input_3', Fraction(5, 10))
        ])  # type: Dict[str, float]

        self.assertEqual(Fraction(43, 100), result['output_1'])
        self.assertEqual(Fraction(55, 100), result['output_2'])

    def test_basicExampleWithCycles(self):
        input_layer = {}  # type: Dict[str, Node]
        output_layer = {}  # type: Dict[str, Node]
        hidden_layer = []  # type: List[Node]
        cycle_nodes = []  # type: List[CycleNode]

        input_layer['input_1'] = Node()
        input_layer['input_2'] = Node()

        output_layer['output_1'] = Node()
        output_layer['output_2'] = Node()

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[0], Fraction(7, 10))
        input_layer['input_2'].add_successor(hidden_layer[0], Fraction(3, 10))

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[1], Fraction(6, 10))
        hidden_layer[0].add_successor(hidden_layer[1], Fraction(4, 10))

        single_cycle_node = CycleNode(Fraction(74, 100))
        hidden_layer.append(single_cycle_node)
        cycle_nodes.append(single_cycle_node)
        hidden_layer[1].add_successor(hidden_layer[2], Fraction(3, 10))
        single_cycle_node.add_cycle_successor(hidden_layer[0], Fraction(6, 10))

        hidden_layer[1].add_successor(output_layer['output_1'], Fraction(7, 10))
        hidden_layer[2].add_successor(output_layer['output_2'], Fraction(5, 10))

        gen = SimulationGenome(
            1,
            input_layer=input_layer,
            output_layer=output_layer,
            hidden_layer=hidden_layer,
            cycle_nodes=cycle_nodes
        )

        result = gen.calculate_step([
            ('input_1', Fraction(5, 10)),
            ('input_2', Fraction(5, 10))
        ])
        print(result)
        print(single_cycle_node.memory_value)

        self.assertEqual(Fraction(5929, 12500), result['output_1'])
        self.assertEqual(Fraction(2541, 25000), result['output_2'])
        self.assertEqual(Fraction(2541, 12500), single_cycle_node.memory_value)
