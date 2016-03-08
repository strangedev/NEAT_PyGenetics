"""
Makes decisions lol
"""

class DecisionMaker(object):

    def __init__(self, decision_making_parameters):
        self._decision_making_parameters = decision_making_parameters
        self._time = 0

    def advance_time(self):
        self._time += 1

    def reset_time(self):
        self._time = 0

    @property
    def inter_cluster_breeding_time(self):
        return (   
            self._time %
            self._decision_making_parameters["inter_cluster_breeding_interval"]
            == 0
        )

