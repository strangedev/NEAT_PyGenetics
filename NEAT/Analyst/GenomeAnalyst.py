from typing import List, Dict, Set, Iterable
import copy
from NEAT.GenomeStructures.AnalysisStructure import AnalysisGenome
from NEAT.Analyst import AnalysisResult


class GenomeAnalyst(object):

    def __init__(self):
        """
        _node_visited:
          _node_visited[i] = 0 => node with id i was not visited yet
          _node_visited[i] = 1 => node with id i was visited
        :return:
        """
        self._cycle_nodes = set({})  # type: Set[int]
        self._cycle_edges = dict({})  # type: Dict[int, List[int]]

        self._working_nodes = set({})  # type: Set[int]
        self._working_edges = dict({})  # type: Dict[int, List[int]]

        self._nodes_top_sorted = []  # type: List[int]
        self._cycle_nodes_top_sorted = []  # type: List[int]

        self._result = AnalysisResult.AnalysisResult()
        self._node_visited = dict({})  # type: Dict[int, int]

    def _add_cycle_node(self, node_id: int) -> None:
        self._cycle_nodes.add(node_id)

    def _add_cycle_edge(self, source: int, target: int) -> None:
        """
        Adds a cycle-edge to the working graph.

        :param source: The label of the outgoing node.
        :param target: The label of the incoming node
        :return: None
        """
        if source not in self._cycle_edges.keys():
            self._cycle_edges[source] = [target]

        elif target not in self._cycle_edges[source]:
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
            raise Exception("Analysis called before genome graph was "
                            "initialized")

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
        self._dfs(genome.input_nodes.values())

        # nodes stay the same
        self._result.nodes = copy.deepcopy(self._nodes_top_sorted)
        # remove the cycle edges later
        self._result.edges = copy.deepcopy(genome.edges)
        #  Don't add cycle nodes yet, as they are not sorted at this point
        self._result.cycle_edges = copy.deepcopy(self._cycle_edges)

        for source in self._cycle_nodes:  # removal of the cycle edges
            target = self._cycle_edges[source]
            self._result.edges[source].remove(target)

        self._reset_analysis()
        self._set_working_graph(self._cycle_nodes, self._cycle_edges)
        self._dfs(self._working_nodes)

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
        self._node_visited.clear()
        self._cycle_nodes.clear()
        self._cycle_edges.clear()
        self._nodes_top_sorted.clear()
        self._cycle_nodes_top_sorted.clear()

    def _set_working_graph(self, nodes: Set[int], edges: Dict[int, List[int]]) -> None:
        """
        Creates a working copy of the graph to be analyzed in order
        to preserve the original graph.

        :param nodes: A set of node labels
        :param edges: A dict (adjacency list) of edges
        :return: None
        """
        self._working_nodes = nodes
        self._working_edges = edges

    def _dfs(self, entry_points: Iterable[int]) -> None:
        """
        Performs depth first search on _working_edges.
        Classifies back-edges while encountering them and creates
        a topological ordering in self._nodes_top_sorted.

        entry_points is used to tell the dfs, from which nodes only to start
        the search.

        :return: None
        """
        for node in entry_points:
            self._node_visited[node] = 0

        for node in entry_points:
            if self._node_visited[node] == 0:
                self._dfs_visit(node)

    def _dfs_visit(self, node: int) -> None:
        """
        Main DFS method. Separated from _dfs because of the possibility of
        multiple entry points in the graph.

        :param node: The label of the starting node.
        :return: None
        """
        self._node_visited[node] = 1  # mark node as discovered

        for neighbor in self._working_edges[node]:
            if self._node_visited[neighbor] == 0:
                self._dfs_visit(neighbor)

            # if an edge leads to a node that was already visited, the edge clo-
            # ses a cycle.
            if self._node_visited[neighbor] == 1:
                self._add_cycle_node(node)
                self._add_cycle_edge(node, neighbor)

        self._nodes_top_sorted.insert(0, node)
