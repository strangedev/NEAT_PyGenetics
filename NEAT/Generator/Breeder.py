import random
from typing import Dict

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


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

        random.seed()

        bigger_genome, smaller_genome = (genome_one, genome_two) \
            if len(genome_one.genes) > len(genome_two.genes) \
            else (genome_two, genome_one)

        bigger_genome_gene_ids = bigger_genome.genes.keys()
        smaller_genome_gene_ids = smaller_genome.genes.keys()

        all_gene_ids = list(smaller_genome_gene_ids) + list(bigger_genome_gene_ids)

        matching_gene_ids = [gene_id for gene_id in bigger_genome_gene_ids
                             if gene_id in smaller_genome_gene_ids]

        differing_gene_ids = [gene_id for gene_id in all_gene_ids
                              if gene_id not in matching_gene_ids]

        fitter_genome_table = genome_one.genes \
            if genome_one.fitness > genome_two.fitness \
            else genome_two.genes

        new_genome = StorageGenome()

        # Insert inherited matching genes.
        for gene_id in matching_gene_ids:
            parent_genome_table = random.choice(
                [
                    genome_one.genes,
                    genome_two.genes
                ]
            )
            gene_enabled = self.should_gene_be_enabled(
                genome_one.genes[gene_id],
                genome_two.genes[gene_id]
            )
            gene_weight = parent_genome_table[gene_id][1]

            new_genome.genes[gene_id] = (gene_enabled, gene_weight)

        # Insert inherited differing genes.
        if abs(genome_one.fitness - genome_two.fitness) > \
                self.breeding_parameters["fitness_difference_threshold"]:

            for gene_id in differing_gene_ids:

                if gene_id in fitter_genome_table.keys():
                    gene_enabled = self.should_gene_be_enabled(
                        fitter_genome_table[gene_id]
                    )
                    gene_weight = fitter_genome_table[gene_id][1]

                    new_genome.genes[gene_id] = (gene_enabled, gene_weight)

        else:

            for gene_id in differing_gene_ids:

                inherit_gene = True \
                    if random.random() < self.breeding_parameters[
                           "inherit_randomly_if_same_fitness_probability"
                       ] \
                    else False

                if inherit_gene:
                    parent_genome_table = genome_one.genes \
                        if gene_id in genome_one.genes.keys() \
                        else genome_two.genes

                    gene_enabled = self.should_gene_be_enabled(
                        parent_genome_table[gene_id]
                    )
                    gene_weight = parent_genome_table[gene_id][1]

                    new_genome.genes[gene_id] = (gene_enabled, gene_weight)

        return new_genome

    def should_gene_be_enabled(self, instance_one, instance_two=None):
        """
        Decides whether the inherited variant of a gene should be
        enabled in the offspring genome based on both parents' instances
        of the gene.
        :param instance_one: The first gene instance
        :param instance_two:  The second gene instance
        :return: Whether the inherited gene should be enabled
        """

        gene_one_enabled = instance_one[1]

        if not instance_two:
            gene_two_enabled = False
        else:
            gene_two_enabled = instance_two[1]

        if (not gene_one_enabled) or (not gene_two_enabled):
            return not random.random() < self.breeding_parameters[
                    "gene_inherited_as_disabled_probability"
            ]
