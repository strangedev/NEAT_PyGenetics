from typing import Generic, Dict

from NEAT.ErrorHandling.Exceptions.InputMissingException import \
    InputMissingException
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import Node
from NEAT.GenomeStructures.SimulationStructure.SimulationNodes import CycleNode
from NEAT.Repository.GeneRepository import GeneRepository


class SimulationGenome(Generic[GenomeStructure]):
    """
    The SimulationGenome is a structural representation of a genome's genepool.
    It is optimized for the purpose of simulating a neural network and is gene-
    rated from a given StorageGenome.

    Attributes:
        _gene_repository:
            Access to information about the node ids in the StorageGenome
        _output:
            Contains the results of the last calculation process.
        _input_layer:
            A set of Nodes as the input layer. These are identical in number and
             ids with the input ids in the StorageGenome.
        _output_layer:
            A set of Nodes as the output layer. These are identical in number
            and ids with the output ids in the StorageGenome.
        _hidden_layer:
            A hidden layer. This consists of a list of nodes which are calcula-
            ted in the order of the list. This list is taken from the topologi-
            cally sorted node list in the given StorageGenome's AnalysisResult.
            So to ensure a functioning neural network, that list has to be cor-
            rect.
        _cycle_nodes:
            A list of CycleNodes, topologically sorted (like the hidden layer).
            These are nodes that have outgoing links that close a cycle. These
            nodes have to be treated separately, because the cycle closing edges
            have to be calculated first. For this initial calculation the last
            calculation value is used as the outgoing base value. If the genome
            was not simulated yet. a default value is used as the initial value.

    Usage:
        insert StorageGenome
        call calculate_step
        have fun
    """
    def __init__(
            self,
            gene_repository: GeneRepository,
            storage_genome: StorageGenome
    ) -> None:
        """
        :param GeneRepository gene_repository: Needed for access to the node
          storage. Is used when generating the structure.
        :param StorageGenome storage_genome: The StorageGenome from which the
          SimulationStructure is generated.
        """
        self._gene_repository = gene_repository
        self._init_from_storage_structure(storage_genome)

    def _init_from_storage_structure(
            self,
            storage_genome: StorageGenome
    ):
        """
        Builds the internal structure from a given StorageGenome.
        :param storage_genome:
        :return:
        """
        # Create all CycleNode Objects
        cycle_nodes = {}  # type: Dict[int, CycleNode]
        for node_id in \
                storage_genome.analysis_result.topologically_sorted_cycle_nodes:
            cycle_nodes[node_id] = CycleNode(0.0)

        # Create all Node Objects excluding previously created CycleNodes
        hidden_layer = {}  # type: Dict[int, Node]
        for node_id in \
                storage_genome.analysis_result.topologically_sorted_nodes:
            if node_id in cycle_nodes:
                hidden_layer[node_id] = cycle_nodes[node_id]
            else:
                hidden_layer[node_id] = Node()

        # Adds edges to the nodes based on the StorageGenome's Genes.
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

        # Generate sets of input and output nodes
        self._input_layer = \
            {label: hidden_layer[node_id] for label, node_id in storage_genome.inputs.items()}
        self._output_layer = \
            {label: hidden_layer[node_id] for label, node_id in storage_genome.outputs.items()}

        # Generate again topologically sorted list of Node Objects including
        # CycleNode Objects
        self._hidden_layer = \
            [hidden_layer[node_id]
             for node_id
             in storage_genome.analysis_result.topologically_sorted_nodes
             if node_id not in storage_genome.inputs.values() and
             node_id not in storage_genome.outputs.values()]

        # Generate again topologically sorted list of CycleNode Objects
        self._cycle_nodes = \
            [cycle_nodes[node_id]
             for node_id
             in storage_genome.analysis_result.topologically_sorted_cycle_nodes]

    def _set_inputs(
            self,
            inputs: Dict[str, float]
    ) -> None:
        """
        Sets the values of all input nodes to the corresponding values in the
        given input map.
        :param inputs:
            A map of the form
              id => value
        :return:
        """
        for node_id in self._input_layer:
            if node_id not in inputs:
                raise InputMissingException("Input for node " + node_id +
                                            " is missing.")
            self._input_layer[node_id].value = inputs[node_id]

    @property
    def output(self) -> Dict[str, float]:
        """
        :return: Dict of the output nodes' values of the form label:value
        """
        return {label: node.value for label, node in self._output_layer.items()}

    def calculate_step(
            self,
            inputs: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Sets inputs.
        Resets all values in the hidden and output layers.
        Iterates over cycle nodes, then input nodes, then hidden nodes and cal-
        culates each.
        Preserves the values of the Cycle Nodes.
        Returns the output nodes' values.
        :param inputs: List of tuples of the form (node_label, value)
        :return: Dict of output node labels and their current values.
        """
        self._set_inputs(inputs)

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
