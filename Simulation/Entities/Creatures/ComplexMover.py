import Thing
from Paths import Path


class ComplexMover(Thing.Thing):

    """docstring for ComplexMover"""

    def __init__(self):

        super().__init__()

        self._symbol = "%"
        self._path = Path.Path()

    def _new_path(self, world):
        pass

    def _on_movement(self, world):

        next_pos = self._path.dispatch_pos()

        if not world.get_thing(*next_pos):
            world.move(self, *next_pos)

    def _on_food_nearby(self, world, food_locations):

        super()._on_food_nearby()
        self._path.calculate_path(*self._pos)

    def perform_action(self, world):

        if not self._path.is_ready():
            self._new_path(world)

        if self._path.target == self._pos:
            self._new_path(world)

        super().perform_action()
