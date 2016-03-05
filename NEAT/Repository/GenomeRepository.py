from typing import Iterable

from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.Transformator import *


class GenomeRepository(object):
    def __init__(self, database_connector: DatabaseConnector) -> None:
        """

        :param database_connector: Database using
        :return: GenomeRepository
        """
        self._database_connector = database_connector

    def get_new_genome(self) -> StorageGenome:
        """

        :return: StorageGenome new StorageGenome
        """
        storage_genome = StorageGenome()
        return storage_genome

    def get_current_population(self) -> Iterable[StorageGenome]:
        """

        :return: Iterable[StorageGenomes] which are alive
        """
        o = self._database_connector.find_many("genomes", {"is_alive": True})
        genomes = []
        for genome in o:
            genomes.append(decode_StorageGenome(genome))
        return genomes

    def get_genome_by_id(self, genome_id: ObjectId) -> StorageGenome:
        """

        :param genome_id: ObjectId genome_id from genome to find
        :return: StorageGenome of given genome_id
        """
        o = self._database_connector.find_one_by_id("genomes", genome_id)
        return decode_StorageGenome(o)

    def get_genomes_in_cluster(self, cluster_id: ObjectId) \
            -> Iterable[StorageGenome]:
        """

        :param cluster_id: ObjectID cluster_id from Cluster
        :return: Iterable[StorageGenome] from Cluster
        """
        g = self._database_connector.find_many("genomes", {"cluster": cluster_id})
        genomes = []
        for genome in g:
            genomes.append(decode_StorageGenome(genome))
        return genomes

    def insert_genome(self, genome: StorageGenome) -> None:
        """

        :param genome: StorageGenome to insert
        :return:
        """
        i = encode_StorageGenome(genome)
        self._database_connector.insert_one("genomes", i)

    def insert_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        """

        :param genomes: Iterable[Genome] to insert
        :return:
        """
        g = []
        for i in genomes:
            g.append(encode_StorageGenome(i))
        self._database_connector.insert_many("genomes", g)

    def update_genome(self, genome: StorageGenome) -> None:
        """

        :param genome: StorageGenome to update in DB
        :return:
        """
        doc = encode_StorageGenome(genome)
        self._database_connector.update_one("genomes", genome._id, doc)

    def update_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        """

        :param genomes: Iterable[StorageGenome] to update in DB
        :return:
        """
        g = []
        for genome in genomes:
            g.append((genome._id), encode_StorageGenome(genome))
        self._database_connector.update_many("genomes", g)
