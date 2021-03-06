import random
from typing import Tuple

from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Utilities import ProbabilisticTools


class Mutator(object):
    def __init__(self, gene_repository, mutation_parameters):

        self.gene_repository = gene_repository
        self.mutation_parameters = mutation_parameters

    def mutate_genome(self, genome) -> StorageGenome:

        analysis_genome = AnalysisGenome(self.gene_repository, genome)

        if len(analysis_genome.edges) == 0:
            return self.mutate_add_edge(analysis_genome, genome)

        edge_or_vertex = ProbabilisticTools.weighted_choice(
            [
                (0, self.mutation_parameters["add_edge_probability"]),
                (1, 1 - self.mutation_parameters["add_edge_probability"])
            ]
        )

        if edge_or_vertex == 0:
            new_genome = self.mutate_add_edge(analysis_genome, genome)
        else:
            new_genome = self.mutate_add_node(analysis_genome, genome)

        return self.mutate_perturb_weights(new_genome)

    def mutate_add_edge(
            self,
            analysis_genome: AnalysisGenome,
            storage_genome: StorageGenome
    ) -> StorageGenome:

        random.seed()

        starting_vertex = random.choice(list(analysis_genome.nodes))

        if starting_vertex not in analysis_genome.edges.keys():
            # if the chosen vertex has no outgoing edges (i.e. is a sink), every
            # other vertex may be a possible endpoint
            possible_endpoints = list(analysis_genome.nodes)
        else:
            possible_endpoints = []
            for node in analysis_genome.nodes:
                for target_node, _ in analysis_genome.edges[starting_vertex]:
                    if node != target_node:
                        # if there is no edge from the selected node to the cur-
                        # rent node, it is a possible endpoint
                        possible_endpoints.append(node)

        endpoint = random.choice(possible_endpoints)

        gene_id = self.gene_repository.get_gene_id_for_endpoints(
            starting_vertex,
            endpoint
        )
        gene_weight = random.random()
        gene_enabled = ProbabilisticTools.weighted_choice(
            [
                (True, self.mutation_parameters["new_gene_enabled_probability"]),
                (False, 1 - self.mutation_parameters["new_gene_enabled_probability"])
            ]
        )

        new_genome = StorageGenome(storage_genome)
        new_genome.genes[gene_id] = (gene_enabled, gene_weight)

        return new_genome

    def mutate_add_node(
            self,
            analysis_genome: AnalysisGenome,
            storage_genome: StorageGenome
    ) -> StorageGenome:

        random.seed()

        starting_vertex = random.choice(list(analysis_genome.edges.keys()))
        endpoint, _ = random.choice(list(analysis_genome.edges[starting_vertex]))

        old_gene_id = self.gene_repository.get_gene_id_for_endpoints(
            starting_vertex,
            endpoint
        )

        old_gene = storage_genome.genes[old_gene_id]

        # try to find an existing gene from the repository first
        # if a matching gene that connects start -> new vertex
        # and new_vertex -> end is not found, we'll ask gene repository for a new one.

        connecting_nodes = self.gene_repository.find_connecting_nodes(
            starting_vertex,
            endpoint
        )

        connecting_node = None

        for node in connecting_nodes:

            if node not in analysis_genome.nodes:
                connecting_node = node
                break
            else:
                connecting_node = self.gene_repository.get_next_node_label()

        new_gene_one_id = self.gene_repository.get_gene_id_for_endpoints(
            starting_vertex,
            connecting_node
        )
        new_gene_one_weight = old_gene[1]
        new_gene_one = (True, new_gene_one_weight)

        new_gene_two_id = self.gene_repository.get_gene_id_for_endpoints(
            connecting_node,
            endpoint
        )
        new_gene_two = (True, 1.0)

        new_genome = StorageGenome(storage_genome)

        for gid, gene in new_genome.genes.items():
            if gid == old_gene_id:
                new_genome.genes[gid] = (False, gene[1])
                break

        new_genome.genes[new_gene_one_id] = new_gene_one
        new_genome.genes[new_gene_two_id] = new_gene_two

        return new_genome

    def mutate_perturb_weights(self, genome: StorageGenome) -> StorageGenome:

        random.seed()

        new_genome = StorageGenome(genome)

        for gid, gene in genome.genes.items():
            perturb_weight = random.random() < self.mutation_parameters[
                "perturb_gene_weight_probability"
            ]
            if perturb_weight:
                new_gene = self.perturb_weight(gene)
                genome.genes[gid] = new_gene

        return new_genome

    @staticmethod
    def perturb_weight(
            gene: Tuple[bool, float]
    ) -> Tuple[bool, float]:

        random.seed()
        new_weight = gene[1] * random.random()
        return gene[0], new_weight
