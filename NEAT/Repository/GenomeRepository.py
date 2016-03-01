from typing import Iterable, Union

from bson import ObjectId

from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class GenomeRepository(object):
    def __init__(self, database_connector: DatabaseConnector) -> None:
        self._database_connector = database_connector

    def get_new_genome(self) -> StorageGenome:
        storage_genome = StorageGenome()
        return storage_genome

    def get_current_population(self) -> Iterable[StorageGenome]:
        return self._database_connector.find_many("genomes", {"is_alive": True})

    def get_genome_by_id(self, genome_id: ObjectId) -> StorageGenome:
        return self._database_connector.find_one_by_id("genomes", genome_id)

    def get_genomes_in_cluster(self, cluster_id: ObjectId) \
            -> Iterable[StorageGenome]:
        return self._database_connector.find_many("genomes", {"cluster": cluster_id})

    def insert_genome(self, genome: StorageGenome) -> None:
        self._database_connector.insert_one("genomes", genome)

    def insert_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        self._database_connector.insert_many("genomes", genomes)

    def update_genome(self, genome: StorageGenome) -> None:
        self._database_connector.update_one("genomes", genome)

    def update_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        self._database_connector.update_many("genomes", genomes)
