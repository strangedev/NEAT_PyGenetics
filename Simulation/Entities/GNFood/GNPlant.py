"""
GNPlant Module
"""
from Entities import Thing


class GNPlant(Thing.Thing):

    """
    GNPlant class
    """

    def __init__(self):
        """
        """

        super().__init__()

        self.seed_cycle = 6

    def perform_action(self, world):

        super().perform_action()

        # if self.age % self.seed_cycle == 0:
        #   self._reproduce(world)
