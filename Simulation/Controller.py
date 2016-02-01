import World
from Entities import Thing
from Entities.GNFood import GNCorn
from Entities.GNDangers import GNMouseTrap
from Entities.GNCreatures import GNMouse
from time import sleep
from random import choice

ENTITY_TYPES = {
    "GNCorn": GNCorn.GNCorn,
    "GNT": GNMouseTrap.GNMouseTrap,
    "GNMouse": GNMouse.GNMouse
}


class Controller(object):

    def __init__(self):

        self.world = None

    def new_world(self, width, height):

        self.world = World.World(width, height)

    def next_cycle(self):

        self.world.compute_life_cycle()

    def animate_cycles(self, cycle_amount, dt=0.1):

        for tick in range(cycle_amount):

            self.next_cycle()
            self.print_map()

            sleep(dt)

    def draw_map(self):

        return self.world.draw_map()

    def spawn_entity(self, entity_type, x, y):

        if entity_type in ENTITY_TYPES.keys():

            entity_class = ENTITY_TYPES[entity_type]

            self.world.add_thing(entity_class(), x, y)

    def spawn_at_random_pos(self, entity_type):

        if entity_type not in ENTITY_TYPES.keys():
            return

        entity = ENTITY_TYPES[entity_type]()

        coords = []

        if entity.spawn_location == "ALL":
            coords = self.world.get_coords()
        else:
            coords = self.world.get_free_coords()

        if coords:

            self.world.add_thing(entity, *choice(coords))

    def spawn_multiple_at_random_pos(self, entity_type, amount):

        for i in range(amount):

            self.spawn_at_random_pos(entity_type)
