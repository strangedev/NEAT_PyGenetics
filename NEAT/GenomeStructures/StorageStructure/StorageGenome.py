from typing import List, Tuple, Dict
from fractions import Fraction

from bson import ObjectId

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
        self._id = ObjectId()
        self.is_alive = True
        self.fitness = 0  # type: float
        self.inputs = {}  # type: Dict[str, int]
        self.outputs = {}  # type: Dict[str, int]
        self.genes = []  # type: List[Tuple[int, bool, Fraction]]
        self.analysis_result = AnalysisResult()
        self.cluster = ObjectId()
        pass

    def __eq__(self, obj: 'StorageGenome'):
        if not self._id.__eq__(obj._id) \
                or not self.is_alive.__eq__(obj.is_alive) \
                or not self.inputs.__eq__(obj.inputs) \
                or not self.outputs.__eq__(obj.outputs) \
                or not self.genes.__eq__(obj.genes) \
                or not self.analysis_result.__eq__(obj.analysis_result) \
                or not self.fitness.__eq__(obj.fitness) \
                or not self.cluster.__eq__(obj.cluster):
            return False
        return True
