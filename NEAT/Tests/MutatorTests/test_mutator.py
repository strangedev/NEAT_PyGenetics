from unittest import TestCase
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.GenomeStructures.AnalysisStructure.AnalysisGenome import AnalysisGenome
from NEAT.Generator.Mutator import Mutator
from unittest.mock import MagicMock

class TestMutator(TestCase):

    def setUp(self):

        self.gene_repo = MagicMock()

        endpoints_for_id = {
            0: (1, 2),
            1: (1, 3),
            2: (2, 1),
            3: (3, 2),
            4: (2, 3),
            5: (2, 2),
            6: (3, 3),
            7: (3, 1),
            8: (1, 1),
            11: (1, 4),
            21: (4, 2)
        }
        id_for_endpoints = {v: k for k, v in endpoints_for_id.items()}

        self.gene_repo.find_connecting_nodes = (lambda h, t: [4])
        self.gene_repo.get_node_labels_by_gene_id = (lambda id: endpoints_for_id[id])
        self.gene_repo.get_gene_id_for_endpoints = (lambda h, t:  id_for_endpoints[(h, t)])
        self.gene_repo.get_next_node_label = (lambda : 4)

        self.genome = StorageGenome()
        self.genome.inputs = {
            "1": 1
        }
        self.genome.outputs = {
            "2": 2,
            "3": 3
        }
        self.genome.genes = {
            0: (True, 0.745)
        }
        self.genome_ana = AnalysisGenome(self.gene_repo, self.genome)

        mutation_parameters = dict(
            {
                "add_edge_probability": 0.5,
                "new_gene_enabled_probability": 0.7,
                "perturb_gene_weight_probability": 1
            }
        )

        self.mutator = Mutator(self.gene_repo, mutation_parameters)

    def test_mutate_genome(self):

        new_genome = self.mutator.mutate_genome(self.genome)
        self.assertNotEqual(
            new_genome.genes,
            self.genome.genes,
            "Mutation din't change the genome."
        )

    def test_mutate_add_edge(self):

        new_genome = self.mutator.mutate_add_edge(self.genome_ana, self.genome)

        differing_genes = [gid for gid in new_genome.genes.keys() \
                           if gid not in self.genome.genes.keys()]

        self.assertEqual(len(differing_genes), 1)
        print("added edge: ", differing_genes)

    def test_mutate_add_node(self):

        new_genome = self.mutator.mutate_add_node(self.genome_ana, self.genome)

        differing_genes = [gid for gid in new_genome.genes.keys() \
                           if gid not in self.genome.genes.keys()]

        self.assertEqual(len(differing_genes), 2)
        self.assertListEqual(
            differing_genes,
            [11, 21]
        )
        self.assertEqual(
            new_genome.genes[0][0],
            False,
            "The replaced gene hasn't been disabled."
        )

    def test_mutate_perturb_weights(self):

        new_genome = self.mutator.mutate_perturb_weights(self.genome)

        print(new_genome.genes)

        self.assertNotEqual(
            new_genome.genes[0][1],
            self.genome.genes[0][1],
            "mutate_perturb_weights() didn't change gene weights in genome."
        )


    def test_perturb_weight(self):

         gene = (True, 0.1337)
         perturbed_gene = self.mutator.perturb_weight(gene)

         self.assertNotEqual(
             gene[1],
             perturbed_gene[1],
             "Gene weight did not change."
         )
