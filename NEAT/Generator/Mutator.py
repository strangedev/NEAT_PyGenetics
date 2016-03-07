from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.GeneRepository import GeneRepository
from NEAT.Utilities import ProbabilisticTools
import random
import copy
from typing import Tuple
from fractions import Fraction

class Mutator(object):

    def __init__(self, gene_repository, mutation_parameters):

        self.gene_repository = gene_repository
        self.mutation_parameters = mutation_parameters

    def mutate_genome(self, genome) -> StorageGenome:
        if len(genome.genes) == 0:
            return self.mutate_add_edge(genome)

        edge_or_vertex = ProbabilisticTools.weighted_choice( # TODO:
            [
                (0, self.mutation_parameters["add_edge_probability"]),
                (1, 1 - self.mutation_parameters["add_edge_probability"])
            ]
        )

        if edge_or_vertex == 0:
            new_genome = self.mutate_add_edge(genome)
        else:
            new_genome = self.mutate_add_node(genome)

        return self.mutate_perturb_weights(new_genome)

    def mutate_add_edge(
            self,
            genome: StorageGenome
    ) -> StorageGenome:

        random.seed()

        input_nodes = [v for v in genome.inputs.values()]
        output_nodes = [v for v in genome.outputs.values()]
        gene_endpoints = []
        for gid in genome.genes.keys():
            h, t = self.gene_repository.get_node_labels_by_gene_id(gid)
            gene_endpoints.append(h)
            gene_endpoints.append(t)

        nodes = list(set(input_nodes
                    + output_nodes
                    + gene_endpoints))

        edges = {h: t for h, t in \
                 [self.gene_repository.get_node_labels_by_gene_id(gid) \
                  for gid in genome.genes.keys()]}

        starting_vertex = random.choice(list(nodes))

        if starting_vertex not in edges.keys():
            # if the chosen vertex has no outgoing edges (i.e. is a sink), every
            # other vertex may be a possible endpoint
            possible_endpoints = nodes
        else:
            possible_endpoints = \
                [node for node in nodes
                 if node not in edges[starting_vertex]]

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

        new_genome = copy.deepcopy(genome) # TODO: never deepcopy a StorageGenome. It WILL break the database because of the ObjectID. We need a copyconstructor.
        new_genome.genes[gene_id] = (gene_enabled, gene_weight)

        return new_genome

    def mutate_add_node(
            self,
            analysis_genome: AnalysisGenome,
            storage_genome: StorageGenome
    ) -> StorageGenome:

        random.seed()

        starting_vertex = random.choice(list(analysis_genome.edges.keys()))
        endpoint = random.choice(list(analysis_genome.edges[starting_vertex]))

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

            if not node in analysis_genome.nodes:
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

        new_genome = copy.deepcopy(storage_genome) # TODO: never deepcopy a StorageGenome. It WILL break the database because of the ObjectID. We need a copyconstructor.

        for gid, gene in new_genome.genes.items():
            if gid == old_gene_id:
                new_genome.genes[gid] = (False, gene[1])
                break

        new_genome.genes[new_gene_one_id] = new_gene_one
        new_genome.genes[new_gene_two_id] = new_gene_two

        return new_genome

    def mutate_perturb_weights(self, genome: StorageGenome) -> StorageGenome:

        random.seed()

        new_genome = copy.deepcopy(genome) # TODO: never deepcopy a StorageGenome. It WILL break the database because of the ObjectID. We need a copyconstructor.

        for gid, gene in genome.genes.items():
            perturb_weight = True \
                if random.random() < self.mutation_parameters["perturb_gene_weight_probability"] \
                else False

            if perturb_weight:
                new_gene = self.perturb_weight(gene)
                genome.genes[gid] = new_gene

        return new_genome

    def perturb_weight(
            self,
            gene: Tuple[bool, Fraction]
    ) -> Tuple[bool, Fraction]:

        random.seed()

        new_weight = Fraction(gene[1] * random.random())

        return (gene[0], new_weight)
