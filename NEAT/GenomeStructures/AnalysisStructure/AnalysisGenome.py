"""
AnalysisGenome module
"""

import copy
from typing import List, Dict, Set, Generic

from NEAT.Analyst import AnalysisResult
from NEAT.GenomeStructures.StorageStructure import StorageGenome
from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure


class AnalysisGenome(Generic[GenomeStructure]):
    """
    Data structure used for analysing genome graphs.
    It uses an adjacency list representation of the genome graph
    which is compatible with well known graph algorithms.
    """

    def __init__(
            self,
            other_structure: StorageGenome = None
    ) -> None:

        self._nodes = set({})  # type: Set[str]
        self._edges = dict({})  # type: Dict[str, List[str]]
        self._graph_initialised = False  # type: bool

        if other_structure:
            self.init_from_storage_structure(other_structure)

    def _add_node(self, label: str) -> None:

        self._nodes.add(label)

    def _add_edge(self, source: str, target: str) -> None:
        """
        Adds an edge to the original graph.

        :param source: The label of the outgoing node.
        :param target: The label of the incoming node
        :return: None
        """

        if not source in self._edges.keys():
            self._edges[source] = [target]

        elif not target in self._edges[source]:
            self._edges[source].append(target)

    def init_from_storage_structure(
            self,
            other_structure: StorageGenome.StorageGenome
    ) -> None:

        self._graph_initialised = True

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._edges

    @property
    def initialised(self):
        return self._graph_initialised