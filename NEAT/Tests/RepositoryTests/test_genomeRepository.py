from unittest import TestCase
from unittest.mock import MagicMock

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.GenomeRepository import GenomeRepository


class TestGenomeRepository(TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.genome_repo = GenomeRepository(self.db)

    def test_get_new_genome(self):
        self.assertEqual(StorageGenome().__class__, self.genome_repo.get_new_genome().__class__)

    def test_get_current_population(self):
        self.db.find_many = (lambda x, y: [{},{},{}])
        self.assertListEqual([None, None, None], self.genome_repo.get_current_population())

    def test_get_genome_by_id(self):
        self.db.find_one_by_id = (lambda x, y: {})
        self.assertEqual(None, self.genome_repo.get_genome_by_id(2))

    def test_get_genomes_in_cluster(self):
        self.db.find_many = (lambda x, y: [{}, {}, {}])
        self.assertEqual([None, None, None], self.genome_repo.get_genomes_in_cluster(2))

    def test_insert_genome(self):
        self.db.insert_one = (lambda x, y: False)
        self.genome_repo.insert_genome(StorageGenome())

    def test_insert_genomes(self):
        self.db.insert_one = (lambda x, y: False)
        g = []
        for i in range(1,4):
            g.append(StorageGenome())
        self.genome_repo.insert_genomes(g)

    def test_update_genome(self):
        self.db.update_one = (lambda x, y, z: False)
        self.genome_repo.update_genome(StorageGenome())

    def test_update_genomes(self):
        self.db.update_many = (lambda x, y: False)
        g = []
        for i in range(1,4):
            g.append(StorageGenome())
        self.genome_repo.update_genomes(g)
