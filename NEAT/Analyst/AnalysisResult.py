from typing import List, Set, Dict


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.
    """
    def __init__(self) -> None:
        self.disabled_nodes = set({})  # type: Set[int]
        self.edges = dict({})  # type: Dict[int, List[int]]
        self.topologically_sorted_nodes = []  # type: List[int]

        self.cycle_nodes = set({})  # type: Set[int]
        self.cycle_edges = dict({})  # type: Dict[int, List[int]]
        self.topologically_sorted_cycle_nodes = []  # type: List[int]

    def clear(self) -> None:
        self.__init__()
