from bson import ObjectId


class Cluster(object):
    """
    Object used to represent a single cluster as stored
    in the database.
    """

    def __init__(
            self,
            id: ObjectId,
            representative: ObjectId
    ):

        self._id = id # type: ObjectId
        self.representative = representative # type: ObjectId
        self.fitness = 0 # type: float
        self.offspring = 0 # type: int
