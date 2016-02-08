from typing import Iterable, Tuple, Generic

from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure

class SimulationGenome(Generic[GenomeStructure]):
    def __init__(
            self,
            id: int,
            input_layer=None,
            output_layer=None,
            hidden_layer=None,
            cycle_nodes=None
    ) -> None:
        """
        :param input_layer: Dict of input label:nodes.
        :param output_layer: Dict of output label:nodes.
        :param hidden_layer: List of hidden nodes in topological order.
        :param cycle_nodes: List of cycle nodes in topological order.
         Subset of hidden_layer.
        :return SimulationGenome:
        """
        self.id = id
        self.input_layer = input_layer or {} # type: dict
        self.output_layer = output_layer or {} # type: dict
        self.hidden_layer = hidden_layer or [] # type: list
        self.cycle_nodes = cycle_nodes or [] # type: list

    def set_input(
            self,
            inputs: Iterable[Tuple[str, float]]
    ) -> None:

        for label, value in inputs:
            self.input_layer[label].set_value(value)

    @property
    def output(self) -> dict:
        """
        :return: Dict of output nodes' label:value
        """
        return {label: node.get_value() for label, node in self.output_layer}

    def calculate_step(
            self,
            inputs: Iterable[Tuple[str, float]]
    ) -> dict:
        """
        :param inputs: List of tuples of the form (node_label, value)
        :return: None
        """
        self.set_input(inputs)

        for node in self.hidden_layer:
            node.reset()
        for node in self.output_layer:
            node.reset()

        for node in self.cycle_nodes:
            node.fire_cycles()
        for node in self.input_layer:
            node.fire()
        for node in self.hidden_layer:
            node.fire()

        return self.output
