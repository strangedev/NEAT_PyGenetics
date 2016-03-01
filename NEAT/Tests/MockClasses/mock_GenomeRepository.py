from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome

class mock_GenomeRepository(object):

    def __init__(self):

        self.mock_population = []

        genome_one = StorageGenome()
        genome_one.id = 1
        genome_one.fitness = 0.5
        genome_one.genes = [

            (1, True, 0.5),
            (2, True, 0.5),
            (3, True, 0.5),
            (4, True, 0.5)

        ]

        genome_two = StorageGenome()
        genome_two.id = 2
        genome_two.fitness = 0.7
        genome_two.genes = [

            (1, True, 0.5),
            (3, True, 1),
            (4, True, 0),
            (5, True, 0.5)

        ]

        self.mock_population.append(genome_one)
        self.mock_population.append(genome_two)

    def get_current_population(self):

        return self.mock_population

    def update_cluster_for_genome(self, genome_id, cluster_id):

        # print("Genome ", genome_id, " is now in cluster ", cluster_id)

        for genome in self.mock_population:

            if genome.id == genome_id:

                genome.cluster = cluster_id

                break

    def get_genome_by_id(self, genome_id):

        for genome in self.mock_population:

            if genome.id == genome_id:

                return genome

    def get_genomes_in_cluster(self, cluster_id):

        genomes_in_cluster = []

        for genome in self.mock_population:

            if genome.cluster == cluster_id:

                genomes_in_cluster.append(genome)

        return genomes_in_cluster
