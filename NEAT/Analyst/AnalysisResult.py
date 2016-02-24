from typing import List, Set, Dict


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.
    Note, that the field edges does not contain cycle closing edges anymore.
    The original set of edges is split into edges and cycle_edges, with
    edges and cycle_edges being disjoint sets.
    """
    def __init__(self) -> None:
        self.disabled_nodes = set({})  # type: Set[int]
        self.edges = dict({})  # type: Dict[int, List[int]]
        self.topologically_sorted_nodes = []  # type: List[int]

        self.cycle_edges = dict({})  # type: Dict[int, List[int]]
        self.topologically_sorted_cycle_nodes = []  # type: List[int]

    def clear(self) -> None:
        self.__init__()

    @property
    def nodes(self) -> Set[int]:
        return set([node for node in self.edges.keys()])

    @property
    def cycle_nodes(self) -> Set[int]:
        return set([node for node in self.cycle_edges.keys()])
