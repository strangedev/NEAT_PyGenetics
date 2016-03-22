from fractions import Fraction
from unittest import TestCase
from unittest.mock import MagicMock

from bson import ObjectId

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
        self.db.find_many = (lambda x, y: [{}, {}, {}])
        self.assertListEqual([None, None, None], self.genome_repository.get_current_population())

    def test_get_genome_by_id(self):
        self.db.find_one_by_id = (lambda x, y: {})
        self.assertEqual(None, self.genome_repository.get_genome_by_id(ObjectId()))

    def test_get_genomes_in_cluster(self):
        self.db.find_many = (lambda x, y: [{}, {}, {}])
        self.assertEqual([None, None, None], self.genome_repository.get_genomes_in_cluster(ObjectId()))

    def test_insert_genome(self):
        self.db.insert_one = (lambda x, y: y)
        genome = StorageGenome()
        encode = Transformator.Transformator.encode_StorageGenome(genome)
        self.assertDictEqual(encode, self.genome_repository.insert_genome(genome))

    def test_insert_genomes(self):
        self.db.insert_many = (lambda x, y: y)
        e = []
        g = []
        for i in range(1, 4):
            genome = StorageGenome()
            g.append(genome)
            e.append(Transformator.Transformator.encode_StorageGenome(genome))
        self.assertListEqual(e, self.genome_repository.insert_genomes(g))

    def test_update_genome(self):
        self.db.update_one = (lambda x, y, z: False)
        self.assertFalse(self.genome_repository.update_genome(StorageGenome()))

    def test_update_genomes(self):
        self.genome_repository.update_genome = lambda x: x
        g = []
        count = 0
        for i in range(1, 4):
            g.append(StorageGenome())
        self.assertListEqual(g, self.genome_repository.update_genomes(g))

    def test_disable_genome(self):
        g = StorageGenome()
        g.is_alive = True

        genome = Transformator.Transformator.encode_StorageGenome(g)
        self.db.find_one_by_id = MagicMock(return_value=genome)
        self.genome_repository.update_genome = lambda x: x

        self.assertFalse(self.genome_repository.disable_genome(g._id).is_alive)

    def test_disable_genomes(self):

        self.db.find_one_by_id = lambda x, y: Transformator.Transformator.encode_StorageGenome(StorageGenome())
        genomes = []
        for i in range(0, 10):
            genomes.append(self.db.find_one_by_id(i, ObjectId()))
        self.genome_repository.update_genomes = lambda x: x

        for i in self.genome_repository.disable_genomes(genomes):
            self.assertFalse(i.is_alive)

    def test_updateGenomeFitness(self):
        genome = StorageGenome()
        genome.fitness = 1.0

        self.genome_repository.get_genome_by_id = lambda x: genome
        self.genome_repository.update_genome = lambda x: x
        self.assertEqual(Fraction(2.0), self.genome_repository.update_genome_fitness(genome._id, Fraction(2.0)).fitness)

    def test_updateGenomesFitness(self):
        genomes = []
        for i in range(0, 10):
            g = StorageGenome()
            g.fitness = float(1 / (i + 2))
            genomes.append((g, 4.7))
        self.genome_repository.get_genome_by_id = lambda x: x
        self.genome_repository.update_genomes = lambda x: x
        for i in self.genome_repository.update_genomes_fitness(genomes):
            self.assertEqual(4.7, i.fitness)
