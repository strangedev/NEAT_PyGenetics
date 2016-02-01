from Entities.Creatures import Creature
from Entities.Creatures import Mouse


class ZombieMouse(Creature.Creature):

    """docstring for ZombieMouse"""

    def __init__(self):

        super().__init__()

        self._symbol = "W"
        self.food_sources = [Mouse.Mouse]

    def perform_action():

        super().perform_action()

        self.age = 0
        self.offspring_cycle = 0

        pass
