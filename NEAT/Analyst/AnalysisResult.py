from typing import List, Set, Dict


class AnalysisResult(object):
    """
    Object used to store results of graph analysis.

    Attributes:
        genomeDisabledMap: a dict that consists of gene id's (ints) as keys
            a boolean value that is true, if the gene closes a circle in the a-
            nalyzed graph.
        topologically_sorted_nodes: a list of all nodes in the analyzed graph in
            topological order.
        topologically_sorted_cycle_nodes: a list of all cycle closing nodes (at
            the source of the closing edge) in topological order. This is a sub-
            set of topologically_sorted_nodes.
    """
    def __init__(self) -> None:
        self.disabled_nodes = set({})  # type: Set[int]

        # maps edges to true, if the close a circle in the analyzed graph,
        #               false, if the don't.
        self.genomeDisabledMap = dict({})  # type: Dict[int, bool]

        # all nodes in topological order
        self.topologically_sorted_nodes = []  # type: List[int]
        # all circle closing nodes in topological order (subset of nodes)
        self.topologically_sorted_cycle_nodes = []  # type: List[int]

    def __eq__(self, obj: 'AnalysisResult'):
        return self.disabled_nodes.__eq__(obj.disabled_nodes) \
            or self.genomeDisabledMap.__eq__(obj.genomeDisabledMap) \
            or self.topologically_sorted_nodes\
                   .__eq__(obj.topologically_sorted_nodes) \
            or self.topologically_sorted_cycle_nodes\
                   .__eq__(obj.topologically_sorted_cycle_nodes)

    def clear(self) -> None:
        self.__init__()

    @property
    def cycle_nodes(self) -> Set[int]:
        return set(self.topologically_sorted_cycle_nodes)
