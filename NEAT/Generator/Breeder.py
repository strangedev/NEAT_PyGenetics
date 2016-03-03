from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Utilities import ProbabilisticTools
from typing import Dict, Tuple, List
import random

class Breeder(object):

    def __init__(
            self,
            breeding_parameters: Dict[str, object]
    ) -> None:

        self.breeding_parameters = breeding_parameters


    def breed_genomes(
            self,
            genome_one: StorageGenome,
            genome_two: StorageGenome
    ) -> StorageGenome:
        """
        Generates a new genome based on two input genomes.
        Matching genes are inherited randomly from one of the
        parents. Differing genes are inherited from the fitter
        parent. If the fitness value difference is below
        fitness_difference_threshold, the differing genes are inherited
        randomly as well.

        :param genome_one:
        :param genome_two:
        :return:
        """

        # Distinction between bigger and smaller genome is made to
        # be able to distinguish between disjoint and excess genes
        # potentially needed for later approaches.

        bigger_genome, smaller_genome = (genome_one, genome_two) \
            if len(genome_one.genes) > len(genome_two.genes) \
            else (genome_two, genome_one)

        bigger_genome_gene_ids = [gene[0] for gene in bigger_genome.genes]
        smaller_genome_gene_ids = [gene[0] for gene in smaller_genome.genes]

        all_gene_ids = smaller_genome_gene_ids + bigger_genome_gene_ids

        matching_gene_ids = [gene_id for gene_id in bigger_genome_gene_ids \
                          if gene_id in smaller_genome_gene_ids]

        differing_gene_ids = [gene_id for gene_id in all_gene_ids \
                           if gene_id not in matching_gene_ids]

        # Gene tables are generated in order to perform fast lookup while breeding.
        # Oh my flying spaghetti monster, I love dict comprehensions.
        genome_one_table = {gene[0]: (gene[1], gene[2]) for gene in genome_one.genes}
        genome_two_table = {gene[0]: (gene[1], gene[2]) for gene in genome_two.genes}

        fitter_genome_table = genome_one_table \
            if genome_one.fitness > genome_two.fitness \
            else genome_two_table

        new_genome = StorageGenome()

        # Insert inherited matching genes.
        for gene_id in matching_gene_ids:

            parent_genome_table = random.choice(
                    [
                        genome_one_table,
                        genome_two_table
                    ]
                )
            gene_enabled = parent_genome_table[gene_id][0]
            gene_weight = parent_genome_table[gene_id][1]

            new_genome.genes.append((gene_id, gene_enabled, gene_weight))

        # Insert inherited differing genes.
        if abs(genome_one.fitness - genome_two.fitness) < \
                self.breeding_parameters["fitness_difference_threshold"]:


            for gene_id in differing_gene_ids:

                gene_enabled = fitter_genome_table[gene_id][0]
                gene_weight = fitter_genome_table[gene_id][1]
                
                new_genome.genes.append((gene_id, gene_enabled, gene_weight))

        else:

            for gene_id in differing_gene_ids:

                parent_genome_table = random.choice(
                    [
                        genome_one_table,
                        genome_two_table
                    ]
                )
                gene_enabled = parent_genome_table[gene_id][0]
                gene_weight = parent_genome_table[gene_id][1]

                new_genome.genes.append((gene_id, gene_enabled, gene_weight))



