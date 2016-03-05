from unittest import TestCase, mock
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Generator.Breeder import Breeder
from fractions import Fraction

class TestBreeder(TestCase):

    def setUp(self):

        breeding_conf = dict(
            {
                "fitness_difference_threshold": 1,
                "inherit_randomly_if_same_fitness_probability": 0.5,
                "gene_inherited_as_disabled_probability": 0.5
            }
        )

        self.breeder = Breeder(breeding_conf)

    def test_breed_genomes(self):

        fitter_genome = StorageGenome()
        fitter_genome.fitness = 22.74
        fitter_genome.genes = {

            0: (True, Fraction(0.21)),
            1: (True, Fraction(-0.56)),
            2: (True, Fraction(0.354)),
            3: (True, Fraction(0.98)),
            7: (True, Fraction(0.47)),
            8: (True, Fraction(-0.13))

        }

        other_genome = StorageGenome()
        other_genome.fitness = 19.233
        other_genome.genes = {

            0: (True, Fraction(0.1)),
            1: (True, Fraction(0.1)),
            2: (True, Fraction(0.1)),
            4: (True, Fraction(0.1)),
            5: (True, Fraction(-0.1)),
            6: (True, Fraction(-0.1))

        }

        similar_genome = StorageGenome()
        similar_genome.fitness = 21.83
        similar_genome.genes = {

            0: (True, Fraction(0.1)),
            1: (True, Fraction(0.1)),
            2: (True, Fraction(0.1)),
            4: (True, Fraction(0.1)),
            5: (True, Fraction(-0.1)),
            6: (True, Fraction(-0.1))

        }

        new_genome = self.breeder.breed_genomes(
            fitter_genome,
            other_genome
        )

        new_genome_two = self.breeder.breed_genomes(
            fitter_genome,
            similar_genome
        )

        # print(new_genome.genes) # TODO: proper testing
        # self.fail("Not implemented.")

        self.assertListEqual(
            list(new_genome.genes.keys()),
            [0, 1, 2, 3, 7, 8],
            "The wrong genes were inherited by breed_genomes()."
        )

        self.assertEqual(
            new_genome.genes[3][1],
            0.98,
            "The differing gene with id 3 wasn't inherited correctly by breed_genomes()."
        )

        self.assertEqual(
            new_genome.genes[7][1],
            0.47,
            "The differing gene with id 3 wasn't inherited correctly by breed_genomes()."
        )

        self.assertEqual(
            new_genome.genes[8][1],
            -0.13,
            "The differing gene with id 3 wasn't inherited correctly by breed_genomes()."
        )


        in_set = [(g in new_genome_two.genes.keys()) for g in [0, 1, 2]]
        self.assertTrue(
           lambda : not False in in_set
        )

        differing_genes = [g for g in new_genome_two.genes.keys() if (g not in [0, 1, 2])]
        for gene_id in differing_genes:

            weight = new_genome_two.genes[gene_id][1]

            parent_genome = fitter_genome \
                if gene_id in fitter_genome.genes.keys() \
                else similar_genome

            original_weight = parent_genome.genes[gene_id][1]

            self.assertEqual(
                weight,
                original_weight
            )