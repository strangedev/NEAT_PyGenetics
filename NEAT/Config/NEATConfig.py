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

        self.error_check()

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

        raise NotImplementedError

    def error_check(self):

        db_connector = DatabaseConnector("error_check_dummy")
        repo = GenomeRepository(db_connector)
        genome = StorageGenome()

        try:

            repo.insert_genome(genome)

        except Exception as e:

            print("An Error occurred while error checking.")
            print("Error checking occurs while NEATConfig is loading the configuration files.")
            print("\n", e)
            print("\nThis usually means MongoDB isn't running.")

            raise e
