from typing import Dict, List, Iterable, Tuple


class Node(object):
    def __init__(self, initial_value: float = 0) -> None:
        """
        Successors are stored in a set to prevent adding the same successor mul-
        tiple times. Weights are stored separately and are accessed with the
        successor as the key.
        :param initial_value: Optional initial value. May or may not be over-
         written when starting a simulation-step.
        :return:
        """
        if initial_value < 0 or initial_value > 1:
            raise ValueError("SimulationNodes.Node's initial_value has to be "
                             .join("in the interval [0,1]."))
        self.successors = []  # type: List[Node]
        self.weights = {}  # type: Dict[Node, float]
        self.initial_value = initial_value
        self.value = initial_value

    def add_successor(self,
                      successor_node: 'Node',
                      weight: float
                      ) -> None:
        """
        Adds a successor_node to the list of stored successors.
        :param successor_node: A new node to be added as a successor
        :param weight: The weight of the edge to the new node
        :raises: ValueError, if the weight of the given nodes is not in the
        interval [0,1].
        :raises: Exception, if the given successor_node already exists in the
         stored list of successors.
        """
        if weight < 0 or weight > 1:
            raise ValueError("Successor weight has to be in the interval "
                             .join("[0,1]."))
        if successor_node not in self.successors:
            self.successors.append(successor_node)
            self.weights[successor_node] = weight
        else:
            raise Exception("The given successor_node "
                            .join(str(successor_node))
                            .join(" is already present in Node ")
                            .join(str(self)).join("."))

    def add_successors(self,
                       successor_nodes: Iterable[Tuple['Node', float]]) -> None:
        """
        Adds multiple successor_nodes to the list.
        :param successor_nodes:
        :raises: ValueError, if the weight of one of the given nodes is not in
         the interval [0,1].
        :raises: Exception, if one of the given nodes already exists in the
         stored list of successors.
        :return:
        """
        for successor_node, weight in successor_nodes:
            self.add_successor(successor_node, weight)

    def fire(self) -> None:
        """
        Adds the currently stored value multiplied with the specific weights
        to each successor.
        :return:
        """
        # TODO: Some sort of transformation function should be applied here, to
        # transform the stored value after it is complete and before advancing
        # in the simulation.
        for successor in self.successors:
            successor.add_value(self.value * self.weights[successor])

    def reset(self) -> None:
        """
        Resets the value to the initial_value.
        :return:
        """
        self.value = self.initial_value

    def add_value(self, value: float) -> None:
        """
        Adds the given value to the currently stored value.
        :param value: The value to be added.
        :return:
        """
        self.value += value


class CycleNode(Node):
    def __init__(self, initial_memory_value: float, initial_value: float = 0):
        """
        Unlike in Node here the initial_value is mandatory. It is used for the
        first step of firing the cycle edges.
        :param initial_value:
        :return:
        """
        super().__init__(initial_value)
        self.cycle_successors = []  # type: List[Node]
        self.cycle_weights = {}  # type: Dict[Node, float]
        self.memory_value = initial_memory_value

    def add_cycle_successor(self, successor_node: Node, weight: float) -> None:
        """
        Adds a cycle successor to the list. Throws an Exception otherwise.
        :param successor_node:
        :param weight:
        :raises: ValueError, if the weight of the given nodes is not in the
         interval [0,1].
        :raises: Exception, if the given successor_node already exists in the
         stored list of successors.
        :return:
        """
        if successor_node not in self.cycle_successors:
            self.cycle_successors.append(successor_node)
            self.cycle_weights[successor_node] = weight
        else:
            raise Exception("The given cycle_successor_node "
                            .join(str(successor_node))
                            .join(" is already present in CycleNode ")
                            .join(str(self)).join("."))

    def add_cycle_successors(
            self,
            successor_nodes: Iterable[Tuple[Node, float]]
    ) -> None:
        """
        Adds multiple successor_nodes to the list.
        :param successor_nodes:
        :raises: ValueError, if the weight of one of the given nodes is not in
         the interval [0,1].
        :raises: Exception, if one of the given nodes already exists in the
         stored list of successors.
        :return:
        """
        for successor_node, weight in successor_nodes:
            self.add_cycle_successor(successor_node, weight)

    def fire_cycles(self) -> None:
        """
        Adds the last stored value multiplied with the specific weights to all
        cycle closing successors.
        Serves as some kind of short time memory. (Use to be determined)
        :return:
        """
        for cycle_successor in self.cycle_successors:
            cycle_successor.add_value(
                self.memory_value * self.cycle_weights[cycle_successor]
            )

    def reset(self) -> None:
        self.memory_value = self.value
        self.value = self.initial_value
