import unittest

from bson import ObjectId

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class StorageGenomeTestCase(unittest.TestCase):
    def test_eq(self):
        """
        Tests, that the equality operator works.
        :return:
        """
        s1 = StorageGenome()
        s2 = StorageGenome()
        s2._id = ObjectId(s1._id)
        s2.cluster = ObjectId(s1.cluster)
        self.assertEquals(s1, s2)

    def test_notEq(self):
        s1 = StorageGenome()
        s2 = StorageGenome()
        self.assertNotEqual(s1, s2)
