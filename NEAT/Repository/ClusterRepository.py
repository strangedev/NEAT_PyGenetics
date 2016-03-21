from typing import List
from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.Transformator import Transformator
from NEAT.GenomeStructures.StorageStructure import StorageGenome
from NEAT.Analyst.Cluster import Cluster
from bson import ObjectId

class ClusterRepository(object):

    def __init__(self, database_connector: DatabaseConnector):
        self._database_connector = database_connector

    def get_current_clusters(self) -> List[Cluster]:
        clusters = self._database_connector.find_many(
            "clusters",
            {
                "alive": True
            }
        )
        return [Transformator.decode_Cluster(c) for c in clusters]

    def add_cluster_with_representative(
            self,
            genome_id: ObjectId
    ) -> ObjectId:
        cluster = Cluster()
        cluster.representative = genome_id
        return self._database_connector.insert_one(
            "clusters",
            Transformator.encode_Cluster(cluster)
        )

    def archive_cluster(self, cluster_id: ObjectId) -> dict:
        cluster = Transformator.decode_Cluster(
            self._database_connector.find_one_by_id(
                "clusters",
                cluster_id
            )
        )
        cluster.alive = False
        return self._database_connector.update_one(
            "clusters",
            cluster_id,
            Transformator.encode_Cluster(
                cluster
            )
        )

    def get_cluster_by_representative(self, genome_id: ObjectId):
        cluster = Transformator.decode_Cluster(
            self._database_connector.find_one(
                "clusters",
                {
                    "representative": genome_id
                }
            )
        )
        return cluster

    def get_cluster_count(self) -> int:
        clusters = self.get_current_clusters()
        return len(clusters)

    def update_offspring_for_cluster(
            self,
            cluster_id: ObjectId,
            cluster_offspring: int
    ):
        cluster = Transformator.decode_Cluster(
            self._database_connector.find_one_by_id(
                "clusters",
                cluster_id
            )
        )
        cluster.offspring = cluster_offspring
        return self._database_connector.update_one(
            "clusters",
            cluster_id,
            Transformator.encode_Cluster(
                cluster
            )
        )

    def update_fitness_for_cluster(
            self,
            cluster_id: ObjectId,
            cluster_fitness: float
    ):
        cluster = Transformator.decode_Cluster(
            self._database_connector.find_one_by_id(
                "clusters",
                cluster_id
            )
        )
        cluster.offspring = cluster_fitness
        return self._database_connector.update_one(
            "clusters",
            cluster_id,
            Transformator.encode_Cluster(
                cluster
            )
        )

    def update_max_population_for_cluster(
            self,
            cluster_id: ObjectId,
            cluster_max_population: int
    ):
        cluster = Transformator.decode_Cluster(
            self._database_connector.find_one_by_id(
                "clusters",
                cluster_id
            )
        )
        cluster.offspring = cluster_max_population
        return self._database_connector.update_one(
            "clusters",
            cluster_id,
            Transformator.encode_Cluster(
                cluster
            )
        )