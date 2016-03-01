
class Cluster(object):
    """
    Object used to represent a single cluster as stored
    in the database.
    """

    def __init__(
            self,
            id: int,
            representative: int
    ):

        self._id = id # type: int
        self.representative = representative # type: int
        self.fitness = 0 # type: float
        self.offspring = 0 # type: int
