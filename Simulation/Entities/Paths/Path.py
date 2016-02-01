from Entities.Paths import LinearPathSolver


class Path(object):

    def __init__(self, world):
        self._world = world
        self._target = (-1, -1)
        self._path_solver = LinearPathSolver.LinearPathSolver()
        self._steps = []
        self._step_index = 0

    @property
    def is_ready(self):
        return self._target is not (-1, -1)

    def set_target(self, x, y):

        self._target = (x, y)

    def calculate_path(self, world, x, y):

        self._steps, self._target = self._path_solver.path_from_to(
            (x, y), self._target)

    def dispatch_pos(self):

        next_pos = self._steps[self._step_index]
        self._step_index += 1
        return next_pos
