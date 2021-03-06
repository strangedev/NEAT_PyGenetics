"""
AnalysisGenome module
"""

import copy
from typing import List, Dict, Set, Generic
from typing import Tuple

from NEAT.Analyst import AnalysisResult
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure
from NEAT.Repository.GeneRepository import GeneRepository


class AnalysisGenome(Generic[GenomeStructure]):
    """
    Data structure used for analysing genome graphs.
    It uses an adjacency list representation of the genome graph
    which is compatible with well known graph algorithms.
    """

    def __init__(
            self,
            gene_repository: GeneRepository,
            storage_structure: StorageGenome = None
    ) -> None:
        """
        Creates an AnalysisGenome. If a StorageGenome is given, it is used for
        construction. Otherwise the AnalysisGenome is constructed empty.
        :param gene_repository:
        :param storage_structure:
        :return:
        """
        self._nodes = set({})  # type: Set[int]
        self._input_nodes = dict({})  # type: Dict[str, int]
        self._output_nodes = dict({})  # type: Dict[str, int]
        # TODO: fix all uses of _edges and property edges
        self._edges = dict({})  # type: Dict[int, List[Tuple[int, int]]]
        self._graph_initialized = False  # type: bool
        self._gene_repository = gene_repository

        if storage_structure:
            self._init_from_storage_structure(storage_structure)

    def _add_node(self, node_id: int) -> None:
        """
        Adds a node.
        :param node_id:
        :return:
        """
        self._nodes.add(node_id)

    def _add_input_node(self, node_id: int, label: str) -> None:
        """
        Adds a mapping (label => id) for an input node.
        :param node_id: The node's id.
        :param label: The node's label.
        :return:
        """
        self._nodes.add(node_id)
        self._input_nodes[label] = node_id

    def _add_output_node(self, node_id: int, label: str) -> None:
        """
        Adds a mapping (label => id) for an output node.
        :param node_id: The node's id.
        :param label: The node's label.
        :return:
        """
        self._nodes.add(node_id)
        self._output_nodes[label] = node_id

    def _add_edge(self, source: int, target: int, gene_id: int) -> None:
        """
        Adds an edge to the graph.

        :param source: The label of the outgoing node.
        :param target: The label of the incoming node
        :param gene_id: The id of the gene that connects the given nodes.
        :return: None
        """

        if source not in self._edges.keys():
            self._edges[source] = [(target, gene_id)]
            self._add_node(source)
            self._add_node(target)

        elif target not in self._edges[source]:
            self._edges[source].append((target, gene_id))
            self._add_node(target)

    def _init_from_storage_structure(
            self,
            storage_structure: StorageGenome
    ) -> None:
        """
        Initializes the AnalysisGenome based on a StorageGenome.
        Reads information from the given StorageGenome and creates a adjacency
        list based on it.
        :param storage_structure:
        :return:
        """
        for node_label, node_id in storage_structure.inputs.items():
            self._add_input_node(node_id, node_label)

        for node_label, node_id in storage_structure.outputs.items():
            self._add_output_node(node_id, node_label)

        for gene_id in storage_structure.genes.keys():
            head, tail = self._gene_repository.get_node_labels_by_gene_id(gene_id)
            self._add_edge(head, tail, gene_id)

        self._graph_initialized = True

    @property
    def input_nodes(self) -> Dict[str, int]:
        return self._input_nodes

    @property
    def output_nodes(self) -> Dict[str, int]:
        return self._output_nodes

    @property
    def nodes(self) -> Set[int]:
        return self._nodes

    @property
    def edges(self) -> Dict[int, List[Tuple[int, int]]]:
        return self._edges

    @property
    def initialised(self) -> bool:
        return self._graph_initialized
