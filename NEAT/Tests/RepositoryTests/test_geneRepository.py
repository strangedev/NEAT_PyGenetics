from unittest import TestCase
from NEAT.Repository.GeneRepository import GeneRepository
from NEAT.Tests.MockClasses.mock_DatabaseConnector import mock_DatabaseConnector


class TestGeneRepository(TestCase):
    def test_get_gene_id_for_endpoints(self):

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

        gene_id = gene_repo.get_gene_id_for_endpoints(1, 2)
        self.assertEqual(
            gene_id,
            0,
            "The GeneRepository didn't find the appropriate gene_id for endpoints."
        )

        gene_id = gene_repo.get_gene_id_for_endpoints(3, 2)
        self.assertEqual(
            gene_id,
            2,
            "The GeneRepository didn't find the appropriate gene_id for endpoints."
        )

        gene_id = gene_repo.get_gene_id_for_endpoints(4, 3)
        self.assertEqual(
            gene_id,
            4,
            "The GeneRepository didn't find the appropriate gene_id for endpoints."
        )

        gene_id = gene_repo.get_gene_id_for_endpoints(10, 20)
        self.assertEqual(
            gene_id,
            6,
            "The GeneRepository didn't find the appropriate gene_id for endpoints."
        )



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

        con = mock_DatabaseConnector()
        rep = GeneRepository(con)

        generated_labels = []

        for i in range(100):

            generated_labels.append(
                rep.get_next_node_label()
            )

        self.assertListEqual(
            generated_labels,
            list(range(100)),
            "The GeneRepository didn't generate the appropriate node labels."
        )

    def test_get_node_labels_by_gene_id(self):

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

        edge = gene_repo.get_node_labels_by_gene_id(0)
        self.assertTupleEqual(
            edge,
            (1, 2),
            "GeneRepository didn't find the appropriate endpoints for gene id."
        )

        edge = gene_repo.get_node_labels_by_gene_id(4)
        self.assertTupleEqual(
            edge,
            (4, 3),
            "GeneRepository didn't find the appropriate endpoints for gene id."
        )