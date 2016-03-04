from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
import json
import os

class NEATConfig(object):

    def __init__(self):

        self.parameters = dict({})

        self.config_directory = os.path.dirname(__file__)
        self.working_directory = os.path.join(
            self.config_directory,
            "../../"
        )

        self.config_categories = [
            "clustering",
            "selection",
            "decision_making",
            "discarding",
            "breeding",
            "mutating"
        ]

        self.load_config()

        self.load_defaults()

    def load_config(self):

        for category in self.config_categories:

            try:
                self.parameters[category] = os.path.join(
                    self.config_directory,
                    ("./" + category + ".conf")
                )

            except Exception as e:

                print(e, " - loading defaults.")


    def load_defaults(self):

        if not "clustering" in self.parameters.keys():
            self.clustering_parameters = dict(
                {
                    "delta_threshold": 1,
                    "excess_coefficient": 1,
                    "disjoint_coefficient": 1,
                    "weight_difference_coefficient": 1,
                    "max_population": 10,
                    "discarding_percentage": 0.2
                }
            )
            print("defaults for clustering loaded.")

        if not "mutating" in self.parameters.keys():
            self.selection_parameters = dict(
                {
                    "add_edge_probability": 0.5,
                    "new_gene_enabled_probability": 0.7,
                    "perturb_gene_weight_probability": 0.5
                }
            )
            print("defaults for selection loaded.")