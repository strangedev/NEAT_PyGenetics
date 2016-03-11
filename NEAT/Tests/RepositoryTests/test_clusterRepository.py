from unittest import TestCase
from unittest.mock import MagicMock

from NEAT.Analyst.Cluster import Cluster
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository import Transformator
from NEAT.Repository.ClusterRepository import ClusterRepository


class TestClusterRepository(TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.cluster_repository = ClusterRepository(self.db)

    def test_get_current_clusters(self):
        self.db.find_many = MagicMock(return_value=[{}, {}, {}, {}])
        self.assertListEqual([None, None, None, None], self.cluster_repository.get_current_clusters())

    def test_add_cluster_with_representative(self):
        genome = StorageGenome()
        self.db.insert_one = lambda x, y: y

        self.assertEqual(
            genome._id,
            Transformator.Transformator.decode_Cluster(
                self.cluster_repository.add_cluster_with_representative(genome._id)).representative
        )

    def test_archive_cluster(self):
        self.db.find_one_by_id = lambda x, y: y
        self.db.update_one = lambda x, y, z: z
        cluster = Cluster()
        genome = StorageGenome()
        cluster.representative = genome
        cluster.alive = True
        encode = Transformator.Transformator.encode_Cluster(cluster)
        decode = Transformator.Transformator.decode_Cluster(self.cluster_repository.archive_cluster(encode))
        self.assertFalse(decode.alive)

    def test_get_cluster_by_representative(self):
        cluster = Cluster()
        self.db.find_one = MagicMock(return_value=Transformator.Transformator.encode_Cluster(cluster))
        storage_genome = StorageGenome()
        self.assertEqual(cluster, self.cluster_repository.get_cluster_by_representative(storage_genome._id))

    def test_get_cluster_count(self):
        self.db.find_many = MagicMock(return_value=[Transformator.Transformator.encode_Cluster(Cluster()),
                                                    Transformator.Transformator.encode_Cluster(Cluster()),
                                                    Transformator.Transformator.encode_Cluster(Cluster())
                                                    ])
        self.assertEqual(3, self.cluster_repository.get_cluster_count())
