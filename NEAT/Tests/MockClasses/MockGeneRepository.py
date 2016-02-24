from typing import Tuple
from NEAT.Repository.GeneRepository import GeneRepository


class MockGeneRepository(GeneRepository):
    def get_node_ids_from_gene(self, gene_id: int) -> Tuple[int, int]:
        return (2 * gene_id), (2 * gene_id + 1)
