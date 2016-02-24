
from typing import List, Dict, Set
import copy
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome
from NEAT.Analyst import AnalysisResult


class GenomeAnalyst(object):

    def __init__(self):
        self._cycle_nodes = set({})  # type: Set[str]
        self._cycle_edges = dict({})  # type: Dict[str, List[str]]
        self._working_edges = dict({})  # type: Dict[str, List[str]]
        self._working_nodes = set({})  # type: Set[str]
        self._result = AnalysisResult.AnalysisResult()
        self._colors = dict({})  # type: Dict[str, int]
        self._nodes_top_sorted = []  # type: List[str]

    def _add_cycle_node(self, label: str) -> None:
        self._cycle_nodes.add(label)

    def _add_cycle_edge(self, source: str, target: str) -> None:
        """
        Adds a cycle-edge to the working graph.

        :param source: The label of the outgoing node.
        :param target: The label of the incoming node
        :return: None
        """
        if not source in self._cycle_edges.keys():
            self._cycle_edges[source] = [target]

        elif not target in self._cycle_edges[source]:
            self._cycle_edges[source].append(target)

    def analyse(
            self,
            genome: AnalysisGenome.AnalysisGenome
    ) -> AnalysisResult.AnalysisResult:
        """
        Analysis method.
        Runs depth first search on the graph in order to find cycles and
        sort the graph topologically.
        Creates an AnalysisResult object which can be accessed through
        AnalysisGenome.result.

        :param genome:
        :return: None
        """
        if not genome.initialised:
            raise Exception("Analysis called before genome graph was initialized")

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
        self._set_working_graph(genome.nodes, genome.edges)
        self._dfs()

        self._result.nodes = copy.deepcopy(self._nodes_top_sorted)  # nodes stay the same
        self._result.edges = copy.deepcopy(genome.edges)  # remove the cycle edges later
        #  Don't add cycle nodes yet, as they are not sorted at this point
        self._result.cycle_edges = copy.deepcopy(self._cycle_edges)

        for source in self._cycle_nodes:  # removal of the cycle edges

            target = self._cycle_edges[source]
            self._result.edges[source].remove(target)

        self._reset_analysis()
        self._set_working_graph(self._cycle_nodes, self._cycle_edges)
        self._dfs()

        self._result.cycle_nodes = copy.deepcopy(self._nodes_top_sorted)

        return copy.deepcopy(self._result)

    def _reset_analysis(self):
        """
        Resets internal fields of class where intermediate results
        of the analysis are stored in order to be able to perform
        another (sub-)analysis.

        :return:
        """
        self._result.clear()
        self._colors.clear()
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
        self._working_nodes = nodes
        self._working_edges = edges

    def _dfs(self) -> None:
        """
        Performs depth first search on _working_edges.
        Classifies back-edges while encountering them and creates
        a topological ordering in self._nodes_top_sorted.

        :return: None
        """
        for node in self._working_nodes:
            self._colors[node] = 0

        for node in self._working_nodes:

            if self._colors[node] == 0:
                self._dfs_visit(node)

    def _dfs_visit(self, node: str) -> None:
        """
        Main DFS method. Separated from _dfs because of the possibility of
        multiple entry points in the graph.

        :param node: The label of the starting node.
        :return: None
        """
        self._colors[node] = 1  # node is discovered

        for neighbor in self._working_edges[node]:

            if self._colors[neighbor] == 0:

                self._dfs_visit(neighbor)

            if self._colors[neighbor] == 1:  # Grey indicates back edge

                self._add_cycle_node(node)
                self._add_cycle_edge(node, neighbor)

        self._colors[node] = 2  # no more neighbors, node is finished
        self._nodes_top_sorted.insert(0, node)