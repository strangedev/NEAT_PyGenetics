from unittest import TestCase
from unittest.mock import MagicMock

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository import Transformator
from NEAT.Repository.GenomeRepository import GenomeRepository


class TestGenomeRepository(TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.genome_repository = GenomeRepository(self.db)

    def test_get_new_genome(self):
        self.assertEqual(StorageGenome().__class__, self.genome_repository.get_new_genome().__class__)

    def test_get_current_population(self):
        self.db.find_many = (lambda x, y: [{},{},{}])
        self.assertListEqual([None, None, None], self.genome_repository.get_current_population())

    def test_get_genome_by_id(self):
        self.db.find_one_by_id = (lambda x, y: {})
        self.assertEqual(None, self.genome_repository.get_genome_by_id(2))

    def test_get_genomes_in_cluster(self):
        self.db.find_many = (lambda x, y: [{}, {}, {}])
        self.assertEqual([None, None, None], self.genome_repository.get_genomes_in_cluster(2))

    def test_insert_genome(self):
        self.db.insert_one = (lambda x, y: y)
        genome = StorageGenome()
        encode = Transformator.Transformator.encode_StorageGenome(genome)
        self.assertDictEqual(encode, self.genome_repository.insert_genome(genome))

    def test_insert_genomes(self):
        self.db.insert_many = (lambda x, y: y)
        e = []
        g = []
        for i in range(1,4):
            genome = StorageGenome()
            g.append(genome)
            e.append(Transformator.Transformator.encode_StorageGenome(genome))
        self.assertListEqual(e, self.genome_repository.insert_genomes(g))

    def test_update_genome(self):
        self.db.update_one = (lambda x, y, z: False)
        self.assertFalse(self.genome_repository.update_genome(StorageGenome()))

    def test_update_genomes(self):
        self.db.update_many = (lambda x, y: False)
        g = []
        for i in range(1,4):
            g.append(StorageGenome())
        self.assertFalse(self.genome_repository.update_genomes(g))

    def test_disable_genome(self):
        g = StorageGenome()
        g.is_alive = True

        genome = Transformator.Transformator.encode_StorageGenome(g)
        self.db.find_one_by_id = MagicMock(return_value=genome)
        self.db.update_one = MagicMock(return_value=True)

        self.assertTrue(
            self.genome_repository.disable_genome(g._id)
        )
        self.assertFalse(Transformator.Transformator.decode_StorageGenome(genome).is_alive)

    def test_disable_genomes(self):
        self.genome_repository.update_genomes = (lambda x:x)
        self.db.find_one_by_id = (lambda x:x)
        genomes = []
        for i in range(0,10):
            g = StorageGenome()
            g.is_alive = True
            genomes.append(g)

        for i in self.genome_repository.disable_genomes(genomes):
            self.assertFalse(i.is_alive)