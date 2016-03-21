"""
Makes decisions lol
"""
import math


class DecisionMaker(object):

    def __init__(self, decision_making_parameters):
        self._decision_making_parameters = decision_making_parameters
        self._time = 0

    def advance_time(self):
        self._time += 1

    def reset_time(self):
        self._time = 0

    @property
    def mutation_percentage(self):
        base_percentage = self._decision_making_parameters["mutation_base_percentage"]
        additional_percentage = self._cutoff_function(
            self._time,
            self._decision_making_parameters["mutation_cutoff_point"]
        )
        return base_percentage + (1 - base_percentage) * additional_percentage

    @property
    def inter_cluster_breeding_time(self):
        return (
            self._time %
            self._decision_making_parameters["inter_cluster_breeding_interval"] == 0
        )

    def _cutoff_function(self, x, cutoff_point):
        return (1 / math.exp(x /
                             self._decision_making_parameters["cutoff_point_scalar"] *
                             math.log(cutoff_point)
                             )
                )
