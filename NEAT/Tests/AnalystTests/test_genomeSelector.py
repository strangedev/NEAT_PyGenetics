from unittest import TestCase

from bson import ObjectId

from NEAT.Analyst.GenomeSelector import GenomeSelector
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Tests.MockClasses.mock_ClusterRepository import mock_ClusterRepository
from NEAT.Tests.MockClasses.mock_GenomeRepository import mock_GenomeRepository

class test_genomeSelector(TestCase):
    def test_selectGenomesForDiscarding_and_selectClusterForDiscarding(self):
        """
        checks if 20% of worst cluster or genomes were selected
        :return:
        """
        self.mock_genome_repository = mock_GenomeRepository()
        self.mock_cluster_repository = mock_ClusterRepository()

        self.mock_selection_parameters = {"discarding_by_genome_fitness": 0.2,
                                          "discarding_by_cluster_fitness": 0.2}

        genomes_from_all_cluster = []
        cluster = []
        self.mock_genome_repository.mock_population = []

        for i in range(0, 10):
            self.mock_cluster_repository.add_cluster_with_representative(ObjectId(str(i).rjust(24, "0")))
            test_genome = []

            for j in range(0,10):
                storage_genome = StorageGenome()
                storage_genome._id = ObjectId(str(j + 10*i).rjust(24, "0"))
                storage_genome.fitness = j
                self.mock_genome_repository.mock_population.append(storage_genome)
                self.mock_genome_repository.update_cluster_for_genome(ObjectId(str(j+(10*i)).rjust(24, "0")), ObjectId(str(i).rjust(24, "0")))
                if j <= 1:
                    test_genome.append(storage_genome)

            if i <= 1:
                cluster.append(self.mock_cluster_repository.get_cluster_by_representative(ObjectId(str(i).rjust(24, "0"))))

            self.mock_cluster_repository.update_fitness_for_cluster(ObjectId(str(i).rjust(24, "0")), i)
            genomes_from_all_cluster.extend(test_genome)

        genome_selector = GenomeSelector(
            self.mock_genome_repository,
            self.mock_cluster_repository,
            self.mock_selection_parameters
        )

        self.assertListEqual(cluster, genome_selector.select_clusters_for_discarding())
        self.assertListEqual(genomes_from_all_cluster, genome_selector.select_genomes_for_discarding())

