from typing import List, Dict


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.
    """

    def __init__(self) -> None:
        self.nodes = set({})  # type: Set[str]
        self.cycle_nodes = set({})  # type: Set[str]
        self.edges = dict({})  # type: Dict[str, List[str]]
        self.cycle_edges = dict({})  # type: Dict[str, List[str]]

    def clear(self) -> None:
        self.__init__()

        
