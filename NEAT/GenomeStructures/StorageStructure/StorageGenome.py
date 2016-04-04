from copy import deepcopy
from typing import List, Tuple, Dict
from fractions import Fraction

from bson.objectid import ObjectId

from NEAT.Analyst.AnalysisResult import AnalysisResult


class StorageGenome(object):
    """
    A data structure for storing genome information in a
    compact way.

    Attributes:
        genome_id (_id):
            The Genome's ID, unique in the population.
        inputs:
            A list of the ids of the input nodes. There has to be at least
            one gene per input that is connected to it. Represented as a list
            of tuples of the form (Input_Label, Node-ID).
        outputs:
            A list of the ids of the output nodes. There has to be at least
            one gene per output that is connected to it. Represented as a list
            of tuples of the form (Output_Label, Node-ID).
        genes:
            A list of all genes, that make up the genome. Presented as a tu-
            ple of Gene-ID, a boolean that is true, if the gene is disabled
            and a Fraction that stores the weight of the gene.
        analysis_result:
            A result object that is generated when analyzing the genome.
            This is empty per default.
        cluster:
            The cluster to which the Genome belongs.
    """

    def __init__(
            self,
            genome: 'StorageGenome' = None,
            inputs: List[str] = None,
            outputs: List[str] = None
    ):
        """
        :param genome: If genome is given, its inputs are copied
            (except for id)
        :param inputs: A list of strings, representing the inputs nodes' labels
        """
        self._id = ObjectId()
        self.is_alive = True if genome is None else genome.is_alive
        self.fitness = 0 if genome is None else genome.fitness  # type: float
        self.inputs = {} if genome is None else deepcopy(genome.inputs)  # type: Dict[str, int]
        self.outputs = {} if genome is None else deepcopy(genome.outputs)  # type: Dict[str, int]
        self.genes = {} if genome is None else deepcopy(genome.genes)  # type: Dict[int, Tuple[bool, Fraction]]
        self.analysis_result = AnalysisResult() if genome is None \
            else AnalysisResult(genome.analysis_result)
        self.cluster = ObjectId() if genome is None else genome.cluster
        if inputs and outputs:
            self._init_with_nodes(inputs, outputs)

    def _init_with_nodes(self, inputs: List[str], outputs: List[str]):
        node_id = 0
        for input_label in inputs:
            self.inputs[input_label] = node_id
            node_id += 1
        for output_label in outputs:
            self.outputs[output_label] = node_id
            node_id += 1

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

    @property
    def genome_id(self):
        return self._id
