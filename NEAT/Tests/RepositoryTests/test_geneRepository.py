from unittest import TestCase
from NEAT.Repository.GeneRepository import GeneRepository
from NEAT.Tests.MockClasses.mock_DatabaseConnector import mock_DatabaseConnector


class TestGeneRepository(TestCase):
    def test_get_gene_id_for_endpoints(self):
        self.fail()

    def test_find_connecting_nodes(self):

        con = mock_DatabaseConnector()
        con.insert_many(
            "genes",
            [
                {"head": 1, "tail": 2},
                {"head": 1, "tail": 3},
                {"head": 3, "tail": 2},
                {"head": 1, "tail": 4},
                {"head": 4, "tail": 3},
                {"head": 5, "tail": 2}
            ]
        )
        gene_repo = GeneRepository(con)

        connecting_nodes = gene_repo.find_connecting_nodes(1, 2)

        self.assertListEqual(
            connecting_nodes,
            [3],
            "GeneRepository didn't find the right connecting nodes."
        )

    def test_get_next_node_label(self):
        self.fail()

    def test_get_node_labels_by_gene_id(self):
        self.fail()
