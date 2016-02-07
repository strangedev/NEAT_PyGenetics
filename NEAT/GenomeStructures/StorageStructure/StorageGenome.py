from NEAT.GenomeStructures.SimulationStructure import SimulationGenome

class StorageGenome(object):
    """
    This is BS -> Rework

    A data structure for storing genome information in a
    compact way.
    It stores genome information as tuple:
    (gene_id, weight, disabled)
    """

    def __init__(
            self,
            genome: SimulationGenome.SimulationGenome=None
    ):
        """
        TODO: augment default constructor
        """

        if genome:
            self.add_genome(genome)

    def add_genome(
            self,
            genome: SimulationGenome.SimulationGenome
    ) -> None:
        """
        Initializes self with structure of a given genome.
        """



        pass


