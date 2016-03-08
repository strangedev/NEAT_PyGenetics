from bson import ObjectId


class Cluster(object):
    """
    Object used to represent a single cluster as stored
    in the database.
    """

    def __init__(
            self,
    ):

        self._id = ObjectId() # type: ObjectId
        self.representative = None # type: ObjectId
        self.fitness = 0 # type: float
        self.offspring = 0 # type: int
        self.alive = True