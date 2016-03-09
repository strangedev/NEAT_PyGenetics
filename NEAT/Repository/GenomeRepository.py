from fractions import Fraction
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
        alive = self._database_connector.find_many("genomes", {"is_alive": True})
        genomes = []
        for genome in alive:
            genomes.append(Transformator.decode_StorageGenome(genome))
        return genomes

    def get_genome_by_id(self, genome_id: ObjectId) -> StorageGenome:
        """

        :param genome_id: ObjectId genome_id from genome to find
        :return: StorageGenome of given genome_id
        """
        o = self._database_connector.find_one_by_id("genomes", genome_id)
        return Transformator.decode_StorageGenome(o)

    def get_genomes_in_cluster(self, cluster_id: ObjectId) \
            -> Iterable[StorageGenome]:
        """

        :param cluster_id: ObjectID cluster_id from Cluster
        :return: Iterable[StorageGenome] from Cluster
        """
        g = self._database_connector.find_many("genomes", {"cluster": cluster_id})
        genomes = []
        for genome in g:
            genomes.append(Transformator.decode_StorageGenome(genome))
        return genomes

    def insert_genome(self, genome: StorageGenome) -> None:
        """

        :param genome: StorageGenome to insert
        :return:
        """
        i = Transformator.encode_StorageGenome(genome)
        return self._database_connector.insert_one("genomes", i)

    def insert_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        """

        :param genomes: Iterable[Genome] to insert
        :return:
        """
        g = []
        for i in genomes:
            g.append(Transformator.encode_StorageGenome(i))
        return self._database_connector.insert_many("genomes", g)

    def update_genome(self, genome: StorageGenome) -> dict:
        """

        :param genome: StorageGenome to update in DB
        :return: information about update process (from mongoDB)
        """
        doc = Transformator.encode_StorageGenome(genome)
        return self._database_connector.update_one("genomes", genome._id, doc)

    def update_genomes(self, genomes: Iterable[StorageGenome]) -> dict:
        """

        :param genomes: Iterable[StorageGenome] to update in DB
        :return: information about update process (from mongoDB)
        """
        g = []
        for genome in genomes:
            g.append(self._database_connector.find_one_by_id("genomes", genome._id))
        return self._database_connector.update_many("genomes", g)

    def disable_genome(self, genome_id: ObjectId) -> dict:
        """

        :param genome_id: ObjectId from genome to disable
        :return:
        """
        genome = self._database_connector.find_one_by_id(genome_id)
        genome.__setitem__('is_alive', False)
        return self._database_connector.update_one("genomes", genome_id, genome)

    def disable_genomes(self, genomes_id: [ObjectId]) -> [dict]:
        """

        :param genomes_id: [ObjectId] from genomes to disable
        :return: [dict] information about update process (from mongoDB)
        """
        result = []
        for genome_id in genomes_id:
            genome = self._database_connector.find_one_by_id(genome_id)
            genome.is_alive = False
            result.append(genome)
        return self.update_genomes(result)

    def update_genome_fitness(self, genome_id: ObjectId, fitness: Fraction) -> dict:
        """

        :param genome_id: ObjectId from genomes to update fitness
        :param fitness: Fraction to set
        :return: dict information about update process (from mongoDB)
        """
        genome = self._database_connector.find_one_by_id(genome_id)
        genome.fitness = fitness
        return self.update_genome(genome)

    def update_genomes_fitness(self, genome_fitness: List[Tuple[ObjectId, Fraction]]) -> dict:
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
