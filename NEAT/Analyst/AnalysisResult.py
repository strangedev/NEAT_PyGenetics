from typing import List, Set


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.
    """
    def __init__(self) -> None:
        self.disabled_nodes = set({})  # type: Set[int]
        self.topologically_sorted_nodes = []  # type: List[int]

        self.cycle_nodes = set({})  # type: Set[int]
        self.topologically_sorted_cycle_nodes = []  # type: List[int]

    def clear(self) -> None:
        self.__init__()
