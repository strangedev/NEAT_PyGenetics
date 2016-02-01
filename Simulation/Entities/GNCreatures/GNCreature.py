"""
Creature Module
"""
from Entities import Thing
from random import choice


class GNCreature(Thing.Thing):

    """
    """

    def __init__(self):
        """
        """

        super().__init__()

        self.offspring_cycle = 12
        self.max_starving = 7
        self.max_age = 25
        self.starving = 0

    def _on_food_nearby(self, world, food_locations):

        prey_location = choice(food_locations)

        world.move(self, *prey_location)

        self.starving = 0

        return True

    def _on_die_of_age(self, world):
        world.remove_thing_at_coords(*self._pos)
        return True

    def _on_die_of_starvation(self, world):
        world.remove_thing_at_coords(*self._pos)
        return True

    def _on_movement(self, world):

        free_location = world.get_random_neighboring_free(*self._pos)

        if free_location != (-1, -1):
            world.move(self, *free_location)

    def perform_action(self, world):

        super().perform_action()

        if self.age > self.max_age:
            if self._on_die_of_age(world):
                return

        if self.starving > self.max_starving:
            if self._on_die_of_starvation(world):
                return

        if self.age % self.offspring_cycle == 0:
            if self._reproduce(world):
                return

        food_locations = self.find_food_locations(world)

        if food_locations:
            if self._on_food_nearby(world, food_locations):
                return

        if self._on_movement(world):
            return

        self.starving += 1
