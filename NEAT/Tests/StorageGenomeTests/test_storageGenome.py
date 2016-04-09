import unittest
from fractions import Fraction

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

    def test_copyConstruct(self):
        s1 = StorageGenome()
        s1.inputs['uiae'] = 1
        s1.inputs['eaiu'] = 2
        s1.outputs['nrtd'] = 3
        s1.outputs['dtrn'] = 4
        s1.genes[2] = (True, float(Fraction(15, 11)))
        s1.genes[5] = (True, float(Fraction(135, 9)))
        s1.genes[12] = (True, float(Fraction(17, 81)))
        s1.analysis_result.topologically_sorted_nodes = [1, 5, 7, 2, 3, 8]
        s1.analysis_result.topologically_sorted_cycle_nodes = [3, 2, 8, 1]
        s1.analysis_result.gene_closes_cycle_map[5] = True
        s2 = StorageGenome(s1)

        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1._id, s2._id)
        self.assertDictEqual(s1.inputs, s2.inputs)
        self.assertDictEqual(s1.outputs, s2.outputs)
        self.assertDictEqual(s1.genes, s2.genes)
        self.assertEqual(s1.cluster, s2.cluster)
        self.assertEqual(s1.analysis_result, s2.analysis_result)
        self.assertNotEqual(s1.__repr__(), s2.__repr__())
