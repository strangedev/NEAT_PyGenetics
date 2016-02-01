from Entities.Creatures import Creature
from Entities.Creatures import Cat
from Entities.Creatures import Mouse
from Entities.Plants import Corn


class JohnCena(Creature.Creature):

    """docstring for JohnCena"""

    def __init__(self):

        super().__init__()

        self._symbol = "J"
        self.food_sources = [Cat.Cat, Mouse.Mouse, Corn.Corn]
        self.max_starving = 400
        self.offspring_cycle = 8000
        self.max_age = 4000
