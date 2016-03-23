from bson.objectid import ObjectId


class Cluster(object):
    """
    Object used to represent a single cluster as stored
    in the database.

    Attributes:
        cluster_id (_id):
            The Cluster's ID, unique
        representative:
            The ID of the representative StorageGenome.
            All genomes in the cluster are topologically similar
            to it's representative genome.
        fitness:
            The cluster's fitness value.
            This is calculated from the fitness values of the
            contained genomes by a shared fitness approach.
        offspring:
            The amount of offspring that will be generated based
            on genomes from this clusters during the next generation.
        alive:
            Whether the cluster is alive, i.e. if there are any
            genomes in the current population which belong to this
            cluster.
    """

    def __init__(
            self,
    ):
        self._id = ObjectId()  # type: ObjectId
        self.representative = None  # type: ObjectId
        self.fitness = 0  # type: float
        self.offspring = 0  # type: int
        self.alive = True

    def __eq__(self, obj: 'Cluster') -> bool:
        return self._id.__eq__(obj._id) and \
            self.representative.__eq__(obj.representative) and \
            self.fitness.__eq__(obj.fitness) and \
            self.offspring.__eq__(obj.offspring) and \
            self.alive.__eq__(obj.alive)

    @property
    def cluster_id(self):
        return self._id
