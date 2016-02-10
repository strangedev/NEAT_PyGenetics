from typing import List, Dict


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.
    """

    def __init__(self):

        self.nodes = []  # type: List[str]
        self.cycle_nodes = []  # type: List[str]
        self.edges = dict({})  # type: Dict[str, List[str]]
        self.cycle_edges = dict({})  # type: Dict[str, List[str]]
