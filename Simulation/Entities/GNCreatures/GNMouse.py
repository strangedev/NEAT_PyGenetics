# from Entities.Creatures import Creature
from Entities.GNFood import GNCorn
from Entities.GNDangers import GNMouseTrap
from Entities.GNCreatures import GNCreature


class GNMouse(GNCreature.GNCreature):

    """docstring for Mouse"""

    def __init__(self):

        super().__init__()

        self._symbol = "M"
        self.food_sources = [GNCorn.GNCorn]
        self.dangers = [GNMouseTrap]
