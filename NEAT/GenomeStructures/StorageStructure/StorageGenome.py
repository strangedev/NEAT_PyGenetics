from typing import List, Tuple
from fractions import Fraction

from NEAT.Analyst.AnalysisResult import AnalysisResult


class StorageGenome(object):
    """
    A data structure for storing genome information in a
    compact way.
    It stores genome information as tuple:
    (gene_id, weight, disabled)
    """

    def __init__(self):
        """
        id: The Genome's ID, unique in the population.
        inputs: A list of the ids of the input nodes. There has to be at least
          one gene per input that is connected to it. Represented as a list of
          tuples of the form (Input_Label, Node-ID).
        outputs: A list of the ids of the output nodes. There has to be at least
          one gene per output that is connected to it. Represented as a list of
          tuples of the form (Output_Label, Node-ID).
        genes: A list of all genes, that make up the genome. Presented as a tu-
          ple of Gene-ID, a boolean that is true, if the gene is disabled and a
          Fraction that stores the weight of the gene.
        analysis_result: A result object that is generated when analyzing the
          genome. This is per default empty.
        cluster: The cluster to which the Genome belongs.
        """
        self.id = int()
        self.inputs = {}  # type: Dict[str, int]
        self.outputs = {}  # type: Dict[str, int]
        self.genes = []  # type: List[Tuple[int, bool, Fraction]]
        self.analysis_result = AnalysisResult()
        self.cluster = int()
        pass
