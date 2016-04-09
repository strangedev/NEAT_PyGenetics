from typing import Iterable, Tuple, List

from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.Transformator import *


class GenomeRepository(object):
    def __init__(self, database_connector: DatabaseConnector) -> None:
        """

        :param database_connector: Database using
        :return: GenomeRepository
        """
        self._database_connector = database_connector

    @staticmethod
    def get_new_genome() -> StorageGenome:
        """

        :return: StorageGenome new StorageGenome
        """
        storage_genome = StorageGenome()
        return storage_genome

    def get_current_population(self) -> Iterable[StorageGenome]:
        """

        :return: Iterable[StorageGenomes] which are alive
        """
        genomes_alive = self._database_connector.find_many(
            "genomes",
            {
                "is_alive": True
            }
        )
        genomes = []
        for genome in genomes_alive:
            genomes.append(Transformator.decode_StorageGenome(genome))
        return genomes

    def get_genome_by_id(self, genome_id: ObjectId) -> StorageGenome:
        """

        :param genome_id: ObjectId genome_id from genome to find
        :return: StorageGenome of given genome_id
        """
        genome_encoded = self._database_connector.find_one_by_id(
            "genomes",
            genome_id
        )
        return Transformator.decode_StorageGenome(genome_encoded)

    def get_genomes_in_cluster(self, cluster_id: ObjectId) \
            -> Iterable[StorageGenome]:
        """

        :param cluster_id: ObjectID cluster_id from Cluster
        :return: Iterable[StorageGenome] from Cluster
        """
        genomes_in_cluster = self._database_connector.find_many(
            "genomes",
            {
                "cluster": cluster_id
            }
        )
        genomes = []
        for genome in genomes_in_cluster:
            genomes.append(Transformator.decode_StorageGenome(genome))
        return genomes

    def insert_genome(self, genome: StorageGenome) -> None:
        """

        :param genome: StorageGenome to insert
        :return:
        """
        genome_encoded = Transformator.encode_StorageGenome(genome)
        return self._database_connector.insert_one(
            "genomes",
            genome_encoded
        )

    def insert_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        """

        :param genomes: Iterable[Genome] to insert
        :return:
        """
        genomes_to_insert = []
        for genome in genomes:
            genomes_to_insert.append(
                Transformator.encode_StorageGenome(
                    genome
                )
            )
        return self._database_connector.insert_many(
            "genomes",
            genomes_to_insert
        )

    def update_genome(self, genome: StorageGenome) -> dict:
        """

        :param genome: StorageGenome to update in DB
        :return: information about update process (from mongoDB)
        """
        genome_encoded = Transformator.encode_StorageGenome(genome)
        return self._database_connector.update_one(
            "genomes",
            genome.genome_id,
            genome_encoded
        )

    def update_genomes(self, genomes: Iterable[StorageGenome]) -> dict:
        """

        :param genomes: Iterable[StorageGenome] to update in DB
        :return: information about update process (from mongoDB)
        """
        result = []
        for genome in genomes:
            result.append(
                self.update_genome(genome)
            )
        return result

    def disable_genome(self, genome_id: ObjectId) -> dict:
        """

        :param genome_id: ObjectId from genome to disable
        :return:
        """
        genome = self.get_genome_by_id(genome_id)
        genome.is_alive = False
        return self.update_genome(genome)

    def disable_genomes(self, genomes_id: [ObjectId]) -> [dict]:
        """

        :param genomes_id: [ObjectId] from genomes to disable
        :return: [dict] information about update process (from mongoDB)
        """
        result = []
        for genome_id in genomes_id:
            genome = self.get_genome_by_id(genome_id)
            genome.is_alive = False
            result.append(genome)
        return self.update_genomes(result)

    def update_genome_fitness(self, genome_id: ObjectId, fitness: float) -> dict:
        """

        :param genome_id: ObjectId from genomes to update fitness
        :param fitness: Fraction to set
        :return: dict information about update process (from mongoDB)
        """
        genome = self.get_genome_by_id(genome_id)
        genome.fitness = fitness
        return self.update_genome(genome)

    def update_genomes_fitness(self, genome_fitness: List[Tuple[ObjectId, float]]) -> dict:
        """

        :param genome_fitness: List[Tuple[ObjectId, Fraction]] genome_id and fitness to update
        :return: [dict] information about update process (from mongoDB)
        """
        result = []
        for genome_id, fitness in genome_fitness:
            genome = self.get_genome_by_id(genome_id)
            genome.fitness = fitness
            result.append(genome)
        return self.update_genomes(result)

    def update_genome_cluster(
            self,
            genome_id: ObjectId,
            cluster_id: ObjectId
    ):
        """

        :param genome_id: The ObjectId of the genome to update
        :param cluster_id: The new cluster of the genome as ObjectId
        :return: dict information about update process (from mongodb)
        """
        genome = self.get_genome_by_id(genome_id)
        genome.cluster = cluster_id
        return self.update_genome(genome)
