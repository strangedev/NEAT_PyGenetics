from Entities.Creatures import Creature
from Entities.Creatures import Mouse


class Cat(Creature.Creature):

    """docstring for Cat"""

    def __init__(self):

        super().__init__()

        self._symbol = "C"
        self.food_sources = [Mouse.Mouse]
        self.max_starving = 30
        self.offspring_cycle = 45
        self.max_age = 75
