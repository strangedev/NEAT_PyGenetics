from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.GenomeRepository import GenomeRepository
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
import json
import os

class NEATConfig(object):

    def __init__(self):

        self.config_directory = os.path.dirname(__file__)
        self.working_directory = os.path.join(
            self.config_directory,
            "../../"
        )

        self.clustering_parameters = None
        self.selection_parameters = None
        self.decision_making_parameters = None
        self.discarding_parameters = None

        self.clustering_parameters_loaded = False
        self.selection_parameters_loaded = False
        self.decision_making_parameters_loaded = False
        self.discarding_parameters_loaded = False

        self.clustering_parameters_path = os.path.join(
            self.config_directory,
            "./clustering.conf"
        )
        self.selection_parameters_path = os.path.join(
            self.config_directory,
            "./selection.conf"
        )
        self.decision_making_parameters_path = os.path.join(
            self.config_directory,
            "./decision_making.conf"
        )
        self.discarding_parameters_path = os.path.join(
            self.config_directory,
            "./discarding.conf"
        )


        self.load_config()

        if (not self.clustering_parameters_loaded) \
            or (not self.selection_parameters_loaded) \
            or (not self.decision_making_parameters_loaded) \
            or (not self.discarding_parameters_loaded):

            self.load_defaults()

    def load_config(self):

        try:

            cluster_conf_file = open(self.clustering_parameters_path)
            self.clustering_parameters = json.load(cluster_conf_file)
            self.clustering_parameters_loaded = True

        except Exception as e:

            print(e, " - loading defaults.")

        try:

            selection_conf_file = open(self.selection_parameters_path)
            self.selection_parameters = json.load(selection_conf_file)
            self.selection_parameters_loaded = True

        except Exception as e:

            print(e, " - loading defaults.")

        try:

            decision_making_conf_file = open(self.decision_making_parameters_path)
            self.decision_making_parameters = json.load(decision_making_conf_file)
            self.decision_making_parameters_loaded = True

        except Exception as a:

            print(e, " - loading defaults.")

        try:

            discarding_conf_file = open(self.discarding_parameters_path)
            self.discarding_parameters = json.load(discarding_conf_file)
            self.discarding_parameters_loaded = True

        except Exception as e:

            print(e, " - loading defaults.")


    def load_defaults(self):

        if not self.clustering_parameters_loaded:
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
            print("defaults for clustering_parameters loaded.")

        if not self.selection_parameters_loaded:
            self.selection_parameters = dict(
                {
                    "add_edge_probability": 0.5,
                    "new_gene_enabled_probability": 0.7,
                    "perturb_gene_weight_probability": 0.5
                }
            )
            print("defaults for selection_parameters loaded.")
