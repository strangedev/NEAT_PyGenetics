from unittest import TestCase, mock
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Generator.Breeder import Breeder
from fractions import Fraction

class TestBreeder(TestCase):

    def setUp(self):

        breeding_conf = dict(
            {
                "fitness_difference_threshold": 1
            }
        )

        self.breeder = Breeder(breeding_conf)

    def test_breed_genomes(self):

        fitter_genome = StorageGenome()
        fitter_genome.fitness = 22.74
        fitter_genome.genes = [

            (0, True, Fraction(0.21)),
            (1, True, Fraction(-0.56)),
            (2, True, Fraction(0.354)),
            (6, True, Fraction(0.98)),
            (8, True, Fraction(0.47)),
            (10, True, Fraction(-0.13))

        ]

        other_genome = StorageGenome()
        other_genome.fitness = 25
        other_genome.genes = [

            (3, True, Fraction(0.1)),
            (4, True, Fraction(0.1)),
            (5, True, Fraction(0.1)),
            (7, True, Fraction(0.1)),
            (9, True, Fraction(-0.1)),
            (11, True, Fraction(-0.1))

        ]

        new_genome = self.breeder.breed_genomes(
            fitter_genome,
            other_genome
        )

        print(new_genome) # TODO: proper testing