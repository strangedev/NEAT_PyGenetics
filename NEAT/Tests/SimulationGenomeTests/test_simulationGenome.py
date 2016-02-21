from typing import Dict, List
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
        input_layer['input_1'].add_successor(hidden_layer[0], 0.2)
        input_layer['input_2'].add_successor(hidden_layer[0], 0.7)

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[1], 0.1)
        input_layer['input_3'].add_successor(hidden_layer[1], 0.3)

        hidden_layer[0].add_successor(output_layer['output_1'], 0.6)
        hidden_layer[1].add_successor(output_layer['output_1'], 0.8)
        input_layer['input_2'].add_successor(output_layer['output_2'], 0.9)
        hidden_layer[1].add_successor(output_layer['output_2'], 0.5)

        gen = SimulationGenome(
            0,
            input_layer=input_layer,
            output_layer=output_layer,
            hidden_layer=hidden_layer,
            cycle_nodes=cycle_nodes
        )

        result = gen.calculate_step([
            ('input_1', 0.5),
            ('input_2', 0.5),
            ('input_3', 0.5)
        ])  # type: Dict[str, float]

        self.assertEqual(0.43, result['output_1'])
        self.assertEqual(0.55, result['output_2'])

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
        input_layer['input_1'].add_successor(hidden_layer[0], 0.7)
        input_layer['input_2'].add_successor(hidden_layer[0], 0.3)

        hidden_layer.append(Node())
        input_layer['input_1'].add_successor(hidden_layer[1], 0.6)
        hidden_layer[0].add_successor(hidden_layer[1], 0.4)

        single_cycle_node = CycleNode(0.74)
        hidden_layer.append(single_cycle_node)
        cycle_nodes.append(single_cycle_node)
        hidden_layer[1].add_successor(hidden_layer[2], 0.3)
        single_cycle_node.add_cycle_successor(hidden_layer[0], 0.6)

        hidden_layer[1].add_successor(output_layer['output_1'], 0.7)
        hidden_layer[2].add_successor(output_layer['output_2'], 0.5)

        gen = SimulationGenome(
            1,
            input_layer=input_layer,
            output_layer=output_layer,
            hidden_layer=hidden_layer,
            cycle_nodes=cycle_nodes
        )

        result = gen.calculate_step([
            ('input_1', 0.5),
            ('input_2', 0.5)
        ])
        print(result)
        print(single_cycle_node.memory_value)

        self.assertEqual(0.47431999999999996, result['output_1'])
        self.assertEqual(0.10164, result['output_2'])
        self.assertEqual(0.20328, single_cycle_node.memory_value)
