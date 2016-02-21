from typing import Tuple, Generic, Dict, List

from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import Node
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import CycleNode


class SimulationGenome(Generic[GenomeStructure]):
    def __init__(
            self,
            genome_id: int,
            input_layer: Dict[str, Node],
            output_layer: Dict[str, Node],
            hidden_layer: List[Node],
            cycle_nodes: List[CycleNode]
    ) -> None:
        """
        :param genome_id: The genome's global id.
        :param input_layer: Dict of input label:nodes.
        :param output_layer: Dict of output label:nodes.
        :param hidden_layer: List of hidden nodes in topological order.
        :param cycle_nodes: List of cycle nodes in topological order.
         Subset of hidden_layer.
        :return SimulationGenome:
        """
        self.genome_id = genome_id
        self.input_layer = input_layer if input_layer else {}
        self.output_layer = output_layer if output_layer else {}
        self.hidden_layer = hidden_layer if hidden_layer else []
        self.cycle_nodes = cycle_nodes if cycle_nodes else []

    def set_input(
            self,
            inputs: List[Tuple[str, float]]
    ) -> None:

        for label, value in inputs:
            self.input_layer[label].value = value

    @property
    def output(self) -> Dict[str, float]:
        """
        :return: Dict of output nodes' label:value
        """
        return {label: node.value for label, node in self.output_layer.items()}

    def calculate_step(
            self,
            inputs: List[Tuple[str, float]]
    ) -> Dict[str, float]:
        """
        :param inputs: List of tuples of the form (node_label, value)
        :return: Dict of output node labels and their current values.
        """
        self.set_input(inputs)

        for node in self.hidden_layer:
            node.reset()
        for node in self.output_layer.values():
            node.reset()

        for node in self.cycle_nodes:
            node.fire_cycles()
        for node in self.input_layer.values():
            node.fire()
        for node in self.hidden_layer:
            node.fire()

        for node in self.cycle_nodes:
            node.preserve_memory()

        return self.output
