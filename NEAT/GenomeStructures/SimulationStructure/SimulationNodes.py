class Node(object):
    def __init__(self) -> None:
        pass

    def add_successor(self,
                      successor_node: 'Node',
                      weight: float
                      ) -> None:
        pass

    def fire(self) -> None:
        pass

    def reset(self) -> None:
        pass


class CycleNode(Node):
    def fire_cycles(self) -> None:
        pass
