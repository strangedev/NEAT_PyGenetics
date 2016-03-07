from collections import defaultdict
from typing import List, Dict, Set, Iterable, Tuple
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
        self._working_nodes = set({})  # type: Set[int]
        self._working_edges = dict({})  # type: Dict[int, List[int]]

        self._result = AnalysisResult.AnalysisResult()

    def analyze(
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
        # reset result object
        # set working graph to original graph
        # copy original edges to result
        # call dfs on working copy
        #   retrieve topologically sorted nodes and store them in result
        #   retrieve cycle edges and store them in result
        # remove cycle edges from edges in result
        # set working graph to cycle graph
        # call dfs on working copy
        #   retrieve topologically sorted cycle nodes and store them in result
        #   throw away empty cycle edges since at this point, there are no more
        #     edges in the working graph

        self._reset_analysis()
        self._set_working_graph(genome.nodes, genome.edges)

        # first add all edges to the result, remove found cycle closing edges
        # later
        self._result.genomeDisabledMap = copy.deepcopy(genome.edges)  # TODO: refactor AnalysisResult

        # store found topologically_sorted_nodes directly into the AnalysisRe-
        # sult
        # store found cycle_edges locally for further processing
        self._result.topologically_sorted_nodes, self._result.cycle_edges = \
            self._dfs(sorted(genome.input_nodes.values()))

        # removal of the cycle edges from the AnalysisResult
        for source in self._result.cycle_nodes:
            target_list = self._result.cycle_edges[source]
            for target in target_list:
                if target in self._result.genomeDisabledMap[source]:  # TODO: refactor AnalysisResult
                    self._result.genomeDisabledMap[source].remove(target)  # TODO: refactor AnalysisResult

        self._set_working_graph(
            self._result.cycle_nodes,
            self._result.cycle_edges)
        self._result.topologically_sorted_cycle_nodes, _ = \
            self._dfs(sorted(self._working_nodes))

        return self._result

    def _reset_analysis(self):
        """
        Resets internal fields of class where intermediate results
        of the analysis are stored in order to be able to perform
        another (sub-)analysis.

        :return:
        """
        self._result.clear()

    def _set_working_graph(self, nodes: Set[int],
                           edges: Dict[int, List[int]]) -> None:
        """
        Creates a working copy of the graph to be analyzed in order
        to preserve the original graph.

        :param nodes: A set of node labels
        :param edges: A dict (adjacency list) of edges
        :return: None
        """
        self._working_nodes = nodes
        self._working_edges = edges

    def _dfs(self, entry_points: Iterable[int]) \
            -> Tuple[List[int], Dict[int, List[int]]]:
        """
        Performs depth first search on _working_edges.
        Classifies back-edges while encountering them and creates
        a topological ordering in self._nodes_top_sorted.

        entry_points is used to tell the dfs, from which nodes only to start
        the search.

        :return: A tuple consisting of
          a topologically sorted list of the input nodes
          an adjacency list of found cycle edges in the form
            Dict[int, List[int]]
        """
        nodes_top_sorted = []  # type: List[int]
        cycle_edges = defaultdict(list)  # type: Dict[int, List[int]]
        visited_nodes = set({})  # type: Set[int]
        # node_visitation_status:
        # 0 means not visited yet
        # 1 means currently being visited
        # 2 means visited
        node_visitation_status = \
            {node: 0 for node in self._working_nodes}  # type: Dict[int, int]

        for node in entry_points:
            if node_visitation_status[node] == 0:
                self._dfs_visit(
                    node,
                    nodes_top_sorted,
                    cycle_edges,
                    visited_nodes,
                    node_visitation_status)

        return nodes_top_sorted, cycle_edges

    def _dfs_visit(self,
                   node: int,
                   nodes_top_sorted: List[int],
                   cycle_edges: Dict[int, List[int]],
                   visited_nodes: Set[int],
                   node_visitation_status: Dict[int, int]) -> None:
        """
        Main DFS method. Separated from _dfs because of the possibility of
        multiple entry points in the graph.

        First marks the node as currently being visited.

        If the node is not contained in the working edges dict (i.e. if the node
        does not have any successors), it is marked as finished and returned.

        The node's neighbors are iterated over.
        If a neighbor is not contained in the working nodes set (this only hap-
        pens when calling dfs on the cycleedge only subgraph and means, that the
        node is not one of the cycle nodes), it is skipped.
        If the neighbor was not visited yet, dfs is called on it.
        If the neighbor is currently being visited, the edge to it closes a cy-
        cle and is added to the dict of cycle_edges.

        The node is marked as finished and added at the front of the topologi-
        cally sorted list of nodes.

        :param node: The label of the starting node.
        :return: None
        """
        node_visitation_status[node] = 1

        if node not in self._working_edges:
            node_visitation_status[node] = 2
            return

        for neighbor in sorted(self._working_edges[node]):
            if neighbor not in self._working_nodes:
                continue
            if node_visitation_status[neighbor] == 0:
                self._dfs_visit(
                    neighbor,
                    nodes_top_sorted,
                    cycle_edges,
                    visited_nodes,
                    node_visitation_status)
            # if an edge leads to a node that is currently being visited, the
            # edge closes a cycle.
            elif node_visitation_status[neighbor] == 1:
                cycle_edges[node].append(neighbor)

        node_visitation_status[node] = 2
        nodes_top_sorted.insert(0, node)
