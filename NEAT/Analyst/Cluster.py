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

    def __eq__(self, obj: 'Cluster') -> bool:
        return self._id.__eq__(obj._id) and \
            self.representative.__eq__(obj.representative) and \
            self.fitness.__eq__(obj.fitness) and \
            self.offspring.__eq__(obj.offspring) and \
            self.alive.__eq__(obj.alive)