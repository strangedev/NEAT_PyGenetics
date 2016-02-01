import Catastrophe
from random import choice


class Lightning(Catastrophe.Catastrophe):

    """docstring for Lightning"""

    def __init__(self, charge=150):
        super().__init__()
        self.max_duration = 1
        self.charge = charge

        # world.move(*choice(world.get_coords()))

    def perform_action(self, world):
        super().perform_action()

        if self.duration > self.max_duration or self.charge == 0:
            world.remove_thing_at_coords(*self._pos)
            return

        victom_location = self._pos

        if self.duration != 1:
            victom_location = choice(world.get_coords())

        world.move(self, *victom_location)

        victoms = world.get_all_neighbors_from_coords(*victom_location)

        self.smite_victoms_from_coords(world, victoms)

    def smite_victoms_from_coords(self, world, victoms):

        for victom, coords in victoms:

            if not victom:
                continue

            world.remove_thing_at_coords(*coords)

            world.add_thing(self.__class__(self.charge // 2), *coords)
