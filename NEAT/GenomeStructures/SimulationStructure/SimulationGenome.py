from typing import Tuple, Generic, Dict, List
from fractions import Fraction

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import Node
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import CycleNode
from NEAT.Repository.GeneRepository import GeneRepository


class SimulationGenome(Generic[GenomeStructure]):
    def __init__(
            self,
            gene_repository: GeneRepository,
            storage_genome: StorageGenome
    ) -> None:
        """
         Subset of hidden_layer.
        :param gene_repository:
        :param storage_genome:
        :return SimulationGenome:
        """
        self._gene_repository = gene_repository
        self._init_from_storage_structure(storage_genome)

    def _init_from_storage_structure(
            self,
            storage_genome: StorageGenome
    ):
        self._input_layer = \
            {label: Node() for label in storage_genome.inputs.keys()}
        self._output_layer = \
            {label: Node() for label in storage_genome.outputs.keys()}

        cycle_nodes = {}  # type: Dict[int, CycleNode]
        for node_id in \
                storage_genome.analysis_result.topologically_sorted_cycle_nodes:
            cycle_nodes[node_id] = CycleNode(Fraction(0))

        hidden_layer = {}  # type: Dict[int, Node]
        for node_id in \
                storage_genome.analysis_result.topologically_sorted_nodes:
            if node_id in cycle_nodes:
                hidden_layer[node_id] = cycle_nodes[node_id]
            else:
                hidden_layer[node_id] = Node()

        for gene_id, (is_disabled, weight) in storage_genome.genes.items():
            if is_disabled:
                continue
            closes_circle = \
                storage_genome.analysis_result.gene_closes_cycle_map[gene_id]
            source, target = \
                self._gene_repository.get_node_labels_by_gene_id(gene_id)
            if closes_circle:
                cycle_nodes[source].add_cycle_successor(
                    hidden_layer[target], weight
                )
            else:
                hidden_layer[source].add_successor(hidden_layer[target], weight)

        self._hidden_layer = \
            [hidden_layer[node_id]
             for node_id
             in storage_genome.analysis_result.topologically_sorted_nodes]

        self._cycle_nodes = \
            [cycle_nodes[node_id]
             for node_id
             in storage_genome.analysis_result.topologically_sorted_cycle_nodes]

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
