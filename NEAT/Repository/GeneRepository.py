from NEAT.Repository.DatabaseConnector import DatabaseConnector
import itertools


class GeneRepository(object):

    def __init__(self, database_connector: DatabaseConnector) -> None:
        self._database_connector = database_connector

    def get_gene_id_for_endpoints(self, head_node_id, tail_node_id):
        gene = self._database_connector.find_one(
            "genes",
            {
                "head": head_node_id,
                "tail": tail_node_id
            }
        )

        if gene:
            gene_id = gene["_id"]
        else:
            gene_id = self._database_connector.insert_one(
                "genes",
                {
                    "head": head_node_id,
                    "tail": tail_node_id
                }
            )

        return gene_id

    def find_connecting_nodes(self, head_node_id, tail_node_id):

        # TODO: Figure out a more efficient algo then brute force

        head_edge_candidates = self._database_connector.find_many(
            "genes",
            {
                "head": head_node_id
            }
        )
        tail_edge_candidates = self._database_connector.find_many(
            "genes",
            {
                "tail": tail_node_id
            }
        )

        edge_pairs = list(
            itertools.product(
                head_edge_candidates,
                tail_edge_candidates
            )
        )

        connection_candidates = [pair
                                 for pair in edge_pairs
                                 if pair[0]["tail"] == pair[1]["head"]]

        connecting_nodes = [pair[0]["tail"] for pair in connection_candidates]

        return connecting_nodes

    def get_next_node_label(self):

        label_tracker = self._database_connector.find_one("node_label_tracker", None)

        if label_tracker:
            next_label = label_tracker["next_label"]
            new_label = next_label + 1
            self._database_connector.update_one(
                "node_label_tracker",
                label_tracker["_id"],
                {
                    "next_label": new_label
                }
            )
        else:
            next_label = 0
            new_label = next_label + 1
            self._database_connector.insert_one(
                "node_label_tracker",
                {
                    "next_label": new_label
                }
            )

        return next_label

    def get_node_labels_by_gene_id(self, gene_id):

        gene = self._database_connector.find_one_by_id("genes", gene_id)
        if gene:
            return gene["head"], gene["tail"]
        else:
            return None, None
