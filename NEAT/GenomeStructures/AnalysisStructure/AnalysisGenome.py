"""
AnalysisGenome module
"""
from typing import Tuple, List, Dict, Set, Generic
import copy
from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure
from NEAT.GenomeStructures.AnalysisStructure import AnalysisResult
from NEAT.GenomeStructures.SimulationStructure import SimulationGenome
from NEAT.GenomeStructures.SimulationStructure import SimulationNodes
from NEAT.GenomeStructures.StorageStructure import StorageGenome


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
        self._cycle_nodes = set({})  # type: Set[str]
        self._cycle_edges = dict({})  # type: Dict[str, List[str]]
        self._working_edges = dict({})  # type: Dict[str, List[str]]
        self._working_nodes = set({})  # type: Set[str]
        self._result = AnalysisResult.AnalysisResult()
        self._colors = dict({})
        self._predecessors = dict({})  # do I even need this?
        self._nodes_top_sorted = []  # type: List[str]
        self._analysis_has_finished = False  # type: bool
        self._graph_initialized = False  # type: bool

        if other_structure:
            self.init_from_storage_structure(other_structure)
            self.analyse()

    def _add_node(self, label: str):

        self._nodes.add(label)

    def _add_edge(self, source: str, target: str) -> None:
        """
        Adds an edge to the original graph.

        :param source: The label of the outgoing node.
        :param target: The label of the incoming node
        :param id:
        :return:
        """

        if not source in self._edges.keys():
            self._edges[source] = [target]

        elif not target in self._edges[source]:
            self._edges[source].append(target)

    def init_from_storage_structure(
            self,
            other_structure: StorageGenome.StorageGenome
    ) -> None:

        pass

    def analyse(self) -> None:
        """
        Analysis method.
        Runs depth first search on the graph in order to find cycles and
        sort the graph topologically.
        Creates an AnalysisResult object which can be accessed through
        AnalysisGenome.result.

        :return: None
        """

        if not self._graph_initialized:
            raise Exception("Analysis called before graph was initialized")

        # Algo:
        # reset internal fields
        # copy graph to working copy
        # call dfs on working copy
        #   classify edges
        #   mark cycle nodes
        # ^ deprecated, cycles are detected while dfs_visit is running
        # write analysis of dag to result
        # reset internal fields
        # move only cycle node edges to working copy
        # call dfs on working copy
        # write analysis of cycle dag to result

        self._reset_analysis()
        self._set_working_graph(self._nodes, self._edges)
        self._dfs()

        self._result.nodes = copy.deepcopy(self._nodes_top_sorted)  # nodes stay the same
        self._result.edges = copy.deepcopy(self._edges)  # remove the cycle edges later
        #  Don't add cycle nodes yet, as they are not sorted at this point
        self._result.cycle_edges = copy.deepcopy(self._cycle_edges)

        for source in self._cycle_nodes:  # removal of the cycle edges

            target = self._cycle_edges[source]
            self._result.edges[source].remove(target)

        self._reset_analysis()
        self._set_working_graph(self._cycle_nodes, self._cycle_edges)
        self._dfs()

        self._result.cycle_nodes = copy.deepcopy(self._nodes_top_sorted)

        self._analysis_has_finished = True

    def _reset_analysis(self):
        """
        Resets internal fields of class where intermediate results
        of the analysis are stored in order to be able to perform
        another (sub-)analysis.

        :return:
        """

        self._colors.clear()
        self._predecessors.clear()
        self._cycle_nodes.clear()
        self._cycle_edges.clear()
        self._nodes_top_sorted.clear()

    def _set_working_graph(self, nodes: Set[str], edges: Dict[str, List[str]]) -> None:
        """
        Creates a working copy of the graph to be analyzed in order
        to preserve the original graph.

        :param nodes: A set of node labels
        :param edges: A dict (adjacency list) of edges
        :return: None
        """

        self._working_nodes = copy.deepcopy(nodes)
        self._working_edges = copy.deepcopy(edges)

    def _dfs(self) -> None:
        """
        Performs depth first search on _working_edges.
        Classifies back-edges while encountering them and creates
        a topological ordering in self._nodes_top_sorted.

        :return: None
        """

        pass

    def _dfs_visit(self, node: str) -> None:
        """
        Main DFS method. Separated from _dfs because of the possibility of
        multiple entry points in the graph.

        :param node: The label of the starting node.
        :return: None
        """

        pass


    @property
    def result(self) -> AnalysisResult.AnalysisResult:

        if self._analysis_has_finished:
            return self._result

        else:
            raise Exception("Analysis not completed before accessing result")
