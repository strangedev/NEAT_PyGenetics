import unittest
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class StorageGenomeTestCase(unittest.TestCase):
    def test_eq(self):
        """
        Tests, that the equality operator works.
        :return:
        """
        s1 = StorageGenome()
        s2 = StorageGenome()
        self.assertEquals(s1, s2)
