"""
AnalysisGenome module
"""
from typing import Tuple, List, Dict, Set, Generic

from NEAT.GenomeStructures.TH_GenomeStructure import GenomeStructure

from NEAT.GenomeStructures.SimulationStructure import SimulationGenome
from NEAT.GenomeStructures.SimulationStructure import SimulationNodes
from NEAT.GenomeStructures.StorageStructure import StorageGenome


class AnalysisGenome(object, Generic[GenomeStructure]):
    """
    Data structure used for analysing genome graphs.
    It uses an adjacency list representation of the genome graph
    which is compatible with well known graph algorithms.
    """

    def __init__(
            self,
            other_structure: GenomeStructure=None
    ) -> None:

        self.__edges = {} # type: Dict[str, List[str]]
        self.__dag = {} # type: Dict[str, List[str]]
        self.__predecessors = {} # type: Dict[str, List[str]]
        self.__reverse_edges = set({}) # type: Set[Tuple[str, str]]
        self.__reverse_predecessors = {} # type: Dict[str, List[str]]

        if other_structure:

            structure_class = other_structure.__class__

            if structure_class == "SimulationGenome":
                self.init_from_simulation_structure(other_structure)
            elif structure_class == "StorageGenome":
                self.init_from_storage_structure(other_structure)


    def init_from_storage_structure(
            self,
            other_structure: StorageGenome.StorageGenome
    ) -> None:

        pass


    def init_from_simulation_structure(
            self,
            other_structure: SimulationGenome.SimulationGenome
    ) -> None:

        pass

    def get_dag_nodes(self) -> List[str]:
        """
        Returns the remaining nodes, after cycles have been removed
        from the graph.
        :return: A list of nodes in the dag.
        """

        pass

    def get_predecessors(self, node_label: str) -> List[str]:
        """
        :param node_label: The label of the node
        :return: A list of predecessors (labels) according to top. sort
        """
        pass

    def get_cycle_nodes(self) -> List[str]:
        """
        Returns nodes which are part of a cycle.
        :return: A list of cycle node labels.
        """
        pass


