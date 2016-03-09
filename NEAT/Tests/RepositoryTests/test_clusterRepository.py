from unittest import TestCase
from unittest.mock import MagicMock

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.ClusterRepository import ClusterRepository


class TestClusterRepository(TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.cluster_repository = ClusterRepository(self.db)

    def test_get_current_clusters(self):
        self.db.find_many = MagicMock(return_value= [{},{},{},{}])
        self.assertListEqual([None,None,None,None], self.cluster_repository.get_current_clusters())

    def test_add_cluster_with_representative(self):
        genome = StorageGenome()
        self.fail()

    def test_archive_cluster(self):
        self.fail()

    def test_get_cluster_by_representative(self):
        self.fail()

    def test_get_cluster_count(self):
        self.fail()
