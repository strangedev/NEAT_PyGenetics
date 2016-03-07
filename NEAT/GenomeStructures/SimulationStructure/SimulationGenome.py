from typing import Tuple, Generic, Dict, List
from fractions import Fraction

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
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
        self._genome_id = genome_id
        self._input_layer = input_layer if input_layer else {}
        self._output_layer = output_layer if output_layer else {}
        self._hidden_layer = hidden_layer if hidden_layer else []
        self._cycle_nodes = cycle_nodes if cycle_nodes else []

    def _build_from_storage_genome(self, storage_genome: StorageGenome):
        self._input_layer = \
            {label: Node() for label in storage_genome.inputs.keys()}
        self._output_layer = \
            {label: Node() for label in storage_genome.outputs.keys()}

        cycle_nodes = {}
        for node_id in storage_genome.analysis_result.topologically_sorted_cycle_nodes:
            cycle_nodes[node_id] = CycleNode(Fraction(0))

        hidden_layer = {}
        for node_id in storage_genome.analysis_result.topologically_sorted_nodes:
            if node_id in cycle_nodes:
                hidden_layer[node_id] = cycle_nodes[node_id]
            else:
                hidden_layer[node_id] = Node()

        for label, node_id in storage_genome.inputs.items():
            for target_id in storage_genome.analysis_result.edges[node_id]:
                # TODO: add edge with correct weight (weight is stored in StorageGenome
                # and accessible with gene_id as key. gene_id has to be read from the edges
                # in the analysisResult. thus the gene_id has to be stored there in the analyst
                self._input_layer[label].add_successor(hidden_layer[target_id],)

    def set_input(
            self,
            inputs: List[Tuple[str, Fraction]]
    ) -> None:

        for label, value in inputs:
            self._input_layer[label].value = value

    @property
    def output(self) -> Dict[str, Fraction]:
        """
        :return: Dict of output nodes' label:value
        """
        return {label: node.value for label, node in self._output_layer.items()}

    def calculate_step(
            self,
            inputs: List[Tuple[str, Fraction]]
    ) -> Dict[str, Fraction]:
        """
        :param inputs: List of tuples of the form (node_label, value)
        :return: Dict of output node labels and their current values.
        """
        self.set_input(inputs)

        for node in self._hidden_layer:
            node.reset()
        for node in self._output_layer.values():
            node.reset()

        for node in self._cycle_nodes:
            node.fire_cycles()
        for node in self._input_layer.values():
            node.fire()
        for node in self._hidden_layer:
            node.fire()

        for node in self._cycle_nodes:
            node.preserve_memory()

        return self.output
