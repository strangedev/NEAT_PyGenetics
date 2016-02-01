"""
Thing Module
"""


class Thing(object):

    def __init__(self):
        """
        """
        self.spawn_location = "FREE"
        self._symbol = "T"
        self._pos = (None, None)
        self.age = 0
        self.food_sources = []

    @property
    def symbol(self):
        return self._symbol if self._symbol else "."

    def set_pos(self, pos):
        self._pos = pos

    def perform_action(self):
        """
        """

        self.age += 1

    def find_food_locations(self, world):
        neighbors = world.get_all_neighbors_from_coords(*self._pos)

        food_locations = []

        for neighbor, coord in neighbors:

            if neighbor.__class__ in self.food_sources:
                food_locations.append(coord)

        return food_locations

    def _reproduce(self, world):
        x, y = world.get_random_neighboring_free(*self._pos)

        if x == -1 and y == -1:
            return

        world.add_thing(self.__class__(), x, y)
