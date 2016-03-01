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
        pass

    def get_genome_by_id(self, genome_id: ObjectId) -> StorageGenome:
        pass

    def get_genomes_in_cluster(self, cluster_id: ObjectId) \
            -> Iterable[StorageGenome]:
        pass

    def insert_genome(self, genome: StorageGenome) -> None:
        pass

    def insert_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        pass

    def update_genome(self, genome: StorageGenome) -> None:
        pass

    def update_genomes(self, genomes: Iterable[StorageGenome]) -> None:
        pass
